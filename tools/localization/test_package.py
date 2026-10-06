"""Package safety regressions using temporary files and mocked Git (no commits).

Run: python -m unittest discover -s tools/localization -p 'test_package.py'
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

# unittest discovery supplies this directory on sys.path, as does direct execution.
import package as builder
import glyphs


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory()
        self.addCleanup(self.sandbox.cleanup)
        self.root = Path(self.sandbox.name) / 'checkout'
        self.root.mkdir()
        self.output = Path(self.sandbox.name) / 'deliverables' / 'localization.zip'
        self.locale = 'Aut_Caesar_Aut_Nihil/languages/cns/ui.csv'
        self.files = {
            self.locale: b'\xef\xbb\xbfui_test|' + '中文'.encode() + b'\n',
            'docs/localization/README.md': b'# Install\n',
            'docs/localization/FONT_OPTIONS.md': b'# Font options\n',
            'docs/localization/coverage.json': b'{"partial": true}\n',
            'LICENSE': b'MIT License\nCopyright (c) 2025 Butters\n',
            'Aut_Caesar_Aut_Nihil/Textures/font.dds': b'PROPRIETARY_FONT_BYTES',
            'Aut_Caesar_Aut_Nihil/mb.fx': b'PROPRIETARY_SHADER_BYTES',
            'Aut_Caesar_Aut_Nihil/Data/font_data.xml': b'<font><character code="20013"/></font>',
        }
        for name, data in self.files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.dirty = b''
        self.changed = [self.locale, 'docs/localization/README.md']
        self.review_patch = b'diff --git a/localization b/localization\n+translated\n'
        self.calls = []

    def git(self, *args):
        self.calls.append(args)
        if args[0] == 'status':
            return self.dirty
        if args[0] == 'merge-base':
            return b''
        if args[0] == 'rev-parse':
            return b'1234567890abcdef1234567890abcdef12345678\n'
        if args[0] == 'show':
            if '--format=%ct' in args:
                return b'1777777777\n'
            # Allow implementations to read committed blob bytes instead of worktree files.
            name = args[-1].split(':', 1)[1]
            return self.files[name]
        if args[0] == 'branch':
            return b'localization/test\n'
        if args[0] == 'ls-files':
            delimiter = '\0' if '-z' in args else '\n'
            return (delimiter.join(sorted(self.files)) + delimiter).encode()
        if args[0] == 'diff':
            if '--name-only' in args:
                delimiter = '\0' if '-z' in args else '\n'
                return (delimiter.join(self.changed) + delimiter).encode()
            return self.review_patch
        raise AssertionError(f'Unexpected Git invocation: {args}')

    def build(self, output=None, validator_error=None):
        with patch.object(builder, 'ROOT', self.root), \
             patch.object(builder, 'git', side_effect=self.git), \
             patch.object(builder, 'font_report', side_effect=lambda **kwargs: glyphs.font_report(self.root, **kwargs)), \
             patch.object(builder.subprocess, 'run', side_effect=validator_error) as validate, \
             patch.object(sys, 'argv', ['package.py', '--output', str(output or self.output)]), \
             contextlib.redirect_stdout(io.StringIO()), \
             contextlib.redirect_stderr(io.StringIO()):
            builder.main()
        return validate

    def test_archive_contents_checksums_and_determinism(self):
        self.build()
        first = self.output.read_bytes()
        with zipfile.ZipFile(self.output) as archive:
            names = set(archive.namelist())
            expected = {
                'Modules/' + self.locale,
                'Documentation/localization/README.md',
                'Documentation/localization/FONT_OPTIONS.md',
                'Documentation/localization/coverage.json',
                'Review/font-coverage.json', 'Review/acan-zh-cn.patch',
                'Review/build.json', 'LICENSE', 'START_HERE.txt', 'SHA256SUMS',
            }
            self.assertEqual(names, expected)
            self.assertEqual(archive.read('Modules/' + self.locale), self.files[self.locale])
            self.assertEqual(archive.read('LICENSE'), self.files['LICENSE'])
            self.assertEqual(archive.read('Review/acan-zh-cn.patch'), self.review_patch)
            manifest = dict(line.split('  ', 1)[::-1] for line in
                            archive.read('SHA256SUMS').decode().splitlines())
            self.assertEqual(set(manifest), names - {'SHA256SUMS'})
            for name, digest in manifest.items():
                self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), digest, name)
            self.assertIsNone(archive.testzip())
            metadata = json.loads(archive.read('Review/build.json'))
            self.assertEqual(metadata['base_commit'], builder.BASE)
            self.assertEqual(metadata['runtime_locale'], 'cns')
            self.assertFalse(metadata['in_game_tested'])
            self.assertFalse(metadata['fonts_included'])
            self.assertFalse(metadata['shaders_included'])
            for info in archive.infolist():
                self.assertFalse(info.filename.startswith('/'))
                self.assertNotIn('..', Path(info.filename).parts)
        second = self.output.with_name('second.zip')
        self.build(second)
        self.assertEqual(first, second.read_bytes())
        self.assertFalse(self.output.with_suffix('.zip.tmp').exists())

    def test_payload_uses_reviewed_commit_bytes(self):
        # Simulate a worktree discrepancy hidden by assume-unchanged/skip-worktree.
        (self.root / self.locale).write_bytes(b'UNREVIEWED_WORKTREE_BYTES')
        (self.root / 'docs/localization/README.md').write_bytes(b'UNREVIEWED_DOCS')
        self.build()
        with zipfile.ZipFile(self.output) as archive:
            self.assertEqual(archive.read('Modules/' + self.locale), self.files[self.locale])
            self.assertEqual(archive.read('Documentation/localization/README.md'),
                             self.files['docs/localization/README.md'])

    def test_dirty_checkout_rejected_before_validation_or_output(self):
        self.dirty = b' M docs/localization/README.md\n'
        with self.assertRaises(SystemExit):
            self.build()
        self.assertFalse(self.output.exists())

    def test_inside_checkout_and_symlink_outputs_rejected(self):
        link = Path(self.sandbox.name) / 'alias'
        link.symlink_to(self.root, target_is_directory=True)
        for output in [self.root, self.root / 'package.zip', link / 'package.zip']:
            with self.subTest(output=output), self.assertRaises(SystemExit):
                self.build(output)
        self.assertEqual(self.calls, [])

    def test_failed_validation_does_not_replace_existing_output(self):
        self.output.parent.mkdir()
        self.output.write_bytes(b'PREVIOUS_VALID_DELIVERY')
        with self.assertRaises(subprocess.CalledProcessError):
            self.build(validator_error=subprocess.CalledProcessError(1, ['check.py']))
        self.assertEqual(self.output.read_bytes(), b'PREVIOUS_VALID_DELIVERY')

    def test_ignored_untracked_text_is_not_packaged_as_reviewed(self):
        unreviewed = self.root / 'Aut_Caesar_Aut_Nihil/languages/cns/ignored.csv'
        unreviewed.write_text('ui_unreviewed|未审阅\n', encoding='utf-8-sig')
        # A clean Git status can coexist with ignored files; either reject or omit.
        try:
            self.build()
        except (SystemExit, ValueError):
            self.assertFalse(self.output.exists())
        else:
            with zipfile.ZipFile(self.output) as archive:
                self.assertNotIn('Modules/Aut_Caesar_Aut_Nihil/languages/cns/ignored.csv',
                                 archive.namelist())

    def test_proprietary_asset_change_cannot_leak_through_review_patch(self):
        self.changed.append('Aut_Caesar_Aut_Nihil/Textures/font.dds')
        self.review_patch += b'GIT binary patch\nPROPRIETARY_FONT_BYTES\n'
        # Text-only distribution must reject such commits before emitting a patch.
        with self.assertRaises((SystemExit, ValueError)):
            self.build()
        self.assertFalse(self.output.exists())

    def test_only_patch_workflow_is_allowed(self):
        self.changed.append('.github/workflows/localization-prerelease.yml')
        self.build()
        self.changed.append('.github/workflows/create-release.yml')
        with self.assertRaises(SystemExit):
            self.build(self.output.with_name('rejected.zip'))


class GlyphTests(unittest.TestCase):
    def test_descriptor_and_translation_values_are_compared_without_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            locale = root / 'Aut_Caesar_Aut_Nihil/languages/cns'
            locale.mkdir(parents=True)
            (locale / 'ui.csv').write_text('ui_略|中文中\nmalformed\n', encoding='utf-8-sig')
            descriptor = root / 'Aut_Caesar_Aut_Nihil/Data/font_data.xml'
            descriptor.parent.mkdir()
            data = b'<font><character code="20013"/><character code="65"/></font>'
            descriptor.write_bytes(data)
            report = glyphs.font_report(root)
            self.assertEqual(report['translated_han_count'], 2)
            self.assertEqual(report['descriptor_glyph_count'], 2)
            self.assertEqual(report['missing_han_codepoints'], ['U+6587'])
            self.assertEqual(report['descriptor_sha256'], hashlib.sha256(data).hexdigest())


    def test_compatibility_and_recent_supplementary_han_are_counted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            locale = root / 'Aut_Caesar_Aut_Nihil/languages/cns'
            locale.mkdir(parents=True)
            (locale / 'ui.csv').write_text('ui_han|\uf900\U00030000\U00031350\n',
                                          encoding='utf-8-sig')
            descriptor = root / 'Aut_Caesar_Aut_Nihil/Data/font_data.xml'
            descriptor.parent.mkdir()
            descriptor.write_text('<font/>')
            report = glyphs.font_report(root)
            self.assertEqual(report['translated_han_count'], 3)
            self.assertEqual(report['missing_han_codepoints'],
                             ['U+F900', 'U+30000', 'U+31350'])


if __name__ == '__main__':
    unittest.main()

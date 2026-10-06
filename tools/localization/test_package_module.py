import unittest
from package_module import archive_path, classify_missing

class LayoutTests(unittest.TestCase):
    def test_upstream_audio_is_a_warning_not_structural_failure(self):
        audit = dict(module_resources={'missing': []}, compiled_tables={'missing': []},
                     unknown_external_sounds=['riot_sound.wav'])
        structural, audio = classify_missing(audit)
        self.assertEqual(structural, [])
        self.assertEqual(audio, ['riot_sound.wav'])
        audit['compiled_tables']['missing'] = ['troops.txt']
        self.assertEqual(classify_missing(audit)[0], ['troops.txt'])
    def test_runtime_layout(self):
        self.assertEqual(archive_path('Aut_Caesar_Aut_Nihil/module.ini'), 'Modules/Aut_Caesar_Aut_Nihil/module.ini')
        self.assertEqual(archive_path('Aut_Caesar_Aut_Nihil/languages/cns/ui.csv'), 'Modules/Aut_Caesar_Aut_Nihil/languages/cns/ui.csv')
    def test_compiler_excluded_not_shader(self):
        self.assertIsNone(archive_path('Aut_Caesar_Aut_Nihil/fxc.exe'))
        self.assertIsNone(archive_path('Aut_Caesar_Aut_Nihil/compile_fx.bat'))
        self.assertIsNotNone(archive_path('Aut_Caesar_Aut_Nihil/mb.fx'))
    def test_reject_escape_and_wrong_tree(self):
        for value in ['../secret','Aut_Caesar_Aut_Nihil/../secret','module_system/compiler.py','/Aut_Caesar_Aut_Nihil/module.ini']:
            with self.assertRaises(ValueError):archive_path(value)

if __name__=='__main__':unittest.main()

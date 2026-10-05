"""Regression tests for the localization parser and validation safety boundary.

Run: python -m unittest discover -s tools/localization -p 'test_*.py'
Only temporary fixtures are written; the mod and its translations are untouched.
"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('localization_check', Path(__file__).with_name('check.py'))
check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check)


class SignaturesTests(unittest.TestCase):
    def test_hex_face_data_is_not_translation_prose(self):
        self.assertEqual(check.classification('000000003d1001c134568644e5a9591600000000001c96b500'), 'hex_data')
        self.assertEqual(check.classification('{reg1?Woman:Man}'), 'text')

    def test_translation_and_reordered_registers_are_allowed(self):
        self.assertEqual(check.signatures('{s1} paid {reg2}.'), check.signatures('支付{reg2}，{s1}。'))

    def test_lost_repeated_register_is_detected(self):
        self.assertNotEqual(check.signatures('{s1} met {s1}'), check.signatures('{s1}会面'))

    def test_printf_newline_and_escapes_are_protected(self):
        source = r'%d %% %s ^^ Hello\n'
        for changed in (r'%s %% %s ^^ Hello\n', r'%d % %s ^^ Hello\n',
                        r'%d %% %s ^ Hello\n', r'%d %% %s ^^ Hello\t'):
            with self.subTest(changed=changed):
                self.assertNotEqual(check.signatures(source), check.signatures(changed))

    def test_register_percent_followed_by_prose_is_literal(self):
        self.assertEqual(check.signatures('{reg49}% from relation, +{reg47}% from skills'),
                         check.signatures('{reg49}%来自关系，+{reg47}%来自技能'))
        self.assertNotEqual(check.signatures('{reg49}% from relation'), check.signatures('{reg49}来自关系'))
        self.assertEqual(check.signatures('5% of the price'), check.signatures('价格的5%'))
        self.assertNotEqual(check.signatures('Value: % f'), check.signatures('值：%d'))

    def test_nonpositional_printf_argument_order_is_protected(self):
        self.assertNotEqual(check.signatures('%s paid %d coins'), check.signatures('%d枚钱币由%s支付'))

    def test_conditional_branch_placeholder_swap_is_detected(self):
        self.assertNotEqual(check.signatures('{reg1?{s1}:{s2}}'),
                            check.signatures('{reg1?{s2}:{s1}}'))

    def test_nested_conditional_translation_is_valid(self):
        # This nesting occurs in the mod's str_rebellion_agree_* strings.
        self.assertEqual(check.signatures('{reg5?you:your {reg3?woman:man} {s45}}'),
                         check.signatures('{reg5?你:你的{reg3?女士:先生}{s45}}'))

    def test_placeholders_cannot_move_between_distinct_conditions(self):
        self.assertNotEqual(check.signatures('{reg1?{s1}:{s2}} {reg2?{s3}:{s4}}'),
                            check.signatures('{reg1?{s3}:{s4}} {reg2?{s1}:{s2}}'))

    def test_gender_branch_register_loss_is_detected(self):
        self.assertNotEqual(check.signatures('{sir {s1}/madam {s2}}'),
                            check.signatures('{先生{s1}/女士}'))

    def test_malformed_source_and_translation_are_rejected(self):
        for source in ('hello {s1', 'hello s1}', '{reg1?{s1}:other'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                check.signatures(source)


class TemporaryProject(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.module = self.root / 'Aut_Caesar_Aut_Nihil'
        self.locale = self.module / 'languages/cns'
        self.docs = self.root / 'docs/localization'
        self.locale.mkdir(parents=True)
        self.docs.mkdir(parents=True)
        for name, value in [('ROOT', self.root), ('MODULE', self.module),
                            ('LOCALE', self.locale), ('DOCS', self.docs)]:
            p = patch.object(check, name, value)
            p.start()
            self.addCleanup(p.stop)

    def write(self, name, value):
        path = self.module / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding='utf-8')

    def fixture(self):
        # Field layouts match compiler.py process_* functions. Operation blocks
        # intentionally have numbers before and after text, including zero args.
        sources = {
            'languages/en/hints.csv': 'hint_1|Read {s1}\n',
            'languages/en/ui.csv': 'ui_ok|OK\n',
            'languages/en/uimain.csv': 'ui_start|Start\n',
            'Data/item_modifiers.txt': 'imod_plain Plain_%s 1.000000 1.000000\nimod_cracked Cracked_%s 0.400000 0.900000\n',
            'strings.txt': 'stringsfile version 1\n1\nstr_label Literal_text\n',
            'quick_strings.txt': '1\nqstr_Case_{s1} Quick_{s1}\n',
            'factions.txt': 'factionsfile version 1\n1\nfac_rome Roman_Empire 0 0\n0\n0\n',
            'troops.txt': 'troopsfile version 2\n1\ntrp_legionary Legionary Legionaries 0 0\n0 1 2\n',
            'item_kinds1.txt': 'itemsfile version 3\n1\nitm_sword Roman_Sword Roman_Swords 0 0\n0\n',
            'party_templates.txt': 'partytemplatesfile version 1\n1\npt_patrol Roman_Patrol 0 0\n',
            'parties.txt': 'partiesfile version 1\n1 1\n1 0 0 p_roma Roma 0 0\n0.0\n',
            'quests.txt': 'questsfile version 1\n1\nqst_delivery Deliver_{s1} 0 Bring_{s2}_to_{s1}.\n',
            'skills.txt': '1\nskl_trade Trade 0 10 Reduces_loss_by_5%%.\n',
            'info_pages.txt': 'infopagesfile version 1\n1\nip_history History Roman_history.\n',
            'conversation.txt': 'dialogsfile version 2\n2\n'
                'dlga_start:end 0 0 2 31 2 1 2 4 0 Hello_{s1} 1 1 2133 2 10 20 NO_VOICEOVER\n'
                'dlga_start:end.1 0 0 0 Goodbye 1 0 NO_VOICEOVER\n',
            'menus.txt': 'menusfile version 1\n1\n'
                'menu_start 0 Start_here none 1 2133 2 1 2 2\n'
                ' mno_continue 1 31 2 0 0 Continue 0 . '
                'mno_continue 0 Continue_again 1 4 0 door_name\n',
            'skins.txt': 'skins_file version 1\n1\n'
                'skinkey_chin_size 1 2 0.0 1.0 Chin_Size skinkey_nose 2 3 0.0 1.0 Nose\n',
        }
        for name, value in sources.items():
            self.write(name, value)

    def row(self, text='你好{s1}', key='str_test'):
        path = self.locale / 'game_strings.csv'
        path.write_text(key + '|' + text + '\n', encoding='utf-8-sig')
        return path

    def groups(self, text='Hello {s1}'):
        return check.grouped([dict(category='game_strings.csv', id='str_test', text=text,
                                   runtime=True, classification='text')])

    def errors(self, text='Hello {s1}'):
        return check.validate(self.groups(text))[0]


class ValidationTests(TemporaryProject):
    def test_valid_translation(self):
        self.row()
        self.assertEqual(self.errors(), [])

    def test_duplicate_id(self):
        path = self.row()
        with path.open('a', encoding='utf-8') as stream:
            stream.write('str_test|您好{s1}\n')
        self.assertTrue(any('duplicate ID' in x for x in self.errors()))

    def test_unknown_id(self):
        self.row(key='str_typo')
        self.assertTrue(any('unknown/unverified ID' in x for x in self.errors()))

    def test_missing_placeholder(self):
        self.row(text='你好')
        self.assertTrue(any('placeholder mismatch' in x for x in self.errors()))

    def test_source_malformed_placeholder_not_silently_repaired(self):
        self.row()
        self.assertTrue(any('unclosed brace' in x for x in self.errors('Hello {s1')))

    def test_branch_selector_changed(self):
        self.row('{reg2?女士:先生}')
        self.assertTrue(any('placeholder mismatch' in x for x in self.errors('{reg1?lady:lord}')))

    def test_delimiter_and_embedded_control_rejected(self):
        for value in ('你好|{s1}', '你好\x00{s1}', '你好\ufeff{s1}'):
            with self.subTest(value=value):
                self.row(value)
                self.assertTrue(any('delimiter/control' in x for x in self.errors()))

    def test_invalid_utf8(self):
        path = self.row()
        path.write_bytes(b'\xef\xbb\xbfstr_test|\xff\n')
        self.assertTrue(any('not UTF-8' in x for x in self.errors()))

    def test_missing_bom(self):
        path = self.row()
        path.write_text('str_test|你好{s1}\n', encoding='utf-8')
        self.assertTrue(any('expected UTF-8 BOM' in x for x in self.errors()))

    def test_nontranslatable_marker(self):
        self.row('{!}内部标记')
        self.assertTrue(any('nontranslatable marker' in x for x in self.errors('{!}internal marker')))

    def test_missing_pinned_id_and_source_drift(self):
        self.fixture()
        (self.locale / 'ui.csv').write_text('ui_ok|确定\n', encoding='utf-8-sig')
        def run(*args):
            with patch('sys.argv', ['check.py', *args]), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                return check.main()
        self.assertFalse(run('--pin'))
        (self.locale / 'ui.csv').unlink()
        report = self.docs / 'report.json'
        self.assertTrue(run('--check', '--report', str(report)))
        self.assertTrue(any('missing 1 milestone IDs' in x for x in json.loads(report.read_text())['errors']))
        self.write('languages/en/ui.csv', 'ui_ok|Changed\n')
        self.assertTrue(run('--check', '--report', str(report)))
        self.assertTrue(any('source drift' in x for x in json.loads(report.read_text())['errors']))


class InventoryTests(TemporaryProject):
    def test_compiler_layouts_ids_and_collisions(self):
        self.fixture()
        records, hashes = check.inventory()
        groups = check.grouped(records)
        self.assertEqual(groups['quick_strings.csv']['qstr_Case_{s1}'][0]['text'], 'Quick {s1}')
        self.assertEqual(groups['dialogs.csv']['dlga_start:end'][0]['text'], 'Hello {s1}')
        self.assertIn('dlga_start:end.1', groups['dialogs.csv'])
        self.assertEqual([x['text'] for x in groups['game_menus.csv']['mno_continue']],
                         ['Continue', 'Continue again'])
        self.assertNotIn('mno_continue.1', groups['game_menus.csv'])
        self.assertEqual(groups['troops.csv']['trp_legionary_pl'][0]['text'], 'Legionaries')
        self.assertEqual(groups['item_kinds.csv']['itm_sword_pl'][0]['text'], 'Roman Swords')
        self.assertEqual(groups['quests.csv']['qst_delivery_text'][0]['text'], 'Bring {s2} to {s1}.')
        self.assertEqual(groups['skills.csv']['skl_trade_desc'][0]['text'], 'Reduces loss by 5%%.')
        self.assertEqual(groups['parties.csv']['p_roma'][0]['text'], 'Roma')
        self.assertEqual(groups['skins.csv']['skinkey_chin_size'][0]['text'], 'Chin Size')
        self.assertEqual(groups['skins.csv']['skinkey_nose'][0]['text'], 'Nose')
        self.assertEqual(groups['info_pages.csv']['ip_history_text'][0]['text'], 'Roman history.')
        self.assertTrue(groups['info_pages.csv']['ip_history_text'][0]['runtime'])
        self.assertEqual(len(groups['item_modifiers.csv']), 2)
        self.assertEqual(groups['item_modifiers.csv']['imod_plain'][0]['text'], 'Plain %s')
        self.assertIn('Data/item_modifiers.txt', hashes)
        self.assertEqual(len(hashes), 17)

    def test_record_count_drift_detected(self):
        self.fixture()
        self.write('strings.txt', 'stringsfile version 1\n2\nstr_label Text\n')
        with self.assertRaisesRegex(ValueError, 'header says 2'):
            check.inventory()

    def test_operation_block_overrun_rejected(self):
        with self.assertRaises((AssertionError, IndexError, ValueError)):
            check.skip_operations(['1', '2133', '4', '1'], 0)

    def test_nonbreaking_space_is_not_an_engine_separator(self):
        self.assertEqual(check.words('str_test Roman\u00a0Empire'), ['str_test', 'Roman\u00a0Empire'])


if __name__ == '__main__':
    unittest.main()

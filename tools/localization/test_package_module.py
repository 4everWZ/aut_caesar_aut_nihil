import unittest
from package_module import archive_path

class LayoutTests(unittest.TestCase):
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

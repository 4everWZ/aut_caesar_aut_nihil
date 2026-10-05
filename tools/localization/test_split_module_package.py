import json, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path

class SplitTests(unittest.TestCase):
    def test_later_volume_keeps_source_offsets(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/'source.zip';out=root/'parts'
            expected={f'Modules/test/{i}.dat':bytes([i])*700000 for i in range(3)}
            with zipfile.ZipFile(source,'w',compression=zipfile.ZIP_DEFLATED) as z:
                for name,data in expected.items():z.writestr(name,data)
            subprocess.run([sys.executable,str(Path(__file__).with_name('split_module_package.py')),str(source),'--output-dir',str(out),'--part-size-mib','1'],check=True,capture_output=True)
            metadata=json.loads((out/'PACKSET.json').read_text());self.assertEqual(len(metadata['parts']),3)
            combined={}
            for part in metadata['parts']:
                with zipfile.ZipFile(out/part['file']) as z:
                    for name in z.namelist():
                        if name!='READ_ALL_PACKS.txt':combined[name]=z.read(name)
            self.assertEqual(combined,expected)

if __name__=='__main__':unittest.main()

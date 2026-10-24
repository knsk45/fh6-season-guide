"""Real offline Git reproduction of rollover assets outside a sparse checkout."""
import subprocess
import tempfile
import unittest
from pathlib import Path


def git(root,*args,check=True):
    return subprocess.run(['git','-C',str(root),*args],check=check,capture_output=True,text=True)


class Tests(unittest.TestCase):
    def test_rollover_assets_are_staged_without_changing_sparse_rules(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);seed=base/'seed';seed.mkdir()
            git(seed,'init','--quiet')
            git(seed,'config','user.name','Fixture');git(seed,'config','user.email','fixture@example.test')
            (seed/'automation').mkdir();(seed/'automation/script.py').write_text('fixture')
            (seed/'reports/assets/summer').mkdir(parents=True)
            (seed/'reports/assets/summer/monthly.png').write_bytes(b'original monthly bytes')
            git(seed,'add','.');git(seed,'commit','--quiet','-m','fixture')
            clone=base/'publisher'
            git(base,'clone','--quiet','--no-local',str(seed),str(clone))
            git(clone,'sparse-checkout','set','automation')
            rules=(clone/'.git/info/sparse-checkout').read_bytes()
            assets=clone/'reports/assets/autumn';assets.mkdir(parents=True)
            for name in ('monthly.png','source.png'):(assets/name).write_bytes(b'original monthly bytes')
            (clone/'private-unrelated.txt').write_text('must not be staged')
            rejected=git(clone,'add','--','reports/assets',check=False)
            self.assertNotEqual(rejected.returncode,0)
            self.assertIn('sparse',rejected.stderr.lower())
            git(clone,'add','--sparse','--','reports/assets')
            staged=git(clone,'diff','--cached','--name-only').stdout.splitlines()
            self.assertEqual(staged,['reports/assets/autumn/monthly.png','reports/assets/autumn/source.png'])
            for name in ('monthly.png','source.png'):
                self.assertEqual(git(clone,'show',':reports/assets/autumn/'+name).stdout,'original monthly bytes')
            self.assertEqual((clone/'.git/info/sparse-checkout').read_bytes(),rules)
            self.assertFalse((clone/'reports/assets/summer/monthly.png').exists())

    def test_publisher_uses_sparse_with_explicit_path_list(self):
        source=(Path(__file__).resolve().parents[1]/'publish_to_github.ps1').read_text(encoding='utf-8-sig')
        self.assertEqual(source.count('git add --sparse -- @PublishPaths'),1)
        self.assertNotIn('git add .',source)
        self.assertNotIn('--force',source)


if __name__=='__main__':unittest.main()

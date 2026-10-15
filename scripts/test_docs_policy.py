"""Exercise documentation enforcement using disposable Git histories, no app data."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER=Path(__file__).with_name('check_docs.py').resolve()

class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.git('init','-q','-b','main')
        self.git('config','user.name','Documentation policy tests')
        self.git('config','user.email','docs-test@example.invalid')
        # Fixtures deliberately test failing historical commits, outside app hooks.
        self.git('config','core.hooksPath',str(self.root/'unused-hooks'))
    def tearDown(self):
        self.temp.cleanup()
    def git(self,*args):
        return subprocess.check_output(['git',*args],cwd=self.root,text=True,stderr=subprocess.DEVNULL).strip()
    def put(self,name,text):
        (self.root/name).write_text(text,encoding='utf-8')
        self.git('add','--',name)
    def commit(self):
        self.git('commit','-q','-m','Synthetic policy fixture')
        return self.git('rev-parse','HEAD')
    def check(self,*args):
        return subprocess.run([sys.executable,str(CHECKER),*args],cwd=self.root,capture_output=True,text=True).returncode
    def test_adoption_staged_commit_range_and_deletion(self):
        self.put('README.md','Legacy setup\n'); legacy=self.commit()
        self.assertEqual(self.check('--commit',legacy),0)
        self.put('DOCUMENTATION.md','# Reference\n\nInitial behavior.\n'); self.put('README.md','Setup with application reference.\n'); baseline=self.commit()
        self.assertEqual(self.check('--commit',baseline),0)
        self.put('README.md','Changed setup\n')
        self.assertEqual(self.check('--staged'),1)
        bad=self.commit()
        self.assertEqual(self.check('--commit',bad),1)
        self.put('DOCUMENTATION.md','# Reference\n\nUpdated setup instructions.\n')
        self.assertEqual(self.check('--staged'),1)
        self.put('README.md','Setup and documentation reviewed.\n')
        self.assertEqual(self.check('--staged'),0)
        good=self.commit()
        self.assertEqual(self.check('--commit',good),0)
        self.assertEqual(self.check('--base',baseline,'--head',good),1)
        self.assertEqual(self.check('--base',bad,'--head',good),0)
        self.git('rm','DOCUMENTATION.md')
        self.assertEqual(self.check('--staged'),1)
        deleted=self.commit()
        self.assertEqual(self.check('--commit',deleted),1)
    def test_whitespace_only_change_rejected(self):
        self.put('DOCUMENTATION.md','# Reference\n\nBehavior.\n'); self.put('README.md','Initial setup.\n'); self.commit()
        self.put('README.md','New code/setup\n')
        self.put('DOCUMENTATION.md','# Reference  \n\nBehavior.\n\n')
        self.assertEqual(self.check('--staged'),1)

if __name__=='__main__':
    unittest.main()

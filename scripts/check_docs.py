"""Require a substantive documentation diff in each new commit after adoption."""
import argparse
import subprocess
import sys

DOC = 'DOCUMENTATION.md'
REQUIRED = (DOC, 'README.md')

def git(*args, check=True):
    return subprocess.run(['git',*args],check=check,capture_output=True,text=True,encoding="utf-8")

def exists(rev):
    return git('cat-file','-e',f'{rev}:{DOC}',check=False).returncode == 0

def resolve(rev):
    return git('rev-parse','--verify','--end-of-options',rev+'^{commit}').stdout.strip()

def check_commit(rev):
    commit=resolve(rev)
    parents=git('rev-list','--parents','-n','1',commit).stdout.split()[1:]
    present=exists(commit)
    if not present:
        # History before adoption is grandfathered. Removing the guide is not.
        return not any(exists(parent) for parent in parents)
    for path in REQUIRED:
        if git('cat-file','-e',f'{commit}:{path}',check=False).returncode:
            return False
        if parents:
            diff=git('diff','--ignore-all-space','--ignore-blank-lines','--numstat',parents[0],commit,'--',path).stdout.strip()
        else:
            diff=git('diff-tree','--root','--no-commit-id','--numstat','-r',commit,'--',path).stdout.strip()
        if not diff:
            return False
    return True

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--staged',action='store_true')
    group.add_argument('--commit')
    group.add_argument('--base')
    parser.add_argument('--head',default='HEAD')
    args=parser.parse_args()
    if args.staged:
        changed=git('diff','--cached','--name-only','--diff-filter=ACDMRT').stdout.splitlines()
        if not changed:
            return 0
        valid=True
        for path in REQUIRED:
            content=git('show',':'+path,check=False)
            substantive=git('diff','--cached','--ignore-all-space','--ignore-blank-lines','--numstat','--',path).stdout.strip()
            valid=valid and path in changed and bool(substantive) and content.returncode==0 and bool(content.stdout.strip())
        if not valid:
            print('Update and stage both DOCUMENTATION.md and README.md with this commit. Review the affected behavior or record its maintenance impact.',file=sys.stderr)
        return 0 if valid else 1
    if args.commit:
        revisions=[resolve(args.commit)]
    else:
        head=resolve(args.head)
        revisions=git('rev-list','--reverse',head if not args.base.strip('0') else resolve(args.base)+'..'+head).stdout.splitlines()
    failed=[rev for rev in revisions if not check_commit(rev)]
    if failed:
        print('Commits missing DOCUMENTATION.md or README.md updates: '+', '.join(failed),file=sys.stderr)
        return 1
    print('Documentation commit policy passed.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())

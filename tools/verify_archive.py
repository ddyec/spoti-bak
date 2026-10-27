#!/usr/bin/env python3
"""Verify archived bytes; optionally reconstruct exact source trees in an isolated Git index."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, tempfile
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('--source-repo',type=Path)
args=p.parse_args()
entries={}
for line in (root/'SHA256SUMS').read_text().splitlines():
    digest,name=line.split('  ',1)
    path=root/name
    assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest, f'Changed/missing: {name}'
    entries[name]=digest
provenance=json.loads((root/'provenance.json').read_text())
for commit in provenance['commits']:
    assert entries[commit['patch']]==commit['sha256']
    raw=(root/commit['raw_commit']).read_bytes()
    assert entries[commit['raw_commit']]==commit['raw_commit_sha256']
    assert hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==commit['sha'], f'Commit object mismatch: {commit["sha"]}'
for snapshot in provenance['snapshots'].values():
    assert snapshot['consolidated_patch'] in entries
    for item in snapshot['files']:
        if item['status']=='deleted':continue
        assert entries[item['archive_path']]==item['sha256']
        actual=os.stat(root/item['archive_path']).st_mode & 0o111
        assert bool(actual)==(item['source_mode']=='100755'), f'Executable mode mismatch: {item["archive_path"]}'
print(f'PASS: {len(entries)} archived files, {len(provenance["commits"])} original commits, all snapshot bytes/modes')
if args.source_repo:
    repo=args.source_repo.resolve()
    def git(*cmd,env=None):return subprocess.check_output(['git',*cmd],cwd=repo,env=env).decode().strip()
    def check(label,base,patches,target_tree):
        with tempfile.TemporaryDirectory(prefix='spoti-archive-index-') as tmp:
            env=os.environ.copy();env['GIT_INDEX_FILE']=str(Path(tmp)/'index')
            git('read-tree',base,env=env)
            for patch in patches:git('apply','--cached','--binary',str(root/patch),env=env)
            assert git('write-tree',env=env)==target_tree, f'Tree mismatch: {label}'
            print(f'PASS: {label}, exact original Git tree ({len(patches)} patch(es))')
    for name,snapshot in provenance['snapshots'].items():
        check('consolidated '+name,snapshot['base'],[snapshot['consolidated_patch']],snapshot['expected_tree'])
    main=[c for c in provenance['commits'] if c['group']=='mainline']
    merge=next(i for i,c in enumerate(main) if len(c['parents'])>1)
    check('initial commit series',provenance['base'],[c['patch'] for c in main[:merge]],provenance['snapshots']['initial-lyrics']['expected_tree'])
    check('beta integration + subsequent commit series',provenance['beta_integration_base'],[c['patch'] for c in main[merge:]],provenance['snapshots']['final']['expected_tree'])
    extra=[c['patch'] for c in provenance['commits'] if c['group']=='parallel-ev1']
    check('parallel EV1 commit series',provenance['base'],extra,provenance['snapshots']['parallel-ev1']['expected_tree'])

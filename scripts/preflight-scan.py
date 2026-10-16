#!/usr/bin/env python3
"""发前安检：扫 evidence 数据集是否含密钥/内网信息模式。"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).parent
pats = {
    'ghp_/gho_ token': r'gh[pousr]_[A-Za-z0-9]{20,}',
    'sk_live/priv key': r'(sk_live_[A-Za-z0-9]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',
    'api key-ish': r'(?i)(api[_-]?key|secret[_-]?key|password)\s*[:=]\s*\S{8,}',
    'aws key': r'AKIA[0-9A-Z]{16}',
    'ipv4 private/internal': r'\b(10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+)\b',
    'bearer': r'(?i)bearer\s+[A-Za-z0-9._-]{20,}',
}
hits = []
for f in ROOT.rglob('*.json'):
    t = f.read_text()
    for name, p in pats.items():
        for m in re.finditer(p, t):
            hits.append((str(f), name, m.group(0)[:60]))
if hits:
    for h in hits: print('LEAK?', *h, sep='\t')
    sys.exit(1)
print('CLEAN: no secret/internal-network patterns in', sum(1 for _ in ROOT.rglob('*.json')), 'json files')

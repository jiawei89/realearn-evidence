#!/usr/bin/env python3
"""发前安检：扫 evidence 数据集全部文本文件是否含密钥/内网信息模式。"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
pats = {
    'ghp_/gho_ token': r'gh[pousr]_[A-Za-z0-9]{20,}',
    'sk_live/priv key': r'(sk_live_[A-Za-z0-9]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',
    'api key-ish': r'(?i)(api[_-]?key|secret[_-]?key|password)\s*[:=]\s*\S{8,}',
    'aws key': r'AKIA[0-9A-Z]{16}',
    'ipv4 private/internal': r'\b(10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2\d|3[01])\.\d+\.\d+)\b',
    'bearer': r'(?i)bearer\s+[A-Za-z0-9._-]{20,}',
}
hits = []
files = [f for f in ROOT.rglob('*') if f.suffix in ('.json', '.md', '.py') and '.git' not in f.parts]
for f in files:
    t = f.read_text()
    for name, p in pats.items():
        for m in re.finditer(p, t):
            hits.append((str(f), name, m.group(0)[:60]))
for h in hits: print('LEAK?', *h, sep='\t')
print(f'{"FAIL" if hits else "CLEAN"}: scanned {len(files)} files')
sys.exit(1 if hits else 0)

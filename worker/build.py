#!/usr/bin/env python3
"""Builds worker/worker.js (and a test copy) from worker.src.js plus the shared logic in ../index.html."""
import re, sys, pathlib
here = pathlib.Path(__file__).parent
html = (here.parent / 'index.html').read_text(encoding='utf-8')

def block_cw():
    a = html.index('const CW=(function(){')
    b = html.index('\n})();', a) + len('\n})();')
    return html[a:b]

def grab_const(name):
    m = re.search(r'^const %s=.*;$' % re.escape(name), html, re.M)
    if not m: sys.exit('missing const ' + name)
    return m.group(0)

def grab_fn(name):
    a = html.index('function %s(' % name)
    i = html.index('{', html.index(')', a))
    depth, q = 0, None
    while True:
        c = html[i]
        if q:
            if c == '\\': i += 1
            elif c == q: q = None
        elif c in '\'"`': q = c
        elif c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: return html[a:i+1]
        i += 1

parts = [block_cw(), 'const LG=CW.LEAGUES;']
for n in ['isTk','legsOf','ticketTitle','teamOf','FB','LEGW','gamesOf','scoreText','sameState']: parts.append(grab_const(n))
for n in ['pickTitle','deadText','stateOf','scoreLabel','scorePhrase','scoredFor','describeChange']: parts.append(grab_fn(n))
shared = '\n'.join(parts)
src = (here / 'worker.src.js').read_text(encoding='utf-8')
out = src.replace('/*@@SHARED@@*/', shared).replace('const LG=CW.LEAGUES;\nconst SITE', 'const SITE')
(here / 'worker.js').write_text(out, encoding='utf-8')
(here / 'worker.test.mjs').write_text(out + '\nexport {detect,encryptPush,vapidAuth,tick,pickGames,cleanBet,mkItem,messagesFor,handle,getVapid,CW};\n', encoding='utf-8')
print('worker.js', len(out), 'bytes')

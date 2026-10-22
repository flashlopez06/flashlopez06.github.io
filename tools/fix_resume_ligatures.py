"""Make the resume PDF readable by hiring software (ATS).

Pages (Apple's word processor) draws letter pairs like "fl", "tf", "ti" as one
joined glyph (a ligature). Most resume parsers drop those, so the email reads
"michael@ashlopez.dev". This swaps each ligature for its plain letters, same
font, squeezed to the same width, so the page looks identical.

Usage: python3 tools/fix_resume_ligatures.py IN.pdf OUT.pdf
Check: pdftotext OUT.pdf - | head -3   (must show michael@flashlopez.dev)
"""
import pymupdf,re,sys
src,dst=sys.argv[1],sys.argv[2]
d=pymupdf.open(src)
def cmap(fx):
    o=d.xref_object(fx); m=re.search(r'/ToUnicode (\d+) 0 R',o)
    s=d.xref_stream(int(m.group(1))).decode('latin1'); M={}
    for a,b,u in re.findall(r'<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>',s):
        for k in range(int(a,16),int(b,16)+1):
            hexu=u; v=int(hexu,16)+k-int(a,16)
            M[k]=bytes.fromhex('%0*x'%(len(hexu),v)).decode('utf-16-be')
    return M
ESC={'n':10,'r':13,'t':9,'b':8,'f':12}
def lit(s):
    out=bytearray();i=0
    while i<len(s):
        ch=s[i]
        if ch=='\\':
            n=s[i+1]
            if n in ESC: out.append(ESC[n]);i+=2
            elif n.isdigit():
                m=re.match(r'[0-7]{1,3}',s[i+1:]).group(0);out.append(int(m,8)&255);i+=1+len(m)
            elif n in '\r\n': i+=2
            else: out.append(ord(n));i+=2
        else: out.append(ord(ch));i+=1
    return bytes(out)
def esc(bs): return '('+''.join(chr(b) if 32<=b<127 and chr(b) not in '()\\' else '\\%03o'%b for b in bs)+')'
n=0
for p in d:
    fonts={f[4]:f[0] for f in p.get_fonts()}
    info={}
    for name,fx in fonts.items():
        o=d.xref_object(fx); fc=int(re.search(r'/FirstChar (\d+)',o).group(1))
        W=[float(x) for x in re.search(r'/Widths \[([^\]]*)\]',o).group(1).split()]
        info[name]=(fc,W,{v:k for k,v in cmap(fx).items() if len(v)==1})
    for cx in p.get_contents():
        c=d.xref_stream(cx).decode('latin1')
        def rep(m):
            global n
            at=lit(m.group(1)); txt=at[2:].decode('utf-16-be') if at[:2]==b'\xfe\xff' else at.decode('latin1')
            body=m.group(2)
            if txt.isspace(): return m.group(0)
            t=re.fullmatch(r'(.*?/(\S+)\s+([\d.]+)\s+Tf\s*)(\((?:\\.|[^\\)])*\)|<[0-9a-fA-F]+>)(\s*Tj.*)',body,re.S)
            assert t,body
            pre,f,_,s,post=t.groups()
            g=lit(s[1:-1]) if s[0]=='(' else bytes.fromhex(s[1:-1]); assert len(g)==1
            fc,W,inv=info[f]; parts=bytes(inv[ch] for ch in txt)
            scale=100*W[g[0]-fc]/sum(W[b-fc] for b in parts)
            n+=1
            return pre+'%.3f Tz '%scale+esc(parts)+post
        c2=re.sub(r'/Span\s*<<\s*/ActualText\s*\(((?:\\.|[^\\)])*)\)\s*>>\s*BDC(.*?)EMC',rep,c,flags=re.S)
        d.update_stream(cx,c2.encode('latin1'))
print('replaced',n)
d.save(dst,garbage=0,deflate=True)

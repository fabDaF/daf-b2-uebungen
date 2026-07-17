"""V3-Gerüst für breitenfüllende Stil-C-Banner (Banner-Rework 2026-07).
Jedes Banner: heller Himmel + Bernstein-Sonne + gestaffelte Uferhügel, die die
Flanken füllen + mittlere Wellenbahn + Front-Welle. Der zentrale Motiv-Inhalt
wird als SVG-Fragment übergeben und soll x in [180,1020] füllen.
Palette-Regel: die Sonne ist EIN Bernstein-Akzent; das Motiv darf EINEN weiteren
goldenen Akzent tragen (Franks V3-Freigabe 2026-07)."""
P={'sky':'#EEEDFE','w1':'#CECBF6','w2':'#AFA9EC','w3':'#7F77DD','w4':'#534AB7','w5':'#3C3489','w6':'#26215C','amber':'#f3c46a'}
def head(alt): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 200" role="img" aria-label="{alt}">'
def birds(x,y,c=P['w4']):
    return (f'<path d="M{x},{y} q7,-7 14,0" stroke="{c}" stroke-width="2.6" fill="none"/>'
            f'<path d="M{x+16},{y+3} q7,-7 14,0" stroke="{c}" stroke-width="2.6" fill="none"/>')
def moon(x=980,y=58): return f'<path d="M{x},{y-18} a18,18 0 1,0 8,34 a14,14 0 1,1 -8,-34 z" fill="{P["w2"]}"/>'
def scaffold_open(sun_x=195,sun_y=60,sun=True):
    """Hintergrund bis vor das Motiv. Danach Motiv einfügen, dann scaffold_close()."""
    s=[f'<rect width="1200" height="200" fill="{P["sky"]}"/>']
    if sun: s.append(f'<circle cx="{sun_x}" cy="{sun_y}" r="24" fill="{P["amber"]}"/>')
    # Uferhügel füllen BEIDE Flanken, überlappen mittig (keine Lücke)
    s.append(f'<path d="M0,132 C130,104 270,100 400,120 C470,131 560,128 680,128 L680,200 H0 Z" fill="{P["w1"]}"/>')
    s.append(f'<path d="M1200,132 C1070,104 930,100 800,120 C730,131 620,128 520,128 L520,200 H1200 Z" fill="{P["w1"]}"/>')
    s.append(f'<path d="M0,158 C300,144 600,166 900,156 C1050,151 1150,160 1200,156 L1200,200 H0 Z" fill="{P["w3"]}"/>')
    return "".join(s)
def scaffold_close():
    return f'<path d="M0,180 C300,170 600,188 900,178 C1050,173 1150,182 1200,178 L1200,200 H0 Z" fill="{P["w6"]}"/></svg>'
def banner(alt, motif, sun_x=195, sun=True, extra_bg=""):
    return head(alt)+scaffold_open(sun_x=sun_x,sun=sun)+extra_bg+motif+scaffold_close()

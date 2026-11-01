# Gera oficina/como-fazer-um-terco.html; o PDF faz-se com o Chrome (--print-to-pdf)
# Tutorial ilustrado das Sete Rosas: os nós e como se faz uma dezena e um terço, passo a passo, para crianças
import math

BG = '#fffdf9'
CORD, CORD_HI, CORD_LINE = '#c9a26a', '#ecd3a2', '#8a6a3f'
CORD_B = '#8f6a4a'           # a segunda ponta, pintada mais escura para se ver qual é qual
AVE, AVE_LINE = '#f3dcb0', '#a8875a'
PAI, PAI_LINE = '#9b4f2b', '#6b3419'
OURO, OURO_LINE = '#d6b26e', '#9a7843'
ROSA = '#c7577a'
NO = '#5e4630'

def corda(d, cor=CORD, largura=6):
    """Um bocado de cordel. O que se desenha depois passa por cima, com uma folga da cor do fundo."""
    return (f'<path d="{d}" fill="none" stroke="{BG}" stroke-width="{largura+6}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{CORD_LINE if cor == CORD else "#5a3f29"}" stroke-width="{largura+1.6}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="{largura}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{CORD_HI if cor == CORD else "#b08a68"}" stroke-width="1.4" stroke-linecap="round" opacity=".8"/>')

def seta(d, texto=None, tx=0, ty=0, tracejado=True):
    s = f'<path d="{d}" fill="none" stroke="{ROSA}" stroke-width="2.2" {"stroke-dasharray=\"5 4\"" if tracejado else ""} marker-end="url(#ponta)" stroke-linecap="round"/>'
    if texto:
        s += f'<text x="{tx}" y="{ty}" class="et" fill="{ROSA}">{texto}</text>'
    return s

def rotulo(x, y, t, ancora='middle'):
    return f'<text x="{x}" y="{y}" class="et" text-anchor="{ancora}">{t}</text>'

def conta_lado(x, y, cor=AVE, linha=AVE_LINE, w=22, h=18, rot=0):
    """Uma conta pony vista de lado, enfiada no cordel."""
    return (f'<g transform="translate({x},{y}) rotate({rot})"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="6" fill="{cor}" stroke="{linha}" stroke-width="1.4"/>'
            f'<rect x="{-w/2+3}" y="{-h/2+3}" width="{w*0.35}" height="3" rx="1.5" fill="#fff" opacity=".55"/></g>')

def svg(w, h, corpo, rotulo_acess):
    defs = (f'<defs><marker id="ponta" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{ROSA}"/></marker></defs>')
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{rotulo_acess}">{defs}{corpo}</svg>'

# ---------- os nós ----------
VOLTA_A = 'M18,96 L100,96 C142,96 150,44 118,38 C88,32 80,58 88,78'
VOLTA_B = 'M88,78 C93,90 100,104 108,114 L124,134'

def volta():
    return corda(VOLTA_A) + corda(VOLTA_B)

def no_feito(x, y, duplo=False, comp=(18, 222)):
    """Um nó apertado no meio do cordel, visto de frente."""
    a, b = comp
    s = corda(f'M{a},{y} L{x-8},{y}')
    s += corda(f'M{x+8},{y} L{b},{y}')
    n = 2 if duplo else 1
    for i in range(n):
        cx = x + (i - (n - 1) / 2) * 13
        s += (f'<ellipse cx="{cx}" cy="{y}" rx="11" ry="10" fill="{CORD}" stroke="{CORD_LINE}" stroke-width="1.6"/>'
              f'<path d="M{cx-6},{y+4} C{cx-2},{y-6} {cx+2},{y-6} {cx+6},{y+4}" fill="none" stroke="{CORD_LINE}" stroke-width="1.4"/>'
              f'<path d="M{cx-6},{y-3} C{cx-1},{y+5} {cx+3},{y+5} {cx+7},{y-2}" fill="none" stroke="{CORD_LINE}" stroke-width="1.2" opacity=".7"/>')
    return s

def puxa(y):
    return seta(f'M60,{y+22} L22,{y+22}', tracejado=False) + seta(f'M180,{y+22} L218,{y+22}', tracejado=False) + rotulo(120, y + 27, 'puxa as duas pontas')

NOS = []

NOS.append(dict(id='simples', nome='O nó simples',
  para='É o nó de todos os dias. Serve para separar as contas e para segurar a cruz.',
  passos=[
    ('Faz uma volta com a ponta do cordel, como uma argola.', volta() + rotulo(150, 26, 'a volta') + rotulo(132, 146, 'a ponta')),
    ('Passa a ponta por trás e depois por dentro da argola.', volta() + seta('M124,134 C160,128 158,92 132,78 C122,72 114,68 108,62')),
    ('Puxa as duas pontas devagar até o nó ficar pequenino.', no_feito(120, 80) + puxa(80)),
  ]))

NOS.append(dict(id='duplo', nome='O nó duplo',
  para='Usa este quando o nó simples é pequeno e passa pelo furo da conta. Fica mais gordo.',
  passos=[
    ('Faz a volta, igual ao nó simples.', volta()),
    ('Passa a ponta por dentro da argola uma vez, e depois outra vez.',
       volta() + seta('M124,134 C160,128 158,92 132,78 C122,72 114,68 108,62', '1', 150, 128)
               + seta('M124,134 C176,126 176,80 140,66 C128,60 118,58 112,52', '2', 182, 86)),
    ('Puxa as duas pontas. O nó fica com duas voltas, mais grosso.', no_feito(120, 80, duplo=True) + puxa(80)),
  ]))

OITO_1 = 'M18,104 L96,104 C130,104 140,60 112,52 C86,46 76,74 90,92'
OITO_2 = 'M90,92 C98,104 104,116 112,126 L120,140'
NOS.append(dict(id='oito', nome='O nó em oito',
  para='Ainda mais gordo e não escorrega. Bom para o cordel fino.',
  passos=[
    ('Faz uma volta, como no nó simples.', corda(OITO_1) + corda(OITO_2)),
    ('Passa a ponta por trás do cordel comprido.', corda(OITO_1) + corda(OITO_2)
        + seta('M120,140 C150,146 168,128 160,112 C154,100 140,96 128,98', 'por trás', 172, 132)),
    ('Agora enfia a ponta na argola, pela frente.', corda(OITO_1) + corda(OITO_2)
        + seta('M128,98 C118,92 112,82 110,72', 'pela frente', 132, 40)),
    ('Puxa. O nó fica com a forma de um 8 deitado.',
        corda('M18,80 L84,80') + corda('M152,80 L222,80')
        + corda('M84,80 C92,62 116,62 118,80') + corda('M118,80 C120,98 146,98 152,80')
        + corda('M118,80 C116,62 142,60 152,80') + corda('M84,80 C92,98 116,100 118,80') + puxa(80)),
  ]))

def pontas(cruzado=False):
    """As duas pontas do terço a sair das contas, uma de cada cor."""
    if not cruzado:
        return corda('M80,142 C80,110 96,90 120,74') + corda('M160,142 C160,110 144,90 120,74', CORD_B)
    return ''

NOS.append(dict(id='direito', nome='O nó direito',
  para='Serve para atar duas pontas uma à outra, no fim do terço. Pintámos uma ponta mais escura para se ver qual é qual.',
  passos=[
    ('Cruza a ponta da direita por cima da ponta da esquerda.',
        corda('M80,142 C80,100 120,80 160,36') + corda('M160,142 C160,100 120,80 80,36', CORD_B)
        + rotulo(64, 30, 'esquerda') + rotulo(178, 30, 'direita')),
    ('Dá-lhe uma volta por baixo e puxa: fica a primeira meia-volta.',
        corda('M80,142 C80,104 104,92 120,86 C136,80 150,66 156,34')
        + corda('M160,142 C160,104 128,82 112,80 C96,78 90,96 104,100 C116,104 108,60 86,34', CORD_B)),
    ('Agora ao contrário: a da esquerda por cima da da direita, e outra volta.',
        corda('M80,142 C80,110 104,98 120,96 C136,94 150,80 150,64 C150,48 120,44 90,30')
        + corda('M160,142 C160,110 136,98 120,96 C104,94 90,80 90,64 C90,48 120,44 150,30', CORD_B)
        + seta('M150,30 C170,40 172,58 160,66', None)),
    ('Puxa as quatro pontas. O nó fica deitado e direitinho.',
        corda('M80,142 C80,116 96,104 108,98') + corda('M160,142 C160,116 144,104 132,98', CORD_B)
        + corda('M108,98 C100,90 100,78 112,74 C124,70 140,76 132,90 C128,98 116,100 108,98')
        + corda('M132,98 C140,88 140,74 128,72 C114,70 100,80 108,92', CORD_B)
        + corda('M112,74 C108,60 98,48 86,36') + corda('M128,72 C134,58 144,48 156,36', CORD_B)
        + seta('M86,36 L70,22', tracejado=False) + seta('M156,36 L172,22', tracejado=False)),
  ]))

NOS.append(dict(id='cirurgiao', nome='O nó de cirurgião',
  para='É o nó direito com uma volta a mais. Segura melhor e não se desmancha.',
  passos=[
    ('Cruza a da direita por cima da da esquerda e dá duas voltas em vez de uma.',
        corda('M80,142 C80,104 104,92 120,86 C136,80 150,66 156,34')
        + corda('M160,142 C160,104 128,82 112,80 C96,78 90,96 104,100 C116,104 132,96 126,84 C120,74 100,78 104,90 C108,100 110,60 86,34', CORD_B)
        + rotulo(176, 112, '2 voltas')),
    ('Depois a da esquerda por cima da da direita, com uma volta só, como no nó direito.',
        corda('M80,142 C80,110 104,98 120,96 C136,94 150,80 150,64 C150,48 120,44 90,30')
        + corda('M160,142 C160,110 136,98 120,96 C104,94 90,80 90,64 C90,48 120,44 150,30', CORD_B)),
    ('Puxa as quatro pontas com força.',
        corda('M80,142 C80,116 96,104 108,98') + corda('M160,142 C160,116 144,104 132,98', CORD_B)
        + corda('M108,98 C98,88 98,72 112,70 C126,68 142,74 132,92 C128,100 114,102 108,98')
        + corda('M132,98 C142,86 142,70 128,68 C112,66 98,78 108,94', CORD_B)
        + corda('M104,86 C112,80 128,80 136,86')
        + corda('M112,70 C108,58 98,48 86,36') + corda('M128,68 C134,56 144,48 156,36', CORD_B)
        + seta('M86,36 L70,22', tracejado=False) + seta('M156,36 L172,22', tracejado=False)),
  ]))

ALFINETE = [
  ('Faz o nó solto, sem apertar, perto da conta.',
     corda('M18,90 L222,90') + conta_lado(170, 90) + '<circle cx="118" cy="82" r="14" fill="none" stroke="' + CORD_LINE + '" stroke-width="6.5"/>'
     + '<circle cx="118" cy="82" r="14" fill="none" stroke="' + CORD + '" stroke-width="5"/>' + rotulo(118, 56, 'nó solto') + rotulo(170, 122, 'a conta')),
  ('Enfia um alfinete dentro do nó e empurra-o até encostar à conta.',
     corda('M18,90 L222,90') + conta_lado(170, 90) + '<circle cx="146" cy="84" r="9" fill="none" stroke="' + CORD_LINE + '" stroke-width="6.5"/>'
     + '<circle cx="146" cy="84" r="9" fill="none" stroke="' + CORD + '" stroke-width="5"/>'
     + '<line x1="146" y1="84" x2="96" y2="30" stroke="#8d8d94" stroke-width="2.4" stroke-linecap="round"/><circle cx="94" cy="28" r="5" fill="' + ROSA + '"/>'
     + seta('M96,116 L136,116', 'empurra', 116, 136, tracejado=False)),
  ('Puxa as pontas e só no fim tiras o alfinete. O nó fica mesmo encostado.',
     corda('M18,90 L222,90') + conta_lado(172, 90) + '<ellipse cx="152" cy="90" rx="8" ry="8" fill="' + CORD + '" stroke="' + CORD_LINE + '" stroke-width="1.6"/>'
     + rotulo(150, 122, 'nó encostado')),
]

# ---------- o terço e a dezena ----------
def cruz(x, y, h=40, novo=False):
    w = h * 0.62
    s = (f'<path d="M{x},{y} V{y+h} M{x-w/2},{y+h*0.3} H{x+w/2}" stroke="{OURO_LINE}" stroke-width="9" stroke-linecap="round"/>'
         f'<path d="M{x},{y} V{y+h} M{x-w/2},{y+h*0.3} H{x+w/2}" stroke="{OURO}" stroke-width="6.4" stroke-linecap="round"/>')
    if novo:
        s = f'<rect x="{x-w/2-7}" y="{y-7}" width="{w+14}" height="{h+14}" rx="10" fill="none" stroke="{ROSA}" stroke-width="2" stroke-dasharray="4 3"/>' + s
    return s

def medalha(x, y, novo=False):
    s = ''.join(f'<circle cx="{a}" cy="{b}" r="3.4" fill="none" stroke="{OURO_LINE}" stroke-width="1.8"/>'
                for a, b in ((x - 8, y - 14), (x + 8, y - 14), (x, y + 16)))
    s += f'<ellipse cx="{x}" cy="{y}" rx="11" ry="13.5" fill="{OURO}" stroke="{OURO_LINE}" stroke-width="1.6"/>'
    s += f'<text x="{x}" y="{y+4.5}" font-size="12" text-anchor="middle" fill="{OURO_LINE}" font-family="IM Fell English, Georgia, serif">M</text>'
    if novo:
        s = f'<ellipse cx="{x}" cy="{y}" rx="20" ry="24" fill="none" stroke="{ROSA}" stroke-width="2" stroke-dasharray="4 3"/>' + s
    return s

def peca(x, y, t, estado):
    """estado: 'feito', 'novo' ou 'falta' (desenhado a tracejado, para se ver onde vai)."""
    if t == 'k':
        if estado == 'falta':
            return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="none" stroke="#d9c39b" stroke-width="1"/>'
        s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{NO}"/>'
        if estado == 'novo':
            s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="none" stroke="{ROSA}" stroke-width="1.8"/>' + s
        return s
    cor, linha = (PAI, PAI_LINE) if t == 'P' else (AVE, AVE_LINE)
    if estado == 'falta':
        return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.6" fill="none" stroke="#d9c39b" stroke-width="1.1" stroke-dasharray="2 2"/>'
    s = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.8" fill="{cor}" stroke="{linha}" stroke-width="1.2"/>'
         f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{BG}" stroke="{linha}" stroke-width=".6"/>')
    if estado == 'novo':
        s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9.5" fill="none" stroke="{ROSA}" stroke-width="1.8"/>' + s
    return s

def planta(pendente, roda, cx, cy, R, my, cruz_y, passo=0.0):
    """Posições de todas as peças: o pendente sobe da cruz para a medalha; a roda vai da medalha para a esquerda, à volta, e volta à medalha pela direita."""
    pos = [('cruz', 150, cruz_y)]
    y = cruz_y - 9
    for t in pendente:
        y -= 5 if t == 'k' else 6.5
        pos.append((t, 150, y))
        y -= 5 if t == 'k' else 6.5
    pos.append(('medalha', 150, my))
    tam = [7 if t == 'k' else 12.6 for t in roda]
    ini, fim = 90 + 13, 90 + 347
    total = sum(tam)
    acc = 0
    for t, l in zip(roda, tam):
        a = math.radians(ini + (fim - ini) * (acc + l / 2) / total)
        pos.append((t, cx + R * math.cos(a), cy + R * math.sin(a)))
        acc += l
    pos.append(('fecha', 150, my))
    return pos

def desenho(pos, feito, novos, cx, cy, R, my, vb, fechado=False):
    """feito: quantas peças já estão; novos: quantas destas foram postas neste passo."""
    s = []
    # o cordel: a tracejado onde ainda falta, cheio onde já está
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#e6d6b8" stroke-width="1.4" stroke-dasharray="3 4"/>')
    s.append(f'<line x1="150" y1="{my+16}" x2="150" y2="{pos[0][2]}" stroke="#e6d6b8" stroke-width="1.4" stroke-dasharray="3 4"/>')
    pts = [(x, y) for t, x, y in pos[:feito] if t not in ('fecha',)]
    if len(pts) > 1:
        d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        if fechado:
            d += f' L{150+9},{my-14}'
        s.append(f'<path d="{d}" fill="none" stroke="{CORD}" stroke-width="2.2" stroke-linejoin="round"/>')
    for i, (t, x, y) in enumerate(pos):
        if t == 'fecha':
            continue
        estado = 'falta' if i >= feito else ('novo' if i >= feito - novos else 'feito')
        if t == 'cruz':
            s.append(cruz(x, y, 34, estado == 'novo') if estado != 'falta' else f'<path d="M{x},{y} V{y+34} M{x-10},{y+10} H{x+10}" stroke="#d9c39b" stroke-width="1.6" stroke-dasharray="3 3"/>')
        elif t == 'medalha':
            s.append(medalha(x, y, estado == 'novo') if estado != 'falta' else f'<ellipse cx="{x}" cy="{y}" rx="11" ry="13.5" fill="none" stroke="#d9c39b" stroke-width="1.4" stroke-dasharray="3 3"/>')
        else:
            s.append(peca(x, y, t, estado))
    return svg(vb[0], vb[1], ''.join(s), 'Terço a meio')

DEZ = ['A'] * 10
# o terço: cruz, Pai-Nosso, três Ave-Marias, Pai-Nosso, medalha, e na roda as cinco dezenas com os Pai-Nossos pelo meio
T_PEND = ['k', 'P', 'k', 'A', 'A', 'A', 'k', 'P', 'k']
T_RODA = ['k'] + DEZ + ['k', 'P', 'k'] + DEZ + ['k', 'P', 'k'] + DEZ + ['k', 'P', 'k'] + DEZ + ['k', 'P', 'k'] + DEZ + ['k']
T = dict(cx=150, cy=168, R=128, my=300, cruz_y=430, vb=(300, 476))
TPOS = planta(T_PEND, T_RODA, T['cx'], T['cy'], T['R'], T['my'], T['cruz_y'])
assert sum(1 for t in T_PEND + T_RODA if t == 'P') == 6 and sum(1 for t in T_PEND + T_RODA if t == 'A') == 53

# a dezena de bolso: cruz, Pai-Nosso, medalha, e uma roda de dez Ave-Marias
D_PEND = ['k', 'P', 'k']
D_RODA = ['k'] + DEZ + ['k']
D = dict(cx=150, cy=92, R=40, my=140, cruz_y=196, vb=(300, 240))
DPOS = planta(D_PEND, D_RODA, D['cx'], D['cy'], D['R'], D['my'], D['cruz_y'])

def passos(pos, cfg, lista):
    """lista de (texto, até que peça, quantas são novas)."""
    out, ate = [], 0
    for texto, n, *fech in lista:
        novos = n - ate
        out.append((texto, desenho(pos, n, novos, cfg['cx'], cfg['cy'], cfg['R'], cfg['my'], cfg['vb'], fechado=bool(fech))))
        ate = n
    return out

# índices: 0 cruz; pendente; medalha; roda
def idx_terco():
    p = 1 + len(T_PEND)  # depois do pendente vem a medalha
    return p
MED_T = 1 + len(T_PEND)
r0 = MED_T + 1
seg = lambda k: r0 + 1 + k * 13  # início de cada dezena na roda (k=0..4)
TERCO_PASSOS = passos(TPOS, T, [
  ('Ata a cruz na ponta do cordel com um <b>nó duplo</b>. Deixa um bocadinho de ponta, do tamanho de um dedo.', 1),
  ('Dá um nó encostado à cruz, enfia <b>uma conta de Pai-Nosso</b> e dá outro nó por cima.', 4),
  ('Enfia <b>três contas de Ave-Maria</b>, uma a seguir à outra, e dá um nó.', 8),
  ('Enfia <b>uma conta de Pai-Nosso</b> e dá um nó. É o Pai-Nosso da primeira dezena.', 10),
  ('Passa o cordel pela <b>medalha</b>: entra pela argola de baixo e sai pela argola de cima, do lado esquerdo.', MED_T + 1),
  ('<b>Primeira dezena:</b> um nó, dez contas de Ave-Maria (conta-as pelos dedos), e um nó.', seg(0) + 11),
  ('Enfia <b>uma conta de Pai-Nosso</b>, dá um nó, e faz a <b>segunda dezena</b>: dez contas de Ave-Maria e um nó.', seg(1) + 11),
  ('Igual para a <b>terceira dezena</b>: Pai-Nosso, nó, dez Ave-Marias, nó.', seg(2) + 11),
  ('Igual para a <b>quarta dezena</b>.', seg(3) + 11),
  ('E a <b>quinta dezena</b>: Pai-Nosso, nó, dez Ave-Marias e um nó.', seg(4) + 11),
  ('Para fechar, passa a ponta pela argola de cima da medalha, do lado direito, e dá um <b>nó duplo</b> bem apertado. Pede a um adulto para cortar e queimar a ponta.', len(TPOS) - 1, True),
])

MED_D = 1 + len(D_PEND)
DEZENA_PASSOS = passos(DPOS, D, [
  ('Ata a cruz na ponta do cordel com um <b>nó duplo</b>.', 1),
  ('Um nó, <b>uma conta de Pai-Nosso</b>, outro nó.', 4),
  ('Passa o cordel pela <b>medalha</b>: entra pela argola de baixo e sai pela de cima, à esquerda.', MED_D + 1),
  ('Um nó e <b>dez contas de Ave-Maria</b>. Conta-as pelos dedos!', MED_D + 1 + 11),
  ('Um nó, passa a ponta pela argola de cima, à direita, e fecha com um <b>nó duplo</b>.', len(DPOS) - 1, True),
])

def final(pos, cfg, etiquetas):
    corpo = desenho(pos, len(pos) - 1, 0, cfg['cx'], cfg['cy'], cfg['R'], cfg['my'], cfg['vb'], fechado=True)
    extra = ''.join(rotulo(x, y, t, a) for x, y, t, a in etiquetas)
    return corpo.replace('</svg>', extra + '</svg>')

def ang(cfg, frac):
    a = math.radians(90 + 13 + 334 * frac)
    return cfg['cx'] + (cfg['R'] + 22) * math.cos(a), cfg['cy'] + (cfg['R'] + 22) * math.sin(a)

py = lambda i: TPOS[i][2]
et_t = [(174, py(0) + 16, 'a cruz', 'start'), (166, py(2) + 4, 'Pai-Nosso', 'start'), (166, py(5) + 4, '3 Ave-Marias', 'start'),
        (166, py(8) + 4, 'Pai-Nosso', 'start'), (172, py(10) + 4, 'a medalha', 'start')]
for k in range(5):
    i = r0 + 1 + 13 * k + 5          # a conta do meio de cada dezena
    _, x, y = TPOS[i]
    x, y = T["cx"] + (x - T["cx"]) * 0.7, T["cy"] + (y - T["cy"]) * 0.7
    et_t.append((x, y + 4, f'Dezena {k+1}', 'middle'))
TERCO_FINAL = final(TPOS, T, et_t)
DEZENA_FINAL = final(DPOS, D, [(174, DPOS[0][2] + 16, 'a cruz', 'start'), (166, DPOS[2][2] + 4, 'Pai-Nosso', 'start'),
                               (172, DPOS[4][2] + 4, 'a medalha', 'start'), (150, D['cy'] - D['R'] - 14, '10 Ave-Marias', 'middle')])

# ---------- a página ----------
def cartao_no(n):
    ps = ''.join(f'<li><div class="fig">{svg(240, 150, c, t)}</div><p><span class="n">{i+1}</span><span>{t}</span></p></li>' for i, (t, c) in enumerate(n['passos']))
    return f'<article class="no" id="{n["id"]}"><h3>{n["nome"]}</h3><p class="para">{n["para"]}</p><ol class="passos">{ps}</ol></article>'

def lista_passos(ps):
    return ''.join(f'<li><div class="fig">{s}</div><p><span class="n">{i+1}</span><span>{t}</span></p></li>' for i, (t, s) in enumerate(ps))

leg = (f'<ul class="leg"><li>{svg(20,20,peca(10,10,"P","feito"),"conta de Pai-Nosso")}conta de Pai-Nosso (cor forte)</li>'
       f'<li>{svg(20,20,peca(10,10,"A","feito"),"conta de Ave-Maria")}conta de Ave-Maria</li>'
       f'<li>{svg(20,20,peca(10,10,"k","feito"),"nó")}nó</li>'
       f'<li>{svg(20,20,peca(10,10,"A","novo").replace("r=\"9.5\"","r=\"8.6\""),"o que se põe agora")}o que pões neste passo</li>'
       f'<li>{svg(20,20,peca(10,10,"A","falta"),"o que ainda falta")}o que ainda falta</li></ul>')

html = f'''<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Como fazer um terço</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=Karla:wght@400;700&display=swap">
<style>
:root{{--bg:#fdf9f3;--paper:#fffdf9;--ink:#4b4038;--muted:#85786b;--line:#ece2d3;--gold:#9a7843;--rose:#b56f7f}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:Karla,system-ui,sans-serif;font-size:18px;line-height:1.5;padding:0 16px}}
.wrap{{max-width:980px;margin:0 auto;padding:32px 0 64px;display:grid;gap:40px}}
h1,h2,h3{{font-family:"IM Fell English",Georgia,serif;font-weight:400;margin:0;text-align:center}}
h1{{font-size:46px;color:var(--gold)}}h2{{font-size:34px}}h3{{font-size:26px;color:var(--rose)}}
.kicker{{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--rose);font-weight:700;text-align:center;margin:0}}
.lead{{text-align:center;color:var(--muted);max-width:640px;margin:8px auto 0}}
section{{display:grid;gap:22px}}
.card{{background:var(--paper);border:1px solid var(--line);border-radius:22px;padding:22px}}
.precisas{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px 24px;margin:12px 0 0;padding:0;list-style:none}}
.precisas li{{display:flex;gap:10px;align-items:baseline}}.precisas b{{font-family:Karla,system-ui,sans-serif;font-size:20px;color:var(--gold);min-width:34px;text-align:right}}
.no{{background:var(--paper);border:1px solid var(--line);border-radius:22px;padding:22px;display:grid;gap:10px;break-inside:avoid}}
.para{{text-align:center;color:var(--muted);margin:0}}
.passos{{list-style:none;margin:6px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}}
.passos li{{display:grid;gap:8px;align-content:start}}
.fig{{background:#fffaf1;border:1px solid var(--line);border-radius:16px;padding:6px}}
.fig svg{{width:100%;height:auto;display:block}}
.passos p{{margin:0;display:flex;gap:10px;align-items:flex-start}}
.n{{flex:none;width:30px;height:30px;border-radius:50%;background:var(--rose);color:#fff;font-weight:700;display:grid;place-items:center;font-size:16px}}
.et{{font-family:Karla,system-ui,sans-serif;font-size:12.5px;fill:#6f6357}}
.leg{{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px 20px;justify-content:center;font-size:15px;color:var(--muted)}}
.leg li{{display:flex;align-items:center;gap:6px}}.leg svg{{width:20px;height:20px}}
.grande{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:28px;align-items:center}}
.grande .fig{{padding:10px}}
.conta{{display:grid;gap:8px}}.conta p{{margin:0}}
.conta .tot{{font-family:"IM Fell English",Georgia,serif;font-size:24px;color:var(--gold)}}
.etapas{{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}}
.dica{{background:#fbf0d9;border-radius:16px;padding:14px 18px;margin:0}}
@media(max-width:700px){{.grande{{grid-template-columns:1fr}}h1{{font-size:36px}}}}
@page{{size:A4;margin:12mm}}@media print{{body{{background:#fff;font-size:13px;padding:0}}.passos{{grid-template-columns:repeat(3,1fr)}}h1{{font-size:34px}}.wrap{{padding:0;gap:20px}}.no,.card{{break-inside:avoid}}.passos li{{break-inside:avoid}}}}
</style></head><body><div class="wrap">

<header><p class="kicker">Sete Rosas</p><h1>Como fazer um terço</h1>
<p class="lead">Primeiro aprendes os nós. Depois fazes uma dezena de bolso, para treinar, e a seguir o terço inteiro. Vai sempre da cruz para cima.</p></header>

<section class="card">
<h2>O que precisas</h2>
<ul class="precisas">
<li><b>53</b> contas de Ave-Maria, da cor que escolheres</li>
<li><b>6</b> contas de Pai-Nosso, de uma cor forte, sempre a mesma</li>
<li><b>1</b> cruz</li>
<li><b>1</b> medalha com três argolas</li>
<li><b>1</b> cordel comprido (corta um bocado a mais: os nós gastam cordel)</li>
<li><b>1</b> alfinete, para encostar os nós</li>
<li><b>1</b> tesoura e um isqueiro, que só um adulto usa</li>
</ul>
<p class="dica" style="margin-top:14px">Para uma dezena de bolso chegam <b>10</b> contas de Ave-Maria, <b>1</b> de Pai-Nosso, uma cruz e uma medalha.</p>
</section>

<section>
<div><p class="kicker">Parte 1</p><h2>Os nós</h2><p class="lead">Treina cada nó num bocado de cordel antes de começares o terço.</p></div>
{"".join(cartao_no(n) for n in NOS)}
<article class="no"><h3>O truque do alfinete</h3><p class="para">Para o nó ficar mesmo encostado à conta, sem espaço a mais.</p>
<ol class="passos">{"".join(f'<li><div class="fig">{svg(240, 150, c, t)}</div><p><span class="n">{i+1}</span><span>{t}</span></p></li>' for i, (t, c) in enumerate(ALFINETE))}</ol></article>
</section>

<section>
<div><p class="kicker">Parte 2</p><h2>A dezena de bolso</h2><p class="lead">Uma cruz, um Pai-Nosso, a medalha e dez Ave-Marias numa roda.</p></div>
{leg}
<div class="card grande"><div class="fig">{DEZENA_FINAL}</div>
<div class="conta"><p class="tot">Assim fica a dezena</p><p>De baixo para cima: a cruz, um nó, a conta do Pai-Nosso, um nó, a medalha, e a roda de dez contas de Ave-Maria, com um nó no princípio e outro no fim.</p><p><b>11 contas:</b> 1 de Pai-Nosso e 10 de Ave-Maria.</p></div></div>
<ol class="passos etapas">{lista_passos(DEZENA_PASSOS)}</ol>
</section>

<section>
<div><p class="kicker">Parte 3</p><h2>O terço inteiro</h2><p class="lead">O terço de Nossa Senhora tem cinco dezenas. Cada dezena tem uma conta de Pai-Nosso e dez de Ave-Maria.</p></div>
{leg}
<div class="card grande"><div class="fig">{TERCO_FINAL}</div>
<div class="conta"><p class="tot">Assim fica o terço</p>
<p>De baixo para cima: a <b>cruz</b>, <b>1</b> conta de Pai-Nosso, <b>3</b> de Ave-Maria, <b>1</b> de Pai-Nosso, e a <b>medalha</b>.</p>
<p>Depois da medalha vem a roda com as <b>5 dezenas</b> de 10 Ave-Marias. Entre cada dezena há uma conta de Pai-Nosso: são 4 na roda. A da primeira dezena é a que está por baixo da medalha.</p>
<p><b>59 contas:</b> 6 de Pai-Nosso e 53 de Ave-Maria.</p>
<p class="dica">Antes de fechares, conta as dezenas: tem de haver cinco grupos de dez.</p></div></div>
<ol class="passos etapas">{lista_passos(TERCO_PASSOS)}</ol>
</section>

<p class="lead" style="font-family:'IM Fell English',Georgia,serif;font-style:italic;color:var(--gold);font-size:22px">Um terço de cada vez, até à paz no mundo.</p>
</div></body></html>'''

open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'como-fazer-um-terco.html'), 'w', encoding='utf-8').write(html)
print('ok', len(TPOS), len(DPOS))

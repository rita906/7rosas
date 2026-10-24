# Desenha o terço da pagela em SVG: a coroa de 5 dezenas, a medalha, as 3 contas, o Pai-Nosso e a cruz, com os números dos passos
import math
ARCO = ["#f2b8c6", "#f7cfa8", "#f3df98", "#bcd9b0", "#b6cfee", "#cfc0ea"]
PEROLA, OURO, FIO = "#fbf6ec", "#b08d57", "#d9c39b"
cx, cy, R = 60, 50, 38
out = ['<svg viewBox="0 0 120 172" width="100%" xmlns="http://www.w3.org/2000/svg" aria-label="Um terço com os passos numerados">']
out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{FIO}" stroke-width="0.6"/>')
out.append(f'<line x1="{cx}" y1="{cy+R}" x2="{cx}" y2="150" stroke="{FIO}" stroke-width="0.6"/>')
# 55 posições à volta: em cada dezena, uma conta grande e dez pequenas; deixa um espaço em baixo para a medalha
pos = 55
inicio, fim = 90 + 9, 90 + 351
for k in range(pos):
    ang = math.radians(inicio + (fim - inicio) * k / (pos - 1))
    x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
    grande = k % 11 == 0
    r = 3.0 if grande else 2.0
    cor = PEROLA if grande else ARCO[(k // 11) % len(ARCO)]
    out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{cor}" stroke="{OURO}" stroke-width="0.35"/>')
# medalha
out.append(f'<ellipse cx="{cx}" cy="{cy+R+1}" rx="4.2" ry="5" fill="{PEROLA}" stroke="{OURO}" stroke-width="0.6"/>')
out.append(f'<text x="{cx}" y="{cy+R+2.6}" font-size="5" text-anchor="middle" fill="{OURO}" font-family="IM Fell English, Georgia, serif">M</text>')
# pendente: 3 contas pequenas, 1 grande, cruz
for i, y in enumerate([100, 106, 112]):
    out.append(f'<circle cx="{cx}" cy="{y}" r="2" fill="{ARCO[i+1]}" stroke="{OURO}" stroke-width="0.35"/>')
out.append(f'<circle cx="{cx}" cy="121" r="3" fill="{PEROLA}" stroke="{OURO}" stroke-width="0.35"/>')
out.append(f'<path d="M{cx} 129 V158 M{cx-7} 137 H{cx+7}" stroke="{OURO}" stroke-width="2.6" stroke-linecap="round"/>')
# números dos passos, num círculo dourado ao lado de cada parte
def num(n, x, y):
    out.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#fffdf9" stroke="{OURO}" stroke-width="0.6"/>')
    out.append(f'<text x="{x}" y="{y+2.2}" font-size="6.5" text-anchor="middle" fill="{OURO}" font-family="IM Fell English, Georgia, serif">{n}</text>')
num(1, cx + 16, 146)
num(5, cx + 13, 121)
num(4, cx + 13, 106)
num(2, cx + R + 12, cy - 18)
num(3, cx - 15, cy + R + 1)
out.append('</svg>')
print("".join(out))

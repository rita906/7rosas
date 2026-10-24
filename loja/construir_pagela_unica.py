# Gera a pagela numa só página A4 (pagela-unica.html) a partir de pagela-unica.src.html e de oracoes.json
import base64, json, pathlib
aqui = pathlib.Path(__file__).parent
s = (aqui / 'pagela-unica.src.html').read_text(encoding='utf-8')
G = [("Gozosos", "Mistérios da alegria: o nascimento e a infância de Jesus", "segunda e quinta",
      ["A Anunciação do Anjo a Nossa Senhora", "A Visitação de Nossa Senhora a Santa Isabel", "O Nascimento de Jesus em Belém",
       "A Apresentação do Menino Jesus no Templo", "O Encontro do Menino Jesus no Templo"]),
     ("Dolorosos", "Mistérios da dor: a Paixão e a morte de Jesus", "terça e sexta",
      ["A Agonia de Jesus no Horto", "A Flagelação de Jesus", "A Coroação de espinhos",
       "Jesus a caminho do Calvário com a cruz às costas", "A Crucifixão e morte de Jesus"]),
     ("Gloriosos", "Mistérios da glória: a Ressurreição de Jesus e Nossa Senhora no Céu", "quarta, sábado e domingo",
      ["A Ressurreição de Jesus", "A Ascensão de Jesus ao Céu", "A Vinda do Espírito Santo",
       "A Assunção de Nossa Senhora ao Céu", "A Coroação de Nossa Senhora"])]
mist = ''.join(
    f'<div class="grupo"><h3>{n}</h3><p class="exp">{e}</p><p class="dias">{d}</p><ol>'
    + ''.join(f'<li><span>{i+1}.º</span>{x}</li>' for i, x in enumerate(l)) + '</ol></div>'
    for n, e, d, l in G)
ORAS = json.loads((aqui / 'oracoes.json').read_text(encoding='utf-8'))
ors = ''.join(f'    <p class="or" lang="pt-PT"><b>{o[0]}</b>{o[1]}</p><p class="or" lang="la"><b>{o[2]}</b>{o[3]}</p>\n' for o in ORAS)
html = s.replace('__MISTERIOS__', mist).replace('__ORACOES__', ors)
img = 'data:image/jpeg;base64,' + base64.b64encode((aqui / 'img/como-rezar.jpg').read_bytes()).decode()
(aqui / 'pagela-unica.html').write_text(html.replace('src="img/como-rezar.jpg"', f'src="{img}"'), encoding='utf-8')

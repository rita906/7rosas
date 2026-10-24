# Gera o index.html do site a partir de loja/index.src.html (a mesma fonte da pré-visualização no Claude)
import pathlib
raiz = pathlib.Path(__file__).parent
s = (raiz / 'loja/index.src.html').read_text(encoding='utf-8')
i = s.index('<nav class="topbar"')
head = s[:i].replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
reset = ('<style>body{margin:0;font-size:14px}img{max-width:100%}[hidden]{display:none!important}'
         ':root{padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}</style>\n')
html = ('<!doctype html>\n<html lang="pt-PT">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="description" content="Terços coloridos, feitos à mão por sete irmãs, com a pagela de como rezar o terço. Ad Iesum per Mariam.">\n'
        '<meta property="og:title" content="Sete Rosas">\n<meta property="og:description" content="Um terço de cada vez, até à paz no mundo.">\n'
        '<meta property="og:image" content="https://seterosas.pt/img/logo.jpg">\n<link rel="icon" href="img/logo.jpg">\n'
        + reset + head + '</head>\n<body>\n' + s[i:] + '\n</body>\n</html>\n')
html = html.replace('__LOGO__', 'img/logo.jpg').replace('__ROSAS__', 'img/rosas.jpg').replace('__COMO__', 'img/como-rezar.jpg')
assert '__LOGO__' not in html and '__ROSAS__' not in html and '__COMO__' not in html
(raiz / 'index.html').write_text(html, encoding='utf-8')

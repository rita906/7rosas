# Sete Rosas

Terços e dezenas de bolso feitos à mão por sete irmãs. Ad Iesum per Mariam.
A missão: que todas as famílias rezem o terço, pelas mãos das crianças.

## Onde vive cada coisa
- Loja: `index.html`, gerado por `python3 construir.py` a partir de `loja/index.src.html`. Publicada no GitHub Pages com o domínio seterosas.pt (ficheiro CNAME).
- Encomendas, stock, custos, pedidos e opiniões: Google Sheet "Sete Rosas: gestão", com o código em `folha/` (Apps Script). O código copia-se para o editor da folha e publica-se como app web (versão nova a cada mudança).
- Back office: a página Painel servida pela app web, com chave. O link está em PAINEL-PRIVADO.txt, que não vai para o GitHub.
- Pagela: `pagela-como-rezar-o-terco.pdf` (4 páginas A5: mistérios, como se reza, orações em português, orações em latim), anexada ao email de confirmação. Fonte em `loja/pagela.src.html`.

## Decisões (24-10-2026)
- Preços com portes incluídos: terço 12 €, dezena de bolso 7 €. Modelos: Rosa de Lisieux, Manto de Maria, Carmelo, Arco-íris.
- Personalizado (15 € terço, 9 € dezena) não é stock: entra como pedido personalizado por mensagem.
- Prazo: em stock, 5 a 8 dias úteis. Esgotado: pede-se por mensagem.
- Stock por modelo e formato (terço e dezena), começa a zero; as meninas juntam no painel o que fazem.
- Os terços não são benzidos; cada um leva a pagela de como rezar o terço.
- Encomendas fechadas ("disponíveis em breve") até se abrir no código (ABERTAS=false em loja/index.src.html).
- Emails ao cliente: confirmação com a pagela; aviso de envio com o pedido de opinião. As opiniões só aparecem na loja depois de aprovadas no painel.

## Por fazer
- Apontar seterosas.pt para o GitHub Pages na dominios.pt (a gestão de DNS não guardava a 24-10-2026).
- Números de MB WAY e WhatsApp; atividade e faturas (falar com o contabilista).
- Passar a folha e a app para 7rosas@gmail.com e o domínio para titular próprio.

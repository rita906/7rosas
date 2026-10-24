// Sete Rosas: encomendas, stock e opiniões numa Google Sheet.
// A loja (seterosas.pt) lê o stock e as opiniões com GET e envia encomendas com POST.
// Cada encomenda entra no separador Encomendas, desconta o stock, avisa a Rita e confirma ao cliente por email.

// Um stock por modelo e por formato: cada linha da folha Stock é "Modelo · Formato"
const BASES = ['Rosa de Lisieux', 'Manto de Maria', 'Carmelo', 'Arco-íris', 'Personalizado'];
const FORMATOS = ['Terço', 'Dezena de bolso'];
const MODELOS = BASES.flatMap(b => FORMATOS.map(f => `${b} · ${f}`));
const STOCK_INICIAL = 0;
// O endereço público da app (o de /a/macros/ pede sessão a quem é de fora)
const APP_URL = 'https://script.google.com/macros/s/AKfycbzDHMQaDLvuKFeFQKKcO9V5Hv6wFDiDo6OFAEM8Lc2cZCOvasNbtkcBbx-hNLXzr__Peg/exec';
const LOJA_URL = 'https://seterosas.pt';

// Colunas do separador Encomendas (1 = A)
const C = { numero: 1, data: 2, nome: 3, tel: 4, entrega: 5, morada: 6, nif: 7, nomeFiscal: 8, tercos: 9, pecas: 10,
  total: 11, nota: 12, pago: 13, enviado: 14, registo: 15, fatura: 16, email: 17, token: 18 };

// As funções sem chave só podem correr no editor, pela dona da folha. Qualquer página servida por este
// script (a da opinião é pública) consegue chamar funções pelo google.script.run, e assim ficam fechadas.
function soNoEditor_() {
  const ativo = Session.getActiveUser().getEmail();
  if (!ativo || ativo !== Session.getEffectiveUser().getEmail()) throw new Error('Só no editor');
}

// Corre uma vez, à mão, no editor: cria os separadores com cabeçalhos, fórmulas e caixas. Apaga o que lá estiver.
function preparar() {
  soNoEditor_();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.setSpreadsheetLocale('pt_PT');

  const stock = ss.getSheetByName('Stock') || ss.insertSheet('Stock');
  stock.clear();
  stock.getRange(1, 1, 1, 4).setValues([['Modelo', 'Stock da fornada', 'Vendidos', 'Restam']]).setFontWeight('bold');
  MODELOS.forEach((m, i) => {
    const r = i + 2;
    stock.getRange(r, 1, 1, 4).setValues([[m, STOCK_INICIAL, 0, `=B${r}-C${r}`]]);
  });
  stock.setFrozenRows(1);
  stock.autoResizeColumns(1, 4);

  const enc = ss.getSheetByName('Encomendas') || ss.insertSheet('Encomendas');
  enc.clear();
  const cab = ['N.º', 'Data', 'Nome', 'Telemóvel', 'Entrega', 'Morada', 'NIF', 'Nome na fatura',
    'Terços', 'Peças', 'Total (€)', 'Nota', 'Pago', 'Enviado', 'Registo CTT', 'Fatura n.º', 'Email', 'Código da opinião'];
  enc.getRange(1, 1, 1, cab.length).setValues([cab]).setFontWeight('bold');
  enc.setFrozenRows(1);
  enc.getRange('M2:N1000').insertCheckboxes();

  const compras = ss.getSheetByName('Compras') || ss.insertSheet('Compras');
  compras.clear();
  compras.getRange(1, 1, 1, 7).setValues([['Data', 'Loja', 'O quê', 'Quantidade', 'Valor pago (€)', 'Link', 'Fatura guardada']])
    .setFontWeight('bold');
  compras.setFrozenRows(1);
  compras.getRange('G2:G500').insertCheckboxes();

  const op = ss.getSheetByName('Opiniões') || ss.insertSheet('Opiniões');
  op.clear();
  op.getRange(1, 1, 1, 7).setValues([['Data', 'Encomenda n.º', 'Nome a mostrar', 'Rosas (1 a 5)', 'Opinião', 'Mostrar na loja', 'Email']])
    .setFontWeight('bold');
  op.setFrozenRows(1);
  op.getRange('F2:F1000').insertCheckboxes();

  const ped = ss.getSheetByName('Pedidos') || ss.insertSheet('Pedidos');
  ped.clear();
  ped.getRange(1, 1, 1, 6).setValues([['Data', 'Nome', 'Email', 'Telemóvel', 'Mensagem', 'Respondido']]).setFontWeight('bold');
  ped.setFrozenRows(1);
  ped.getRange('F2:F1000').insertCheckboxes();

  // O painel junta tudo: dinheiro, encomendas por tratar e stock
  const painel = ss.getSheetByName('Painel') || ss.insertSheet('Painel', 0);
  painel.clear();
  painel.getRange('A1').setValue('Sete Rosas').setFontSize(18).setFontWeight('bold');
  painel.getRange('A3:B12').setValues([
    ['Dinheiro', ''],
    ['Receita recebida (encomendas pagas)', '=SUMIF(Encomendas!M2:M,TRUE,Encomendas!K2:K)'],
    ['Receita por receber (encomendas por pagar)', '=SUMIFS(Encomendas!K2:K,Encomendas!M2:M,FALSE,Encomendas!A2:A,"<>")'],
    ['Custos de materiais', '=SUM(Compras!E2:E)'],
    ['Resultado (recebido menos custos)', '=B4-B6'],
    ['', ''],
    ['Encomendas', ''],
    ['Por pagar', '=COUNTIFS(Encomendas!A2:A,"<>",Encomendas!M2:M,FALSE)'],
    ['Pagas e por enviar', '=COUNTIFS(Encomendas!M2:M,TRUE,Encomendas!N2:N,FALSE)'],
    ['Enviadas', '=COUNTIF(Encomendas!N2:N,TRUE)'],
  ]);
  painel.getRange('A14').setValue('Stock desta fornada');
  painel.getRange('A15').setFormula('=Stock!A1:D' + (MODELOS.length + 1));
  painel.getRange('B4:B7').setNumberFormat('#,##0.00 "€"');
  ['A3', 'A9', 'A14'].forEach(c => painel.getRange(c).setFontWeight('bold'));
  painel.setColumnWidth(1, 320);

  const folha1 = ss.getSheetByName('Folha1') || ss.getSheetByName('Sheet1');
  if (folha1) ss.deleteSheet(folha1);
}

// Nova fornada: repõe os vendidos a zero. As encomendas antigas ficam na folha.
function novaFornada() {
  soNoEditor_();
  novaFornada_();
}

function novaFornada_() {
  const stock = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Stock');
  stock.getRange(2, 3, MODELOS.length, 1).setValue(0);
}

function lerStock_() {
  const linhas = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Stock')
    .getRange(2, 1, MODELOS.length, 4).getValues();
  const restam = {};
  linhas.forEach(([modelo, , , r]) => { restam[modelo] = Math.max(0, Number(r) || 0); });
  return restam;
}

// Só as opiniões marcadas para mostrar, as mais recentes primeiro
function opinioesPublicas_() {
  const op = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Opiniões');
  const n = primeiraVazia_(op, 1) - 2;
  if (n < 1) return [];
  return op.getRange(2, 1, n, 6).getValues().filter(r => r[5] === true).reverse().slice(0, 12)
    .map(r => ({ nome: String(r[2]), rosas: Number(r[3]) || 5, texto: String(r[4]),
      data: r[0] instanceof Date ? Utilities.formatDate(r[0], 'Europe/Lisbon', 'MM/yyyy') : '' }));
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// Sem parâmetros devolve o stock e as opiniões à loja.
// ?painel=<chave> abre a página de gestão; ?opiniao=<n.º>&t=<código> abre a página para deixar uma opinião.
function doGet(e) {
  const p = (e && e.parameter) || {};
  if (p.painel) {
    if (p.painel !== chave_()) return HtmlService.createHtmlOutput('Ligação inválida.');
    const t = HtmlService.createTemplateFromFile('Painel');
    t.chave = p.painel;
    return t.evaluate().setTitle('Sete Rosas: o nosso negócio')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1');
  }
  if (p.opiniao) {
    const enc = encomendaPorCodigo_(Number(p.opiniao), String(p.t || ''));
    const t = HtmlService.createTemplateFromFile('Opiniao');
    t.numero = enc ? enc.numero : '';
    t.codigo = enc ? String(p.t) : '';
    t.nome = enc ? primeiroNome_(enc.nome) : '';
    t.valida = enc ? 'sim' : 'nao';
    t.loja = LOJA_URL;
    return t.evaluate().setTitle('Sete Rosas: a tua opinião')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1');
  }
  return json_({ ok: true, restam: lerStock_(), opinioes: opinioesPublicas_() });
}

// A chave do painel vive nas propriedades do script; cria-se na primeira vez que é pedida
function chave_() {
  const props = PropertiesService.getScriptProperties();
  let k = props.getProperty('CHAVE_PAINEL');
  if (!k) { k = Utilities.getUuid().replace(/-/g, ''); props.setProperty('CHAVE_PAINEL', k); }
  return k;
}

function confirmar_(chave) {
  if (chave !== chave_()) throw new Error('Sem acesso');
}

// Corre no editor para saber o endereço do painel (aparece no registo de execução)
function enderecoDoPainel() {
  soNoEditor_();
  Logger.log(APP_URL + '?painel=' + chave_());
}

function primeiroNome_(nome) {
  return String(nome || '').trim().split(/\s+/)[0] || '';
}

function eur_(n) {
  return (Number(n) || 0).toFixed(2).replace('.', ',') + ' €';
}

function encomendaPorCodigo_(numero, codigo) {
  if (!numero || !codigo) return null;
  const enc = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Encomendas');
  const linha = numero + 1;
  if (linha > enc.getMaxRows()) return null;
  const r = enc.getRange(linha, 1, 1, C.token).getValues()[0];
  if (Number(r[C.numero - 1]) !== numero || String(r[C.token - 1]) !== codigo) return null;
  return { numero, nome: r[C.nome - 1], email: r[C.email - 1], linha };
}

function painelDados(chave) {
  confirmar_(chave);
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const stock = ss.getSheetByName('Stock').getRange(2, 1, MODELOS.length, 4).getValues()
    .map(([modelo, total, vendidos, restam]) => ({ modelo, total: Number(total), vendidos: Number(vendidos), restam: Math.max(0, Number(restam)) }));

  const enc = ss.getSheetByName('Encomendas');
  const n = primeiraVazia_(enc, C.numero) - 2;
  const encomendas = n > 0 ? enc.getRange(2, 1, n, C.token).getValues().map((r, i) => ({
    linha: i + 2, numero: r[0], nome: r[2], tel: String(r[3]), entrega: r[4], morada: r[5], nif: String(r[6]),
    nomeFiscal: r[7], tercos: r[8], pecas: Number(r[9]) || 0, total: Number(r[10]) || 0, nota: r[11],
    pago: r[12] === true, enviado: r[13] === true, registo: String(r[14] || ''), fatura: String(r[15] || ''),
    email: String(r[16] || '')
  })) : [];

  const comp = ss.getSheetByName('Compras');
  const m = primeiraVazia_(comp, 3) - 2;
  const compras = m > 0 ? comp.getRange(2, 1, m, 5).getValues().map((r, i) => ({
    linha: i + 2,
    data: r[0] instanceof Date ? Utilities.formatDate(r[0], 'Europe/Lisbon', 'dd-MM-yyyy') : String(r[0]),
    dataIso: r[0] instanceof Date ? Utilities.formatDate(r[0], 'Europe/Lisbon', 'yyyy-MM-dd') : '',
    loja: r[1], oque: r[2], valor: Number(r[4]) || 0
  })).filter(c => c.oque !== '') : [];

  const op = ss.getSheetByName('Opiniões');
  const k = primeiraVazia_(op, 1) - 2;
  const opinioes = k > 0 ? op.getRange(2, 1, k, 6).getValues().map((r, i) => ({
    linha: i + 2, numero: r[1], nome: String(r[2]), rosas: Number(r[3]) || 0, texto: String(r[4]), mostrar: r[5] === true
  })).reverse() : [];

  const ped = ss.getSheetByName('Pedidos');
  const q = ped ? primeiraVazia_(ped, 1) - 2 : 0;
  const pedidos = q > 0 ? ped.getRange(2, 1, q, 6).getValues().map((r, i) => ({
    linha: i + 2, data: r[0] instanceof Date ? Utilities.formatDate(r[0], 'Europe/Lisbon', 'dd-MM-yyyy') : String(r[0]),
    nome: String(r[1]), email: String(r[2]), tel: String(r[3]), mensagem: String(r[4]), respondido: r[5] === true
  })).reverse() : [];

  const pagas = encomendas.filter(o => o.pago);
  const entrou = pagas.reduce((s, o) => s + o.total, 0);
  const gastos = compras.reduce((s, c) => s + c.valor, 0);
  return {
    dinheiro: { entrou, gastos, sobrou: entrou - gastos, vendido: entrou,
      porReceber: encomendas.filter(o => !o.pago).reduce((s, o) => s + o.total, 0) },
    pecasVendidas: pagas.reduce((s, o) => s + o.pecas, 0),
    stock, encomendas, compras, opinioes, pedidos
  };
}

function marcarEncomenda(chave, linha, campo, valor, registo) {
  confirmar_(chave);
  const enc = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Encomendas');
  if (campo === 'pago') enc.getRange(linha, C.pago).setValue(valor === true);
  if (campo === 'enviado') {
    const jaEnviada = enc.getRange(linha, C.enviado).getValue() === true;
    enc.getRange(linha, C.enviado).setValue(valor === true);
    if (registo) enc.getRange(linha, C.registo).setValue(registo);
    if (valor === true && !jaEnviada) avisarEnvio_(enc.getRange(linha, 1, 1, C.token).getValues()[0]);
  }
  if (campo === 'fatura') enc.getRange(linha, C.fatura).setValue(String(valor));
}

function novaCompra(chave, c) {
  confirmar_(chave);
  const comp = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Compras');
  comp.getRange(primeiraVazia_(comp, 3), 1, 1, 7)
    .setValues([[c.data ? new Date(c.data) : new Date(), c.loja || '', c.oque, '', Number(c.valor) || 0, '', false]]);
}

// Corrige uma compra (o quê, onde, valor, data) na linha indicada
function editarCompra(chave, linha, c) {
  confirmar_(chave);
  const comp = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Compras');
  if (linha < 2 || comp.getRange(linha, 3).getValue() === '') throw new Error('Compra não encontrada');
  comp.getRange(linha, 1, 1, 3).setValues([[c.data ? new Date(c.data) : comp.getRange(linha, 1).getValue(), c.loja || '', c.oque]]);
  comp.getRange(linha, 5).setValue(Number(c.valor) || 0);
}

// Apaga uma compra: tira a linha e acrescenta uma vazia no fim, com a caixa de verificação, para a folha não encolher
function apagarCompra(chave, linha) {
  confirmar_(chave);
  const comp = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Compras');
  if (linha < 2 || comp.getRange(linha, 3).getValue() === '') throw new Error('Compra não encontrada');
  comp.deleteRow(linha);
  comp.insertRowAfter(comp.getMaxRows());
  comp.getRange(comp.getMaxRows(), 7).insertCheckboxes();
}

function marcarPedido(chave, linha, valor) {
  confirmar_(chave);
  SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Pedidos').getRange(linha, 6).setValue(valor === true);
}

function mostrarOpiniao(chave, linha, valor) {
  confirmar_(chave);
  SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Opiniões').getRange(linha, 6).setValue(valor === true);
}

// Chamada pela página da opinião. Uma opinião por encomenda; fica escondida até a Rita a mostrar.
function guardarOpiniao(numero, codigo, rosas, texto, nomeMostrar) {
  const enc = encomendaPorCodigo_(Number(numero), String(codigo));
  if (!enc) throw new Error('Ligação inválida');
  const op = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Opiniões');
  const n = primeiraVazia_(op, 1) - 2;
  if (n > 0 && op.getRange(2, 2, n, 1).getValues().some(r => Number(r[0]) === enc.numero)) throw new Error('Já existe');
  const r = Math.min(5, Math.max(1, Number(rosas) || 5));
  op.getRange(n + 2, 1, 1, 7).setValues([[new Date(), enc.numero, String(nomeMostrar || primeiroNome_(enc.nome)).slice(0, 60),
    r, String(texto || '').slice(0, 1000), false, enc.email]]);
  MailApp.sendEmail(Session.getEffectiveUser().getEmail(), `Sete Rosas: nova opinião (${r} rosas)`,
    `${nomeMostrar} deixou uma opinião sobre a encomenda n.º ${enc.numero}:\n\n${texto}\n\n` +
    'Está escondida até carregares em "Mostrar na loja" no painel.');
}

function fornadaNova(chave) {
  confirmar_(chave);
  novaFornada_();
}

// Quantos terços de um modelo estão prontos para enviar: acerta o stock da fornada para que restem esses
// Passa o separador Stock para uma linha por modelo e formato, tudo a zero, sem mexer nas encomendas nem nas compras. Só no editor.
function migrarStock() {
  soNoEditor_();
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const stock = ss.getSheetByName('Stock');
  stock.clear();
  stock.getRange(1, 1, 1, 4).setValues([['Modelo', 'Stock da fornada', 'Vendidos', 'Restam']]).setFontWeight('bold');
  MODELOS.forEach((m, i) => { const r = i + 2; stock.getRange(r, 1, 1, 4).setValues([[m, 0, 0, `=B${r}-C${r}`]]); });
  stock.setFrozenRows(1);
  stock.autoResizeColumns(1, 4);
  ss.getSheetByName('Painel').getRange('A15').setFormula('=Stock!A1:D' + (MODELOS.length + 1));
}

function definirProntos(chave, modelo, prontos) {
  confirmar_(chave);
  const i = MODELOS.indexOf(modelo);
  if (i < 0) throw new Error('Modelo desconhecido');
  const stock = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Stock');
  const vendidos = Number(stock.getRange(i + 2, 3).getValue()) || 0;
  stock.getRange(i + 2, 2).setValue(vendidos + Math.max(0, Math.floor(Number(prontos) || 0)));
}

// Põe o stock de todos os modelos a zero (sem terços prontos). Só no editor.
function zerarStock() {
  soNoEditor_();
  const stock = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Stock');
  MODELOS.forEach((m, i) => stock.getRange(i + 2, 2).setValue(Number(stock.getRange(i + 2, 3).getValue()) || 0));
}

// Primeira linha sem nada na coluna indicada (as caixas de verificação enchem as outras colunas)
function primeiraVazia_(folha, coluna) {
  const valores = folha.getRange(2, coluna, folha.getMaxRows() - 1, 1).getValues();
  const i = valores.findIndex(r => r[0] === '');
  return i === -1 ? folha.getMaxRows() + 1 : i + 2;
}

// Os emails ao cliente: texto simples numa caixa creme, com a mesma assinatura da loja
function emailHtml_(paragrafos) {
  const corpo = paragrafos.map(p => `<p style="margin:0 0 14px">${p}</p>`).join('');
  return `<div style="background:#fdf9f3;padding:24px;font-family:Georgia,serif;color:#4b4038;font-size:16px;line-height:1.5">` +
    `<div style="max-width:520px;margin:0 auto">` +
    `<p style="margin:0 0 4px;font-size:26px;color:#9a7843">Sete Rosas</p>` +
    `<p style="margin:0 0 20px;font-style:italic;color:#9a7843">Ad Iesum per Mariam</p>${corpo}` +
    `<p style="margin:24px 0 0;font-style:italic;color:#9a7843">Um terço de cada vez, até à paz no mundo.</p>` +
    `</div></div>`;
}

function escapar_(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

const PAGELA_URL = LOJA_URL + '/pagela-como-rezar-o-terco.pdf';

// A pagela vai em anexo; se o site não responder, vai o link
function pagela_() {
  try {
    const r = UrlFetchApp.fetch(PAGELA_URL, { muteHttpExceptions: true });
    if (r.getResponseCode() === 200) return r.getBlob().setName('Como rezar o terço - Sete Rosas.pdf');
  } catch (err) { console.error(err); }
  return null;
}

function confirmarEncomenda_(p, numero, texto, total, especiais) {
  if (!p.email) return;
  const prazo = especiais.length
    ? 'Os modelos esgotados ficam como pedido especial: vamos falar contigo para combinar o prazo. ' +
      'O que está em stock chega em 5 a 8 dias úteis depois do pagamento.'
    : 'Está tudo em stock, por isso chega em 5 a 8 dias úteis depois do pagamento.';
  const anexo = pagela_();
  MailApp.sendEmail({
    to: p.email,
    name: 'Sete Rosas',
    attachments: anexo ? [anexo] : [],
    subject: `Sete Rosas: recebemos a tua encomenda n.º ${numero}`,
    htmlBody: emailHtml_([
      `Olá ${escapar_(primeiroNome_(p.nome))},`,
      `Recebemos a tua encomenda n.º ${numero}. Obrigada!`,
      escapar_(texto).replace(/\n/g, '<br>'),
      `<b>Total: ${eur_(total)}</b>, com portes incluídos.`,
      `Vamos enviar-te uma mensagem para o ${escapar_(p.tel)} com os dados para pagares por MB WAY. ` +
        'Assim que o pagamento chegar, começamos a preparar o teu terço.',
      prazo,
      anexo ? 'Juntamos a pagela <b>Como rezar o terço</b>, para rezarem juntos desde o primeiro dia.'
        : `Deixamos-te a pagela <a href="${PAGELA_URL}" style="color:#9a7843">Como rezar o terço</a>, para rezarem juntos desde o primeiro dia.`,
      'Se tiveres alguma dúvida, basta responderes a este email.'
    ])
  });
}

function avisarEnvio_(r) {
  const email = r[C.email - 1], codigo = r[C.token - 1], numero = r[C.numero - 1];
  if (!email) return;
  const link = `${APP_URL}?opiniao=${numero}&t=${codigo}`;
  const registo = r[C.registo - 1];
  MailApp.sendEmail({
    to: email,
    name: 'Sete Rosas',
    subject: `Sete Rosas: a tua encomenda n.º ${numero} já seguiu`,
    htmlBody: emailHtml_([
      `Olá ${escapar_(primeiroNome_(r[C.nome - 1]))},`,
      `A tua encomenda n.º ${numero} já seguiu, com a pagela de como rezar o terço.`,
      registo ? `O registo dos CTT é <b>${escapar_(registo)}</b>.` : '',
      'Quando o terço chegar e o rezarem a primeira vez, conta-nos como foi. Ajuda outras famílias a decidir.',
      `<a href="${link}" style="display:inline-block;background:#9a7843;color:#fffdf9;text-decoration:none;font-family:Arial,sans-serif;font-weight:bold;padding:12px 22px;border-radius:999px">Deixar a minha opinião</a>`
    ].filter(Boolean))
  });
}

// Pedido personalizado (quantidades, casamentos, cores à medida): guarda, avisa a Rita e confirma ao cliente
function pedidoPersonalizado_(p) {
  if (!p.nome || !p.email || !p.mensagem) return json_({ ok: false, erro: 'dados' });
  const ped = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Pedidos');
  const linha = primeiraVazia_(ped, 1);
  ped.getRange(linha, 1, 1, 6).setValues([[new Date(), p.nome, p.email, p.tel ? "'" + p.tel : '',
    String(p.mensagem).slice(0, 3000), false]]);
  MailApp.sendEmail({
    to: Session.getEffectiveUser().getEmail(), replyTo: p.email,
    subject: `Sete Rosas: pedido personalizado de ${p.nome}`,
    body: `${p.nome} · ${p.email}${p.tel ? ' · ' + p.tel : ''}\n\n${p.mensagem}\n\nPara responder, basta responder a este email.`
  });
  try {
    MailApp.sendEmail({
      to: p.email, name: 'Sete Rosas',
      subject: 'Sete Rosas: recebemos o teu pedido',
      htmlBody: emailHtml_([
        `Olá ${escapar_(primeiroNome_(p.nome))},`,
        'Recebemos o teu pedido personalizado. Obrigada por pensares em nós!',
        `<i>${escapar_(p.mensagem).replace(/\n/g, '<br>')}</i>`,
        'Vamos ver com calma e respondemos-te por email a dizer se é possível e quais são os prazos.'
      ])
    });
  } catch (err) { console.error(err); }
  return json_({ ok: true });
}

// Corpo esperado: {nome, email, tel, entrega, morada, nif, nomeFiscal, obs, itens:[{modelo, formato, det, q, preco}]}
// ou {tipo: 'pedido', nome, email, tel, mensagem} para um pedido personalizado
function doPost(e) {
  const corpo = JSON.parse(e.postData.contents);
  if (corpo.tipo === 'pedido') return pedidoPersonalizado_(corpo);
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  let p, numero, texto, total, especiais;
  try {
    p = corpo;
    const itens = (p.itens || []).filter(it => MODELOS.includes(it.modelo) && it.q > 0);
    if (!itens.length || !p.nome || !p.tel) return json_({ ok: false, erro: 'dados' });

    // Sem stock não se recusa: o modelo esgotado fica como pedido especial e o prazo combina-se com a família
    const pedido = {};
    itens.forEach(it => { pedido[it.modelo] = (pedido[it.modelo] || 0) + Number(it.q); });
    const restam = lerStock_();
    especiais = Object.keys(pedido).filter(m => pedido[m] > restam[m]);

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const stock = ss.getSheetByName('Stock');
    Object.keys(pedido).forEach(m => {
      const cel = stock.getRange(MODELOS.indexOf(m) + 2, 3);
      cel.setValue(Number(cel.getValue()) + pedido[m]);
    });

    // As caixas de Pago e Enviado ocupam as linhas todas, por isso conta-se pela coluna do número
    const enc = ss.getSheetByName('Encomendas');
    numero = primeiraVazia_(enc, C.numero) - 1;
    total = itens.reduce((s, it) => s + it.q * it.preco, 0);
    const pecas = itens.reduce((s, it) => s + Number(it.q), 0);
    texto = itens.map(it => `${it.q} × ${it.formato}, ${it.det}` +
      (especiais.includes(it.modelo) ? ' (PEDIDO ESPECIAL: esgotado, combinar prazo)' : ' (em stock: 5 a 8 dias úteis)')).join('\n');
    const codigo = Utilities.getUuid().replace(/-/g, '').slice(0, 12);
    enc.getRange(numero + 1, 1, 1, C.token).setValues([[numero, new Date(), p.nome, "'" + p.tel, p.entrega, p.morada || '',
      p.nif ? "'" + p.nif : '', p.nomeFiscal || '', texto, pecas, total, p.obs || '', false, false, '', '',
      p.email || '', codigo]]);
  } finally {
    lock.releaseLock();
  }

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  MailApp.sendEmail(Session.getEffectiveUser().getEmail(),
    `Sete Rosas: encomenda n.º ${numero} (${eur_(total)})`,
    `${p.nome} · ${p.tel}${p.email ? ' · ' + p.email : ''}\n\n${texto}\n\nTotal: ${eur_(total)}\nEntrega: ${p.entrega}` +
    `${p.morada ? '\nMorada: ' + p.morada : ''}${p.nif ? '\nNIF: ' + p.nif : ''}${p.obs ? '\nNota: ' + p.obs : ''}` +
    `\n\nFolha: ${ss.getUrl()}`);
  try { confirmarEncomenda_(p, numero, texto, total, especiais); } catch (err) { console.error(err); }

  return json_({ ok: true, numero, total, especiais, restam: lerStock_() });
}

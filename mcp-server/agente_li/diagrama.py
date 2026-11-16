"""Diagramas a partir de um modelo JSON (decisão 0012): a IA descreve, o código valida e desenha.

Saídas: <nome>.drawio (editável, abre no draw.io e no Miro), <nome>.png (vai no .docx) e <nome>.json (modelo).

Modelos aceitos ("tipo"):
  bpmn          raias + nos (inicio | tarefa | decisao | fim) + ligacoes   -> processos e fluxos
  casos_de_uso  sistema + atores + casos (cada caso lista os atores)        -> UML de casos de uso
  sequencia     participantes + mensagens (de, para, texto, retorno?)       -> UML de sequência
"""
import json, os, re, textwrap, unicodedata
from xml.sax.saxutils import quoteattr

from PIL import Image, ImageDraw, ImageFont

# tamanhos uniformes (regra da equipe)
TW, TH, EV, GW = 150, 64, 36, 50           # tarefa, evento, decisão
COL, RAIA, CAB, MARG = 180, 104, 30, 14    # passo da coluna, altura da raia, faixa do nome da raia, margem
ESCALA = 2                                 # PNG em 2x para ficar nítido no Word
AZUL, CINZA, BORDA = (232, 244, 248), (245, 245, 245), (60, 60, 60)


class ErroDiagrama(ValueError):
    pass


def _slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:60] or 'diagrama'


_FONTES = ['C:/Windows/Fonts/calibri.ttf', 'C:/Windows/Fonts/arial.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf',
           '/Library/Fonts/Arial.ttf', '/System/Library/Fonts/Helvetica.ttc', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
           '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf']
_fonte_arquivo = next((f for f in _FONTES if os.path.exists(f)), None)


def _fonte(tam):
    # fonte do sistema (tem acentos); a embutida do Pillow só serve de último recurso
    if _fonte_arquivo:
        return ImageFont.truetype(_fonte_arquivo, tam * ESCALA)
    return ImageFont.load_default(tam * ESCALA)


def _quebrar(texto, largura_chars):
    return '\n'.join(textwrap.wrap(str(texto), largura_chars)) or ''


# ------------------------------------------------------------------ BPMN
def _validar_bpmn(m):
    raias = m.get('raias') or []
    nos = {n['id']: n for n in m.get('nos') or []}
    lig = m.get('ligacoes') or []
    if not raias:
        raise ErroDiagrama('BPMN precisa de raias (uma por ator/sistema)')
    if len(nos) != len(m.get('nos') or []):
        raise ErroDiagrama('ids de nós repetidos')
    for n in nos.values():
        if n.get('tipo') not in ('inicio', 'tarefa', 'decisao', 'fim'):
            raise ErroDiagrama(f"nó {n['id']}: tipo deve ser inicio, tarefa, decisao ou fim")
        if n.get('raia') not in raias:
            raise ErroDiagrama(f"nó {n['id']}: raia '{n.get('raia')}' não existe")
    for l in lig:
        if l['de'] not in nos or l['para'] not in nos:
            raise ErroDiagrama(f"ligação {l['de']} -> {l['para']}: nó inexistente")
    entra = {i: [l for l in lig if l['para'] == i] for i in nos}
    sai = {i: [l for l in lig if l['de'] == i] for i in nos}
    if sum(n['tipo'] == 'inicio' for n in nos.values()) != 1:
        raise ErroDiagrama('o fluxo precisa de exatamente um evento de início')
    for i, n in nos.items():
        if n['tipo'] == 'inicio' and entra[i]:
            raise ErroDiagrama('evento de início não recebe ligação')
        if n['tipo'] == 'fim':
            if sai[i]:
                raise ErroDiagrama(f'evento de fim {i} não pode ter saída')
            if len(entra[i]) != 1:
                raise ErroDiagrama(f'evento de fim {i}: cada caminho termina no seu próprio fim (uma entrada só)')
        elif not sai[i]:
            raise ErroDiagrama(f'nó {i} não leva a lugar nenhum: todo caminho termina em um evento de fim')
        if n['tipo'] != 'inicio' and not entra[i]:
            raise ErroDiagrama(f'nó {i} está solto (sem entrada)')
        if n['tipo'] == 'decisao' and len(sai[i]) < 2:
            raise ErroDiagrama(f'decisão {i} precisa de pelo menos duas saídas')
    # colunas pelo caminho mais longo; ciclo = loop inválido
    col, visitando = {}, set()

    def prof(i):
        if i in col:
            return col[i]
        if i in visitando:
            raise ErroDiagrama(f'loop inválido passando por {i}: o fluxo segue da esquerda para a direita')
        visitando.add(i)
        col[i] = 1 + max((prof(l['de']) for l in entra[i]), default=-1)
        visitando.discard(i)
        return col[i]
    for i in nos:
        prof(i)
    # dois nós na mesma raia e coluna: empurra o segundo (e o que vem depois) para a direita
    mudou = True
    while mudou:
        mudou = False
        ocupado = {}
        for i in sorted(nos, key=lambda k: (col[k], list(nos).index(k))):
            chave = (nos[i]['raia'], col[i])
            if chave in ocupado:
                col[i] += 1; mudou = True
            else:
                ocupado[chave] = i
        for l in lig:
            if col[l['para']] <= col[l['de']]:
                col[l['para']] = col[l['de']] + 1; mudou = True
    return raias, nos, lig, col


def _geo_bpmn(m):
    raias, nos, lig, col = _validar_bpmn(m)
    geo = {}
    for i, n in nos.items():
        w, h = {'tarefa': (TW, TH), 'decisao': (GW, GW)}.get(n['tipo'], (EV, EV))
        cx = CAB + MARG + col[i] * COL + TW / 2
        cy = raias.index(n['raia']) * RAIA + RAIA / 2
        geo[i] = (cx - w / 2, cy - h / 2, w, h)
    largura = CAB + MARG * 2 + (max(col.values()) + 1) * COL
    return raias, nos, lig, geo, largura, len(raias) * RAIA


def _rota(a, b, decisao=False):
    """Linha ortogonal de a para b. Decisão que muda de raia sai por baixo/por cima, para as saídas não se sobreporem."""
    ax, ay, aw, ah = a; bx, by, bw, bh = b
    y1, y2 = ay + ah / 2, by + bh / 2
    x1, x2 = ax + aw, bx
    if abs(y1 - y2) < 1:
        return [(x1, y1), (x2, y2)]
    if decisao:
        cx = ax + aw / 2
        return [(cx, ay + ah if y2 > y1 else ay), (cx, y2), (x2, y2)]
    meio = x2 - 25
    return [(x1, y1), (meio, y1), (meio, y2), (x2, y2)]


def _seta(d, p, q, cor=BORDA):
    import math
    ang = math.atan2(q[1] - p[1], q[0] - p[0]); t = 9 * ESCALA
    d.polygon([q, (q[0] - t * math.cos(ang - .4), q[1] - t * math.sin(ang - .4)),
               (q[0] - t * math.cos(ang + .4), q[1] - t * math.sin(ang + .4))], fill=cor)


def _texto_centro(d, caixa, texto, tam, chars):
    x, y, w, h = caixa
    d.multiline_text((x + w / 2, y + h / 2), _quebrar(texto, chars), font=_fonte(tam), fill=(20, 20, 20), anchor='mm',
                     align='center', spacing=2 * ESCALA)


def _png_bpmn(m, destino):
    raias, nos, lig, geo, W, H = _geo_bpmn(m)
    topo = 40 if m.get('titulo') else 0
    img = Image.new('RGB', (int(W * ESCALA), int((H + topo) * ESCALA)), 'white')
    d = ImageDraw.Draw(img)
    S = lambda *v: [x * ESCALA for x in v]
    if topo:
        d.text((MARG * ESCALA, 10 * ESCALA), m['titulo'], font=_fonte(14), fill=(20, 60, 90))
    for i, r in enumerate(raias):
        y = topo + i * RAIA
        d.rectangle(S(0, y, W - 1, y + RAIA), outline=BORDA, width=ESCALA)
        d.rectangle(S(0, y, CAB, y + RAIA), fill=AZUL, outline=BORDA, width=ESCALA)
        rot = Image.new('RGBA', (int(RAIA * ESCALA), int(CAB * ESCALA)), (0, 0, 0, 0))
        ImageDraw.Draw(rot).text((RAIA * ESCALA / 2, CAB * ESCALA / 2), r[:18], font=_fonte(11), fill=(20, 20, 20), anchor='mm')
        rot = rot.rotate(90, expand=True)
        img.paste(rot, (0, int(y * ESCALA)), rot)
    for l in lig:
        pts = [(x * ESCALA, (y + topo) * ESCALA) for x, y in _rota(geo[l['de']], geo[l['para']], nos[l['de']]['tipo'] == 'decisao')]
        d.line(pts, fill=BORDA, width=ESCALA)
        _seta(d, pts[-2], pts[-1])
        if l.get('texto'):
            px, py = pts[0]
            vertical = abs(pts[1][0] - px) < 1
            d.text((px + 6 * ESCALA, py + (6 if vertical and pts[1][1] > py else -16) * ESCALA), str(l['texto'])[:22], font=_fonte(9), fill=(90, 90, 90))
    for i, n in nos.items():
        x, y, w, h = geo[i]; y += topo
        if n['tipo'] == 'tarefa':
            d.rounded_rectangle(S(x, y, x + w, y + h), radius=8 * ESCALA, fill='white', outline=BORDA, width=ESCALA)
            _texto_centro(d, S(x, y, w, h), n.get('texto', ''), 11, 22)
        elif n['tipo'] == 'decisao':
            cx, cy = x + w / 2, y + h / 2
            d.polygon(S(cx, y, x + w, cy, cx, y + h, x, cy), fill=(255, 250, 225), outline=BORDA)
            d.multiline_text((cx * ESCALA, (y - 4) * ESCALA), _quebrar(n.get('texto', ''), 22), font=_fonte(9), fill=(20, 20, 20), anchor='md', align='center')
        else:
            fim = n['tipo'] == 'fim'
            d.ellipse(S(x, y, x + w, y + h), fill=(255, 228, 225) if fim else (225, 245, 225), outline=BORDA, width=(4 if fim else 1) * ESCALA)
            if n.get('texto'):
                d.multiline_text(((x + w / 2) * ESCALA, (y + h + 3) * ESCALA), _quebrar(n['texto'], 16), font=_fonte(9), fill=(60, 60, 60), anchor='ma', align='center')
    img.save(destino)


def _cel(i, valor, estilo, x, y, w, h, pai='1'):
    return (f'<mxCell id="{i}" value={quoteattr(str(valor))} style="{estilo}" vertex="1" parent="{pai}">'
            f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>')


def _aresta(i, de, para, texto='', estilo='edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;'):
    return (f'<mxCell id="{i}" value={quoteattr(str(texto))} style="{estilo}" edge="1" parent="1" source="{de}" target="{para}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>')


def _drawio(celulas, titulo):
    return ('<mxfile host="agente-li-tasy"><diagram name=' + quoteattr(titulo or 'Diagrama') + '><mxGraphModel dx="1200" dy="800" grid="1" '
            'gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169">'
            '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + ''.join(celulas) + '</root></mxGraphModel></diagram></mxfile>')


def _drawio_bpmn(m):
    raias, nos, lig, geo, W, H = _geo_bpmn(m)
    cs = []
    for i, r in enumerate(raias):
        cs.append(_cel(f'raia{i}', r, 'swimlane;horizontal=0;startSize=%d;html=1;fillColor=#E8F4F8;' % CAB, 0, i * RAIA, W, RAIA))
    estilos = {'tarefa': 'rounded=1;whiteSpace=wrap;html=1;', 'decisao': 'rhombus;whiteSpace=wrap;html=1;fillColor=#FFFAE1;verticalLabelPosition=top;verticalAlign=bottom;',
               'inicio': 'ellipse;html=1;fillColor=#E1F5E1;verticalLabelPosition=bottom;verticalAlign=top;',
               'fim': 'ellipse;html=1;strokeWidth=3;fillColor=#FFE4E1;verticalLabelPosition=bottom;verticalAlign=top;'}
    for i, n in nos.items():
        x, y, w, h = geo[i]
        r = raias.index(n['raia'])
        cs.append(_cel(f'n_{i}', n.get('texto', ''), estilos[n['tipo']], x, y - r * RAIA, w, h, pai=f'raia{r}'))
    for k, l in enumerate(lig):
        cs.append(_aresta(f'l{k}', f"n_{l['de']}", f"n_{l['para']}", l.get('texto', '')))
    return _drawio(cs, m.get('titulo'))


# ------------------------------------------------------------------ UML: casos de uso
def _geo_casos(m):
    atores, casos = m.get('atores') or [], m.get('casos') or []
    if not atores or not casos:
        raise ErroDiagrama('casos_de_uso precisa de atores e casos')
    nomes = [a['nome'] if isinstance(a, dict) else a for a in atores]
    lados = [(a.get('lado', 'esquerda') if isinstance(a, dict) else ('esquerda' if i == 0 else 'direita')) for i, a in enumerate(atores)]
    for c in casos:
        for a in c.get('atores', []):
            if a not in nomes:
                raise ErroDiagrama(f"caso '{c['nome']}': ator '{a}' não declarado")
    CW, CH, PASSO = 230, 46, 62
    H = max(len(casos) * PASSO + 70, 240)
    geo_c = {c['nome']: (190, 50 + i * PASSO, CW, CH) for i, c in enumerate(casos)}
    geo_a = {}
    for lado, x in (('esquerda', 50), ('direita', 190 + CW + 110)):
        deste = [n for n, l in zip(nomes, lados) if l == lado]
        for k, n in enumerate(deste):
            geo_a[n] = (x, H * (k + 1) / (len(deste) + 1) - 35)
    return casos, nomes, geo_c, geo_a, 190 + CW + 190, H, (160, 20, CW + 60, H - 30)


def _png_casos(m, destino):
    casos, nomes, gc, ga, W, H, sis = _geo_casos(m)
    img = Image.new('RGB', (int(W * ESCALA), int(H * ESCALA)), 'white'); d = ImageDraw.Draw(img)
    S = lambda *v: [x * ESCALA for x in v]
    d.rectangle(S(sis[0], sis[1], sis[0] + sis[2], sis[1] + sis[3]), outline=BORDA, width=ESCALA)
    d.text(((sis[0] + sis[2] / 2) * ESCALA, (sis[1] + 6) * ESCALA), m.get('sistema', 'Integração'), font=_fonte(11), fill=(20, 60, 90), anchor='ma')
    for c in casos:
        x, y, w, h = gc[c['nome']]
        for a in c.get('atores', []):
            ax, ay = ga[a]
            d.line(S(ax + (18 if ax < x else -18), ay + 30, x if ax < x else x + w, y + h / 2), fill=BORDA, width=ESCALA)
    for c in casos:
        x, y, w, h = gc[c['nome']]
        d.ellipse(S(x, y, x + w, y + h), fill=AZUL, outline=BORDA, width=ESCALA)
        _texto_centro(d, S(x, y, w, h), c['nome'], 9, 34)
    for n, (x, y) in ga.items():
        d.ellipse(S(x - 9, y, x + 9, y + 18), outline=BORDA, width=ESCALA)
        for seg in ((x, y + 18, x, y + 44), (x - 16, y + 27, x + 16, y + 27), (x, y + 44, x - 13, y + 62), (x, y + 44, x + 13, y + 62)):
            d.line(S(*seg), fill=BORDA, width=ESCALA)
        d.multiline_text((x * ESCALA, (y + 66) * ESCALA), _quebrar(n, 14), font=_fonte(10), fill=(20, 20, 20), anchor='ma', align='center')
    img.save(destino)


def _drawio_casos(m):
    casos, nomes, gc, ga, W, H, sis = _geo_casos(m)
    cs = [_cel('sis', m.get('sistema', 'Integração'), 'rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fillColor=none;', *sis)]
    for k, n in enumerate(nomes):
        x, y = ga[n]
        cs.append(_cel(f'a{k}', n, 'shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;', x - 15, y, 30, 60))
    for k, c in enumerate(casos):
        cs.append(_cel(f'c{k}', c['nome'], 'ellipse;whiteSpace=wrap;html=1;fillColor=#E8F4F8;', *gc[c['nome']]))
        for a in c.get('atores', []):
            cs.append(_aresta(f'l{k}_{nomes.index(a)}', f'a{nomes.index(a)}', f'c{k}', '', 'endArrow=none;html=1;'))
    return _drawio(cs, m.get('titulo'))


# ------------------------------------------------------------------ UML: sequência
def _geo_seq(m):
    parts, msgs = m.get('participantes') or [], m.get('mensagens') or []
    if len(parts) < 2 or not msgs:
        raise ErroDiagrama('sequencia precisa de ao menos 2 participantes e 1 mensagem')
    for g in msgs:
        if g['de'] not in parts or g['para'] not in parts:
            raise ErroDiagrama(f"mensagem '{g.get('texto', '')}': participante inexistente")
    PX, PASSO = 210, 46
    xs = {p: 90 + i * PX for i, p in enumerate(parts)}
    return parts, msgs, xs, 180 + (len(parts) - 1) * PX, 90 + len(msgs) * PASSO + 20, PASSO


def _png_seq(m, destino):
    parts, msgs, xs, W, H, PASSO = _geo_seq(m)
    img = Image.new('RGB', (int(W * ESCALA), int(H * ESCALA)), 'white'); d = ImageDraw.Draw(img)
    S = lambda *v: [x * ESCALA for x in v]
    for p in parts:
        x = xs[p]
        d.rectangle(S(x - 70, 15, x + 70, 55), fill=AZUL, outline=BORDA, width=ESCALA)
        _texto_centro(d, S(x - 70, 15, 140, 40), p, 10, 20)
        for y in range(55, int(H) - 10, 10):
            d.line(S(x, y, x, y + 5), fill=(120, 120, 120), width=ESCALA)
    for i, g in enumerate(msgs):
        y = 90 + i * PASSO
        a, b = xs[g['de']], xs[g['para']]
        if g.get('retorno'):
            for x in range(int(min(a, b)), int(max(a, b)), 12):
                d.line(S(x, y, min(x + 6, max(a, b)), y), fill=BORDA, width=ESCALA)
        else:
            d.line(S(a, y, b, y), fill=BORDA, width=ESCALA)
        _seta(d, (a * ESCALA, y * ESCALA), (b * ESCALA, y * ESCALA))
        d.text(((a + b) / 2 * ESCALA, (y - 4) * ESCALA), f"{i + 1}. {g.get('texto', '')}"[:44], font=_fonte(9), fill=(20, 20, 20), anchor='md')
    img.save(destino)


def _drawio_seq(m):
    parts, msgs, xs, W, H, PASSO = _geo_seq(m)
    cs = []
    for k, p in enumerate(parts):
        cs.append(_cel(f'p{k}', p, 'shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;size=40;fillColor=#E8F4F8;',
                       xs[p] - 70, 15, 140, H - 25))
    for i, g in enumerate(msgs):
        y = 90 + i * PASSO
        est = 'html=1;verticalAlign=bottom;endArrow=open;dashed=1;' if g.get('retorno') else 'html=1;verticalAlign=bottom;endArrow=block;endFill=1;'
        cs.append(f'<mxCell id="m{i}" value={quoteattr(str(i + 1) + ". " + str(g.get("texto", "")))} style="{est}" edge="1" parent="1">'
                  f'<mxGeometry relative="1" as="geometry"><mxPoint x="{xs[g["de"]]}" y="{y}" as="sourcePoint"/>'
                  f'<mxPoint x="{xs[g["para"]]}" y="{y}" as="targetPoint"/></mxGeometry></mxCell>')
    return _drawio(cs, m.get('titulo'))


_TIPOS = {'bpmn': (_png_bpmn, _drawio_bpmn), 'casos_de_uso': (_png_casos, _drawio_casos), 'sequencia': (_png_seq, _drawio_seq)}


def gerar(modelo, pasta, idioma='pt-BR'):
    """Valida e desenha. Devolve {'png', 'drawio', 'json'}; levanta ErroDiagrama se o modelo violar o padrão."""
    tipo = modelo.get('tipo')
    if tipo not in _TIPOS:
        raise ErroDiagrama(f'tipo de diagrama deve ser um de {list(_TIPOS)}')
    os.makedirs(pasta, exist_ok=True)
    base = os.path.join(pasta, modelo.get('nome') or _slug(modelo.get('titulo') or tipo))
    png, drawio = _TIPOS[tipo]
    xml = drawio(modelo)          # valida antes de gravar qualquer coisa
    png(modelo, base + '.png')
    open(base + '.drawio', 'w', encoding='utf8').write(xml)
    json.dump(modelo, open(base + '.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    with Image.open(base + '.png') as im:
        largura_cm = round(im.width / ESCALA / 38, 1)  # tamanho natural: texto de 10 px fica legível no Word
    return {'png': base + '.png', 'drawio': base + '.drawio', 'json': base + '.json', 'largura_cm': largura_cm}

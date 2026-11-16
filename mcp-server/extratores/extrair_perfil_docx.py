"""Extrai o perfil de formatação de um template .docx (página, margens, fontes, estilos, cabeçalho/rodapé).

Uso: python extrair_perfil_docx.py <template.docx> <saida.json>
Só lê o XML do .docx (biblioteca padrão). Serve de referência para o gerador e para validar que o
documento gerado manteve a formatação do template oficial.
"""
import json, re, sys, zipfile

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
import xml.etree.ElementTree as ET

def attr(el, name):
    return el.get(W + name) if el is not None else None

def run_props(rpr):
    if rpr is None:
        return {}
    out = {}
    f = rpr.find(W + 'rFonts')
    if f is not None:
        out['fonte'] = attr(f, 'ascii') or attr(f, 'hAnsi') or attr(f, 'asciiTheme')
    sz = rpr.find(W + 'sz')
    if sz is not None:
        out['tamanho_pt'] = int(attr(sz, 'val')) / 2
    if rpr.find(W + 'b') is not None and attr(rpr.find(W + 'b'), 'val') not in ('0', 'false'):
        out['negrito'] = True
    if rpr.find(W + 'i') is not None and attr(rpr.find(W + 'i'), 'val') not in ('0', 'false'):
        out['italico'] = True
    c = rpr.find(W + 'color')
    if c is not None and attr(c, 'val') not in (None, 'auto'):
        out['cor'] = '#' + attr(c, 'val')
    return out

def para_props(ppr):
    if ppr is None:
        return {}
    out = {}
    sp = ppr.find(W + 'spacing')
    if sp is not None:
        for k, n in (('before', 'espaco_antes_pt'), ('after', 'espaco_depois_pt')):
            if attr(sp, k):
                out[n] = int(attr(sp, k)) / 20
        if attr(sp, 'line'):
            out['entrelinha'] = int(attr(sp, 'line')) / 240
    jc = ppr.find(W + 'jc')
    if jc is not None:
        out['alinhamento'] = attr(jc, 'val')
    if ppr.find(W + 'numPr') is not None:
        out['numerado'] = True
    return out

def twip_cm(v):
    return round(int(v) / 567, 2) if v else None

def main(src, dst):
    z = zipfile.ZipFile(src)
    doc = ET.fromstring(z.read('word/document.xml'))
    styles = ET.fromstring(z.read('word/styles.xml'))
    perfil = {'template': src.split('/')[-1]}
    sect = doc.find('.//' + W + 'sectPr')
    if sect is not None:
        pg, mar = sect.find(W + 'pgSz'), sect.find(W + 'pgMar')
        perfil['pagina'] = {'largura_cm': twip_cm(attr(pg, 'w')), 'altura_cm': twip_cm(attr(pg, 'h')),
                            'orientacao': attr(pg, 'orient') or 'portrait'}
        perfil['margens_cm'] = {k: twip_cm(attr(mar, k)) for k in ('top', 'bottom', 'left', 'right', 'header', 'footer')}
    if 'word/theme/theme1.xml' in z.namelist():
        th = z.read('word/theme/theme1.xml').decode('utf-8', 'ignore')
        maj = re.search(r'<a:majorFont><a:latin typeface="([^"]*)"', th)
        mnr = re.search(r'<a:minorFont><a:latin typeface="([^"]*)"', th)
        perfil['fontes_tema'] = {'titulos': maj.group(1) if maj else None, 'corpo': mnr.group(1) if mnr else None}
    dd = styles.find(W + 'docDefaults')
    if dd is not None:
        perfil['padrao'] = {**run_props(dd.find('.//' + W + 'rPr')), **para_props(dd.find('.//' + W + 'pPr'))}
    used = set(re.findall(r'w:(?:pStyle|tStyle|rStyle) w:val="([^"]+)"', z.read('word/document.xml').decode('utf-8', 'ignore')))
    est = {}
    for s in styles.findall(W + 'style'):
        sid = attr(s, 'styleId')
        if sid not in used and not re.match(r'(Heading|Ttulo|Titulo|T\xedtulo)\d|Normal|Title|TOC', sid or ''):
            continue
        nome = s.find(W + 'name')
        base = s.find(W + 'basedOn')
        est[sid] = {'nome': attr(nome, 'val'), 'tipo': attr(s, 'type'), 'baseado_em': attr(base, 'val'),
                    **run_props(s.find(W + 'rPr')), **para_props(s.find(W + 'pPr'))}
    perfil['estilos_usados'] = est
    hf = {}
    for n in z.namelist():
        if re.match(r'word/(header|footer)\d+\.xml$', n):
            x = z.read(n).decode('utf-8', 'ignore')
            hf[n.split('/')[-1]] = {'texto': ' '.join(t for t in re.findall(r'<w:t[^>]*>([^<]*)</w:t>', x) if t.strip())[:300],
                                     'tem_imagem': 'graphicData' in x or '<v:imagedata' in x,
                                     'campos': sorted(set(re.findall(r'instr(?:Text>|="\s*)\s*(\w+)', x)))}
    perfil['cabecalhos_rodapes'] = hf
    perfil['controles_lista_suspensa'] = len(re.findall(r'<w:dropDownList', z.read('word/document.xml').decode('utf-8', 'ignore')))
    perfil['sumario_automatico'] = 'TOC \\' in z.read('word/document.xml').decode('utf-8', 'ignore')
    json.dump(perfil, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(dst, len(est), 'estilos')

main(sys.argv[1], sys.argv[2])

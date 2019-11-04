import json
import requests
import re
import orodja

# URL glavne strani z nepremičninami
# https://www.nepremicnine.net/oglasi-oddaja/slovenija/stanovanje/

# mapa, v katero bomo shranili zajete strani
# 'zajeti-podatki'

# mapa, v katero bomo shranili podatke
# 'obdelani-podatki'

# ime CSV datoteke v katero bomo shranili podatke
# 'stanovanja.csv'

# shranjene spletne strani dne 28.10.2019

# regularni izraz, ki poišče vse bloke na strani z več oglasi
vzorec_bloka = re.compile(
    r'<div class="oglas_container oglasbold oglasi\d{3}".*?'
    r'<div class="clearer"></div>',
    flags=re.DOTALL
)

# regularni izraz, ki poišče blok na strani od vsakega oglasa posebaj
vzorec_bloka2 = re.compile(
    r'<div class="clearer"></div><div class="more_info">Posredovanje.*?'
    r'data-layout="button_count" data-size="small"',
    flags=re.DOTALL
)

# regularni izrazi za podatke iz oglasa
vzorec_stanovanja = re.compile(
    r'id="o(?P<id>\d{7})".*?'
    r'content="(?P<url>https://www.nepremicnine.net/oglasi-oddaja/(?P<ime>[\w\-]+)_\d{7}/)" />.*?'
    r'<div class="kratek" itemprop="description">(?P<opis>[^\n]*)</div>.*?' #vse razen /n
    r'<span class="velikost" lang="sl">(?P<velikost>\d*,?\d*) m2</span><br />.*?'
    r'<span class="cena">(?P<cena>.*?)\s*?&euro;.*?',
    flags=re.DOTALL
)

vzorec_tip = re.compile(
    r'<span class="tipi">(?P<tip>[a-zA-Z]+)</span></span>.*?',
    flags=re.DOTALL
)

vzorec_nadstropje = re.compile(
    r'<span class="atribut">Nadstropje: <strong>(?P<nadstropje>[\w\+\\]+)</strong>/.*?',
    flags=re.DOTALL
)

vzorec_agencija = re.compile(
    r'<span class="agencija">(?P<agencija>.*)</span>.*?',
    flags=re.DOTALL
)

vzorec_leto = re.compile(
    r'<span class="atribut leto">Leto: <strong>(?P<leto>\d{4}).*?',
    flags=re.DOTALL
)

# regularni izraz, ki iz kratkega opisa ugotovi, 
# kdaj je bilo stanovanje adaptirano
vzorec_adaptacija = re.compile(
    r'adaptiran\w*?\sl\.\s(?P<adaptirano>\d{4})',
    flags=re.DOTALL
)

# regularni izraz, ki pridobi podatke iz strani od oglasa
vzorec_stanovanja2 = re.compile( 
    r'Regija: (?P<regija>[-\w\.\s]+).*?'
    r'Upravna enota: (?P<mesto>[-\w\.\s]+)',
    flags=re.DOTALL
)

# funkcija, ki izloči podatke iz bloka oglasa
def izloci_podatke_stanovanja(blok):
    ''' Iz bloka izloči vse iskane podatke in jih spravi v slovar.'''
    stanovanje = {}
    ujemanje = vzorec_stanovanja.search(blok)
    if ujemanje is not None:
        stanovanje = ujemanje.groupdict()

        stanovanje['id'] = int(stanovanje['id'])
        stanovanje['ime'] = str(stanovanje['ime'])
        stanovanje['url'] = stanovanje['url']
        stanovanje['opis'] = str(stanovanje['opis']).replace('&quot;', '')
        stanovanje['velikost'] = float(stanovanje['velikost'].replace(',', '.'))
        stanovanje['cena'] = float(stanovanje['cena'].replace('.', '').replace(',', '.'))

        '''Zabeležimo tip stanovanja, če je omenjen'''
        tip = vzorec_tip.search(blok)
        if tip:
            stanovanje['tip'] = str(tip['tip'])
        else:
            stanovanje['tip'] = None
        
        '''Zabeležimo nadstropje, če je omenjeno'''
        nadstropje = vzorec_nadstropje.search(blok)
        if nadstropje:
            stanovanje['nadstropje'] = str(nadstropje['nadstropje'])
        else:
            stanovanje['nadstropje'] = None

        '''Zabeležimo agencijo, če je omenjena'''
        agencija = vzorec_agencija.search(blok)
        if agencija:
            stanovanje['agencija'] = str(agencija['agencija'])
        else:
            stanovanje['agencija'] = None

        '''Zabeležimo leto adaptacije, če je omenjeno'''
        adaptirano = vzorec_adaptacija.search(blok)
        if adaptirano:
            stanovanje['adaptirano'] = int(adaptirano['adaptirano'])
        else:
            stanovanje['adaptirano'] = None

        '''Zabeležimo leto gradnje, če je omenjeno'''
        leto = vzorec_leto.search(blok)
        if leto:
            stanovanje['leto'] = int(leto['leto'])
        else: 
            stanovanje['leto'] = None
        return stanovanje

# funkcija, ki izloči podatke iz spletne strani od oglasa
def izloci_podatke2(blok2):
    dodatni_podatki = {}
    ujemanje = vzorec_stanovanja2.search(blok2)
    if ujemanje is not None:
        dodatni_podatki = ujemanje.groupdict()

        dodatni_podatki['regija'] = str(dodatni_podatki['regija'].strip())
        dodatni_podatki['mesto'] = str(dodatni_podatki['mesto'].strip())
    return dodatni_podatki

# funkcija, ki iz zajete strani oglasa, izloči podatke
# na teh blokih uporabi funkcijo izloci_podatke 2
def dodatni_podatki_na_strani(url, id):
    ime_datoteke =f"zajeti-podatki/{id}.html"
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka2.finditer(vsebina):
        return (izloci_podatke2(blok.group(0)))

# funkcija, ki iz zajete strani, izloči podatke
# na teh blokih uporabi funkcijo izloci_podatke 
# in v slovar doda še podatke o regiji in mestu
def stanovanje_na_strani(st_strani):
    url = (
        "https://www.nepremicnine.net/"
        "oglasi-oddaja/slovenija/"
        f"stanovanje/{st_strani}/"
        )
    ime_datoteke = f"zajeti-podatki/stanovanja-{st_strani}.html"
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)

    for blok in vzorec_bloka.finditer(vsebina):
        url2 = str(izloci_podatke_stanovanja(blok.group(0)).get("url"))
        id = izloci_podatke_stanovanja(blok.group(0)).get("id")
        drugo = dodatni_podatki_na_strani(url2, id)
        stanovanje = izloci_podatke_stanovanja(blok.group(0))
        stanovanje.update(drugo)
        yield stanovanje
        
# for zanka, ki uporabi funkcijo stanovanje_na_strani na vsaki
# spletni strani in slovar s podatki oglasa doda v seznam stanovanja
stanovanja = []
for st_strani in range(1, 32):
    for stanovanje in stanovanje_na_strani(st_strani):
        stanovanja.append(stanovanje)

# csv datoteka
orodja.zapisi_csv(
    stanovanja,
    ['id', 'ime','regija', 'mesto','velikost','cena','tip','leto','adaptirano','nadstropje','agencija','opis','url'],
    'obdelani-podatki/stanovanja.csv'
)

# json datoteka
orodja.zapisi_json(stanovanja, 'obdelani-podatki/stanovanja.json')

# Projektna naloga pri programiranju 1: Analiza stanovanj
Pri projektni nalogi bom analizirala stanovanja, ki se oddajajo v Sloveniji. 
Podatke bom pridobila na spletni strani [nepremicnine.net](www.nepremicnine.net).

Zajeti podatki:

* id 
* url
* kratek opis 
* velikost 
* cena
* agencija
* leto adaptacije
* leto izgradnje
* regija
* mesto

Hipoteze:
* Kje so najdražja oz. najcenejša stanovanja
* Kako stara so stanovanja in kdaj so bila adaptirana
* Kje so najstarejša oz. najnovejša stanovanja
* Kako se višina mesečne najemnine spreminja v odvisnosti od kraja, velikosti, starosti in tipa
* Ali so stanovanja, ki jih oddajajo agencije dražja, katere so najdražje agencije

CSV datoteka z zgoraj navedenimi zajetimi podatki se nahaja v mapi `podatki`. Podatke sem pridobila s pomočjo python datotek `zajemi_stanovanja.py` in `orodja.py`. V mapi `spletne-strani` se nahajajo html datoteke.
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
* Katera regija ima najdražja oz. najcenejša stanovanja?
* Katero mesto ima najdražja oz. najcenejša stanovanja?
* Ali so novejša oz. adaptirana stanovanja stanovanja dražja?
* Ali se cena povečuje z velikostjo?
* Katera regija ima največ stanovanj?
* Ali so stanovanja, ki jih oddajajo agencije dražje, katere agencije imajo najdražja stanovanja? 

#
CSV datoteka z zgoraj navedenimi zajetimi podatki se nahaja v mapi `podatki`. Podatke sem pridobila s pomočjo python datotek `zajemi_stanovanja.py` in `orodja.py`. V mapi `spletne-strani` se nahajajo html datoteke.
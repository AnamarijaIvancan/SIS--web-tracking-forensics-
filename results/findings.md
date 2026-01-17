# Zaključci i zapažanja (Findings)

U ovom projektu provedena je detaljna analiza web praćenja korisnika na temelju
snimljenog mrežnog prometa. Cilj analize bio je identificirati različite oblike
praćenja korisnika, s posebnim naglaskom na fingerprinting tehnike koje ne koriste
klasične kolačiće.

## Prikupljanje i pohrana podataka

Mrežni promet prikupljen je korištenjem alata **mitmproxy**, pri čemu su zabilježeni
HTTP zahtjevi i odgovori tijekom posjeta različitim web stranicama. Snimljeni promet
spremljen je u datoteku `traffic.mitm`.

Iz snimljenog prometa izdvojeni su relevantni podaci (URL-ovi, domene, HTTP zaglavlja,
kolačići) te su pohranjeni u SQLite bazu podataka `cookies.db`. Baza sadrži tablice
za stranice (`pages`), kolačiće (`cookies`), trackere (`trackers`) i njihove međusobne
poveznice (`mapping`).

## Analiza kolačića i trackera

Tijekom analize utvrđeno je da velik broj analiziranih stranica ne koristi klasične
third-party kolačiće. Zbog toga tablice povezane s third-party kolačićima i trackerima
u početnoj fazi analize ostaju djelomično ili potpuno prazne. To upućuje na činjenicu
da se praćenje korisnika u velikoj mjeri odvija bez oslanjanja na kolačiće.

## Detekcija fingerprinting tehnika

Kako bi se identificiralo cookie-less praćenje, provedena je analiza HTML i JavaScript
odgovora iz snimljenog mrežnog prometa. Detekcija se temelji na heuristikama koje traže
poznate JavaScript API-je i obrasce povezane s fingerprintingom, kao što su:
- Canvas i WebGL API-ji
- AudioContext
- Informacije o ekranu i rezoluciji
- Informacije o hardveru i pregledniku
- MediaDevices i srodni API-ji

Stranice i domene kod kojih su pronađeni takvi obrasci označene su u bazi podataka
stupcem `fingerprinting = 1`. Uz to su spremljene i dodatne informacije o pronađenim
ključnim riječima te vremenu detekcije.

Rezultati analize pokazuju da je fingerprinting detektiran na više poznatih domena,
uključujući oglašivačke i analitičke servise, ali i društvene mreže. To potvrđuje da
se praćenje korisnika često provodi putem skripti trećih strana učitanih na različitim
web stranicama.

## Vizualizacija odnosa stranica i trackera

Na temelju podataka iz baze generirani su strukturirani podaci za vizualizaciju.
Vizualizacija prikazuje mrežu odnosa između web stranica i tracker domena, gdje su:
- web stranice prikazane kao jedan tip čvorova
- tracker domene prikazane kao drugi tip čvorova
- veze predstavljaju komunikaciju između stranice i treće strane

Osim mrežnog grafa, izrađena je i stupčasta vizualizacija koja prikazuje stranice
rangirane prema broju detektiranih fingerprinting trackera. Vizualizacije jasno
pokazuju koje stranice imaju najveći intenzitet praćenja.

## Zaključak

Rezultati projekta pokazuju da suvremeno web praćenje često ne ovisi isključivo o
kolačićima, već se u velikoj mjeri oslanja na fingerprinting tehnike koje su korisniku
teže uočljive i teže ih je blokirati. Analiza mrežnog prometa u kombinaciji s
pohranom podataka i vizualizacijom omogućuje jasan uvid u razinu praćenja pojedinih
web stranica.

Razvijeni sustav pruža osnovu za daljnje proširenje analize, uključujući precizniju
klasifikaciju trackera, kvantitativno mjerenje intenziteta praćenja te automatizirano
generiranje izvještaja o privatnosti web stranica.


## Fingerprinting mapping to pages

- Total flows: 1814
- HTML/JS scanned: 715
- FP tracker domains detected: 25
- Requests with Referer (to FP trackers): 1017
- Requests with Origin (to FP trackers): 417
- Mapped hits (Referer/Origin -> page): 774
- Pages marked fingerprinting=1: 10


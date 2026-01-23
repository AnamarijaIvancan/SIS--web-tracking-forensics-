# Web Tracking Forensics

## Opis projekta
Ovaj projekt istražuje kako kolačići (cookies) i skripte prate korisnike na internetu.  
Cilj je izraditi sustav koji:
1. Nadgleda mrežni promet i otkriva praćenje (cookie-based i cookie-less).  
2. Bilježi i klasificira ponašanja praćenja (third-party cookies, beacons, fingerprinting).  
3. Sprema podatke u bazu radi kasnije analize.  
4. Vizualizira veze između web stranica i trećih strana koje prate korisnika.

## Članovi tima
- Gabriel Vesel - Snimanje i analiza HTTP/HTTPS prometa, identifikacija kolačića i osnovnih oblika praćenja korisnika.
- Jakov Bišćan  - Implementacija skripti za obradu prikupljenih podataka, pohrana u bazu podataka i priprema podataka za daljnju analizu.
- Anamarija Ivančan - Razvoj logike za detekciju third-party trackera i browser fingerprintinga te njihova klasifikacija prema vrsti praćenja.
- Karlo Jurič - Izrada vizualizacija rezultata (grafovi, HTML prikazi), priprema izvještaja i prezentacija projekta.

## Cilj projekta
Razviti okvir (framework) koji omogućuje:
- Praćenje i prikupljanje podataka o mrežnim zahtjevima.  
- Detekciju različitih oblika praćenja korisnika.  
- Pohranu prikupljenih informacija u bazu podataka.  
- Prikaz odnosa između web stranica i trackera putem grafova.

## Struktura projekta
project-name/
│
├── README.md
├── .gitignore
│
├── docs/
│ ├── theory.md # Teorijska podloga
│ ├── plan.md # Plan implementacije
│ ├── report.md # Završno izvješće
│ └── references.md # Reference i izvori
│
├── implementation/
│ ├── setup.md # Upute za pokretanje
│ ├── src/ # Kod-intenzitet
│ └── tests/ # Kod-za report
│
├── results/
│ ├── screenshots/ # Slike i grafovi rezultata
│ ├── logs/ # Log datoteke
│ └── findings.md # Zaključci i otkrića
│
└── presentation/
└── slides.pdf/pptx # Završna prezentacija



##  Pokretanje projekta
Upute za pokretanje bit će dodane u datoteku `implementation/setup.md`.

##  Dokumentacija
Teorijski dio, plan i završno izvješće nalaze se u mapi `docs/`.

##  Rezultati
Grafovi, slike i zapažanja nalaze se u mapi `results/`.

##  Prezentacija
Završna prezentacija projekta bit će spremljena u mapi `presentation/`.

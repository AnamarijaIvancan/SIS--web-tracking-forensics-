# Upute za pokretanje projekta

Projekt služi za analizu web praćenja korištenjem mrežnog prometa snimljenog alatom
mitmproxy. Analiza uključuje pohranu HTTP zahtjeva i kolačića u SQLite bazu podataka,
detekciju fingerprinting tehnika (cookie-less tracking) te vizualizaciju odnosa između
web stranica i trećih strana (trackera).

Projekt se pokreće iz root direktorija repozitorija.

Za rad na projektu potrebno je imati instaliran:
- Python (verzija 3.10 ili novija)
- mitmproxy
- Git
- Visual Studio Code (preporučeno)

Potrebne Python biblioteke instaliraju se naredbom:
```bash
pip install mitmproxy tldextract

Mrežni promet se snima pomoću mitmproxy alata, pri čemu se generira datoteka traffic.mitm.
Web preglednik mora biti konfiguriran da koristi proxy 127.0.0.1:8080.

Snimljeni promet se zatim obrađuje skriptom koja podatke sprema u SQLite bazu cookies.db:

python implementation/src/mitm_to_sqlite.py

Detekcija fingerprinting tehnika provodi se analizom HTML i JavaScript odgovora iz
snimljenog prometa. Rezultati se upisuju u tablicu pages u bazi podataka, a dodatni
log se sprema u JSON datoteku:

python implementation/src/detect_fingerprinting.py

Na temelju podataka iz baze generira se datoteka za vizualizaciju odnosa između stranica
i trackera:
python implementation/src/export_for_visualization.py

Vizualizacija se prikazuje otvaranjem HTML datoteke:

results/visualization/visualization.html

preko Live Server ekstenzije u Visual Studio Codeu ili direktno u web pregledniku.

Svi generirani grafovi, slike i logovi nalaze se u direktoriju results/.

# Teorijska podloga
Ovdje dolazi teorijski dio projekta – objašnjenje pojmova praćenja, kolačića i skripti.
# Forenzika web praćenja: analiza kolačića, skripti i mrežnog prometa

## Uvod

Web praćenje predstavlja skup tehnika i mehanizama kojima web stranice i povezane treće strane prikupljaju informacije o korisnicima tijekom njihovog pregledavanja interneta. U suvremenom digitalnom okruženju gotovo svaka web stranica koristi neku vrstu praćenja, bilo u svrhu funkcionalnosti, personalizacije sadržaja, analitike ili digitalnog oglašavanja. Iako takvi mehanizmi omogućuju poboljšano korisničko iskustvo i optimizaciju usluga, istovremeno otvaraju značajna pitanja vezana uz privatnost i sigurnost korisnika.

Istraživanja provedena na velikom broju web stranica pokazuju da korisnici često nisu svjesni količine podataka koji se prikupljaju u pozadini, niti broja različitih entiteta koji sudjeluju u toj razmjeni podataka. Englehardt i Narayanan (2016) ukazuju na široku rasprostranjenost online trackera i složene mreže trećih strana uključenih u praćenje korisnika. U tom kontekstu, web forenzika se pojavljuje kao disciplina koja se bavi analizom digitalnih tragova nastalih korištenjem web preglednika, s ciljem rekonstrukcije aktivnosti, razumijevanja načina prijenosa podataka i identifikacije potencijalnih narušavanja privatnosti.

Cilj ovog projekta je otkriti, analizirati i prikazati mehanizme web praćenja kroz forenzičku analizu kolačića, skripti i mrežnog prometa, te procijeniti kakve tragove takve aktivnosti ostavljaju iza sebe.

---

## Praćenje korisnika putem kolačića

Jedan od temeljnih mehanizama web praćenja su kolačići, male tekstualne datoteke koje web preglednik pohranjuje na korisnikov uređaj. Kolačići se automatski šalju natrag poslužitelju pri svakom sljedećem zahtjevu prema istoj domeni, čime omogućuju identifikaciju sesije ili korisnika.

First-party kolačići postavljaju se od strane domene koju korisnik izravno posjećuje. Njihova osnovna svrha je omogućavanje funkcionalnosti web aplikacije, poput održavanja prijavljene sesije, pamćenja korisničkih postavki ili poboljšanja sigurnosti. Iako se često smatraju manje invazivnima, first-party kolačići i dalje omogućuju detaljno praćenje korisnikovog ponašanja unutar jedne web stranice, uključujući obrasce navigacije i interakcije sa sadržajem.

Third-party kolačići, s druge strane, postavljaju se od strane domena koje nisu izravno posjećene od strane korisnika, već su učitane putem ugrađenih skripti, oglasa ili analitičkih servisa. Njihova glavna karakteristika je mogućnost praćenja korisnika kroz više različitih web stranica, čime se omogućuje izgradnja opsežnih profila korisničkih interesa i ponašanja. Upravo zbog takvih mogućnosti, third-party kolačići predstavljaju značajan rizik za privatnost te su predmet sve strožih zakonskih regulacija, uključujući Opću uredbu o zaštiti podataka (GDPR).

---

## Skripte i druge metode praćenja

Osim kolačića, moderne web stranice intenzivno koriste JavaScript skripte za prikupljanje dodatnih podataka o korisnicima. Te skripte mogu bilježiti različite oblike interakcije, poput klikova, trajanja boravka na stranici, pomicanja sadržaja, kao i tehničke karakteristike uređaja i preglednika. Prikupljeni podaci često se u stvarnom vremenu šalju udaljenim poslužiteljima, gdje se dalje obrađuju u analitičke ili marketinške svrhe.

Najčešći primjeri takvih sustava su Google Analytics, Facebook Pixel i TikTok Analytics, koji omogućuju praćenje korisnika čak i u slučajevima kada su kolačići ograničeni ili onemogućeni. Uz standardne skripte, sve češće se koriste i napredne tehnike praćenja koje dodatno otežavaju kontrolu privatnosti. Browser fingerprinting omogućuje identifikaciju korisnika na temelju kombinacije karakteristika poput vrste preglednika, operacijskog sustava, rezolucije ekrana, jezika sustava i drugih parametara. Tracking pixels, poznati i kao web beacons, predstavljaju nevidljive elemente koji služe za bilježenje učitavanja stranica ili otvaranja sadržaja. Local storage i tzv. supercookies omogućuju dugotrajnu pohranu podataka koja može ostati prisutna čak i nakon brisanja klasičnih kolačića.

---

## Posljedice praćenja i utjecaj na privatnost

Kombinacija kolačića, skripti i naprednih metoda praćenja omogućuje prikupljanje velike količine podataka o korisnicima, često bez njihove potpune svijesti o opsegu takvog praćenja. Dugoročno, takvi podaci mogu se koristiti za izgradnju detaljnih profila koji uključuju interese, navike pregledavanja, obrasce ponašanja i potencijalno osjetljive informacije.

Ovakva razina praćenja ima izravan utjecaj na privatnost korisnika i postavlja pitanja transparentnosti, informiranog pristanka i zakonitosti obrade podataka. Iako zakonodavni okviri poput GDPR-a nastoje osigurati veću kontrolu korisnika nad vlastitim podacima, u praksi se često pojavljuju izazovi u provedbi i razumijevanju tih mehanizama od strane krajnjih korisnika.

---

## Forenzička analiza web praćenja

Forenzička analiza web praćenja usmjerena je na sustavno proučavanje tragova koje web stranice i povezani servisi ostavljaju tijekom interakcije s korisnikom. Takva analiza nastoji odgovoriti na pitanja tko, kada i na koji način prati korisnika, kao i koje se vrste podataka razmjenjuju u pozadini.

Analizom kolačića i mrežnog prometa moguće je rekonstruirati odnose između web stranica i uključenih trackera te identificirati tokove podataka prema trećim stranama. Prikupljanje i analiza mrežnog prometa omogućeni su pomoću specijaliziranih alata koji bilježe HTTP zahtjeve i odgovore, čime se stvaraju forenzički artefakti pogodni za daljnju analizu.

---

## Svrha forenzičke aktivnosti i rezultati analize

Svrha forenzičke aktivnosti u ovom projektu je identificirati skripte i domene koje sudjeluju u praćenju korisnika, analizirati učestalost i intenzitet takvog praćenja te vizualno prikazati odnose između web stranica i trackera. Rezultati forenzičke analize uključuju popis uključenih skripti, statističke podatke o broju i vrsti kolačića, mrežne grafove povezanih stranica i trackera te procjenu rizika za privatnost korisnika.

Dobiveni rezultati mogu poslužiti kao temelj za procjenu potencijalnih povreda privatnosti i kao dokazni materijal u kontekstu regulatornih zahtjeva, uključujući i moguće narušavanje GDPR-a.

---

## Plan i cilj praktičnog dijela projekta

Praktični dio projekta usmjeren je na razvoj okvira za analizu web trackinga i privatnosti korisnika. Cilj tog okvira je omogućiti snimanje i analizu mrežnog prometa web preglednika, klasifikaciju kolačića i trackera, detekciju naprednih metoda praćenja te pohranu prikupljenih podataka u strukturiranu bazu podataka radi kasnije forenzičke analize i usporedbe.

Poseban naglasak stavljen je na vizualizaciju odnosa između web stranica i trackera te na generiranje izvještaja koji jasno prikazuju razinu praćenja, tzv. intenzitet praćenja, za svaku analiziranu stranicu. Time se teorijski koncepti web praćenja povezuju s konkretnim, mjerljivim primjerima iz stvarnog mrežnog prometa.

---

## Metodologija (Practical Implementation)

Metodologija projekta temelji se na pasivnoj forenzičkoj analizi stvarnog mrežnog prometa generiranog tijekom korištenja web stranica. Analiza se provodi na razini web preglednika, bez zaobilaženja sigurnosnih mehanizama ili dešifriranja TLS komunikacije, čime se osigurava etički i zakonit pristup prikupljanju podataka.

Tijekom analize bilježi se mrežni promet koji nastaje prilikom učitavanja web stranica i interakcije korisnika s njima. Poseban naglasak stavlja se na HTTP zahtjeve i odgovore, kolačiće koji se postavljaju tijekom sesije te domene s kojima preglednik komunicira. Prikupljeni podaci pohranjuju se u strukturiranom formatu kako bi se omogućila kasnija obrada i usporedba različitih scenarija korištenja, poput pristupa stranici prije i nakon prijave korisnika.

Analiza uključuje razlikovanje first-party i third-party elemenata usporedbom domena web stranice i domena iz kojih potječu pojedini zahtjevi ili kolačići. Na temelju te klasifikacije moguće je identificirati vanjske servise koji sudjeluju u praćenju korisnika. Dodatno se analizira ponašanje JavaScript skripti s ciljem detekcije telemetry zahtjeva i indikatora naprednih metoda praćenja, poput browser fingerprintinga.

Svi prikupljeni podaci pohranjuju se u relacijsku bazu podataka, što omogućuje strukturiranu forenzičku analizu, izvođenje statistika i generiranje vizualnih prikaza. Vizualizacijom odnosa između web stranica i trackera omogućuje se jasan prikaz mreže praćenja i intenziteta razmjene podataka.

---

## Zaključak

Rezultati ovog projekta pokazuju da web praćenje predstavlja znatno kompleksniji i intenzivniji proces nego što većina korisnika pretpostavlja. Forenzička analiza mrežnog prometa, kolačića i skripti otkriva velik broj zahtjeva, domena i mehanizama koji djeluju u pozadini čak i tijekom osnovnog korištenja web stranica.

Poseban učinak projekta ogleda se u tzv. “paranoja” ili awareness efektu, pri kojem korisnici postaju svjesni količine podataka koja se prikuplja bez njihove aktivne uključenosti. Ovaj efekt nije usmjeren na stvaranje straha, već na povećanje transparentnosti i razumijevanja modernog web ekosustava. Uvid u stvarni mrežni promet omogućuje korisnicima i istraživačima da kritički sagledaju odnose između funkcionalnosti, privatnosti i kontrole nad osobnim podacima.

Projekt potvrđuje važnost forenzičke analize kao alata za razumijevanje web praćenja te naglašava potrebu za daljnjim razvojem alata i metoda koje će korisnicima omogućiti veću kontrolu i informiranost u digitalnom prostoru.

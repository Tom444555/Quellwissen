# Gegenprüfung region_saarland.json (26.11.2026)

Geprüft: alle `kategorie: "Störungsnummern"` (ohne qui-werke, heu-*, sb-*, st-energis-*) sowie sr-ukw-sr1, sr-ukw-sr3, sr-ukw-kultur, swl-leuchtturm-*, z-oberste.
Methode: Quelle per curl (Proxy) geladen, Text Zeichen für Zeichen verglichen; Bild-Seiten der PDF gerendert und angesehen.

| id | Ergebnis | Befund |
|---|---|---|
| vse-netz | ✔ | Strom 0681 4030-2611, Gas -2610, Wasser -2613 wörtlich auf vse-verteilnetz.de; keine Zeitangabe auf der Seite (Warnung stimmt). |
| pfw-netz | ✔ | „Ihre Auskunft bei Stromausfall … Störung online melden … Hotline: 0800 797 77 77“; keine Zeiten genannt. |
| kew-nk | ✔ | „Bereitschaftsdienst rund um die Uhr“; Gas/Strom/Wasser/Fernwärme +49 6821 200 - 100/101/102/103 (Quelle mit Leerzeichen um den Bindestrich). |
| swsls | ✔ | „rund um die Uhr … 24 Stunden am Tag“; 9596-301/-302/-303/-304, E-Ladesäulen 0800 0670 000. Hinweis: „rund um die Uhr“ bezieht sich im Satz auf Strom, Erdgas, Trinkwasser; Glasfaser/E-Ladesäulen stehen nur in derselben Liste. |
| swvk-netz | ✔ | „Bei Störungen und Notfällen erreichen Sie uns jederzeit unter der Nummer +49 6898 150-222“; stoerung@swvk.de „(Bei akuten Störungen bitte telefonisch melden)“. |
| swh-hom | ✔ | Störungshotline „0800 / 789 4662“, Telefonzentrale „06841 / 694-0“ (Kontaktseite und Startseite). Keine Sparten/Zeiten. |
| swigb | ✔ (Ergänzung möglich) | 06894 9552-400 / 9552-0, Reinhold-Becker-Straße 1, 66386 St. Ingbert bestätigt. Die Unterseite https://www.sw-igb.de/notfallnummer/ sagt: „In Not- und Störungsfällen steht Ihnen unsere Hotline rund um die Uhr zur Verfügung.“ → Warnung „Erreichbarkeitszeiten nicht angegeben“ ist überholt. |
| swd-dil | ✔ | „Im Fall einer Störung in den Bereichen Strom, Erdgas oder Wasser ist unser Bereitschaftsdienst rund um die Uhr für euch erreichbar. 06831 9747-0“. |
| swm-mzg | ✔ | „Störungsmeldung Erdgas, Wasser und Wärme Tel.: 06861 7006-111 / Strom (energis) Tel.: 0681 9069-2611“; keine Zeiten. |
| swb-bex | ✔ | „Kundenservice 06826-9202-333 / für Notfälle 06826 9202-300“; keine Sparten/Zeiten. |
| sws-sul | ✔ | „Rufbereitschaft für alle Störungsfälle rund um die Uhr unter: 06897 / 575-0“; Gasgeruch: „von einem Telefonanschluss oder Handy außerhalb des Hauses“. |
| wvw-wnd | ✗ | Website ist jetzt abrufbar. https://wvw-wnd.de/ und https://wvw-wnd.de/kontakt/ nennen „24h-Service-Hotline +49 (0) 6851 - 8003-0“ (Kopfzeile schreibt auch „80030“). Die PDF-Angabe 06851/8003-0 stimmt; „nicht gefunden / nicht abrufbar“ ist überholt → wert „06851 8003-0“ (24h-Service-Hotline), Quelle WVW-Startseite. Hinweis: Telefonzentrale besetzt nur Mo–Do 8–16, Fr 8–13 Uhr; dass die 24h-Hotline ausdrücklich für Störungen gilt, steht nicht wörtlich da. |
| sr-ukw-sr1 | ✔ | Alle 6 Sender/Frequenzen/Leistungen identisch; DAB 9A; „Verkehrsfunkdurchsagen werden von SR 1 und SR 3 Saarlandwelle ausgestrahlt“; DC.date 02.03.2022. |
| sr-ukw-sr3 | ✔ | Alle 5 Sender identisch; DAB 9A; DC.date 27.10.2026. |
| sr-ukw-kultur | ✔ | Alle 6 Sender identisch (inkl. Saarbrücken 91,3 MHz 100 kW, Homburg 98,6 MHz 200 W); DAB-Block 9A; DC.date 21.01.2026. |
| swl-leuchtturm-saarwellingen | ✔ | PDF Seite 7 (Bild): „Bei großflächigem Stromausfall über einen Zeitraum ab 1 Stunde sind die notstromgespeisten Gerätehäuser der Feuerwehr Saarwellingen in dem betroffenen Ortsteil als Leuchttürme besetzt, damit sie hier im Notfall einen Ansprechpartner haben.“ Adresse Schloßstraße 31-33, 66793 Saarwellingen auf feuerwehrsaarwellingen.de/kontakt. |
| swl-leuchtturm-schwarzenholz | ✔ | Dorfstraße 20, 66793 Saarwellingen (Kontaktseite); Aussage wie oben. |
| swl-leuchtturm-reisbach | ✔ | Kirchenstraße 73, 66793 Saarwellingen (Kontaktseite); Aussage wie oben. |
| z-oberste | ✔ (Teil ?) | Beide Sätze wörtlich auf landkreis-neunkirchen.de/recht-ordnung/katastrophenschutz. Zusatzbeleg saarland.de/mibs nicht prüfbar (Bot-Schutz 403, WebFetch nicht freigegeben). |

Randnotiz: PDF Saarwellingen nennt zum Melden von Stromausfällen 0681 – 40302611 (= VSE-Strom-Störungsnummer), passt zu vse-netz.

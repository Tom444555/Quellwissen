import json
Q={
 "caniuse":{"t":"caniuse.com: BarcodeDetector API (Daten aus MDN browser-compat-data)","u":"https://caniuse.com/mdn-api_barcodedetector","stand":"abgerufen 26.11.2026 (Nutzungsdaten StatCounter 10/2026)"},
 "mdn":{"t":"MDN Web Docs: BarcodeDetector","u":"https://developer.mozilla.org/en-US/docs/Web/API/BarcodeDetector","stand":"11.06.2026"},
 "webkitbug":{"t":"WebKit Bugzilla 198174: Shape Detection API (BarcodeDetector)","u":"https://bugs.webkit.org/show_bug.cgi?id=198174","stand":"Duplikat von Bug 255803 seit 27.10.2023"},
 "npm_bd":{"t":"npm-Register: barcode-detector 3.2.5 (README und Metadaten)","u":"https://www.npmjs.com/package/barcode-detector","stand":"Version 3.2.5, geändert 24.11.2026"},
 "npm_zx":{"t":"npm-Register: zxing-wasm 3.1.8 (README und Metadaten)","u":"https://www.npmjs.com/package/zxing-wasm","stand":"Version 3.1.8, geändert 24.11.2026"},
 "npm_jsqr":{"t":"npm-Register: jsqr 1.4.0","u":"https://www.npmjs.com/package/jsqr","stand":"Version 1.4.0"},
 "npm_lean":{"t":"npm-Register: lean-qr 2.7.4 (README)","u":"https://www.npmjs.com/package/lean-qr","stand":"Version 2.7.4, geändert 07.09.2026"},
 "npm_uqr":{"t":"npm-Register: uqr 0.1.3","u":"https://www.npmjs.com/package/uqr","stand":"Version 0.1.3"},
 "npm_quagga":{"t":"npm-Register: @ericblade/quagga2 1.14.0","u":"https://www.npmjs.com/package/@ericblade/quagga2","stand":"Version 1.14.0, geändert 22.11.2026"},
 "off_api":{"t":"Open Food Facts: Introduction to Open Food Facts API documentation","u":"https://openfoodfacts.github.io/openfoodfacts-server/api","stand":"ohne Datum, abgerufen 26.11.2026"},
 "off_tut":{"t":"Open Food Facts: Tutorial on using the Open Food Facts API","u":"https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/tutorial-off-api/","stand":"ohne Datum, abgerufen 26.11.2026"},
 "off_cond":{"t":"Open Food Facts Forum: Conditions to use the Open Food Facts API","u":"https://forum.openfoodfacts.org/t/conditions-to-use-the-open-food-facts-api/443","stand":"27.11.2023"},
 "keyence":{"t":"KEYENCE: What is a QR code? (Kapazität und Fehlerkorrektur)","u":"https://www.keyence.com/ss/products/auto_id/codereader/basic_2d/qr.jsp","stand":"ohne Datum, abgerufen 26.11.2026"},
 "rfc":{"t":"RFC 5545 (iCalendar), Abschnitt 3.6.6 Alarm Component (icalendar.org)","u":"https://icalendar.org/iCalendar-RFC-5545/3-6-6-alarm-component.html","stand":"RFC 5545, 09/2009"},
 "rfc_ev":{"t":"RFC 5545 (iCalendar), Abschnitt 3.6.1 Event Component (icalendar.org)","u":"https://icalendar.org/iCalendar-RFC-5545/3-6-1-event-component.html","stand":"RFC 5545, 09/2009"},
 "macwelt":{"t":"Macwelt: Termine per .ics-Datei am iPhone empfangen und in Kalender übernehmen","u":"https://www.macwelt.de/article/950169/tipp-ical-termine-per-ics-datei-empfangen-und-in-kalender-uebernehmen.html","stand":"26.01.2023"},
 "gcal":{"t":"Google Kalender-Hilfe: Termine in Google Kalender importieren","u":"https://support.google.com/calendar/answer/37118?hl=en","stand":"ohne Datum, abgerufen 26.11.2026"},
}
def e(id,titel,text,q,wert=None,einheit=None,warnung=None,kat=None):
    return {"id":id,"kategorie":kat,"titel":titel,"text":text,"wert":wert,"einheit":einheit,"warnung":warnung,"quelle":Q[q]}
ICS="BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Quellwissen//Vorrat//DE\r\nBEGIN:VEVENT\r\nUID:vorrat-wasser-2027-05@quellwissen.local\r\nDTSTAMP:20261126T120000Z\r\nDTSTART;VALUE=DATE:20270526\r\nSUMMARY:Wasservorrat tauschen\r\nDESCRIPTION:Selbst abgefülltes Leitungswasser austauschen (alle 6 Monate).\r\nBEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:Wasservorrat tauschen\r\nTRIGGER:-PT15H\r\nEND:VALARM\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n"
E=[
 # (a) Barcode
 e("bd-safari-ios","BarcodeDetector in Safari (iPhone/iPad)","Laut caniuse/MDN-Daten in Safari auf iOS 17.0 bis 27.2 vorhanden, aber standardmäßig deaktiviert (nur über Funktions-Schalter „Shape Detection API“). Für die App also nicht nutzbar – Ersatzbibliothek nötig.","caniuse",kat="Barcode",warnung="Nicht auf natives BarcodeDetector unter iOS verlassen."),
 e("bd-webkit","WebKit-Stand","Der WebKit-Fehlereintrag zur Shape Detection API wurde 2023 als Duplikat geschlossen; Nutzer berichteten, die API sei in der Technology Preview nur hinter einem Feature-Flag verfügbar und in Web Workern nicht nutzbar.","webkitbug",kat="Barcode"),
 e("bd-chrome-android","BarcodeDetector in Chrome (Android)","In Chrome für Android unterstützt (caniuse listet Version 157). Samsung Internet ab 13.0 unterstützt. Chrome am Desktop nur teilweise, Firefox gar nicht.","caniuse",kat="Barcode"),
 e("bd-mdn","Rahmenbedingungen","MDN führt die API als experimentell und nicht „Baseline“. Sie läuft nur in sicheren Kontexten (HTTPS) und auch in Web Workern. Unterstützte Formate zur Laufzeit mit BarcodeDetector.getSupportedFormats() abfragen.","mdn",kat="Barcode"),
 e("bd-ersatz","Ersatz: barcode-detector (Polyfill)","Freie Bibliothek „barcode-detector“ (MIT-Lizenz), bildet die BarcodeDetector-Schnittstelle nach und liest u. a. EAN-8, EAN-13, UPC-A/E und QR. Nutzt intern ZXing-C++ als WebAssembly; die .wasm-Datei wird standardmäßig von einem CDN geladen, kann für Offline-Betrieb aber selbst ausgeliefert werden.","npm_bd",264650,"Byte Paketgröße entpackt (ohne .wasm)",kat="Barcode",warnung="Für Offline-Nutzung den .wasm-Pfad auf die eigene App umstellen (prepareZXingModule)."),
 e("bd-wasm","Größe der Lese-Engine","zxing-wasm (MIT): Nur-Lesen-Variante „reader“ ca. 1,04 MiB WebAssembly, „full“ (lesen und schreiben) ca. 1,46 MiB, „writer“ ca. 636 KiB.","npm_zx",1.04,"MiB (.wasm, nur lesen)",kat="Barcode"),
 e("bd-quagga","Alternative ohne WebAssembly","@ericblade/quagga2 (MIT) liest 1D-Strichcodes wie EAN in reinem JavaScript; minimierte Größe nicht belegt.","npm_quagga",kat="Barcode"),
 # (b) Open Food Facts
 e("off-endpunkt","Open Food Facts: Produkt per Strichcode","Abruf über /api/v2/product/{Strichcode} (auch v3). Mit fields= nur benötigte Felder anfordern, z. B. https://world.openfoodfacts.org/api/v2/product/3017624010701?fields=product_name,nutriments","off_tut",kat="Open Food Facts"),
 e("off-antwort","Open Food Facts: Antwort","Die Antwort enthält code, status, status_verbose und product; „status: 1“ bedeutet „product found“. Nährwerte stehen im Objekt nutriments, z. B. energy-kcal_100g, carbohydrates_100g, sugars_100g.","off_tut",kat="Open Food Facts"),
 e("off-ua","Open Food Facts: User-Agent Pflicht","Jede Anfrage braucht einen eigenen User-Agent im Format App-Name/Version (Kontakt-E-Mail). Lesen braucht sonst keine Anmeldung; Schreiben schon.","off_api",kat="Open Food Facts"),
 e("off-limit-produkt","Open Food Facts: Abfragegrenze Produkt","Höchstens 15 Produktabrufe je Minute und IP-Adresse.","off_api",15,"Anfragen je Minute",kat="Open Food Facts",warnung="Überschreitung kann zur Sperre der IP führen."),
 e("off-limit-suche","Open Food Facts: Abfragegrenze Suche","Höchstens 10 Suchanfragen je Minute; nicht für Suche-beim-Tippen verwenden.","off_api",10,"Anfragen je Minute",kat="Open Food Facts"),
 e("off-lizenz","Open Food Facts: Lizenz","Datenbank unter Open Database License (ODbL), Einzelinhalte unter DbCL, Bilder unter CC BY-SA. Bedingungen: Namensnennung und Weitergabe unter gleichen Bedingungen.","off_api",kat="Open Food Facts"),
 e("off-test","Open Food Facts: Testumgebung","Zum Testen world.openfoodfacts.net nutzen (HTTP-Basic-Auth Benutzer „off“, Passwort „off“).","off_api",kat="Open Food Facts"),
 # (c) QR
 e("qr-erzeugen","QR-Code erzeugen: lean-qr","lean-qr (MIT): weniger als 4 kB komprimiert, ca. 7 kB unkomprimiert, ohne Abhängigkeiten; „nano“-Variante ca. 2 kB komprimiert.","npm_lean",4,"kB komprimiert (weniger als)",kat="QR"),
 e("qr-erzeugen-alt","QR-Code erzeugen: uqr","uqr (MIT), Paket entpackt ca. 79 kB; erzeugt QR-Codes (z. B. als SVG).","npm_uqr",79278,"Byte Paketgröße entpackt",kat="QR"),
 e("qr-lesen","QR-Code lesen: jsQR","jsQR (Apache-2.0), reines JavaScript, liest nur QR-Codes aus Bilddaten (ImageData); Paket entpackt ca. 280 kB. Alternativ liest barcode-detector auch QR-Codes.","npm_jsqr",279741,"Byte Paketgröße entpackt",kat="QR"),
 e("qr-kapazitaet","QR-Code: Kapazität","Höchstens 7.089 Ziffern, 4.296 alphanumerische Zeichen oder 2.953 Byte (größte Version, niedrigste Fehlerkorrektur). Fehlerkorrektur: L 7 %, M 15 %, Q 25 %, H 30 % wiederherstellbar.","keyence",2953,"Byte (Maximum)",kat="QR",warnung=None),
 # (d) ics
 e("ics-aufbau","Kalenderdatei mit Erinnerung","Ein VALARM muss innerhalb eines VEVENT (oder VTODO) stehen und ACTION und TRIGGER enthalten; bei ACTION:DISPLAY zusätzlich DESCRIPTION. TRIGGER:-PT30M bedeutet 30 Minuten vorher.","rfc",kat="Kalender"),
 e("ics-beispiel","Minimalbeispiel .ics","Ganztägiger Termin (DTSTART mit VALUE=DATE, dauert ohne DTEND einen Tag) mit Erinnerung am Vortag um 9 Uhr (TRIGGER -PT15H vor Tagesbeginn). DTSTAMP und UID sind im VEVENT Pflicht und dürfen nur einmal vorkommen.","rfc_ev",ICS,"Dateiinhalt",kat="Kalender"),
 e("ics-iphone","iPhone: .ics übernehmen","Aus Mail: Anhang antippen, „Zum Kalender hinzufügen“, Kalender wählen, „Fertig“. Erinnerungen lassen sich dabei setzen. Ob der Weg direkt aus Safari-Downloads gleich funktioniert und ob der Alarm aus der Datei übernommen wird, ist in der Quelle nicht beschrieben.","macwelt",kat="Kalender"),
 e("ics-android","Android/Google Kalender: .ics übernehmen","Laut Google-Hilfe lassen sich .ics- und CSV-Dateien nur am Computer über die Google-Kalender-Webseite importieren (Einstellungen → Importieren & Exportieren). Gäste und Konferenzdaten werden nicht übernommen; importierte Termine bleiben nicht synchron.","gcal",kat="Kalender",warnung="Für Android zusätzlich einen Weg ohne Datei anbieten (z. B. Termin manuell anlegen) – Verhalten anderer Kalender-Apps nicht belegt."),
]
data={"thema":"Technik für den Vorrats-Planer (Barcode, Open Food Facts, QR, Kalender)","stand":"26.11.2026","eintraege":E,"quellen":list(Q.values()),
 "hinweis":"Paketgrößen aus dem npm-Register sind entpackte Paketgrößen (inkl. Quellcode/Typen), nicht die minimierte Ladegröße – nur lean-qr und zxing-wasm nennen Ladegrößen selbst. Bibliotheksnamen sind technische Angaben für den Bau-Helfer, keine Produktempfehlung. Das .ics-Beispiel wurde nach RFC 5545 erstellt; PRODID/VERSION im VCALENDAR, CRLF-Zeilenenden und MIME-Typ text/calendar sind übliche Praxis, aber in den geöffneten Abschnitten nicht belegt. Weitere OFF-Nährwertfeldnamen (proteins_100g, fat_100g, salt_100g …) nicht in den gelesenen Seiten belegt."}
json.dump(data,open('/home/claude/scratch/vorrat2/fakten/technik.json','w'),ensure_ascii=False,indent=1)
print(len(E))

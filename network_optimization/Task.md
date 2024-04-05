# Energiekonzepte für Städe: Netzoptimierung

### Links

- [Data](..%2Fdata)
- [Github](https://github.com/Sonaion/hackHPI2024)
- [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)

---

Im Kontext der Energiewende muss nicht nur die Industrie und jeder Privathaushalt
seinen energetischen Konzepte neu denken um den Co2 Fußabdruck zu senken, das ganze gilt auch für Städte und Kommunen. 
Ein großer Teil dieses Wandelns ist die Kommunale Wärmeplanung und der einsatz ernuerbarer Energien um Bedarfe zu decken.

Die Planung dieser werden aktuell zumeinst manuell getätigt und bieten potential automatisiert gelöst zu werden.
Im Kontext dieser Aufgabe geht es darum einen Algorithmus zu schreiben, welcher eine Energiekonzept Planung für eine
Stadt ermöglicht, dabei werden annahmen getroffen, welche die umsetzung innerhalb von 24h ermöglichen sollten.
Darunter gilt unter andrem, dass die gegeben Städte keine Bestands Anlagen haben um Energie zu beziehen.
Dementsprechend darf die Planung von Grund auf neu gestaltet werden.

Hierfür werden Stadtdaten bereitgestellt welche via dem Preprocessing Script aus den OSM Daten via der Overpass API
gezogen wurden, der Prozess kann für beliebige Städte durchgeführt werden, siehe [01_CityDataPreprocessing.ipynb](01_CityDataPreprocessing.ipynb). 
Diese Daten beinhalten Gebäudedaten und deren Nutzungsdaten, Straßendaten und Daten für Nutzbarkeit von erneuerbaren Energien wie Photo Voltaik und
Solarthermie.

Weiterhin werden Daten für Erzeuger, Speicher und Leitungen in einfachster form bereitgestellt. 
Diese Daten beinhalten die Investitionskosten, Betriebskosten und CO2 Emissionen.
Am Ende soll das Programm zu ein Energiekonzept erschließen, welches die Investitionskosten, Betriebskosten und CO2 Emissionen berechnet 
und basierend auf gegebenen Gewichtungen optimiert. Diese Zielwerte werden am Ende mittels diesen Gewichtungen zusammen gerechnet um einen 
Fitness wert zu berechnen, welcher die Güte der Lösung bestimmt. Das Ziel ist es dementsprechend diesen Fitness wert zu minimieren.
Diese Zielfunktionen sind dabei wie folgt definiert:

```math
investFaktor * Gesamtinvestkosten + betriebstksotenFaktor * GeamtBetriebskosten + co2Faktor * GesamtCO2Emissionen
```

Die Summe der Faktoren kann dabei als '1' angenommen werden.

Am Ende soll ein Netzwerk auf den Stadtdaten herrauskommen, welche die Erzeuger und Leitungen dimensioniert und deren
Betriebsverhalten anhand von den 2 gegeben Referenztagen auf das Jahr hochrechnet. 
Für die genaue Datenstruktur und die Schnittstellen wird in den folgenden Abschnitten eingegangen-

## Getroffene Annahmen/ Gegebene Parameter

- Es gibt eine Stadt mit Gebäuden mit spezifischen Nutzungsdaten, Straßendaten, und Flächendaten für erneuerbare Energien.
- Es gibt Erzeuger, Leitungen und optional Speicher
- Erzeuger, Leittungen und Speicher haben Investitionskosten, Betriebskosten und CO2 Emissionen
- Erzeuger und Speicher können nur auf den jeweils angegeben Flächen gebaut werden und haben ein Leistungspotential was
  sich stets auf die Fläche in m² bezieht
- Leitungen können nur auf den Straßen gebaut werden und haben eine Länge in m
- Gebäude haben Energiebedarfe die spezifisch pro m² angegeben werden und hochgerechnet werden müssen
- Energiebedarfe liegen für einen Referenz Sommer- und Wintertag ab.
- Es sind Energie Potentiale in [potentials](data/loadprofiles/summer/potentials.json) vorgegeben, wo beschrieben wird, wieviel Energie pro m^2 einer gewissenen Energie genutzt werden kann.
- Es gibt eine Gewichtung die die Investitionskosten, Instandhaltungskosten und CO2 Emissionen berücksichtigt
- Pro Fläche können nicht mehr Erzeuger, Speicher bereitgestellt werden als es die Fläche zulässt.
- Energienetze können von Eckpunkten von Flächen/ Gebäuden zum nächst befindlichen Straßenpunkt gebaut werden.
- Leitungen haben pro m einen Energieverlust
- Speicher haben pro h einen Energieverlust
- 'operatingCost' und 'co2' sind Werte die pro Nutzung einer Enität gezahlt werden müssen.
- 'invest' muss nur einmal pro gewählter Entität bezahlt werden
- pro Nutzungstype sind die Bedarfe in [Sommer/Winter](data/loadprofiles/summer) gegeben. 
- Es gibt Sommer und Winter Referenzdaten, diese sollen jeweils auf 180 Tage hochgerechnet werden um ein ganzes Jahr zu betrachten.

## Aufgabe

Schreibe ein Programm, welche die Input Datein einer Stadt entgegennimmt und ein Energiekonzept erstellt. Die Inputdateien
beinhaltet die Stadt-, Erzeuger-, Speicher-, Leitungen, Energiepotential und Bedarfsinformationen.
Diese sind in folgenden Files:
[Potsdam](data/total_Potsdam.json)
[Systems](data/systems.json)
[Referenzlastgänge](data/loadprofiles/summer)


Das Programm soll eine Outputdatei erstellen, welche bezüglich jeder Fläche angibt, welche Erzeuger und Speicher auf
dieser gebaut wurden.
Wieviel Energie pro Stunde produziert wird und ber welche Leitungen oder welche Bedarfe diese decken.
Am ende sollen weiterhin kennzahlen ausgegeben werden wieviel Investitionskosten, Betriebskosten und CO2
Emissionen durch das Konzept entstehen.
Leitungen können dabei stets nur von und zu in der inputdatei angegebenen Punkten (Straßen bzw. Eckpunkte von ) gezogen werden.

## Output format

Das format des Outputs kann frei gewählt werden soll aber die folgenden Inhalte behalten.

Gebe in einer JSON Datei folgende Informationen aus:
- Gesamt Investitionskosten
- Gesamt Betriebskosten
- Gesamt CO2 Emissionen

Gebe für jeden Erzeuger, Leitung und optional Speicher folgende Informationen aus:
- Gesamt Investitionskosten
- Gesamt Betriebskosten
- Gesamt CO2 Emissionen

Gebe für jede Fläche/ Gebäude folgende Informationen aus:
- Welche Erzeuger, Speicher in welcher quantität auf dieser Fläche gebaut wurden
- Pro Erzeuger, Speicher:
  - wieviel Energie in der jeweiligen Stunde produziert wurde
  - (optional Speicher) wieivel in den Speicher geladen/ entladen wurde und wie der Speicherstand ist.

Gebe für jede Leitung folgende Informationen aus:
- Wieviel Energie in der jeweiligen Stunde durch jedes Leitungssegment fließt.
- Wieviel verluste durch die Leitung entstehen

Finde eine Datenstruktur die den Netzwerk gut als Graphen abbildet.
# Energiekonzepte für Städe: Netzoptimierung

### Links

- [Preprocessing](Preprocessing.md)
- [Github](github.com/)
- [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API)

---

Im Kontext der Energiewende muss nicht nur die Industrie oder jede Privatperson
seinen energetischen fußabdruck neu denken. Das ganze gilt auch für Städte. Ein Stichwort
hierzu wäre die Kommunale Wärmeplanung oder den Bezug von Strom aus erneuerbaren Energien.

Diese Planungsaufwände werden aktuell zumeinst manuell gefertigt und bieten potential optimiert zu werden.
Im Kontext dieser Aufgabe geht es darum einen Algorithmus zu schreiben, welcher eine Energiekonzept Planung für eine
Stadt ermöglicht. Aufgrund der zeitlichen einschränkungen sind natürlich einige annahmen getroffen wurden.
Darunter gilt unter andrem, dass die gegeben Städte keine Bestands Anlagen haben um Energie zu beziehen.
Dementsprechend darf die Planung von Grund auf neu gestaltet werden.

Hierfür werden Stadtdaten bereitgestellt welche via dem Preprocessing Script aus den OSM Daten via der Overpass API
gezogen wurden. Diese Daten beinhalten Flächen spezifische Nutzungsdaten wie z.B. Wohngebiete, Gewerbegebiete, etc.
und Straßendaten.

Weiterhin werden Daten für Erzeuger, Speicher und Leitungen in einfachster form bereitgestellt werden. Diese werden
dafür genutzt
um Investitionskosten, Instandhaltungskosten und CO2 Emissionen zu berechnen. Am Ende soll das Programm zu einem
Energiekonzept die
Investitionskosten, Instandhaltungskosten und CO2 Emissionen berechnen. Diese werden als Fitnesswerte angenommen und
dienen zum vergleich.
Der Algorithmus soll eine gewisse Zielfunktion die sich wie folgt zusammensetzt optimieren,
wobei die SUmme der Faktoren 1 ergeben muss:

```math
investFaktor * Investitionskosten + instandhaltungFaktor * Instandhaltungskosten + co2Faktor * CO2 Emissionen
```

Es gilt dementsprechend ein Netzwerk auf den Stadtdaten zu erstellen was unter den gegeben vorraussetzungen ein
möglichst
effizientes netzwerk darstellt. Das ganze wird in einem stark angelehnten format an kompetitve Programmierung
stattfinden.
Für die genaue Datenstruktur und die Schnittstellen wird später eingegangen.

## Getroffene Annahmen

- Es gibt eine Stadt mit Flächen spezifischen Nutzungsdaten und Straßendaten
- Es gibt Erzeuger, Speicher und Leitungen
- Erzeuger, Speicher, Leittungen haben Investitionskosten, Instandhaltungskosten und CO2 Emissionen
- Erzeuger und Speicher können nur auf den jeweils angegeben Flächen gebaut werden und haben ein Leistungspotential was
  sich stets auf die Fläche in m² bezieht
- Leitungen können nur auf den Straßen gebaut werden und haben eine Länge in m
- Flächen haben Energiebedarfe die spezifisch pro m² angegeben werden und hochgerechnet werden müssen
- Energiebedarfe sind für einen Tag angegeben.
- Es sind Wetterdaten angegeben und Erzeuger, Speicher können abhängig von den Wetterdaten Energie produzieren. (
  Beispiel PV)
- Es gibt eine Gewichtung die die Investitionskosten, Instandhaltungskosten und CO2 Emissionen berücksichtigt
- Pro fläche können nicht mehr Erzeuger, Speicher bereitgestellt werden als es die Fläche zulässt.
- Energienetze können von Rendern von Flächen zum nächst befindlichen Straßenpunkt gebaut werden.
- Innerhalb einer Fläche können Leitungen nur gebaut werden (um weg zu sparen), wenn diese den gesamten Energie bedarf
  der Fläche decken. Ansonsten reicht für eine Fläche der anschluss an einem Randpunkt.
- Leitungen haben pro m einen Energieverlust
- Speicher haben pro h einen Energieverlust

## Aufgabe

Schreibe ein Programm, welche eine Inputdatei einer Stadt entgegennimmt und ein Energiekonzept erstellt. Die Inputdatei
beinhaltet die Stadt-, Erzeuger-, Speicher-, Leitungen, Wetter- und Bedarfsinformationen.

Das Programm soll eine Outputdatei erstellen, welche bezüglich jeder Fläche angibt, welche Erzeuger und Speicher auf
dieser gebaut wurden.
Wo von dieser aus eine Leitung gezogen wurde und wie wieviel Energie in der jeweiligen Stunde durch diese Leitung
fließt.
Am ende sollen weiterhin kennzahlen ausgegeben werden wieviel Investitionskosten, Instandhaltungskosten und CO2
Emissionen entstanden sind.
Leitungen können dabei stets nur von und zu in der inputdatei angegebenen Punkten gezogen werden.

## Output format

Gebe in einer JSON Datei folgende Informationen aus:
- Gesamt Investitionskosten
- Gesamt Betriebskosten
- Gesamt CO2 Emissionen

Gebe für jeden Erzeuger, Speicher und Leitung folgende Informationen aus:
- Gesamt Investitionskosten
- Gesamt Betriebskosten
- Gesamt CO2 Emissionen

Gebe für jede Fläche folgende Informationen aus:
- Welche Erzeuger, Speicher in welcher quantität auf dieser Fläche gebaut wurden
- Pro Erzeuger, Speicher:
- wieviel Energie in der jeweiligen Stunde produziert/ geladen/ entladen wurde

Gebe für jede Leitung folgende Informationen aus:
- Wieviel Energie in der jeweiligen Stunde durch diese Leitung fließt
- Wieviel verluste durch die Leitung entstehen

Weierhin gebe Leistungen als Graphen an, welcher durch eine adjazenzliste dargestellt wird.
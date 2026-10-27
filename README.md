# Automatisierter Reporting-Generator

Ein Python-Skript, das Versicherungsdaten **bereinigt**, **validiert** und automatisch einen **Excel-Bericht** erstellt.

## Ablauf

1. **Laden:** CSV-Datei mit Vertragsdaten einlesen (pandas)
2. **Bereinigen:** Leerzeichen entfernen, Schreibweise vereinheitlichen, Duplikate löschen
3. **Validieren:** fehlerhafte Datensätze finden (ungültiges Alter, fehlender oder negativer Beitrag, unbekannter Status)
4. **Bericht:** Excel-Datei mit drei Tabellenblättern erstellen (pandas + openpyxl)
   - *Uebersicht*: Anzahl Verträge, Summe der Beiträge und Durchschnittsalter pro Tarif
   - *Gueltige Vertraege*: alle sauberen Datensätze
   - *Fehler*: Liste aller gefundenen Probleme

## Starten

```bash
pip install pandas openpyxl pytest
python reporting.py      # erstellt bericht.xlsx
python -m pytest -v      # startet die Tests
```

## Technologien

Python, pandas, openpyxl, pytest

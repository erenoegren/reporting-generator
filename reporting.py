"""
Automatisierter Reporting-Generator fuer Versicherungsvertraege.

Ablauf:
1. Daten laden      (CSV-Datei einlesen)
2. Daten bereinigen (Leerzeichen, Gross-/Kleinschreibung, Duplikate)
3. Daten validieren (fehlerhafte Datensaetze finden)
4. Bericht erstellen (Excel-Datei mit mehreren Tabellenblaettern)
"""

import pandas as pd
from openpyxl.styles import Font, PatternFill

GUELTIGE_STATUS = ["aktiv", "beitragsfrei", "gekuendigt"]


def daten_laden(pfad):
    """Liest die CSV-Datei ein und gibt eine Tabelle (DataFrame) zurueck."""
    return pd.read_csv(pfad)


def daten_bereinigen(df):
    """Vereinheitlicht die Texte und entfernt doppelte Vertraege."""
    df = df.copy()
    df["kunde"] = df["kunde"].str.strip()
    df["tarif"] = df["tarif"].str.strip().str.capitalize()   # "premium" -> "Premium"
    df["status"] = df["status"].str.strip().str.lower()      # " AKTIV" -> "aktiv"
    df = df.drop_duplicates(subset="vertragsnummer")         # gleiche Vertragsnummer nur 1x
    return df


def daten_validieren(df):
    """Prueft jede Zeile. Gibt gueltige Daten und eine Fehlerliste zurueck."""
    fehler = []

    for _, zeile in df.iterrows():
        nr = zeile["vertragsnummer"]

        if zeile["alter"] < 18 or zeile["alter"] > 65:
            fehler.append({"vertragsnummer": nr, "fehler": f"Ungueltiges Alter: {zeile['alter']}"})

        if pd.isna(zeile["monatsbeitrag"]):
            fehler.append({"vertragsnummer": nr, "fehler": "Monatsbeitrag fehlt"})
        elif zeile["monatsbeitrag"] < 0:
            fehler.append({"vertragsnummer": nr, "fehler": "Monatsbeitrag ist negativ"})

        if zeile["status"] not in GUELTIGE_STATUS:
            fehler.append({"vertragsnummer": nr, "fehler": f"Unbekannter Status: {zeile['status']}"})

    fehler_df = pd.DataFrame(fehler, columns=["vertragsnummer", "fehler"])
    gueltig = df[~df["vertragsnummer"].isin(fehler_df["vertragsnummer"])]
    return gueltig, fehler_df


def uebersicht_erstellen(df):
    """Fasst die gueltigen Vertraege pro Tarif zusammen."""
    return (
        df.groupby("tarif")
        .agg(
            anzahl_vertraege=("vertragsnummer", "count"),
            summe_monatsbeitrag=("monatsbeitrag", "sum"),
            durchschnitt_alter=("alter", "mean"),
        )
        .round(2)
        .reset_index()
    )


def tabelle_formatieren(blatt):
    """Macht die Kopfzeile fett und farbig und passt die Spaltenbreite an."""
    for zelle in blatt[1]:
        zelle.font = Font(bold=True, color="FFFFFF")
        zelle.fill = PatternFill("solid", fgColor="1F4E78")

    for spalte in blatt.columns:
        breite = max(len(str(zelle.value)) for zelle in spalte if zelle.value is not None)
        blatt.column_dimensions[spalte[0].column_letter].width = breite + 3


def bericht_erstellen(gueltig, fehler, uebersicht, pfad):
    """Schreibt alles in eine Excel-Datei mit drei Tabellenblaettern."""
    with pd.ExcelWriter(pfad, engine="openpyxl") as writer:
        uebersicht.to_excel(writer, sheet_name="Uebersicht", index=False)
        gueltig.to_excel(writer, sheet_name="Gueltige Vertraege", index=False)
        fehler.to_excel(writer, sheet_name="Fehler", index=False)

        for blatt in writer.sheets.values():
            tabelle_formatieren(blatt)


def main():
    df = daten_laden("vertraege.csv")
    print(f"Eingelesen: {len(df)} Zeilen")

    df = daten_bereinigen(df)
    print(f"Nach Bereinigung: {len(df)} Zeilen (Duplikate entfernt)")

    gueltig, fehler = daten_validieren(df)
    print(f"Gueltige Vertraege: {len(gueltig)}, Fehler gefunden: {len(fehler)}")

    uebersicht = uebersicht_erstellen(gueltig)
    bericht_erstellen(gueltig, fehler, uebersicht, "bericht.xlsx")
    print("Bericht gespeichert: bericht.xlsx")


if __name__ == "__main__":
    main()
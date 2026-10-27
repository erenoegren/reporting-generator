"""
Tests fuer reporting.py  -  starten mit:  python -m pytest -v
"""

import pandas as pd

from reporting import daten_bereinigen, daten_validieren


def beispieldaten():
    return pd.DataFrame({
        "vertragsnummer": ["LV-1", "LV-2", "LV-2"],
        "kunde": [" Anna ", "Ben", "Ben"],
        "alter": [30, 40, 40],
        "tarif": ["basis", "Komfort", "Komfort"],
        "versicherungssumme": [100000, 50000, 50000],
        "monatsbeitrag": [8.33, 10.0, 10.0],
        "status": [" AKTIV", "aktiv", "aktiv"],
    })


def test_duplikate_werden_entfernt():
    df = daten_bereinigen(beispieldaten())
    assert len(df) == 2


def test_texte_werden_vereinheitlicht():
    df = daten_bereinigen(beispieldaten())
    assert df.iloc[0]["status"] == "aktiv"
    assert df.iloc[0]["tarif"] == "Basis"
    assert df.iloc[0]["kunde"] == "Anna"


def test_gueltige_daten_haben_keine_fehler():
    df = daten_bereinigen(beispieldaten())
    gueltig, fehler = daten_validieren(df)
    assert len(fehler) == 0
    assert len(gueltig) == 2


def test_falsches_alter_wird_gefunden():
    df = daten_bereinigen(beispieldaten())
    df.loc[0, "alter"] = 17
    gueltig, fehler = daten_validieren(df)
    assert len(fehler) == 1
    assert "Alter" in fehler.iloc[0]["fehler"]
    assert len(gueltig) == 1


def test_fehlender_beitrag_wird_gefunden():
    df = daten_bereinigen(beispieldaten())
    df.loc[0, "monatsbeitrag"] = None
    gueltig, fehler = daten_validieren(df)
    assert fehler.iloc[0]["fehler"] == "Monatsbeitrag fehlt"
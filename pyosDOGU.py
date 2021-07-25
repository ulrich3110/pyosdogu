#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import tkinter
from tkinter import filedialog
from tkinter import ttk

'''
pyosDOGU.py - [D]ateien und [O]rdner [g]leichzeitig [u]mbenennen
Copyright (c) Juni 2021: Andreas Ulrich
<http://erasand.ch>, <andreas@erasand.ch>

LIZENZ
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

DEUTSCHE ÜBERSETZUNG: <http://www.gnu.de/documents/gpl-3.0.de.html>
'''


def f_loadjson(tx_pfad):
    '''
    tx_pfad = Pfad
    dc_verz = Verzeichnis
    '''
    print("# f_loadjson #")
    # Json laden
    tx_pfad = os.path.normcase(os.path.normpath(tx_pfad))
    try:
        with open(tx_pfad) as ob_f:
            dc_verz = json.load(ob_f)
    except Exception as ob_err:
        # Fehlermeldung ausgeben und leeres Verzeichnis erzeugen
        tx_t = "FEHLER -- PFAD: {0} -- ERROR: {1}".format(
            tx_pfad,
            str(ob_err)
        )
        print(tx_t)
        dc_verz = {}
    return(dc_verz)


def f_savejson(tx_pfad, dc_verz):
    '''
    dc_verz = Verzeichnis
    tx_pfad = Pfad
    '''
    print("# f_savejson #")
    # Json speichern
    tx_pfad = os.path.normcase(os.path.normpath(tx_pfad))
    try:
        with open(tx_pfad, 'w', encoding='utf-8',
                  errors='ignore') as ob_jsonfile:
            json.dump(dc_verz, ob_jsonfile, indent=2, sort_keys=True)
    except Exception as ob_err:
        # Fehlermeldung ausgeben
        tx_t = "FEHLER -- PFAD: {0} -- ERROR: {1}".format(
            tx_pfad,
            str(ob_err)
        )
        print(tx_t)
    return()


class Verzeichnis():
    '''
    Datei-Verzeichnis Inhalt
    '''

    def __init__(self):
        '''
        Initieren
        '''
        print("# Verzeichnis.__init__ #")
        self.m_clear()

    def m_clear(self):
        '''
        Zurücksetzen
        '''
        print("# Verzeichnis.m_clear #")
        self.ls_dateien = []
        self.ls_verzeich = []
        self.tx_stammpfad = ''

    def m_read(self):
        '''
        .ls_dateien = ['name.erw', ]
        .ls_verzeich = ['name', ]
        '''
        print("# Verzeichnis.m_readdir #")
        # Listen leeren
        self.ls_dateien = []
        self.ls_verzeich = []
        # Verzeichnis lesen
        ls_dir = os.listdir(self.tx_stammpfad)
        # Prüfen ob Datei oder Verzeichnis
        for tx_name in ls_dir:
            tx_pfad = os.path.join(self.tx_stammpfad, tx_name)
            if os.path.isfile(tx_pfad):
                # Eine Datei
                self.ls_dateien.append(tx_pfad)
            elif os.path.isdir(tx_pfad):
                # Ein Verzeichnis
                self.ls_verzeich.append(tx_pfad)


class Umbenennen():
    '''
    Dateien und Ordner umbenennen
    '''

    def __init__(self):
        '''
        .dc_rename = {"pfad/alt": "pfad/neu", }
        '''
        print("# Umbenennen.__init__ #")
        self.m_clear()

    def m_clear(self):
        '''
        Zurücksetzen
        '''
        print("# Umbenennen.m_clear #")
        self.ls_elemente = []
        self.tx_alt = ""
        self.tx_neu = ""
        self.tx_modus = ""
        self.in_anzahl = 0
        self.in_position = 0
        self.dc_rename = {}
        self.tx_renalt = ""
        self.tx_renneu = ""

    def m_ersetzen(self):
        '''
        Zeichen ersetzen
        '''
        print("# Umbenennen.m_ersetzen #")
        self.dc_rename = {}
        for tx_pfad in self.ls_elemente:
            # Pfad ()
            tx_base = os.path.basename(tx_pfad)
            tx_dir = os.path.dirname(tx_pfad)
            tx_baseneu = ""
            # Ersetzen
            if self.tx_modus == "SUCHE":
                # Im Suchmodus ersetzen
                if tx_base.find(self.tx_alt) != -1:
                    # Scuhtext wurde gefunden
                    tx_baseneu = tx_base.replace(
                        self.tx_alt,
                        self.tx_neu
                    )
            elif self.tx_modus == "START":
                if tx_base.startswith(self.tx_alt):
                    # Anfang ersetzen
                    in_anf = len(self.tx_alt)
                    tx_ende = tx_base[in_anf:]
                    tx_baseneu = "{0}{1}".format(self.tx_neu, tx_ende)
            elif self.tx_modus == "ENDE":
                if tx_base.endswith(self.tx_alt):
                    # Ende ersetzen
                    in_end = len(tx_base) - len(self.tx_alt)
                    tx_anfang = tx_base[:in_end]
                    tx_baseneu = "{0}{1}".format(tx_anfang, self.tx_neu)
            if tx_baseneu:
                # Dateipfad nach umbenennen bilden
                tx_pfadneu = os.path.join(tx_dir, tx_baseneu)
                # Ins Umbenennen Verzeichnis aufnehmen
                self.dc_rename[tx_pfad] = tx_pfadneu

    def m_loeschen(self):
        '''
        Zeichen löschen
        '''
        print("# Umbenennen.m_loeschen #")
        self.dc_rename = {}
        for tx_pfad in self.ls_elemente:
            # Pfad ()
            tx_base = os.path.basename(tx_pfad)
            tx_dir = os.path.dirname(tx_pfad)
            tx_baseneu = ""
            in_posanf = -1
            in_posend = -1
            in_len = len(tx_base)
            if self.tx_modus == "START":
                in_posanf = self.in_position - 1
                in_posend = in_posanf + self.in_anzahl
            elif self.tx_modus == "ENDE":
                in_posend = in_len - self.in_position + 1
                in_posanf = in_posend - self.in_anzahl
            if in_posanf >= 0 and in_posend <= in_len:
                # Teil löschen
                tx_anfang = tx_base[:in_posanf]
                tx_ende = tx_base[in_posend:]
                # print ("# Anfang:", tx_anfang, "# Ende:", tx_ende, "#")
                tx_baseneu = "{0}{1}".format(tx_anfang, tx_ende)
                # Dateipfad nach umbenennen bilden
                tx_pfadneu = os.path.join(tx_dir, tx_baseneu)
                # Ins Umbenennen Verzeichnis aufnehmen
                self.dc_rename[tx_pfad] = tx_pfadneu


    def m_einfuegen(self):
        '''
        Zeichen einfügen
        '''
        print("# Umbenennen.m_einfuegen #")
        self.dc_rename = {}
        for tx_pfad in self.ls_elemente:
            # Pfad ()
            tx_base = os.path.basename(tx_pfad)
            tx_dir = os.path.dirname(tx_pfad)
            tx_baseneu = ""
            in_pos = -1
            in_len = len(tx_base)
            if self.tx_modus == "START":
                in_pos = self.in_position - 1
            elif self.tx_modus == "ENDE":
                in_pos = in_len - self.in_position + 1
            if in_pos >= 0 and in_pos <= in_len:
                # Anfang und Ende auftrennen
                tx_anfang = tx_base[:in_pos]
                tx_ende = tx_base[in_pos:]
                tx_baseneu = "{0}{1}{2}".format(
                    tx_anfang,
                    self.tx_neu,
                    tx_ende
                )
                # Dateipfad nach umbenennen bilden
                tx_pfadneu = os.path.join(tx_dir, tx_baseneu)
                # Ins Umbenennen Verzeichnis aufnehmen
                self.dc_rename[tx_pfad] = tx_pfadneu

    def m_aendernalle(self):
        '''
        Nimmt alle vorbereiteten Änderungen vor.
        '''
        print("# Umbenennen.m_aendernalle #")
        # Vorbereitetes Verzeichnis abarbeiten
        for self.tx_renalt, self.tx_renneu in self.dc_rename.items():
            # Umbenennen mit Prüfung
            self.m_rename()

    def m_aenderneinzel(self):
        '''
        Nimmt die Änderung an der gegebenen Datei vor
        '''
        print("# Umbenennen.m_aenderneinzel #")
        # Anhand des alten Dateinamens den neuen Dateinamen aus dem
        # Verzeichnis mit den vorbereiteten Änderungen lesen
        if self.tx_renalt in self.dc_rename.keys():
            # Alter Name vorhanden, neuer Name lesen
            self.tx_renneu = self.dc_rename[self.tx_renalt]
            # Umbenennen mit Prüfung
            self.m_rename()

    def m_rename(self):
        '''
        Namen umbenenennen mit Prüfung
        '''
        print("# Umbenennen.m_rename #")
        try:
            # Existiert der neue Pfad als Datei oder Verzeichnis?
            bl_datei = os.path.isfile(self.tx_renneu)
            bl_verz = os.path.isdir(self.tx_renneu)
            while  bl_datei or bl_verz:
                # Datei oder Verzeichnis existiert
                # Pfad auftrennen
                tx_base = os.path.basename(self.tx_renneu)
                tx_dir = os.path.dirname(self.tx_renneu)
                ls_nametyp = os.path.splitext(tx_base)
                tx_dateiname = ls_nametyp[0]
                tx_dateityp = ls_nametyp[1]
                # Dateityp mit einem Zähler erweitern
                tx_dateineu = self.m_get_dateizaehler(tx_dateiname)
                print("# Dateineu:", tx_dateineu, "#")
                # Neuer Dateipfad bilden
                tx_baseneu = "{0}{1}".format(
                    tx_dateineu,
                    tx_dateityp
                )
                self.tx_renneu = os.path.join(tx_dir, tx_baseneu)
                # Existiert der neue Pfad als Datei oder Ordner?
                bl_datei = os.path.isfile(self.tx_renneu)
                bl_verz = os.path.isdir(self.tx_renneu)
            # Umbenennen
            ''' print("# {0}-{1} #".format(
                self.tx_renalt, self.tx_renneu
            )) '''
            os.rename(self.tx_renalt, self.tx_renneu)
        except Exception as ob_err:
            # Fehlermeldung ausgeben
            tx_t = "".join([
                "# Umbenennen.m_aendern ERROR: ",
                str(ob_err),
                " # Pfad alt = ",
                self.tx_renalt,
                " # Pfad neu = ",
                selff.tx_renneu,
                " #"
            ])
            print(tx_t)

    def m_get_dateizaehler(self, tx_t):
        '''
        Sucht am Textende einen Zähler nach folgendem Schema
        "..(xxx)", liest die Zahl aus und zählt diese hoch.
        Rückgabe: Neuer Text
        '''
        if tx_t.endswith(")"):
            # Scheint ein Zähler zu sein
            in_len = len(tx_t)
            # Den Zähler ermitteln und die Position links davon
            if tx_t[in_len - 3] == "(":
                # 1-stelliger Zähler
                tx_zaehler = tx_t[in_len-2]
                # Ende vor dem Zähler
                in_posend = in_len - 3
            elif tx_t[in_len - 4] == "(":
                # 2-stelliger Zähler
                tx_zaehler = tx_t[in_len-3:in_len-2]
                # Ende vor dem Zähler
                in_posend = in_len - 4
            elif tx_t[in_len - 5] == "(":
                # 3-stelliger Zähler
                tx_zaehler = tx_t[in_len-4:in_len-2]
                # Ende vor dem Zähler
                in_posend = in_len - 5
            else:
                # Kein bekannter Zähler
                tx_zaehler = "0"
                # Ende vor dem Zähler
                in_posend = in_len
            # Text Zähler in einen Integer umwandeln und hochzählen
            try:
                in_zaehler = int(tx_zaehler)
            except Exception:
                in_zaehler = 0
        else:
            # Scheint ohne Zähler
            in_zaehler = 0
            in_posend = len(tx_t)
        in_zaehler += 1
        # Text Links von bestehendem Zähler auslesen
        tx_links = tx_t[:in_posend]
        # Neuen Text bilden und zurückgeben
        tx_n = "{0}({1})".format(tx_links, in_zaehler)
        return(tx_n)


class Gui():
    '''
    Benutzeroberfläche
    '''

    def __init__(self, ob_master):
        '''
        ob_master = tkinter.Tk()
        '''
        print("# Gui.__init__ #")
        self.ob_master = ob_master
        # Name der App
        self.tx_app = "pyosDOGU"
        # Name der Json datei
        self.tx_einst = "pyosDOGU.json"
        # Einstellungen laden
        self.m_load_einst()
        # Fenster Titel & Grösse
        self.ob_master.title(self.tx_app)
        self.ob_master.geometry(self.dc_einst["GUI Fenster"])
        # Widgets definieren
        self.m_set_widgets()
        # Layout
        self.m_set_layout(self.ob_master)
        # Verzeichnis und Umbenennen eröffnen
        self.ob_verzeich = Verzeichnis()
        self.ob_rename = Umbenennen()
        # Update
        self.m_update()

    def m_load_einst(self):
        '''
        Einstellungen
        '''
        print("# Gui.m_load_einst #")
        # Json laden
        self.dc_einst = f_loadjson(self.tx_einst)
        if not self.dc_einst:
            # Fehler beim Laden, Einstellungen erzeugen
            self.dc_einst = {
                "GUI Fenster": "800x600"
            }
            # Einstellungen sichern
            f_savejson(self.tx_einst, self.dc_einst)

    def m_set_widgets(self):
        '''
        Elemente des GUI
        '''
        print("# Gui.m_set_widgets #")
        # Verzeichnis-Wahl Button
        self.ob_verzwahl = ttk.Button(
            self.ob_master,
            text="Verzeichnis wählen",
            command=self.m_on_verzwahl
        )
        # Modus Combobox
        self.ob_modus = ttk.Combobox(self.ob_master)
        self.ob_modus.bind("<<ComboboxSelected>>", self.m_on_modus)
        self.ls_modus = [
            "Zeichen ersetzen mit Suchen",
            "Zeichen ersetzen am Anfang",
            "Zeichen ersetzen am Ende",
            "Zeichen einfügen am Anfang",
            "Zeichen einfügen am Ende",
            "Zeichen löschen am Anfang",
            "Zeichen löschen am Ende",
        ]
        self.ls_labelA = [
            "Suchtext",
            "Suchtext",
            "Suchtext",
            "Vor Position",
            "Nach Position",
            "Vor Position",
            "Nach Position",
        ]
        self.ls_labelB = [
            "Neuer Text",
            "Neuer Text",
            "Neuer Text",
            "Text",
            "Text",
            "Anzahl Zeichen",
            "Anzahl Zeichen",
        ]
        self.ob_modus.config(values=self.ls_modus)
        self.ob_modus.current(0)
        # Input A Bezeichnung
        self.ob_labelAvar = tkinter.StringVar()
        self.ob_labelA = ttk.Label(
            self.ob_master,
            textvariable=self.ob_labelAvar
        )
        # Input A Eingabefeld
        self.ob_inputAvar = tkinter.StringVar()
        self.ob_inputA = ttk.Entry(
            self.ob_master,
            textvariable=self.ob_inputAvar
        )
        self.ob_inputA.bind("<FocusOut>", self.m_on_entry)
        # Input B Bezeichnung
        self.ob_labelBvar = tkinter.StringVar()
        self.ob_labelB = ttk.Label(
            self.ob_master,
            textvariable=self.ob_labelBvar
        )
        # Input B Eingabefeld
        self.ob_inputBvar = tkinter.StringVar()
        self.ob_inputB = ttk.Entry(
            self.ob_master,
            textvariable=self.ob_inputBvar
        )
        self.ob_inputB.bind("<FocusOut>", self.m_on_entry)
        # Ergebnis Liste mit Scrollbar
        self.ob_liste = tkinter.Listbox(self.ob_master)
        self.ob_liste.bind("<Double-Button-1>", self.m_on_listdouble)
        self.ob_listscrollv = ttk.Scrollbar(
            self.ob_master,
            orient=tkinter.VERTICAL,
            command=self.ob_liste.yview
        )
        self.ob_listscrollh = ttk.Scrollbar(
            self.ob_master,
            orient=tkinter.HORIZONTAL,
            command=self.ob_liste.xview
        )
        self.ob_liste.configure(yscroll=self.ob_listscrollv.set)
        self.ob_liste.configure(xscroll=self.ob_listscrollh.set)
        # Auswahl umbenennen
        self.ob_auswahl = ttk.Button(
            self.ob_master,
            text="Auswahl umbenennen",
            command=self.m_on_auswahl
        )
        # Alle umbenennen
        self.ob_alle = ttk.Button(
            self.ob_master,
            text="Alle umbenennen",
            command=self.m_on_alle
        )
        # Beenden Button
        self.ob_beenden = ttk.Button(
            self.ob_master,
            text="Beenden",
            command=self.ob_master.quit
        )
        # Layout-Liste[
        #   ("#", "Bemerkung"),
        #   ("EXP", [x, ],
        #   (Widget, Reihe, Spalte, Anzahl Reihen, Anzahl Spalten,
        #    Position, Abstand X, Abstand Y, in Höhe expandieren),
        # ]
        self.ls_layout = [
            ("EXP", [0, 1, 2, 3]),
            ("#", "Verzeichniswahl, Modus"),
            (self.ob_verzwahl, 0, 0, 1, 1, "EW", 5, 5, False),
            (self.ob_modus, 0, 1, 1, 3, "EW", 5, 5, False),
            ("#", "Input A, Input B"),
            (self.ob_labelA, 1, 0, 1, 1, "E", 5, 5, False),
            (self.ob_inputA, 1, 1, 1, 1, "W", 5, 5, False),
            (self.ob_labelB, 1, 2, 1, 1, "E", 5, 5, False),
            (self.ob_inputB, 1, 3, 1, 1, "W", 5, 5, False),
            ("#", "Liste mit Scrollbars"),
            (self.ob_liste, 2, 0, 1, 4, "NSEW", 5, 5, True),
            (self.ob_listscrollv, 2, 4, 1, 1, "NS", 5, 5, False),
            (self.ob_listscrollh, 3, 0, 1, 4, "EW", 5, 5, False),
            ("#", "Auswahl, Alle, Beenden"),
            (self.ob_auswahl, 4, 0, 1, 1, "EW", 5, 5, False),
            (self.ob_alle, 4, 1, 1, 1, "EW", 5, 5, False),
            (self.ob_beenden, 4, 3, 1, 1, "EW", 5, 5, False)
        ]

    def m_set_layout(self, ob_parent):
        '''
        GUI mit einem Raster layouten, ob_parent ist zum das Gitter-
        Verhalten zu steuern. Die Widgets sind in einer Liste mit
        folgendem Format definiert: [
            ("EXPAND", [x, ])
            ("#", "Bemerkung"),
            (Widget, Reihe, Spalte, Anzahl Reihen, Anzahl Spalten,
             Position, Abstand X, Abstand Y, Höhe expandieren),
        ]
            - ("EXP", [x, ]) = Tupel mit Spalten, welche expanidert
                               werden, Liste mit Spalten-Index
            - ("#", "Bemerkung") = Tupel mit Texten: Bemerkung, wird
                                   für das Grid-Layout nicht verwendet
            - Widget = <tkinter.Objekt> oder <ttk.Objekt>
            - Reihe = Integer, 0 bis ..
            - Spalte = Integer, 0 bis ..
            - Anzahl Reihen, Anzahl Spalten = Integer, Wieviele werden
                                              zusammengefasst, 1 bis ..
            - Position = Text, "E", "W", "EW", "N", "S", "NS", "NSEW",
                               "NW", "NE", "SW", "SE"
            - Abstand X und Abstand Y = Integer, 0 bis ..
            - Höhe expandieren = Bool, False oder True
        '''
        print("# GUI.m_set_layout #")
        # Verzeichnis für Ausrichtung definieren
        dc_sticky = {
            "E": tkinter.E,
            "W": tkinter.W,
            "N": tkinter.N,
            "S": tkinter.S,
            "NW": tkinter.NW,
            "NE": tkinter.NE,
            "SW": tkinter.SW,
            "SE": tkinter.SE,
            "NS": tkinter.NS,
            "EW": tkinter.EW,
            "NSEW": tkinter.NSEW
        }
        # Layout Liste abarbeiten
        for tp_i in self.ls_layout:
            if tp_i[0] == "EXP":
                # Spalten expandieren
                for in_spalte in tp_i[1]:
                    ob_parent.columnconfigure(in_spalte, weight=1)
            elif tp_i[0] != "#":
                # Keine Bemerkung
                # Expanndieren in Höhe prüfen
                if tp_i[8]:
                    # In Höhe expandieren
                    ob_parent.rowconfigure(tp_i[1], weight=1)
                # Im Gitter mit Einstellungen hinzufügen
                tp_i[0].grid(
                    row=tp_i[1],
                    column=tp_i[2],
                    rowspan=tp_i[3],
                    columnspan=tp_i[4],
                    sticky=dc_sticky[tp_i[5]],
                    padx=tp_i[6],
                    pady=tp_i[7]
                )

    def m_update(self):
        '''
        Gui updaten
        '''
        print("# Gui.m_update #")
        # Combobox Eintrag auslesen und Index ermitteln
        tx_item = self.ob_modus.get()
        in_id = self.ls_modus.index(tx_item)
        # Eingabebezeichnungen
        self.ob_labelAvar.set(self.ls_labelA[in_id])
        self.ob_labelBvar.set(self.ls_labelB[in_id])
        # Vorschauliste
        self.m_set_vorschau()

    def m_on_verzwahl(self):
        '''
        Verzeichnis wählen
        '''
        print("# Gui.m_on_verzwahl #")
        # Filedalog
        tx_pfad = filedialog.askdirectory()
        # Verzeichnis Stammpfad setzen und Verzeichnis lesen
        self.ob_verzeich.tx_stammpfad = tx_pfad
        self.m_readverz()

    def m_readverz(self):
        '''
        Verzeichnis lesen
        '''
        print("# Gui.m_readverz #")
        # Verzeichnis lesen
        self.ob_verzeich.m_read()
        # Liste an Umbenennen geben
        ls_elemente = []
        ls_elemente.extend(self.ob_verzeich.ls_dateien)
        ls_elemente.extend(self.ob_verzeich.ls_verzeich)
        self.ob_rename.ls_elemente = ls_elemente
        # Update
        self.m_update()

    def m_on_modus(self, event):
        '''
        Modus wechseln
        '''
        print("# GUI.m_on_modus #")
        # Update
        self.m_update()

    def m_on_entry(self, event):
        '''
        Die Eingabefelder verloren den Fokus
        '''
        print("# GUI.m_on_entry #")
        # Update
        self.m_update()

    def m_on_listdouble(self, event):
        '''
        Doppelklick auf die Liste
        '''
        print("# Gui.m_on_listdouble #")
        # Auswahl umbenennen
        self.m_rename_auswahl()

    def m_on_auswahl(self):
        '''
        Klick auf Auswahl umbenennen
        '''
        print("# Gui.m_on_auswahl #")
        # Auswahl umbenennen
        self.m_rename_auswahl()

    def m_rename_auswahl(self):
        '''
        Auswahl umbenennen
        '''
        print("# Gui.m_rename_auswahl #")
        # Wert aus der Liste holen
        tx_item = self.ob_liste.get(tkinter.ANCHOR)
        # Dateipfad ermitteln
        if tx_item.startswith("- "):
            # Scheint eine Datei oder Verzeichnis zu sein
            # Bereinigen
            tx_pfad = tx_item.lstrip("- ")
            # Autrennen in alter und neuer Name: ["alt", "neu"]
            ls_pfad = tx_pfad.split("   >>   ")
            # mit Stammpfad kombinieren
            self.ob_rename.tx_renalt = os.path.join(
                self.ob_verzeich.tx_stammpfad,
                ls_pfad[0]
            )
            # Eintrag einzeln umbenennen
            # print("# {0} #".format(self.ob_rename.tx_renalt))
            self.ob_rename.m_aenderneinzel()
            # Verzeichnis erneut lesen
            self.m_readverz()

    def m_on_alle(self):
        '''
        Alle umbenennen
        '''
        print("# Gui.m_on_alle #")
        # Alle Dateien umbenennen
        self.ob_rename.m_aendernalle()
        # Verzeichnis erneut lesen
        self.m_readverz()


    def m_set_vorschau(self):
        '''
        Erstellt die Vorschau
        '''
        print("# Gui.m_set_vorschau #")
        # Wurde das Verzeichnis gelesen
        if self.ob_verzeich.ls_dateien or self.ob_verzeich.ls_verzeich:
            # Dateien oder Verzeichnisse sind vorhanden, Modus lesen
            tx_item = self.ob_modus.get()
            in_id = self.ls_modus.index(tx_item)
            # Input A lesen
            tx_inpA = self.ob_inputAvar.get()
            # Input B Lesen
            tx_inpB = self.ob_inputBvar.get()
            # Sind alle Eingaben gemacht
            ''' print("".join([
                "Modus=", tx_item, "\n",
                "ID=", str(in_id), "\n",
                "Input A=", tx_inpA, "\n",
                "Input B=", tx_inpB, "\n"
            ])) '''
            if tx_item and tx_inpA and tx_inpB:
                # Umbenennen vorbereiten, nach in_id modus wählen:
                # 0 = Zeichen ersetzen mit Suchen
                # 1 = Zeichen ersetzen am Anfang
                # 2 = Zeichen ersetzen am Ende
                # 3 = Zeichen einfügen am Anfang
                # 4 = Zeichen einfügen am Ende
                # 5 = Zeichen löschen am Anfang
                # 6 = Zeichen löschen am Ende
                if in_id in [0, 1, 2]:
                    # Ersetzen: Modus
                    dc_modus = {0: "SUCHE", 1: "START", 2: "ENDE"}
                    self.ob_rename.tx_modus = dc_modus[in_id]
                    # Suchtext und Neuer Text
                    self.ob_rename.tx_alt = tx_inpA
                    self.ob_rename.tx_neu = tx_inpB
                    # Ersetzen vorbereiten
                    self.ob_rename.m_ersetzen()
                elif in_id in [3, 4]:
                    # Einfügen: Modus
                    dc_modus = {3: "START", 4: "ENDE"}
                    self.ob_rename.tx_modus = dc_modus[in_id]
                    # Position
                    try:
                        in_pos = int(tx_inpA)
                    except Exception:
                        in_pos = 0
                    self.ob_rename.in_position = in_pos
                    # Text
                    self.ob_rename.tx_neu = tx_inpB
                    # Einfügen vorbereiten
                    self.ob_rename.m_einfuegen()
                elif in_id in [5, 6]:
                    # Löschen: Modus
                    dc_modus = {5: "START", 6: "ENDE"}
                    self.ob_rename.tx_modus = dc_modus[in_id]
                    # Position
                    try:
                        in_pos = int(tx_inpA)
                    except Exception:
                        in_pos = 0
                    self.ob_rename.in_position = in_pos
                    # Anzahl Zeichen
                    try:
                        in_anz = int(tx_inpB)
                    except Exception:
                        in_anz = 0
                    self.ob_rename.in_anzahl = in_anz
                    # Löschen vorbereiten
                    self.ob_rename.m_loeschen()
            else:
                # Nicht alle Eingaben wurden gemacht
                self.ob_rename.dc_rename = {}
            # Vorschau erstellen / Liste vorbereiten mit Titel
            tx_t = "VERZEICHNISPFAD: {0}".format(
                self.ob_verzeich.tx_stammpfad
            )
            ls_gui = [tx_t]
            # Verzeichnisse / Titel anfügen
            ls_gui.append("")
            ls_gui.append("VERZEICHNISSE")
            # Verzeichnis sortieren
            self.ob_verzeich.ls_verzeich.sort()
            for self.tx_vorschau_pfad in self.ob_verzeich.ls_verzeich:
                # Vorschautext erstellen und der Liste anfügen
                self.m_set_vorschautext()
                ls_gui.append(self.tx_vorschau_liste)
            # Dateien / Titel anfügen
            ls_gui.append("")
            ls_gui.append("DATEIEN")
            # Dateien sortieren
            self.ob_verzeich.ls_dateien.sort()
            for self.tx_vorschau_pfad in self.ob_verzeich.ls_dateien:
                # Vorschautext erstellen und der Liste anfügen
                self.m_set_vorschautext()
                ls_gui.append(self.tx_vorschau_liste)
        else:
            # Das Verzeichnis wurde nicht gelesen
            ls_gui = ["KEIN VERZEICHNIS GELESEN"]
        # Liste leeren
        self.ob_liste.delete(0, tkinter.END)
        # Liste abfüllen
        in_id = 0
        for tx_item in ls_gui:
            in_id += 1
            self.ob_liste.insert(in_id, tx_item)

    def m_set_vorschautext(self):
        '''
        Vorschautext erstellen
        '''
        print("# Gui.m_set_vorschautext #")
        # Werte auslesen
        dc_rename = self.ob_rename.dc_rename
        tx_pfad = self.tx_vorschau_pfad
        if tx_pfad in dc_rename.keys():
            # Umbenennung für diesen Pfad ist vorbereitet
            self.tx_vorschau_liste = "- {0}   >>   {1}".format(
                os.path.basename(tx_pfad),
                os.path.basename(dc_rename[tx_pfad])
            )
            # print("# {0} #".format(dc_rename[tx_pfad]))
            # print("# {0} #".format(dc_rename.keys()))
        else:
            self.tx_vorschau_liste = "- {0}".format(
                os.path.basename(tx_pfad))
            # print("# {0} #".format(tx_pfad))
            # print("# {0} #".format(dc_rename.keys()))


if __name__ == '__main__':
    ob_root = tkinter.Tk()
    ob_gui = Gui(ob_root)
    ob_root.mainloop()

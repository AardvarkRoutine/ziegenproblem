from tkinter import *
from PIL import Image, ImageTk
import random

# Hauptfenster erstellen
fenster = Tk()
fenster.title("Automatisch maximiertes Fenster")
fenster.state('zoomed')
fenster.configure(bg='#B22222')  # FireBrick Rot

# Spielstatus
ausgewählte_türen = []
preise = ['Niete', 'Niete', 'Auto']
random.shuffle(preise)

spiel_vorbei = False  # Spielstatus

# Bilder laden (Originale behalten)
bild_tür_geschlossen_original = Image.open("door_closed.png")
bild_tür_offen_original = Image.open("door_open.png")
bild_auto_original = Image.open("auto.png")
bild_moderator_original = Image.open("moderator.png")

# Platzhalter für die dynamisch skalierten Bilder
bild_tür_geschlossen = None
bild_tür_offen = None
bild_auto = None
bild_moderator = None

# Container für den unteren Bereich (Moderator + Textzeile)
unterer_bereich = Frame(fenster, bg='#B22222')
unterer_bereich.grid(row=1, column=0, columnspan=3, pady=20)

# Moderator-Bild
moderator_label = Label(unterer_bereich, bg='#B22222')
moderator_label.pack(side=LEFT, padx=10)

# Textzeile (Statusanzeige)
status_label = Label(unterer_bereich, text="Wähle eine Tür und finde den Gewinn!", bg='#B22222', fg='gold', font=('Arial', 20, 'bold'))
status_label.pack(side=LEFT)

# Liste der Tür-Buttons zur späteren Aktualisierung
tür_buttons = []

# Funktion zur dynamischen Bildskalierung
def bilder_aktualisieren(event=None):
    global bild_tür_geschlossen, bild_tür_offen, bild_auto, bild_moderator

    # Neue Größen berechnen basierend auf Fenstergröße
    neue_breite = max(int(fenster.winfo_width() / 4), 100)
    neue_höhe = int(neue_breite * 2)

    # Türbilder anpassen (ohne Seitenverhältnis zu verlieren)
    tür_geschlossen_skaliert = bild_tür_geschlossen_original.resize((neue_breite, neue_höhe), Image.ANTIALIAS)
    tür_offen_skaliert = bild_tür_offen_original.resize((neue_breite, neue_höhe), Image.ANTIALIAS)

    bild_tür_geschlossen = ImageTk.PhotoImage(tür_geschlossen_skaliert)
    bild_tür_offen = ImageTk.PhotoImage(tür_offen_skaliert)

    # Auto proportional skalieren
    auto_verhältnis = bild_auto_original.width / bild_auto_original.height
    max_auto_breite = neue_breite
    max_auto_höhe = neue_höhe

    if max_auto_breite / auto_verhältnis <= max_auto_höhe:
        auto_größe = (int(max_auto_breite), int(max_auto_breite / auto_verhältnis))
    else:
        auto_größe = (int(max_auto_höhe * auto_verhältnis), int(max_auto_höhe))

    auto_skaliert = bild_auto_original.resize(auto_größe, Image.ANTIALIAS)
    bild_auto = ImageTk.PhotoImage(auto_skaliert)

    # Moderator proportional skalieren
    moderator_verhältnis = bild_moderator_original.width / bild_moderator_original.height
    moderator_höhe = int(status_label.winfo_reqheight() * 1.2)
    moderator_größe = (int(moderator_höhe * moderator_verhältnis), moderator_höhe)

    moderator_skaliert = bild_moderator_original.resize(moderator_größe, Image.ANTIALIAS)
    bild_moderator = ImageTk.PhotoImage(moderator_skaliert)

    moderator_label.config(image=bild_moderator)

    # Alle Tür-Buttons aktualisieren
    for index, button in enumerate(tür_buttons):
        if (index + 1) in ausgewählte_türen:
            preis = preise[index]
            if preis == 'Auto':
                button.config(image=bild_auto)
            else:
                button.config(image=bild_tür_offen)
        else:
            button.config(image=bild_tür_geschlossen)

# Funktion für den Klick auf eine Tür
def tür_geklickt(tür_nummer, button):
    global ausgewählte_türen, spiel_vorbei

    if spiel_vorbei or tür_nummer in ausgewählte_türen or len(ausgewählte_türen) >= 2:
        return  # Entweder Spiel vorbei, Tür schon gewählt oder Maximum erreicht

    preis = preise[tür_nummer - 1]
    if preis == 'Auto':
        status_label.config(text="Glückwunsch! Du hast das Auto gewonnen!")
        button.config(image=bild_auto)
        spiel_vorbei = True
    else:
        button.config(image=bild_tür_offen)
        if len(ausgewählte_türen) == 0:
            status_label.config(text="Leider eine Niete. Du darfst noch eine Tür wählen.")
        else:
            status_label.config(text="Leider wieder eine Niete. Spiel beendet.")
            spiel_vorbei = True

    ausgewählte_türen.append(tür_nummer)

# Funktion zur Erstellung der Tür-Buttons
def tür_erstellen(parent, text, tür_nummer):
    button = Button(parent, text=text, compound='top', bg='#8B0000', fg='white', font=('Arial', 24, 'bold'))
    button.config(command=lambda b=button: tür_geklickt(tür_nummer, b))
    button.grid(row=0, column=tür_nummer - 1, padx=40, pady=40, sticky="nsew")
    tür_buttons.append(button)
    return button

# Grid-Konfiguration für gleichmäßige Verteilung
fenster.grid_rowconfigure(0, weight=1)
for i in range(3):
    fenster.grid_columnconfigure(i, weight=1)

# Türen erstellen
tür_erstellen(fenster, "Tür 1", 1)
tür_erstellen(fenster, "Tür 2", 2)
tür_erstellen(fenster, "Tür 3", 3)

# Initiale Skalierung durchführen
bilder_aktualisieren()

# Event-Handler für Fenstergröße
fenster.bind('<Configure>', bilder_aktualisieren)

# Hauptloop starten
fenster.mainloop()

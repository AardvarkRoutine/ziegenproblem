from tkinter import *
from PIL import Image, ImageTk
import random

# Hauptfenster erstellen
root = Tk()
root.title("Automatisch maximiertes Fenster")
root.state('zoomed')
# Hintergrundfarbe setzen
root.configure(bg='#B22222')  # FireBrick Rot

# Spielzustände
selected_doors = []
prizes = ['Niete', 'Niete', 'Auto']
random.shuffle(prizes)

game_over = False  # Spielstatus

# Bilder laden (Originale behalten)
door_closed_original = Image.open("door_closed.png")
door_open_original = Image.open("door_open.png")
auto_original = Image.open("auto.png")
moderator_original = Image.open("moderator.png")

# Platzhalter für die Bilder
door_closed_photo = None
door_open_photo = None
auto_photo = None
moderator_photo = None

# Feame für Ergebnisbereich
bottom_frame = Frame(root, bg='#B22222')
bottom_frame.grid(row=1, column=0, columnspan=3, pady=20)

# Moderator-Bild
moderator_label = Label(bottom_frame, bg='#B22222')
moderator_label.pack(side=LEFT, padx=10)

# Ergebnis-Label
result_label = Label(bottom_frame, text="Wähle eine Tür und finde den Gewinn!", bg='#B22222', fg='gold', font=('Arial', 20, 'bold'))
result_label.pack(side=LEFT)

# Tür-Buttons speichern, damit wir sie bei Resize neu setzen können
door_buttons = []

# Funktion zur dynamischen Bildskalierung
def resize_images(event=None):
    global door_closed_photo, door_open_photo, auto_photo, moderator_photo

    # Berechne neue Größe abhängig vom Fenster
    new_width = max(int(root.winfo_width() / 4), 100)
    new_height = int(new_width * 2)

    # Bilder skalieren (Türbilder vollflächig)
    door_closed_resized = door_closed_original.resize((new_width, new_height), Image.ANTIALIAS)
    door_open_resized = door_open_original.resize((new_width, new_height), Image.ANTIALIAS)

    door_closed_photo = ImageTk.PhotoImage(door_closed_resized)
    door_open_photo = ImageTk.PhotoImage(door_open_resized)

    # Auto skalieren proportional
    auto_ratio = auto_original.width / auto_original.height
    max_auto_width = new_width
    max_auto_height = new_height

    if max_auto_width / auto_ratio <= max_auto_height:
        auto_size = (int(max_auto_width), int(max_auto_width / auto_ratio))
    else:
        auto_size = (int(max_auto_height * auto_ratio), int(max_auto_height))

    auto_resized = auto_original.resize(auto_size, Image.ANTIALIAS)
    auto_photo = ImageTk.PhotoImage(auto_resized)

    # Moderator skalieren proportional
    moderator_ratio = moderator_original.width / moderator_original.height
    moderator_height = int(result_label.winfo_reqheight() * 1.2)
    moderator_size = (int(moderator_height * moderator_ratio), moderator_height)
    moderator_resized = moderator_original.resize(moderator_size, Image.ANTIALIAS)
    moderator_photo = ImageTk.PhotoImage(moderator_resized)
    moderator_label.config(image=moderator_photo)

    # Bilder der Buttons aktualisieren
    for idx, button in enumerate(door_buttons):
        if (idx + 1) in selected_doors:
            prize = prizes[idx]
            if prize == 'Auto':
                button.config(image=auto_photo)
            else:
                button.config(image=door_open_photo)
        else:
            button.config(image=door_closed_photo)

# Funktion, die beim Drücken einer Tür ausgelöst wird
def door_clicked(door_number, button):
    global selected_doors, game_over

    if game_over or door_number in selected_doors or len(selected_doors) >= 2:
        return  # Tür schon gewählt oder Maximum erreicht oder Spiel vorbei

    prize = prizes[door_number - 1]
    if prize == 'Auto':
        result_label.config(text="Glückwunsch! Du hast das Auto gewonnen!")
        button.config(image=auto_photo)
        game_over = True
    else:
        button.config(image=door_open_photo)
        if len(selected_doors) == 0:
            result_label.config(text="Leider eine Niete. Du darfst noch eine Tür wählen.")
        else:
            result_label.config(text="Leider wieder eine Niete. Spiel beendet.")
            game_over = True

    selected_doors.append(door_number)

# Drei Türen mit Grid-Layout erstellen
def create_door(parent, text, door_number):
    button = Button(parent, text=text, compound='top', bg='#8B0000', fg='white', font=('Arial', 24, 'bold'))
    button.config(command=lambda b=button: door_clicked(door_number, b))
    button.grid(row=0, column=door_number - 1, padx=40, pady=40, sticky="nsew")
    door_buttons.append(button)
    return button

# Grid-Konfiguration für gleiche Verteilung
root.grid_rowconfigure(0, weight=1)
for i in range(3):
    root.grid_columnconfigure(i, weight=1)

# Türen erstellen
create_door(root, "Tür 1", 1)
create_door(root, "Tür 2", 2)
create_door(root, "Tür 3", 3)

# Initiale Skalierung
resize_images()

# Event-Handler für Fenstergrößenänderung
root.bind('<Configure>', resize_images)

# Hauptloop starten
root.mainloop()
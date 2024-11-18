import serial
import time
import tkinter as tk
from tkinter import messagebox, ttk
import serial.tools.list_ports


# Variable pour la connexion série
ser = None

# Fonction pour lister les ports COM disponibles
def list_ports():
    """Liste les ports COM disponibles."""
    ports = [port.device for port in serial.tools.list_ports.comports()]
    return ports

# Fonction pour ouvrir la connexion série
def open_serial_connection():
    """Ouvre la connexion série avec le port sélectionné."""
    global ser
    port = port_combobox.get()
    if not port:
        messagebox.showerror("Erreur", "Veuillez sélectionner un port COM.")
        return

    try:
        ser = serial.Serial(port, 115200, timeout=1)
        time.sleep(2)  # Attendre que la communication série soit établie
        log_message(f"Connecté à {port}")
        status_label.config(text=f"Connecté à {port}")
        open_button.config(state=tk.DISABLED)
        close_button.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de se connecter au port {port}.")
        log_message(f"Erreur : {e}")

# Fonction pour fermer la connexion série
def close_serial_connection():
    """Ferme la connexion série."""
    global ser
    if ser:
        ser.close()
        ser = None
        status_label.config(text="Non connecté")
        open_button.config(state=tk.NORMAL)
        close_button.config(state=tk.DISABLED)
        log_message("Connexion série fermée")

# Fonction pour envoyer une commande G-code
def send_command(command):
    """Envoie une commande G-code à l'Arduino."""
    global ser
    if ser:
        ser.write(f"{command}\n".encode())
        log_message(f"Commande envoyée : {command}")
        time.sleep(0.1)
        response = ser.readline().decode().strip()
        if response:
            log_message(f"Réponse : {response}")

# Contrôle manuel des positions via sliders
def confirm_position():
    """Confirme la position choisie avec les sliders avant d'envoyer la commande."""
    x = x_slider.get()
    y = y_slider.get()
    send_command(f"G1 X{x} Y{y}")

# Animation prédéfinie (exemple : carré)
def run_animation():
    """Effectue une animation prédéfinie."""
    log_message("Démarrage de l'animation prédéfinie (carré).")
    animation_commands = [
        "G1 X0 Y0", "G1 X100 Y0", "G1 X100 Y100",
        "G1 X0 Y100", "G1 X0 Y0"
    ]
    for cmd in animation_commands:
        send_command(cmd)
        time.sleep(1)  # Pause pour visualiser les mouvements

# Gestion des macros
automation_commands = []

def add_to_automation():
    """Ajoute une commande à la liste d'automatisation."""
    command = gcode_entry.get()
    if command:
        automation_commands.append(command)
        automation_listbox.insert(tk.END, command)
        gcode_entry.delete(0, tk.END)

def execute_automation():
    """Exécute toutes les commandes de la liste d'automatisation."""
    if automation_commands:
        log_message("Exécution de l'automatisation.")
        for cmd in automation_commands:
            send_command(cmd)
            time.sleep(0.5)  # Pause entre les commandes
    else:
        log_message("Aucune commande à exécuter.")

def clear_automation():
    """Vide la liste d'automatisation."""
    global automation_commands
    automation_commands = []
    automation_listbox.delete(0, tk.END)

# Logs
def log_message(message):
    """Affiche un message dans la zone de logs."""
    log_textbox.insert(tk.END, f"{message}\n")
    log_textbox.see(tk.END)

# Interface graphique
root = tk.Tk()
root.title("Contrôle du bras robotique")

root.iconbitmap("C:/Users/Louis/Desktop/RobotControlv2/robot.ico")


# Ports COM
port_label = tk.Label(root, text="Choisir le port COM:")
port_label.grid(row=0, column=0, padx=10, pady=5)

port_combobox = ttk.Combobox(root, state="readonly")
port_combobox.grid(row=0, column=1, padx=10, pady=5)

open_button = tk.Button(root, text="Connecter", command=open_serial_connection)
open_button.grid(row=1, column=0, padx=10, pady=5)

close_button = tk.Button(root, text="Déconnecter", state=tk.DISABLED, command=close_serial_connection)
close_button.grid(row=1, column=1, padx=10, pady=5)

status_label = tk.Label(root, text="Non connecté", fg="red")
status_label.grid(row=2, column=0, columnspan=2, pady=5)

# Contrôle des moteurs avec sliders
x_slider = tk.Scale(root, from_=0, to=300, orient=tk.HORIZONTAL, label="Position X")
x_slider.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

y_slider = tk.Scale(root, from_=0, to=300, orient=tk.HORIZONTAL, label="Position Y")
y_slider.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

confirm_button = tk.Button(root, text="Confirmer position", command=confirm_position)
confirm_button.grid(row=5, column=0, columnspan=2, pady=5)

# Contrôle du laser
laser_on_button = tk.Button(root, text="Allumer Laser", command=lambda: send_command("M106 S49"))
laser_on_button.grid(row=6, column=0, padx=10, pady=5)

laser_off_button = tk.Button(root, text="Éteindre Laser", command=lambda: send_command("M107"))
laser_off_button.grid(row=6, column=1, padx=10, pady=5)

# Animation prédéfinie
animation_button = tk.Button(root, text="Lancer animation (carré)", command=run_animation)
animation_button.grid(row=7, column=0, columnspan=2, pady=5)

# Gestion des macros
gcode_label = tk.Label(root, text="Commande G-code personnalisée :")
gcode_label.grid(row=8, column=0, padx=10, pady=10)

gcode_entry = tk.Entry(root, width=20)
gcode_entry.grid(row=8, column=1, padx=10, pady=10)

add_command_button = tk.Button(root, text="Ajouter à l'automatisation", command=add_to_automation)
add_command_button.grid(row=9, column=0, columnspan=2, pady=10)

automation_label = tk.Label(root, text="Automatisation :")
automation_label.grid(row=10, column=0, padx=10, pady=10)

automation_listbox = tk.Listbox(root, width=30, height=10)
automation_listbox.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

execute_automation_button = tk.Button(root, text="Exécuter Automatisation", command=execute_automation)
execute_automation_button.grid(row=12, column=0, padx=10, pady=5)

clear_automation_button = tk.Button(root, text="Vider Automatisation", command=clear_automation)
clear_automation_button.grid(row=12, column=1, padx=10, pady=5)

# Logs
log_label = tk.Label(root, text="Logs en direct:")
log_label.grid(row=13, column=0, columnspan=2, pady=5)

log_textbox = tk.Text(root, width=50, height=10)
log_textbox.grid(row=14, column=0, columnspan=2, padx=10, pady=5)

# Mettre à jour les ports disponibles
def update_ports():
    """Met à jour la liste des ports COM."""
    ports = list_ports()
    port_combobox['values'] = ports
    if ports:
        port_combobox.current(0)

update_ports()

root.mainloop()

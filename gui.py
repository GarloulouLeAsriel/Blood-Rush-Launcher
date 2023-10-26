from pathlib import Path
from tkinter import *
from tkinter import ttk
import os
import requests
import zipfile
import subprocess
import threading  
import shutil


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")

try:
    with open('version.txt', 'r') as file:
        installed_version = file.read().strip()
except FileNotFoundError:
    installed_version = "0"  

print(installed_version)

filename = "version.txt"
pastebin_url = "https://pastebin.com/raw/LBFpUgAA"

response = requests.get(pastebin_url)
if response.status_code == 200:
    content = response.text

    lines = content.splitlines()

    if len(lines) >= 2:
        LastVer = lines[0]
        LastVerUrl = lines[1]

        print(LastVer)
        print(LastVerUrl)

update_url = LastVerUrl

update_dir = "updates"

game_executable = f"{update_dir}/hellscape.exe"

game_process = None  

def launch_game():
    global game_process  
    status_label.config(text="Le jeu est lancé")
    if os.path.isfile(game_executable):
        game_process = subprocess.Popen([game_executable])

        # Surveille l'état du processus
        game_process.poll()
        if game_process.returncode is not None:  
            status_label.config(text="Le Jeu A crash ")


def check_for_update():
    
    response = requests.head(update_url)
    if response.status_code == 200:

        if installed_version == LastVer:
            launch_game()

        else:
            download_and_install_update()






def download_and_install_update():
    def download_update_thread():
        status_label.config(text="Préparation en cours ...")
        response = requests.get(update_url, stream=True)
        if response.status_code == 200:
            if os.path.exists(update_dir):
                shutil.rmtree(update_dir)
                os.makedirs(update_dir) 
            else:
                os.makedirs(update_dir)
            status_label.config(text="Telechargement en cours...")
            update_file = os.path.join(update_dir, "update.zip")
            with open(update_file, "wb") as file:
                total_size = int(response.headers.get('content-length', 0))
                progress_bar = ttk.Progressbar(window, length=600, mode='determinate')  # Crée une barre de progression
                progress_bar.place(x=0.0, y=261.0) 
                progress = 0

                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    progress += len(data)
                    percentage = (progress / total_size) * 100
                    progress_bar['value'] = percentage
                    window.update_idletasks()  # Met à jour l'interface utilisateur

                progress_bar.destroy()
                status_label.config(text="Installation en cours...")

            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                zip_ref.extractall(update_dir)

            os.remove(update_file)

            status_label.config(text="Mise à jour installée avec succès.")

            with open(filename, 'w') as file:
                file.write(LastVer)
            launch_game()
        else:
            status_label.config(text="Échec du téléchargement de la mise à jour.")

    download_thread = threading.Thread(target=download_update_thread)
    download_thread.start()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Blood Rush Launcher")

window.geometry("600x400")
window.configure(bg = "#FFFFFF")
logo = PhotoImage(file="iconbitmap.gif")
window.call('wm', 'iconphoto', window._w, logo)


canvas = Canvas(
    window,
    bg = "#000000",
    height = 400,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    300.0,
    140.0,
    image=image_image_1
)

canvas.create_rectangle(
    27.0,
    280.0,
    865.0,
    426.0,
    fill="#000000",
    outline="#000000")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check_for_update(),
    relief="flat"
)
button_1.place(
    x=215.0,
    y=317.0,
    width=170.0,
    height=23.0
)

canvas.create_text(
    0.0,
    377.0,
    anchor="nw",
    text="Blood Rush Par MaxEstLa",
    fill="#FFFFFF",
    font=("Imprima Regular", 20 * -1)
)

canvas.create_text(
    320.0,
    377.0,
    anchor="nw",
    text="Launcher Par GarloulouLeAsriel",
    fill="#FFFFFF",
    font=("Imprima Regular", 20 * -1)
)

canvas.create_rectangle(
    0.0,
    261.0,
    600.0,
    280.0,
    fill="#000000",
    outline="")
status_label = Label(
    window,
    text="",
    fg="#FFFFFF",
    bg="#000000",
    font=("Imprima Regular", 12)
)
status_label.place(x=215.0, y=285.0,)
window.resizable(False, False)
window.mainloop()

#roulette russe
import random as nombre
import tkinter as tk
import threading
from PIL import Image, ImageTk
import time
import pygame
import os

# Constantes
son_clic_souris = "resources\clic_souris.mp3"
son_tir = "resources\son_tir.mp3"
son_chargement = "resources\son_chargement.mp3"

# Variables globales
score = 0
score_record =0
nb_balles_mortelles =1
nb_balles_blanches =6
son_activé=True

son_lock = threading.Lock()
pygame.mixer.init()

def verifier_fichier_audio(fichier_audio):
    # Vérifier si le fichier existe
    if not os.path.exists(fichier_audio):
        print(f"Erreur: Le fichier {fichier_audio} n'existe pas.")
        return False
    # Essayer de charger le fichier avec pygame pour vérifier qu'il est valide
    try:
        pygame.mixer.music.load(fichier_audio)
    except pygame.error as e:
        print(f"Erreur: Le fichier {fichier_audio} ne peut pas être lu. Détails: {e}")
        return False
    return True

# Fonction pour jouer un son avec pygame
def jouer_son(fichier_audio):
    if son_activé == True:
        with son_lock:  # Bloquer l'accès aux autres threads
            pygame.mixer.music.load(fichier_audio)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Attendre la fin du son
                pygame.time.wait(100)  # Attendre 100ms entre chaque vérification

# Fonction pour jouer un son dans un thread
def jouer_son_dans_thread(fichier_audio):
    threading.Thread(target=jouer_son, args=(fichier_audio,), daemon=True).start()

def charger_image(image_path):# Charger et redimensionner une image
    image = Image.open(image_path)
    image.thumbnail((max_width, max_height))  # Redimensionner l'image
    return ImageTk.PhotoImage(image)

def afficher_label_plus_un():# label "+1 animé quand on tire"
    label_plus_un.place(x=61, y=30)
    animer_score_flash(label_plus_un )
    roulette.after(500, lambda: label_plus_un.place_forget())  # Cache le label après 500 ms

def animer_score_flash(label, colors=["red", "white"], delay=100, repeat=5):#animer augmentation score et le "+1" 
    def flasher(count=0):
        if count < repeat:
            current_color = colors[count % len(colors)]
            label.config(fg=current_color)
            label.after(delay, flasher, count + 1)
        else:
            label.config(fg="black")  # Remet la couleur à la normale
    flasher()

def quitter_programe():
    print("Sortie du programme")
    roulette.destroy()

def tirer():# Fonction principale pour simuler le tir
    global score
    global score_record
    score += 1
    balle_tiree = nombre.randint(nb_balles_mortelles, nb_balles_blanches)
    jouer_son_dans_thread(son_clic_souris)
    time.sleep(1.2)
    if balle_tiree < nb_balles_blanches:  # balle blanche
        print("Vous avez survécu x",score)
        score_label.config(text="Score: " + str(score))
        afficher_label_plus_un()
        animer_score_flash(score_label)
        jouer_son_dans_thread(son_chargement)
    else:  # balle qui tue
        jouer_son_dans_thread(son_tir)
        print("Vous êtes morts")
        score_label.config(text="Vous êtes mort!\nScore final: " + str(score))
        print("Score final:", score)
        bouton_tirer.place_forget()
        label_revolver.pack_forget()
        label_tombe.pack(side=tk.RIGHT, padx=20, pady=20)
        bouton_rejouer.place(x=120, y=235)
        bouton_menu.place(x=20, y=20)
        score_label.place(x=170, y=20)
        score_record_label.place(x=170, y=20)
        if score >= score_record:
            score_record = score
            score_record_label.config(text="Score record: " + str(score_record))
        score_record_label.place(x=170, y=20)

def rejouer():#rejouer une partie
    jouer_son_dans_thread(son_clic_souris)
    global score
    score=0
    score_label.place(x=20, y=50)
    bouton_rejouer.place_forget()
    label_tombe.pack_forget()
    score_record_label.place_forget()
    bouton_menu.place_forget()
    label_revolver.pack()
    bouton_tirer.place(x=148, y=200)
    score_label.config(text="Score: " + str(score))

def menu_du_jeu ():#main menu
    label_tombe.pack_forget()
    score_record_label.place_forget()
    score_label.place_forget()
    label_crédits.place_forget()
    bouton_parametres.place_forget()
    bouton_son_on_off.place_forget()
    bouton_menu.place_forget()
    bouton_rejouer.place_forget()
    label_chargeur.pack()
    titre_menu.place(x=75, y=0)
    bouton_jouer.place(x=130, y=105)
    bouton_parametres.place(x=182, y=146)
    bouton_quitter.place(x=60, y=224)
    bonton_crédits.place(x=60, y=146)

def charger_crédits():
    label_chargeur.pack_forget()
    titre_menu.place_forget()
    bouton_parametres.place_forget()
    bouton_jouer.place_forget()
    bonton_crédits.place_forget()
    bouton_parametres.place_forget()
    bouton_quitter.place_forget()
    label_crédits.place(x=60, y=280)
    bouton_menu.place(x=20, y=50)

def parametres():
    label_chargeur.pack_forget()
    titre_menu.place_forget()
    bouton_parametres.place_forget()
    bouton_jouer.place_forget()
    bonton_crédits.place_forget()
    bouton_parametres.place_forget()
    bouton_quitter.place_forget()
    bouton_son_on_off.place(x=100, y=150)
    bouton_menu.place(x=20, y=50)

def son_on_off():
    global son_activé
    if bouton_son_etat.get():
        bouton_son_on_off.config(text="Off")
        son_activé=False
    else:
        bouton_son_on_off.config(text="On")
        son_activé=True

def démarrage_jeu():
    print('jeu demmarre')
    label_chargeur.pack_forget()
    titre_menu.place_forget()
    bouton_parametres.place_forget()
    bouton_jouer.place_forget()
    bouton_parametres.place_forget()
    bouton_quitter.place_forget()
    bonton_crédits.place_forget()
    bouton_tirer.place(x=146, y=200)
    score_label.place(x=20, y=50)
    label_revolver.pack()

# Paramètres de la fenêtre
max_width = 390
max_height = 400
roulette = tk.Tk()
roulette.title("Roulette Russe")
roulette.iconbitmap('resources/balle_roulette.ico')
roulette.geometry("300x400")
roulette.resizable(False, False)
roulette.config(bg="lightgrey")

# Charger les images
photo_revolver = charger_image("resources/chargeur.jpg")
photo_tombe = charger_image("resources/tombes_dessins.jpg")
photo_chargeur = charger_image("resources/chargeur.jpg")
# Créer un label pour les images
label_revolver = tk.Label(roulette, image=photo_revolver, bg="lightgrey")
label_tombe = tk.Label(roulette, image=photo_tombe, bg="lightgrey")
label_chargeur = tk.Label(roulette, image=photo_chargeur, bg="lightgrey")
# Création des labels pour afficher les résultats
score_label = tk.Label(roulette, text="Score: " + str(score), bg="lightgrey", font=("Arial", 12))
label_plus_un = tk.Label(roulette, text="+1", bg="lightgrey", font=("Arial", 12))
score_record_label = tk.Label(roulette, text="Score reccord: " + str(score), bg="lightgrey", font=("Arial", 12))

titre_menu = tk.Label(roulette, text="roulette russe !", bg="lightgrey", font=("Arial", 18))

label_crédits=tk.Label(roulette, text="game made by kelqu'1\n with love <3", bg="lightgrey", font=("Forte", 14))

#boutons

bouton_menu =tk.Button(roulette, text="retour\n au menu", bg="black", fg="white", command=menu_du_jeu, bd=2, relief="ridge")
bouton_jouer =tk.Button(roulette, text="jouer", bg="black", fg="white", command= démarrage_jeu, bd=2, relief="ridge")
bonton_crédits =tk.Button(roulette, text="crédits", bg="black", fg="white", command=charger_crédits, bd=2, relief="ridge")
bouton_quitter =tk.Button(roulette, text="quitter", bg="black", fg="white", command=quitter_programe, bd=2, relief="ridge")
bouton_parametres =tk.Button(roulette, text="paramètres", bg="black", fg="white", command= parametres, bd=2, relief="ridge")
bouton_son_etat = tk.IntVar()
bouton_son_on_off =tk.Checkbutton(roulette, text="On",variable=bouton_son_etat, onvalue=1, offvalue=0, bg="black", fg="white", command= son_on_off, bd=2, relief="ridge")
bouton_tirer =tk.Button(roulette, text="Tirer", bg="black", fg="white", command=tirer, bd=2, relief="ridge")
bouton_rejouer =tk.Button(roulette, text="réessayer", bg="black", fg="white", command=rejouer, bd=2, relief="ridge")

menu_du_jeu ()

#tester la validité des sons 
if verifier_fichier_audio(son_clic_souris) and verifier_fichier_audio(son_tir) and verifier_fichier_audio(son_chargement):
    print("Tous les fichiers audio sont valides.")
    roulette.mainloop()# Démarrer la boucle principale de l'interface
else:
    print("Un ou plusieurs fichiers audio sont invalides.")
    print("le programme ne demarre pas du à une erreur")
# coding: utf-8
#Importation de la bibliothèque Tkinter

from tkinter import *
import tkinter.font as tkFont
from tkinter.messagebox import *
from tkinter.colorchooser import askcolor

#importation randint,choice de random
from random import randint,choice

#bibliothèque nécéssaires à la lecture de fichier externe
import json
import os.path
import os
#Importation de la bibliothèque image de Tkinter
from PIL import ImageTk, Image
#sauvegarde
global_color=("#2A9D8F","#E9C46A","#F4A261","#E76F51","#264653")#https://coolors.co/264653-2a9d8f-e9c46a-f4a261-e76f51

base_mots="base.txt"#base contenant 22k mots, pour Sutom
with open(base_mots,"r",encoding="utf-8") as f:
    ListeMots=f.readlines()

save_path=".data.save"#le nom du fichier de Sauvegarde
if not os.path.exists(save_path):#si le fichier n'existe pas
    with open(save_path,"w") as f:f.write('{"color":["#6b0505","#04195d","#474038","#d9d9d9"]}')#on crée le fichier
    print("Aucune sauvegarde trouvée, création d'un nouveau fichier de sauvegarde vide")#log

ModeDaltonien=0#Le ModeDaltonien sert aux personnes disposant de problèmes de visibilités

def rickroll():
    """
    Cette fonction ouvre le navigateur, et lance un rickroll
    """
    os.system('xdg-open https://link.discode.fr/images/rick.webm')#ouvrir le navigateur sous système Unix (Linux, MacOS, ...)
    os.system('start https://link.discode.fr/images/rick.webm')#ouvrir le navigateur sous système Windows

def black_or_white(color):
    """
    color : str, une couleur en hex
    Cette fonction renvoie la couleur qui aurait le meilleur contraste avec la couleur, entre noir ou blanc en hex
    """
    rgb_couleur=list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))#transformation du hex en rgb
    if (rgb_couleur[0]*0.299 + rgb_couleur[1]*0.587 + rgb_couleur[2]*0.114) > 186:
        return "#000000"#si la couleur  est claire
    else:return "#ffffff"#si la couleur  est foncée

class Save:#classe qui n'a pas besoin d'initialisation
    def edit(jeu:str,data):
      """
        prends en paramètres :
        jeu : str
        data : str,float,liste,tuple,dictionnaire

        Sauvegarde les données pour le jeu
      """
      try:
        with open(save_path,"r") as f:#ouvrir fichier en mode lecture
            a=json.load(f);print("Sauvegarde modifiée");a[jeu]=data#on lit, et change les données + log
        with open(save_path,"w") as f:#ouvrir fichier en mode écriture
            json.dump(a,f)#on enregistre en json
      except:print("Sauvegarde corrompue")#log erreur

    def load(jeu:str):
        """
        paramètre :
        jeu : str

        Renvoie les données sauvegardé pour le jeu
        """
        with open(save_path,"r") as f:#ouvrir fichier en mode lecture
            try:a=json.loads(f.read());return a.get(jeu,None)#on obtient l'élément + log
            except:print("Sauvegarde corrompue")#log erreur
#Mode et réglages
class Param:
    """
    Les différents paramètres pour rendre l'expérience de jeu la plus agréable possible
    """
    def daltonien():
        """
        Active le mode ModeDaltonien, qui permet d'afficher des caractères dans les cases afin d'aider à différencier les différentes couleurs
        """
        global ModeDaltonien
        ModeDaltonien=1-ModeDaltonien#inverser le ModeDaltonien
    def color_choice():
        """
        fonction qui permet de modifier les couleurs par défaut, accessible via Save.load("color)
        """
        a=[]
        for id_c in range(len(Save.load("color"))):#pour id_c dans la longueur de Save.load("color")
            b=askcolor(color="#"+str(randint(111111,999999)), title="Couleur "+str(id_c))[1]
            if b not in a and "#" in str(b):#si la couleur n'existe pas dans la liste de couleur, et que la couleur est bien en hex
                a.append(b)#on ajoute la couleur à la liste
            else:a.append(["#6b0505","#04195d","#474038","#d9d9d9"][id_c])#sinon, mets la couleur par défaut
        Save.edit("color",a)
#grille
class Grille :
    """
    Éléments principal des jeux, la grille s'adapte partout, selon la taille requise, elle peut aussi afficher des caractères afin d'aider à différentier les couleurs
    """
    def __init__(self,longueur,hauteur,fonction,master,mode_fast=0,highlightcolor=""):
        """
        Attributs : longueur, hauteur, fonction, master, mode_fast, highlightcolor
        longueur, hauteur (int): nombre de bouton par ligne et par colonne
        fonction (fonction): la fonction qui sera lancée lors d'un clique sur une case de la grille (la fonction doit prendre un seul argument)
        master (TopLevel/Tk) : la fenêtre où sera placée la grille
        mode_fast (booléen) : si le booléen est vrai, aucune grille ne sera affichée et la vitesse de calcul pour la grille augmentera, sert lors de la génération de certains jeux
        highlightcolor : couleur de surlignage des boutons


        Créer une grille avec ces boutons de hauteur et longueur donné avec une fonction donnée pour master
        """
        #définition des constantes
        self.longueur=longueur
        self.hauteur=hauteur
        self.fonction=fonction
        self.mode_fast=mode_fast
        #définition des variables
        self.listebutton=[]#on va bientôt stocker tous nos boutons dans cette liste
        self.l_color=[]#sert au mode daltonien
        colonnes = []
        for y in range(self.hauteur):
            colonnes.append(Frame(master) if not self.mode_fast else "")#on ajoute une Frame
            for x in range(self.longueur):
                if not self.mode_fast:#si le mode fast n'est pas actif
                    self.listebutton.append(Button(colonnes[y],bg="#d9d9d9",))#on ajoute les boutons
                    self.listebutton[x+y*self.longueur].configure(command=lambda x=x,y=y:fonction((x,y)))
                    if highlightcolor!="":#si le surlignage n'est pas vide
                        self.listebutton[x+y*self.longueur].configure(highlightbackground=highlightcolor,highlightcolor=highlightcolor,highlightthickness=1,command=lambda x=x,y=y:fonction((x,y)))#on ajoute le surlignage si définit
                    self.listebutton[y*self.longueur+x].pack(fill="both",expand=True,side=LEFT)#place(relx=x/self.longueur,rely=1,anchor=W)
                else:#si le mode_fast est actif
                    self.listebutton.append({"color":"#d9d9d9"})
            if not self.mode_fast:
                colonnes[y].pack(fill="both", expand=True)
        #on les recolore (pour le ModeDaltonien )
        for y in range(self.hauteur):
            for x in range(self.longueur):
                self.setColor(x,y,Save.load("color")[3])
            
    def setColor(self,x,y,color):
        """
        paramètres : x,y,couleur
        Permet de changer la couleur d'un bouton précis
        """
        DaltonLettre=""
        if not self.mode_fast:#si le mode fast n'est pas actif
            if ModeDaltonien and "#" in color:#si le mode daltonien est actif et que la couleur est bien en hex
                if color in self.l_color:#si la couleur est dans la liste l_color
                    DaltonLettre="AZERTYUIOPQSDFGHJKLMWXCVBN?#123456789=+%*-"[self.l_color.index(color)]#si la couleur  est dans la liste couleurs, on mets le caractère assigné à cette couleur
                else:#sinon
                    self.l_color.append(color)#on ajoute à la liste couleur
                    DaltonLettre="AZERTYUIOPQSDFGHJKLMWXCVBN?#123456789=+%*-"[self.l_color.index(color)]#on mets le caractère correspondant à la position de la couleur dans la liste
                    self.listebutton[x+y*self.longueur].configure(fg=black_or_white(color))#on définit la couleur du texte pour ce bouton (black_or_white renvoye la couleur avec le plus de contraste)
            self.listebutton[x+y*self.longueur].configure(bg=color,activebackground=color,text=DaltonLettre)#changer la couleur du bouton selon sa position x, y
        else:#sinon
            self.listebutton[x+y*self.longueur]["color"]=color#on change la couleur

    def getColor(self,x,y):
        """
        paramètres x,y
        renvoye la couleur bg du bouton
        """
        if not self.mode_fast:#si le mode fast n'est pas actif
            return self.listebutton[x+y*self.longueur].cget('bg')#on récupére la valeur sur le bouton
        else:#si le mode_fast est actif
            return self.listebutton[x+y*self.longueur]["color"]#on récupére la valeur dans le dict
    def setImg(self,x,y,photo):
        """
        permet de changer l'image d'un bouton
        """
        self.listebutton[x+y*self.longueur].configure(image=photo)#change l'image
    def getImg(self,x,y):
        """
        paramètres x,y
        renvoye l'image' du bouton
        """
        return self.listebutton[x+y*self.longueur].cget('image')#on renvoie image
    def setText(self,x,y,text):
        """
        permet de changer le texte d'un bouton
        """
        if not self.mode_fast:
            try:self.listebutton[x+y*self.longueur].configure(text=text,fg=black_or_white(self.listebutton[x+y*self.longueur]["bg"]))#on essaye de changer le texte du bouton
            except:showerror("Couleur invalide","Merci de changer la couleur vers une valeur hex avant d'afficher du texte")#en cas d'erreur, on en informe l'utilisateur
        else:
           self.listebutton[x+y*self.longueur]["text"]=text#on assigne la valeur dans le dict
    def getText(self,x,y):
        """
        Renvoie le texte de x y
        """
        if not self.mode_fast:#si le mode fast n'est pas actif
            return self.listebutton[x+y*self.longueur].cget('text')#on récupére le texte sur le bouton
        else:#si le mode_fast est actif
            return self.listebutton[x+y*self.longueur].get("text",None)#on récupére la valeur dans le dict

#----MENU-----
class Welcome:#cette élément sera la popup principale, affiche la bibliothèque des jeux
    def propos(self) :
        """
        Popup "À propos"
        """
        propos = Toplevel()#On fonde l'élément#On fonde l'élément de la fenêtre
   
        propos.title("A propos")#on définit le titre
   
        propos.geometry("400x300")#on définit la taille de la fenêtre
   
        propos.resizable(width=False, height=False)#ne pas redimentionner la fenêtre
   
        texte1 = Label(propos, text="Groupe :", font="BOLD")#on définit la première ligne
        texte1.pack()#on place le texte
        texte2 = Label(propos, text="Yannis, Quentin, Matéo,", font="BOLD")#on définit la ligne suivante
        texte2.pack()#on place le texte
        texte3 = Label(propos, text="François, Alexandre\n\n\nLes icones ont été réalisée via Krita\nou trouvée sur https://www.flaticon.com", font="BOLD")#on définit la ligne suivante
        texte3.pack()#on place le texte
   
        boutonq=Button(propos, text="Quitter", command=propos.destroy)#on définit le bouton "quitter"
        boutonq.place(x=180, y=260, anchor=CENTER)#on place le bouton
   
        propos.mainloop()#on lance la fenêtre
   
    def contact(self) :
        """
        Popup "Contact"
        """
        contact = Toplevel()#On fonde l'élément#On fonde l'élément de la fenêtre
   
        contact.title("Contact")#on définit le titre
   
        contact.geometry("400x300")#on définit la taille
   
        contact.resizable(width=False, height=False)#ne pas redimentionner la fenêtre
   
        texte1 = Label(contact, text="Groupe :", font="BOLD")#on définit la première ligne
        texte1.pack()#on place le texte
        texte2 = Label(contact, text="Yannis, Quentin, Matéo,", font="BOLD")#on définit la ligne suivante
        texte2.pack()#on place le texte
        texte3 = Label(contact, text="François, Alexandre", font="BOLD")#on définit la ligne suivante
        texte3.pack()#on place le texte
   
        boutonq=Button(contact, text="Quitter", command=contact.destroy)#on définit le bouton "quitter"
        boutonq.place(x=180, y=260,anchor=CENTER)#on place le bouton
   
        contact.mainloop()#on lance la fenêtre

#fonctions qui affichent une popup du réglement
    def quarto_regles(self):
        showinfo('Règles de Quarto', 'Règles de Quarto :' + '\n' + '\n' + '- Mode de jeu : Duo' + '\n' + ' - À chaque tour, chaque joueur :' + '\n' + ' - Doit choisir une pièce pour son adversaire,\nl\'adversaire doit alors la placer\n,pour gagner, il suffit d\'aligner 4 pièce\navec une caractéristique similaire, par exemple : cercle rouge')

    def rush_hour_regles(self):
        showinfo('Règles de Rush Hour', 'Règles de Rush Hour :' + '\n' + '\n' + '- Mode de jeu : Solo' + '\n' + ' - déplacez les véhicules bloquant votre passage de haut en bas et de gauche à droite et vice-versa, jusqu’à ce que la voie se libère, permettant à votre voiture rouge de quitter l’embouteillage.')
   
    def grattes_ciel_regles(self):
        showinfo('Règles du Grattes Ciel', 'Règles du Grattes Ciel :' + '\n' + '\n' + '- Mode de jeu : Solo' + '\n' + ' - Une grille de carrés représente la zone de la ville occupée par les gratte-ciel.\nChaque ligne et chaque colonne de cette grille est occupée par un bâtiment avec un nombre d\'étages différent, de 1 à N. N est la taille de la grille.\nPar exemple, pour une grille 4x4, chaque ligne et chaque colonne doit contenir les nombres 1, 2, 3 et 4 représentant les bâtiments.\nLe bâtiment est le seul de sa seule hauteur dans la rangée et la colonne qu\'il occupe.\nDes indices à l’extérieur de la grille indiquent le nombre d’immeubles vus de ce point de vue.\nSachant qu’un immeuble cache derrière lui tous les immeubles plus petits, on ne pourra pas voir un immeuble de 1 ou 2 étages situés derrière un immeuble de 3 étages d’un certain point de vue.\nLes indices doivent mener à une solution unique.\nLe but du jeu est de trouver l\'emplacement des bâtiments à l\'intérieur de la grille à partir d\'indices extérieurs à la grille.')
   
    def nerdle_regles(self):
        showinfo('Règles de Nerdle', 'Règles de Nerdle :' + '\n' + '\n' + '- Mode de jeu : Solo' + '\n' + ' - Devinez le NERDLE en 6 essais. Après chaque supposition, la couleur des tuiles changera pour montrer à quel point votre supposition était proche de la solution. \nRègles :\nChaque supposition est un calcul.\nVous pouvez utiliser 0 1 2 3 4 5 6 7 8 9 + - * / ou =.\nIl doit contenir un seul "=".\nIl ne doit y avoir qu\'un nombre entier à droite du "=", pas un autre calcul.\nL\'ordre standard des opérations s\'applique, donc calculez * et / avant + et - par exemple. 3+2*5=13 pas 25!.\nLes quotients peuvent être euclidien (//) ou décimale (/)')
   
    def mastermind_regles(self):
        showinfo('Règles du Mastermind', 'Règles du Mastermind :' + '\n' + '\n' + '- Mode de jeu : Duo' + '\n' + ' - Le premier joueur va choisir une combinaison de couleurs\n le chercheur devra alors trouver cette combinaison. Pour l\'aider, il dispose de plusieurs essais. À chaque essai, des lettres et couleurs s\'afficheront à côté de votre essai :\n   -\"C\" Vert - Correct\n     -\"P\" Rouge - Mal placé\n      -\"N\" Noir - Non existant',)
   
    def bataille_navale_regles(self):
        showinfo('Règles de la Bataille Navale', 'Règles de la Bataille Navale :' + '\n' + '\n' + '- Mode de jeu : Solo' + '\n' + ' - Placez vos navires, capitaines, placez les, mais faites bien attention à respecter le placement indiqué par sur le coté')
   
    def tentes_regles(self):
        showinfo('Règles de Tentes', 'Règles de Tentes :' + '\n' + '\n' + '- Mode de jeu : Solo' + '\n' + ' - La règle est très simple : sur une grille (de plus en plus grande en grimpant les niveaux), vous devez placer une tente près de chaque arbre. Les numéros autour de la grille indiquent quant à eux le nombre de tentes à positionnez sur chaque ligne ou colonne. Attention, les tentes ne doivent pas se toucher !')
   
    def isola_regles(self):
        showinfo('Règles de Isola', 'Règles de Isola :' + '\n' + '\n' + '- Mode de jeu : Duo' + '\n' + ' - À chaque tour, chaque joueur :' + '\n' + ' - Déplace son pion vers une case libre adjacente ou touchant la case ! de départ par un coin (comme un roi aux échecs) et' + '\n' + '- Détruit ensuite une case du jeu non occupée pour le reste de la partie ! (dans la version commercialisée, on appuyait avec le doigt sur la case qui se déboitait alors du tablier).')

    def puissance_regles(self):
        showinfo('Règles du Puissance 4', 'Règles du Puissance 4 :' + '\n' + '\n' + 'Le but du jeu est d aligner une suite de 4 pions de même couleur sur une grille comptant 6 rangées et 7 colonnes. Chaque joueur dispose de 21 pions d une couleur (par convention, en général jaune ou rouge). Tour à tour, les deux joueurs placent un pion dans la colonne de leur choix, le pion coulisse alors jusqu à la position la plus basse possible dans la dite colonne à la suite de quoi c est à l adversaire de jouer. Le vainqueur est le joueur qui réalise le premier un alignement (horizontal, vertical ou diagonal) consécutif d au moins quatre pions de sa couleur. Si, alors que toutes les cases de la grille de jeu sont remplies, aucun des deux joueurs n a réalisé un tel alignement, la partie est déclarée nulle.')
    
    def sutom_regles(self):
        showinfo('Règles de Sutom', 'Règles de Sutom :' + '\n' + '\n' + 'Il n’y a rien de compliqué dans le SUTOM, l’objectif est simple : trouver un mot ! Le mot à trouver contient entre 6 et 9 lettres. Cela ne peut pas être un nom propre, mais les pluriels et verbes conjugués sont acceptés. Il faut obligatoirement un mot qui existe : vous ne pouvez pas proposer une suite hasardeuse de lettres. Vous n’avez pas à vous préoccuper des accents. Comme pour le célèbre jeu Mastermind, vous avez le droit à plusieurs tentatives pour trouver la solution. Pour être plus précis, vous disposez de 6 essais, représentés par 6 lignes différentes. Afin de limiter le champ des possibles, la première lettre est toujours indiquée. Elle doit restée identique à chaque tentative.À mesure des essais, lorsque vous trouvez la bonne position d’une lettre, elle apparait dans un carré rouge. Si la lettre est présente dans le mot final, mais mal placée, elle apparait dans un cercle jaune. À l’inverse, une lettre absente de la solution reste en bleu.')
# FIN fonctions qui affichent une popup du réglement
    def __init__(self):
        """
        Élément princpal de la fenêtre Welcome
        Sert de "HUB"
        """
        self.fenetre_principale=Tk()#On fonde l'élément#On fonde l'élément de la fenêtre
        self.fenetre_principale.geometry("800x600")#on définit la taille de la fenêtre
        img= Image.open('./img/image.png')
        img= ImageTk.PhotoImage(img)
        self.fenetre_principale.iconphoto(True,img)
        Fond1=Canvas(self.fenetre_principale,width=10000,height=10000,bg=global_color[0],bd=0,borderwidth = 0, highlightthickness = 0)#on crée le fond de la fenêtre
        Fond1.pack(fill="both")#on place le Canvas
        Fond2=Canvas(self.fenetre_principale,width=800,height=600,bg=global_color[1],bd=0,borderwidth = 0, highlightthickness = 0)#on crée le fond de la liste des jeux
        Fond2.place(anchor=CENTER, relx=0.5, rely=0.5,relwidth=0.8, relheight=0.5)#on place le Canvas

        imglabel= Image.open("./img/menu/t_logo1.jpg")
        imglabel= ImageTk.PhotoImage(imglabel)
        
        label = Label(self.fenetre_principale,image=imglabel,bg ="#2A9D8F") #text="Application jeu", fg="white", bg ="#2A9D8F", font=("System",25))#on définit la grande ligne de texte
        
        label.place(anchor=CENTER, rely=0.2, relx=0.5)#on place le label

        #on définit l'image
        img = Image.open("./img/menu/isola.png")
        mon_image = ImageTk.PhotoImage(img)  
        label = Label(image=mon_image)
        label.image=mon_image
   
        #on place la case Isola
        jeu_isola=Button(Fond2, image = mon_image, command=lambda :AppMenu("Isola",Isola,self.isola_regles,"Bloquez, ou soyez bloqué"),bg=global_color[2],overrelief='flat')
        jeu_isola.place(relwidth=0.2, relheight=0.4, relx=0, rely=0.2, anchor=NW)#side=LEFT,relwidth=0.1)
        texte1 = Label(jeu_isola, text="Isola", font="System", bg="white")
        texte1.place(x=0, y=0)

        #on définit l'image
        img = Image.open("./img/menu/puissance.png")
        mon_image = ImageTk.PhotoImage(img)        
        label = Label(image=mon_image)
        label.image=mon_image

        #on place la case Puissance4
        jeu_puissance=Button(Fond2, image = mon_image, command=lambda : AppMenu("Puissance4",Puissance4,self.puissance_regles,"À vos pièces"),overrelief='flat',bg="#002AE0",activebackground="#002AE0")#,border_color="F4A261")
        jeu_puissance.place(relwidth=0.2, relheight=0.4, relx=0.2, rely=0.2, anchor=NW)

        texte2 = Label(jeu_puissance, text="Puissance 4", font="System", bg="white")
        texte2.place(x=0, y=0)
        
        #on définit l'image
        img= Image.open("./img/menu/quarto.png")
        img1= ImageTk.PhotoImage(img)
        #on place la case quarto
        jeu_quarto=Button(Fond2,image=img1 , command=lambda :AppMenu("Quarto",Quarto,self.quarto_regles,"Quatre pièces, quatre"),overrelief='flat',bg="#f7d0c6",activebackground="#f7d0c6")
        jeu_quarto.place(relwidth=0.2, relheight=0.4, relx=0.40, rely=0.2, anchor=NW)
        texte3 = Label(jeu_quarto, text="Quarto", font="System", bg="white")
        texte3.place(x=0, y=0)

        #on définit l'image
        img= Image.open("./img/menu/nerdle.png")
        img2= ImageTk.PhotoImage(img)
        #on place la case nerdle
        jeu_nerdle=Button(Fond2, image=img2, command=lambda :AppMenu("Nerdle",Nerdle,self.nerdle_regles,"Comptez bien"), overrelief='flat',bg="#84DEEA",activebackground="#84DEEA")
        jeu_nerdle.place(relwidth=0.2, relheight=0.4, relx=0.60, rely=0.2, anchor=NW)
        texte4 = Label(jeu_nerdle, text="Nerdle", font="System", bg="white")
        texte4.place(x=0, y=0)

        #on définit l'image
        img= Image.open("./img/menu/mastermind.png")
        img3= ImageTk.PhotoImage(img)
        #on place la case mastermind
        jeu_mastermind=Button(Fond2, image=img3, command=lambda : AppMenu("Mastermind",Mastermind,self.mastermind_regles,"Le maître des cerveaux"),bg="#ff7045",activebackground="#ff7045")
        jeu_mastermind.place(relwidth=0.2, relheight=0.4, relx=0.80, rely=0.2, anchor=NW)
        texte5 = Label(jeu_mastermind, text="Mastermind", font="System", bg="white")
        texte5.place(x=0, y=0)

        #on définit l'image
        img= Image.open("./img/menu/sutom.jpg")
        img5= ImageTk.PhotoImage(img)
        #on place la case sutom
        jeu_sutom=Button(Fond2, image=img5, command=lambda : AppMenu("Sutom",Sutom,self.sutom_regles))
        jeu_sutom.place(relwidth=0.20, relheight=0.4, relx=0, rely=0.6, anchor=NW)
        texte6 = Label(jeu_sutom, text="Sutom", font="System", bg="white")
        texte6.place(x=0, y=0)

        #on définit l'image
        img= Image.open("./img/menu/battleship.png")
        img6= ImageTk.PhotoImage(img)
        #on place la case navale
        jeu_navale=Button(Fond2, image=img6, command=lambda : AppMenu("Bataille Navale",Navale,self.bataille_navale_regles,"Placez vos navires"),bg="#FFB52D",activebackground="#FFB52D")
        jeu_navale.place(relwidth=0.20, relheight=0.4, relx=0.20, rely=0.6, anchor=NW)
        texte7 = Label(jeu_navale, text="Bataille\nNavale", font="System", bg="white")
        texte7.place(x=0, y=0)

        #on définit l'image
        img= Image.open("./img/menu/rush.png")
        img7= ImageTk.PhotoImage(img)
        #on place la case rush
        jeu_rush=Button(Fond2, image=img7, command=lambda : AppMenu("Rush Hour",Rush,self.rush_hour_regles,"Heure de pointe"),bg="#C1C5D1",activebackground="#C1C5D1")
        jeu_rush.place(relwidth=0.20, relheight=0.4, relx=0.40, rely=0.6, anchor=NW)
        texte71 = Label(jeu_rush, text="Rush Hour", font="System", bg="white")
        texte71.place(x=0, y=0)

        #on définit l'image
        img= Image.open("./img/menu/gratte-ciel.png")
        img8= ImageTk.PhotoImage(img)
        #on place la case gratte
        jeu_gratte=Button(Fond2, image=img8, command=lambda : AppMenu("Gratte-ciel",Gratte_ciel,self.grattes_ciel_regles),bg="#a4c3b2",activebackground="#a4c3b2")
        jeu_gratte.place(relwidth=0.2, relheight=0.4, relx=0.60, rely=0.6, anchor=NW)
        texte8 = Label(jeu_gratte, text="Gratte-Ciel", font="System", bg="white")
        texte8.place(x=0, y=0)

        #on définit l'image
        img= Image.open("./img/menu/tente.png")
        img9= ImageTk.PhotoImage(img)
        #on place la case tentes
        jeu_tentes=Button(Fond2, image=img9, command=lambda : AppMenu("Tentes",Tentes,self.tentes_regles),bg="#024C67",activebackground="#024C67")
        jeu_tentes.place(relwidth=0.2, relheight=0.4, relx=0.80, rely=0.6, anchor=NW)
        texte9 = Label(jeu_tentes, text="Tentes", font="System", bg="orange")
        texte9.place(x=0, y=0)

#Barre de menu

        menubar = Menu(self.fenetre_principale,bg=global_color[4],fg="white",bd=0)

        menu1 = Menu(menubar, tearoff=0,bg=global_color[4],fg=black_or_white(global_color[4]))
        menu1.add_checkbutton(label="Mode daltonien",command=Param.daltonien)
        menu1.add_command(label="Changer couleurs", command=Param.color_choice)
        menu1.add_command(label="Quitter", command=self.fenetre_principale.destroy)
        menubar.add_cascade(label="Paramètre", menu=menu1)

        menu3 = Menu(menubar, tearoff=0 ,bg=global_color[4],fg=black_or_white(global_color[4]))
        menubar.add_cascade(label="Jeu", menu=menu3)
        menu_recent = Menu(menu3, tearoff=0,bg=global_color[4],fg="white",bd=0)
        menu_recent.add_command(label="Quarto", command=self.quarto_regles)
        menu_recent.add_command(label="Rush Hour", command=self.rush_hour_regles)
        menu_recent.add_command(label="Gratte-Ciel", command=self.grattes_ciel_regles)
        menu_recent.add_command(label="Sutom", command=self.sutom_regles)
        menu_recent.add_command(label="Isola", command=self.isola_regles)
        menu_recent.add_command(label="Nerdle", command=self.nerdle_regles)
        menu_recent.add_command(label="Mastermind", command=self.mastermind_regles)
        menu_recent.add_command(label="Puissance 4", command=self.puissance_regles)
        menu_recent.add_command(label="Bataille navale", command=self.bataille_navale_regles)
        menu_recent.add_command(label="Tentes", command=self.tentes_regles)
        menu_recent.add_command(label="You know the rules",command=rickroll)
        menu3.add_cascade(label="Règles", underline=0, menu=menu_recent)

        menu4 = Menu(menubar, tearoff=0,bg=global_color[4],fg="white",bd=0)
        menu4.add_command(label="A propos", command=self.propos)
        menu4.add_command(label="Contact", command=self.contact)
        menubar.add_cascade(label="Aide", menu=menu4)

        self.fenetre_principale.config(menu=menubar)  
        label_text = Label(self.fenetre_principale, text="Cliquer sur une icone pour commencer !", font="System", bg=global_color[1])
        label_text.place(rely=0.3, relx=0.5, anchor=CENTER)
        self.fenetre_principale.title("Bibliothèque de jeux")
        self.fenetre_principale.mainloop()#on lance la fenêtre
#FIN MENU
#menu par app
class AppMenu:
    """
    Menu d'une application
    """
    def __init__(self,appname:str,fonction,rule,phrase:str=None):
        """
        appname : le nom d'application
        fonction : la fonction pour lancer le jeu
        rule : emplacement des règles du jeu
        phrase : le slogan du jeu
        """
        main= Toplevel()#On fonde l'élément#On fonde l'élément de la fenêtre
        main.geometry("240x260")#on définit la taille de la fenêtre
        main.title(appname)#on définit le titre
        main.config(bg=global_color[0])
        menubar = Menu(main,bg=global_color[4],fg="white",bd=0)
        menubar.add_command(label="Règles",command=rule)
        label = Label(main, text=appname, fg="white", bg =global_color[0], font=("System",25))
        label.place(anchor=CENTER, rely=0.2, relx=0.5)
        label1 = Label(main, text=phrase, fg="white", bg =global_color[0], font=("System",12))
        label1.place(anchor=CENTER, rely=0.4, relx=0.5)
        play=Button(main,text="Jouer", command=fonction,bg=global_color[3],fg=black_or_white(global_color[3]),bd=0)
        play.place(anchor=CENTER, rely=0.6, relx=0.5)
        main.config(menu=menubar)  

#Isola
class Isola:
    def __init__(self):
        """
        Isola, un jeu où l'on bloque
        """
        self.main = Toplevel()#On fonde l'élément
        self.main.geometry("200x240")#on définit la taille
        self.main.title("Isola - Bloquez, ou soyez bloqué")#on définit le titre
        self.label= Label(self.main,text="Où allons nous ?")#on définit le texte
        self.label.pack(anchor=CENTER, fill="both")#on place le texte
        self.grille=Grille(7,7,self.action,self.main)#on crée une grille
        self.p2_tour=0#alternance des tours
        self.bouger=1#le joueur bouge ou détruit
        self.main.configure(bg="#d9d9d9")#on définit la couleur de fond
        self.co=[[3,0],[3,6]]#on définit les coordonées des joueurs
        if Save.load("color")==None:
            self.color=("#6b0505","#04195d","#474038","#d9d9d9")
        else:self.color=Save.load("color")
        #on charge nos deux joueurs
        for i in range(2):#pour i dans 2
            self.grille.setColor(self.co[i][0],self.co[i][1],self.color[i])#on place la couleur
        self.label["bg"]=self.color[self.p2_tour]#on change la couleur du label
        self.label["fg"]=black_or_white(self.color[self.p2_tour])#on change la couleur font du label

        self.main.mainloop()#on lance la fenêtre
    def clear(self):
        """
        Reset le jeu
        """
        for y in range(7):#pour y dans 7
            for x in range(7):#pour x dans 7
                self.grille.setColor(x,y,self.color[3])#on place la couleur
        self.p2_tour=0
        self.bouger=1
        self.co=[[3,0],[3,6]]
        #on charge nos deux joueurs
        for i in range(2):#pour i dans 2
            self.grille.setColor(self.co[i][0],self.co[i][1],self.color[i])#on place la couleur
    def changer_texte(self,txt,color="#d9d9d9"):
        """
        Sert à changer le label
        """
        self.label["text"]=str(txt)#on change le texte du label
        self.label["bg"]=color#on change la couleur du label
        #recherche de la couleur opposées pour le colorfont
        
        self.label["fg"]=black_or_white(color)#on change la couleur font du label
    def perdu(self):
        """
        compte les cases proche qui sont colorées et renvoye True si ce nombre dépasse 8
        """
        #on définit les constantes pour cette fonction
        a=0
        x=self.co[self.p2_tour][0]
        y=self.co[self.p2_tour][1]
        #pour chaque coordonée adjacente
        for cx in range(x-1,x+2):
            for cy in range(y-1,y+2):
                if cx<0 or cy<0 or cx>6 or cy>6:#si on dépasse de la grille
                    a+=1#incrémenter a
                else:#sinon
                    if self.grille.getColor(cx,cy)!=self.color[3]:#si la couleur est différente de self.color[3]
                        a+=1#incrémenter a
        return a>8#renvoie le résultat de ce test
    def proche(self,a,b):
        """
        Renvoye True si la case a est proche de b
        """
        return a[0] >= b[0]-1 and a[0] <= b[0]+1 and a[1] >= b[1]-1 and a[1] <= b[1]+1 and not (a[0] == b[0] and a[1] == b[1])#renvoie True si la case a est proche de b
    def action(self,co):
        #on s'assure que le joueur existe
        if self.bouger:#si le joueur bouge
            self.changer_texte("Où aller ? - "+str(self.p2_tour+1),self.color[self.p2_tour])#on change le texte du label
            if self.proche(self.co[self.p2_tour],co) and self.grille.getColor(*co)==self.color[3]:#si la case est proche et vide
                 self.grille.setColor(co[0],co[1],self.color[self.p2_tour])#on change la couleur
                 self.grille.setColor(self.co[self.p2_tour][0],self.co[self.p2_tour][1],self.color[3])#on change la couleur
                 self.co[self.p2_tour]=co#on actualise les coordonées
                 self.bouger=1-self.bouger#inverser self.bouger
                 self.changer_texte("Quelle case supprimer ?",self.color[self.p2_tour])#on change le texte
            else:self.changer_texte("Déplacement Impossible",self.color[self.p2_tour])#sinon on change le texte
        else:#si suppression
            if self.grille.getColor(*co)==self.color[3]:#si la couleur est égale à self.color[3]
                self.grille.setColor(co[0],co[1],self.color[2])#on change la couleur
                self.p2_tour=1-self.p2_tour#inverser self.p2_tour
                self.bouger=1-self.bouger#inverser self.bouger
                self.changer_texte("Déplace-toi",self.color[self.p2_tour])#on change le texte
        if self.perdu():#si le joueur a perdu
            if askyesno("🎉 Nous avons un vainqueur 🎉","Joueur "+str(self.p2_tour)+" est vainqueur\nSouhaitez-vous rejouer ?",master=self.main, parent=self.main):#demander si le joueur souhaite rejouer
                self.clear()#on reset le terrain de jeu
            else:#sinon
                self.main.destroy()#explosion de la fenêtre
#Rush
class Rush:
    def __init__(self):
        self.main= Toplevel()#on fonde l'élément
        self.main.geometry("210x190")#on définit la taille
        self.main.title("Rush Hour - Heure de pointe")#on définit le titre
        fr=Frame(self.main)
        self.grille=Grille(6,6,self.action,fr)#on crée une grille
        fr.pack(side=LEFT, fill="both",expand=True)
        fr1=Frame(self.main,bg="#222224")
        for i in ["","","➤","","",""]:
            Button(fr1,command=lambda :self.verif_win(1),border=0,overrelief='flat',text=i,bg="#222224",activebackground="#222224",highlightthickness=0,highlightbackground="#222224",highlightcolor="#222224",fg=black_or_white("#222224")).pack(side=TOP,fill="both",expand=True)
        fr1.pack(side=RIGHT, fill="both",expand=True)
        #chargement des couleurs UI
        if Save.load("color")==None:#si les couleurs n'existe pas dans la sauvegarde
            self.color=("#6b0505","#04195d","#474038","#d9d9d9")#on définit la variable couleur
        else:self.color=Save.load("color")#sinon on charge la sauvegarde
        self.select_color=self.color[3]
        self.difficultes=[60,20]
        self.directwin=0#booléen (victoire rapide True ou lente False)
        self.posvoiture=self.gen()#on génère les voitures
        for y in range(6):
            for x in range(6):
                self.grille.setColor(x,y,self.posvoiture[y][x] if self.posvoiture[y][x]!="" else self.color[3])
        
        menubar = Menu(self.main,bg=global_color[4],fg="white",bd=0)
        listeDiff=("Facile","Normal","Expert"),([20,0],[40,20],[60,40])
        menu1 = Menu(menubar, tearoff=0,bg=global_color[4],fg=black_or_white(global_color[4]))
        for i in range(3):
            menu1.add_command(label=listeDiff[0][i],command=lambda x=listeDiff[1][i]:self.changerDiff(x))
        menubar.add_cascade(label="Difficulté", menu=menu1)
        menubar.add_command(label="Regénérer", command=self.clear)
        menubar.add_checkbutton(label="↠",command=self.dWin)
        self.main.config(menu=menubar)

    def changerDiff(self,d):
        self.difficultes=d
    def dWin(self):
        self.directwin=1-self.directwin

    def gen(self):
        """
        Génère un niveau
        """
        color=["#ff0000","#0000ff","#00ff00","#00ffff","#ffff00","#055f5f","#123465","#ff8844","#990990","#ddaadd","#4848dd","#564544","#874655","#878a54","#5454aa","#aa5400"]
        level_path="rush.level"#le nom du fichier de niveaux
        #la base de données par défaut est trouvable sur le site https://www.michaelfogleman.com/rush/#DatabaseDownload
        pos_voiture=[["","","","","","",""],["","","","","","",""],["","","","","","",""],["","","","","","",""],["","","","","","",""],["","","","","","",""]]
        if os.path.exists(level_path):#si le fichier n'existe pas
            with open(level_path,"r") as f:#ouvrir fichier level
                a=f.readlines()#on met tous en format liste
                element=randint(0,len(a))
                b=a[element]#on sélectionne un élément aléatoire
                b=b.split()
                c=[0,len(a)]
                while not self.difficultes[0]>int(b[0])>self.difficultes[1]:
                    element=randint(c[0],c[1])
                    b=a[element]
                    b=b.split()
                    if self.difficultes[1]>int(b[0]):
                        c[1]=element
                    if self.difficultes[0]<int(b[0]):
                        c[0]=element
                a=b[1]#on prend la chaine
                print(a)
                try:#tenter
                    for i in range(36):#pour i dans 36
                        pos_voiture[i//6][i%6]= color[ord(a[i])-65] if a[i] not in ("o","x") else "#000000" if a[i]=="x" else ""#élément vaut color si i n'est pas dans ox, noir si x, et """ si rien
                except:#en cas d'erreur, on retente
                    a=f.readlines()#on met tous en format liste
                    a=a[randint(0,len(a))]#on sélectionne un élément aléatoire
                    a=a.split()[1]#on prend la chaine
                    for i in range(36):#pour i dans 36
                        pos_voiture[i//6][i%6]= color[ord(a[i])-65] if a[i] not in ("o","x") else "#000000" if a[i]=="x" else ""#élément vaut color si i n'est pas dans ox, noir si x, et """ si rien
        else:#sinon, si le fichier niveau n'existe pas
            showinfo("Niveaux","Aucun niveau détécté, chargement du niveau par défaut",master=self.main, parent=self.main)#on affiche une popup
            pos_voiture=[["#00ff00","#00ff00","","","","#00ffff"],["#ffff00","","","#0000ff","","#00ffff"],["#ffff00","#ff0000","#ff0000","#0000ff","","#00ffff"],["#ffff00","","","#0000ff","",""],["#99582A","","","","#432818","#432818"],["#99582A","","#BB9457","#BB9457","#BB9457",""]]
        return pos_voiture
    def action(self,co):#action pour mouvement
        if self.grille.getColor(co[0],co[1])!=self.color[3]:#si la couleur de la case est différent de xself.color[3]
            self.select_color=self.grille.getColor(co[0],co[1])#on change la couleur sélectionnée
            print(co)
        else:
            #on bouge la voiture en x
            if self.grille.getColor(co[0],co[1])!=self.color[3]:return None#on évite aux couleurs de se superposer
            for i in range(6):#pour i dans 6
                a=self.indexall(self.posvoiture[i],self.select_color)#on récupére chaque index de select_color
                if co[1]==i and len(a)>=2 and a[0]<a[1]:#on parcours y jusqu'à la ligne
                    j=a[0]
                    if co[0]>j:#si co[0] est supérieur à j
                        if all(j in [self.color[3],self.select_color,""] for j in self.posvoiture[co[1]][a[0]:co[0]]):#si  il n'y a aucune case génante pour se déplacer
                            for j in a:#pour i dans a
                                self.retirer(j,co[1])#on retire la case du plateau
                            for j in a:#pour i dans a
                                self.placerx(j,co[1],co[0]-a.index(j)-j)#on place sur le plateau à la nouvelle position
                    else:
                        if all(j in [self.color[3],self.select_color,""] for j in self.posvoiture[co[1]][a[-1]:co[0]:-1]):#si  il n'y a aucune case génante pour se déplacer
                            for j in a:#pour i dans a 
                                self.retirer(j,co[1])#on retire la case du plateau
                            for j in a:#pour i dans a
                                self.placerx(j,co[1],co[0]+a.index(j)-j)#on place sur le plateau à la nouvelle position
            #on bouge la voiture en y
            for i in range(6):#pour i dans 6
                liste_voiture_x=[]
                for y in range(6):#pour y dans 6
                    liste_voiture_x.append(self.posvoiture[y][i])#on ajoute à liste_voiture_x
                a=self.indexall(liste_voiture_x,self.select_color)#on récupére chaque index de select_color
                if co[0]==i and len(a)>=2 and a[0]<a[1]:#on parcours y jusqu'à la ligne
                    j=a[0]
                    print(a)
                    if co[1]>j:#si co[1] est supérieur à j
                        if all(j in [self.color[3],self.select_color,""] for j in liste_voiture_x[a[0]:co[1]-1]):#si il n'y a aucune case génante
                            for j in a:#pour i dans a
                                self.retirer(co[0],j)#on retire la case du plateau
                            for j in a:#pour i dans a
                                self.placery(co[0],j,co[1]-a.index(j)-j)#on place sur le plateau à la nouvelle position
                                
                    else:#sinon
                        if all(j in [self.color[3],self.select_color,""] for j in liste_voiture_x[a[0]:co[1]:-1]):#si  il n'y a aucune case génante
                            for j in a:#pour i dans a
                                self.retirer(co[0],j)#on retire la case du plateau
                            for j in a:#pour i dans a 
                                self.placery(co[0],j,co[1]+a.index(j)-j)#on place sur le plateau à la nouvelle position
            self.select_color=self.color[3]
            if self.verif_win():#si win
                if askyesno("🎉 Nous avons un vainqueur 🎉","Bravo, vous avez réussi à vous échapper de ce parking\nSouhaitez vous rejouer ?",master=self.main, parent=self.main):#demander si le joueur souhaite rejouer
                    self.clear()#on reset le terrain
                else:#sinon
                    self.main.destroy()#explosion de la fenêtre
    def retirer(self,x,y):
        """
        Cette fonction va faire disparaitre par magie la case du plateau
        """
        self.posvoiture[y][x]=""#on change la couleur dans la liste
        self.grille.setColor(x,y,self.color[3])#on change la couleur
    def placery(self,x,y,c):
        """
        Réaparition de la case
        """
        color=self.select_color
        self.posvoiture[y+c][x]=color#on change la couleur dans la liste
        self.grille.setColor(x,y+c,color)#on change la couleur
    def placerx(self,x,y,c):
        """
        Réaparition de la case
        """
        color=self.select_color
        self.posvoiture[y][x+c]=color#on change la couleur dans la liste
        self.grille.setColor(x+c,y,color)#on change la couleur
    def verif_win(self,t=0):
        """
        Renvoie True si la voiture rouge peut sortir, sinon, renvoie False
        """
        if self.directwin or t:
            a=self.indexall(self.posvoiture[2],"#ff0000")#indexation de chaque "#ff0000"
            print(a,self.posvoiture[2][a[1]::])#print de debug
            for i in self.posvoiture[2][a[1]::]:#pour i dans la liste
                if i not in (self.color[3],"#ff0000",""):#si i n'est pas dans (color,"#ff0000","")
                    return False
        else:
            return self.indexall(self.posvoiture[2],"#ff0000")==(4,5)
        if t:
            if askyesno("🎉 Nous avons un vainqueur 🎉","Bravo, vous avez réussi à vous échapper de ce parking\nSouhaitez vous rejouer ?",master=self.main, parent=self.main):#demander si le joueur souhaite rejouer
                self.clear()#on reset le terrain
            else:#sinon
                self.main.destroy()#explosion de la fenêtre
        return True
        

    def indexall(self,a,b):
        """
        Renvoie la liste de chaque position de l'element b dans a
        """
        c=[]
        for i in range(len(a)):#pour i dans longueur a
            if a[i] == b:#si élément vaut b
                c.append(i)#on ajoute i à la liste c
        return c
    def clear(self):
        """
        Prépare la grille pour une nouvelle partie
        """
        #on définit les constantes
        self.select_color=self.color[3]
        self.posvoiture=self.gen()#on génère les voitures
        for y in range(6):#pour y dans 6
            for x in range(6):#pour x dans 6
                self.grille.setColor(x,y,self.color[3])#on place la couleur 
                self.grille.setColor(x,y,self.posvoiture[y][x] if self.posvoiture[y][x]!="" else self.color[3])#on place la couleur


#Sutom INIT
for u in range(len(ListeMots) - 1, 0, -1):
    if 9+1 < len(ListeMots[u]) or 6+1 > len(ListeMots[u]) or ListeMots[u].istitle():
        ListeMots.remove(ListeMots[u])
ListeMots.remove(ListeMots[8054])
ListeMots.remove(ListeMots[8053])

IndicMot = randint(0, len(ListeMots))
MotChercher = ListeMots[IndicMot]#on retire les espaces
print(MotChercher)
ListeChercher = [x for x in MotChercher]
ListeChercher.remove("\n")#on retire le passage à la ligne
xlongmot = len(ListeChercher)


class Sutom:

    def __init__(self):
        self.main = Tk()
        """
        w, h = self.main.winfo_screenwidth(), self.main.winfo_screenheight()
        self.main.geometry("%dx%d" % (w, h))
        """
        self.main.configure(background="#DDDDDD", borderwidth=5)
        # On ajoute un titre à la fenêtre
        self.main.title("Sutom")
        label1 = Label(self.main, text="Tapez un mot")
        label1.pack()
        regle = Label(self.main,background="#DEE550",text="Règles de Sutom :\n\nIl n’y a rien de compliqué dans le SUTOM, l’objectif est simple : trouver un mot !\n Le mot à trouver contient entre 6 et 9 lettres.\n Cela ne peut pas être un nom propre, mais les pluriels et verbes conjugués sont acceptés.\n Il faut obligatoirement un mot qui existe : vous ne pouvez pas proposer une suite hasardeuse de lettres.\n  Comme pour le célèbre jeu Mastermind, vous avez le droit à plusieurs tentatives pour trouver la solution.\n Pour être plus précis, vous disposez de 6 essais, représentés par 6 lignes différentes.\n À mesure des essais, lorsque vous trouvez la bonne position d’une lettre, elle apparait dans un carré rouge.\n Si la lettre est présente dans le mot final, mais mal placée, elle apparait dans un carré jaune.\n À l’inverse, une lettre absente de la solution reste en bleu.\n")

        self.grille = Grille(xlongmot, 6, print, self.main)
        for x in range(xlongmot):
            for y in range(6):
                self.grille.setColor(x, y, "#3f6ef9")
        self.strvar = StringVar(master=self.main)
        c = Frame(self.main)
        self.input = Entry(c, textvariable=self.strvar)
        self.input.pack(side=LEFT, fill="both", expand=True)
        c.pack(fill="both")
        self.strvar.trace("w", lambda *args: self.character_limit(self.strvar))
        self.submit = Button(c, command=self.envoi, text="Entrée")
        self.submit.pack(side=RIGHT, fill="both", expand=True)
        self.NbEssais = 0

        regle.pack()
        self.main.bind('<Return>', self.envoi_enter)#en cas de [Entrer] executer self.envoi_enter

        self.main.mainloop()
    def clear(self):
        global IndicMot
        global MotChercher
        global ListeChercher
        global xlongmot
        IndicMot = randint(0, len(ListeMots))
        MotChercher = ListeMots[IndicMot]
        ListeChercher = [x for x in MotChercher]
        xlongmot = len(ListeChercher)
        self.main.destroy()
        Sutom()

    def envoi_enter(self,event):
        self.envoi()
    def envoi(self):
        MotTapée = self.strvar.get()
        ListeTapée = [elt for elt in MotTapée]
        if len(MotTapée) <= xlongmot-1:
            return showerror("Erreur", "Le mot rentrée doit contenir plus de caractères.",parent=self.main)
        if self.NbEssais == 6:
            if askyesno("Fin de jeu","Vous avez perdu!\n Souhaiter vous rejouer? Le mot était : "+str(MotChercher),parent=self.main):
                return self.clear()
            else:
                self.main.destroy()
        for x in range(xlongmot):
            self.grille.setText(x, self.NbEssais, ListeTapée[x])
        self.verification(MotTapée,self.NbEssais)
        self.NbEssais += 1

    def character_limit(self, txt):
        """
        Cette fonction permet de s'assurer que le texte ne contienne pas trop de caractères, ou des charactères interdits.
        """
        try:
            if len(txt.get()) > xlongmot:
                txt.set(txt.get()[:-1])
        except Exception as e:
            print("erreur non fatale - " + str(e))
    def verification(self,mot,NbTry):
        ListeMot=[elt for elt in mot]
        ListeSpécial=list(set(ListeMot))
        Enregistremment=[]
        for i in range(len(ListeMot)):
            for x in range(len(ListeChercher)):
                if ListeMot[i] == ListeChercher[x]:
                        self.grille.setColor(i, NbTry, "#FCFC3E")
                        if i == x:
                            Enregistremment.append(i)
        for e in Enregistremment:
            self.grille.setColor(e, NbTry, "#FF522D")



        for a in range(len(ListeMot)):
            self.grille.setText(a, NbTry, ListeMot[a])
        if mot==MotChercher[0:-1]:#si mot est dans motchercher (on retire le dernier caractères)
            if askyesno("Fin de jeu","Bien joué vous avez trouvé le mot mystère\nRejouer ?",parent=self.main):
                self.clear()
            else:
                self.main.destroy()

#Tentes
class Tentes :
    def __init__(self):
        self.main = Tk()
        self.main.title("Tentes")
        self.grille=Grille(7,7,self.action,self.main)
        self.grille_calc=Grille(7,7,self.action,self.main,mode_fast=1)
        for i in range(49):
            self.grille_calc.setText(i,0,"")
       
        self.listex=[""]
        self.listey=[""]
       
        a=randint(7,15)
        #Boucle pour placer les arbres et les tentes
        for i in range(a):
            x=randint(1, 6)
            y=randint(1, 6)
            if x>1 and y>1:
                tente_plus_x=randint(-1,1) if x<6 else randint(-1,0)
                tente_plus_y=randint(-1,1) if y<6 else randint(-1,0)
            else:
                tente_plus_x=randint(0,1) if x<6 else 0
                tente_plus_y=randint(0,1) if y<6 else 0

            print(x,y,tente_plus_x,tente_plus_y) 

            self.grille_calc.setText(x,y,"🌳")
            anti_bug=0
            b=[self.grille_calc.getText(x+tente_plus_x-1,y+tente_plus_y-1),self.grille_calc.getText(x+tente_plus_x-1,y+tente_plus_y),self.grille_calc.getText(x+tente_plus_x,y+tente_plus_y-1)]
            while 1:
                anti_bug+=1
                print(x,y,tente_plus_x,tente_plus_y)
                if y+tente_plus_y+1<7:
                    b+=[self.grille_calc.getText(x+tente_plus_x,y+tente_plus_y),"Jujh" if y+tente_plus_y+1<7 or x+tente_plus_x+1<7 else self.grille_calc.getText(x+tente_plus_x+1,y+tente_plus_y+1),self.grille_calc.getText(x+tente_plus_x+1,y+tente_plus_y) if x+tente_plus_x+1<7 else "JUH","GTF" if y+tente_plus_y+1<7 else self.grille_calc.getText(x+tente_plus_x,y+tente_plus_y+1)]
                if anti_bug>999:
                    self.grille_calc.setText(x,y,"");break
                if "⛺" not in b and tente_plus_x+x<7:
                    #si toutes les cases autour de l'emplacement choisit  sont vide
                    self.grille_calc.setText(x+tente_plus_x,y+tente_plus_y,"⛺");break
                else:
                    if x>1 and y>1:
                        tente_plus_x=randint(-1,1) if x<6 else randint(-1,0)
                        tente_plus_y=randint(-1,1) if y<6 else randint(-1,0)
                    else:
                        tente_plus_x=randint(0,1) if x<6 else 0
                        tente_plus_y=randint(0,1) if y<6 else 0
        #Boucle pour placer les Tentes  
        #for i in range(a):
        #    x=randint(1, 6)
        #    y=randint(1, 6)
            
           
        #    if self.grille.getText(x,y)!="🌳" and self.grille.getText(x-1,y-1)!="⛺" and self.grille.getText(x,y-1)!="⛺" and self.grille.getText(x-1,y)!="⛺" :
        #        self.grille.setText(x,y,"⛺")
       
        #Boucle pour compter le nombre de tente en y
        for y in range(7):
            compte=0
            for x in range(7):
                if self.grille_calc.getText(x,y) == "⛺":
                    compte=compte+1
           
            self.listey.append(str(compte))
           
       #Boucle pour compter le nombre de tente en x
        for x in range(7):
            compte1=0
            for y in range(7):
                if self.grille_calc.getText(x,y) == "⛺":
                    compte1=compte1+1
                     
            self.listex.append(str(compte1))
           
        #Boucle pour le nombre de tente par ligne/colonne
        print(self.grille_calc.listebutton)
        for y in range(7):
            for x in range(7):
                if x==0:  
                    self.grille.setText(x,y,self.listey[y])
               
                if y==0:
                    self.grille.setText(x,y,self.listex[x])
        for i in range(49):
            if self.grille_calc.getText(i,0)=="🌳":
                self.grille.setText(i,0,"🌳")
                   
        self.main.mainloop()
       
    def action(self,buton):
        if self.grille.getText(buton[0],buton[1]) not in  ("🌳","⛺"):
            self.grille.setText(buton[0],buton[1],"⛺")
        elif self.grille.getText(buton[0],buton[1])=="⛺":
            self.grille.setText(buton[0],buton[1],"")
        self.verifier()

    def verifier(self):
        #Boucle pour compter le nombre de tente en y
        for y in range(7):
            compte=0
            for x in range(7):
                if self.grille_calc.getText(x,y) == "⛺":
                    compte=compte+1
           
            listey.append(str(compte))
           
        #Boucle pour compter le nombre de tente en x
        for x in range(7):
            compte1=0
            for y in range(7):
                if self.grille_calc.getText(x,y) == "⛺":
                    compte1=compte1+1
                     
            listex.append(str(compte1))
        if listex==self.listex and listey==self.listey:
            showinfo("bravo","vous avez gagné")

#Bataille navale
class Navale:
    def __init__(self):
        self.main = Toplevel()#On fonde l'élément
        self.main.geometry("250x400")#on définit la taille
        self.main.title("Bataille Navale - Placez vos navires")#on définit le titre
        fr=Frame(self.main)
        self.cote=6
        self.labelx= [Label(fr,text=" ") for j in range(self.cote+1)]#on crée les différents labels
        for j in self.labelx:#pour j dans labelx
            j.pack(fill="both", expand=True,side=LEFT)#place le label
        fr.pack(fill="both", expand=True,side=TOP)#place la frame

        fra0=Frame(self.main)
        fra1=Frame(fra0)
        fra2=Frame(fra0)
        self.labely= [Label(fra1,text=" ") for j in range(self.cote+1)]#on crée les différents labels
        for j in self.labely:#pour j dans labely
            j.pack(side=TOP)#place labely
        self.grille1=Grille(self.cote,self.cote,self.placer,fra2)#on crée une grille
        fra2.pack(fill='both',expand=True,side=RIGHT)#placer frame
        fra1.pack(fill="both",expand=True,side=LEFT)#placer fra1
        fra0.pack(fill="both", expand=True)#placer fra0
        #on charge les couleurs
        if Save.load("color")==None:
            self.color=("#6b0505","#04195d","#474038","#d9d9d9")
        else:self.color=Save.load("color")
        frm=Frame(self.main)
        self.label2=Label(frm,text="ᐁ Réserve de navires ᐁ")
        self.label2.pack(side=LEFT)
        self.DaButton=Button(frm,text="Retourner",command=self.switch)
        self.DaButton.pack(side=RIGHT,fill="both", expand=True)
        frm.pack(fill="both", expand=True)
        self.color_b=["#ff0000","#820458","#000000","#474038","#00FF00","#0000ff"]
        self.longb=[1,2,2,3]
        self.coulp=[]
        self.retournement=1
        self.to_place=self.gen()#on génère

        a=list(zip(*self.to_place))
        for y in range(0,self.cote):
            self.labely[y].configure(text=str(a[1].count(y)))
        for x in range(1,self.cote+1):
            self.labelx[x].configure(text=str(a[0].count(x-1)))
        

        self.grille_selection=Grille(6,5,self.select,self.main)
        self.select_color=self.color[3]
        for i in range(len(self.longb)):
            for y in range(self.longb[i]):
                self.grille_selection.setColor(i,4-y,self.color_b[i])

        self.main.mainloop()#on lance la fenêtre
    def placer(self,co):
        if self.select_color and self.notin(co,co[1-self.retournement],co[1-self.retournement]+self.longb[self.color_b.index(self.select_color)]):#str=true
            if self.select_color not in self.coulp:
                for i in range(self.longb[self.color_b.index(self.select_color)]):
                    self.grille1.setColor(co[0]+i if self.retournement else co[0],co[1] if self.retournement else co[1]+i,self.select_color)
                    self.coulp.append(self.select_color)
            else:
                self.remove_col(self.select_color)
                self.placer(co)
        if self.verif(self.grille1,self.to_place):
            if askyesno("🎉 Nous avons un vainqueur 🎉",choice(["Bien joué","Vous avez gagné","C\'était simple ?"])+"\nSouhaitez-vous rejouer ?",master=self.main, parent=self.main):
                self.clear()
            else:
                self.main.destroy()

    def clear(self):
        self.to_place=self.gen()

        a=list(zip(*self.to_place))
        for y in range(0,self.cote):
            self.labely[y].configure(text=str(a[1].count(y)))
        for x in range(1,self.cote+1):
            self.labelx[x].configure(text=str(a[0].count(x-1)))
        for i in self.color_b:
            self.remove_col(i)
    def notin(self,co,a,b):
        l=[]
        if self.retournement:
            for i in range(a,b-1):
                print(co,i)
                l.append(self.grille1.getColor(i,co[1]))
        else:
            for i in range(a,b-1):
                print(co,i)
                l.append(self.grille1.getColor(co[0],i))
                
        return l.count(self.color[3])==len(range(a,b-1))
    def select(self,co):
        self.select_color=self.grille_selection.getColor(co[0],co[1]) if self.grille_selection.getColor(co[0],co[1])!=self.color[3] else 0
    def switch(self):
        self.retournement=1-self.retournement
        a="right" if self.retournement else "down"
        self.DaButton.configure(text="Retourner "+a)
    def remove_col(self,color):
        for y in range(self.cote):
            for x in range(self.cote):
                if self.grille1.getColor(x,y)==color:
                    self.grille1.setColor(x,y,self.color[3])
        self.coulp.remove(color)
    def gen(self):
        a=[]
        g=Grille(self.cote,self.cote,print,self.main,mode_fast=1)
        v=self.longb[::-1]
        for j in range(len(v)):
                placed=0
                while not placed:
                    start=(randint(0,self.cote-1),randint(0,self.cote-1),randint(0,1))
                    try:
                        if all(g.getColor(start[0]+start[2]*i,start[1]+(1-start[2])*i)==g.getColor(start[0]+start[2]*i+1,start[1]+(1-start[2])*i+1)==g.getColor(start[0]+start[2]*i-1,start[1]+(1-start[2])*i-1)==g.getColor(start[0]+start[2]*i+1,start[1]+(1-start[2])*i-1)==g.getColor(start[0]+start[2]*i-1,start[1]+(1-start[2])*i+1)==g.getColor(start[0]+start[2]*i-1,start[1]+(1-start[2])*i)==g.getColor(start[0]+start[2]*i+1,start[1]+(1-start[2])*i)==g.getColor(start[0]+start[2]*i,start[1]+(1-start[2])*i+1)==g.getColor(start[0]+start[2]*i,start[1]+(1-start[2])*i-1)==self.color[3] and 0<=start[0]+start[2]*i<=self.cote and 0<=start[1]+(1-start[2])*i<=self.cote for i in range(v[j])):
                            for i in range(v[j]) :
                                    g.setColor(start[0]+start[2]*i,start[1]+(1-start[2])*i,self.color_b[j])
                                    a.append((start[0]+start[2]*i,start[1]+(1-start[2])*i))
                                    placed=1
                                #else:
                                    #break
                        else:
                            start=(randint(0,self.cote-1),randint(0,self.cote-1),randint(0,1))
                    except:start=(randint(0,self.cote-1),randint(0,self.cote-1),randint(0,1))
        print(a)
        return a
    def verif(self,g,a):
        for co in a:
           if g.getColor(co[0],co[1])==self.color[3]:
                print(co)
                return False
        return True

#Quarto
class Quarto:
    def __init__(self):
        self.main = Toplevel()#On fonde l'élément de la fenêtre (ici, on utilise Toplevel pour éviter de faire buger les images)
        self.main.geometry("230x460")#on définit la taille
        self.main.title("Quarto - Quatres pieces, quatres")#on définit le titre
        self.main.configure(bg="#432818")#on définit la couleur de fond
        #chargement des couleurs
        if Save.load("color")==None:
            self.color=("#6b0505","#04195d","#474038","#d9d9d9")
        else:self.color=Save.load("color")        
        self.label= Label(self.main,text="Quelle pièce allez vous donner ?",bg="#432818",fg="#FFFFFF")
        self.label.pack()#on place
        self.grille1=Grille(4,4,self.pose,self.main,highlightcolor="#99582A")#on crée une grille
        for i in range(16):
            self.grille1.setColor(i,0,"#432818")#on définit la couleur
#frame centrale
        frm=Frame(self.main)
        frm.configure(bg="#432818")
        self.label2=Label(frm,text="ᐁ Réserve de pièce ᐁ",bg="#432818",fg="#FFFFFF")
        self.label2.pack(side=LEFT)
        self.DaButton=Button(frm,bg="#432818",activebackground="#432818")
        self.DaButton.pack(side=RIGHT,fill="both", expand=True)
        frm.pack(fill="both", expand=True)
#on génère les variables images
        self.posé=[""]
        self.attr=[[],[]]
        self.grille=Grille(4,4,self.action,self.main,highlightcolor="#99582A")#on crée une grille

        img0 = Image.open("./img/quarto/bgcc.png")
        self.cb = ImageTk.PhotoImage(img0)
        img0=img0.resize((25,25))
        self.smoll_cb=ImageTk.PhotoImage(img0)

        img1= Image.open("./img/quarto/wgcc.png")
        self.cw= ImageTk.PhotoImage(img1)
        img1=img1.resize((25,25))
        self.smoll_cw=ImageTk.PhotoImage(img1)

        img2= Image.open("./img/quarto/wgcn.png")
        self.w=ImageTk.PhotoImage(img2)
        img2=img2.resize((25,25))
        self.smoll_w=ImageTk.PhotoImage(img2)

        img3=Image.open("./img/quarto/bgcn.png")
        self.b=ImageTk.PhotoImage(img3)
        img3=img3.resize((25,25))
        self.smoll_b=ImageTk.PhotoImage(img3)

        img4= Image.open("./img/quarto/bgpn.png")
        self.bc=ImageTk.PhotoImage(img4)
        img4=img4.resize((25,25))
        self.smoll_bc=ImageTk.PhotoImage(img4)

        img5= Image.open("./img/quarto/wgpn.jpg")
        self.wc=ImageTk.PhotoImage(img5)
        img5=img5.resize((25,25))
        self.smoll_wc=ImageTk.PhotoImage(img5)

        img6= Image.open("./img/quarto/bgpc.png")#cblack_circle.png")
        self.cbc=ImageTk.PhotoImage(img6)
        img6=img6.resize((25,25))
        self.smoll_cbc=ImageTk.PhotoImage(img6)#Small Creu black Circle

        img7= Image.open("./img/quarto/wgpc.png")
        self.cwc=ImageTk.PhotoImage(img7)#Creu white Circle
        img7=img7.resize((25,25))
        self.smoll_cwc=ImageTk.PhotoImage(img7)#Small Creu white Circle 
        
        #placement sur la grille secondaire
#grand noir plein rectangle
        self.grille.setColor(0,0,"#432818")
        self.grille.setImg(0,0,self.b)
#grand noir clein cercle
        self.grille.setColor(1,0,"#432818")
        self.grille.setImg(1,0,self.cbc)
#grand noir creu rectangle
        self.grille.setColor(2,0,"#432818")
        self.grille.setImg(2,0,self.cb)
#grand noir creu cercle
        self.grille.setColor(3,0,"#432818")
        self.grille.setImg(3,0,self.bc)
#petit noir plein rectangle
        self.grille.setColor(0,1,"#432818")
        self.grille.setImg(0,1,self.smoll_b)
#petit noir clein cercle
        self.grille.setColor(1,1,"#432818")
        self.grille.setImg(1,1,self.smoll_bc)
#petit noir creu rectangle
        self.grille.setColor(2,1,"#432818")
        self.grille.setImg(2,1,self.smoll_cb)
#petit noir creu cercle
        self.grille.setColor(3,1,"#432818")
        self.grille.setImg(3,1,self.smoll_cbc)
#grand blanc plein rectangle
        self.grille.setColor(0,2,"#432818")
        self.grille.setImg(0,2,self.w)
#grand blanc clein cercle
        self.grille.setColor(1,2,"#432818")
        self.grille.setImg(1,2,self.cwc)
#grand blanc creu rectangle
        self.grille.setColor(2,2,"#432818")
        self.grille.setImg(2,2,self.cw)
#grand blanc creu cercle
        self.grille.setColor(3,2,"#432818")
        self.grille.setImg(3,2,self.wc)
#petit blanc plein rectangle
        self.grille.setColor(0,3,"#432818")
        self.grille.setImg(0,3,self.smoll_w)
#petit blanc plein cercle
        self.grille.setColor(1,3,"#432818")
        self.grille.setImg(1,3,self.smoll_wc)
#petit blanc creu rectangle
        self.grille.setColor(2,3,"#432818")
        self.grille.setImg(2,3,self.smoll_cw)
#petit blanc creu cercle
        self.grille.setColor(3,3,"#432818")
        self.grille.setImg(3,3,self.smoll_cwc)
        
        self.a=""#variable de communication entre fonction de cette classe
        self.main.mainloop()#on lance la fenêtre
    def action(self,co):
        """
        Action lors de la séléction d'une pièce
        """
        if self.a in self.posé:
            self.label.configure(text="Où placer cette pièce ?")#on change le texte
            color=self.grille.getColor(co[0],co[1])
            img=self.grille.getImg(co[0],co[1])
            if color!=self.color[3]:#si la couleur est différente de self.color[3]
                self.a=color,img
                self.grille.setImg(co[0],co[1],"")
                self.grille.setColor(co[0],co[1],self.color[3])
                self.DaButton.configure(bg=color,activebackground=color,image=img)
    def verif(self):
        """
        Vérifie si un joueur a gagné
        on test horizontalement, puis verticalement, puis diagonalement
        On test d'abords pour les couleurs, puis les images
        """
#test image
        a=[]
        for y in range(4):#pour y dans 4 
            a.append([])
            for x in range(4):#pour x dans 4 
                a[y].append(self.grille1.getImg(x,y))
            if self.get_num_po(a[y]):self.win()#si combinaison gagnante, gagner
            if self.get_num_po(a):self.win()#si combinaison gagnante, gagner
        b=list(zip(a[0],a[1],a[2],a[3]))
        print(b)
        #verticalement
        for i in b:#pour i dans b
            if self.get_num_po(i):self.win()#si combinaison gagnante, gagner
        #diagonalement
        c=[]
        d=[]
        for i in range(4):#pour i dans 4 
            c.append(b[i][i])
            d.append(b[i][3-i])
        if self.get_num_po(c):self.win()#si combinaison gagnante, gagner
        if self.get_num_po(d):self.win()#si combinaison gagnante, gagner



    def get_num_po(self,a):
        """
        Paramètre : 
        a: Liste d'imageTK

        Cette fonction renvoie True lorsque la liste a contient uniquement des imagesTK inclues dans les ensembles possibles
        """
        for j in [[self.b,self.cb,self.bc,self.cbc,self.smoll_b,self.smoll_cb,self.smoll_bc,self.smoll_cbc],
        [self.w,self.cw,self.wc,self.cwc,self.smoll_w,self.smoll_cw,self.smoll_wc,self.smoll_cwc],
        [self.cw,self.cb,self.cbc,self.cwc,self.smoll_cw,self.smoll_cb,self.smoll_cbc,self.smoll_cwc],
        [self.w,self.b,self.wc,self.bc,self.smoll_w,self.smoll_b,self.smoll_wc,self.smoll_bc],
        [self.wc,self.cwc,self.cbc,self.bc,self.smoll_wc,self.smoll_cwc,self.smoll_cbc,self.smoll_bc],
        [self.b,self.w,self.bc,self.wc,self.smoll_w,self.smoll_b,self.smoll_bc,self.smoll_wc],
        [self.b,self.w,self.bc,self.wc,self.cbc,self.cb,self.cw,self.cwc],
        [self.smoll_b,self.smoll_bc,self.smoll_cbc,self.smoll_cb,self.smoll_w,self.smoll_wc,self.smoll_cwc,self.smoll_cw]]:
            f=0
            for i in a:#pour i dans a
                for k in j:#pour k dans j
                    if str(i)==str(k):#si les deux images sont identiques
                        f+=1#incrémenter f
            if f==4:return True#si f vaut 4, renvoie vrai
    def pose(self,co):
        """
        Va poser la pièce stockée dans self.a aux coordonées
        """
        if self.a not in self.posé and self.grille1.getColor(co[0],co[1])=="#432818" and self.grille1.getImg(co[0],co[1])=="":#si la case est vide, et que la pièce n'est pas placée
            self.posé.append(self.a)
            self.DaButton.configure(bg=self.color[3],activebackground=self.color[3],image="")
            self.grille1.setColor(co[0],co[1],self.a[0])
            self.label.configure(text="Quelle pièce allez vous donner ?")
            self.grille1.setImg(co[0],co[1],self.a[1])
            self.verif()#on vérifie si win
    def win(self):
        """
        Affiche un texte de félicitation
        """
        if askyesno("🎉 Nous avons un vainqueur 🎉",choice(["L'autre joueur n'a pas du voir ce coup","Une petite erreur de l'adversaire ?","Et si tu avais joué autrement ?"])+", bravo\nSouhaitez-vous rejouer ?",master=self.main, parent=self.main):#demander si le joueur souhaite rejouer
            self.clear()#on reset le terrain
        else:#sinon
            self.main.destroy()#explosion de la fenêtre 
    def clear(self):
        """
        On reset le jeu
        """
        #grand noir plein rectangle
        self.grille.setColor(0,0,"#432818")
        self.grille.setImg(0,0,self.b)
#grand noir clein cercle
        self.grille.setColor(1,0,"#432818")
        self.grille.setImg(1,0,self.cbc)
#grand noir creu rectangle
        self.grille.setColor(2,0,"#432818")
        self.grille.setImg(2,0,self.cb)
#grand noir creu cercle
        self.grille.setColor(3,0,"#432818")
        self.grille.setImg(3,0,self.bc)
#petit noir plein rectangle
        self.grille.setColor(0,1,"#432818")
        self.grille.setImg(0,1,self.smoll_b)
#petit noir clein cercle
        self.grille.setColor(1,1,"#432818")
        self.grille.setImg(1,1,self.smoll_bc)
#petit noir creu rectangle
        self.grille.setColor(2,1,"#432818")
        self.grille.setImg(2,1,self.smoll_cb)
#petit noir creu cercle
        self.grille.setColor(3,1,"#432818")
        self.grille.setImg(3,1,self.smoll_cbc)
#grand blanc plein rectangle
        self.grille.setColor(0,2,"#432818")
        self.grille.setImg(0,2,self.w)
#grand blanc clein cercle
        self.grille.setColor(1,2,"#432818")
        self.grille.setImg(1,2,self.cwc)
#grand blanc creu rectangle
        self.grille.setColor(2,2,"#432818")
        self.grille.setImg(2,2,self.cw)
#grand blanc creu cercle
        self.grille.setColor(3,2,"#432818")
        self.grille.setImg(3,2,self.wc)
#petit blanc plein rectangle
        self.grille.setColor(0,3,"#432818")
        self.grille.setImg(0,3,self.smoll_w)
#petit blanc plein cercle
        self.grille.setColor(1,3,"#432818")
        self.grille.setImg(1,3,self.smoll_wc)
#petit blanc creu rectangle
        self.grille.setColor(2,3,"#432818")
        self.grille.setImg(2,3,self.smoll_cw)
#petit blanc creu cercle
        self.grille.setColor(3,3,"#432818")
        self.grille.setImg(3,3,self.smoll_cwc)
        
        self.a=""
        self.posé=[]
        for y in range(4):#pour y dans 4
            for x in range(4):#pour x dans 4
                self.grille1.setColor(x,y,"#432818")
                self.grille1.setImg(x,y,"")
        self.DaButton.configure(bg=self.color[3],activebackground=self.color[3],image="")
        self.a=""#variable de communication entre fonction de cette classe
        self.pose((0,0))

#mastermind
class Mastermind:
    def __init__(self):
        self.main= Toplevel()#On fonde l'élément
        self.main.geometry("270x280")#on définit la taille de la fenêtre
        self.main.title("Mastermind - Le maitre des cerveaux")#on définit le titre
        if Save.load("color")==None:
            self.color=("#6b0505","#04195d","#474038","#d9d9d9")
        else:self.color=Save.load("color")
        #on définit les constantes et variables
        self.list_colors=["#ff0000","#820458","#000000","#00ff00","#0000ff","#485451","#574641","#ffff00","#00ffff"]
        self.select_color=self.color[3]
        self.selected_color=[]
        self.count=0

        self.grille=Grille(8,8,print,self.main)#on crée une grille
        self.sub_btn=Button(self.main,text="Deviner les couleurs", command=self.color_picker,highlightcolor="black",highlightthickness=2,highlightbackground="black")
        self.sub_btn.pack(fill="both",expand=True)
        self.color_picker()

        self.main.mainloop()#on lance la fenêtre
    def onchange(self):
        if self.count>=1:
            print(self.selected_color,self.count)
            for i in range(4):
                self.grille.setColor(i,self.count-1,self.selected_color[self.count][i])
                self.verif(self.count-1)
    def verif(self,y):
        bon=0
        for col in range(4):
            if self.grille.getColor(col,y) in self.selected_color[0]:
                if self.grille.getColor(col,y) == self.selected_color[0][col]:
                    self.grille.setColor(col+4,y,"#00ff00")
                    self.grille.setText(col+4,y,"C")
                    bon+=1
                else:
                    self.grille.setColor(col+4,y,"#ff0000")
                    self.grille.setText(col+4,y,"P")
            else:
                self.grille.setColor(col+4,y,"#000000")
                self.grille.setText(col+4,y,"N")
        if bon==4:
            self.win.destroy()
            if askyesno("🎉 Nous avons un vainqueur 🎉","Le chercheur a gagné, bravo\nSouhaitez vous rejouer",master=self.main, parent=self.main):
                self.clear()
            else:
                self.main.destroy()
    def clear(self):
        for y in range(8):
            for x in range(8):
                self.grille.setColor(x,y,self.color[3])
                self.grille.setText(x,y,"")
        self.select_color=self.color[3]
        self.selected_color=[]
        self.count=0
        self.color_picker()

    def color_picker(self):
        self.win=Toplevel()
        self.win.geometry("260x125")
        self.win.title("Placez vos couleurs")
        self.win.attributes('-topmost', 1)#on affiche au premier plan
        self.g_f=Grille(4,1,self.select,self.win)
        self.g_p=Grille(len(self.list_colors),1,self.get,self.win)
        for i in self.list_colors:
            self.g_p.setColor(self.list_colors.index(i),0,i)
        self.DaButton=Button(self.win,text="Valider",command=self.valider_colorpicker)
        self.DaButton.pack(side=BOTTOM,fill="both",expand=True)
        self.RandBtn=Button(self.win,text="Générer aléatoirement",command=self.gen)
        if self.count==0:
            self.RandBtn.pack(side=BOTTOM,fill="both",expand=True)

        self.win.mainloop()#on lance la fenêtre
    def gen(self):
        for i in range(4):
            self.g_f.setColor(i,0,choice(self.list_colors))
        self.valider_colorpicker()
    def valider_colorpicker(self):
        a=[]
        for i in range(4):
            a.append(self.g_f.getColor(i,0) if self.g_f.getColor(i,0)!=self.color[3] else "#ff0000")
        print(a)
        self.selected_color.append(tuple(a))
        self.onchange()
        self.win.destroy()
        self.count+=1
    def select(self,co):
        self.g_f.setColor(co[0],co[1],self.select_color)
    def get(self,co):
        self.select_color=self.g_p.getColor(co[0],co[1])
class Puissance4 :
    def __init__(self):
        self.main = Toplevel()
        self.main.geometry("200x210")
        self.main.title("Puissance 4 - À vos pièces")
        self.label= Label(self.main,text="Place ta pièce?")
        self.label.pack(anchor=CENTER, fill="both", expand=True)
        self.grille=Grille(7,6,self.action,self.main)
        self.color=('red','yellow')
        self.tour=0
        self.label.configure(bg=self.color[self.tour],fg=black_or_white(["#ff0000","#ffff00"][self.tour]))
        

        self.main.mainloop()#on lance la fenêtre
    def verifier(self,piece):
        bonne_cases=1
        if piece[0]-1!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]-1,piece[1]) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
            bonne_cases=bonne_cases+1
            if piece[0]-2!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]-2,piece[1]) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
                bonne_cases=bonne_cases+1
                if piece[0]-3!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]-3,piece[1]) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
                    bonne_cases=bonne_cases+1
        if piece[0]+1!=7 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]+1,piece[1]) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
            bonne_cases=bonne_cases+1
            if piece[0]+2!=7 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]+2,piece[1]) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
                bonne_cases=bonne_cases+1
                if piece[0]+3!=7 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]+3,piece[1]) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
                    bonne_cases=bonne_cases+1
        if bonne_cases>=4:
            if askyesno("🎉 Nous avons un vainqueur 🎉","Joueur "+self.grille.getColor(piece[0],piece[1])+" est vainqueur\nSouhaitez-vous rejouer ?",master=self.main, parent=self.main):
                self.clear()
            else:
                self.main.destroy()
        
        
        #Faire axe Y
        print(bonne_cases)
        bonne_cases=1
        
        

        
        
        
        if piece[1]-1!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0],piece[1]-1) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
            bonne_cases=bonne_cases+1
            if piece[1]-2!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0],piece[1]-2) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
                bonne_cases=bonne_cases+1
                if piece[1]-3!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0],piece[1]-3) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
                    bonne_cases=bonne_cases+1
        if piece[1]+1!=6 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0],piece[1]+1) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
            bonne_cases=bonne_cases+1
            if piece[1]+2!=6 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0],piece[1]+2) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
                bonne_cases=bonne_cases+1
                if piece[1]+3!=6 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0],piece[1]+3) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):
                    bonne_cases=bonne_cases+1
        if bonne_cases>=4:
            if askyesno("🎉Nous avons un vainqueur 🎉","Joueur "+self.grille.getColor(piece[0],piece[1])+" est vainqueur\nSouhaitez-vous rejouer ?",master=self.main, parent=self.main):
                self.clear()
            else:
                self.main.destroy()
        print(bonne_cases)
        bonne_cases=1
        
        if piece[1]-1!=-1 and piece[0]-1!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]-1,piece[1]-1) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
            bonne_cases=bonne_cases+1
            if piece[1]-2!=-1 and piece[0]-2!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]-2,piece[1]-2) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
                bonne_cases=bonne_cases+1
                if piece[1]-3!=-1 and piece[0]-3!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]-3,piece[1]-3) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
                    bonne_cases=bonne_cases+1
        if piece[1]+1!=6 and piece[0]+1!=6 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]+1,piece[1]+1) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
            bonne_cases=bonne_cases+1
            if piece[1]+2!=6 and piece[0]+2!=6 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]+2,piece[1]+2) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
                bonne_cases=bonne_cases+1
                if piece[1]+3!=6 and piece[0]+3!=6 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]+3,piece[1]+3) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
                    bonne_cases=bonne_cases+1
                    
        if bonne_cases>=4:
            if askyesno("🎉 Nous avons un vainqueur 🎉","Joueur "+self.grille.getColor(piece[0],piece[1])+" est vainqueur\nSouhaitez-vous rejouer ?",master=self.main, parent=self.main):
                self.clear()
            else:
                self.main.destroy()
        print(bonne_cases)
        bonne_cases=1
        
        
        if piece[0]-1!=-1 and piece[1]+1!=6 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]-1,piece[1]+1) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
            bonne_cases=bonne_cases+1
            if piece[0]-2!=-1 and piece[1]+2!=6 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]-2,piece[1]+2) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
                bonne_cases=bonne_cases+1
                if piece[0]-3!=-1 and piece[1]+3!=6 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]-3,piece[1]+3) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
                    bonne_cases=bonne_cases+1
                    
        if piece[0]+1!=6 and piece[1]-1!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]+1,piece[1]-1) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
            bonne_cases=bonne_cases+1
            if piece[0]+2!=6 and piece[1]-2!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]+2,piece[1]-2) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
                bonne_cases=bonne_cases+1
                if piece[0]+3!=6 and piece[1]-3!=-1 and self.grille.getColor(piece[0],piece[1])==self.grille.getColor(piece[0]+3,piece[1]-3) and self.grille.getColor(piece[0],piece[1]) in ('yellow','red'):     
                    bonne_cases=bonne_cases+1
        if bonne_cases>=4:
            if askyesno("🎉 Nous avons un vainqueur 🎉","Joueur "+self.grille.getColor(piece[0],piece[1])+" est vainqueur\nSouhaitez-vous rejouer ?",master=self.main, parent=self.main):
                self.clear()
            else:
                self.main.destroy()
        print(bonne_cases)
        bonne_cases=1
        
            
        
                   
                    
            
        
        
        
        
    def action(self,bouton):
        print(self.grille.getColor(bouton[0],bouton[1]))
        if self.grille.getColor(bouton[0],bouton[1]) in ('yellow','red'):
            return print('Veuillez sélectionner une case non prise.')
        piece=(self.casetombe(bouton)[0],self.casetombe(bouton)[1])
        self.grille.setColor(piece[0],piece[1],self.color[self.tour])
        if self.tour==0:
            self.tour=1
        else:
            self.tour=0
        self.label.configure(bg=self.color[self.tour],fg=black_or_white(["#ff0000","#ffff00"][self.tour]))
        self.verifier(piece)
        
        
        
        
        
    def casetombe(self,bouton):
        i=1
        if bouton[1]==5:
            return (bouton[0],bouton[1])
        
            
        while self.grille.getColor(bouton[0],bouton[1]+i)!='red' and self.grille.getColor(bouton[0],bouton[1]+i)!='yellow':
            if bouton[1]+i==6:
                return (bouton[0],bouton[1]+i)
            if bouton[1]+i==5:
                return (bouton[0],bouton[1]+i)
            i=i+1
        return (bouton[0],(bouton[1]+i)-1)
        
       
        
        
        
    def clear(self):
        for y in range(6):
            for x in range(7):
                self.grille.setColor(x,y,"#d9d9d9")
                
                
                
    def tour(self,bouton):
        if self.tour==0:
            self.tour=1
        else:
            self.tour=0
#Nerdle
class Nerdle:
    def __init__(self):
        self.main= Toplevel()#On fonde l'élément#On fonde l'élément de la fenêtre
        self.main.geometry("280x250")
        self.main.title("Nerdle - Comptez bien")
        self.grille=Grille(8,6,print,self.main)
        self.strvar=StringVar(master=self.main)
        c=Frame(self.main)
        self.input=Entry(c,textvariable=self.strvar)
        self.input.pack(side=LEFT, fill="both",expand=True)
        self.strvar.trace("w", lambda *args: self.character_limit(self.strvar))
        self.submit=Button(c,command=self.subm,text="GO")
        self.submit.pack(side=RIGHT,fill="both",expand=True)
        c.pack(fill="both")
        a=Grille(3,1,print,self.main)
        self.color=["#398874","#820458","#000000",Save.load("color")[3]]
        b=list(zip(self.color,["Correct","Mal placé","Invalide"]))
        for i in range(len(b)):
            a.setColor(i,0,b[i][0])
            a.setText(i,0,b[i][1])
        
        self.expr=self.gen()
        self.tour=0
        print(self.expr)
        self.main.bind('<Return>', self.action_entrer)#lancer self.action_entrer si [Enter]
        self.main.mainloop()#on lance la fenêtre
    def character_limit(self,txt):
        """
        Cette fonction permet de s'assurer que le texte ne contienne pas trop de caractères, ou des charactères interdits.
        """
        try:
            if len(txt.get()) > 8:
                txt.set(txt.get()[:-1])
            if txt.get()[-1] not in "0123456879/*-+=":
                txt.set(txt.get()[:-1])
        except Exception as e:print("erreur non fatale - "+str(e))

    def action_entrer(self,event):
        self.subm()
    def action(self):
        bon=0
        if self.tour==5:
            if askyesno("Perdu, quel domage", "Hélas, vous avez perdu\n "+self.expr+"\nSouhaitez-vous rejouer ?",master=self.main, parent=self.main):
                self.clear()
            else:
                self.main.destroy()
        for char in range(8):
            if self.strvar.get()[char] in self.expr:
                if self.strvar.get()[char] == self.expr[char]:
                    self.grille.setColor(char,self.tour,self.color[0])
                    self.grille.setText(char,self.tour,self.strvar.get()[char])
                    bon+=1
                else:
                    self.grille.setColor(char,self.tour,self.color[1])
                    self.grille.setText(char,self.tour,self.strvar.get()[char])
            else:
                self.grille.setColor(char,self.tour,self.color[2])
                self.grille.setText(char,self.tour,self.strvar.get()[char])
        self.input.delete(0, last=END)
        self.tour+=1
        if bon==8:
            if askyesno("🎉 Bravo, vous avez gagné 🎉", "Bravo, vous avez réussi \nSouhaitez-vous rejouer ?",master=self.main, parent=self.main):
                self.clear()
            else:
                self.main.destroy()
    def subm(self):
        if self.strvar.get().count("=")!=1:
            return showerror("Ce calcul est incorect","Ce calcul est invalide, il doit contenir un seul \"=\"",master=self.main, parent=self.main)
        a=self.strvar.get().split("=")
        if eval(a[0])==eval(a[1]):
            print("action")
        else:
            return showerror("Ce calcul est incorect","Ce calcul est invalide, assure toi que chaque partie autour du \"=\" soit la même valeur",master=self.main, parent=self.main)
        if len(self.strvar.get())!=8:
            return showerror("Caractères manquant","Votre calcul doit comporter 8 caractères",parent=self.main,master=self.main)
        self.action()
    def gen(self):
        a=choice("123456879/*-+")
        b=""
        for i in range(randint(1,2)):
            b+=str(randint(1,9))
        print(b)
        t=0
        while 1:
            for i in range(8-len(str(b))-2):
                a+=choice("0123456879/*-+")
            try:
                if eval(a)==eval(b) and "++" not in a and "--" not in a and a!="+"+str(b):break
                else:a=choice("123456879/*-+")
            except:a=choice("123456879/*-+")
            if t>99999999:
                t=0
                b=""
                for i in range(randint(0,2)):
                    b+=str(randint(1,9))
            t+=1
        return str(a+"="+str(b))
    def clear(self):
        for y in range(6):
            for x in range(8):
                self.grille.setColor(x,y,self.color[3])
                self.grille.setText(x,y,"")
        self.expr=self.gen()
        self.tour=0
        self.strvar.set("")

#gratte Ciel
class Gratte_ciel :
    def __init__(self):
        self.main = Toplevel()
        self.main.geometry("200x200")
        self.main.title("Gratte-ciel")
        self.grille=Grille(6,6,self.action,self.main)
        self.color="#716F6F"
        self.listenombre=[1,2,3,4]
        self.clique=0
        #Génération du niveau
        colonne_bonne=[[],[],[],[]]
        ligne_bonne=[[],[],[],[]]
        for y in range(6):
            for x in range(6):
                
                if x==0 or x==5 or y==0 or y==5:
                    self.grille.setColor(x,y,self.color)#Colories les contours
                    
                else:
                    a=randint(1,4)
                    anti_bug=0
                    while a in colonne_bonne[x-1] or a in ligne_bonne[y-1]:#Tant qu'il trouve pas une valeur non prise
                        a=randint(1,4)
                        anti_bug=anti_bug+1
                        
                        if anti_bug>999999:#si la génération du niveau bug
                            print("erreur - génération de niveaux, lancement nouvelle fenêtre")
                            Gratte_ciel()
                            self.main.destroy()
                    
                    
                    
                    colonne_bonne[x-1].append(a)#La solution sous forme de colonne
                    ligne_bonne[y-1].append(a)#La solution sous forme de ligne
                    
        #Contours du niveau  
        for j in range(4):
            
            
            maxi=colonne_bonne[j][0]
            compt=1
            for i in range(3):
                if colonne_bonne[j][i+1]>maxi:
                    maxi=colonne_bonne[j][i+1]
                    compt=compt+1
            self.grille.setText(j+1, 0, compt)
        
        for j in range(4):
           
           
            maxi=ligne_bonne[j][0]
            compt=1
            for i in range(3):
                if ligne_bonne[j][i+1]>maxi:
                    maxi=ligne_bonne[j][i+1]
                    compt=compt+1
            self.grille.setText(0, j+1, compt)
            
            
        for j in range(4):
            
            
            maxi=colonne_bonne[j][-1]
            compt=1
            for i in range(3,-1,-1):
                if colonne_bonne[j][i-1]>maxi:
                    maxi=colonne_bonne[j][i-1]
                    compt=compt+1
            self.grille.setText(j+1, 5, compt)
            
            
        for j in range(4):
            
            
            maxi=ligne_bonne[j][-1]
            compt=1
            for i in range(3,-1,-1):
                if ligne_bonne[j][i-1]>maxi:
                    maxi=ligne_bonne[j][i-1]
                    compt=compt+1
            self.grille.setText(5, j+1, compt)
            
        self.colonne_bonne=colonne_bonne
        self.ligne_bonne=ligne_bonne
        
        self.main.mainloop()
    def action(self,bouton):
        """
        Paramètres: un tuple bouton qui possede les coordonnées dess boutons
        Fonction qui permet d'afficher des nombres allant de 1 a 4 sur une grille 
        """
        if bouton[0]==0 or bouton[0]==5 or bouton[1]==0 or bouton[1]==5:
            print('Veuillez sélectionner les cases intérieures')
        else:
            
            self.grille.setText(bouton[0],bouton[1],self.listenombre[self.clique])
            self.clique=self.clique+1
            if self.clique==4:
                self.clique=0
            self.verifier()
        
            
            
        
        

        

        
    def verifier(self):
        grille_joueur=[[],[],[],[]] # initialisation de la grille du joueur
        for y in range(4):
            for x in range(4):
                grille_joueur[x].append(self.grille.getText(x+1, y+1)) #récupère la grille du joueur
        print(grille_joueur)
        print(self.colonne_bonne)
        if grille_joueur==self.colonne_bonne or grille_joueur==self.ligne_bonne: #vérifie si le joueur a gagné
            if askyesno("Nous avons un vainqueur","Vous avez gagné, bravo\nSouhaitez vous rejouer ?",parent=self.main):
                Gratte_ciel()
                self.main.destroy()
            else:
                self.main.destroy()




try:
    Welcome()#Menu d'acceuil
except Exception as e:
    showerror("Erreur fatale","Une erreur fatale est survenue\n\nChoisissez qui sera chargé de corriger cette erreur :\nYannis, Quentin, Matéo, François, Alexandre")
    print(e)
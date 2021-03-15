#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################
# CNG - Campus Naked Graphic
# Version 1.2 (nov. 2013)
# module graphique minimaliste
# Christian NGUYEN - nguyen@univ-tln.fr
# http://nguyen.univ-tln.fr
###############################################################

###############################################################
#
#    Copyright (c) 2011 Christian Nguyen
#    Copyright (c) 2012-2014 Christian Nguyen, Joseph Razik
#
#    This program is free software; you can redistribute it
#    and/or modify it under the terms of the GNU General
#    Public License as published by the Free Software
#    Foundation (version 2 of the License).
#
#    This program is distributed in the hope that it will
#    be useful, but WITHOUT ANY WARRANTY; without even the
#    implied warranty of MERCHANTABILITY or FITNESS FOR A
#    PARTICULAR PURPOSE.  See the GNU General Public License
#    for more details.
#
#    For a copy of the GNU General Public License, write to the
#    Free Software Foundation, Inc., 675 Mass Ave, Cambridge,
#    MA 02139, USA.
#
###############################################################

###############################################################
# TODO
# utiliser la <Python Imaging Library (PIL)> pour faire du
# traitement d'images
# PIL dispose du module <ImageTk>
# utilisation
# - chargement de l'image en mémoire: img = Image.open(mon_fichier)
# - conversion en "ImageTk": imgtk = ImageTk.PhotoImage(image = img,master=mon_canvas)"
# - chargement dans le Canvas.

###############################################################
# prise en compte de la version de Python
module_image = True
import sys
if sys.version_info >= (3,):
    from tkinter import *
    # pour les images avec Pillow
    try:
        from PIL import Image
        from PIL import ImageTk
    except:
        module_image = False
else:
    from Tkinter import *
    # pour les images avec PIL
    try:
        import Image
        import ImageTk
    except:
        module_image = False

###############################################################
# prise en compte des images avec PIL/Pillow

FLIP_LEFT_RIGHT = 0
FLIP_TOP_BOTTOM = 1
ROTATE_90 = 2
ROTATE_180 = 3
ROTATE_270 = 4

###############################################################
# variables globales

dico_touches = {} # dictionnaire des touches du clavier
__curkey = '' # touche du clavier courante
__lboutons = [0, 1, 2, 3, 4, 5] # boutons de la souris
__curx, __cury = 0, 0 # position courante
__ccol = "black" # couleur courante
__idlef = -1 # fonction associe a la idle_func
__the_end = False # bool d'arret de la idle_func

###############################################################
# fonctions privees
###############################################################

###############################################################
##### fonction privee d'affichage d'une erreur
def __erreur(perr):
    if sys.version_info >= (3,):
        # le parser detecte une erreur de syntaxe pour les versions < 3
        # solution : evaluation retardee
        eval("print(perr, file=sys.stderr)")
    else:
        print >> sys.stderr, perr

###############################################################
##### fonction privee associee a la fermeture de la fenetre principale
def __quitter():
    global __the_end
    __the_end = True
    root.destroy()

###############################################################
##### fonction privee de gestion du clavier
def __key_press(event):
    global dico_touches, __curkey, __the_end

    # avant tout, touche reservee : ESC
    if event.keysym == 'Escape':
        __the_end = True
        return
    # touches comportant un caractere
    if event.char == event.keysym or (event.char != event.keysym and event.char != ''):
        __curkey = event.char
        if sys.version_info >= (3,):
            if event.char in dico_touches:
                dico_touches[event.char]()
            else:
                __erreur("la touche "+event.char+" n'est associee a aucune fonction")
        else:
            if dico_touches.has_key(event.char):
                dico_touches[event.char]()
            else:
                __erreur("la touche "+event.char+" n'est associee a aucune fonction")
    # touches speciales (PageUp, Left, etc.)
    else:
        __erreur("touche speciale "+event.keysym+" non prise en compte")

###############################################################
##### fonction privee de gestion des boutons de la souris (1, 2 ou 3)
def __button_release(event):
    global __lboutons, __curx, __cury, la, ha

    # si le curseur est bien dans la fenetre
    if event.x >= 0 and event.x <= la and event.y >= 0 and event.y <= ha:
        __curx, __cury = event.x, event.y
        if __lboutons[event.num] != event.num:
            __lboutons[event.num]()

###############################################################
# fonctions publiques
###############################################################

###############################################################
##### creation et affichage de la fenetre graphique
# ATTENTION : premiere instruction du programme
def init_window(pnom='', pla=None, pha=None, color='white'):
    """ATTENTION : premiere instruction du programme
    creation et affichage de la fenetre graphique
    de nom pnom, de largeur pla et de hauteur pha
    """
    global root # fenetre principale
    global canv # zone graphique
    global la, ha # hauteur et largeur de la fenetre

    root = Tk()
    if pla == None and pha == None:
        # ATTENTION : ne prend pas en compte les barres du WM (!)
        la, ha = root.winfo_screenwidth(), root.winfo_screenheight()
    else:
        la, ha = pla, pha
    root.title(pnom)
    root.resizable(width=False, height=False)
    root.protocol("WM_DELETE_WINDOW", __quitter)
    root.bind("<Key>", __key_press)
    # binding bouton relachee pour laisser la possibilite a l'utilisateur de
    # corriger une erreur en sortant le curseur de l'application
    root.bind("<ButtonRelease>", __button_release)
    # zone graphique
    canv = Canvas(width = la, height = ha, bg = color)
    canv.pack()
    return root , canv

# information sur l'ecran
def get_screen_width():
    return root.winfo_screenwidth()

def get_screen_height():
    return root.winfo_screenheight()

###############################################################
##### boucle d'attente des evenements
# ATTENTION : derniere instruction du programme
def main_loop():
    """ATTENTION : derniere instruction du programme
    boucle d'attente des evenements
    """
    root.mainloop()

###############################################################
##### efface l'ecran de travail
def clear_screen():
    "efface l'ecran de travail"
    global canv
    canv.delete('all')

###############################################################
##### polymorphisme parametrique : couleur definie
# soit en hexadecimal avec r, v, b dans [O, 255] (8 bits / composante)
# soit par son nom (white, black, red, green, blue, cyan, yellow, magenta, ...)
def current_color(*args):
    """Definition de la couleur courante
       - soit en r, v, b dans [O, 255]
       - soit par son nom (white, black, red, green, blue, ...)
    """
    global __ccol

    # initialisation a noir en cas d'erreur
    __ccol = "black"
    # 1 parametre : le nom de la couleur
    if len(args) == 1:
        if isinstance(args[0], str):
            __ccol = args[0]
        else:
            __erreur("[current_color] le paramètre n'est pas une chaine")
    # 3 parametres : code RVB sur [0, 255]
    elif len(args) == 3:
        if isinstance(args[0], int) and isinstance(args[1], int) and isinstance(args[2], int):
            tc = [0, 0, 0]
            tc[0], tc[1], tc[2] = int(args[0]), int(args[1]), int(args[2])
            if -1<tc[0]<256 and -1<tc[1]<256 and -1<tc[2]<256:
                # concatenation avec suppression du prefixe 0x et
                # ajout d'un zero pour les nombres inf. a 16
                __ccol = '#'
                for i in range(3):
                    if tc[i] < 16:
                        __ccol += '0'+hex(tc[i])[2:]
                    else:
                        __ccol += hex(tc[i])[2:]
            else:
                __erreur("[current_color] composantes RVB pas entre 0 et 255")
        else:
            __erreur("[current_color] l'un des paramètres n'est pas un entier")
    # erreur : nombre de parametres incorrect
    else:
        __erreur("[current_color] nombre de paramètres incorrect (1 ou 3)")

###############################################################
# force la mise a jour
def refresh():
    "refraichit l'ecran (force le dessin)"
    # ATTENTION : update_idletasks prend en compte les animations en cours
    # ce qui n'est pas le cas du simple update
    canv.update_idletasks()
    #canv.update()

###############################################################
##### DRAWING
###############################################################

###############################################################
##### affichage d'un point
def point(px, py):
    """affichage d'un point de coordonnees (px, py) dans la couleur courante
    retour de l'identificateur unique de l'objet cree
    """
    global __ccol, la, ha

    if px < 0 or px > la or py < 0 or py > ha:
        __erreur("[point] coordonnees hors fenetre")
    # changement de repère
    py=ha-py
    id = canv.create_line(px, py, px+1, py+1, fill=__ccol)
    # retour de l'id de l'obj du canvas (pour translation, suppression, ...)
    return id

##### affichage d'un segment
def line(px1, py1, px2, py2, pep=1):
    """affichage d'un segment de sommets (px1, py1) et (px2, py2),
    d'epaisseur pep, dans la couleur courante
    retour de l'identificateur unique de l'objet cree
    """
    global __ccol, canv
    # changement de repère
    py1,py2=ha-py1,ha-py2
    id = canv.create_line(px1, py1, px2, py2, fill=__ccol, width=pep)
    return id

##### affichage d'un rectangle
def rectangle(px1, py1, px2, py2, pep=1):
    """affichage d'un rectangle dans la couleur courante
    defini par le sommet inf. gauche (px1, py1)
    et le sommet sup. droit (px2, py2) et d'epaisseur pep
    retour de l'identificateur unique de l'objet cree
    """
    # changement de repère
    py1,py2=ha-py1,ha-py2
    id = canv.create_print(ox, oy)
    rectangle(px1, py1, px2, py2, outline=__ccol, width=pep)
    return id

##### affichage d'un rectangle plein
def box(px1, py1, px2, py2):
    """affichage d'un rectangle plein dans la couleur courante
    defini par le sommet inf. gauche (px1, py1)
    et le sommet sup. droit (px2, py2)
    retour de l'identificateur unique de l'objet cree
    """
    global __ccol, canv
    # changement de repère
    py1,py2=ha-py1,ha-py2
    id = canv.create_rectangle(px1, py1, px2, py2, fill=__ccol, width=0)
    return id

##### affichage d'un cercle
def circle(px, py, pr, pep=1):
    """affichage d'un cercle de centre (px, py), de rayon pr et d'epaisseur pep
    retour de l'identificateur unique de l'objet cree
    """
    global canv
    # changement de repère
    py=ha-py
    id = canv.create_oval(px-pr, py-pr, px+pr, py+pr, outline=__ccol, width=pep)
    return id

##### affichage d'un disque
def disc(px, py, pr):
    """affichage d'un disque de centre (px, py) et de rayon pr
    retour de l'identificateur unique de l'objet cree
    """
    global canv
    # changement de repère
    py=ha-py
    id = canv.create_oval(px-pr, py-pr, px+pr, py+pr, fill=__ccol, width=0)
    return id

##### affichage d'un polygone
def polygon(*args):
    """affichage d'un polygone construit a partir d'une liste de coordonnees
    retour de l'identificateur unique de l'objet cree
    """
    # 1 parametre : une liste ou un tuple de coordonnees
    if len(args) == 1:
        if isinstance(args[0], list) or isinstance(args[0], tuple):
            # changement de repère
            nb = len(args[0])
            ll = [0 for i in range(nb)]
            for i in range(nb):
                if i%2 != 0:
                    ll[i] = ha-args[0][i]
                else:
                    ll[i] = args[0][i]
            id = canv.create_polygon(ll, fill=__ccol)
        else:
            __erreur("[polygon] le parametre n'est pas une liste ou un tuple")
    # N parametres : une suite de coordonnees
    elif len(args) > 1:
        # changement de repère
        nb = len(args)
        ll = [0 for i in range(nb)]
        for i in range(nb):
            if i%2 != 0:
                ll[i] = ha-args[i]
            else:
                ll[i] = args[i]
        id = canv.create_polygon(ll, fill=__ccol)
    else:
        __erreur("[polygon] parametre incorrect")
    return id

##### affichage d'un texte
def text(px, py, pch):
    """affichage d'un texte pch a partir de la position (px, py) aligne a gauche
    retour de l'identificateur unique de l'objet cree
    """
    global canv
    # changement de repère
    py=ha-py
    id = canv.create_text(px, py, text=pch, fill=__ccol, anchor='sw')
    return id

###############################################################
# manipulation des objets graphiques

##### recuperer la couleur courante de l'objet pid
def obj_get_color(pid):
    """retourne la couleur de fond de l'objet pid sous forme d'une
    chaine de caracteres
    """
    return canv.itemcget(pid, 'fill')

##### redefinir la couleur de l'objet pid avec la couleur courante
def obj_put_color(pid):
    """remplace la couleur de fond de l'objet pid par la couleur courante"""
    canv.itemconfigure(pid, fill=__ccol)

##### recuperer la position (centre geometrique) d'un objet
def obj_get_position(pid):
    """retourne la position, au sens du centre geometrique, de l'objet pid
    en coordonnees entieres"""
    lcoord = canv.coords(pid)
    lg = len(lcoord)
    x = 0
    for a in [lcoord[i] for i in range(lg) if i%2 == 0]:
        x += a
    y = 0
    for b in [lcoord[i] for i in range(lg) if i%2 == 1]:
        y += b
    n = lg/2
    return int(x/n), int(y/n)

##### deplacer un objet
def obj_move(pid, pdx, pdy):
    """deplacement relatif de l'objet graphique pid de (pdx, pdy)"""
    canv.move(pid, pdx, -pdy)

##### supprimer un objet
def obj_delete(pid):
    """suppression de l'objet graphique pid"""
    canv.delete(pid)

##### rendre visible un objet
def obj_show(pid):
    """rendre visible l'objet graphique pid"""
    canv.itemconfigure(pid, state='normal')

##### rendre invisible un objet
def obj_hide(pid):
    """rendre invisible l'objet graphique pid"""
    canv.itemconfigure(pid, state='hidden')

##### afficher un objet au dessus d'un autre
def obj_above(pid1, pid2):
    """l'objet graphique pid1 s'affiche au dessus de l'objet graphique pid2"""
    canv.tag_raise(pid1, pid2)

###############################################################
##### BINDINGS
###############################################################

##### association d'une touche pt avec une fonction pf
def assoc_key(pt, pf):
    "association d'une touche pt avec une fonction pf"
    global dico_touches
    dico_touches[pt] = pf

##### retourne le caractere correspondant a la touche pressee
def get_key():
    "retourne le caractere correspondant a la touche pressee"
    return __curkey

##### association d'un bouton pb (1, 2 ou 3) avec une fonction pf
def assoc_button(pb, pf):
    "association d'un bouton pb (1, 2 ou 3) avec une fonction pf"
    global __lboutons
    __lboutons[pb] = pf

##### retourne la position en X (resp. Y) du curseur de la souris
def get_mouse_x():
    "retourne la position en X du curseur de la souris"
    global __curx
    return __curx

def get_mouse_y():
    "retourne la position en Y du curseur de la souris"
    global __cury, ha
    return ha - __cury

##### fonction activee en l'absence d'action effectuee par l'utilisateur
def init_idle_func(pfunc):
    global __idlef
    __idlef = pfunc

def idle_func():
    __idlef() # appel de la fonction associee
    # MAJ du canvas, indispensable !
    canv.update()
    # recursion
    if (not __the_end):
        root.after(1, idle_func)

def idle_stop():
    global __the_end
    __the_end = True

def idle_start():
    global __the_end
    __the_end = False

# la fonction idle associee est-elle encore active ?
def idle_dead():
    return __the_end


###############################################################
##### IMAGE
###############################################################

##### chargement du fichier image et retour de son handle
# modifie le 08/01/2014 par Christian Nguyen
def image(name, width=None, height=None):
    """
    retourne une image a placer, avec changement de taille si demande.
    ATTENTION : la reference a l'image doit etre *globale*.
    """
    if module_image:
        im = Image.open(name)
        # changement de la taille de l'image si demande
        if width:
            # im.resize((width, height), Image.ANTIALIAS )
            im.thumbnail((width, height), Image.ANTIALIAS )
            # Joseph : resize marche pas mais thumbnail marche ...
            # Chris : resize marche mais renvoie une copie de l'image
        imp =  ImageTk.PhotoImage(im)
        return [im, imp]
    else:
        if sys.version_info >= (3,):
            __erreur("[image] module Pillow non charge")
        else:
            __erreur("[image] module PIL non charge")
        return None

##### affichage de l'image imp dans le canvas
def image_draw(px, py, pim):
    """
    place une image dans la fenetre par rapport a son centre
    pim : couple image pil, image tk
    retour de l'identificateur unique de l'objet cree
    """
    global canv
    if module_image:
        # changement de repère
        py = ha-py
        id = canv.create_image(px, py, image=pim[1], anchor='center')
        return id
    else:
        if sys.version_info >= (3,):
            __erreur("[image] module Pillow non charge")
        else:
            __erreur("[image] module PIL non charge")

##### extraction d'une region d'une image et retour de son handle
def image_from_tiles(name, tile_width=None, tile_height=None, idx_x=0, idx_y=0, modif=None, final_width=None, final_height=None):
    """
    retourne une image a partir d'une image regroupant plusieurs sous-images (sprites) avec possibilite de modifications simples (dilatations/symetries/rotations)
    transformation possible: FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, ROTATE_90, ROTATE_180, ROTATE_270
    """
    if module_image:
        # charge l'image complete
        im = Image.open(name)
        # recupere que le sprite voulu
        im = im.transform((tile_width, tile_height), Image.EXTENT, (tile_width * idx_x, tile_height * idx_y, tile_width * (idx_x + 1), tile_height * (idx_y + 1)))

        # transforme le sprite si besoin
        if modif == FLIP_LEFT_RIGHT:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        elif modif == FLIP_TOP_BOTTOM:
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        elif modif == ROTATE_90:
            im = im.transpose(Image.ROTATE_90)
        elif modif == ROTATE_180:
            im = im.transpose(Image.ROTATE_180)
        elif modif == ROTATE_270:
            im = im.transpose(Image.ROTATE_270)

        # mise a l'echelle si besoin
        if final_width:
            im.thumbnail((final_width, final_height))

        # retourne l'image (en fait un widget label)
        imp = ImageTk.PhotoImage(im)
        return im, imp
    else:
        if sys.version_info >= (3,):
            __erreur("[image] module Pillow non charge")
        else:
            __erreur("[image] module PIL non charge")
        return None

##### tourner une image
def image_rotate(pim, pid, pangle):
    """
    rotation *absolue* de l'image pid de pangle (en *degres*)
    cette transformation passe par PIL d'ou la necessite du parametre pim.
    Effet de bord : si l'image etait cachee, elle est a nouveau visible.
    """
    if pangle < 0:
        pangle += 360
    # mise a jour : transformation de l'image
    im = pim[0].rotate(pangle) # angle doit etre positif
    pim[1] = ImageTk.PhotoImage(im)
    # antecedent : on doit toujours avoir une image
    x, y = canv.coords(pid)
    canv.delete(pid)
    # nouvelle image de l'avion en lieu et place de l'ancienne
    id = canv.create_image(x, y, image=pim[1], anchor='center')
    return id

##### dilater ou reduire une image (sans deformation)
def image_scale(pim, pid, pfacteur):
    """
    agrandissement (pfacteur > 1) ou reduction (pfacteur < 1) d'une image.
    Effet de bord : si l'image etait cachee, elle est a nouveau visible.
    """
    l, h = pim[0].size
    width, height = int(l*pfacteur), int(h*pfacteur)
    im = pim[0].resize((width, height), Image.ANTIALIAS)
    pim[1] = ImageTk.PhotoImage(im)
    # antecedent : on doit toujours avoir une image
    x, y = canv.coords(pid)
    canv.delete(pid)
    # nouvelle image de l'avion en lieu et place de l'ancienne
    id = canv.create_image(x, y, image=pim[1], anchor='center')
    return id

##### homothetie + rotation : comme on ne modifie jamais l'image d'origine
#     on doit faire appel a une fonction particuliere
def image_transformation(pim, pid, pangle, pfacteur):
    """
    agrandissement (pfacteur > 1) ou reduction (pfacteur < 1) d'une image
    associe a une rotation d'angle pangle (en *degres*).
    Effet de bord : si l'image etait cachee, elle est a nouveau visible.
    """
    # homothetie
    l, h = pim[0].size
    width, height = int(l*pfacteur), int(h*pfacteur)
    im = pim[0].resize((width, height), Image.ANTIALIAS)
    # rotation
    if pangle < 0:
        pangle += 360
    im = im.rotate(pangle) # angle doit etre positif
    # mise a jour : transformation de l'image
    pim[1] = ImageTk.PhotoImage(im)
    # antecedent : on doit toujours avoir une image
    x, y = canv.coords(pid)
    canv.delete(pid)
    # nouvelle image de l'avion en lieu et place de l'ancienne
    id = canv.create_image(x, y, image=pim[1], anchor='center')
    return id

##### retour de la valeur d'un pixel d'une image
def get_pixel(pim, px, py):
    """
    retour de la valeur d'un pixel d'une image dont la reference est
    passee en parametre
    """
    return pim[1].getpixel((px, py))


###############################################################
###############################################################
# test unitaire
# la condition permet que les lignes suivantes ne soient pas executees si
# le script est importe en tant que module
im1 = 1
tim_mago = [-1 for i in range(10)]

#####
def __aide():
    current_color('green')
    rectangle(20, 600-20, 250, 600-130)
    line(20, 600-40, 250, 600-40)
    current_color('black')
    text(30, 600-40, "AIDE")
    text(30, 600-60, "touche a : aide")
    text(30, 600-80, "touche z : trace les objets")
    text(30, 600-100, "touche e : efface l'ecran")
    text(30, 600-120, "bouton gauche : ")

#####
def init_animation():
    global tim_mago
    # animation par sprites
    y = 5.16
    for i in range(4):
        tim_mago[i] = image_from_tiles('mago.png', 60, 60, 5, y)
        y += 1

def animation():
    for i in range(4):
        id = image_draw(540, 240, tim_mago[i])
        refresh()
        sleep(0.2)
        obj_delete(id)

    id = image_draw(540, 240, tim_mago[0])
    refresh()
    sleep(0.2)
    obj_delete(id)
    id = image_draw(540, 240, tim_mago[1])
    refresh()
    sleep(0.2)
    obj_delete(id)
    id = image_draw(540, 240, tim_mago[2])
    refresh()
    sleep(0.2)
    obj_delete(id)
    id = image_draw(540, 240, tim_mago[3])
    refresh()
    sleep(0.2)
    obj_delete(id)

#####
def __figures():
    global im1
    # couleurs arc en ciel de Newton + cyan, black - indigo
    lcoul = ('red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'black')
    # points
    current_color('red')
    for i in range(1,200):
        point(randint(30, 130), randint(300, 400))
    # segments
    current_color('blue')
    for i in range(1,10):
        line(randint(150, 250), randint(300, 400), randint(150, 250), randint(300, 400))
    # rectangles
    current_color('green')
    for i in range(1,10):
        rectangle(randint(270, 370), randint(300, 400), randint(270, 370), randint(300, 400), randint(1,5))
    # cercles
    current_color('black')
    for i in range(1,10):
        circle(randint(410, 470), randint(320, 380), randint(10, 30))
    # rectangles pleins
    for i in range(1,10):
        current_color(lcoul[randint(0,6)])
        box(randint(510, 610), randint(300, 400), randint(510, 610), randint(300, 400))
    # disques
    for i in range(1,10):
        current_color(lcoul[randint(0,6)])
        disc(randint(60, 100), randint(220, 260), randint(10, 30))
    # polygones
    current_color('black')
    polygon(150, 200, 250, 200, 200, 280) # triangle
    ll1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    angle = 90.0
    for i in range(5):
        ll1[i*2] = 30*cos(angle*pi/180.0) + 200
        ll1[i*2+1] = 30*sin(angle*pi/180.0) + 230
        angle += 72
    current_color('red')
    polygon(ll1) # pentagone
    # texte
    mot1, mot2, mot3 = 'dans', 'tous les', 'sens'
    current_color('black')
    y = 260
    for i in range(4):
        text(270, y, mot1[i])
        y -= 20
    x, y = 290, 190
    for i in range(8):
        text(x, y, mot2[i])
        x, y = x+7, y+9
    text(320, 190, mot3)
    # image
    im1 = image("ferme.png")
    image_draw(440, 240, im1)
    # animation
    init_animation()
    init_idle_func(animation)
    idle_func()

#####
def __clic1():
    x, y = get_mouse_x(), get_mouse_y()

#####
if __name__ == '__main__':
    from random import randint
    from math import cos, sin, pi
    from time import sleep

    init_window("cng : test unitaire",800,600)
    # mode "direct" (i.e image construite par programme)
    __aide()
    # mode "evenement" (i.e image construite par interaction)
    assoc_key('a', )
    assoc_key('z', __figures)
    assoc_key('e', clear_screen)
    assoc_button(1, __clic1)
    main_loop()

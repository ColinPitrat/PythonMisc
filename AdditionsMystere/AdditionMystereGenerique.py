mots_gauche = []
mots_droite = []
line=raw_input("Addition mystere a resoudre: ")
lettres = [ ]
lettres_non_zero = [ ]
valeurs_possibles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
valeurs = {}
progres = 1
# "Resolution" de l'indicateur de progression (lorsqu'on l'affiche): profondeur de l'arbre a laquelle on incremente le progres
resolution = 3
travail_total = 1

def lit_mot(chaine, liste_mots):
    liste_mots.append([])
    i = 0
    while i < len(chaine) and chaine[i].isalpha():
#        print("Chaine[%s] = %s" % (i, chaine[i]))
        liste_mots[-1].append(chaine[i])
        i += 1
    return chaine[i:]


def lit_addition(chaine):
    global mots_gauche, mots_droite
    while len(chaine) > 0:
        chaine = lit_mot(chaine, mots_gauche)
        if len(chaine) == 0:
            print("Je n'ai pas trouve le signe = dans l'addition !")
            return 1
        if chaine[0] == "+":
            chaine = chaine[1:]
        elif chaine[0] == "=":
            chaine = chaine[1:]
            break
        else:
            print("Je n'ai pas compris l'addition a ce caractere: '%s'" % chaine[0])
            return 1
    while len(chaine) > 0:
        chaine = lit_mot(chaine, mots_droite)
        if len(chaine) == 0:
            break
        elif chaine[0] == "+":
            chaine = chaine[1:]
        else:
            print("Je n'ai pas compris l'addition a ce caractere: '%s'" % chaine[0])
            return 1
    return 0

def construit_listes():
    global mots_gauche, mots_droite, lettres, lettres_non_zero
    for mot in mots_gauche + mots_droite:
        lettres_non_zero.append(mot[0])
        for lettre in mot:
            lettres.append(lettre)
    # Les listes ne doivent pas contenir deux fois la meme lettre
    lettres = list(set(lettres))
    lettres_non_zero = list(set(lettres_non_zero))
    # Nous voulons placer en debut de liste les lettres de poids faible:
    for l = range(max_len_mots, 0, -1):
        if len(mot) <= l:
            lettres.remove(mot[-l])
            lettres.insert(0, mot[-l])

lit_addition(line)
#print("Mots de gauche: %s - Mots de droite: %s" % (mots_gauche, mots_droite))
construit_listes()
#print("Lettres de l'addition: %s - Lettres non nulles: %s" % (lettres, lettres_non_zero))

for i in range(0, resolution):
    travail_total *= len(valeurs_possibles) - i

for l in lettres:
    valeurs[l] = None

def solution_valable():
    global mots_gauche, mots_droite, valeurs
    v_gauche = 0
    v_droite = 0
    for mot in mots_gauche:
        l = mot[-1]
        if valeurs[l] is None:
            return True
        v_gauche += valeurs[l]
    for mot in mots_droite:
        l = mot[-1]
        if valeurs[l] is None:
            return True
        v_droite += valeurs[l]
    return (v_gauche % 10) == (v_droite % 10)

def solution_valide():
    global mots_gauche, mots_droite, valeurs
    v_gauche = 0
    v_droite = 0
    for mot in mots_gauche:
#        print(" + %s" % mot)
        i = len(mot)-1
        for l in mot:
#            print("   _ %s" % (10**i*valeurs[l]))
            v_gauche += 10**i*valeurs[l]
            i -= 1
    for mot in mots_droite:
#        print(" = %s" % mot)
        i = len(mot)-1
        for l in mot:
#            print("   _ %s" % (10**i*valeurs[l]))
            v_droite += 10**i*valeurs[l]
            i -= 1
#    print("%s => %s == %s ?" % (valeurs, v_gauche, v_droite))
    return v_gauche == v_droite

def choisis_lettre(i):
    global resolution, progres, travail_total
    if i == resolution:
#        print("%s / %s" % (progres, travail_total))
        progres = progres + 1
    l = lettres[i]
    for v in valeurs_possibles:
        valeur_unique = True
        if v == 0 and l in lettres_non_zero:
            continue
        for v2 in valeurs.itervalues():
            if v == v2:
                valeur_unique = False
                break
        if not valeur_unique:
            continue
        if not solution_valable():
            continue
        valeurs[l] = v
        if i == len(lettres) - 1:
            if solution_valide():
                print(valeurs)
        else:
            choisis_lettre(i+1)
        valeurs[l] = None

choisis_lettre(0)

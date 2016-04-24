# send + more = money
lettres = [ "d", "e", "y", "s", "n", "m", "o", "r" ]
lettres_non_zero = [ "s", "m" ]
valeurs_possibles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
valeurs = {}
progres = 1
resolution = 3
travail_total = 1

for i in range(0, resolution):
    travail_total *= len(lettres) - i

for l in lettres:
    valeurs[l] = None

def solution_valable():
    # send + more = money
    if valeurs["d"] is not None and valeurs["e"] is not None and valeurs["y"] is not None:
        return ((valeurs["d"]+valeurs["e"])%10 == valeurs["y"])
    else:
        return True

def solution_valide():
    # send + more = money
    return 1000*valeurs["s"] + 100*valeurs["e"] + 10 * valeurs["n"] + valeurs["d"] + 1000*valeurs["m"] + 100*valeurs["o"] + 10*valeurs["r"] + valeurs["e"] == 10000*valeurs["m"] + 1000*valeurs["o"] + 100*valeurs["n"] + 10*valeurs["e"] + valeurs["y"]

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
        valeurs[l] = v
        if not solution_valable():
            valeurs[l] = None
            continue
        if i == len(lettres) - 1:
            if solution_valide():
                print(valeurs)
        else:
            choisis_lettre(i+1)
        valeurs[l] = None

choisis_lettre(0)

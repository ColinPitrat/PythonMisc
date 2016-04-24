# send + more = money
lettres = [ "d", "e", "y", "s", "n", "m", "o", "r" ]
lettres_non_zero = [ "s", "m" ]
# pleiade + poesies + de = ronsard
#lettres = [ "s", "e", "d", "p", "l", "i", "a", "o", "r", "n" ]
#lettres_non_zero = [ "p", "d", "r" ]
# du + poete + marot = epitre
#lettres = [ "d", "u", "p", "o", "e", "t", "m", "a", "r", "i" ]
#lettres_non_zero = [ "d", "p", "m", "e" ]
# maurois + et + mauriac = auteurs
#lettres = [ "m", "a", "u", "r", "o", "i", "s", "e", "t", "c" ]
#lettres_non_zero = [ "m", "e", "a" ]
# alberto + alberto = moravia
#lettres = [ "a", "l", "b", "e", "r", "t", "o", "m", "v", "i" ]
#lettres_non_zero = [ "a", "m" ]
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
    # pleiade + poesies + de = ronsard
    if valeurs["s"] is not None and valeurs["e"] is not None and valeurs["d"] is not None:
        return ((valeurs["s"]+2*valeurs["e"])%10 == valeurs["d"])
    else:
        return True

def solution_valide():
    # send + more = money
    return 1000*valeurs["s"] + 100*valeurs["e"] + 10 * valeurs["n"] + valeurs["d"] + 1000*valeurs["m"] + 100*valeurs["o"] + 10*valeurs["r"] + valeurs["e"] == 10000*valeurs["m"] + 1000*valeurs["o"] + 100*valeurs["n"] + 10*valeurs["e"] + valeurs["y"]
    # pleiade + poesies + de = ronsard
    return 1000000*valeurs["p"] + 100000*valeurs["l"] + 10000*valeurs["e"] + 1000*valeurs["i"] + 100*valeurs["a"] + 10*valeurs["d"] + valeurs["e"] + 1000000*valeurs["p"] + 100000*valeurs["o"] + 10000*valeurs["e"] + 1000*valeurs["s"] + 100*valeurs["i"] + 10*valeurs["e"] + valeurs["s"] + 10*valeurs["d"] + valeurs["e"] == 1000000*valeurs["r"] + 100000*valeurs["o"] + 10000*valeurs["n"] + 1000*valeurs["s"] + 100*valeurs["a"] + 10*valeurs["r"] + valeurs["d"]
    # du + poete + marot = epitre
    return 10*valeurs["d"] + valeurs["u"] + 10000*valeurs["p"] + 1000*valeurs["o"] + 100*valeurs["e"] + 10*valeurs["t"] + valeurs["e"] + 10000*valeurs["m"] + 1000*valeurs["a"] + 100*valeurs["r"] + 10*valeurs["o"] + valeurs["t"] == 100000*valeurs["e"] + 10000*valeurs["p"] + 1000*valeurs["i"] + 100*valeurs["t"] + 10*valeurs["r"] + valeurs["e"]
    # maurois + et + mauriac = auteurs
    return 1000000*valeurs["m"] + 100000*valeurs["a"] + 10000*valeurs["u"] + 1000*valeurs["r"] + 100*valeurs["o"] + 10*valeurs["i"] + valeurs["s"] + 10*valeurs["e"] + valeurs["t"] + 1000000*valeurs["m"] + 100000*valeurs["a"] + 10000*valeurs["u"] + 1000*valeurs["r"] + 100*valeurs["i"] + 10*valeurs["a"] + valeurs["c"]  == 1000000*valeurs["a"] + 100000*valeurs["u"] + 10000*valeurs["t"] + 1000*valeurs["e"] + 100*valeurs["u"] + 10*valeurs["r"] + valeurs["s"]
    # alberto + alberto = moravia
    return 2*(1000000*valeurs["a"] + 100000*valeurs["l"] + 10000*valeurs["b"] + 1000*valeurs["e"] + 100*valeurs["r"] + 10*valeurs["t"] + valeurs["o"]) == 1000000*valeurs["m"] + 100000*valeurs["o"] + 10000*valeurs["r"] + 1000*valeurs["a"] + 100*valeurs["v"] + 10*valeurs["i"] + valeurs["a"]

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

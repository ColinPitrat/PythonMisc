#!/usr/bin/python
import sys

"""Dans une equipe de basket de douze joueurs, la mesentente reigne.
Chaque joueur refuse de jouer avec les joueurs dont le maillot porte un numero immediatement inferieur ou immediatement superieur au sien.
Combien d'equipe de 5 joueurs acceptant de jouer est il possible de former ?

Une solution est de definir les combinaisons d'ecart 1, semblable aux combinaisons mais avec les lois suivantes:
 - C1_n_0 = 1
 - C1_n_1 = n
 - C1_n_n = 0 si n > 1, 1 si n = 0 ou n = 1
 - C1_n_p = C1_n-1_p + C1_n-2_p-1 
En effet, une combinaison de p joueurs parmi les n peut etre:
 - soit une combinaison de p parmi les n-1 premiers
 - soit une combinaison comprenant le neme joueur et ne comportant donc pas le n-1eme, completee de p-1 joueurs pris parmis les n-2 premiers

Une autre facon de voir le probleme est de prendre 7 elements (representant les joueurs ne participant pas) et de choisir une des facons de placer 5 elements entre (certains emplacement pouvant etre laisses vides).
Il y a 8 emplacements, donc C_8_5 choix possibles.

Plus generalement, C1_n_p = C_(n-p+1)_p

Encore plus generalement, pour un ecart de k entre chaque element, on peut definir:
 - Ck_n_0 = 1
 - Ck_n_1 = n
 - Ck_n_n = 0 si n > 1, 1 si n = 0 ou n = 1
 - Ck_n_p = Ck_n-1_p + Ck_n-1-k_p-1 

"""

def combik_intern(k, n, p):
    if p == 0:
        return 1
    if p == 1:
        return n
    if n == p:
        return 0
    if n <= 0:
        return 0
    return combik_intern(k, n-1, p) + combik_intern(k, n-1-k, p-1)

def combik(k, n, p):
    if n < 0 or p < 0 or p > n:
        return None
    if not type(n) == int or not type(p) == int or not type(k) == int:
        raise ValueError
    return combik_intern(k, n, p)

def combi1_intern(n, p):
    if p == 0:
        return 1
    if p == 1:
        return n
    if n == p:
        return 0
    return combi1_intern(n-1, p) + combi1_intern(n-2, p-1)

def combi1(n, p):
    if n < 0 or p < 0 or p > n:
        return None
    if not type(n) == int or not type(p) == int:
        raise ValueError
    return combi1_intern(n, p)

def combi_intern(n, p):
    if p == 0 or n == p:
        return 1
    if p == 1:
        return n
    return combi_intern(n-1, p) + combi_intern(n-1, p-1)

def combi(n, p):
    if n < 0 or p < 0 or p > n:
        return None
    if not type(n) == int or not type(p) == int:
        raise ValueError
    return combi_intern(n, p)

n = int(sys.argv[1])
p = int(sys.argv[2])
k = 1
if len(sys.argv) >= 4:
    k = int(sys.argv[3])
print("C1_%s_%s = %s" , (n, p, combi1(n, p)))
print("C_%s_%s = %s" , (n-p+1, p, combi(n-p+1, p)))
print("C%s_%s_%s = %s" , (k, n, p, combik(k, n, p)))

largeur = 98
hauteur = 18

lettre_courante = 'a'
carre = []
carre2 = []
for j in range(0, hauteur):
    carre.append([])
    carre2.append([])
    for i in range(0, largeur):
        carre[j].append(lettre_courante)
        carre2[j].append(lettre_courante)
        if lettre_courante == 'z':
            lettre_courante = 'a'
        else:
            lettre_courante = chr(ord(lettre_courante) + 1)

lettre_courante = 'a'
nb_communs = 0
for i in range(0, largeur):
    for j in range(0, hauteur):
        carre2[j][i] = lettre_courante
        if lettre_courante == carre[j][i]:
            print("%s,%s: %s" % (j,i,lettre_courante))
            nb_communs += 1
        if lettre_courante == 'z':
            lettre_courante = 'a'
        else:
            lettre_courante = chr(ord(lettre_courante) + 1)

for j in range(0, hauteur):
    for i in range(0, largeur):
        print(carre[j][i]),
    print("")
print( "=="*98)
for j in range(0, hauteur):
    for i in range(0, largeur):
        print(carre2[j][i]),
    print("")

print("Solution: %s" % nb_communs)

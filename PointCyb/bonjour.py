#age = int(input("Quel age as tu ? "))
# On ne veut pas qu'un mineur accede a cette partie
#if age >= 18:
#    print("Bienvenue !")
#elif age == 7:
#    print("Tu as l'age de raison !")
#print(age)

reponse = "" # Contiendra la reponse de l'utilisateur
while reponse != "oui":
    reponse = input("Ai-je raison ? ")

if reponse == "oui":
    print("Je le savais bien !")



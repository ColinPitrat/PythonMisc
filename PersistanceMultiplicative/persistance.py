# -*- coding: utf-8 -*-

# La suite multiplicative d'un nombre est la suite de nombres qu'on obtient en
# multipliant les chiffres de ce nombre et en réitérant sur le résultat. Par
# exemple 1729: 1*7*2*9 = 126, 1*2*6 = 12, 1*2 = 2.
# La suite multiplicative de 1729 est donc: 1729, 126, 12, 2
#
# La persistance multiplicative d'un nombre est le nombre de fois qu'il a fallu
# répéter l'opération pour aboutir à un point fixe (un nombre d'un seul
# chiffre). Pour 1729, p = 3 (il a fallu appliquer l'opération 3 fois).
#
# Bien sûr, la suite et la persistence dépendent de la base dans laquelle on
# écrit le nombre.

# La version recursive ne peut pas gerer des nombres trop grands (RuntimeError: maximum recursion depth exceeded)
def __entier_en_base_interne_recursive(num, b, numerals):
   return ((num == 0) and numerals[0]) or (__entier_en_base_interne(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def __entier_en_base_interne(num, b, numerals):
   result = ""
   while num > 0:
      result = numerals[num % b] + result
      num = num // b
   return result


def entier_en_base(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
   if num > 0:
      return __entier_en_base_interne(num, b, numerals)
   if num < 0:
      return "-" + __entier_en_base_interne(-num, b, numerals)
   return "0"

def produit_chiffres(num, base):
   if not isinstance(num, int) and not isinstance(num, long):
      raise TypeError
   if num < 0:
      raise ValueError
   if num == 0:
      return 0
   result = 1
   while num > 0:
      digit = num % base
      result *= digit
      num = num // base
   return result

def persistance_et_point_final(num, base):
   n = 0
   while num >= base:
      n += 1
      num = produit_chiffres(num, base)
   return (n, num)

def persistance(num, base):
   (p, f) = persistance_et_point_final(num, base)
   return p

def repartitions_point_final(max_num, base):
   result = {}
   for num in xrange(0, max_num):
      (p, pf) = persistance_et_point_final(num, base)
      if pf in result:
         result[pf] += 1
      else:
         result[pf] = 1
   return result

# Ne fonctionnne qu'en base <= 10
def genere_nombre(chiffres, repetitions, base):
   result = 0
   for c, r in zip(chiffres, repetitions):
      for i in range(0, r):
         result *= base
         result += c
   return result

def genere_candidats(chiffres):
   opt1 = [2, 3, 7]
   opt2 = [3, 5, 7]
   while True:
      for i in range(0, chiffres+1):
         for j in range(0, chiffres-i+1):
            yield genere_nombre(opt1, [chiffres-i-j, j, i], 10)
            # Pour ne pas generer deux fois les combinaisons de 3 et 7
            if j != 0:
               yield genere_nombre(opt2, [chiffres-i-j, j, i], 10)
      chiffres += 1
      print("Recherche parmi les nombres avec %s chiffres" % chiffres)

def histogramme_repartition_point_finaux(max_puiss, base):
   print("Repartiton des nombres par point final en base %s:" % base)
   heading = ""
   for k in range(0, base):
      heading += "%011s " % k
   print("                %s" % heading)
   for n in range(1, max_puiss + 1):
      histo = repartitions_point_final(10**n, base)
      line  = "Entre 1 et 10^%02s" % n
      line2 = "                "
      total = 0
      for k in range(0, base):
         if k in histo:
            total += histo[k]
      for k in range(0, base):
         r = 0
         if k in histo:
            r = histo[k]
         line += "%011s " % r
         line2 += "%010s%% " % (100*r/total)
      print("")
      print(line)
      print(line2)

def premier_nombre_par_persistance(max_num, base):
   min_persistance = -1
   print("Premier nombre de persistance multiplicative donnee en base %s" % base)
   for num in xrange(0, max_num+1):
      (p, pf) = persistance_et_point_final(num, base)
      if p > min_persistance:
         min_persistance = p
         print("%s: %s (%s) - point final = %s" % (p, entier_en_base(num, base), num, pf))

# Ne fonctionne qu'en base == 10 a cause du generateur
def cherche_nombre_de_persistance_elevee(min_chiffres):
   min_persistance = -1
   base = 10
   print("Un nombre de persistance multiplicative donnee en base %s" % base)
   for num in genere_candidats(min_chiffres):
      (p, pf) = persistance_et_point_final(num, base)
      if p > min_persistance:
         min_persistance = p
         print("%s: %s (%s) - point final = %s" % (p, entier_en_base(num, base), num, pf))

def main():
   cherche_nombre_de_persistance_elevee(10000);
   #for base in range(2, 36):
   #   premier_nombre_par_persistance(1000000, base)
   #   histogramme_repartition_point_finaux(5, base)

if __name__ == '__main__':
   main()

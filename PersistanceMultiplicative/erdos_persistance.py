optim = False
produit = []
max_chunk = 10000000

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

def precalcul_produits():
   global produit, max_chunk, optim
   produit = []
   for i in range(0, max_chunk):
      produit.append(produit_chiffres(i, 10))
   optim = True

def produit_chiffres_base10(num):
   global produit, max_chunk
   result = 1
   while num > 0:
      digit = num % max_chunk
      result *= produit[digit]
      num = num // max_chunk
   return result

def produit_chiffres(num, base):
   global optim
   if not isinstance(num, int) and not isinstance(num, long):
      raise TypeError
   if num < 0:
      raise ValueError
   if num == 0:
      return 0
   if optim and base == 10:
      return produit_chiffres_base10(num)
   result = 1
   while num > 0:
      digit = num % base
      # Quitte a tester, autant aussi eviter de multiplier par 1
      if digit > 1:
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
      while r > 0:
         result *= base
         if c == 2:
            if r > 3:
               result += 8
               r -= 3
            elif r == 2:
               result += 4
               r -= 2
            else:
               result += 2
               r -= 1
         elif c == 3:
            if r > 2:
               result += 9
               r -= 2
            else:
               result += 3
               r -= 1
         else:
            result += c
            r -= 1
   return result

def genere_candidats(chiffres):
   opt = [2, 3, 5, 7]
   while True:
      for i in range(0, chiffres+1):
         for j in range(0, chiffres-i+1):
            for k in range(0, chiffres-i-j+1):
               yield genere_nombre(opt, [chiffres-i-j-k, k, j, i], 10)
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
         #print("%s: %s (%s) - point final = %s" % (p, entier_en_base(num, base), num, pf))
         print("%s: %s - point final = %s" % (p, num, pf))

def main():
   #for base in range(2, 36):
   #   premier_nombre_par_persistance(1000000, base)
   #   histogramme_repartition_point_finaux(5, base)
   #histogramme_repartition_point_finaux(10, 10)
   cherche_nombre_de_persistance_elevee(500000);

if __name__ == '__main__':
   precalcul_produits()

   # Profiling
   import cProfile, pstats, StringIO
   pr = cProfile.Profile()
   pr.enable()

   main()

   # Profiling
   pr.disable()
   s = StringIO.StringIO()
   sortby = 'cumulative'
   ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
   ps.print_stats()
   print s.getvalue()

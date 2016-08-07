import time

# TODO: test this method
def intInBase(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (intInBase(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def reverse(num, base):
   if not isinstance(num, int) and not isinstance(num, long):
      raise TypeError
   if num < 0:
      raise ValueError
   result = 0
   while num > 0:
      result *= base
      digit = num % base
      num = num // base
      result += digit
   return result

def palindrome(num, base):
   return reverse(num, base) == num;

def lychrel_step(num, base):
   return num + reverse(num, base)

def lychrel_loop(num, base):
   result = [num]
   while not palindrome(num, base):
      num = lychrel_step(num, base)
      result.append(num)
   return result

def lychrel_num(num, base):
   result = 0
   rev = reverse(num, base)
   while rev != num:
      result += 1
      num += rev
      rev = reverse(num, base)
   return result

def lychrel_candidate(num, max_steps, base):
   steps = 0
   rev = reverse(num, base)
   while rev != num and steps < max_steps:
      steps += 1
      num += rev
      rev = reverse(num, base)
   return steps == max_steps

# TODO: test this method
def find_candidates(max_num, max_steps, base):
   result = []
   for num in range(0, max_num):
      if lychrel_candidate(num, max_steps, base):
         result.append(num)
   return result

def old_main():
   n = 0
   base = 2
   max_steps = 1000
   #print("\033[2J")
   #print("\033[1;0HSearching for Lychrel number candidates in base %s in %s steps:" % (base, max_steps));
   l = 2
   #while True:
   for b in range(0, 1000):
      #print("\033[%s;0H%s" % (l, intInBase(n, base)))
      if lychrel_candidate(n, max_steps, base):
         print(n)
         l += 1
      n += 1

def main():
   max_steps = 1000
   max_num = 10000
   print("Searching for Lychrel number candidates per base in %s steps between 0 and %s:" % (max_steps, max_num));
   for base in range(2, 36):
      candidates = find_candidates(max_num, max_steps, base)
      print("%s: %s" % (base, len(candidates)))

if __name__ == '__main__':
   main()

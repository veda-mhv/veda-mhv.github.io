# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

import sys
import math
from random import Random

# ---------------------------------------------------------------------------------------

MAX_INITPOINT_TRIALS = 1000000
MAX_CANDIDATE_TRIALS = 25
MAX_SEARCH_DEPTH     = 500

Graphics_Available = 1
try: import Gnuplot
except: Graphics_Available = 0

# ---------------------------------------------------------------------------------------
# Converts an integer into a "n" binary digits list, using the H2B table
# ---------------------------------------------------------------------------------------

H2B = { '0': "0000", '1': "0001", '2': "0010", '3': "0011",
        '4': "0100", '5': "0101", '6': "0110", '7': "0111",
        '8': "1000", '9': "1001", 'a': "1010", 'b': "1011",
        'c': "1100", 'd': "1101", 'e': "1110", 'f': "1111"
      }

def int2bin(x, n):
   out = ""
   for digit in hex(x)[2:]: out += H2B[digit]
   d = n - len(out)
   if d >= 0: out = list('0'*d + out)
   else:      out = list(out[-d:])
   return map(int, out)

# ---------------------------------------------------------------------------------------
# Prints a tuple (x, fx), where x is a list of real numbers, fx a real number
# ---------------------------------------------------------------------------------------

def point_to_string(P):
   out = "--> value      = %f\n" % P[1]
   for i in range(len(P[0])):
      out = out + "--> coord[%3d] = %f\n" % (i, P[0][i])

   return out

# ---------------------------------------------------------------------------------------
# Defines a simple, general-purpose optimizer class
# ---------------------------------------------------------------------------------------

class SimpleOpt:

   def __init__(self, problem, max_steps, step_size, max_search_depth, user_wants_backtracking, user_wants_graphics):
      self.problem = problem
      self.max_steps = max_steps
      self.step_size = step_size
      self.max_search_depth = max(1, min(max_search_depth, MAX_SEARCH_DEPTH))
      self.search_depth = 0
      self.rnd = Random()
      self.abs_best = None
      self.crt_best = None
      self.backtrack = []
      self.toplot = []
      self.logfd = None
      self.use_backtracking = user_wants_backtracking
      self.use_graphics = Graphics_Available and user_wants_graphics

      if self.use_graphics:
         self.g = Gnuplot.Gnuplot()
         self.g.title("Best solution vs. iteration")
         self.g("set data style linespoints")

# ---------------------------------------------------------------------------------------

   def reset(self):
      self.search_depth = 0
      self.abs_best = None
      self.crt_best = None
      self.backtrack = []
      self.toplot = []
      if self.use_graphics: self.g.reset()

# ---------------------------------------------------------------------------------------

   def boxcorners(self):
      n_dimensions = self.problem.dimension
      n_corners = 2 ** n_dimensions
      bounds = self.problem.bounds

      corners = []
      for i in range(n_corners):
         mask = int2bin(i, n_dimensions)
         x = []
         for i in range(n_dimensions): x.append(bounds[i][mask[i]])
         corners.append(x)

      return corners

# ---------------------------------------------------------------------------------------

   def in_box(self, x):
      nr_coords = self.problem.dimension
      bounds = self.problem.bounds

      for i in range(nr_coords):
         if x[i] < bounds[i][0] or x[i] > bounds[i][1]: return 0

      return 1

# ---------------------------------------------------------------------------------------

   def in_constraints(self, x):
      for i in range(self.problem.n_constraints):
         if self.problem.constraint(i, x) > 0: return 0

      return 1

# ---------------------------------------------------------------------------------------

   def allowed(self, x):
      # Test if the point x belongs to the problem "box"
      if not self.in_box(x): return 0

      # Ok, now test if it satisfies the constraints
      if not self.in_constraints(x): return 0

      # All tests passed.
      return 1

# ---------------------------------------------------------------------------------------

   def seedpoint(self):
      n_dimensions = self.problem.dimension
      bounds = self.problem.bounds

      for tries in range(MAX_INITPOINT_TRIALS):
         x = []
         for i in range(n_dimensions):
            x.append(self.rnd.uniform(bounds[i][0], bounds[i][1]))

         if self.allowed(x): return x

      return []

# ---------------------------------------------------------------------------------------

   def startpoint(self, seed, corner):
      n_dimensions = self.problem.dimension
      bounds = self.problem.bounds

      t = 0
      while t < 1:
         z = []
         for i in range(n_dimensions):
            z.append((1.0 - t) * corner[i] + t * seed[i])
         if self.in_constraints(z): return z
         t += 0.0001

      return []

# ---------------------------------------------------------------------------------------

   def get_candidates(self, x):
      nr_coords = len(x)
      crtx = self.crt_best[0]

      candidates = []
      while len(candidates) == 0:
         for tries in range(MAX_CANDIDATE_TRIALS):
            newx = list(x)
            for i in range(nr_coords):
               newx[i] = self.rnd.uniform(x[i] - self.step_size, x[i] + self.step_size)
            if (newx != crtx) and self.allowed(newx):
               candidates.append((newx, self.problem.of(newx)))

      return candidates   # list of tuples: (x, f(x))

# ---------------------------------------------------------------------------------------

   def better(self, x, y):   # true if x better than y (i.e. f(x) >= f(y))
      return x[1] >= y[1]

# ---------------------------------------------------------------------------------------

   def compare(self, x, y):
      if x[1] > y[1]: return 1
      elif x[1] < y[1]: return -1
      else: return 0

# ---------------------------------------------------------------------------------------

   def get_best_candidates(self, candidates):
      candidates.sort(self.compare)
      candidates.reverse()

      best = []
      for candidate in candidates:
         if self.better(candidate, self.crt_best):
            best.append(candidate)
         else: break

      return best

# ---------------------------------------------------------------------------------------

   def onesearch(self, x):
      candidates = self.get_candidates(x[0])              # list of tuples (x, f(x))
      maybe_next = self.get_best_candidates(candidates)   # list of tuples (x, f(x))

      if len(maybe_next) > 0:
         self.crt_best = maybe_next[0]
         if self.use_backtracking: self.backtrack += maybe_next[1:]

         if self.better(self.crt_best, self.abs_best):
            self.abs_best = self.crt_best
            self.toplot.append(self.abs_best[1])   # keep only its function value, f(x)
            return "abs_success"

         return "success"

      if self.search_depth == self.max_search_depth: return "fail"
      self.search_depth += 1

      for candidate in candidates:
         result = self.onesearch(candidate)
         if result != "fail": return result

      return "fail"

# ---------------------------------------------------------------------------------------

   def logged_print(self, text):
      if self.logfd == None:
         self.logfd = open(self.problem.name + ".log", "w")
      else:
         self.logfd = open(self.problem.name + ".log", "a")

      print text
      self.logfd.write(text + '\n')

      self.logfd.close()


# ---------------------------------------------------------------------------------------

   def optsearch(self):
      self.logged_print("")
      self.logged_print("SIMPLEOPT search process started.")
      self.logged_print("-" * 75)
      self.logged_print("")
      self.logged_print("Choosing a starting point. Please wait...")
      self.logged_print("")

      # Try to select a suitable starting point (the "initial best")

      if self.problem.seedpoint == None:
         seed = self.seedpoint()
         if len(seed) == 0:
            self.logged_print("Cannot find a suitable starting point!\nPlease, run SIMPLEOPT again.")
            return
      else:
         seed = self.problem.seedpoint
         if not self.allowed(seed):
            self.logged_print("The given seed point is out of problem space!\nCan run SIMPLEOPT again with an acceptable seed point.")
            return

      corners = self.boxcorners()

      for c in corners:
         self.logged_print("Search process (re)started.")
         print "(Can use Ctrl+C to interrupt it)..."
         self.logged_print("")

         x = self.startpoint(seed, c)
         if len(x) == 0: continue

         fx = self.problem.of(x)
         self.abs_best = self.crt_best = (x, fx)
         self.toplot.append(fx)

         self.logged_print("Initial best:")
         self.logged_print(point_to_string(self.crt_best))

         # Search (again) for an optimum point

         try:
            i = 1
            while i < self.max_steps:
               self.search_depth = 0
               result = self.onesearch(self.crt_best)

               if result == "fail":
                  if self.use_backtracking:
                     if len(self.backtrack) == 0: break
                     self.crt_best = self.backtrack[len(self.backtrack) - 1]
                     self.backtrack = self.backtrack[:-1]
                  else: break

               if result == "abs_success": i += 1

               print " " * 79 + "\r",   # clean up the "statistics" line
               print "Step: %6d\tDepth: %3d\tBack: %5d\tBest: %12.6f" % (i, self.search_depth, len(self.backtrack), self.abs_best[1]) + "\r",
               sys.stdout.flush()
         except: pass

         print " " * 79 + "\r",   # clean up the "statistics" line

         # Plot the graph of the objective function value versus iteration number

         if self.use_graphics:
            self.g.plot(zip(range(len(self.toplot)), self.toplot))
            raw_input('Press <Enter> to continue...\n')

         # Show what we found

         self.logged_print("Final best:")
         self.logged_print(point_to_string(self.abs_best))
         self.logged_print("Found in %d iteration(s) of %d allowed.\n" % (i, self.max_steps))

         if c == corners[len(corners) - 1]: break

         option = raw_input("Interrupt the search process? (y/n) ")
         if option == 'y' or option == 'Y': break
         print

         self.reset()

      self.logged_print("-" * 75)
      self.logged_print("")
      self.logged_print("SIMPLEOPT search process finished.\nThanks for your patience.")
      self.logged_print("")

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

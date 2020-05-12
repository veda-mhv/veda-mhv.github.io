# ---------------------------------------------------------------------------------------
# SimpleOpt's Problem module - (c) 2003 Dan Mugurel Ontanu & Mihnea Horia Vrejoiu
#      *** This is the Python 3.x version - (c) 2020 Mihnea Horia Vrejoiu ***
# ---------------------------------------------------------------------------------------

import sys
from random import Random

# ---------------------------------------------------------------------------------------

MAX_U_POINTS = 1000

# ---------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------

class Problem:

   def __init__(self, name, dimension, n_constraints, bounds, myof, myconstraint, seedpoint = None):
      self.name = name
      self.dimension = dimension
      self.n_constraints = n_constraints
      self.bounds = bounds   # list of tuples, (ximin, ximax) for 0<=i<input_size
      self.of = myof
      self.constraint = myconstraint
      self.seedpoint = seedpoint

   # Returns a real number representing the value of the function to
   # be maximized, given a vector of real numbers as input

   def of(self, x):
      pass

   # Evaluates the constraint ci on given input x

   def constraint(self, ci, x):
      pass

# ---------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------

class EU_Problem:

   def __init__(self, name, dimension, n_constraints, abounds, ubounds, myutility, myPDF, myconstraint, seedpoint = None):
      self.name = name
      self.dimension = dimension
      self.n_constraints = n_constraints
      self.bounds = abounds
      self.ubounds = ubounds
      self.utility = myutility
      self.PDF = myPDF
      self.constraint = myconstraint
      self.seedpoint = seedpoint
      self.rnd = Random()

      # We tabulate the utility function, retaining all the pairs (x, u(x))
      # in the list U

      print("")
      print("EU_Problem initialization:")
      print("Tabulating the utility function (over %d points)... " % (MAX_U_POINTS), end = '')
      sys.stdout.flush()

      self.U = []
      for tries in range(MAX_U_POINTS):
         x = []
         for i in range(len(self.ubounds)):
            x.append(self.rnd.uniform(ubounds[i][0], ubounds[i][1]))
         self.U.append((x, self.utility(x)))

      print("done.\n")
      sys.stdout.flush()

   # Stub for the utility function

   def utility(self, x):
      pass

   # Stub for the probability density function (PDF) which returns the
   # probability of x, given the "action" a

   def PDF(self, x, a):
      pass

   # Evaluates the constraint ci on a given "action" a

   def constraint(self, ci, a):
      pass

   # Returns a real number representing the value of the function to
   # be maximized, given a vector of real numbers as input (an "action",
   # in this case)

   def of(self, a):
      sum = 0
      for i in range(len(self.U)):
         sum += self.U[i][1] * self.PDF(self.U[i][0], a)
      return sum

# ---------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------

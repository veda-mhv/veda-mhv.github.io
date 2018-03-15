# ---------------------------------------------------------------------------------------
# Mandatory imports:
#    - problem definition class
#    - simple, general-purpose optimizer class
# ---------------------------------------------------------------------------------------

from problem import *
from simpleopt import SimpleOpt

# ---------------------------------------------------------------------------------------
# Auxiliary imports
# ---------------------------------------------------------------------------------------

import math
#import Numeric   # needed for plotting purposes
#import Gnuplot   # needed for plotting purposes

# ---------------------------------------------------------------------------------------
# Auxiliary data and function definitions
# ---------------------------------------------------------------------------------------

# For the "humps"

p      = [(1, 6), (0, 3), (2, 1), (3, 3), (5, 5), (6, 4), (6, 2)]
alfa   = [2, 2, 2, 2, 2, 2, 2]
beta   = [1, 1, 1, 1, 1, 1, 1]

# For the "action" constraints

center = (6, 6)
radius = 3

# ---------------------------------------------------------------------------------------

def dist(x, y):
   return math.sqrt((x[0] - y[0])*(x[0] - y[0]) + (x[1] - y[1])*(x[1] - y[1]))

# ---------------------------------------------------------------------------------------

def hump(i, x):
   return beta[i] * math.exp(-dist(p[i], x) / alfa[i])

# ---------------------------------------------------------------------------------------
# Domain of definition for the utility function:
# a list of bounds on each coordinate, in the form (xmin, xmax)
# ---------------------------------------------------------------------------------------

my_u_bounds = [(0, 8), (0, 8)]

# ---------------------------------------------------------------------------------------
# Procedural definition of the utility function u(x)
# ---------------------------------------------------------------------------------------

def myutility(x):
   sum = 0
   for i in range(len(p)): sum += hump(i, x)
   return sum

# ---------------------------------------------------------------------------------------
# Specification of the "action" space:
# a hyperbox, defined as a list of bounds on each coordinate, in the form (xmin, xmax)
# ---------------------------------------------------------------------------------------

my_a_bounds = [(0, 8), (0, 8)]   # the same as the u(x) domain (just in this example :-)

# ---------------------------------------------------------------------------------------
# Procedural definition of the set of constraints gi for the "actions" space
# ---------------------------------------------------------------------------------------
# NOTE: Each i personalizes a constraint function gi. For a given i (that is, a given
# constraint, myconstraint(i, x) must return a value <= 0 if the constraint is
# satisfied, and > 0 if not
# ---------------------------------------------------------------------------------------

# Two disconnected constraint regions

def myconstraint(i, a):
   if i == 0: return dist(a, center) - radius   # circular
   if i == 1: return a[0] + a[1] - 11.8         # linear
   return 1   # no other index allowed

# One constraint region, problem space made of two disconnected regions

#def myconstraint(i, a):
#   if i == 0:
#      if dist(a, center) - radius < 0 and a[0] + a[1] - 11.8 < 0: return 1
#      else: return -1
#   return 1

# ---------------------------------------------------------------------------------------
# Procedural definition of the probability distribution function PDF(x, a)
# ---------------------------------------------------------------------------------------
# It should be defined over the utility function domain, and personalised by
# a given "action"
# ---------------------------------------------------------------------------------------

def myPDF(x, a):
   # A unitary hump, centered at a given "action" a
   d = dist(x, a)
   return math.exp(-(d*d / 0.01))

# ---------------------------------------------------------------------------------------
# Program starting point
# ---------------------------------------------------------------------------------------

if __name__ == "__main__":

   # Specify your optimization problem here, getting an instance of it.
   # Parameters:
   #    - problem name
   #    - dimension of the input space
   #    - number of constraints
   #    - list of bounds
   #    - objective function
   #    - constraints function
   #    - desired starting point reference (optional list of coordinates)

   myproblem = EU_Problem("eu_func2d", 2, 2, my_a_bounds, my_u_bounds, myutility, myPDF, myconstraint)

   # Create a personalized instance of the optimizer, by specifying:
   #    - the problem
   #    - maximum number of steps for the search process
   #    - minimum search step size (the search process resolution)
   #    - maximum search depth (from 1 to 500)
   #    - whether to use backtracking (1), or not (0)
   #    - whether to use graphics (1), or not (0)

   so = SimpleOpt(myproblem, 100000, 0.1, 5, 0, 0)

   # Start the optimizer

   so.optsearch()

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


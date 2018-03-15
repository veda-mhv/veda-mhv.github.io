# ---------------------------------------------------------------------------------------
# Mandatory imports:
#    - problem definition class
#    - simple, general-purpose optimizer class
# ---------------------------------------------------------------------------------------

from problem import Problem
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

p      = [(1, 6), (0, 3), (2, 1), (3, 3), (5, 5), (6, 4), (6, 2)]
alfa   = [2, 2, 2, 2, 2, 2, 2]
beta   = [1, 1, 1, 1, 1, 1, 1]
center = (4, 4)
radius = 3

def dist(x, y):
   return math.sqrt((x[0] - y[0])*(x[0] - y[0]) + (x[1] - y[1])*(x[1] - y[1]))

def hump(i, x):
   return beta[i] * math.exp(-dist(p[i], x) / alfa[i])

# ---------------------------------------------------------------------------------------
# Specification of the problem space:
# list of bounds on each coordinate, in the form (xmin, xmax)
# ---------------------------------------------------------------------------------------

mybounds = [(0, 8), (0, 8)]

# ---------------------------------------------------------------------------------------
# Procedural definition of the objective function f
# ---------------------------------------------------------------------------------------

def myeval(x):
   sum = 0
   for i in range(len(p)): sum += hump(i, x)
   return sum

# ---------------------------------------------------------------------------------------
# Procedural definition of the set of constraints gi
# ---------------------------------------------------------------------------------------
# NOTE: Each i personalizes a constraint function gi. For a given i (that is, a given
# constraint, myconstraint(i, x) must return a value < 0 if the constraint is
# satisfied, and > 0 if not
# ---------------------------------------------------------------------------------------

def myconstraint(i, x):
   return dist(x, center) - radius

# ---------------------------------------------------------------------------------------
# Program starting point
# ---------------------------------------------------------------------------------------

if __name__ == "__main__":

   # Here can be drawn a graph of the objective function
   # < ... (insert appropriate code) ... >

#  x = []
#  y = []
#  for i in range(16):
#     x.append(i/2.0)
#     y.append(i/2.0)

#  m = []
#  for i in range(16):
#     m.append([])
#     for j in range(16):
#        m[i].append(myeval((x[i], y[j])))

#  g = Gnuplot.Gnuplot()
#  g('set parametric')
#  g('set data style lines')
#  g('set hidden')
#  g('set contour base')
#  g.title('Surface plot of the objective function')
#  g.xlabel('x')
#  g.ylabel('y')
#  g.splot(Gnuplot.GridData(m, x, y, binary = 0))

#  raw_input('Please press return to continue...\n')

   # Specify your optimization problem here, getting an instance of it.
   # Parameters:
   #    - problem name
   #    - dimension of the input space
   #    - number of constraints
   #    - list of bounds
   #    - objective function
   #    - constraints function
   #    - desired starting point reference (optional list of coordinates)

   myproblem = Problem("func2d", 2, 1, mybounds, myeval, myconstraint)

   # Create a personalized instance of the optimizer, by specifying:
   #    - the problem
   #    - maximum number of steps for the search process
   #    - minimum search step size (the search process resolution)
   #    - maximum search depth (from 1 to 500)
   #    - whether to use backtracking (1), or not (0)
   #    - whether to use graphics (1), or not (0)

   so = SimpleOpt(myproblem, 100000, 0.01, 5, 0, 0)

   # Start the optimizer

   so.optsearch()

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# Running mode configuration variables
# ---------------------------------------------------------------------------------------

use_backtracking = 0   # = 0 usually, no backtracking needed; = 1 otherwise
show_graphics = 1   # = 1 to plot utility function and optimum value over iterations; = 0 otherwise

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

try:
   import numpy as math
except:
   import math

if show_graphics:
   use_GnuPlot = False
   use_MatPlotLib = not use_GnuPlot

   try:
      if use_GnuPlot:
         import Numeric   # needed for plotting purposes
         import Gnuplot   # needed for plotting purposes
      elif use_MatPlotLib:
         import matplotlib.pyplot as plt   # needed for plotting purposes
      else:
         show_graphics = 0
         print("\nProblems with graphic plotting support (GnuPlot or MatPlotLib).\n")
   except:
      show_graphics = 0
      print("\nProblems with graphic plotting support (GnuPlot or MatPlotLib).\n")

# ---------------------------------------------------------------------------------------
# Auxiliary data and function definitions
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# Specification of the problem space:
# list of bounds on each coordinate, as a tuple (xmin, xmax)
# ---------------------------------------------------------------------------------------

mybounds = [ (-0.9, 2 * math.pi + 0.1) ]

# ---------------------------------------------------------------------------------------
# Procedural definition of the objective function f
# ---------------------------------------------------------------------------------------

def myeval(x):
   return math.sin(x[0])

# ---------------------------------------------------------------------------------------
# Procedural definition of the set of constraints gi
# ---------------------------------------------------------------------------------------
# NOTE: Each i personalizes a constraint function gi. For a given i (that is, a given
# constraint, myconstraint(i, x) must return a value < 0 if the constraint is
# satisfied, and > 0 if not
# ---------------------------------------------------------------------------------------

def myconstraint(i, x):
   # This defines [0.5, 2pi] as the allowed interval

   if i == 0:        # constraint nr. 1
      if x[0] > 0.5: return -1
      else: return 1
   elif i == 1:      # constraint nr. 2
      if x[0] < 2 * math.pi: return -1
      else: return 1
   else: return 1    # any other constraint...

# ---------------------------------------------------------------------------------------
# Program starting point
# ---------------------------------------------------------------------------------------

if __name__ == "__main__":

   # Here can be drawn a graph of the objective function
   # < ... (insert appropriate code) ... >

   if show_graphics:
      if use_GnuPlot:
         data = []
         for x in range(int(mybounds[0][0] * 1000), int(mybounds[0][1] * 1000), 100):
            data.append( [x / 1000.0, myeval( [x / 1000.0] )] )

         g = Gnuplot.Gnuplot()
         g.title('Plot of utility function')
         g('set data style linespoints')
         g.xlabel('x')
         g.ylabel('sin(x)')
         g.plot(data)
      elif use_MatPlotLib:
         x_data = []
         y_data = []
         for x in range(int(mybounds[0][0] * 1000), int(mybounds[0][1] * 1000), 100):
            x_data.append(x / 1000.0)
            y_data.append(myeval([x / 1000.0]))

#         plt.autoscale(enable=True, tight=None)
         plt.title('Plot of utility function')
         plt.xlabel('x')
         plt.ylabel('sin(x)')
         plt.plot(x_data, y_data, linestyle = 'solid', color = 'r')
         plt.show()
      else:
         print("Problems with graphic plotting support (GnuPlot or MatPlotLib).\n")

   # Specify your optimization problem here, getting an instance of it.
   # Parameters:
   #    - problem name
   #    - dimension of the input space
   #    - number of constraints
   #    - list of bounds
   #    - objective function
   #    - constraints function
   #    - desired starting point reference (optional list of coordinates)

   myproblem = Problem("func1d", 1, 2, mybounds, myeval, myconstraint)

   # Complete the problem definition by personalizing it with your objective
   # function and your set of constraints

#   myproblem.eval = myeval
#   myproblem.constraint = myconstraint

   # Create a personalized instance of the optimizer, by specifying:
   #    - the problem
   #    - maximum number of steps for the search process
   #    - minimum search step size (the search process resolution)
   #    - maximum search depth (from 1 to 500)
   #    - whether to use backtracking (1), or not (0)
   #    - whether to use graphics (1), or not (0)

   so = SimpleOpt(myproblem, 100000, 0.01, 5, use_backtracking, show_graphics)

   # Start the optimizer

   so.optsearch()

# ---------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------

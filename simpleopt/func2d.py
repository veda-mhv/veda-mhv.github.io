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
   numpy_used = True
except:
   import math
   numpy_used = False

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

   if show_graphics:
      if use_GnuPlot:
         x = []
         y = []
         for i in range(16):
            x.append(i/2.0)
            y.append(i/2.0)

         m = []
         for i in range(16):
            m.append([])
            for j in range(16):
               m[i].append(myeval((x[i], y[j])))

         g = Gnuplot.Gnuplot()
         g('set parametric')
         g('set data style lines')
         g('set hidden')
         g('set contour base')
         g.title('Surface plot of the objective function')
         g.xlabel('x')
         g.ylabel('y')
         g.splot(Gnuplot.GridData(m, x, y, binary = 0))
      elif use_MatPlotLib:
         do_plotting = True
         if numpy_used:
            np = math
         else:
            try:
               import numpy as np
            except:
               do_plotting = False
         try:
            from mpl_toolkits.mplot3d import axes3d
         except:
            do_plotting = False
         if(do_plotting):
            x = []
            y = []
            for i in range(16):
               x.append([])
               y.append([])
               for j in range(16):
                  x[i].append(j / 2.0)
                  y[i].append(i / 2.0)

            m = []
            for i in range(16):
               m.append([])
               for j in range(16):
                  m[i].append(myeval((x[i][j], y[i][j])))

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

#            wf = ax.plot_wireframe(np.array(x), np.array(y), np.array(m), linestyle = 'solid', color = 'r')
            wf = ax.plot_surface(np.array(x), np.array(y), np.array(m),  cmap = 'binary', alpha = 0.7)

            plt.setp(wf, linestyle = 'solid', color = 'r')
#            plt.autoscale(enable=True, tight=None)
            ax.set_title('Surface plot of the objective function')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z = f(x,y)')

            plt.show()
      else:
         pass

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

   so = SimpleOpt(myproblem, 100000, 0.01, 5, use_backtracking, show_graphics)

   # Start the optimizer

   so.optsearch()

# ---------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------


# =============================
# Student Names: Katelynn Birch, Eleanor Ciceri, and Jalal Ghaus
# Group ID: 49
# Date: January 23 2024
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *

def binary_ne_grid(cagey_grid):
    binary_csp = CSP("binary csp", vars=[])
    n = cagey_grid[0]
    for i in range(1, (n+1)):
        for j in range(1, (n+1)):
            index = (i, j)
            name = "Cell" + index
            var = Variable(name, domain=range(1, n+1))
            binary_csp.add_var(var)
    for i in range (n):
        var1 = binary_csp.get_all_vars[i]
        for j in range(i+1, n):
            var2 = binary_csp.get_all_vars[j]
            tuples = []
            for k in var1.domain:
                for l in var2.domain:
                    if k != l:
                        tuples.append((k, l))
            con = Constraint("Ineq(" + (i+1) + "," + (j+1) + ")", [var1, var2])
            con.add_satisfying_tuples(tuples)
            binary_csp.add_constraint(con)
    binary_vars = binary_csp.get_all_vars
    return binary_csp, binary_vars

def alldiff(list):
    for i in range(len(list)):
        if list[i] in list[i+1:]:
            return False
    return True

def nary_ad_grid(cagey_grid):
    nary_csp = CSP("nary csp", vars=[])
    n = cagey_grid[0]
    for i in range(1, (n+1)):
        for j in range(1, (n+1)):
            index = (i, j)
            name = "Cell" + index
            var = Variable(name, domain=range(1, n+1))
            nary_csp.add_var(var)
    
    nary_vars = nary_csp.get_all_vars
    return nary_csp, nary_vars

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass

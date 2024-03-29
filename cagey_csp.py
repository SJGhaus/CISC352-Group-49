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
    dom = list(range(1, n+1))
    for i in range(1, (n+1)):
        for j in range(1, (n+1)):
            index = (i, j)
            name = "Cell" + str(index)
            var = Variable(name, domain=dom)
            binary_csp.add_var(var)
    for i in range (n):
        var1 = binary_csp.get_all_vars()[i]
        for j in range(i+1, n):
            var2 = binary_csp.get_all_vars()[j]
            tuples = []
            for k in var1.domain():
                for l in var2.domain():
                    if k != l:
                        tuples.append((k, l))
                        con = Constraint("Ineq(" + str(i+1) + "," + str(j+1) + ")", [var1, var2])
                        con.add_satisfying_tuples(tuples)
                        binary_csp.add_constraint(con)
    binary_vars = binary_csp.get_all_vars()
    return binary_csp, binary_vars

#generates a list of tuples satisfying n-ary alldiff
#from www.geeksforgeeks.org/generate-all-the-permutation-of-a-list-in-python/
def alldiff(n, domain):
    domainlist = list(domain)
    if len(domainlist) == 1:
        return [domainlist]
    permslist = []
    for i in range(n):
        next = domainlist[i]
        rest = domainlist[:i] + domainlist[i+1:]
        for j in alldiff(n-1, rest):
            perm = [next] + j
            permslist.append(perm)
    return permslist

def nary_ad_grid(cagey_grid):
    nary_csp = CSP("nary csp", vars=[])
    n = cagey_grid[0]
    dom = list(range(1, n+1))
    for i in range(1, (n+1)):
        for j in range(1, (n+1)):
            index = (i, j)
            name = "Cell" + str(index)
            var = Variable(name, domain=dom)
            nary_csp.add_var(var)
    rownum = n
    for i in range(n):
        row = nary_csp.get_all_vars()[rownum-n:rownum-1]
        con = Constraint("Alldiff row " + str(i+1), row)
        rowtuples = []
        for perm in alldiff(n, range(1, n+1)):
            rowtuples.append(tuple(perm))
        con.add_satisfying_tuples(rowtuples)
        nary_csp.add_constraint(con)
        rownum += n
    colnum = 0
    for i in range(n):
        col = nary_csp.get_all_vars()[colnum::n]
        con = Constraint("Alldiff column " + str(i+1), col)
        coltuples = []
        for perm in alldiff(n, range(1, n+1)):
            coltuples.append(tuple(perm))
        con.add_satisfying_tuples(coltuples)
        nary_csp.add_constraint(con)
        colnum += 1
    nary_vars = nary_csp.get_all_vars()
    return nary_csp, nary_vars

#generates a list of permutations that satisfy the cage constraint
def solve_cage(n, op, target):
    domain = list(range(1, n+1))
    perms = alldiff(n, domain)
    valid = []
    for perm in perms:
        result = perm[0]
        if op == "+":
            result = sum(perm)
        elif op == "-":
            for val in perm[1:]:
                result -= val
        elif op == "*":
            for val in perm[1:]:
                result *= val
        elif op == "/":
            for val in perm[1:]:
                result /= val
        if result == target:
            valid.append(perm)
    return valid

def cagey_csp_model(cagey_grid):
    cagey_csp, vars = binary_ne_grid(cagey_grid)
    for cage in cagey_grid[1]:
        cagenum = 1
        target = cage[0]
        indices = cage[1]
        op = cage[2]
        vars = []
        for index in indices:
            for var in cagey_csp.get_all_vars():
                if var.name == "Cell " + str(index):
                    vars.append(var)
                    break
        con = Constraint("Cage " + str(cagenum), vars)
        lists = solve_cage(cagey_grid[0], op, target)
        tuples = []
        for l in lists:
            tuples.append(tuple(l))
        con.add_satisfying_tuples(tuples)
        cagey_csp.add_constraint(con)
        cagenum += 1
    cagey_vars = cagey_csp.get_all_vars()
    return cagey_csp, cagey_vars
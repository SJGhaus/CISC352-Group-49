# =============================
# Student Names: Katelynn Birch, Eleanor Ciceri, and Jalal Ghaus
# Group ID: 49
# Date: January 23 2024
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    # IMPLEMENT
    unassigned_vars = csp.get_all_unasgn_vars()
    most_con = unassigned_vars[0]

    const = csp.get_all_cons()

    for var in unassigned_vars[1:]:
        if const[var] >= const[most_con]:
                most_con = var

    return most_con

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    unassigned_vars = csp.get_all_unasgn_vars()
    min_rem = unassigned_vars[0]

    const = csp.get_all_cons()

    for var in unassigned_vars[1:]:
        numb_pos_var = var.cur_domain_size()
        numb_pos_min = min_rem.cur_domain_size()

        if numb_pos_var < numb_pos_min:
            min_rem = var

        elif numb_pos_var == numb_pos_min:
            if const[var] >= const[min_rem]:
                min_rem = var
    
    return min_rem

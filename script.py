# The code here will ask the user for input based on the askables
# It will check if the answer is known first

import os

# Check if pyswip package needs to be installed


from pyswip.prolog import Prolog
from pyswip.easy import *


prolog = Prolog() # Global handle to interpreter

retractall = Functor("retractall")
known = Functor("known",3)

#Define foreign functions for getting user input and writing to the screen


def write_py(X):
    print(X)
    return True


def read_py(A,V,Y):
    if isinstance(Y, Variable):
        response = input(str(A) + " is " + str(V) + "? ")
        Y.unify(response)
        return True
    else:
        return False

def read_py_menu(A, V, Y, MenuList):
    if isinstance(Y, Variable):
        print(A)
        for i, x in enumerate(MenuList):
            print(i, ". " ,x)

        response = get_menu_input(MenuList)
        print('\tYou chose', response)
        Y.unify(response)
        return True
    else:
        return False


def get_menu_input(MenuList):
    from_user = input()
    response_int = -1
    try:
        response_int = int(from_user)
        response = str(MenuList[response_int])
    except:
        response = from_user
    return response

write_py.arity = 1
read_py.arity = 3

read_py_menu.arity = 4

registerForeign(read_py)
registerForeign(write_py)
registerForeign(read_py_menu)

prolog.consult('KB.pl') # open the KB for consulting

call(retractall(known))
problem = [s for s in prolog.query("answer(X).", maxresult=1)]
print((problem[0]['X'] +"." if problem else "unknown."))
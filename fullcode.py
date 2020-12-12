KB = '''
%%KB

              
%RULES


%rules for I HAVE SYMPTOMS

answer('You need to contact Geo Blue') :- intention('I am currently experiencing COVID symptoms, I want to know what to do'), \+reside(res), insured('GeoBlue').
answer('You need to contact your local provider') :- intention('I am currently experiencing COVID symptoms, I want to know what to do'), \+reside(res), \+insured('GeoBlue').


answer('You need to test at City Test SF') :- intention('I am currently experiencing COVID symptoms, I want to know what to do'), reside(res), res_hall(turk).
answer('You need to test at chinatown') :- intention('I am currently experiencing COVID symptoms, I want to know what to do'), reside(res), res_hall('851').



%rules for I HAVE TRAVELLED/ WILL BE TRAVELLING

answer('Visit the City Test SF test centera') :-
    intention('I want to travel around'), result(urgent), res_hall(turk).
answer('Visit the glide test center') :-
    intention('I want to travel around'), result(urgent), res_hall(turk).
answer('Visit the chinatown test center') :- 
    intention('I want to travel around'), result(urgent), res_hall('851').
answer('Test privately') :-
    intention('I want to travel around'), \+result(urgent), testing(at_home).
answer('Visit the glide test center') :- 
    intention('I want to travel around'), \+result(urgent), testing(at_testing_center), reside(res), res_hall(turk).
answer('Visit the carbon health market test center') :- 
    intention('I want to travel around'), \+result(urgent), testing(at_testing_center), reside(res), res_hall(turk).
answer('Visit the carbon health market test center') :- 
    intention('I want to travel around'), \+result(urgent), testing(at_testing_center), reside(res), res_hall('851').
answer('Visit the carbon health market test center'):- 
    intention('I want to travel around'), \+result(urgent), testing(at_testing_center), reside(res), res_hall('851').



%rules for HAVE A CLOSE CONTACT WITH COVID

answer('You should start quarantine immediately'):- 
    intention('I had a close contact with a COVID patient. What next?'), exposure(known), \+quarantine_status(qurantine).
answer('You should continue your quarantine'):- 
    intention('I had a close contact with a COVID patient. What next?'), exposure(known), quarantine_status(quarantine).

answer('Visit City Test SF'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), \+symptoms(felt).
answer('Visit the local provider'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), symptoms(felt),  \+reside(res), \+insured('GeoBlue').
answer('Visit Geo Blue'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), symptoms(felt), \+reside(res),\+insured('GeoBlue'). 
answer('Visit City Test SF'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), symptoms(felt), reside(res), res_hall(turk).
answer('Visit chinatown center'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), symptoms(felt), reside(res), res_hall('851').


% rules for A CASUAL CHECK
%The 4 lines below I am not sure, as there are two options glide and carbon for given askables
answer('Visit the glide test center') :-
    intention('I just wanted to know about some casual stuff'), testing(at_testing_center), res_hall(turk).
answer('Visit the carbon health market test center') :-
    intention('I just wanted to know about some casual stuff'), testing(at_testing_center), res_hall(turk).
answer('Visit the Concentera Downtown Center') :- 
    intention('I just wanted to know about some casual stuff'), testing(at_testing_center), res_hall('851').
answer('Visit the carbon health fin test center') :- 
    intention('I just wanted to know about some casual stuff'), testing(at_testing_center), res_hall('851').
answer('Test privately') :- 
    intention('I just wanted to know about some casual stuff'), testing(at_home).



%FACTS 
reside(X) :- 
    ask('Do you live in the', X).

res_hall(X) :- 
    menuask('Which res hall do you reside in?', X, [turk, '851']).

testing(X) :-
    menuask('Where do you want to test?', X, [at_home, at_testing_center]).



exposure(X) :- 
    ask('Is your source of exposure', X).

result(X) :- ask('Is your need for testing', X).

insured(X) :- ask('Are you insured by', X).


intention(X) :- 
    menuask('What is your intention for taking the COVID test?', X, ['I am currently experiencing COVID symptoms, I want to know what to do', 'I want to travel around', 'I had a close contact with a COVID patient. What next?', 'I just wanted to know about some casual stuff']).


quarantine_status(X) :-
    ask('Are you currently in', X).


symptoms(X) :-
    ask('Are your symptoms', X).


% Asking clauses
multivalued(none). % We don't have any multivalued attributes

ask(A, V):-
known(yes, A, V), % succeed if true

!.	% stop looking

ask(A, V):-
known(_, A, V), % fail if false
!, fail.

% If not multivalued, and already known, don't ask again for a different value.
ask(A, V):-
\+multivalued(A),
known(yes, A, V2),
V \== V2,
!.

ask(A, V):-
read_py(A,V,Y), % get the answer
asserta(known(Y, A, V)), % remember it
write_py(known(Y, A, V)),
Y == yes.	% succeed or fail


menuask(A, V, _):-
known(yes, A, V), % succeed if true
!.	% stop looking

menuask(A, V, _):-
known(yes, A, V2), % If already known, don't ask again for a different value.
V \== V2,
!,
fail.

menuask(A, V, MenuList) :-
 read_py_menu(A, X, MenuList),
 check_val(X, A, V, MenuList),
 asserta( known(yes, A, X) ),
 X == V.
check_val(X, _, _, MenuList) :-
 member(X, MenuList),
 !.
check_val(X, A, V, MenuList) :-
 write_py(X), write_py(' is not a legal value, try again.'), nl,
 menuask(A, V, MenuList). 
'''


# The code here will ask the user for input based on the askables
# It will check if the answer is known first

import tempfile
import os
import pylcs
import numpy as np
import requests

# Check if pyswip package needs to be installed


from pyswip.prolog import Prolog
from pyswip.easy import *


prolog = Prolog() # Global handle to interpreter

retractall = Functor("retractall")
known = Functor("known",3)

#Define foreign functions for getting user input and writing to the screen


def write_py(X):
    """Prints the input X to the console and returns True to Prolog"""
    print(f'\t{X}')
    return True


def read_py(A: Atom, V: Atom, Y: Variable) -> bool:
    """
    Asks a question to the user and sends the response to Prolog.
    It is used to get Yes, No questions.
    Yes is normally evaluated by Prolog as True and any other input as False.

    :param A: The question (askable) that the usere should be prompted with.
    :param V: The value that the user needs to agree (yes) or disagree (any other input) with.
    :param Y: The value that Prolog will match with as True. Normally it's 'Yes'.

    :returns True if Y is a Prolog Variable and False otherwise.
    """
    if isinstance(Y, Variable):
        response = input(str(A) + " " + str(V) + "?\n--> ")
        Y.unify(response)
        return True
    else:
        return False

def read_py_menu(A: Atom, Y: Variable, MenuList: list) -> bool:
    """
    Asks the user for input based on a menu. Choosing the index of the option
    as well as the exact text of the option would work. When the response
    has the best LCS match with an option above 10% it is the default response.

    :param A: The prompt (askable) the user needs to answer.
    :param V: The answer that the user would let Prolog know about.
    :param MenuList: The options that the user has to choose from.

    :returns True if Y is a Prolog variable and False otherwise.
    """
    if isinstance(Y, Variable):
        print(A)
        list_for_lcs = []
        for i, x in enumerate(MenuList):
            print(i, ". " ,x)
            list_for_lcs.append(str(x))

        response = get_menu_input(MenuList, list_for_lcs)
        print('\tYou chose', response)
        Y.unify(response)
        return True
    else:
        return False


def get_menu_input(MenuList: list, lst_lcs: list) -> str:
    """
    Carries out the logic of identifying the choice of the user from the menu.
    A user can either choose a number or write some text.
    If they choose a number it has to be a valid number amoung the count of options given.
    If they provide a string it has to have the best match (among the options) be more than 10%.

    :param MenuList: The options that the user needs to choose from. They are stored as Prolog Atoms.
    :param lst_lcs: The options stored in a list of strings that Python can interprate.

    :returns a string of the option that the user chose.
    """
    from_user = input('--> ')
    response_int = float('inf')
    try:
        response_int = int(from_user)
        response = str(MenuList[response_int])
    except:
        response = from_user.lower()
        response = most_appropriate(response, lst_lcs)
    return response

def most_appropriate(response: str, lst_lcs: list) -> str:
    """
    Choose the most appropriate option given the response string.
    It matches the choice by finding out the percentage LCS (Least Common Subsequence match).
    If the best match is above 30%, it is taken as the choice of the user.
    Otherwise the user will be reprompted for another option.

    :parm response: The input from the user.
    :param lst_lcs: The options stored in a list of strings that Python can interprate.

    :returns a string of the option that the user chose.
    """
    lcs = pylcs.lcs_of_list(response, lst_lcs)

    lengths = []
    for option in lst_lcs:
        lengths.append(len(option))

    # Calculate the percentage match of the LCS
    similarities = np.array(lcs)/np.array(lengths)

    # Identify the index of the highest match
    option_idx = np.argmax(similarities)

    # If the highest match is less than 10% return original response
    # so that the user can be reprompted
    # otherwise return the best option
    if similarities[option_idx] < 0.1:
        return response
    return lst_lcs[option_idx]

write_py.arity = 1
read_py.arity = 3

read_py_menu.arity = 3

registerForeign(read_py)
registerForeign(write_py)
registerForeign(read_py_menu)

# Create a temporary file with the KB in it
(FD, name) = tempfile.mkstemp(suffix='.pl', text = "True")
with os.fdopen(FD, "w") as text_file:
    text_file.write(KB)
prolog.consult(name) # open the KB for consulting
os.unlink(name) # Remove the temporary file

call(retractall(known))

#Using covidtracking API to give uptodate information
response = requests.get("https://api.covidtracking.com/v1/states/ca/current.json")
print("Here is  a quick update on COVID situation in San Francisco: \nThe death toll as of",response.json()['checkTimeEt'], "is", response.json()['death'])
print("Today, the number of cases increased by",response.json()['positiveIncrease'],",while death cases increased by",response.json()['deathIncrease'],"\n")
answer = [s for s in prolog.query("answer(X).", maxresult=1)]
print((answer[0]['X'] +"." if answer else "unknown."))
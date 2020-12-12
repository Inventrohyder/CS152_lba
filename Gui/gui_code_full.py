KB = """%%KB

              
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
user_response(Y),
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
 system_response(X), system_response(' is not a legal value, try again.\n'),
 menuask(A, V, MenuList). 
 """

import tempfile
import os
from tkinter import Frame, Label, Button, Tk
from pyswip import Prolog, Functor, Variable, Atom, registerForeign, call
from tkinter import simpledialog
import pylcs
import numpy as np

class DPDP():

    def __init__(self, master):

        frame = Frame(master)
        frame.grid()

        self.chatWindow = Label(master, bd=1, bg='white', width = 100, height = 8, justify="left")
        self.chatWindow.place(x=6,y=6,height=500,width=800)

        self.Button = Button(master, text="Start system", bg='blue',activebackground='light blue',width=12, height=5, command=lambda: queryGenerator())
        self.Button.place(x=6,y=510,height=88,width=800)


prolog = Prolog()  # Global handle to interpreter

# Create a temporary file with the KB in it
(FD, name) = tempfile.mkstemp(suffix='.pl', text = "True")
with os.fdopen(FD, "w") as text_file:
    text_file.write(KB)
prolog.consult(name) # open the KB for consulting
os.unlink(name) # Remove the temporary file

retractall = Functor("retractall")
known = Functor("known", 3)


def system_response(response: str) -> None:
    """
    Prints the input response to the GUI and returns True to Prolog
    and prepending SYSTEM to show that it is the system talking
    """
    app.chatWindow['text'] += f'SYSTEM: {response}'
    return True

def user_response(response: str) -> None:
    """
    Prints the input response to the GUI and returns True to Prolog
    and prepending USER to show that it is the user talking
    """
    app.chatWindow['text'] += f'YOU: {response}\n'
    return True


def read_py(A: Atom, V: Atom, Y: Variable) -> bool:
    """
    Asks a question to the user and sends the response to Prolog.
    It is used to get Yes, No questions.
    Yes is normally evaluated by Prolog as True and any other input as False.

    :param A: The question (askable) that the user should be prompted with.
    :param V: The value that the user needs to agree (yes) or disagree 
                (any other input) with.
    :param Y: The value that Prolog will match with as True. 
                Normally it's 'Yes'.

    :returns True if Y is a Prolog Variable and False otherwise.
    """
    if isinstance(Y, Variable):
        system_response(f'{str(A)} {str(V)}?\n')
        response = simpledialog.askstring("Input", f'{str(A)} {str(V)}?',
                                          parent=root)

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
        list_for_lcs = []
        question = "" + str(A) + "\n"
        for i, x in enumerate(MenuList):
            question += "\t" + str(i) + " .  " + str(x) + "\n"
            list_for_lcs.append(str(x))
        response = get_menu_input(question, MenuList, list_for_lcs)
        user_response(response)
        Y.unify(response)
        return True
    else:
        return False


def get_menu_input(question: str, MenuList: list, lst_lcs: list) -> str:
    """
    Carries out the logic of identifying the choice of the user from the menu.
    A user can either choose a number or write some text.
    If they choose a number it has to be a valid number amount the count of options given.
    If they provide a string it has to have the best match (among the options) be more than 10%.

    :param MenuList: The options that the user needs to choose from. They are stored as Prolog Atoms.
    :param lst_lcs: The options stored in a list of strings that Python can interprate.

    :returns a string of the option that the user chose.
    """
    system_response(question)
    from_user = simpledialog.askstring("Input", question,
                                       parent=root)
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

system_response.arity = 1
user_response.arity = 1
read_py.arity = 3

read_py_menu.arity = 3

registerForeign(read_py)
registerForeign(system_response)
registerForeign(user_response)
registerForeign(read_py_menu)


def queryGenerator():
      # this prints the values that are chosen,correctly

    # Each we query clear all the known values
    call(retractall(known))

    app.chatWindow['text'] = "="*70 + "\n"

    q = list(prolog.query("answer(X).", maxresult=1))  # prolog query

    for v in q:
        app.chatWindow['text'] += f"ANSWER ==> {str(v['X'])}\n"

    app.Button.configure(text="Run again")


root = Tk()
root.geometry("820x600")
root.resizable(0, 0)
root.config(bg='#44689E')
app = DPDP(root)
root.title("DPDP")
root.mainloop()

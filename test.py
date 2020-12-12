from tkinter import *
import tkinter
import tkinter.messagebox
from PIL import ImageTk, Image
from pyswip import *
from tkinter import simpledialog
import pylcs
import numpy as np



sympList = ['--Select--', 'headache', 'sneezing', 'runny_nose', 'sore_throat', 'fever', 'chills', 'bodyache',
            'abdominal_pain', 'loss_of_appetite', 'skin_rash', 'conjunctivitus', 'sweating', 'vomitting', 'diarrhea']


intention = [
    'I am currently experiencing COVID symptoms, I want to know what to do',
    'I want to travel around',
    'I had a close contact with a COVID patient. What next?',
    'I just wanted to know about some casual stuff'
]

reside = [
    "res",
]

halls = [
    'turk',
    '851'
]

class DPDP:

    def __init__(self, master):

        frame = Frame(master)
        frame.grid()

        # ---------medical symbol pic------------------------
        path1 = "Capture.png"
        img = ImageTk.PhotoImage(Image.open(path1))
        panel = Label(root, image=img)
        panel.photo = img
        panel.place(x=20, y=20, width=140, height=130)

        # ----------page title-----------------------------------
        mainHeading = Label(master, text="Disease Prediction & Drug Prescribtion ", font=(
            'Verdana 20'), bg='#44689E')
        mainHeading.grid(padx=200, pady=60)

        # ----------symptoms selection---------------------------------------------------

        # -------Symptom1-------------------------
        symp1 = Label(root, text="Intention",
                      font=('Verdana 15'), bg='#44689E')
        symp1.place(x=20, y=200)

        self.selSymp1 = StringVar()
        self.selSymp1.set(sympList[0])

        sympDropDown1 = OptionMenu(root, self.selSymp1, *intention)
        sympDropDown1.place(x=180, y=200)

        # -------Symptom2-------------------------

        self.symp2 = Label(root, text="Res",
                           font=('Verdana 15'), bg='#44689E')
        self.symp2.place(x=20, y=300)

        self.selSymp2 = StringVar()
        self.selSymp2.set(sympList[0])

        sympDropDown2 = OptionMenu(root, self.selSymp2, *reside)
        sympDropDown2.place(x=180, y=300)

        # -------Symptom3-------------------------

        self.symp3 = Label(root, text="halls",
                           font=('Verdana 15'), bg='#44689E')
        self.symp3.place(x=20, y=400)

        self.selSymp3 = StringVar()
        self.selSymp3.set(sympList[0])

        sympDropDown3 = OptionMenu(root, self.selSymp3, *halls)
        sympDropDown3.place(x=180, y=400)

        # -------Symptom4-------------------------

        symp4 = Label(root, text="4th Symptom",
                      font=('Verdana 15'), bg='#44689E')
        symp4.place(x=20, y=500)

        self.selSymp4 = StringVar()
        self.selSymp4.set(sympList[0])

        sympDropDown4 = OptionMenu(root, self.selSymp4, *sympList)
        sympDropDown4.place(x=180, y=500)

        bt = Button(frame, text="click", width=5,
                    command=lambda: queryGenerator(self.selSymp1.get(), self.selSymp2.get(), self.selSymp3.get(),
                                                   self.selSymp4.get()))
        bt.grid(row=4, column=5)

prolog = Prolog() # Global handle to interpreter
prolog.consult('kb.pl')

retractall = Functor("retractall")
known = Functor("known",3)

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
        response = simpledialog.askstring("Input", str(A) + " " + str(V) + "?",
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
        print(A)
        list_for_lcs = []
        question = "" + str(A) + "\n"
        for i, x in enumerate(MenuList):
            question += str(i) + " .  " + str(x) + "\n"
            list_for_lcs.append(str(x))

        response = get_menu_input(question, MenuList, list_for_lcs)
        print('\tYou chose', response)
        Y.unify(response)
        return True
    else:
        return False


def get_menu_input(question:str, MenuList: list, lst_lcs: list) -> str:
    """
    Carries out the logic of identifying the choice of the user from the menu.
    A user can either choose a number or write some text.
    If they choose a number it has to be a valid number amoung the count of options given.
    If they provide a string it has to have the best match (among the options) be more than 10%.

    :param MenuList: The options that the user needs to choose from. They are stored as Prolog Atoms.
    :param lst_lcs: The options stored in a list of strings that Python can interprate.

    :returns a string of the option that the user chose.
    """
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

write_py.arity = 1
read_py.arity = 3

read_py_menu.arity = 3

registerForeign(read_py)
registerForeign(write_py)
registerForeign(read_py_menu)

def queryGenerator(s1, s2, s3, s4):

    print(s1, s2, s3, s4)  # this prints the values that are chosen,correctly

    call(retractall(known)) 

    q = list(prolog.query("answer(X).", maxresult=1))  # prolog query
   # for e in q[0].values():
   # print("You have " + e)
   # break
    print(q)
    for v in q:
        print(v)
        print(v['X'])
        tkinter.messagebox.showinfo(title=str(v), message=str(v['X']))
    
    



root = Tk()
root.geometry("820x600")
root.resizable(0, 0)
root.config(bg='#44689E')
app = DPDP(root)
root.title("DPDP")
root.mainloop()

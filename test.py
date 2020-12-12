from tkinter import *
import tkinter
import tkinter.messagebox
from PIL import ImageTk, Image
from pyswip import *


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


def queryGenerator(s1, s2, s3, s4):

    print(s1, s2, s3, s4)  # this prints the values that are chosen,correctly
    prolog = Prolog()
    prolog.consult('kb.pl')

    q = list(prolog.query("answer(X, '%s',%s,%s)." % (s1, s2, s3)))  # prolog query
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

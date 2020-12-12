import time
from tkinter import *
import tkinter.messagebox
from itertools import chain, repeat
from tkinter import simpledialog



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
        response = simpledialog.askstring("Input", str(A) + " is " + str(V) + "? ",
                                parent=root)
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

prolog.consult('Engine.pl') # open the KB for consulting

call(retractall(known))
# problem = [s for s in prolog.query("answer(X).", maxresult=1)]
# print((problem[0]['X'] +"." if problem else "unknown."))

window_size="550x450"

#getting response from user 
def chat(user_response):
    problem = [s for s in prolog.query("problem(X).", maxresult=1)]
    return((problem[0]['X'] +"." if problem else "unknown."))       

#showing the user interface 
class chat_UI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        
        #attributes for colors 
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "black"
        self.font = "Verdana 10"

        menu = Menu(self.master)

        
        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        #adding scroll bar 
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        #Adding text box to show the conversation 

        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        #Adding a frame that wraps user entry 
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        #Adding a box that takes user input 
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        # self.users_message = self.entry_field.get()

        #Frame containing send button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        #Send button
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message_insert(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        self.send_button.pack(side=LEFT, ipady=8)
        self.master.bind("<Return>", self.send_message_insert)
        
        self.last_sent_label(date="No messages sent.")
        
        
    #to show the time/date of last seen message 
    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)


    def chatexit(self):
        exit()
    def send_message_insert(self, message):
        user_input = self.entry_field.get() #enter 
        pr1 = "Me : " + user_input + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr1)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        ob=chat(user_input) #give response
        pr="Covid Buddy : " + ob + "\n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        self.last_sent_label(str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        self.entry_field.delete(0,END)
        time.sleep(0)
        #t2 = threading.Thread(target=self.playResponce, args=(ob,))
        #t2.start()
        #return ob  
        
    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.sent_label.config(bg="#EEEEEE", fg="#000000")

        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

    # Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_default()    
        
root=Tk()

a =chat_UI(root)
root.geometry(window_size)
root.title("COVID Buddy")
root.mainloop()
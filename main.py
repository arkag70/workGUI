from tkinter import *
import tkinter.scrolledtext as tkscrolled

def browse():
	pass

root  = Tk()
root.resizable(width=False, height=False)
root.title("Software Restrictions filter")

head = Frame(root,background  = 'grey')
head.grid(row = 0,column = 0)

upper = Frame(root,background  = 'white')
upper.grid(row = 1,column = 0)

gap = Frame(root,background  = 'white')
gap.grid(row = 2,column = 0)

lower = Frame(root,background  = 'white')
lower.grid(row = 3,column = 0)



entry = Entry(upper,width = 80)
entry.grid(row = 0,column = 0)

button = Button(upper,text = "browse",command = browse,width = 10)
button.grid(row = 0,column = 1)

label = Label(gap,height = 1, width = 80)
label.pack()

scrollbar = Scrollbar(lower) 
results = Text(lower, width=80, height=10, wrap="word",
                   yscrollcommand=scrollbar.set,
                   borderwidth=0, highlightthickness=0)
scrollbar.config(command=results.yview)
scrollbar.pack(side="right", fill="y")
results.pack(side="left", fill="both", expand=True)





root.mainloop()
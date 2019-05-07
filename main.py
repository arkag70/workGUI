from tkinter import *
import os
from tkinter import filedialog
from tkinter.ttk import Progressbar
import tkinter.scrolledtext as tkscrolled

stock_words = ["nanospin","getutid","dup2","InterruptHookIdle","nftw","mount_ifs","vfork","pthread_setschedprio"]

count = 0
def readFile(filepath):
    global count
    count += 1
    f = open(filepath, mode = 'r', encoding="Latin-1")
    file_content = f.read()
    return file_content

def getFiles(path):
    
    #list of all .c .h .cpp .hpp files in the above path
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            #ext = file.split('.')[1]
            if '.c' in file or '.h' in file or '.cpp' in file or '.hpp':
                files.append(os.path.join(r, file))
    
    #list to contain contents of all the files
    file_contents_list = []
    
    for file in files:
        file_contents_list.append(readFile(file))
    
    #list to contain filenames of such files which contain stock_words
    file_names_with_stockWords = []
    
    for i in range(len(file_contents_list)):
        words_to_append = ""
        for word in stock_words:
            if word in file_contents_list[i]:
                words_to_append = words_to_append+word+","
        if len(words_to_append) != 0:
            file_names_with_stockWords.append(files[i]+" ---> "+words_to_append)
    
    if len(file_names_with_stockWords) == 0:
        results.insert(END,"None")
    
    files_number.config(text = "files read : "+str(count)+'\t')
    files_found.config(text = 'files with stock_words: '+str(len(file_names_with_stockWords)))
    
    for eachfile in file_names_with_stockWords:
        #print(eachfile)
        results.insert(END,eachfile)
        results.insert(END,'\n\n')
        
#D:\\Arka\\StateHandlerLatestDevelop\\idc5

def browse():
    dirname = filedialog.askdirectory(parent=root, initialdir="D:", title='Select your folder')
    entry.delete(0,END)
    entry.insert(0,dirname)
    
def search():
    global count
    count = 0
    status.config(text = "Searching....")
    files_number.config(text = "")
    files_found.config(text = "")
    results.delete(1.0,END)
    results.update()
    getFiles(entry.get())
    root.after(10000)
    
    status.config(text = "Search Completed\t")
    
    


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

extension_layout = Frame(root,background  = 'white')
extension_layout.grid(row = 4,column = 0)

down = Frame(root,background  = 'white')
down.grid(row = 5,column = 0)


h_gap = Label(head,height = 1, width = 80)
h_gap.pack()

entry = Entry(upper,width = 80)
entry.grid(row = 0,column = 0)

button_browse = Button(upper,text = "browse",command = browse,width = 10)
button_browse.grid(row = 0,column = 1)

button_search = Button(upper,text = "search",command = search,width = 10)
button_search.grid(row = 0,column = 2)

label = Label(gap,height = 1, width = 80)
label.pack()

v_scrollbar = Scrollbar(lower,orient = VERTICAL) 
h_scrollbar = Scrollbar(lower,orient = HORIZONTAL)

results = Text(lower, width=80, height=10, wrap="word",
               yscrollcommand = v_scrollbar.set,
               xscrollcommand = h_scrollbar.set,
               borderwidth = 0, 
               highlightthickness = 0)

v_scrollbar.config(command=results.yview)
h_scrollbar.config(command=results.xview)

v_scrollbar.pack(side="right", fill="y")
h_scrollbar.pack(side="bottom", fill="x")

results.pack()

ext_entry = Entry(extension_layout,width = 80)
ext_entry.grid(row = 0,column = 0)

status = Label(down)
status.pack(side='left')

files_number = Label(down)
files_number.pack(side = 'left')

files_found = Label(down)
files_found.pack(side = 'left')




root.mainloop()

from tkinter import *
import os
from tkinter import filedialog
from tkinter import ttk
import os 
import time
import threading

stock_words = ["nanospin","getutid","dup2","InterruptHookIdle","nftw","mount_ifs","vfork","pthread_setschedprio"]

count = 0
def readFile(filepath):
    global count
    count += 1
    with open(filepath, mode = 'r', encoding="Latin-1") as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

def getFiles(path,extensions):
    
    files = []
    
    # r=root, d=directories, f = files
    if len(extensions) == 1 and extensions[0] == '':
        # no extension is provided, selelct all files
        
        for r, d, f in os.walk(path):
            for file in f:
                files.append(os.path.join(r, file))
    else:
        # for given extensions, list the files

        for r, d, f in os.walk(path):
            for file in f:
                if '.' in file:
                    ext = file.split('.')[1]
                    if ext.lower() in extensions:
                        files.append(os.path.join(r, file))
    
    file_contents_list = []

    for file in files:
        file_contents_list.append(readFile(file))

    #list to contain filenames of such files which contain stock_words
    file_names_with_stockWords = []
    
    for j,file_content in enumerate(file_contents_list):
        words_to_append = ""
        for word in stock_words:
            for i,line in enumerate(file_content):
                if word in line:
                    words_to_append = words_to_append+word+f" (line {i+1}), "
        if len(words_to_append) != 0:
            file_names_with_stockWords.append(files[j]+" ---> "+words_to_append)
    
    if len(file_names_with_stockWords) == 0:
        results.insert(END,"None")
    
    files_number.config(text = "Files read : "+str(count)+'\t')
    files_found.config(text = 'Files with stock_words: '+str(len(file_names_with_stockWords)))
    
    for eachfile in file_names_with_stockWords:
        #print(eachfile)
        results.insert(END,eachfile)
        
#D:\\Arka\\StateHandlerLatestDevelop\\idc5

def browse():
    dirname = filedialog.askdirectory(parent=root, initialdir="D:\\", title='Choose your Project Directory')
    entry.delete(0,END)
    entry.insert(0,dirname)

# def browse_root():
#     global rootname
#     rootname = filedialog.askdirectory(parent=root, initialdir="D:\\", title='Select Project folder')
#     entry_root.delete(0,END)
#     entry_root.insert(0,rootname)
#     entry.delete(0,END)
#     entry.insert(0,'Browser for your Component Directory')

def start_search_thread(event):
    
    global search_thread
    search_thread = threading.Thread(target = search)
    search_thread.daemon = True
    progressbar.start()
    search_thread.start()
    root.after(20,check_search_thread)

def check_search_thread():
    if search_thread.is_alive():
        root.after(20,check_search_thread)
    else:
        progressbar.stop()
  
def search():
    global count
    count = 0
    status.config(text = "Searching....")
    files_number.config(text = "")
    files_found.config(text = "")
    results.delete(0,END)
    extensions = ext_entry.get().lower().split(' ')

    #time.sleep(5)
    
    getFiles(entry.get(),extensions)
    status.config(text = "Search Completed\t")
    
    


root  = Tk()
root.config(background = 'light blue')
root.geometry("900x450")
root.resizable(width=False, height=False)
root.title("Software Restrictions Filter")

# layouts
# upper = Frame(root,background  = 'light blue')
# upper.grid(row = 0,column = 0,padx = 0,pady = 10)



upper = Frame(root,background  = 'light blue')
upper.grid(row = 0,column = 0,padx = 40,pady = 20)

lower = Frame(root,background  = 'white')
lower.grid(row = 1,column = 0)

extension_layout = Frame(root,background  = 'light blue')
extension_layout.grid(row = 2,column = 0,pady = 10)

down = Frame(root,background  = 'white')
down.grid(row = 3,column = 0)

# widgets

# entry_root = Entry(upper,width = 80,bd = 3)
# entry_root.grid(row = 0,column = 0)
# entry_root.config(font=("Times New Roman", 12))
# entry_root.insert(0,'Browser for the Project Directory')

# button_root = Button(upper,text = "...",command = browse_root,width = 4,bd = 3,font=("Times New Roman", 10))
# button_root.grid(row = 0,column = 1)


entry = Entry(upper,width = 80,bd = 3)
entry.grid(row = 0,column = 0)
entry.config(font=("Times New Roman", 12))
entry.insert(0,'Browser for the Project Directory')

button_browse = Button(upper,text = "...",command = browse,width = 4,bd = 3,font=("Times New Roman", 10))
button_browse.grid(row = 0,column = 1)

button_search = Button(upper,text = "search",command = lambda: start_search_thread(None),width = 10,bd = 3,font=("Times New Roman", 10))
button_search.grid(row = 0,column = 2,padx = 5)

v_scrollbar = Scrollbar(lower,orient = VERTICAL,bd = 2) 
h_scrollbar = Scrollbar(lower,orient = HORIZONTAL,bd = 2)

results = Listbox(lower, width=102, height=12,
               yscrollcommand = v_scrollbar.set,
               xscrollcommand = h_scrollbar.set,
               bd = 2)

v_scrollbar.config(command=results.yview)
h_scrollbar.config(command=results.xview)

v_scrollbar.pack(side="right", fill="y")
h_scrollbar.pack(side="bottom", fill="x")

results.pack()
results.configure(font=("Times New Roman", 12))

ext_label = Label(extension_layout,text = "File extensions :  ",font=("Times New Roman", 12))
ext_label.grid(row = 0,column = 0)
ext_label.config(background = 'light blue')

ext_entry = Entry(extension_layout,width = 80,bd = 3,font=("Times New Roman", 12))
ext_entry.grid(row = 0,column = 1)
ext_entry.insert(0,"c cpp h hpp txt cmake")

status = Label(down,background = 'light blue',font=("Times New Roman", 12))
status.grid(row = 0, column = 0)

files_number = Label(down,background = 'light blue',font=("Times New Roman", 12))
files_number.grid(row = 0, column = 1)

files_found = Label(down,background = 'light blue',font=("Times New Roman", 12))
files_found.grid(row = 0, column = 2)

progressbar = ttk.Progressbar(down,mode = 'indeterminate')
progressbar.grid(row = 0, column = 3)

root.iconbitmap('icon1.ico')
root.mainloop()

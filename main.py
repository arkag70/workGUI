from tkinter import *
import os
from tkinter import filedialog

stock_words = ["nanospin","getutid","dup2","InterruptHookIdle","nftw","mount_ifs","vfork","pthread_setschedprio"]

count = 0
def readFile(filepath):
    global count
    count += 1
    f = open(filepath, mode = 'r', encoding="Latin-1")
    file_content = f.read()
    return file_content

def getFiles(path,extensions):
    
    #list of all .c .h .cpp .hpp files in the above path
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.' not in file:
                files.append(os.path.join(r, file))
            else:
                ext = file.split('.')[1]
                if ext in extensions:
            #if '.c' in file or '.cpp' in file or '.h' in file or '.hpp' in file:
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
    
    files_number.config(text = "Files read : "+str(count)+'\t')
    files_found.config(text = 'Files with stock_words: '+str(len(file_names_with_stockWords)))
    
    for eachfile in file_names_with_stockWords:
        #print(eachfile)
        results.insert(END,eachfile)
        results.insert(END,'\n\n')
        
#D:\\Arka\\StateHandlerLatestDevelop\\idc5

def browse():
    dirname = filedialog.askdirectory(parent=root, initialdir="D:\\", title='Select your folder')
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
    
    extensions = ext_entry.get().split(' ')
    
    getFiles(entry.get(),extensions)

    
    status.config(text = "Search Completed\t")
    
    


root  = Tk()
root.config(background = 'light blue')
root.geometry("900x450")
root.resizable(width=False, height=False)
root.title("Software Restrictions Filter")

# layouts
upper = Frame(root,background  = 'light blue')
upper.grid(row = 0,column = 0,padx = 40,pady = 20)

lower = Frame(root,background  = 'white')
lower.grid(row = 1,column = 0)

extension_layout = Frame(root,background  = 'light blue')
extension_layout.grid(row = 2,column = 0,pady = 10)

down = Frame(root,background  = 'white')
down.grid(row = 3,column = 0)

# widgets
entry = Entry(upper,width = 80,bd = 3)
entry.grid(row = 0,column = 0)
entry.config(font=("Times New Roman", 12))

button_browse = Button(upper,text = "browse",command = browse,width = 10,bd = 3,font=("Times New Roman", 10))
button_browse.grid(row = 0,column = 1,padx = 10)

button_search = Button(upper,text = "search",command = search,width = 10,bd = 3,font=("Times New Roman", 10))
button_search.grid(row = 0,column = 2,padx = 5)

v_scrollbar = Scrollbar(lower,orient = VERTICAL,bd = 2) 
h_scrollbar = Scrollbar(lower,orient = HORIZONTAL,bd = 2)

results = Text(lower, width=102, height=12, wrap=NONE,
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

status = Label(down,background = 'light blue',font=("Times New Roman", 12,"bold"))
status.pack(side='left')

files_number = Label(down,background = 'light blue',font=("Times New Roman", 12,"bold"))
files_number.pack(side = 'left')

files_found = Label(down,background = 'light blue',font=("Times New Roman", 12,"bold"))
files_found.pack(side = 'left')




root.mainloop()

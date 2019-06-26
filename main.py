from tkinter import *
import os
from tkinter import filedialog
from tkinter import ttk
import os 
import time
import threading
import subprocess
import pandas as pd
import re
from datetime import datetime, timezone
from multiprocessing import Pool,Value,Lock,current_process

#git log -p
#git blame -L <start>,<end> full file name
Items = []
count = 0
counter = None
reason = []
libm_lib = "abs labs llabs fabs div ldiv lldiv fmod remainder remquo fma fmax fmin fdim nan nanf nanl exp exp2 expm1 log log2 log10 log1p ilogb logb sqrt cbrt hypot pow sin cos tan asin acos atan atan2 sinh cosh tanh asinh acosh atanh erf erfc lgamma tgamma ceil floor trunc round lround llround nearbyint rint lrint llrint frexp ldexp modf scalbn scalbln nextafter nexttoward copysign fpclassify isfinite isinf isnan isnormal signbit".split(" ")
#-------------------------------------------------------------------------------------------------#
def init(args):
    ''' store the counter for later use '''
    global counter
    counter = args

def category1_search(one_file):
    lines = []

    reason = '''An application SHALL NOT use getutid() to search the
user information file for a particular entry.
Instead the application can use getutent() to access successive user
information entries until the correct entry is found (or the table is exhausted)'''

    for i,line in enumerate(one_file):
        if "getutid" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"Category: 1 lines: {lines}:- {reason}")

    return 0

#-------------------------------------------------------------------------------------------------#
# if re.match(regex, content) is not None:
#   blah..
def category2_search(one_file):
    lines = []
    reason = '''Before calling a function in the libm, an application SHOULD call feclearexcept(FE_ALL_EXCEPT).
    After calling a function in the libm, an application SHOULD call fetestexcept().'''
    func_count = 0
    fc_count = 0
    ft_count = 0

    for i,line in enumerate(one_file):
        for func in libm_lib:
            myfunc = r'\b'+re.escape(func)+r'\('
            if re.match(myfunc, line) is not None:
                #print(line)
                lines.append(i+1)
                func_count += 1

        if re.match(r"\bfeclearexcept\b",line) is not None:
            fc_count += 1
        if re.match(r"\bfetestexcept\b",line) is not None:
            ft_count += 1
    if func_count !=0:
        #print(ft_count,func_count,fc_count)
        if not (func_count == ft_count == fc_count):
            
            return (f"Category: 2 lines: {lines}:- {reason}")
        
    return 0
#-------------------------------------------------------------------------------------------------#

def category3_search(one_file):
    lines = []
    reason = '''dup2() found.
    An application SHALL NOT invoke the dup2 function while
simultaneously creating other new file descriptors.
The dup2 function can erroneously return EBADF if another thread in the
application creates a new file descriptor that matches the dup2 newfd parameter
at the same time the dup2 function is executing.'''
    for i,line in enumerate(one_file):
        if "dup2(" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"Category: 3 lines: {lines}:- {reason}")
        
    return 0
#-------------------------------------------------------------------------------------------------#

def category4_search(one_file):
    lines = []
    reason = ''''''
        
    return 0
#-------------------------------------------------------------------------------------------------#

def category5_search(one_file):
    lines = []
    reason = '''By default the clock period (rate at which clock ticks arrive, in
nanoseconds) will be 1 ms. If any other value is required, the value SHOULD be established by calling ClockPeriod() with the desired value at boot time, as early as possible, 
and ClockPeriod() shall be used only for reading the clock period thereafter.\n\n A thread that invokes the ClockPeriod() API MUST be bound to the
same CPU that handles clock interrupts. '''
    
    for i,line in enumerate(one_file):
        if "ClockPeriod(" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"Category: 5 lines: {lines}:- {reason}")
    return 0
#-------------------------------------------------------------------------------------------------#

def category6_search(one_file):
    lines=[]
    reason = '''An application SHALL NOT invoke the mount_ifs utility.'''

    for i,line in enumerate(one_file):
        if "mount_ifs" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"Category: 6 lines: {lines}:- {reason}")
    return 0
#-------------------------------------------------------------------------------------------------#

def category7_search(one_file):
    lines = []
    reason = '''A safety application SHALL NOT use the vfork() API. '''

    for i,line in enumerate(one_file):
        if "vfork(" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"Category: 7 lines: {lines}:- {reason}")
    return 0
#-------------------------------------------------------------------------------------------------#

def category8_search(one_file):
    lines = []
    reason = '''An application SHALL NOT invoke nftw unless the number
of available file descriptors exceeds the depth of the file tree.
The nftw function may use one file descriptor for each level of the tree, regardless
of the value of the depth parameter provided. '''

    for i,line in enumerate(one_file):
        if "nftw(" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"Category: 8 lines: {lines}:- {reason}")

    return 0
#-------------------------------------------------------------------------------------------------#
def category9_search(one_file):
    lines = []
    reason = '''A process that has invoked InterruptHookIdle() SHALL NOT
terminate. The QOS does not provide a mechanism to unregister an idle hook registegreen
with InterruptHookIdle(). If a process that has invoked InterruptHookIdle()
terminates, the system behaviour is not defined.
Note that the InterruptHookIdle() function has been deprecated. The InterruptHookIdle2()
function, which does not suffer from this problem, should
be used instead. '''
    for i,line in enumerate(one_file):
        if "InterruptHookIdle(" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"Category: 9 lines: {lines}:- {reason}")

    return 0
#-------------------------------------------------------------------------------------------------#
def category10_search(one_file):
    reason = ''' '''
    return 0
#-------------------------------------------------------------------------------------------------#
def category11_search(one_file):
    reason = ''' '''
    return 0
#-------------------------------------------------------------------------------------------------#
def category12_search(one_file):
    reason = ''' '''
    return 0
#-------------------------------------------------------------------------------------------------#
def category13_search(one_file):
    reason = ''' '''
    return 0
#-------------------------------------------------------------------------------------------------#
files_processed = 0
def filter_search(one_file):
    issues = []
    global counter
    a = category1_search(one_file)
    if a!=0:
        issues.append(a)
    a = category2_search(one_file)
    if a!=0:
        issues.append(a)
    a = category3_search(one_file)
    if a!=0:
        issues.append(a)
    a = category4_search(one_file)
    if a!=0:
        issues.append(a)
    a = category5_search(one_file)
    if a!=0:
        issues.append(a)
    a = category6_search(one_file)
    if a!=0:
        issues.append(a)
    a = category7_search(one_file)
    if a!=0:
        issues.append(a)
    a = category8_search(one_file)
    if a!=0:
        issues.append(a)
    with counter.get_lock():
        counter.value += 1
        print(counter.value)
    return issues

#---------------------------------------------------------------------------------------------------#
def remove_comments(filepath):
    comment = 0
    final_list = []
    with open(filepath,mode = "r", encoding="Latin-1") as f:
        lines = [line.rstrip('\n') for line in f]

    for line in lines:
        #print(line)
        if comment == 1:
            if "*/" in line:
                _index = line.index('*/')
                final_list.append(line[_index+2:])
                comment = 0
            else:
                final_list.append("     ")

            continue

        if "//" in line:
            #single line comment
            _index = line.index('//')
            final_list.append(line[:_index])

        elif "/*" in line:
            if "*/" in line:
                #single line comment again
                s_index = line.index("/*")
                e_index = line.index("*/")
                final_list.append(line[:s_index] + line[e_index+2:])
            else:
                #multi line comment
                _index = line.index('/*')
                final_list.append(line[:_index])
                comment = 1
        else:
            final_list.append(line)

    return final_list
#---------------------------------------------------------------------------------------------------#
def readFile(filepath):
    global count
    count += 1
    files_number.config(text = "Files scanned : "+str(count)+'\t')
    if checkCmd.get() == 1:
        return remove_comments(filepath)

    else:

        with open(filepath, mode = 'r', encoding="Latin-1") as f:
            lines = [line.rstrip('\n') for line in f]
        return lines

#---------------------------------------------------------------------------------------------------#
findings = []
def getFiles(path,extensions):
    
    files = []
    file_names_with_issues = []
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
        inputs.insert(END,file)
        inputs.yview(END)
        file_contents_list.append(readFile(file))

    
    counter = Value('i', 0)
    starttime = time.time()
    text_status.set("Processing....")
    p = Pool(os.cpu_count(),initializer = init, initargs = (counter, ))
    i = p.map_async(filter_search, file_contents_list, chunksize = 1)
    p.close()
    p.join()
    print(f"Elapsed time: {time.time() - starttime}")

    inception = [lst for lst in i.get()]

    hits = 0
    file_names_with_issues = []
    for i in range(len(inception)):
        if inception[i] != []:
            hits += 1
            findings.append(inception[i])
            file_names_with_issues.append(files[i])
    
    
    occurances.config(text = 'Number of hits: '+str(hits))
    
    for index,eachfile in enumerate(file_names_with_issues):
        #print(eachfile)
        onefile_line =[]
        for onefile_find in findings:
            #get lines list
            lines = ""
            for find in onefile_find:
                l_temp = find.split('[')[1].split(']')[0]
                lines += l_temp+", " 

            onefile_line.append(lines)
        Items.append(f"{eachfile}--->{onefile_line[index]}")
        #print(len(eachfile))
        results.insert(END,eachfile)
        results.yview(END)
    #print(Items)
        
#---------------------------------------------------------------------------------------------------#
initialdir = ""

def browse():
    global initialdir
    if entry.get() == "Browser for the Project Directory" or entry.get() == '':
        initialdir = "D:\\"
    else:
        initialdir = entry.get()
    dirname = filedialog.askdirectory(parent=root, initialdir=initialdir, title='Choose your Project Directory')
    entry.delete(0,END)
    entry.insert(0,dirname)

#---------------------------------------------------------------------------------------------------#
def start_search_thread(event):
    button_search.config(state = DISABLED)
    button_export.config(state = DISABLED)
    global search_thread
    search_thread = threading.Thread(target = search)
    search_thread.daemon = True
    progressbar.start()
    search_thread.start()
    root.after(20,check_search_thread)
#---------------------------------------------------------------------------------------------------#
def check_search_thread():
    if search_thread.is_alive():
        root.after(20,check_search_thread)
    else:
        progressbar.stop()
#---------------------------------------------------------------------------------------------------#
def get_path(path):
    p_list = path.split('\\')
    print(p_list)
    return "\\".join(p_list[:-1])

#---------------------------------------------------------------------------------------------------#
def res_listbox_click(event):
    w = event.widget
    index = w.curselection()[0]
    value = w.get(index)
    if value != "None":
        path = value
        #f_line = findings[index][0].split('[')[1].split(']')[0].split(',')[0]
        os.startfile(path)
#---------------------------------------------------------------------------------------------------#
def res_listbox_click1(event):
    try:
        w = event.widget
        index = w.curselection()[0]
        cat_list.delete(0,END)
        fulltext = findings[index]
        for i in fulltext:
            cat_list.insert(END,i)
    except:
        pass
#---------------------------------------------------------------------------------------------------#
def inp_listbox_click(event):
    w = event.widget
    index = w.curselection()[0]
    value = w.get(index)
    try:
        os.startfile(value)
    except:
        pass

 #---------------------------------------------------------------------------------------------------# 
def search():
    global count
    count = 0
    global Items
    global findings
    findings = []
    Items = []
    text_status.set("Scanning....")
    files_number.config(text = "")
    files_found.config(text = "")
    occurances.config(text = "")
    inputs.delete(0,END)
    results.delete(0,END)
    extensions = ext_entry.get().lower().split(',')

    #time.sleep(5)
    
    getFiles(entry.get(),extensions)
    text_status.set("Scanning Complete\t")
    button_export.config(state = "normal")
    button_search.config(state = "normal")
#---------------------------------------------------------------------------------------------------#
cid = []
line_n = []
auth = []
a_mail = []
a_time = []
committer = []
c_mail = []
c_time = []
summary = []
file_name = []
line_content = []

def structure(output):


    cid.append(output[0].split(' ')[0])
    line_n.append(output[0].split(' ')[1])
    auth.append(" ".join(output[1].split(' ')[1:]))
    a_mail.append(output[2].split(' ')[1])
    epoch = int(output[3].split(' ')[1])
    a_time.append(time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(epoch)))#+" "+output[4].split(' ')[1])
    committer.append(" ".join(output[5].split(' ')[1:]))
    c_mail.append(output[6].split(' ')[1])
    epoch = int(output[7].split(' ')[1])
    c_time.append(time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(epoch)))#+" "+output[8].split(' ')[1])
    summary.append(" ".join(output[9].split(' ')[1:]))
    file_name.append(" ".join(output[10].split(' ')[1:]))
    content = output[11][:]
    content = content.replace("\t"," ")
    content = content.replace("  ","")
    line_content.append(content)
#---------------------------------------------------------------------------------------------------#
def get_dataframe():

    df = pd.DataFrame({
        "Commit_Id" : cid, "Author" : auth, "Author_Mail" : a_mail, "Author_Time" : a_time, "Committer" : committer, "Committer_Mail" : c_mail,
        "Committer_Time" : c_time, "Summary" : summary, "File" : file_name, "Line_Number" : line_n, "Line" : line_content
        })
    return df




#---------------------------------------------------------------------------------------------------#
def export():
    
    errorflag = 0
    cid[:] = []
    line_n[:] = []
    auth[:] = []
    a_mail[:] = []
    a_time[:] = []
    committer[:] = []
    c_mail[:] = []
    c_time[:] = []
    summary[:] = []
    file_name[:] = []
    line_content[:] = []

    if len(Items) > 0:
        #with open(os.getcwd()+"\\git_blame.txt",'w') as f1:
        output = ""
        line_numbers = []
        for onefile in Items:
            path = onefile.split("--->")[0]
            #print(path)
            #output = output + path + "\n\n"
            lines = onefile.split("--->")[1].split(', ')
            lines = lines[:-1]
            line_numbers.append(lines)
            # for line in lines:
            #     try:
            #         line_numbers.append(line.split('(line')[1].replace(")","").replace(" ",""))
            #     except:
            #         pass
            # print(line_numbers)
        #print(line_numbers)
            for line in line_numbers:
                print(path)
                #git blame --line-porcelain file
                try:
                    p = subprocess.Popen(["git", "blame","--line-porcelain","-L", line+","+line, path],cwd = get_path(path),stdout = subprocess.PIPE)
                    output = p.stdout.read().decode("utf-8").split('\n')
                    structure(output)
                    p.kill()
                except:
                    print("There have been errors")
                    errorflag = 1

        if errorflag == 0:    
            df = get_dataframe()
            new_dir = os.getcwd()+"\\Blame_Reports\\"
            if os.path.isdir(new_dir) == False:
                os.makedirs(new_dir)
            writer = pd.ExcelWriter(new_dir+'git_blame'+str(len(os.listdir(new_dir))+1)+'.xlsx')
            df.to_excel(writer,'BlameSheet')
            writer.save()
            print("Blame Report is created")
        else:
            print("No Report is created")
                
    
    # else:
    #     print("Nothing to export")
            
#---------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    

    root  = Tk()
    root.config(background = 'light blue')
    root.geometry("1120x700")
    root.resizable(width=False, height=False)
    root.title("DASy Software Restrictions Scanner")

    upper = Frame(root,background  = 'light blue')
    upper.grid(row = 0,column = 0,padx = 40,pady = 20)

    Labelling = Frame(root,background  = 'light blue')
    Labelling.grid(row = 1,column = 0)

    lower = Frame(root,background  = 'light blue')
    lower.grid(row = 2,column = 0)

    lower_left = Frame(lower,background  = 'light blue')
    lower_left.grid(row = 0,column = 0,padx = 10)

    lower_right = Frame(lower,background  = 'light blue')
    lower_right.grid(row = 0,column = 1,padx = 5)

    extension_layout = Frame(root,background  = 'light blue')
    extension_layout.grid(row = 3,column = 0,pady = 10)

    forcheckbox = Frame(root,background  = 'light blue')
    forcheckbox.grid(row = 4,column = 0,pady = 10)

    category_field = Frame(root,background  = 'light blue')
    category_field.grid(row = 5,column = 0,pady = 10)

    down = Frame(root,background  = 'light blue')
    down.grid(row = 6,column = 0,pady = 10)


    entry = Entry(upper,width = 100,bd = 3)
    entry.grid(row = 0,column = 0)
    entry.config(font=("Times New Roman", 12))
    entry.insert(0,'Browser for the Project Directory')

    button_browse = Button(upper,text = "...",command = browse,width = 4,bd = 3,font=("Times New Roman", 10))
    button_browse.grid(row = 0,column = 1)

    button_search = Button(upper,text = "scan",command = lambda: start_search_thread(None),width = 5,bd = 3,font=("Times New Roman", 10))
    button_search.grid(row = 0,column = 2,padx = 5)

    button_export = Button(upper,text = "generate report",command = export,width = 13,bd = 3,font=("Times New Roman", 10))
    button_export.grid(row = 0,column = 3)

    inputLabel = Label(Labelling,text = "All Files",font=("Times New Roman", 12),anchor = 'w',width = 100)
    inputLabel.grid(row = 0,column = 0)
    inputLabel.config(background = 'light blue')

    resultLabel = Label(Labelling,text = "Files with hits",font=("Times New Roman", 12))
    resultLabel.grid(row = 0,column = 1)
    resultLabel.config(background = 'light blue')

    #   input listbox

    v_scrollbar_i = Scrollbar(lower_left,orient = VERTICAL,bd = 2) 
    h_scrollbar_i = Scrollbar(lower_left,orient = HORIZONTAL,bd = 2)

    inputs = Listbox(lower_left, width=65, height=12,
                   yscrollcommand = v_scrollbar_i.set,
                   xscrollcommand = h_scrollbar_i.set,
                   bd = 2)

    v_scrollbar_i.config(command=inputs.yview)
    h_scrollbar_i.config(command=inputs.xview)

    v_scrollbar_i.pack(side="right", fill="y")
    h_scrollbar_i.pack(side="bottom", fill="x")

    inputs.pack(side = LEFT)
    inputs.configure(font=("Times New Roman", 12))

    inputs.bind("<Double-Button>",inp_listbox_click)


    #   results listbox

    v_scrollbar = Scrollbar(lower_right,orient = VERTICAL,bd = 2) 
    h_scrollbar = Scrollbar(lower_right,orient = HORIZONTAL,bd = 2)

    results = Listbox(lower_right, width=65, height=12,
                   yscrollcommand = v_scrollbar.set,
                   xscrollcommand = h_scrollbar.set,
                   bd = 2)

    v_scrollbar.config(command=results.yview)
    h_scrollbar.config(command=results.xview)

    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")

    results.pack(side = LEFT)
    results.configure(font=("Times New Roman", 12))

    results.bind("<Double-Button>",res_listbox_click)
    results.bind("<<ListboxSelect>>",res_listbox_click1)

    ext_label = Label(extension_layout,text = "File extensions :  ",font=("Times New Roman", 12))
    ext_label.grid(row = 0,column = 0)
    ext_label.config(background = 'light blue')

    ext_entry = Entry(extension_layout,width = 100,bd = 3,font=("Times New Roman", 12))
    ext_entry.grid(row = 0,column = 1)
    ext_entry.insert(0,"c,cpp,h,hpp,txt,cmake")

    checkCmd = IntVar()
    checkCmd.set(0)
    checkBox = Checkbutton(forcheckbox, variable=checkCmd, onvalue=1, offvalue=0, text="Ignore Comments",background="light blue")
    checkBox.grid(row = 0, column = 0)

    cat_label = Label(category_field,text = "Warnings: ",font=("Times New Roman", 12))
    cat_label.pack(side = LEFT)
    cat_label.config(background = 'light blue')

    v_scrollbar_c = Scrollbar(category_field,orient = VERTICAL,bd = 2) 
    h_scrollbar_c = Scrollbar(category_field,orient = HORIZONTAL,bd = 2)

    cat_list = Listbox(category_field, width=100, height=8,
                   yscrollcommand = v_scrollbar_c.set,
                   xscrollcommand = h_scrollbar_c.set,
                   bd = 2)

    v_scrollbar_c.config(command=cat_list.yview)
    h_scrollbar_c.config(command=cat_list.xview)

    v_scrollbar_c.pack(side="right", fill="y")
    h_scrollbar_c.pack(side="bottom", fill="x")

    cat_list.pack(side = LEFT)
    cat_list.configure(font=("Times New Roman", 12))

    global text_status
    text_status = StringVar()
    status = Label(down,background = 'light blue',font=("Times New Roman", 12),textvariable = text_status)
    status.grid(row = 0, column = 1)

    files_number = Label(down,background = 'light blue',font=("Times New Roman", 12))
    files_number.grid(row = 0, column = 2)

    files_found = Label(down,background = 'light blue',font=("Times New Roman", 12))
    files_found.grid(row = 0, column = 3)

    occurances = Label(down,background = 'light blue',font=("Times New Roman", 12))
    occurances.grid(row = 0, column = 4)

    progressbar = ttk.Progressbar(down,mode = 'indeterminate')
    progressbar.grid(row = 0, column = 0)
    #root.iconbitmap('icon1.ico')
    root.mainloop()

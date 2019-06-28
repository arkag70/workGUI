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
from pathlib import Path

#git log -p
#git blame -L <start>,<end> full file name
Items = []
count = 0
counter = None
reason = []
libm_lib = "abs labs llabs fabs div ldiv lldiv fmod remainder remquo fma fmax fmin fdim nan nanf nanl exp exp2 expm1 log log2 log10 log1p ilogb logb sqrt cbrt hypot pow sin cos tan asin acos atan atan2 sinh cosh tanh asinh acosh atanh erf erfc lgamma tgamma ceil floor trunc round lround llround nearbyint rint lrint llrint frexp ldexp modf scalbn scalbln nextafter nexttoward copysign fpclassify isfinite isinf isnan isnormal signbit".split(" ")
libm_qnx = "acos acosf acosh acoshf asin asinf asinh asinhf atan atanf atan2 atan2f atanh atanhf cabs cabsf cbrt cbrtf ceil ceilf copysign copysignf cos cosf cosh coshf drem dremf erf erff erfc erfcf exp expf expm1 expm1f fabs fabsf finite finitef floor floorf fmod fmodf fp_exception_mask fp_exception_value fp_precision fp_rounding frexp frexpf gamma gamma_r gammaf gammaf_r hypot hypotf ilogb ilogbf isinf isinff isnan isnanf ldexp lgamma lgamma_r lgammaf lgammaf_r log logf log1p log1pf log10 log10f logb logbf modf modff nextafter nextafterf pow powf remainder remainderf rint rintf scalb scalbf scalbn scalbnf significand significandf sin sinf sinh sinhf sqrt sqrtf tan tanf tanh tanhf".split(" ")
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
        if "getutid(" in line or "getutid (" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_1676 lines: {lines}:- {reason}")

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
        for func in libm_qnx:
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
            
            return (f"StakeholderRS_Safety_DASy_3330_3329_3247 lines: {lines}:- {reason}")
        
    return 0
#-------------------------------------------------------------------------------------------------#

def category3_search(one_file):
    lines = []
    reason = '''An application SHALL NOT invoke the dup2 function while
simultaneously creating other new file descriptors.
The dup2 function can erroneously return EBADF if another thread in the
application creates a new file descriptor that matches the dup2 newfd parameter
at the same time the dup2 function is executing.'''
    for i,line in enumerate(one_file):
        if "dup2(" in line or "dup2 (" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_2597 lines: {lines}:- {reason}")
        
    return 0
#-------------------------------------------------------------------------------------------------#

def category4_search(one_file):
    lines = []
    reason = '''The QOS SHOULD be configured to ensure mutexes that are shared between processes are safe.

Note that in order to share a mutex, two processes must also share the memory in which the mutex resides.
If an application needs to share a mutex between separate processes, then it must either expose itself to potential interference from unrelated processes, disable priority inheritance, or accept a performance penalty as all operations on the shared mutex must enter the kernel.
Normal kernel configuration does not require that all mutex operations enter the kernel. This enhances the performance of mutex operations but, in such a system, a thread that corrupts a mutex (accidentally or maliciously) can cause the priority of an unrelated thread to be boosted to the first thread’s priority through the priority inheritance mechanism.

The kernel can be configured to reject attempts to lock shared mutexes that would cause a priority inheritance unless all mutex locking operations enter the kernel. This has a significant impact on the performance of shared mutexes, but guarantees that non-cooperating threads cannot interfere with each other. In order to use shared mutexes in a safe manner:
 The system must be configured to require that all mutex operations on shared mutexes that support priority inheritance must enter the kernel. This may be achieved by specifying the -s command-line option to procnto. (Note that this is the default for the QOS; see section A.3.2 Recommended procnto command-line options.)
 All mutexes that are to be shared between processes must either disable priority inheritance by setting the PTHREAD_PRIO_NONE flag or must be explicitly identified as a shared mutex by setting the PTHREAD_PROCESS_SHARED flag.

In a system where the -s option is specified, an attempt to lock a shared priority-inheriting mutex that does not have the THREAD_PROCESS_SHARED flag set will fail and return an error code. '''

    for i,line in enumerate(one_file):
        if ("pthread_mutexattr_getpshared(" in line or "pthread_mutexattr_getpshared (" in line) and not ("PTHREAD_PROCESS_SHARED" in line or "PTHREAD_PRIO_NONE" in line):
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_3315 lines: {lines}:- {reason}")
        
    return 0
#-------------------------------------------------------------------------------------------------#

def category5_search(one_file):
    lines = []
    reason = '''By default the clock period (rate at which clock ticks arrive, in
nanoseconds) will be 1 ms. If any other value is required, the value SHOULD be established by calling ClockPeriod() with the desired value at boot time, as early as possible, 
and ClockPeriod() shall be used only for reading the clock period thereafter.\n\n A thread that invokes the ClockPeriod() API MUST be bound to the
same CPU that handles clock interrupts. '''
    
    for i,line in enumerate(one_file):
        if "ClockPeriod(" in line or "ClockPeriod (" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_3309_2896 lines: {lines}:- {reason}")
    return 0
#-------------------------------------------------------------------------------------------------#

def category6_search(one_file):
    lines=[]
    reason = '''An application SHALL NOT invoke the mount_ifs utility.'''

    for i,line in enumerate(one_file):
        if "mount_ifs" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_2600 lines: {lines}:- {reason}")
    return 0
#-------------------------------------------------------------------------------------------------#

def category7_search(one_file):
    lines = []
    reason = '''A safety application SHALL NOT use the vfork() API. '''

    for i,line in enumerate(one_file):
        if "vfork(" in line or "vfork (" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_2888 lines: {lines}:- {reason}")
    return 0
#-------------------------------------------------------------------------------------------------#

def category8_search(one_file):
    lines = []
    reason = '''An application SHALL NOT invoke nftw unless the number
of available file descriptors exceeds the depth of the file tree.
The nftw function may use one file descriptor for each level of the tree, regardless
of the value of the depth parameter provided. '''

    for i,line in enumerate(one_file):
        if "nftw(" in line or "nftw (" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_2599 lines: {lines}:- {reason}")

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
        if "InterruptHookIdle(" in line or "InterruptHookIdle (" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_2598 lines: {lines}:- {reason}")

    return 0
#-------------------------------------------------------------------------------------------------#
def category10_search(one_file):
    lines = []
    reason = '''Description
It is highly recommended that the system does not use the  high precision event timer (HPET) functions derived 
from the Platform Control Cluster (PCC) as sub-part of the ITSS during the Power On Reset, Initialization and 
Operational state of the safety critical application.
Rationale
The high precision event timer functions derived from platform control cluster were considered as not safety 
relevant during the failure analysis.
Informative
Instead of HPET as a source of timer interrupts, the Atom core internal timers shall be used. '''
    
    for i,line in enumerate(one_file):
        if "use_hpet_timer" in line or "init_qtime_hpet(" in line or "init_qtime_hpet (" in line:
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_2859 lines: {lines}:- {reason}")
    return 0
#-------------------------------------------------------------------------------------------------#
def category11_search(one_file):
    lines = []
    reason = '''Safety applications SHOULD make use of the functionality provided by the _NTO_COF_NOEVENT and/or _NTO_COF_REG_EVENTS connection flags, 
    specified to the ConnectAttach() or ConnectFlags() APIS, to ensure application isolation.
    Servers may accidentally or maliciously deliver events to clients that the clients are not prepared to handle. If the _NTO_COF_NOEVENT flag is specified for a connection, 
    then the server is forbidden from delivering any events to the client. 
    If the _NTO_COF_REG_EVENTS flag is specified for a connection, then the server is forbidden from delivering any event to the client excepting those that the client has registered using the MsgRegisterEvent() API. '''

    for i,line in enumerate(one_file):
        if ("ConnectAttach(" in line or "ConnectAttach (" in line or "ConnectFlags(" in line or "ConnectFlags (" in line) and (("_NTO_COF_NOEVENT" not in line) or ("_NTO_COF_REG_EVENTS" not in line)):  
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_3316 lines: {lines}:- {reason}")

    return 0
#-------------------------------------------------------------------------------------------------#
def category12_search(one_file):
    lines = []
    reason = '''The developer SHALL ensure that, if an interrupt is configured
to be lazy, careful analysis shows that any potential data loss will not
result in a violation of an application’s safety requirements. '''

    for i,line in enumerate(one_file):
        if "InterruptCharacteristic(" in line or "InterruptCharacteristic (" in line:  
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_2589 lines: {lines}:- {reason}")

    return 0
#-------------------------------------------------------------------------------------------------#
def category13_search(one_file):
    #safety
    lines = []
    reason = '''A developer SHOULD NOT use inline assembly in the development of an application that implements a safety function.
The use of inline assembly is discouraged, as the practice is highly error prone. Errors introduced in inline assembly are often subtle and difficult to detect. '''
    for i,line in enumerate(one_file):
        if "asm(" in line or "asm (" in line or "__asm__(" in line or "__asm__ (" in line:  
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_2928 lines: {lines}:- {reason}")
    return 0
#-------------------------------------------------------------------------------------------------#
def category14_search(one_file):
    #safety
    lines = []
    reason = '''A safety application SHALL NOT modify MALLOC_BAND_CONFIG_STR after system start-up '''
    for i,line in enumerate(one_file):
        if ("setenv(" in line or "setenv (" in line) and ("MALLOC_BAND_CONFIG_STR" in line):  
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_2889 lines: {lines}:- {reason}")
    return 0
#-------------------------------------------------------------------------------------------------#
# def category15_search(one_file):
#     #safety
#     lines = []
#     reason = '''An application SHALL set the LD_BIND_NOW environment variable to ensure immediate symbol resolution during application loading. '''
#     for i,line in enumerate(one_file):
#         if ("setenv(" in line or "setenv (" in line) and ("LD_BIND_NOW" in line):  
#             lines.append(i+1)
#     if len(lines) > 0:
#         return (f"StakeholderRS_Safety_DASy_2602 lines: {lines}:- {reason}")
#     return 0
#-------------------------------------------------------------------------------------------------#

def category16_search(one_file):
    #safety
    lines = []
    reason = '''A developer SHOULD NOT use thread cancellation in the development of an application that implements a safety function.

The use of thread cancellation is highly discouraged, as the practice is highly error prone and can lead to unintended resource leaks,
 execution behaviours because of unintended cancellation or the masking of cancellation due to changing the cancellation state.
 Errors introduced with thread cancellation are often subtle and difficult to detect and thus we recommend using a controlled and architected thread termination lifecycle that is co-ordinated. '''
    for i,line in enumerate(one_file):
        if "pthread_cancel(" in line or "pthread_cancel (" in line:  
            lines.append(i+1)
    if len(lines) > 0:
        return (f"StakeholderRS_Safety_DASy_3321 lines: {lines}:- {reason}")
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
    a = category9_search(one_file)
    if a!=0:
        issues.append(a)
    a = category10_search(one_file)
    if a!=0:
        issues.append(a)
    a = category11_search(one_file)
    if a!=0:
        issues.append(a)
    a = category12_search(one_file)
    if a!=0:
        issues.append(a)
    a = category13_search(one_file)
    if a!=0:
        issues.append(a)
    a = category14_search(one_file)
    if a!=0:
        issues.append(a)
    # a = category15_search(one_file)
    # if a!=0:
    #     issues.append(a)
    a = category16_search(one_file)
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
req = []
requirements = ""
linewise_req = []
def getFiles(path,extensions):
    global linewise_req
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
                        full = os.path.join(r, file).replace("\\","/")
                        if "build/" not in full:
                            files.append(full)
        #print(files[0])
    
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

    for file in findings:
        for i in file:
            req.append(i.split(':')[:2])
    for r in req:
        lines = r[1].split('[')[1].split(']')[0].split(',')
        global requirements
        requirements += (r[0]+" ") * (len(lines))
    requirements = requirements.replace("lines ","")
    for r in requirements.split(' '):
        linewise_req.append(r) 
    linewise_req = linewise_req[:-1]
    temp_req = []
    for i in linewise_req:
        temp_req.append(",".join(i.split('_')[3:]))
    linewise_req = temp_req
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
def start_export_thread(event):
    button_search.config(state = DISABLED)
    button_export.config(state = DISABLED)
    global export_thread
    export_thread = threading.Thread(target = export)
    export_thread.daemon = True
    progressbar.start()
    export_thread.start()
    root.after(20,check_export_thread)
#---------------------------------------------------------------------------------------------------#

def check_search_thread():
    if search_thread.is_alive():
        root.after(20,check_search_thread)
    else:
        progressbar.stop()
#---------------------------------------------------------------------------------------------------#
def check_export_thread():
    if export_thread.is_alive():
        root.after(20,check_export_thread)
    else:
        progressbar.stop()
#---------------------------------------------------------------------------------------------------#

def get_path(path):
    p_list = path.split('/')
    return "\\".join(p_list[:-1])

#---------------------------------------------------------------------------------------------------#
def res_listbox_click(event):
    w = event.widget
    index = w.curselection()[0]
    value = w.get(index)
    if value != "None":
        path = value
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
    global req
    global requirements
    req = []
    requirements = ""
    count = 0
    global Items
    global findings
    global linewise_req
    linewise_req = []
    findings = []
    Items = []
    text_status.set("Scanning....")
    files_number.config(text = "")
    files_found.config(text = "")
    occurances.config(text = "")
    inputs.delete(0,END)
    results.delete(0,END)
    cat_list.delete(0,END)
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
rid = []

def structure(output):

    cid.append(output[0].split(' ')[0])
    line_n.append(output[0].split(' ')[2])
    committer.append(" ".join(output[5].split(' ')[1:]))
    c_mail.append(output[6].split(' ')[1])
    epoch = int(output[7].split(' ')[1])
    c_time.append(time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(epoch)))
    summary.append(" ".join(output[9].split(' ')[1:]))
    file_name.append(" ".join(output[10].split(' ')[-1]))
    if "filename" in output[11]:
        content = output[12][:]
    else:
        content = output[11][:]
    content = content.replace("\t"," ")
    content = content.replace("  ","")
    line_content.append(content)
#---------------------------------------------------------------------------------------------------#
def get_dataframe():

    df = pd.DataFrame({
        "Requirement_Id" : linewise_req, "Commit_Id" : cid, "Committer" : committer, "Committer_Mail" : c_mail,
        "Committer_Time" : c_time, "Commit_message" : summary, "File" : file_name, "Line_Number" : line_n, "Line" : line_content
        })
    return df




#---------------------------------------------------------------------------------------------------#
def export():
    text_status.set("Generating Report....")
    errorflag = 0
    rid[:] = []
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
        output = ""
        for onefile in Items:
            path = onefile.split("--->")[0]
            lines = onefile.split("--->")[1].split(', ')
            lines = lines[:-1]
            for line in lines:
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

            writer = pd.ExcelWriter(new_dir+"Project_Application_Deviation_Report"+str(len(os.listdir(new_dir))+1)+'.xlsx')
            df.to_excel(writer,'BlameSheet')
            writer.save()
            print("Blame Report is created")
            text_status.set("Blame Report is created\t")
        else:
            print("No Report is created")
            text_status.set("No Report is created\t")

        
        button_export.config(state = "normal")
        button_search.config(state = "normal")
                
    
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

    button_export = Button(upper,text = "generate report",command =  lambda: start_export_thread(None),width = 13,bd = 3,font=("Times New Roman", 10))
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

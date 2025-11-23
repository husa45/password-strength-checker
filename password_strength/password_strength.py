import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import hashlib
import requests
def check_internet_connectivity(url="https://www.google.com/", timeout=5):
    try:
        requests.get(url,timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
check_internet_connectivity()
class PasswordCheck:
    """
    This class creates the GUI interface
    with implementing All functionality
    """
    def __init__(self):
        #temp variables:
        self.temp_start=0
        self.temp_end = 0
        self.temp_update=0
        #defining the main app window :
        self.root=tk.Tk()
        self.root.geometry("700x500")
        self.root.title("Password strength checker")
        #self.root.resizable(False,False)
        self.background_image=tk.PhotoImage(file='config/paper-background.png')
        self.background_label = tk.Label(master=self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        #defining window features :
        self.label1=tk.Label(master=self.root,text="Enter password",bg="#f5f2e8",fg="black",font=('Roman Times',10,"bold"))
        self.password_entry=tk.Entry(master=self.root,width=24,font=('Roman Times',10,"bold"))
        self.check_pass_but=tk.Button(master=self.root,width=15,height=1,text="Check Password",font=('Roman Times',10,"bold"),command=self.check_password)
        self.label1.place(x=50,y=150)
        self.password_entry.place(x=200, y=150)
        self.check_pass_but.place(x=500,y=150)

        self.style=ttk.Style()
        self.style.theme_use("default")
        self.style.configure("big.Horizontal.TProgressbar",
                             thickness=25
                             )
        self.prg1=ttk.Progressbar(master=self.root,length=280,mode='determinate',maximum=100,value=0,style="big.Horizontal.TProgressbar")

        self.prg1.place(x=200,y=285)
        self.label2 = tk.Label(master=self.root, text="Strength", bg="#f5f2e8", fg="black",
                               font=('Roman Times', 10, "bold"))
        self.label2.place(x=50, y=285)

        self.strength_label=tk.Label(master=self.root)
        self.pwned_label=tk.Label(master=self.root)
        self.root.mainloop()
    def animate(self):
        self.temp_start+=self.temp_update
        self.prg1['value']=self.temp_start
        if self.temp_start!=self.temp_end:
            self.root.after(5,self.animate)
    def progress_move(self,current,target):
        """
        This function handles progress bar updating in
        A smooth graphical way.
        """
        self.temp_start=current
        self.temp_end=target
        if current<target:
            self.temp_update=1
        elif current>target:
            self.temp_update=-1
        else:
            return
        self.animate()
    def check_password(self):
        """
        This function implements password strength checking .
        """
        entered_pass:'str'=self.password_entry.get()
        length:'int'=len(entered_pass)
        strength:'str'=""
        progress:'int'=0
        self.strength_label.destroy()
        # defining styles :
        style1, style2, style3, style4 = ttk.Style(), ttk.Style(), ttk.Style(), ttk.Style()
        style1.configure("Red.Horizontal.TProgressbar",
                         background="red",thickness=25
                         )
        style2.configure("Yellow.Horizontal.TProgressbar",
                         background="yellow",thickness=25
                         )
        style3.configure("Green.Horizontal.TProgressbar",
                         background="green",thickness=25
                         )
        style4.configure("Blue.Horizontal.TProgressbar",
                         background="blue",thickness=25
                         )
        current_progress:'int'=self.prg1['value']
        #checking strength :
        if length<=4 or re.match(r'^(\d+)$',entered_pass) or re.match(r'^([a-zA-Z]+)$',entered_pass) or re.match(r'^(\W+)$',entered_pass):
            self.prg1.configure(style="Red.Horizontal.TProgressbar")
            #very weak password:
            if  re.search('[^a-zA-Z0-9]',entered_pass):
                progress +=5
            if re.search(r'[A-Z]', entered_pass):
                progress +=5
            if re.search(r'[a-z]', entered_pass):
                progress +=5
            if re.search(r'[0-9]', entered_pass):
                progress +=5
            self.progress_move(current_progress,0+progress)
            strength="Very Weak"
        elif length>=5 and length<8:
            self.prg1.configure(style="Yellow.Horizontal.TProgressbar")
            #weak password :
            if re.search('[^a-zA-Z0-9]', entered_pass):
                progress += 5
            if re.search(r'[A-Z]', entered_pass):
                progress += 5
            if re.search(r'[a-z]', entered_pass):
                progress += 5
            if re.search(r'[0-9]', entered_pass):
                progress += 5
            self.progress_move(current_progress, 20 + progress)
            strength = "Weak"
        elif length>=8 and length<=12:
            self.prg1.configure(style="Green.Horizontal.TProgressbar")
            #strong password:
            if re.search('[^a-zA-Z0-9]', entered_pass):
                progress += 10
            if re.search(r'[A-Z]', entered_pass):
                progress += 10
            if re.search(r'[a-z]', entered_pass):
                progress += 10
            if re.search(r'[0-9]', entered_pass):
                progress += 10
            self.progress_move(current_progress, 40 + progress)
            strength="Strong"
        elif length>=13:
            self.prg1.configure(style="Blue.Horizontal.TProgressbar")
            #very strong password:
            if re.search('[^a-zA-Z0-9]', entered_pass):
                progress +=5
            if re.search(r'[A-Z]', entered_pass):
                progress +=5
            if re.search(r'[a-z]', entered_pass):
                progress +=5
            if re.search(r'[0-9]',entered_pass):
                progress +=5
            self.progress_move(current_progress, 80 + progress)
            strength="Very Strong"
        # destroying old label ,and reconfiguring the new :
        self.strength_label=tk.Label(master=self.root,text=f"Password is {strength}",fg=("black" if strength!="Very Weak" and strength!="Weak" else "red"),bg="#f5f2e8",font=('Roman Times',9,"bold"))
        self.strength_label.place(x=500, y=285)
        #checking if the password was exposed in  a data breach :
        self.was_exposed(entered_pass)
    def was_exposed(self,password:"str")->'None':
        """
        This function implements password pwning state ,
        that is , was it exposed in previous data breaches or not ,
        however ,this shouldn't be taken as the only measure ,because sometimes
        the password may not have been exposed in a data breache ,but is considered weak .
        Password strength bar provides a better indication.
        """
        #checking internet connectivity :
        if not check_internet_connectivity():
            self.pwned_label.destroy()
            messagebox.showerror(title="Connection error",
                                 message="You need to be connected to the internet To use pwnd api")
            return
        #the main script :
        password_hash=hashlib.sha1(password.encode()).hexdigest().upper()
        password_hash_prefix=password_hash[:5]
        r=requests.get(f'https://api.pwnedpasswords.com/range/{password_hash_prefix}')
        pwned_list=r.text.splitlines()
        hashes={}
        for line in pwned_list:
            parts=line.split(':')
            hashes[parts[0]]=parts[1]
        #checking if the password is in the breach :
        self.pwned_label.destroy()
        self.pwned_label=tk.Label(master=self.root,bg="#f5f2e8",
                               font=('Roman Times', 12, "bold"))
        for hash_suffix,occurence  in hashes.items():
            if (password_hash_prefix+hash_suffix)==password_hash:
                self.pwned_label.config(text=f"\tOh no — pwned!\n\tThis password was seen {occurence} \n\ttimes before in data breaches !",fg="red")
                self.pwned_label.place(x=80,y=375)
                return
            self.pwned_label.config(
                text=f"Good news — no pwnage found!\nThis password wasn't  seen in any recent  data breach",
                fg="green")
            self.pwned_label.place(x=80,y=375)

PasswordCheck()
import json
import random
import webbrowser
from tkinter import *
from tkinter import messagebox

import bcrypt

from sifreleme import crypt

basla = False
logged_in_email = ""
logged_in_password = ""

# ---------------------------- WARNING ------------------------------- #
warning = Tk()
warning.title("Password Manager")
warning.config(padx=20, pady=20)
# warning.config(padx=20, pady=20)
warning_label1 = Label(warning,text="WARNING!",font='"Times New Roman" 14 bold',fg="RED").pack()
warning_label2=Label(warning,font='"Times New Roman" 12',text=
         "This program uses modern cryptography and very complex hash algorithms.\n"
         "If you forget your login email or password, it is impossible to retrieve.\n"
         "The software developer does not take any responsibility.\n").pack()
warning_label3 = Label(warning,text="UYARI!",font='"Times New Roman" 14 bold',fg="RED").pack()
warning_label4=Label(warning,font='"Times New Roman" 12',text=
         "Bu program, modern kriptografi ve karmaşık hash algoritmaları kullanır.\n"
         "Giriş e-postanızı veya parolanızı unutursanız geri almanız imkansızdır.\n"
         "Yazılım geliştirici herhangi bir sorumluluk kabul etmez.\n\n"
         "Hikmet Alper Başeğmez").pack()

try:
    from ctypes import windll

    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

# Set window icon.
photo = PhotoImage(file="icon.ico")
warning.iconphoto(True, photo)
warning.mainloop()


# ---------------------------- LOGIN ------------------------------- #
def cont():
    global basla, logged_in_email, logged_in_password
    basla = True
    logged_in_email = email_login.get()
    logged_in_password = pword_login.get()
    login.destroy()


def login_check(a=""):
    pword_login_f = pword_login.get().encode()
    email_login_f = email_login.get()
    try:
        with open("login.json", mode="r") as file:
            data = json.load(file)
            if email_login_f in data:
                if bcrypt.checkpw(pword_login_f, data[email_login_f].encode('ISO-8859-1')):
                    messagebox.showinfo("Başarılı!", "Giriş Başarılı!")
                    cont()
                else:
                    messagebox.showinfo("HATA!", message="Yanlış Email/Şifre!")
                    pword_login.delete(0,END)
                    email_login.delete(0,END)
            else:
                messagebox.showinfo("HATA!", message="Yanlış Email/Şifre!")
                pword_login.delete(0, END)
                email_login.delete(0, END)
    except FileNotFoundError:
        messagebox.showinfo(title="HATA!", message="Henüz bir kayıt yok")
        pword_login.delete(0, END)
        email_login.delete(0, END)


def login_new():
    pword_login_new = pword_login.get().encode()
    email_login_new = email_login.get()
    login_salt = bcrypt.gensalt(10)
    login_hashed = bcrypt.hashpw(pword_login_new, login_salt)

    new_login = {
        email_login_new: login_hashed.decode('unicode-escape')
    }
    try:
        with open("login.json", mode="r") as file:
            data = json.load(file)
            if email_login_new in data:
                messagebox.showinfo("HATA!", "Bu email ile bir kayıt zaten mevcut.")
                return
            data.update(new_login)
    except FileNotFoundError:
        data = new_login

    with open("login.json", mode="w") as file:
        json.dump(data, file, indent=4)
    messagebox.showinfo("Başarılı", "Yeni Kayıt Oluşturuldu!")
    cont()


login = Tk()
login.title("Password Manager")
login.config(padx=20, pady=20)
email_label = Label(text="Email:       ")
email_label.grid(row=1, column=1)
email_login = Entry()
email_login.grid(row=1, column=2, sticky="EW")
email_login.focus()
pword_label = Label(text="Password: ")
pword_label.grid(row=2, column=1)
pword_login = Entry(show="*", width=15)
pword_login.grid(row=2, column=2, sticky="EW")
button_login = Button(text="Login", command=login_check)
button_login.grid(row=1, column=3, sticky="EW")
button_newuser = Button(text="New User", command=login_new)
button_newuser.grid(row=2, column=3, sticky="EW")
login.bind('<Return>', login_check)
login.mainloop()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def clear():
    website.delete(0, END)
    pword.delete(0, END)
    website.focus()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def pas():
    pword.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char
    pword.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_ = website.get().lower()
    pword_ = pword.get()
    email_ = email.get()
    if not website_ or not pword_:
        messagebox.showinfo(title="OOPS", message="Boş bırakılamaz!")
        return
    encrypted_data = crypt(logged_in_password, "en", pword_)

    new_data = {
        website_:
            {
                "email": email_,
                "password": encrypted_data[0].decode('unicode-escape'),
                "salt": encrypted_data[1].decode('unicode-escape')
            }
    }

    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
            if logged_in_email not in data:
                data[logged_in_email] = {}
            data[logged_in_email].update(new_data)

    except FileNotFoundError:
        data = {logged_in_email: new_data}

    with open("data.json", mode="w") as file:
        json.dump(data, file, indent=4)
    messagebox.showinfo("Başarılı!","Kayıt Başarılı!")
    website.delete(0, END)
    pword.delete(0, END)
    website.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #

def ara():
    website_ara = website.get().lower()
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
            if website_ara in data[logged_in_email]:
                pword_ara_en = data[logged_in_email][website_ara]['password'].encode('ISO-8859-1')
                salt_ara = data[logged_in_email][website_ara]['salt'].encode('ISO-8859-1')
                pword_ara_de = crypt(logged_in_password, "de", hashed=pword_ara_en, salt_=salt_ara)
                pword.delete(0, END)
                pword.insert(0, pword_ara_de.decode())
                email.delete(0, END)
                email.insert(0, data[logged_in_email][website_ara]['email'])
                messagebox.showinfo("Başarılı!", "Aradığınız kayıt bulundu")
                webbrowser.open(f"{website_ara}.com")
            else:
                messagebox.showinfo("HATA!", message="Kayıt Bulunamadı!")
    except FileNotFoundError:
        messagebox.showinfo(title="HATA!", message="Henüz bir dosya yok")


# ---------------------------- UI SETUP ------------------------------- #
def pop():
    def close():
        website.delete(0, END)
        website.insert(0, selected.get())
        ara()
        popup.destroy()

    popup = Toplevel(window)
    popup.title("Website Registry")
    popup.geometry("200x300")
    pop_label = Label(popup, text="Registered Websites")
    pop_label.grid(row=1, column=1)
    with open("data.json", mode="r") as file:
        data = json.load(file)
        selected = StringVar()
        a = 2
        for each in data[logged_in_email]:
            radio = Radiobutton(popup, text=each, value=each, variable=selected, tristatevalue="fsjha1")
            radio.grid(row=a, column=1, sticky="W")
            a += 1
    select_website = Button(popup, text="    Select   ", command=close)
    select_website.grid(row=(a + 4), column=1, sticky="W")


if basla:
    window = Tk()
    window.title("Password Manager")
    window.config(padx=20, pady=20)
    kanvas = Canvas(width=200, height=200, highlightthickness=0)
    img = PhotoImage(file="logo.png")
    kanvas.create_image(100, 100, image=img)
    kanvas.grid(row=1, column=2)
    label1 = Label(text="Website: ")
    label2 = Label(text="Email/Username: ")
    label3 = Label(text="Password: ")
    label1.grid(row=2, column=1)
    label2.grid(row=3, column=1)
    label3.grid(row=4, column=1)
    website = Entry()
    website.grid(row=2, column=2, sticky="EW")
    website.focus()
    email = Entry()
    email.grid(row=3, column=2, sticky="EW")
    email.insert(0, logged_in_email)
    pword = Entry()
    pword.grid(row=4, column=2, sticky="EW")
    button_gp = Button(text="Generate Password", command=pas)
    button_gp.grid(row=4, column=3)
    button_list = Button(text="Registered Websites", command=pop, bg="#Ffa900")
    button_list.grid(row=3, column=3, sticky="EW")
    button_add = Button(text="Add", command=save)
    button_add.grid(row=5, column=2, sticky="EW")
    button_clear = Button(text="Clear", command=clear)
    button_clear.grid(row=5, column=3, sticky="EW")
    button_search = Button(text="Search", command=ara)
    button_search.grid(row=2, column=3, sticky="EW")
    window.mainloop()
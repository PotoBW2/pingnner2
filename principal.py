from tkinter import *
from tkinter import ttk

from utiles import resource_path

raiz = Tk()
raiz.title("Pingnner v2.00")
raiz.resizable(False, False)
raiz.iconbitmap(resource_path("image/logo2.ico"))

f_principal = ttk.Frame(raiz, padding=10, )
f_principal.grid()
f_new_dir = ttk.Frame(f_principal, padding=10, )
f_new_dir.grid(column=0, row=0)






raiz.update()
raiz.geometry("+" + str(round(raiz.winfo_screenwidth() / 2 - raiz.winfo_reqwidth() / 2)) + "+" + str(
    round(raiz.winfo_screenheight() / 2 - raiz.winfo_reqheight() / 2)))
raiz.update()

raiz.mainloop()

import tkinter as tk

root = tk.Tk()
root.title("Das ist ein Testfenster")
root.geometry("600x800")
root.minsize(width=250, height=250)
root.maxsize(width=250, height=250)
root.resizable(width=False,height=False)
label1 = tk.Label(root, text="Hallo Welt",bg="green")
label1.pack()
root.mainloop()

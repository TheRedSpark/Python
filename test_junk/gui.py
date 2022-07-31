import tkinter as tk


root = tk.Tk()
root.title("Das ist ein Testfenster")
root.geometry("600x800")
label1 = tk.Label(root, text="Hallo Welt")
label1.pack()
root.mainloop()

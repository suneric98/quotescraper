import tkinter as tk

class Gui:
    label_text = [
        "Loading .",
        "Loading . .",
        "Loading . . ."
    ]
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label_index = 0
        self.label_txt = tk.StringVar()
        self.label_txt.set(self.label_text[self.label_index])

        self.label = tk.Label(master, textvariable = self.label_txt)
        self.label.bind("<Button-1>",self.cycle_label_text)

        self.greet_button = tk.Button(master, text="Greet", command=self.greet)

        self.close_button = tk.Button(master, text="Close", command=master.quit)
        
        self.label.pack()
        self.greet_button.pack()
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

    def cycle_label_text(self, event):
        self.label_index += 1
        self.label_index %= len(self.label_text)
        self.label_txt.set(self.label_text[self.label_index])

root = tk.Tk()
my_gui = Gui(root)
root.mainloop()
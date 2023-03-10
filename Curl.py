#!/usr/bin/python3
# Import necessary modules.
from typing import List
from tkinter import *
from tkinter import messagebox
from subprocess import check_output
from platform import system

# Set DPI awareness if OS is Windows.
if system() == "Windows":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

# Create a class called MainWindow that inherits from the Tk class.
class MainWindow(Tk):
    # Define the constructor for the MainWindow class.
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.title(string="Curl")
        self.bind("<Key>", self.input)
        self.argument = StringVar(master=self, value="-I")
        self.url = StringVar(master=self, value="https://www.example.com")

        # Create GUI elements using the grid layout manager.
        Label(master=self, text="Argument:").grid(row=0, column=0)
        Entry(master=self, textvariable=self.argument, foreground="green", width=35).grid(row=0, column=1)

        Label(master=self, text="URL:").grid(row=1, column=0)
        Entry(master=self, textvariable=self.url, foreground="green", width=35).grid(row=1, column=1)

        Button(master=self, text="Exit (ESC)", command=self.quit).grid(row=2, column=0)
        Button(master=self, text="Response (⏎)", command=self.submit).grid(row=2, column=1)

        self.response = Text(master=self)
        self.ys = Scrollbar(master=self, orient="vertical", command=self.response.yview)
        self.response["yscrollcommand"] = self.ys.set
        self.response.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.ys.grid(row=4, column=2, sticky="ns")

        # Make the window resizable and set minimum size.
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.minsize(width=400, height=300)


    # Submit method for sending curl command and displaying response.
    def submit(self) -> None:
        try:
            arguments: str = self.argument.get()
            url: str = self.url.get()
            command: List[str] = f"curl -s {arguments} {url}".split()
            response: bytes = check_output(args=command)
            self.response.delete(index1=0.1, index2=END)
            self.response.insert(index=0.1, chars=response)
        except Exception as error:
            messagebox.showerror(title="Error", message=error)

    # Method for handling keyboard input.
    def input(self, event) -> None:
        if (event.keysym == "Return"):
            self.submit()
        elif (event.keysym == "Escape"):
            self.destroy()

# Start the application.
if __name__ == "__main__":
    try:
        MainWindow = MainWindow()
        MainWindow.mainloop()
    except KeyboardInterrupt:
        MainWindow.quit()

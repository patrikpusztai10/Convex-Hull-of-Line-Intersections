from tkinter import *
import tkinter.font as tkfont
from tkinter import ttk
from tkinter import messagebox
from lineintersection import LineIntersection

class Application:
    @staticmethod
    def check_nr(a):
        return a.isdigit() and int(a) > 0

    def onClick(self):
        a = self.nr_lines.get()
        minx= self.l_X.get()
        maxx= self.u_X.get()
        miny= self.l_Y.get()
        maxy= self.u_Y.get()
        if not ((minx[0]=='-' and minx[1:].isdigit())or minx.isdigit()) or not ((maxx[0]=='-' and maxx[1:].isdigit())or maxx.isdigit()) or not((miny[0]=='-' and miny[1:].isdigit())or miny.isdigit())  or not ((maxy[0]=='-' and maxy[1:].isdigit())or maxy.isdigit()) :
            messagebox.showerror("Error", "Bound is not an integer")
        elif int(minx)>=int(maxx):
            messagebox.showerror("Error", "Incorrect values for x")
        elif int(miny)>=int(maxy):
            messagebox.showerror("Error", "Incorrect values for y")
        elif int(maxx)-int(minx)<5 and int(maxy)-int(miny)<5:
            messagebox.showwarning("Warning", "The range for the coordinates is too small, we suggest a bigger range")
        elif not self.check_nr(a):
            messagebox.showerror("Error", "Number of lines is not a positive integer greater than 0")
        else:
            self.change()

    def selectli(self):
        return self.li.get()

    def selectch(self):
        return self.ch.get()

    def root_destroy(self):
        self.root.destroy()

    def change(self):
        minx = int(self.l_X.get())
        maxx = int(self.u_X.get())
        miny = int(self.l_Y.get())
        maxy = int(self.u_Y.get())
        LineIntersection(self.root_destroy, minx, maxx, miny, maxy, str(self.nr_lines.get()), self.selectli(), self.selectch())

    def start_application(self):
        Application()

    def __init__(self):
        self.root = Tk()
        self.root.title("Computational Geometry Project")
        self.root.geometry("1600x900")
        self.title_font = tkfont.Font(family="Helvetica", size=18, underline=True)
        self.font = tkfont.Font(family="Helvetica", size=14)

        self.title = Label(self.root, text="Convex hull of line intersections", font=self.title_font, fg="blue")
        self.title.pack(pady=60)

        # X Coordinates

        self.xFrame = Frame(self.root)
        self.xFrame.pack(pady=5, padx=10, anchor="w")
        self.x_Text = Label(self.xFrame, justify="left",
                            text="Select the lower and upper bound for the x coordinates:",
                            font=self.font)
        self.x_Text.grid(row=0, column=0, padx=5)

        self.l_X = Entry(self.xFrame, width=10, justify='center', font=('Helvetica', 12, 'normal'))
        self.l_X.grid(row=0, column=1, padx=5)
        self.u_X = Entry(self.xFrame, width=10, justify='center', font=('Helvetica', 12, 'normal'))
        self.u_X.grid(row=0, column=2, padx=5)

        # Y Coordinates

        self.yFrame = Frame(self.root)
        self.y_Text = Label(self.yFrame, justify="left",
                            text="Select the lower and upper bound for the y coordinates:",
                            font=self.font)
        self.y_Text.grid(row=0, column=0, padx=5)
        self.yFrame.pack(pady=5, padx=10, anchor="w")

        self.l_Y = Entry(self.yFrame, width=10, justify='center', font=('Helvetica', 12, 'normal'))
        self.l_Y.grid(row=0, column=1, padx=5)
        self.u_Y = Entry(self.yFrame, width=10, justify='center', font=('Helvetica', 12, 'normal'))
        self.u_Y.grid(row=0, column=2, padx=5)

        self.lineText = Label(self.root, justify="left",
                              text="Select the number of lines which will be used for the computation:",
                              font=self.font)
        self.lineText.pack(pady=25, padx=10, anchor="w")
        self.nr_lines = Entry(self.root, width=35, justify='left', font=('Helvetica', 13, 'normal'))
        self.nr_lines.pack(padx=15, anchor="w")

        self.nr_line_text = Label(self.root, justify="left", text="Select an algorithm to achieve the line intersections:",
                                  font=self.font)
        self.nr_line_text.pack(pady=15, padx=10, anchor="w")

        style = ttk.Style(self.root)
        style.configure(
            "Customized.TRadiobutton",
            font=('Helvetica', 14),
            indicatorsize=18,
            indicatorrelief=FLAT
        )

        self.li = IntVar(value=1)
        #First we ask user for line intersections algorithms
        ttk.Radiobutton(self.root, text="Cramer's Rule", variable=self.li, value=1,
                        style="Customized.TRadiobutton", command=self.selectli).pack(
            padx=15, pady=1, anchor='w')
        ttk.Radiobutton(self.root, text='Bentley-Ottmann Line Sweep', variable=self.li, value=2,
                        style="Customized.TRadiobutton", command=self.selectli).pack(
            padx=15, pady=3, anchor='w')

        # Second we ask user to choose between 3 algorithms for convex hulls
        self.ch = IntVar(value=1)
        self.ConvexHullText = Label(self.root, justify="left", text="Select an algorithm to create the convex hull:",
                                    font=self.font)
        self.ConvexHullText.pack(pady=20, padx=10, anchor="w")


        ttk.Radiobutton(self.root, text='Jarvis March', variable=self.ch, value=1, command=self.selectch,
                        style="Customized.TRadiobutton").pack(
            padx=15, pady=1, anchor='w')
        ttk.Radiobutton(self.root, text='Graham Scan', variable=self.ch, value=2, command=self.selectch,
                        style="Customized.TRadiobutton").pack(
            padx=15, pady=3, anchor='w')
        ttk.Radiobutton(self.root, text="Andrew's variant of the Graham scan", variable=self.ch, value=3,
                        command=self.selectch, style="Customized.TRadiobutton").pack(
            padx=15, pady=3, anchor='w')

        self.submitButton = Button(self.root, text="Submit", font=self.font, bg='blue', fg='white',
                                   command=self.onClick)
        self.submitButton.pack(pady=10)

        self.root.mainloop()

Application()

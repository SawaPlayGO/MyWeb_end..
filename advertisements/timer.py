from tkinter import *


win = Tk()

time = 400
def update_timer():
    global time
    time -= 1
    la.config(text=time)
    if time == 0:
        la.config(text="Время вышло")
    else:
        win.after(1000, update_timer)
pereriv = Label(text="Перерыв", font=(24))
pereriv.pack()
la = Label(win, font=(24))
la.pack()

update_timer()


win.mainloop()
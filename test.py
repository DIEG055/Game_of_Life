import numpy as np
import os
from time import  time
from Depredador_Presa import *
os.chdir('D:/user/Desktop/Game_of_Life')
filename= "data.txt"


w=world(50,50,filename)




window=Tk()
window.title("Game of life")
window.geometry("1000x1000")
c=Canvas(window,width=1000,height=1000)
c.place(x=0,y=0)

def pintar():
    c.create_rectangle(0,0,1000,1000,fill="white")
    for i in range(len(w.preys)):
        y=w.preys[i].posX*10
        x=w.preys[i].posY*10
        if not w.preys[i].mut:
            c.create_rectangle(x,y,x+10,y+10,fill="green")
        else:
            c.create_rectangle(x, y, x + 10, y + 10, fill="black")
    for i in range(len(w.depredators)):
        y=w.depredators[i].posX*10
        x=w.depredators[i].posY*10
        c.create_rectangle(x, y, x + 10, y + 10, fill="red")


    w.checkPreysConditions()
    w.checkDepredatorConditions()



    window.after(50,pintar)


pintar()


window.mainloop()

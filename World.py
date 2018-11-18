from tkinter import *

def start():
    print("The game has started")
def end():
    print("The game has ended ")
window=Tk()
#window.geometry(400*200) -> tamano ventana
window.title("Game of Life")
window.geometry("1500x900")
#command= funcion hecha por mi
'''
.pack -> ajusta a ventana
.grid -> ajusta por columna
.place -> ajusta por coordenada
'''
tam=StringVar()
texto=Label(window,text="Ingrese el tamano del mundo:").place(x=10,y=10)
tamanoMundo=Entry(window,textvariable=tam).place(x=10,y=40)
startButton=Button(window,text="Start",command=start).place(x=10,y=70)
endButton=Button(window,text="End",command=end()).place(x=60,y=70)
#.pack para que se ajuste a la ventanaS
#startButton.pack()
#endButton.pack()



#Canvas
c=Canvas(window,width=1000,height=800)
c.place(x=450,y=50)
c.create_rectangle(0,0,1000,800, fill="#5ea3a3")
for i in range(0,1000,20):
    for j in range(0,1000,10):
        c.create_rectangle(i,j,i+10,j+10, fill="white")
window.mainloop()
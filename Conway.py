from tkinter import *

########################################################
class Cell():
    def __init__(self):
        self.alive=False
    def type(self,t):
        self.type=t
########################################################
class World():
    def __init__(self,tamX,tamY):
        self.tamX=tamX
        self.tamY=tamY
        #Array 3D
        self.cells=[]
        #Array 2D
        self.aliveCells=[]

    def createCells(self,c):
        for i in range(self.tamX):
            row = []
            for j in range(self.tamY):
                row.append(False)
            c.append(row)

    def checkAliveCell(self,posX,posY):
        return self.cells[posX][posY]

    def reviveCell(self,posX,posY):
        self.cells[posX][posY]=True

    def killCell(self,posX,posY):
        self.cells[posX][posY]=False

    def checkNeighbour(self,cellX,cellY):
        neighbour = 0
        if self.checkAliveCell(cellX, cellY):
             neighbour-=1
        cellX-=1
        cellY-=1
        for i in range(3):
            for j in range(3):
                if self.checkAliveCell(cellX+i,cellY+j):
                     neighbour+=1
        return neighbour

    def mostrar(self):
        c.create_rectangle(0,0,600,600,fill="white")
        for i in self.aliveCells:
            i[0] *= 10
            i[1] *= 10
            c.create_rectangle(i[0], i[1], i[0] + 10, i[1] + 10, fill="#071e3d")


    def checkNeighbours(self):
        temp=[]
        self.createCells(temp)
        self.aliveCells=[]
        for i in range(1,self.tamX-2):
            for j in range(1,self.tamY-2):
                neighbours=self.checkNeighbour(i,j)
                if neighbours==3 and  not self.cells[i][j]:
                    temp[i][j]= True
                    self.aliveCells.append([i,j])
                elif neighbours>=2 and neighbours<=3 and self.cells[i][j]:
                    temp[i][j] = True
                    self.aliveCells.append([i,j])
                elif (neighbours>3 or neighbours<2) and self.cells[i][j]:
                    temp[i][j]=False
                else:
                    pass
        self.cells=temp
        del temp

######################################################


def createCellWithClick(event):
    i=int(event.x/10)
    j=int(event.y/10)
    w.reviveCell(i, j)
    i *= 10
    j *= 10
    c.create_rectangle(i, j, i + 10, j + 10, fill="#071e3d")

def deleteCellWithClick(event):
    i=int(event.x/10)
    j=int(event.y/10)
    w.killCell(i,j)
    i *= 10
    j *= 10
    c.create_rectangle(i, j, i + 10, j + 10, fill="white")

def start():
    w.mostrar()
    w.checkNeighbours()

    window.after(75, start)

def end():
    window.destroy()

def create_grid(event=None):
    w = c.winfo_width()-20 # Get current width of canvas
    h = c.winfo_height()-20 # Get current height of canvas
    c.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(20, w, 10):
        c.create_line([(i, 20), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(20, h, 10):
        c.create_line([(20, i), (w, i)], tag='grid_line')
######################################################
w=World(60,60)
w.createCells(w.cells)
window=Tk()
window.title("Game of life")
window.geometry("800x600")
c=Canvas(window,width=600,height=600)
c.place(x=200,y=0)
c.bind("<Button-1>", createCellWithClick)
c.bind("<Button-3>", deleteCellWithClick)
c.bind('<Configure>', create_grid)
startButton=Button(window,text="Start",command= start).place(x=10,y=10)
end=Button(window,text="End",command= end).place(x=10,y=60)
window.mainloop()



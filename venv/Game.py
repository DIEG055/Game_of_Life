from tkinter import *

########################################################
class Cell():
    def __init__(self):
        self.Alive=False

########################################################
class World():
    def __init__(self,tamX,tamY):
        self.tamX=tamX
        self.tamY=tamY
        self.cells=[]
        self.aliveCells=[]

    def createCells(self):
        for i in range(self.tamX):
            row = []
            for j in range(self.tamY):
                cell=Cell()
                row.append(cell)
            self.cells.append(row)

    def createCells2(self):
        c=[]
        for i in range(self.tamX):
            row = []
            for j in range(self.tamY):
                cell=Cell()
                row.append(cell)
            c.append(row)
        return c

    def checkAliveCell(self,posX,posY):
        return self.cells[posX][posY].Alive

    def reviveCell(self,posX,posY):
        self.cells[posX][posY].Alive=True


    def checkNeighbour(self,cellX,cellY):
        cellX-=1
        cellY-=1
        neighbour = 0
        for i in range(3):
            for j in range(3):
                if self.checkAliveCell(cellX+i,cellY+j):
                     neighbour+=1
        if self.checkAliveCell(cellX+1, cellY+1):
             neighbour-=1
        return neighbour

    def mostrar(self):
        c.create_rectangle(0,0,1000,1000,fill="white")
        for i in self.aliveCells:
            i[0] *= 10
            i[1] *= 10
            c.create_rectangle(i[0], i[1], i[0] + 10, i[1] + 10, fill="#071e3d")


    def checkNeighbours(self):
        temp=self.createCells2()
        self.aliveCells=[]
        for i in range(1,self.tamX-3):
            for j in range(1,self.tamY-3):
                neighbours=self.checkNeighbour(i,j)
                if neighbours==3 and  not self.cells[i][j].Alive:
                    temp[i][j].Alive = True

                    self.aliveCells.append([i,j])
                elif neighbours>=2 and neighbours<=3 and self.cells[i][j].Alive:
                    temp[i][j].Alive = True
                    self.aliveCells.append([i,j])
                elif (neighbours>3 or neighbours<2) and self.cells[i][j].Alive:
                    temp[i][j].Alive=False
                else:
                    pass
        self.cells=temp
       # self.mostrar()


#######################################################
w=World(100,100)
w.createCells()
window=Tk()
window.title("Game of life")
window.geometry("1000x1000")
c=Canvas(window,width=1000,height=1000)
c.place(x=0,y=0)
def start():
    time()
def callback(event):
    i=int(event.x/10)
    j=int(event.y/10)
    w.reviveCell(i, j)
    i *= 10
    j *= 10
    c.create_rectangle(i, j, i + 10, j + 10, fill="#071e3d")
startButton=Button(window,text="Start",command=start).place(x=900,y=70)


c.bind("<Button-1>", callback)
def time():
    w.mostrar()
    w.checkNeighbours()


    window.after(100,time)
window.mainloop()

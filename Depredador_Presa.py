import numpy as np
from tkinter import *
from random import randint
import os

os.chdir('D:/user/Desktop/Game_of_Life')
'''######################################################'''
# 0: nothing
# 1: prey
# 2: depredator
# 3: megaprey

class Cell:
    def __init__(self,posX,posY,tamx,tamy,lives):
        self.posX=posX
        self.posY=posY
        self.lives=lives
        self.tamx=tamx
        self.tamy=tamy
    def actualPosition(self):
        return self.posX,self.posY

    def alive(self):
        return self.lives>0

    def move(self,posX,posY):
        pass
    def dead(self):
        pass

'''###################################################'''

class Depredator(Cell):
    def __init__(self,posX,posY,tamx,tamy):
        super().__init__(posX,posY,tamx,tamy,15)
        self.pair=False

# revisa si tiene presas tipo 1 o tipo 3 cerca
    def isTherePrey(self,map):
        for i in range (-1,2):
            for j in range(-1,2):
                if map[(self.posX+i)%self.tamx][(self.posY+j)%self.tamy]==1 or map[(self.posX+i)%self.tamx][(self.posY+j)%self.tamy]==3:
                    return True
        return  False

# buscar presas cercanas, en caso de haber regresa una presa aleotoria
# -1,-1  -> no hay presas cercanas
    def searchPrey(self,map):
        positions=[]
        for i in range (-1,2):
            for j in range(-1,2):
                if map[(self.posX+i)%self.tamx][(self.posY+j)%self.tamy]==1 or map[(self.posX+i)%self.tamx][(self.posY+j)%self.tamy]==3:
                    positions.append([(self.posX+i)%self.tamx,(self.posY+j)%self.tamy])
        if len(positions)==0:
            return -1,-1
        else:
            posPrey=positions[randint(0,len(positions)-1)]
            return posPrey[0],posPrey[1]

# busca depredadores cercanos, en caso de haber regresa un depredador aleatoreamente
# -1,-1  -> no hay depredadores cercanos
    def searchDepredator(self,map):
        positions=[]
        for i in range (-1,2):
            for j in range(-1,2):
                if map[(self.posX+i)%self.tamx][(self.posY+j)%self.tamy]==2:
                    positions.append([(self.posX+i)%self.tamx,(self.posY+j)%self.tamy])
        if len(positions)==1:
            return -1,-1
        else:
            posPrey=positions[randint(0,len(positions)-1)]
            return posPrey[0],posPrey[1]

# pelea de dos depredadores,  determinando ganador a aquel que tenga mas vidad
    def winFight(self,depredator2):
        if self.lives> depredator2.lives:
            return True
        else:
            return False

# mueve a la siguiente posicion y resta una vida
    def move(self,posX,posY):
        if self.lives>=1:
            self.posX=posX
            self.posY=posY
            self.lives -= 1
# realiza moviento aleatorio, en caso de poderse
    def randomMove(self,map):
        i=randint(-1,1)
        j=randint(-1,1)
        if map[(self.posX+i)%self.tamx][(self.posY+j)%self.tamy]==0:
            map[self.posX][self.posY] = 0
            self.posX =(self.posX+i)%self.tamx
            self.posY =(self.posY+j)%self.tamy
            map[self.posX ][self.posY ] = 2
        self.lives -= 1


# se mueve hacia la presa y se alimenta
    def eat(self,posX,posY):
        self.move(posX,posY)
        self.lives+=10

# muere y se convierte en presa
    def dead(self,map):
        self.lives=0
        map[self.posX,self.posY]=1

# revisa si puede tener descendencia
    def checkPair(self):
        if self.lives<=7:
            self.pair=True

''' ###################################################'''

class Prey(Cell):
    def __init__(self,posX,posY,tamx,tamy):
        super().__init__(posX,posY,tamx,tamy,20)
        self.mut=False


# si esta redeada de otras presas, muta a superpresa
    def mutate(self,map):
        count=0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if map[(self.posX + i)%self.tamx][(self.posY + j)%self.tamy] == 1:
                    count+=1
        if count == 9:
            self.mut = True

# realiza un movimiento aleatorio en caso de poderse,restamos 1 vida
    def move(self,map):
        i=randint(-1,1)
        j=randint(-1,1)
        if map[(self.posX+i)%self.tamx][(self.posY+j)%self.tamy]==0:
            map[self.posX][self.posY] = 0
            self.posX =(self.posX+i)% self.tamx
            self.posY =(self.posY+j)% self.tamy
            if self.mut:
                map[self.posX][self.posY] = 3
            else:
                map[self.posX ][self.posY ] = 1
            self.lives-=1

# la presa muere y se actualiza el mapa
    def dead(self,map):
        self.lives=0
        map[self.posX,self.posY]=0
'''####################################################'''
class world():
    def __init__(self,tamX,tamY,filename):
        self.tamX=tamX
        self.tamY=tamY
        self.depredators=[]
        self.preys=[]
        self.map = np.genfromtxt(filename, dtype=int)
        for i in range(self.tamX):
            for j in range(self.tamY):
                if self.map[i][j] == 1 or self.map[i][j] == 3:
                    prey = Prey(i, j,self.tamX,self.tamY)
                    if self.map[i][j]==3:
                        prey.mut=True
                    self.preys.append(prey)
                elif self.map[i][j] == 2:
                    depredator = Depredator(i, j,self.tamX,self.tamY)
                    self.depredators.append(depredator)

# retorna la posicion en la lista de depredadores y el propio depredador
    def searchDep(self,posX,posY):
        for i in range(len(self.depredators)):
            if self.depredators[i].posX==posX and self.depredators[i].posY==posY:
                return i,self.depredators[i]
# retorna la posicion en la lista de presas, y la propia presa
    def searchPre(self, posX,posY):
        for i in range(len(self.preys)):
            if self.preys[i].posX==posX and self.preys[i].posY==posY:
                return i,self.preys[i]

# interaccion de las presas
    def checkPreysConditions(self):
        l=len(self.preys)
        i=0
        while i<l:
            if self.preys[i].alive():
                # revisamos si puede mutar
                if not self.preys[i].mut:
                    self.preys[i].mutate(self.map)
                if self.preys[i].mut:
                        self.map[self.preys[i].posX][self.preys[i].posY]=3
                self.preys[i].move(self.map)
            else:
                # buscamos la presa para eliminarla de la lista de presas
                p=self.searchPre(self.preys[i].posX,self.preys[i].posY)
                # actualizamos el mapa
                self.map[self.preys[i].posX][self.preys[i].posY]=0
                # eliminamos la presa de la lista e presas
                self.preys.pop(p[0])
                l-=1
            i+=1
    def checkDepredatorConditions(self):
        l=len(self.depredators)
        i=0
        while i<l:
            print(l,len(self.depredators))
            if self.depredators[i].alive():
                # se revisa si puede tener descendencia
                self.depredators[i].checkPair()

                # se obtiene un depredador cercano en caso de haber
                # -1,-1  -> no hay depredador cercano

                dep = self.depredators[i].searchDepredator(self.map)
                if dep[0] != -1 and dep[1] != -1:
                    depredator2 = self.searchDep(dep[0], dep[1])

                    # depredador[i] pelea:
                    if self.depredators[i].winFight(depredator2[1]):
                        # se crea la nueva presa
                        newPrey = Prey(depredator2[1].posX, depredator2[1].posY,self.tamX,self.tamY)
                        # agregamos la nueva presa a la lista de presas
                        self.preys.append(newPrey)
                        # se actualiza el mapa
                        self.map[depredator2[1].posX][depredator2[1].posY] = 1
                        # se elimina al depredador que murio de la lista de depredadores
                        self.depredators.pop(depredator2[0])
                        l-=1
                    else:
                        newPrey = Prey(self.depredators[i].posX, self.depredators[i].posY,self.tamX,self.tamY)
                        # agregamos la nueva presa a la lista de presas
                        self.preys.append(newPrey)
                        # se actualiza el mapa
                        self.map[self.depredators[i].posX][self.depredators[i].posY] = 1
                        # se elimina al depredador que murio de la lista de depredadores
                        self.depredators.pop(i)
                        l -= 1
                elif self.depredators[i].isTherePrey(self.map):
                    # posicion de la presa
                    p = self.depredators[i].searchPrey(self.map)
                    # se mueve hacia la presa, se actualiza el mapa
                    # se actualiza posicion actual
                    self.map[self.depredators[i].posX][self.depredators[i].posY] = 0
                    # se actualiza a la nueva posicion(donde esta la presa)

                    if self.map[p[0]][p[1]] == 3:
                        self.map[p[0]][p[1]] = 0
                        self.depredators.pop(i)
                        l-=1
                    else:
                        self.map[p[0]][p[1]] = 2
                    # se busca a la presa de la lista de presas para eliminarla
                        dp = self.searchPre(p[0], p[1])
                    # se elimina de la presa
                        self.preys.pop(dp[0])
                        self.depredators[i].eat(p[0], p[1])
                else:
                    self.depredators[i].randomMove(self.map)
                i+=1
            else:
                # se busca al depredador en la lista de depredadores
                d = self.searchDep(self.depredators[i].posX, self.depredators[i].posY)
                # se crea una presa
                newPrey = Prey(d[1].posX, d[1].posY,self.tamX,self.tamY)
                # se agrega la nueva presa a la lista de presas
                self.preys.append(newPrey)
                # se actualiza el mapa al convertirlo en presa
                self.map[d[1].posX][d[1].posY] = 1
                # se elimina al depredador que acaba de morir de la lista de depredadores
                self.depredators.pop(d[0])
                l-=1
                i+=1

    def checkConditions(self):
        self.checkPreysConditions()
        self.checkDepredatorConditions()



















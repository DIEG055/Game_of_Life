import numpy as np
from tkinter import *
from random import randint
import os

os.chdir('D:/user/Desktop/Game_of_Life')
######################################################
#0: nothing
#1: prey
#2: depredator
#3: megaprey

class Cell():
    def __init__(self,posX,posY,lives):
        self.posX=posX
        self.posY=posY
        self.lives=lives

    def actualPosition(self,posX,posY):
        return self.posX,self.posY

    def alive(self):
        return self.lives>0

    def move(self,posX,posY):
        pass
    def dead(self):
        pass
###################################################
class Depredator(Cell):
    def __init__(self,posX,posY):
        super().__init__(posX,posY,15)
        self.pair=False

    def isTherePrey(self,map):
        for i in range (-1,1):
            for j in range(-1,1):
                if map[self.posX+i][self.posY+j]==1 or map[self.posX+i][self.posY+j]==3:
                    return True
        return  False

    def searchPrey(self,map):
        positions=[]
        for i in range (-1,1):
            for j in range(-1,1):
                if map[self.posX+i][self.posY+j]==1 or map[self.posX+i][self.posY+j]==3:
                    positions.append([self.posX+i,self.posY+j])
        if len(positions)==0:
            return -1,-1
        else:
            posPrey=positions[randint(0,len(positions)-1)]
            return posPrey[0],posPrey[1]

    def searchDepredator(self,map):
        positions=[]
        for i in range (-1,1):
            for j in range(-1,1):
                if map[self.posX+i][self.posY+j]==2:
                    positions.append([self.posX+i,self.posY+j])
        if len(positions)==0:
            return -1,-1
        else:
            posPrey=positions[randint(0,len(positions)-1)]
            return posPrey[0],posPrey[1]

    def winFight(self,depredator2):
        if self.lives> depredator2.lives:
            return True
        else:
            return False

    def move(self,posX,posY):
        if self.lives>=1:
            self.posX=posX
            self.posY=posY
            self.lives -= 1

    def randomMove(self,map):
        i=randint(-1,1)
        j=randint(-1,1)
        if map[self.posX+i][self.posY+j]==0:
            self.posX =self.posX+i
            self.posY =self.posX+j

    def eat(self,posX,posY):
        self.move(posX,posY)
        self.lives+=10

    def dead(self,map):
        self.lives=0
        map[self.posX,self.posY]=1

    def checkPair(self):
        if self.lives<=7:
            self.pair=True
#####################################################
class Prey(Cell):
    def __init__(self,posX,posY):
        super().__init__(posX,posY,20)
        self.mut=False

    def mutate(self,map):
        count=0
        for i in range(-1, 1):
            for j in range(-1, 1):
                if map[self.posX + i][self.posY + j] == 1:
                    count+=1
        if count == 9:
            self.mut = True

    def move(self,map):
        i=randint(-1,1)
        j=randint(-1,1)
        if map[self.posX+i][self.posY+j]==0:
            self.posX =self.posX+i
            self.posY =self.posX+j
            map[self.posX ][self.posY ] = 1
            self.lives-=1
    def dead(self,map):
        self.lives=0
        map[self.posX,self.posY]=0
####################################################
class world():
    def __init__(self,tamX,tamY):
        self.tamX=tamX
        self.tamY=tamY
        self.depredators=[]
        self.preys=[]

    def readFile(self,filename):
        self.map= np.genfromtxt(filename,dtype=int)
        for i in range(self.tamX):
            for j in range(self.tamY):
                if self.map[i][j]==1:
                    prey=Prey(i,j)
                    self.preys.append(prey)
                elif self.map[i][j]==2:
                    depredator = Depredator(i,j)
                    self.depredators.append(depredator)

    def searchDep(self,posX,posY):
        for i in range(len(self.depredators)):
            if self.depredators[i].posX==posX and self.depredators[i].posY==posY:
                return i,self.depredators[i]

    def searchPre(self,posX,posY):
        for i in range(len(self.preys)):
            if self.preys[i].posX==posX and self.preys[i].posY==posY:
                return i,self.preys[i]

    def checkConditions(self):
        for i in range(len(self.depredators)):
            if self.depredators[i].alive():
                self.depredators[i].checkPair()
                depX,depY=self.depredators[i].searchDepredators(self.map)
                if depX != -1 and depY!=-1:
                    posdep2,depredator2=self.searchDep(depX,depY)
                    if self.depredators.winFight(depredator2):
                        newPrey = Prey(depredator2.posX, depredator2.posY)
                        self.preys.append(newPrey)
                        self.map[depredator2.posX][depredator2.posY]=1
                        self.depredators.pop(posdep2)
                elif self.depredators[i].isTherePrey(self.map):
                    pX,pY=self.depredators[i].searchPrey(self.map)
                    self.map[self.depredators[i].posX][self.depredators[i].posY]=0
                    self.map[pX][pY] = 2
                    pos,p=self.searchPre(pX,pY)
                    self.preys.pop(pos)
                    self.depredators[i].eat(pX,pY)
                else:
                    self.depredators[i].randomMove(self.map)
            else:
                posdep2, depredator2 = self.searchDep(depX, depY)
                newPrey = Prey(depredator2.posX, depredator2.posY)
                self.preys.append(newPrey)
                self.map[depredator2.posX][depredator2.posY] = 1
                self.depredators.pop(posdep2)
        for i in range(len(self.preys)):
            if self.preys[i].alive():
                self.preys[i].mutate(self.map)
                self.preys[i].move(self.map)
            else:
                j,p=self.searchPre(self.preys[i].posX,self.preys[i].posY)
                self.map[self.preys[i].posX][self.preys[i].posY]=0
                self.preys.pop(j)


















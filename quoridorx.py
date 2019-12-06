import turtle
from turtle import *

class QuoridorX(quoridor):
    def afficher(self, état_parties):

        #Base 
        turtle.setx(-150)
        turtle.sety(-200)
        turtle.setup(width=500, height=600)
        color('Black', 'white')
        begin_fill()
        pensize(5)
        turtle.speed(speed = 0)

        #Faire le contour
        for i in range(2):
            forward(300)
            left(90)
            forward(400)
            left(90)


        pensize(1)
        #Mettre les colonnes
        for i in range(5):
            penup()
            forward(30)
            left(90)
            pendown()
            forward(400)
            left(-90)
            penup()
            forward(30)
            left(-90)
            pendown()
            forward(400)
            left(90)

        #Mettre les lignes
        for i in range(5):
            left(90)
            penup()
            forward(40)
            left(90)
            pendown()
            forward(300)
            right(90)
            forward(40)
            right(90)
            forward(300)

        #Insérer les chiffres 
        penup()
        left(180)
        forward(290)
        left(90)
        forward(20)
        for i in range(10):
            turtle.print(i)
            forward(40)

        #Actualiser avec l'état de la partie
        #Insérer joueur




            


        end_fill()
        done()



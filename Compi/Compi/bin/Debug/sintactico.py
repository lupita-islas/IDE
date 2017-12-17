import sys
import os
from Tabla import HashMap

#debe recibir una copia del arbol

from anytree  import Node, PreOrderIter, PostOrderIter

PRE_ALOW=["ASSIGN","CIN","ID"]
POST_ALOW=["IF","ASSIGN","REPEAT"]
miTabla = HashMap()

MEMORIA=0
nombreError=""
#miTabla.insert('x','int',MEMORIA,MEMORIA,2)
#miTabla.imprimirTabla()

#Construir la tabla hash con preorden, se insertan declaraciones, asignaciones, lectura (cin)
#Primero manda llamar a construir la tabla de simbolos en forma de preorden que usa la funcion de insertar
def insertar(nodoPrincipal,nombre):
    global nombreError
    global MEMORIA
    global miTabla

    miTabla.abrir(nombre)
    nombreError=nombre

    for nodo in PreOrderIter(nodoPrincipal):
        if (PRE_ALOW.__contains__(nodo.tipo)):
            miTabla.insert(nodo.nombre,nodo.type,MEMORIA,nodo.linea,nodo.valor,nodo.parent.tipo)
            MEMORIA+=1

    miTabla.errorDec(nombreError)

def imprimirTabla(nombreArchivo):
    miTabla.imprimirTabla(nombreArchivo)

def instValue(node):
    global MEMORIA, miTabla
    miTabla.instValTable(node.nombre,node.value,MEMORIA,node.linea)
    MEMORIA+=1

def regresar(nombre):
    return miTabla.retrieve(nombre)

def regTipo(nombre):
    return miTabla.retrieveT(nombre)

def abir(nombre):
    miTabla.abrir(nombre)

def memoria(nombre):
    return miTabla.retrieveM(nombre)

def allTable():
    return miTabla


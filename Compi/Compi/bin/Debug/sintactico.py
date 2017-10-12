import sys
import os
from Tabla import HashMap

#debe recibir una copia del arbol

from anytree  import Node, PreOrderIter, PostOrderIter

PRE_ALOW=["ASSIGN","CIN","ID"]
POST_ALOW=["IF","ASSIGN","REPEAT"]
miTabla = HashMap()

MEMORIA=0

#miTabla.insert('x','int',MEMORIA,MEMORIA,2)
#miTabla.imprimirTabla()

#Construir la tabla hash con preorden, se insertan declaraciones, asignaciones, lectura (cin)
#Primero manda llamar a construir la tabla de simbolos en forma de preorden que usa la funcion de insertar
def insertar(nodoPrincipal):
    global MEMORIA
    global miTabla
    for nodo in PreOrderIter(nodoPrincipal):
        if (PRE_ALOW.__contains__(nodo.tipo)):
            miTabla.insert(nodo.nombre,nodo.type,MEMORIA,nodo.linea,nodo.valor)
            MEMORIA+=1
    miTabla.imprimirTabla()
    miTabla.errorDec()

#Pregunta: si el valor cambia en cierto momento en una asignacion y no corresponde
#a su declaracion es un error, pero si se sigue cambiando mas adelante, como detecta
#en que linea estaba el error, una lista de atributos tal vez?

def checar(nodoPrincipal):
    for nodo in PostOrderIter(nodoPrincipal):
        if nodo.tipo=="OP":
            if nodo.type=="boolean":
                error(nodo.linea,"Operacion a un tipo boolean")

#Crear un archivo de texto para los errores <-----CESAR
def error(linea,texto):
    archivoError.write(texto+" "+linea+"\n")

def instValue(node):
    global MEMORIA, miTabla
    miTabla.instValTable(node.nombre,node.value,MEMORIA,node.linea)
    MEMORIA+=1

#Checar tipos
#hacer una lista de signos +, -, * y /
#checar que el nombre este en una de estas listas
#si es asi verificar que los hijos sean enteros o reales de lo contrario es un error
#
#
#
#
#CUANDO NO ESTA DECLARADO, NO COINCIDAN LOS TIPOS (DECLARARLO DE UNO Y DE OTRO,

#hacer el casteo, si es flotante y


def regresar(nombre):
    return miTabla.retrieve(nombre)
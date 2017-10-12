import sys
import os

#debe recibir una copia del árbol

from anytree  import Node

MEMORIA=0

#tabla hash debe contener
#nombre, tipo, localidad memoria, num linea (lista), valor
#controlar colisiones ???
estructura_hash = {
    "name":"",
    "type":"",
    "loc_mem":"",
    "num_lin":[],
    "value":"",
    "siguiente":
}

#Construir la tabla hash con preorden, se insertan declaraciones, asignaciones, lectura (cin)
def insertar(nodoPrincipal):
    global MEMORIA
    for nodo in PreOrderIter(nodoPrincipal):
        if (nodo.tipo == "ASSIGN" or nodo.tipo == "CIN" or nodo.tipo == "ID"):
            if (buscar_hash(nodo.name)== -1): #si no esta en la tabla hash devuelve -1
                insertar_hash(nodo.name, nodo.linea, MEMORIA)
                MEMORIA=MEMORIA+1
            else:
                insertar_hash(nodo.name, nodo.linea, 0)

def insertar_hash():


def buscar_hash():
    hash()


#Tener una función que haga el recorrido p
#Recorrido preorden: (raiz izquierda derecha) #PreOrderIter
#si el nodo es diferente de vacio
#manda llamar a la funcion de checar o insertar
#entra y recorre todos los hijos que tiene node.children (numero de hijos o algo asi)
#manda llamar de nuevo a la funcion de recorrido enviandole a su hijo

#Recorrido post orden (izquierda derecha raiz) #PostOrderIter
#entra y recorre todos los hijos que tiene node.children (numero de hijos o algo asi)
#cuando ya llega al ultimo hijo manda llamar a la funcion de checar o insertar
#manda de nuevo a recorrer el arbol con el hermano

#Primero manda llamar a construir la tabla de simbolos en forma de preorden que usa la funcion de insertar

#Funcion de insertar #agregar al nodo un atributo tipo

# buscar si se encuentra en la tabla
#si no se encuentra se inserta
# si se encuentra se agrega la linea donde se encontro

#agregar al nodo un atributo numero de linea (lineas[2]
#debemos modificar la gramatica para agregar al nodo un atributo name para usarlo
# al construir la tabla hash
#primero verificar que el atributo no se encuentra en la tabla hash (con su nombre)
# si ya se encuentra se agrega el numero de linea donde esta a la lista de lineas
# y borrar el valor anterior para poner un nuevo valor ??
# si no esta se agrega el nombre, la localidad de memoria es un numero entero global
# que se aumenta cada vez que se manda llamar a la funcion de entero, se agrega al
# numero de linea el atributo de linea y se agrega el valor

#Pregunta: si el valor cambia en cierto momento en una asignacion y no corresponde
#a su declaracion es un error, pero si se sigue cambiando mas adelante, como detecta
#en que linea estaba el error, una lista de atributos tal vez?



#Checar tipos
#hacer una lista de signos +, -, * y /
#checar que el nombre este en una de estas listas
#si es asi verificar que los hijos sean enteros o reales de lo contrario es un error
#
#
#
#
#

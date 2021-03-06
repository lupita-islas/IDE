import sys
import os
from anytree  import Node, RenderTree, AsciiStyle, AbstractStyle
from anytree.dotexport import RenderTreeGraph

class MyNode(Node):
        separator = "|"
nombre=sys.argv[1]
#nombre = "C:/Users/cesar/Documents/GitHub/IDE/IDE/Compi/Compi/bin/Debug/pruebFire.vol"
#nombre="while.vol"
archivo = open(nombre, 'r')
nombreError=nombre.replace("vol","errS")
nombreArbol=nombre.replace("vol","tree")
if os.path.exists(nombreError):
    os.remove(nombreError)
    archivoError = open(nombreError, "w+")
else:
    archivoError= open(nombreError,"w+")
if os.path.exists(nombreArbol):
    os.remove(nombreArbol)
    archivoArbol = open(nombreArbol, "w+")
else:
    archivoArbol= open(nombreArbol,"w+")
token = ""
ERROR = "False"

#NODOS
#mainNode=Node("Main",parent=None)
#
# global lineas
# global token
# global ERROR

# conjuntos siguiente
S_PROGRAMA = ["$"]
S_LIST_DEC = ["if", "while", "repeat", "cin", "cout", "{", "IDENTIFICADOR", "}","break"]
S_DECLARACION = [";"]
S_TIPO = ["IDENTIFICADOR"]
S_LISTA_VARIABLES = [";"]
S_LISTA_SENTENCIAS = ["}"]
S_SENTENCIA = ["if", "while", "repeat", "cin", "cout", "{", "IDENTIFICADOR", "}","break"]
S_SELECCION = S_SENTENCIA
S_ITERACION = S_SENTENCIA
S_REPETICION = S_SENTENCIA
S_SENT_CIN = S_SENTENCIA
S_COUT = S_SENTENCIA
S_BLOQUE = ["if", "while", "repeat", "cin", "cout", "{", "IDENTIFICADOR", "}", "until", "else","break"]
S_ASIGNACION = S_SENTENCIA
S_EXPRESION = [")", ";"]
S_RELACION = ["(", "REAL", "ENTERO", "IDENTIFICADOR"]
S_EXPRESION_SIMPLE = ["<=", ">", "<", ">=", "==", "!=", ")", ";", "+", "-"]
S_SUMA_OPL = ["(", "REAL", "ENTERO", "IDENTIFICADOR"]
S_TERMINO = ["<=", ">", "<", ">=", "==", "!=", ")", ";", "+", "-", "*", "/"]
S_MULT_OP = ["(", "REAL", "ENTERO", "IDENTIFICADOR"]
S_FACTOR = ["<=", ">", "<", ">=", "==", "!=", ")", ";", "+", "-", "*", "/"]
#S_IDENTIFICADOR = [",", ":", ":=", S_FACTOR]
#S_NUMERO = S_FACTOR
#S_CP = ["THEN", "{", ";", S_FACTOR]
#S_CIN = [S_IDENTIFICADOR]
#S_COUT = ["(", "REAL", "ENTERO", "IDENTIFICADOR"]

# CONJUNTOS PRIMERO
P_PROGRAMA = ["main"]
P_LISTA_DECLARACION = ["int", "real", "boolean"]  # vacio
P_DECLARACION = ["int", "real", "boolean"]
P_TIPO = ["int", "real", "boolean"]
P_LSTA_VAR = ["IDENTIFICADOR"]
P_LSTA_SENT = ["if", "while", "repeat", "cin", "cout", "{", "IDENTIFICADOR","break"]  # vacio
P_SENT = ["if", "while", "repeat", "cin", "cout", "{", "IDENTIFICADOR", "break"]
P_SEL = ["if"]
P_ITERACION = ["while"]
P_REPET = ["repeat"]
P_SENT_CIN = ["cin"]
P_SENT_COUT = ["cout"]
P_BLOQUE = ["{"]
P_ASIGN = ["IDENTIFICADOR"]
P_EXP = ["(", "REAL", "ENTERO", "IDENTIFICADOR"]
P_REL = ["<=", "<", ">", ">=", "==", "!="]

P_EXP_SIM = ["(", "REAL", "ENTERO", "IDENTIFICADOR"]
P_SUM = ["+", "-"]
P_TERM = ["(", "REAL", "ENTERO", "IDENTIFICADOR"]
P_MUL = ["*", "/"]
P_FACT = ["(", "REAL", "ENTERO", "IDENTIFICADOR"]


def verificar(primero, siguiente):
    global token
    if not token in primero:
        error()
        scanto(primero + siguiente)


def scanto(synchset):
    global token
    synchset.append("$")
    while not token in synchset:
        token = leer()


def error():
    global ERROR,lineas, fila_anterior, col_anterior

    if(lineas[2]!=fila_anterior and lineas[3]!=col_anterior):
        #print ("Error")
        archivoError.write("Token inesperado en linea ->")
        archivoError.write(lineas[2]+"\n")
        fila_anterior=lineas[2]
        col_anterior=lineas[3]
    # error en linea->lineas[2] y columna-> lineas[3]
    # error=lineas[0]
    # ERROR="True"
    # mandar a archivo que Cesar sabe ;) :*


def comparar(token_esperado):
    global token
    if (token == token_esperado):
         token = leer()
    else:
        error()


def leer():
    global archivo,lineas
    linea = archivo.readline()
    if(linea!= ""):
        lineas = linea.split("\t")

        #if ((lineas[1] == 'IDENTIFICADOR\n') or (lineas[1] == 'REAL\n') or (lineas[1] == 'ENTERO\n') or (lineas[1] == 'OPERADOR\n')):
        if ((lineas[1] == 'IDENTIFICADOR') or (lineas[1] == 'REAL') or (lineas[1] == 'ENTERO')):
            #line = lineas[1].split("\t")
            return lineas[1]
        else:
            return lineas[0]  # lineas con 0=token 1=lexema
    else:
        return "$"

def principalMain(synchset):  # checar
    global token, fila_anterior, col_anterior,ls
    fila_anterior= -1
    col_anterior=-1
    token = leer()
    verificar (P_PROGRAMA, synchset)

    if token in P_PROGRAMA:

        nodo=MyNode(token)
        comparar("main")

        comparar("{")
        if(token in P_LISTA_DECLARACION):
            listaDeclaracion(S_LIST_DEC).parent=nodo

        if (token in P_LSTA_SENT):
            #ls=Node("ls",parent=nodo)
            listaSentencias(S_LISTA_SENTENCIAS).parent=nodo
        comparar("}")
    verificar(synchset,P_PROGRAMA)
    return nodo


def listaDeclaracion(synchset):
    global token,lista,nodoLista,lineas
    # while var==0: #Mientras la declaracion sea vacia
    nodo= MyNode(lineas[2]+" ListDec")
    #nodo.linea=lineas[2]
    #nodo.nombre="ListDec"
    #nodo.tipo="ListDec"
    #nodo= MyNode("ListDec")
    verificar(P_LISTA_DECLARACION, synchset)
    #if not token in synchset:
    if token in P_LISTA_DECLARACION:
        while (token in P_LISTA_DECLARACION):
            declaracion(S_DECLARACION).parent=nodo
            comparar(";")
    verificar(synchset, P_LISTA_DECLARACION)
    return nodo


def declaracion(synchset):
    global token, listDecNod,nodoLista
    nodo= MyNode(lineas[2]+" Dec")
    #nodo.linea=lineas[2]
    #nodo.nombre="Dec"
    #nodo.tipo="Dec"
    verificar(P_DECLARACION, synchset)
    #if not token in synchset:
    if token in P_DECLARACION:

       # Node(token,parent=listDecNod)
        tipo(S_TIPO).parent=nodo
        listaVariables(S_LISTA_VARIABLES).parent=nodo
    verificar(synchset, P_DECLARACION)
    return nodo


def tipo(synchset):  # checar
    global token,NodoAux

    verificar(P_TIPO, synchset)
    nodo=MyNode(lineas[2]+ " "+token)
    #nodo.linea=lineas[2]
    #nodo.nombre=token
    #nodo.tipo="Tipo"
    #nodo.type=token
    #if not token in synchset:
    if token in P_TIPO:
        if token == "int":
            comparar("int")
        elif token == "real":
            comparar("real")
        elif token == "boolean":
            comparar("boolean")
    verificar(synchset, P_TIPO)
    return nodo


def listaVariables(synchset):
    global token,lineas
    nodoAux= MyNode(lineas[2]+" ListVar")
    #nodoAux.linea=lineas[2]
    #nodoAux.nombre="ListVar"
    #nodoAux.tipo="ListVar"
    #nodoAux= MyNode("ListVar: "+lineas[2])
    verificar(P_LSTA_VAR, synchset)
    #if not token in synchset:
    if token in P_LSTA_VAR:
        while (token in P_LSTA_VAR):
            nodo=MyNode(lineas[0])
            nodo.parent=nodoAux
            comparar("IDENTIFICADOR")
            if (token != ","):
                break
            else:
                comparar(",")
    verificar(synchset, P_LSTA_VAR)
    return nodoAux

def listaSentencias(synchset):
    global token,ls,lineas
    nodo= MyNode("")
    nodo_aux= MyNode(lineas[2]+" ListSent")#Cambiar el nombre
    #nodo_aux.linea=lineas[2]
    #nodo_aux.nombre="LISTSENT"
    #nodo_aux.tipo="LISTSENT"
    verificar(P_LSTA_SENT, synchset)
    if token in P_LSTA_SENT:
        while (token in P_LSTA_SENT):
            nodo = sentencia(S_SENTENCIA)
            nodo.parent=nodo_aux
    verificar(synchset, P_LSTA_SENT)
    return nodo_aux


def sentencia(synchset):
    global token
    #nodo = Node(token)
    nodo= MyNode("")
    verificar(P_SENT, synchset)
    # if not token in synchset:
    if token in P_SENT:
        if (token == "if"):
           nodo=seleccionIF(S_SELECCION)
        elif (token == "while"):  # while
            nodo=iteracionWhile(S_ITERACION)
        elif (token == "repeat"):  # for
            nodo = repeticion(S_REPETICION)
        elif (token == "cin"):  # CIN
            nodo=sentCin(S_SENT_CIN)
        elif (token == "cout"):
            nodo=sentCout(S_COUT)
        elif (token == "IDENTIFICADOR"):  # identificador CHECAR
            nodo = asignacion(S_ASIGNACION)
        elif (token == "{"):   # bloque
            nodo = bloque(S_BLOQUE)
        elif(token=="break"):
            nodo=MyNode(lineas[2]+" "+token)
            comparar("break")
            comparar(";")
            return nodo
    verificar(synchset, P_SENT)
    return nodo

def seleccionIF(synchset):
    global token,lineas
    verificar(P_SEL, synchset)
    nodo= MyNode("")
    # if not token in synchset:
    if token in P_SEL:
        nodo = MyNode(lineas[2]+" "+token)
        #nodo.linea=lineas[2]
        #nodo.nombre=token
        #nodo.tipo="IF"
        comparar("if")
        comparar("(")
        expresion(S_EXPRESION).parent=nodo  # nodo hijo primero
        comparar(")")
        comparar("then")
        try:
            bloque(S_BLOQUE).parent=nodo  # hijo dos
        except ValueError:
            print("Nodo vacio")

        if (token == "else"):
            comparar("else")
            bloque(S_BLOQUE).parent=nodo  # nodo hijo tres
    verificar(synchset, P_SEL)
    return nodo

def iteracionWhile(synchset):
    global token,lineas
    verificar(P_ITERACION, synchset)
    nodo= MyNode("")
    # if not token in synchset:
    if token in P_ITERACION:
        nodo = MyNode(lineas[2]+" "+token)
        #nodo.linea=lineas[2]
        #nodo.nombre=token
        #nodo.tipo="WHILE"
        comparar("while")  # nodo padre
        comparar("(")
        expresion(S_EXPRESION).parent=nodo  # nodo hijo 1
        comparar(")")
        bloque(S_BLOQUE).parent=nodo  # nodo hijo 2
    verificar(synchset, P_ITERACION)
    return nodo

def repeticion(synchset):
    global token, lineas
    verificar(P_REPET, synchset)
    nodo= MyNode("")
    # if not token in synchset:
    if token in P_REPET:
        nodo = MyNode(lineas[2]+" "+token)
        #nodo.linea=lineas[2]
        #nodo.nombre=token
        #nodo.tipo="REPEAT"
        comparar("repeat")  # nodo padre
        bloque(S_BLOQUE).parent = nodo  # nodo hijo 1
        comparar("until")
        comparar("(")
        expresion(S_EXPRESION).parent=nodo  # nodo hijo 2
        comparar(")")
        comparar(";")
    verificar(synchset, P_REPET)
    return nodo

def sentCin(synchset):  # es solo el nodo padre
    global token,lineas
    verificar(P_SENT_CIN, synchset)
    nodo= MyNode("")
    # if not token in synchset:
    if token in P_SENT_CIN:
        comparar("cin")  # nodo padre
        nodo = MyNode(lineas[2]+" cin: "+lineas[0])
        #nodo.linea=lineas[2]
        #nodo.nombre=lineas[0]
        #nodo.tipo="CIN"
        comparar("IDENTIFICADOR")  # lo que lee es su atributo o nombre
        comparar(";")
    verificar(synchset, P_SENT_CIN)
    return nodo

def sentCout(synchset):
    global token,lineas
    verificar(P_SENT_COUT, synchset)
    nodo= MyNode("")
    # if not token in synchset:
    if token in P_SENT_COUT:
        nodo= MyNode(lineas[2]+" "+token)
        #nodo.linea=lineas[2]
        #nodo.nombre=token
        #nodo.tipo="COUT"
        comparar("cout")  # nodo padre
        expresion(S_EXPRESION).parent=nodo  # nodo hijo
        comparar(";")
    verificar(synchset,P_SENT_COUT)
    return nodo

def bloque(synchset):
    global token
    verificar(P_BLOQUE, synchset)
    nodo= MyNode("")
    # if not token in synchset:
    if token in P_BLOQUE:
        comparar("{")
        nodo= listaSentencias(S_LISTA_SENTENCIAS)
        comparar("}")
    verificar(synchset, P_BLOQUE)

    return nodo


def asignacion(synchset):
    global token, lineas
    verificar(P_ASIGN, synchset)
    nodo= MyNode("")
    # if not token in synchset:
    if token in P_ASIGN:
        nodo = MyNode(lineas[2]+" Assign "+lineas[0])
        #nodo.linea=lineas[2]
        #nodo.nombre=lineas[0]
        #nodo.tipo="ASSIGN"
        comparar("IDENTIFICADOR")
        comparar(":=")
        expresion(S_EXPRESION).parent=nodo
        comparar(";")
    verificar(synchset, P_ASIGN)
    return nodo


def expresion(synchset):
    global token,lineas
    verificar(P_EXP, synchset)
    nodo= MyNode("")
    #if not token in synchset:
    if token in P_EXP:
        nodo=expresionSimple(S_EXPRESION_SIMPLE)
        if (token in P_REL):
            nodoPadre=MyNode(lineas[2]+" "+token)
            #nodoPadre.linea=lineas[2]
            #nodoPadre.nombre=token
            #nodoPadre.tipo="REL"
            nodo.parent=nodoPadre
            comparar(token)
            nodo=nodoPadre
            hijo=expresionSimple(S_EXPRESION_SIMPLE)
            hijo.parent=nodo
    verificar(synchset, P_EXP)
    return nodo

def expresionSimple(synchset):
    global token,lineas
    verificar(P_EXP_SIM, synchset)
    nodo= MyNode("")
    if token in P_EXP_SIM:
    #if not token in synchset:
        nodo= termino(S_TERMINO)
        while (token == "+" or token == "-"):
            nodoPadre=MyNode(lineas[2]+" "+token)
            #nodoPadre.linea=lineas[2]
            #nodoPadre.nombre=token
            #nodoPadre.tipo="OP"
            nodo.parent=nodoPadre
            if token == "+":
                comparar("+")
            elif token == "-":
                comparar("-")
            nodo=nodoPadre
            hijo=termino(S_TERMINO)
            hijo.parent=nodo

    verificar(synchset, P_EXP_SIM)
    return nodo

def termino(synchset):
    global token,lineas
    verificar(P_TERM, synchset)
    nodo= MyNode("")
    #if not token in synchset:
    if token in P_TERM:
        nodo = factor(S_FACTOR)
        while (token == "/" or token == "*"):
            nodoPadre= MyNode(lineas[2]+" "+token)
            #nodoPadre.linea=lineas[2]
            #nodoPadre.nombre=token
            #nodoPadre.tipo="OP"
            nodo.parent=nodoPadre
            if token == "/":
                comparar("/")
            elif token == "*":
                comparar("*")
            nodo=nodoPadre
            hijo=factor(S_FACTOR)
            hijo.parent=nodo
    verificar(synchset, P_TERM)
    return nodo

def factor(synchset):
    global token,lineas
    verificar(P_FACT, synchset)
    nodo= MyNode("")
    if token in P_FACT:
    #if not token in synchset:

        if (token == "("):

            comparar("(")
            nodo=expresion(S_EXPRESION)
            comparar(")")
        elif (token == "REAL"):
            nodo = MyNode(lineas[0])
            #nodo.linea=lineas[2]
            #nodo.nombre=lineas[0]
            #nodo.tipo="REAL"
            comparar("REAL")
        elif (token == "ENTERO"):
            nodo = MyNode(lineas[0])
            #nodo.linea=lineas[2]
            #nodo.nombre=lineas[0]
            #nodo.tipo="ENTERO"
            comparar("ENTERO")
        else:
            nodo = MyNode(lineas[0])
            #nodo.linea=lineas[2]
            #nodo.nombre=lineas[0]
            #nodo.tipo="ID"
            comparar("IDENTIFICADOR")
    verificar(synchset, P_FACT)
    return nodo

#def recorridoPos(mainNode):
 #   for node in PostOrderIter(mainNode,filter_=lambda n: n.tipo in("Tipo","ListVar","ID")):#Lista variable,Identificador
    #print (node.name," ",node.type)
    #if(node.siblings!=None):
 #       node.siblings[0].type=node.type
        
  #  print(mainNode)    


nodo=principalMain(S_PROGRAMA)
#recorridoPos(nodo)



#print(RenderTree(nodo).by_attr())
#for pre, node in RenderTree(nodo):
 #   print("%s%s" % (pre, node.name))
#RenderTreeGraph(nodo).to_dotfile("arbol.dot")
#archivoArbol.write(RenderTree(nodo).by_attr("lines"))
#for pre, _, node in RenderTree(nodo, childiter=reversed):
#    print("%s%s" % (pre, node))

#print(RenderTree(nodo,style=AbstractStyle("\t","\t","\t")).by_attr())
print(RenderTree(nodo,style=AbstractStyle("","","")))
arbolito=RenderTree(nodo,style=AbstractStyle("","",""))
archivoArbol.write(str(arbolito).replace("MyNode('","").replace("')",""))
#archivoArbol.write(str(arbolito))

#archivoArbol.write(RenderTree(nodo,style=AbstractStyle("|   ","|-- ","|__ ")).by_attr())
#archivoArbol.write(RenderTree(nodo).by_attr())
archivo.close()
archivoError.close()
archivoArbol.close()

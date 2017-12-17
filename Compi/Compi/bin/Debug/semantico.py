import sys
import os
from anytree  import Node, RenderTree, AsciiStyle, AbstractStyle, PostOrderIter, PreOrderIter
from anytree.dotexport import RenderTreeGraph
from sintactico import insertar, regresar, instValue, imprimirTabla, regTipo, memoria, allTable
from Maquina import *

class MyNode(Node):
        separator = "|"
        type=""
        value=""
        nombre=""
        linea=""
        valor=0
        evaluar=0
        leftchild=""
        rightchild=""
        tipo="" 


#nombre=sys.argv[1]
nombre = "C:/Users/cesar/Documents/GitHub/IDE/Compi/Compi/bin/Debug/pruebasSeparadas/impar.vol"
#nombre="/Users/Ruth/Documents/7 semestre/Compiladores/IDE/Compi/Compi/bin/Debug/Semantico/pruebaSem.vol"
#nombre = "pruebaSem.vol"
#nombre="while.vol"
archivo = open(nombre, 'r')
nombreError=nombre.replace("vol","errS")
nombreArbol=nombre.replace("vol","treeSint")
nombreTabla=nombre.replace("vol","table")
nombreSem=nombre.replace("vol","errSem")

nombreMachine=nombre.replace("vol","mach")

if os.path.exists(nombreSem):
    os.remove(nombreSem)
archivoSem = open(nombreSem, "w+")
archivoSem.close()

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

if os.path.exists(nombreMachine):
    os.remove(nombreMachine)
    archivoMachine = open(nombreMachine, "w+")
else:
    archivoMachine = open(nombreMachine, "w+")

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
P_SENT = ["if", "while", "repeat", "cin", "cout", "{", "IDENTIFICADOR","break"]
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


#Generar código intermedio
reservadas=("main","if","then","else","end","do","while","repeat","until","cin","cout","real","int","boolean","break") #lista de palabras reservadas
stmk=("if","while","repeat","cin","cout",":=","break","ASSIGN")
expk=("+","-","*","/",">","<",">=","<=","==","!=")

emitLoc=0 #numero de instruccion emitida
highEmitLoc=0 #localidada TM mas alta que se puede alzanar para usarla junto con emitSkip, emitBackup y emitRestore
fbreak = False
tmpOffset=0
pc=7
mp=6
gp=5
ac=0 #acumulador
ac1=1 #segundo acumulador
#Generar código intermedio

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
    nodo.linea=lineas[2]
    nodo.nombre="ListDec"
    nodo.tipo="ListDec"
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
    nodo.linea=lineas[2]
    nodo.nombre="Dec"
    nodo.tipo="Dec"
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
    nodo.linea=lineas[2]
    nodo.nombre=token
    nodo.tipo="Tipo"
    nodo.type=token
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
    nodoAux.linea=lineas[2]
    nodoAux.nombre="ListVar"
    nodoAux.tipo="ListVar"
    #nodoAux= MyNode("ListVar: "+lineas[2])
    verificar(P_LSTA_VAR, synchset)
    #if not token in synchset:
    if token in P_LSTA_VAR:
        while (token in P_LSTA_VAR):
            nodo=MyNode(lineas[0])
            nodo.tipo="ID"
            nodo.nombre=lineas[0]
            nodo.linea=lineas[2]
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
    nodo_aux.linea=lineas[2]
    nodo_aux.nombre="LISTSENT"
    nodo_aux.tipo="LISTSENT"
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
    nodo.tipo="Sent"
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
        elif (token=="break"):
            nodo=MyNode(lineas[2]+" "+token)
            nodo.tipo="BREAK"
            nodo.linea=lineas[2]
            nodo.nombre=token
            comparar("break")
            comparar(";")
            return nodo
    verificar(synchset, P_SENT)
    return nodo

def seleccionIF(synchset):
    global token,lineas
    verificar(P_SEL, synchset)
    nodo= MyNode("")
    nodo.tipo="IF"
    # if not token in synchset:
    if token in P_SEL:
        nodo = MyNode(lineas[2]+" "+token)
        nodo.linea=lineas[2]
        nodo.nombre=token
        nodo.tipo="IF"
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
    nodo.tipo="WHILE"
    # if not token in synchset:
    if token in P_ITERACION:
        nodo = MyNode(lineas[2]+" "+token)
        nodo.linea=lineas[2]
        nodo.nombre=token
        nodo.tipo="WHILE"
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
    nodo.tipo="REPEAT"
    # if not token in synchset:
    if token in P_REPET:
        nodo = MyNode(lineas[2]+" "+token)
        nodo.linea=lineas[2]
        nodo.nombre=token
        nodo.tipo="REPEAT"
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
    nodo.tipo="CIN"
    # if not token in synchset:
    if token in P_SENT_CIN:
        comparar("cin")  # nodo padre
        nodo = MyNode(lineas[2]+" cin: "+lineas[0])
        nodo.linea=lineas[2]
        nodo.nombre=lineas[0]
        nodo.tipo="CIN"
        comparar("IDENTIFICADOR")  # lo que lee es su atributo o nombre
        comparar(";")
    verificar(synchset, P_SENT_CIN)
    return nodo

def sentCout(synchset):
    global token,lineas
    verificar(P_SENT_COUT, synchset)
    nodo= MyNode("")
    nodo.tipo="COUT"
    # if not token in synchset:
    if token in P_SENT_COUT:
        nodo= MyNode(lineas[2]+" "+token)
        nodo.linea=lineas[2]
        nodo.nombre=token
        nodo.tipo="COUT"
        comparar("cout")  # nodo padre
        expresion(S_EXPRESION).parent=nodo  # nodo hijo
        comparar(";")
    verificar(synchset,P_SENT_COUT)
    return nodo

def bloque(synchset):
    global token
    verificar(P_BLOQUE, synchset)
    nodo= MyNode("")
    nodo.tipo="BLOQUE"
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
    nodo.tipo="ASSIGN"
    # if not token in synchset:
    if token in P_ASIGN:
        nodo = MyNode(lineas[2]+" Assign "+lineas[0])
        nodo.linea=lineas[2]
        nodo.nombre=lineas[0]
        nodo.tipo="ASSIGN"
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
    nodo.tipo="EXP"
    #if not token in synchset:
    if token in P_EXP:
        nodo=expresionSimple(S_EXPRESION_SIMPLE)
        if (token in P_REL):
            nodoPadre=MyNode(lineas[2]+" "+token)
            nodoPadre.linea=lineas[2]
            nodoPadre.nombre=token
            nodoPadre.tipo="REL"
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
    nodo.tipo="EXPSIMP"
    if token in P_EXP_SIM:
    #if not token in synchset:
        nodo= termino(S_TERMINO)
        while (token == "+" or token == "-"):
            nodoPadre=MyNode(lineas[2]+" "+token)
            nodoPadre.linea=lineas[2]
            nodoPadre.nombre=token
            nodoPadre.tipo="OP"
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
    nodo.tipo="TERM"
    #if not token in synchset:
    if token in P_TERM:
        nodo = factor(S_FACTOR)
        while (token == "/" or token == "*"):
            nodoPadre= MyNode(lineas[2]+" "+token)
            nodoPadre.linea=lineas[2]
            nodoPadre.nombre=token
            nodoPadre.tipo="OP"
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
    nodo.tipo="FACT"
    if token in P_FACT:
    #if not token in synchset:

        if (token == "("):

            comparar("(")
            nodo=expresion(S_EXPRESION)
            comparar(")")
        elif (token == "REAL"):
            nodo = MyNode(lineas[0])
            nodo.linea=lineas[2]
            nodo.nombre=lineas[0]
            nodo.tipo="REAL"
            nodo.value=float(lineas[0])
            comparar("REAL")
        elif (token == "ENTERO"):
            nodo = MyNode(lineas[0])
            nodo.linea=lineas[2]
            nodo.nombre=lineas[0]
            nodo.tipo="ENTERO"
            nodo.value=int(lineas[0])
            comparar("ENTERO")
        else:
            nodo = MyNode(lineas[0])
            nodo.linea=lineas[2]
            nodo.nombre=lineas[0]
            nodo.tipo="ID"
            #nodo.value=lineas[0]
            comparar("IDENTIFICADOR")
    verificar(synchset, P_FACT)
    return nodo

def recorridoPosTipo(mainNode):
    permitidos= ["Tipo","ListVar"]
    for node in PostOrderIter(mainNode):#Lista variable,Identificador
        if(permitidos.__contains__(node.tipo) and node.siblings):
            node.siblings[0].type=node.type
        
    #print(RenderTree(mainNode,style=AbstractStyle("","","")))    
 
def recorridoPreTipo(mainNode):
    permitidos= ["ListVar"]
    for node in PreOrderIter(mainNode):#Lista variable,Identificador
        if(permitidos.__contains__(node.tipo) and node.children):
            for nodo in node.children:
                nodo.type=node.type
                print(nodo)
        
    #print(RenderTree(mainNode,style=AbstractStyle("","","")))    

def parser(number):
    #print("Es entero " + str(type(number) is int))
    #print("Es float "+str(type(number) is float))
    #print("Es str " +str(type(number) is str))
    if( not isinstance(number,int) and not isinstance(number,float) and isinstance(number,str)  ):
        if "." not in number:
            return int(number)
        else:
            return float(number) 
    else:
         return number


def recorridoPosValor (mainNode):
    permitidos=["ID","EXP","EXPSIMP","TERM","FACT","REAL","ENTERO","OP","ASSIGN","REL","COUT"]
    for node in PostOrderIter(mainNode):
        if(permitidos.__contains__(node.tipo) and node.parent):
            if(node.parent.tipo!="ListVar"):
                #Trae el valor que tiene en tabla
                if node.tipo!="ENTERO" and node.tipo!="REAL" and node.tipo!="OP" and node.tipo!="ASSIGN" and node.tipo!="REL" and node.tipo!="COUT":
                    node.value=regresar(node.nombre)
                    node.evaluar=1

                if node.evaluar==2:
                    if node.tipo=="ASSIGN":
                        if regTipo(node.nombre)=="real":
                            node.value=float(node.leftchild)
                        else:
                            node.value=node.leftchild
                        instValue(node)
                    elif node.tipo=="OP":
                        if(node.nombre=='+'):
                            node.value=parser(node.leftchild)+parser(node.rightchild)
                        elif (node.nombre=='*'):
                            if isinstance(parser(node.leftchild),int) and isinstance(parser(node.rightchild),int):
                            #if(node.type=="int"):
                                node.value=int(parser(node.leftchild)*parser(node.rightchild))
                            else:
                                node.value=parser(node.leftchild)*parser(node.rightchild)

                        elif(node.nombre=='/'):
                            if ((node.rightchild=='0') or (node.rightchild==0)):
                                archivoSem=open(nombreSem,"a")
                                archivoSem.write("Division entre cero  en linea: "+str(node.linea)+"\n")
                                archivoSem.close()
                                node.value=0
                            else:
                                if isinstance(parser(node.leftchild),int) and isinstance(parser(node.rightchild),int):
                            #if(node.type=="int"):
                                    node.value=int(parser(node.leftchild)/parser(node.rightchild))
                                else:
                                    node.value=parser(node.leftchild)/parser(node.rightchild)
                            
                                

                        elif(node.nombre=='-'):
                            node.value=parser(node.leftchild)-parser(node.rightchild)
                    elif node.tipo=="COUT":
                        node.value=node.leftchild
                    elif node.tipo=="REL":
                        if node.nombre=="!=":
                            if node.leftchild != node.rightchild:
                                node.value=1
                            else:
                                node.value=0
                        elif node.nombre=="==":
                            if node.leftchild == node.rightchild:
                                node.value=1
                            else:
                                node.value=0
                        elif node.nombre==">=":
                            if node.leftchild >= node.rightchild:
                                node.value=1
                            else:
                                node.value=0
                        elif node.nombre=="<=":
                            if node.leftchild <= node.rightchild:
                                node.value=1
                            else:
                                node.value=0
                        elif node.nombre=="<":
                            if node.leftchild < node.rightchild:
                                node.value=1
                            else:
                                node.value=0
                        elif node.nombre == '>':
                            if node.leftchild > node.rightchild:
                                node.value=1
                            else:
                                node.value=0
                
                if not node.siblings and node.parent.evaluar!=2:
                    node.parent.leftchild=node.value
                    node.parent.evaluar=2

                if node.parent.evaluar==0:
                    node.parent.leftchild=node.value
                    node.parent.evaluar=1
                elif node.parent.evaluar==1:
                    node.parent.rightchild=node.value
                    node.parent.evaluar=2

    print(RenderTree(mainNode,style=AbstractStyle("","","")))


def cleanTree(nodo):
    for node in PostOrderIter(nodo):
        #if(nodo.is_leaf ):
        node.name+="      Tipo= "+node.type+"     Valor= "+str(node.value)
    print(RenderTree(nodo,style=AbstractStyle("","","")))


#Generador codigo intermedio
def genRM(op,r,d,s):
    global emitLoc
    global highEmitLoc
    code=str(emitLoc)+": "+str(op)+"  "+str(r)+","+str(d)+"("+str(s)+") \n";
    emitLoc+=1
    archivoMachine.write(code)
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc



#emitSkip retorna cuantas omisiones o saltos de localidades de codigo hay despues del backpatch
def emitSkip(hm):
    global emitLoc
    global highEmitLoc
    i=emitLoc
    emitLoc+=hm
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc
    return i

def emitComment(com):
    archivoMachine.write("* "+com+" \n")

#emitBackup regresa a la localidad antes del salto. loc =a
def emitBackup(loc):
    global emitLoc
    global highEmitLoc
    if loc > highEmitLoc:
        emitComment("BUG in emitBackup\n")
    emitLoc = loc

#convierte una referencia absoluta a una referencia relativa de pc que emite una instruccion RM
def emitRM_Abs(op,r,a):
    global emitLoc
    global highEmitLoc
    x=a-(emitLoc+1)
    code=str(emitLoc)+": "+str(op)+"  "+str(r)+","+str(x)+"("+str(pc)+") \n"
    emitLoc+=1
    archivoMachine.write(code)
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc

#restarura la actual posicion del codigo a la mas alta previamente posicion sin emitir
def emitRestore():
    global emitLoc
    global highEmitLoc
    emitLoc = highEmitLoc

#emite instrucciones TM de register-only
def emitRO(op,r,s,t):
    global emitLoc
    global highEmitLoc
    code=str(emitLoc)+": "+str(op)+"  "+str(r)+","+str(s)+","+str(t)+" \n";
    emitLoc+=1
    archivoMachine.write(code)
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc



def es_id(texto):
    try:
        if texto[0].isalpha():
            if texto in reservadas:
                return False
            else:
                return True
        else:
            return False
    except IndexError:
        return False

def es_num(texto):
    try:
        float(texto)
        return True
    except ValueError:
        return False

#emite instrucciones TM de register-to-memory
def emitRM(op,r,d,s):
    global emitLoc
    global highEmitLoc
    code=str(emitLoc)+": "+str(op)+"  "+str(r)+","+str(d)+"("+str(s)+") \n";
    emitLoc+=1
    archivoMachine.write(code)
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc

#def genSentencia(raiz):
def evaluar(raiz):
    global fbreak,b,tmpOffset
    if raiz.nombre=="if":
        #p1=raiz.children[0] #condicion
        #p2=raiz.children[1] #parte verdadera
        evaluar(raiz.children[0])
        savedLoc1 = emitSkip(1)
        InterCodeGen(raiz.children[1])
        savedLoc2 = emitSkip(1)
        currentLoc = emitSkip(0)
        emitBackup(savedLoc1)
        emitRM_Abs("JEQ",ac,currentLoc)
        emitRestore()
        if len(raiz.children) > 2:
            InterCodeGen(raiz.children[2]) #parte falsa
        currentLoc = emitSkip(0)
        emitBackup(savedLoc2)
        emitRM_Abs("LDA",pc,currentLoc)
        emitRestore()
    elif raiz.nombre=="while":
        p1=raiz.children[0] #condicion
        p2=raiz.children[1] #cuerpo
        savedLoc1 = emitSkip(0)
        evaluar(p1)
        savedLoc2 = emitSkip(1)
        InterCodeGen(p2)
        currentLoc = emitSkip(0)
        emitBackup(savedLoc2)
        emitRM_Abs("JEQ",ac,currentLoc+1)
        if fbreak:
            #emitBackup(breakLoc)
            emitBackup(b)
            emitRM_Abs("LDA",pc,currentLoc+1)
            fbreak = False
        emitRestore()
        emitRM_Abs("LDA",pc,savedLoc1)
    elif raiz.nombre=="repeat":
        p1=raiz.children[0] #cuerpo
        p2=raiz.children[1] #condicion
        savedLoc1 = emitSkip(0)
        #emitComment("repeat: jump after body comes back here")
        # generacion de codigo para el cuerpo
        InterCodeGen(p1)
        # generacion de codigo para la parte de prueba
        evaluar(p2)
        if fbreak:
            currentLoc=emitSkip(0)
            emitBackup(b)
            emitRM_Abs("LDA",pc,currentLoc+1)
            fbreak = False
            emitRestore()
        emitRM_Abs("JEQ",ac,savedLoc1)
    elif raiz.tipo=="ASSIGN": #:=
        #buscamos su localidad de memoria en la tabla hash
        loc=memoria(raiz.nombre)
        # generacion de codugo para id
        evaluar(raiz.children[0])
        #loc = d[raiz.children[0].nombre].locmem
        genRM("ST",ac,loc,gp)
        #emitComment("<- assign")
    elif raiz.tipo=="CIN":
        emitRO("IN",ac,0,0)
        loc=memoria(raiz.nombre)
        #loc = d[raiz.children[0].nombre].locmem
        genRM("ST",ac,loc,gp)
    elif raiz.nombre=="cout":
        InterCodeGen(raiz.children[0])
        #ahora lo muestra
        emitRO("OUT",ac,0,0)
    elif raiz.nombre=="break":
        fbreak=True
        breakLoc=emitSkip(1)
        b=breakLoc
        #print(str(breakLoc))

#def genExpresion(raiz):
    #global d
    #global tmpOffset
    elif es_num(raiz.nombre):
        #emitComment("-> Const")
        #generacion de codigo para carga de constante
        emitRM("LDC",ac,raiz.nombre,0)
    elif es_id(raiz.nombre):
        #emitComment("-> Id")
        loc=memoria(raiz.nombre)
        #loc = d[raiz.nombre].locmem
        emitRM("LD",ac,loc,gp)
    elif raiz.nombre in expk:
        #emitComment("-> Op")
        p1 = raiz.children[0]
        p2 = raiz.children[1]
        # gen code for ac = left arg
        evaluar(p1)
        #gen code to push left operand
        emitRM("ST",ac,tmpOffset,mp)
        tmpOffset-=1
        # gen code for ac = right operand
        evaluar(p2)
        # now load left operand
        tmpOffset+=1
        emitRM("LD",ac1,tmpOffset,mp)
        if raiz.nombre=="+":
            emitRO("ADD",ac,ac1,ac)
        elif raiz.nombre=="-":
            emitRO("SUB",ac,ac1,ac)
        elif raiz.nombre=="*":
            emitRO("MUL",ac,ac1,ac)
        elif raiz.nombre=="/":
            emitRO("DIV",ac,ac1,ac)
        elif raiz.nombre=="<":
            emitRO("SUB",ac,ac1,ac)
            emitRM("JLT",ac,2,pc)
            emitRM("LDC",ac,0,ac)
            emitRM("LDA",pc,1,pc)
            emitRM("LDC",ac,1,ac)
        elif raiz.nombre=="<=":
            emitRO("SUB",ac,ac1,ac)
            emitRM("JLE",ac,2,pc)
            emitRM("LDC",ac,0,ac)
            emitRM("LDA",pc,1,pc)
            emitRM("LDC",ac,1,ac)
        elif raiz.nombre==">":
            emitRO("SUB",ac,ac1,ac)
            emitRM("JGT",ac,2,pc)
            emitRM("LDC",ac,0,ac)
            emitRM("LDA",pc,1,pc)
            emitRM("LDC",ac,1,ac)
        elif raiz.nombre=="<=":
            emitRO("SUB",ac,ac1,ac)
            emitRM("JGE",ac,2,pc)
            emitRM("LDC",ac,0,ac)
            emitRM("LDA",pc,1,pc)
            emitRM("LDC",ac,1,ac)
        elif raiz.nombre=="==":
            emitRO("SUB",ac,ac1,ac)
            emitRM("JEQ",ac,2,pc)
            emitRM("LDC",ac,0,ac)
            emitRM("LDA",pc,1,pc)
            emitRM("LDC",ac,1,ac)
        elif raiz.nombre=="!=":
            emitRO("SUB",ac,ac1,ac)
            emitRM("JNE",ac,2,pc)
            emitRM("LDC",ac,0,ac)
            emitRM("LDA",pc,1,pc)
            emitRM("LDC",ac,1,ac)

'''
def InterCodeGen(raiz):
    if raiz!=None:
        if raiz.nombre in stmk:
            genSentencia(raiz)
        elif raiz.nombre in expk or es_id(raiz.nombre) or es_num(raiz.nombre):
            genExpresion(raiz)
        #InterCodeGen(raiz.children[0])
        #InterCodeGen(raiz.children[1]) '''

def InterCodeGen(raiz):
    if raiz.nombre=="LISTSENT":
        for i in range(0, len(raiz.children)):
            InterCodeGen(raiz.children[i])
    else:
        evaluar(raiz)

def generator(raiz):
    global mp
    global ac
    #emitComment("Compilacion de Tiny para codigo TM")
    #emitComment("Preludio estandar: ")
    genRM("LD",mp,0,ac)
    genRM("ST",ac,0,ac)
    #emitComment("End of standard prelude.")
    InterCodeGen(raiz)
    #emitComment("End of execution.");
    emitRO("HALT",0,0,0);


#FIN generador codigo intermedio


nodo=principalMain(S_PROGRAMA)
recorridoPosTipo(nodo)
recorridoPreTipo(nodo)
print("VALUE")


insertar(nodo,nombreSem)
recorridoPosValor(nodo)


#Generador codigo intermedio
generator(nodo.children[1])

#FIN generador codigo intermedio

imprimirTabla(nombreTabla)

#archivoTabla= open(nombreTabla,"w+")
archivoMachine.close()



print("Clean")
cleanTree(nodo)

arbolito=RenderTree(nodo,style=AbstractStyle("","",""))
archivoArbol.write(str(arbolito).replace("MyNode('","").replace("')","").replace("\'","").replace(")",""))
archivoArbol.close()


archivo.close()
archivoError.close()

archivoMachine = open(nombreMachine, "r")
makina=Maquina(archivoMachine,nombreTabla)
makina.correr()
archivoMachine.close()

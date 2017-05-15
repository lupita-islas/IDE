nombre=""
archivo=open(nombre,'r')
token=""
ERROR="False"
global lineas
global token
global ERROR

#conjuntos siguiente
S_PROGRAMA=["$"]
S_LIST_DEC=["if","while","repeat","cin","cout","{","IDENTIFICADOR","}"]
S_DECLARACION=[";"]
S_TIPO=["IDENTIFICADOR"]
S_LISTA_VARIABLES=[";"]
S_LISTA_SENTENCIAS=["}"]
S_SENTENCIA=["if","while","repeat","cin","cout","{","IDENTIFICADOR","}"]
S_SELECCION=S_SENTENCIA
S_ITERACION=S_SENTENCIA
S_REPETICION=S_SENTENCIA
S_SENT_CIN=S_SENTENCIA
S_COUT=S_SENTENCIA
S_BLOQUE =[S_SENTENCIA,"until","else"]
S_ASIGNACION= S_SENTENCIA
S_EXPRESION= [")",";"]
S_RELACION = ["(","REAL","ENTERO","IDENTIFICADOR"]
S_EXPRESION_SIMPLE= ["<=",">","<",">=","==","!=",")",";","+","-"]
S_SUMA_OPL=["(","REAL","ENTERO","IDENTIFICADOR"]
S_TERMINO = ["<=",">","<",">=","==","!=",")",";","+","-","*","/"]
S_MULT_OP = ["(","REAL","ENTERO","IDENTIFICADOR"]
S_FACTOR = ["<=",">","<",">=","==","!=",")",";","+","-","*","/"]
S_IDENTIFICADOR = [",",":",":=",S_FACTOR]
S_NUMERO=S_FACTOR
S_CP= ["THEN","{",";",S_FACTOR]
S_IF=["("]
S_INT = S_REAL =S_BOOLEAN = [S_IDENTIFICADOR]
S_THEN = ["{"]
S_WHILE= ["("]
S_REPEAT = ["{"]
S_UNTIL = ["("]
S_CIN = [S_IDENTIFICADOR]
S_COUT = ["(","REAL","ENTERO", "IDENTIFICADOR"]
S_ASSIGN = ["(","REAL","ENTERO", "IDENTIFICADOR"]
S_MAIN=["{"]

#CONJUNTOS PRIMERO
P_PROGRAMA=["main"]
P_LISTA_DECLARACION = ["int","real","boolean", vacio] #]****************+
P_DECLARACION =["int","real","boolean"]
P_TIPO = ["int","real","boolean"]
P_LSTA_VAR= ["IDENTIFICADOR"]
P_LSTA_SENT=["if","while","repeat","cin","cout","{","IDENTIFICADOR",vacio]
P_SENT=["if","while","repeat","cin","cout","{","IDENTIFICADOR"]
P_SEL=["if"]
P_ITERACION=["while"]
P_REPET=["repeat"]
P_SENT_CIN=["cin"]
P_SENT_COUT=["cout"]
P_BLOQUE=["{"]
P_ASIGN=["IDENTIFICADOR"]
P_EXP=["(","REAL","ENTERO","IDENTIFICADOR"]
P_REL=["<=","<",">",">=","==","!="]
P_EXP_SIM=["(","REAL","ENTERO","IDENTIFICADOR"]
P_SUM=["+","-"]
P_TERM=["(","REAL","ENTERO","IDENTIFICADOR"]
P_MUL=["*","/"]
P_FACT=["(","REAL","ENTERO","IDENTIFICADOR"]


def verificar(primero, siguiente):
    global token
    if not token in primero :
        error()
        scanto(primero+siguiente)

def scanto(synchset):
    global token
    synchset.append("$")
    while not token in synchset:
            token=leer()

def error():
    global ERROR
    print "Error"
    #error en linea->lineas[2] y columna-> lineas[3]
    #error=lineas[0]
    ERROR="True"
    #mandar a archivo que César sabe ;) :*


def comparar(token_esperado):
    global token
    if (token==token_esperado):
        token=leer()
    else:
        error()

def leer():
     linea=archivo.readline()
     lineas=linea.split(" ")
     if lineas[1] != "IDENTIFICADOR" or lineas[1] != "REAL" or lineas[1] != "ENTERO" or lineas[1] != "OPERADOR":
         return lineas[0]
     else:
         return lineas[1] #lineas con 0=token 1=lexema

def principalMain(): #checar
    global token
    token=leer();
    comparar("main")
    comparar("{")
    listaDeclaracion(S_LIST_DEC)
    listaSentencias(S_LISTA_SENTENCIAS)
    comparar("}")

def listaDeclaracion(synchset):
    global token
    #while var==0: #Mientras la declaracion sea vacia
    verificar(P_LISTA_DECLARACION,synchset)
    if not token in synchset:
        while(token in P_LISTA_DECLARACION):

            declaracion(S_DECLARACION)
            comparar(";")
            verificar(synchset,P_LISTA_DECLARACION)

def declaracion(synchset):
    global token
    verificar(P_DECLARACION,synchset)
    if not token in synchset:
        tipo(S_TIPO)
        listaVariables(S_LISTA_VARIABLES)
        verificar(synchset,P_DECLARACION)

def tipo(synchset): #checar
    global token
    verificar(P_TIPO,synchset)
    if not token in synchset:
        if token=="int":
            comparar("int")
        elif token  == "real":
            comparar("real")
        elif token == "boolean":
            comparar("boolean")
        verificar(synchset,P_TIPO)


def listaVariables(synchset):
    global token
    verificar(P_LSTA_VAR,synchset)
    if not token in synchset:
        while(token in P_LSTA_VAR):
            comparar("IDENTIFICADOR")
            if (token!=","):
                break
            else:
                comparar(",")
        verificar(synchset,P_LSTA_VAR)


def listaSentencias(synchset):
    global token
    verificar(P_LSTA_SENT,synchset)
    if not token in synchset:
        while(token in P_LSTA_SENT):
            sentencia(S_SENTENCIA)
        verificar(synchset,P_LSTA_SENT)

def sentencia(synchset):
    global token
    verificar(P_SENT,synchset)
    if not token in synchset:
        if(token=="if"):
            seleccionIF(S_IF)
        if (token == "while"):  # while
            iteracionWhile(S_ITERACION)
        elif (token == "repeat"):  # for
            repeticion(S_REPEAT)
        elif (token == "cin"):  # CIN
            sentCin(S_CIN)
        elif (token == "cout"):
            sentCout(S_COUT)
        elif (token == "IDENTIFICADOR"):  # identificador CHECAR
            sentCout(S_IDENTIFICADOR)
        else:  # bloque
            bloque(S_BLOQUE)
        verificar(synchset,P_SENT)

def seleccionIF(synchset):
    global token
    verificar(P_SEL,synchset)
    if not token in synchset:
        comparar("if")
        comparar("(")
        #nodo padre
        expresion(S_EXPRESION) #nodo hijo primero
        comparar(")")
        comparar("then")
        bloque(S_THEN) #hijo dos
        if(token=="else"):
            comparar("else")
            bloque(S_BLOQUE) #nodo hijo tres
        verificar(synchset,P_SEL)

def iteracionWhile(synchset):
    global token
    verificar(P_ITERACION,synchset)
    if not token in synchset:
        comparar("while") #nodo padre
        comparar("(")
        expresion(S_EXPRESION) #nodo hijo 1
        comparar(")")
        bloque(S_BLOQUE) #nodo hijo 2
        verificar(synchset,P_ITERACION)

def repeticion(synchset):
    global token
    verificar(P_REPET,synchset)
    if not token in synchset:
        comparar("repeat") #nodo padre
        bloque(S_BLOQUE) #nodo hijo 1
        comparar("until")
        comparar("(")
        expresion(S_EXPRESION) #nodo hijo 2
        comparar(")")
        comparar(";")
        verificar(synchset,P_REPET)

def sentCin(synchset): #es solo el nodo padre
    global token
    verificar(P_SENT_CIN,synchset)
    if not token in synchset:
        comparar("cin") #nodo padre
        comparar("IDENTIFICADOR") #lo que lee es su atributo o nombre
        comparar(";")
        verificar(synchset,P_SENT_CIN)

def sentCout(synchset):
    global token
    verificar(P_SENT_COUT,synchset)
    if not token in synchset:
        comparar("cout") #nodo padre
        expresion(S_EXPRESION) #nodo hijo
        comparar(";")

def bloque(synchset):
    global token
    verificar(P_BLOQUE, synchset)
    if not token in synchset:
        comparar("{")
        listaSentencias(S_LISTA_SENTENCIAS)
        comparar("}")
        verificar(synchset,P_BLOQUE)

def asignacion(synchset):
    global token
    verificar(P_ASIGN,synchset)
    if not token in synchset:
        comparar("IDENTIFICADOR")
        comparar(":=")
        expresion(S_EXPRESION)
        comparar(";")
        verificar(synchset,P_ASIGN)

def expresion(synchset):
    global token
    verificar(P_EXP,synchset)
    if not token in synchset:
        expresionSimple(S_EXPRESION_SIMPLE)
        if (token == "OPERADOR"):
            comparar("OPERADOR")
            expresionSimple(S_EXPRESION_SIMPLE)
        verificar(synchset,P_EXP)

def expresionSimple(synchset):
    global token
    verificar(P_EXP_SIM,synchset)
    if not token in synchset:
        termino(S_TERMINO)
        while(token=="+" or token =="-"):
            if token=="+":
                comparar("+")
            elif token=="-":
                comparar("-")
            termino(S_TERMINO)
        verificar(synchset,P_EXP_SIM)

def termino(synchset):
    global token
    verificar(P_TERM,synchset)
    if not token in synchset:
        factor(S_FACTOR)
        while(token=="/" or token=="*"):
            if token =="/":
                comparar("/")
            elif token =="*":
                comparar("*")
            factor(S_FACTOR)
        verificar(synchset,P_TERM)

def factor(synchset):
    global token
    verificar(P_FACT,synchset)
    if not token in synchset:
        if(token=="("):
            comparar("(")
            expresion(S_EXPRESION)
            comparar(")")
        elif(token=="REAL"):
            comparar("REAL")
        elif (token == "ENTERO"):
            comparar("ENTERO")
        else:
            comparar("IDENTIFICADOR")
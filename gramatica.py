nombre=""
archivo=open(nombre,'r')
global lineas
global lineas[0]

def leer(token):
    if(lineas[0] == token ):
        linea=archivo.readline()
        lineas=linea.split(" ")
        #lineas[0]=linea[0]
        #return lineas #lineas con 0=token 1=lexema
    else:
        error()

def principalMain(): #checar
    leer ("main")
    listaDeclaracion()
    listaSentencias()

def listaDeclaracion():

    #while var==0: #Mientras la declaracion sea vacia
        declaracion()

def declaracion():
    tipo()
    listaVariables()

def tipo(): #checar
    if(leer().__contains__("int") or leer().__contains__("float") or leer().__contains__("boolean")):
        #aqui hacer algo XD
        listaVariables()


def listaVariables():
    while(leer().__contains__("IDENTIFICADOR")): #Ver condicion de paro
        identificador()

def listaSentencias():
    sentencia()

def sentencia():

    if(lineas[0]=="if"):
        seleccionIF()
    if(lineas[0]=="while"):#while
        iteracionWhile()
    elif(lineas[0]=="do"): #for
        repeticionDoUntil()
    elif(lineas[0]=="cin"): #CIN
        sentCin()
    elif(lineas[0]=="cout"):
        sentCout()
    elif (lineas[1] == "IDENTIFICADOR"):#identificador CHECAR
        sentCout()
    else: #bloque
        bloque()

def seleccionIF():
    leer("if")
    leer ("(")
    #nodo padre
    expresion() #nodo hijo primero
    leer(")")
    bloque() #hijo dos
    if(lineas[0]=="else"):
            leer("else")
            bloque() #nodo hijo tres

def iteracionWhile():
    leer("while") #nodo padre
    leer("(")
    expresion() #nodo hijo 1
    leer(")")
    bloque() #nodo hijo 2

def repeticionDoUntil():
    leer("do") #nodo padre
    bloque() #nodo hijo 1
    leer("until")
    leer ("(")
    expresion() #nodo hijo 2
    leer(")")
    leer(";")

def sentCin(): #es solo el nodo padre
    leer("cin") #nodo padre
    identificador() #lo que lee es su atributo o nombre
    leer(";")

def sentCout():
    leer("cout") #nodo padre
    expresion() #nodo hijo
    leer(";")

def bloque():
    #while(True): #Cambiar condicion de paro
    listaSentencias()

def asignacion():
    if(leer().__contains__("IDENTIFICADOR")):
        if(leer().__contains__(":=")):
            expresion()
        else:
            print("Error") ##Aqui ver los errores

def expresion():
    expresionSimple()
    if(lineas[0]=="<=" or lineas[0]=="<" or lineas[0]==">" or lineas[0]==">=" or lineas[0] =="=" or lineas[0]=="!="):
        expresionSimple()

def expresionSimple():
    termino()

    if(leer().__contains__("+") or leer().__contains__("-")):
        termino()

def termino():
    factor()
    while(leer().__contains__("/") or leer().__contains__("*")):
            factor()

def factor():
    if(leer().__contains__("(")):
        expresion()
    elif(leer().__contains__("numero")):
        print("Aqui hay un numero")
    else:
        print("identificador")


def bloque():
    leer()
    while(leer().__contains__("\n")):
        leer();

def identificador():
    if  not leer().__contains__("identificador"):
        print("error")

nombre=""
archivo=open(nombre,'r')
global lineas

def leer():
    linea=archivo.readline()
    lineas=linea.split(" ")
    return lineas

def principalMain():
    listaDeclaracion()
    listaSentencias()

def listaDeclaracion():

    #while var==0: #Mientras la declaracion sea vacia
        declaracion()

def declaracion():
    tipo()

def tipo():
    if(leer().__contains__("int") or leer().__contains__("float") or leer().__contains__("boolean")):
        #aqui hacer algo XD
        listaVariables()


def listaVariables():
    while(leer().__contains__("IDENTIFICADOR")): #Ver condicion de paro
        identificador()

def listaSentencias():
    sentencia()

def sentencia():

    if(leer().__contains__("seleccion")):
        seleccionIF()
    if(leer().__contains__("iteracion")):#while
        iteracionWhile()
    elif(leer().__contains__("repeticion")): #for
        repeticionDoUntil()
    elif(leer().__contains__("sent-cin")): #CIN
        sentCin()
    elif(leer().__contains__("sent-out")):
        sentCout()
    else:
        bloque()

def seleccionIF():
    expresion()
    if(leer().__contains__("then")):
            bloque()
   #Aqui poner la condicion de paro
    if(leer().__contains__("else")):
            bloque()

def iteracionWhile():
    expresion()
    bloque()

def repeticionDoUntil():
    bloque()
    if(leer().__contains__("until")):
        expresion()
    else:
        print ("error")

def sentCin():
    identificador()

def sentCout():
   expresion()

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
    if(leer().__contains__("<=") or leer().__contains__("<") or
     leer().__contains__(">") or leer().__contains__(">=") or
    leer().__contains__("=") or leer().__contains__("!=")):
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

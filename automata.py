especiales=["{", "}","(",")",";",":","&",","]
operadores=["*","%"]
ignorar=["\n","\t"," "]
ncol=0
nfil=0
max=0
linea_actual=""
Token_externo = {
    "tipo": "",
    "lexema": ""
}

def get_character(linea):
    global ncol
    global nfil
    global max
    global linea_actual
    if (ncol==0 or ncol==max):
        linea_actual=linea.readline()
        if linea_actual != "":
            ncol=0
            nfil+=1
            max=len(linea_actual)
        else:
            return "EOF"

    c=linea_actual[ncol]
    ncol+=1
    return c

def iden_lex(linea,x):
    Token = {
        "tipo": "",
        "lexema": ""
    }
    c=get_character(linea)
    estado = "START"
    #x=0
    TAM=len(linea)
    while(estado!="END" and x<TAM):
        if estado == "START":
            if linea[x].isalpha():
                estado="IDEN"
                Token["lexema"]+=linea[x]
                x+=1
            elif linea[x]=="/":
                estado="SLASH"
                Token["lexema"] += linea[x]
                x += 1
            elif linea[x]=="+":
                estado="ADD"
                Token["lexema"] += linea[x]
                x += 1
            elif linea[x]=="-":
                estado="MINUS"
                Token["lexema"] += linea[x]
                x += 1
            elif linea[x]=="=":
                estado="EQ"
                Token["lexema"] += linea[x]
                x += 1
            elif linea[x]=="<":
                estado="LT"
                Token["lexema"] += linea[x]
                x += 1
            elif linea[x]==">":
                estado="HT"
                Token["lexema"] += linea[x]
                x += 1
            elif linea[x]==":":
                estado="ASSIGN"
                Token["lexema"] += linea[x]
                x += 1
            elif linea[x]=="!":
                estado="NEQ"
                Token["lexema"] += linea[x]
                x += 1
            elif linea[x].isdigit():
                estado="ENTERO"
                Token["lexema"] += linea[x]
                x += 1

            elif ignorar.__contains__(linea[x]):
               x+=1
            else:
                estado = "END"
                Token["lexema"] += linea[x]
                if especiales.__contains__(linea[x]):
                    Token["tipo"]="SIMBOLO"
                elif operadores.__contains__(linea[x]):
                    Token["tipo"]="OPERADOR"
                else:
                    Token["tipo"] = "ERROR"
                x += 1

        elif estado=="IDEN":
            Token["tipo"] = "IDENTIFICADOR"
            if (linea[x].isalpha() or linea[x].isdigit() or linea[x]=="_"):
                Token["lexema"] += linea[x]
                x+=1
            else:
                #x-=1
                estado="END"
        elif estado == "SLASH":
            if linea[x]=="/":
                x+=1
                while linea[x]!="\n":
                    x+=1
            elif linea[x]=="*":
                x += 1
                hecho=False
                while hecho==False:
                    while (linea[x]!="*"):
                        x+=1
                    while (linea[x]=="*"):
                        x+=1
                    if(linea[x]=="/"):
                        hecho=True
            else:
                Token["tipo"]="OPERADOR"
                estado="END"
        elif estado == "ADD":
            if(linea[x]=="+"):
                Token["tipo"]="OPERADOR"
                Token["lexema"]+=linea[x]
                estado="END"
                x+=1
            elif linea[x].isnumeric():
                estado="ENTERO"
                x+=1
            else:
                estado="END"
                x-=1
        elif estado == "MINUS":
            if (linea[x] == "-"):
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += linea[x]
                estado = "END"
                x += 1
            elif linea[x].isdigit():
                estado = "ENTERO"
                x += 1
            else:
                estado = "END"
                x -= 1
        elif estado=="ENTERO":
            while(x<TAM and linea[x].isdigit() ):
                Token["lexema"] += linea[x]
                x+=1
            if x<TAM and linea[x]==".":
                Token["lexema"] += linea[x]
                x+=1
                if x<TAM and linea[x].isdigit():
                    Token["lexema"] += linea[x]
                    x+=1
                    while x<TAM and linea[x].isdigit():
                        Token["lexema"] += linea[x]
                        x+=1
                    estado="END"
                    Token["tipo"] = "REAL"
                    #x-=1
                else:
                    estado="END"
                    Token["tipo"] = "ERROR"
                    x+=1
            else:
                estado="END"
                Token["tipo"] = "ENTERO"
                #x-=1



        elif estado=="EQ":
            if linea[x]=="=":
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += linea[x]
                estado = "END"
            else:
                estado = "END"
                x -= 1
        elif estado=="LT":
            if linea[x]=="=":
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += linea[x]
                estado = "END"
            else:
                estado = "END"
                x -= 1
        elif estado=="HT":
            if linea[x]=="=":
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += linea[x]
                estado = "END"
            else:
                estado = "END"
                x -= 1
        elif estado=="ASSIGN":
            if linea[x]=="=":
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += linea[x]
                estado = "END"
            else:
                estado = "END"
                x -= 1
        elif estado=="NEQ":
            if linea[x]=="=":
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += linea[x]
                estado = "END"
            else:
                estado = "END"
                x -= 1

    print Token
    return (x)

archivo = open("texto", "r")
x=0
MAX=len("int vector, su&mas, res@tas,suma1,suma2,25ert;")
#while x<MAX:
 #   x=iden_lex("int vector, su&mas, res@tas,suma1,suma2,25ert;",x)

var=get_character(archivo)
while(var!="EOF"):
    print var
    var = get_character(archivo)




especiales=["{", "}","(",")",";",":","&",","]
operadores=["*","%"]
reservadas=["main","if","then","else","end","do","while","repeat","until","cin","cout","real","int", "boolean"]
ignorar=['\n','\t'," "]
ncol=0
nfil=0
max=0
linea_actual=""
Token_externo = {
    "tipo": "",
    "lexema": ""
}
estado="START"

def get_character(linea):
    global ncol, nfil, estado, linea_actual, max
    if (ncol==0 or ncol==max):
        linea_actual=linea.readline()
        if linea_actual != "":
            ncol=0
            nfil+=1
            max=len(linea_actual)
        else:
            estado="END"
            return "EOF"

    c=linea_actual[ncol]
    ncol+=1
    return c

def iden_lex(linea):
    global ncol, estado
    Token = {
        "tipo": "",
        "lexema": ""
    }
    c=get_character(linea)
    estado = "START"
    while(estado!="END"):
        if estado == "START":
            if c=="EOF":
                estado="END"
                Token["tipo"]="EOF"
            elif c.isalpha():
                estado="IDEN"
                Token["lexema"]+=c
                c=get_character(linea)
            elif c=="/":
                estado="SLASH"
                Token["lexema"] += c
                c=get_character(linea)
            elif c=="+":
                estado="ADD"
                Token["lexema"] += c
                c=get_character(linea)
            elif c=="-":
                estado="MINUS"
                Token["lexema"] += c
                c=get_character(linea)
            elif c=="=":
                estado="EQ"
                Token["lexema"] += c
                c=get_character(linea)
            elif c=="<":
                estado="LT"
                Token["lexema"] += c
                c=get_character(linea)
            elif c==">":
                estado="HT"
                Token["lexema"] += c
                c=get_character(linea)
            elif c==":":
                estado="ASSIGN"
                Token["lexema"] += c
                c=get_character(linea)
            elif c=="!":
                estado="NEQ"
                Token["lexema"] += c
                c=get_character(linea)
            elif c.isdigit():
                estado="ENTERO"
                Token["lexema"] += c
                c=get_character(linea)
            elif ignorar.__contains__(c):
               c=get_character(linea)
            else:
                estado = "END"
                Token["lexema"] += c
                if especiales.__contains__(c):
                    Token["tipo"]="SIMBOLO"
                elif operadores.__contains__(c):
                    Token["tipo"]="OPERADOR"
                else:
                    Token["tipo"] = "ERROR"

        elif estado=="IDEN":
            Token["tipo"] = "IDENTIFICADOR"
            if (c.isalpha() or c.isdigit() or c=="_"):
                Token["lexema"] += c
                c=get_character(linea)
            else:
                ncol -=1
                estado="END"
        elif estado == "SLASH":
            if c=="/":
                Token["lexema"] =""
                c=get_character(linea)
                while c!='\n':
                    c=get_character(linea)
                estado="START"
            elif c=="*":
                Token["lexema"] = ""
                c=get_character(linea)
                hecho=False
                while hecho==False:
                    while (c!="*"):
                        c=get_character(linea)
                    while (c=="*"):
                        c=get_character(linea)
                    if(c=="/"):
                        hecho=True
                        c = get_character(linea)
                estado="START"
            else:
                Token["tipo"]="OPERADOR"
                estado="END"
                ncol-=1
        elif estado == "ADD":
            if(c=="+"):
                Token["tipo"]="OPERADOR"
                Token["lexema"]+=c
                estado="END"
                #c=get_character(linea)
            elif c.isdigit():
                estado="ENTERO"
                Token["lexema"] += c
                c=get_character(linea)
            else:
                Token["tipo"] = "OPERADOR"
                estado="END"
                ncol -=1
        elif estado == "MINUS":
            if (c == "-"):
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += c
                estado = "END"
            elif c.isdigit():
                estado = "ENTERO"
                Token["lexema"] += c
                c=get_character(linea)
            else:
                estado = "END"
                Token["tipo"] = "OPERADOR"
                ncol -=1
        elif estado=="ENTERO":
            while(c.isdigit() ):
                Token["lexema"] += c
                c=get_character(linea)
            if c==".":
                Token["lexema"] += c
                c=get_character(linea)
                if c.isdigit():
                    Token["lexema"] += c
                    c=get_character(linea)
                    while c.isdigit():
                        Token["lexema"] += c
                        c=get_character(linea)
                    estado="END"
                    Token["tipo"] = "REAL"
                    ncol -=1
                else:
                    estado="END"
                    Token["tipo"] = "ERROR"
                    c=get_character(linea)
            else:
                estado="END"
                Token["tipo"] = "ENTERO"
                ncol -=1

        elif estado=="EQ":
            Token["tipo"] = "OPERADOR"
            if c=="=":
                Token["lexema"] += c
                estado = "END"
            else:
                estado = "END"
                ncol -=1
        elif estado=="LT":
            Token["tipo"] = "OPERADOR"
            if c=="=":
                Token["lexema"] += c
                estado = "END"
            else:
                estado = "END"
                ncol -=1
        elif estado=="HT":
            Token["tipo"] = "OPERADOR"
            if c=="=":
                Token["lexema"] += c
                estado = "END"
            else:
                estado = "END"
                ncol -=1
        elif estado=="ASSIGN":
            if c=="=":
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += c
                estado = "END"
            else:
                estado = "END"
                ncol -=1
        elif estado=="NEQ":
            if c=="=":
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += c
                estado = "END"
            else:
                estado = "END"
                ncol -=1

    if reservadas.__contains__(Token["lexema"]):
        Token["tipo"]="RESERVADAS"
    return (Token)

archivo = open("texto", "r")
Token_externo=iden_lex(archivo)
while(Token_externo["tipo"]!="EOF"):
    print Token_externo
    if Token_externo["tipo"]=="ERROR":
        MANDAMOS AL ARCHIVO DE ERROR
    else:
        MANDAMOS AL ARCHIVO LEXEMAS
    Token_externo = iden_lex(archivo)
archivo.close()
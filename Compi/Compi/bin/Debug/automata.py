import os
import sys
especiales=["{", "}","(",")",";",":",","]
operadores=["*","%"]
reservadas=["main","if","then","else","end","do","while","repeat","until","cin","cout","real","int", "boolean"]
ignorar=['\n','\t'," ",'\xef','\xbb','\xbf']
ncol=0
nfil=0
max=0
max_viejo=0
linea_actual=""
Token_externo = {
    "tipo": "",
    "lexema": ""
}
estado="START"

def get_character(linea):
    global ncol, nfil, estado, linea_actual, max, max_viejo
    if (ncol==0 or ncol==max):
        linea_actual=linea.readline()
        if linea_actual != "":
            ncol=0
            nfil+=1
            max_viejo=max
            max=len(linea_actual)
        else:
            estado="END"
            return "EOF"

    c=linea_actual[ncol]
    ncol+=1
    return c

def unget_character(linea):
    global ncol, nfil, estado, linea_actual, max, max_viejo
    if (ncol==0):
        ncol=max_viejo
        nfil-=1
        return max_viejo
    else:
        regresar=ncol - 1
        ncol-=1
        return regresar

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
                unget_character(linea)
                estado="END"
        elif estado == "SLASH":
            if c=="/":
                Token["lexema"] =""
                c=get_character(linea)
                while (c!='\n' and c!="EOF"):
                    c=get_character(linea)
                estado = "START"
                if c=="EOF":
                    estado = "END"
                    Token["tipo"] = "EOF"

            elif c=="*":
                Token["lexema"] = ""
                c=get_character(linea)
                hecho=False
                while hecho==False and c!="EOF":
                    while (c!="*" and c!="EOF"):
                        c=get_character(linea)
                    while (c=="*"):
                        c=get_character(linea)
                    if(c=="/"):
                        hecho=True
                        c = get_character(linea)
                estado="START"
                if (c == "EOF"):
                    estado = "END"
                    Token["tipo"] = "EOF"
            else:
                Token["tipo"]="OPERADOR"
                estado="END"
                unget_character(linea)
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
                unget_character(linea)
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
                unget_character(linea)
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
                    unget_character(linea)
                else:
                    estado="END"
                    Token["tipo"] = "ERROR"
                    unget_character(linea)
                    #c=get_character(linea)
            else:
                estado="END"
                Token["tipo"] = "ENTERO"
                unget_character(linea)

        elif estado=="EQ":
            if c=="=":
                Token["lexema"] += c
                Token["tipo"] = "OPERADOR"
                estado = "END"
            else:
                estado = "END"
                Token["tipo"] = "ERROR"
                unget_character(linea)
        elif estado=="LT":
            Token["tipo"] = "OPERADOR"
            if c=="=":
                Token["lexema"] += c
                estado = "END"
            else:
                estado = "END"
                unget_character(linea)
        elif estado=="HT":
            Token["tipo"] = "OPERADOR"
            if c=="=":
                Token["lexema"] += c
                estado = "END"
            else:
                estado = "END"
                unget_character(linea)
        elif estado=="ASSIGN":
            if c=="=":
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += c
                estado = "END"
            else:
                estado = "END"
                Token["tipo"] = "ERROR"
                unget_character(linea)
        elif estado=="NEQ":
            if c=="=":
                Token["tipo"] = "OPERADOR"
                Token["lexema"] += c
                estado = "END"
            else:
                estado = "END"
                unget_character(linea)

    if reservadas.__contains__(Token["lexema"]):
        Token["tipo"]="RESERVADAS"
    return (Token)

archivo = open("falla.mcp", "r")



#archivo= open(sys.argv[1],"r")


error =archivo.name.replace("mcp","err")
if os.path.exists(error):
    os.remove(error)
    archivoErr = open(error,"w+")
else:
    archivoErr = open(error, "w+")
final = archivo.name.replace("mcp", "fin")
if os.path.exists(final):
    os.remove(final)
    final = open(final, "w+")
else:
    final = open(final, "w+")

Token_externo=iden_lex(archivo)
while(Token_externo["tipo"]!="EOF"):
    print Token_externo
    if Token_externo["tipo"]=="ERROR":
        
        archivoErr.write(Token_externo["lexema"])
        archivoErr.write("\t")
        archivoErr.write(Token_externo["tipo"])
        archivoErr.write("\t Fila:%d" % nfil)
        archivoErr.write(" Columna:%d" % ncol)
        archivoErr.write("\n")

    elif Token_externo["tipo"]!="":
         final.write(Token_externo["lexema"])
         final.write("\t")
         final.write(Token_externo["tipo"])
       
         final.write("\n")

    Token_externo = iden_lex(archivo)
archivo.close()

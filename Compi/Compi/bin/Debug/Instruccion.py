from os import sys
from Nemonico import Nemonico


# Clase para guardar las instrucciones
class Instruccion:
    '''	Constructor recibe
    linea por linea del generador de codigo y obtiene los argumentos
    linea por default es None	'''

    def __init__(self, linea=None):
        # NOTA: iop, arg1,arg2 y arg3 son siempre strings
        # EL nemonico por default es HALT = fin de ejecución, se rectifica mas adelante
        self.iop = Nemonico.HALT
        self.arg1 = None
        self.arg2 = None
        self.arg3 = None

        if linea != None:
            # Separar en partes la instruccion
            # en posicion [0] = numero de la linea y [1] =resto del comando
            # es numero de linea o numero de memoria??????
            contenidoLinea = linea.split(":")

            # Guardar el numero de la linea
            # como atributo de este objeto

            # Este atributo si es entero para formar las llaves
            # strip remueve los vacios al inicio y final del codigo
            self.lineNo = int(contenidoLinea[0].strip())

            # Guardar en otra variable el resto de la instruccion
            restInst = contenidoLinea[1].strip()

            # Separar el resto por sus 2 espacios: [0] = nemonico y [1] = parametros

            # IMPORTANTE: entre el nemonico y sus parametros debe haber 2 espacios siempre
            ParteInst = restInst.split("  ")

            nemonico = ParteInst[0]
            params = ParteInst[1]
            # Verificar que el nemonico esté en la lista
            if not nemonico in Nemonico.Lista_nemonicos:
                print("Error en el nemonico: <" + nemonico + "> linea:" + self.lineNo, file=sys.stderr)
                exit(1)
            else:
                self.iop = nemonico

            self.isRMorRA = ("(" in params) and (")" in params)
            self.isRR = not self.isRMorRA

            # Si es RA sacar los parametros xq hay un parentesis
            if self.isRMorRA:
                SepararXComa = params.split(",")

                self.arg1 = int(SepararXComa[0].strip())
                parentesis = SepararXComa[1]
                separarXPar = parentesis.split("(")

                self.arg2 = int(separarXPar[0].strip())

                self.arg3 = int(separarXPar[1].split(")")[0].strip())

            else:  # Es RM
                SepararXComa = params.split(",")
                self.arg1 = int(SepararXComa[0].strip())
                self.arg2 = int(SepararXComa[1].strip())
                self.arg3 = int(SepararXComa[2].strip())

    def __str__(self):
        return str(self.lineNo) + ": " + str(self.iop) + " " + str(self.arg1) + " - " + str(self.arg2) + " - " + str(
            self.arg3)

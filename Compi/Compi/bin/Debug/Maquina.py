from os import sys
from enum import Enum
from Nemonico import *
from Instruccion import *

# filehandler2 = open('C:\\Users\\Edgardo\\Documents\\Visual Studio 2017\\Projects\\Mandarina Studio\\Mandarina Studio\\hash.obj', 'rb') #abre el .obj que contiene el bytecode de la tabla de simbolos
# d = pickle.load(filehandler2) #deserializa el .obj
d = dict()
cve = ""
es_entero = False

# Constantes globales:
IADDR_SIZE = 1024
DADDR_SIZE = 1024
NO_REGS = 8
PC_REG = 7


class STEPRESULT(Enum):
    OKAY = 1
    HALT = 2
    IMEM_ERR = 3
    DMEM_ERR = 4
    ZERODIVIDE = 5
    INCOM_ERR = 6
    ERROROP = 7


class Maquina:
    def __init__(self, arch, tabla):
        # Guardar archivo de programa que trae los codigos intermedios
        self.arch = arch
        # Definicion de memoria
        self.dMem = []
        # Definicion de los registros
        self.reg = []
        # Instrucciones de memoria (diccionario)
        self.iMem = dict()
        # Tabla hash
        self.tabla = tabla
        self.getTabla()
        self.inicializar()

    def getTabla(self):
        archivoTabla = open(self.tabla, "r")

        lineas = [line.rstrip('\n') for line in archivoTabla]
        for x in lineas:
            temp = x.split("|")
            d[temp[0]] = [temp[1], temp[2]]

        archivoTabla.close()


    def inicializar(self):
        # init memoria en 0
        self.dMem = [0 for x in range(0, DADDR_SIZE)]
        self.dMem[0] = DADDR_SIZE - 1

        # init registros en 0
        self.reg = [0 for x in range(0, NO_REGS)]

        # obtener cada instruccion con los nemonicos del archivo con el codigo intermedios
        # descomopone la instruccion en diccionarios individuales que contienen
        # nemonico y argumentos dependiendo de si son instrucciones RO o RM
        # guarda en un registro de la "memoria" la instruccion
        for line in self.arch:
            instruction = Instruccion(line)
            self.iMem[instruction.lineNo] = instruction

            # Metodo para comenzar la ejecucion de las instrucciones


    def correr(self):
        stepResult = STEPRESULT.OKAY
        while (stepResult == STEPRESULT.OKAY):
            stepResult = self.ejecutar()

    def getKey2(self, k):
        global cve
        # por cada variable en la tabla hash

        for tupla in d:
            # comparar que la locacion de memoria sea igual a k
            if int(d[tupla][1]) == k:
                cve = tupla


    def ejecutar(self):
        global d
        global cve
        global es_entero
        pc = self.reg[PC_REG]
        self.reg[PC_REG] = pc + 1
        currentinstruction = self.iMem[pc]
        if currentinstruction.isRR:
            r = currentinstruction.arg1
            s = currentinstruction.arg2
            t = currentinstruction.arg3
        else:  # isRMorRA
            r = currentinstruction.arg1
            s = currentinstruction.arg3
            k = currentinstruction.arg2
            m = currentinstruction.arg2 + self.reg[s]
            # print(r," ",s," ",m)
        # Evaluar cada nemonico
        if currentinstruction.iop == Nemonico.HALT:
            print("HALT: " + str(r) + "," + str(s) + "," + str(t))
            return STEPRESULT.HALT
        elif currentinstruction.iop == Nemonico.IN:
            num = input("-> ")
            try:
                float(num)
                self.reg[r] = num
                '''if d[cve].tipo=="int" and "." in str(num):
                        print("error-> float a int no valido\n")
                        return STEPRESULT.INCOM_ERR
                if d[cve].tipo=="boolean":
                        if str(num)!="0" and str(num)!="1":
                                print("error-> boolean solom acepta 0 o 1\n")
                                return STEPRESULT.INCOM_ERR
                if d[cve].tipo=="int" or  d[cve].tipo=="boolean":
                        self.reg[r]=int(num)
    
                else:
                        self.reg[r]=float(num) '''
            except ValueError:
                print("Error, tipo incompatible", file=sys.stderr)
                return STEPRESULT.INCOM_ERR
        elif currentinstruction.iop == Nemonico.OUT:
            print("<- " + str(self.reg[r]), end='')
        elif currentinstruction.iop == Nemonico.ADD:
            self.reg[r] = self.reg[s] + self.reg[t]
        elif currentinstruction.iop == Nemonico.SUB:
            self.reg[r] = self.reg[s] - self.reg[t]
        elif currentinstruction.iop == Nemonico.MUL:
            self.reg[r] = self.reg[s] * self.reg[t]
        elif currentinstruction.iop == Nemonico.DIV:
            if self.reg[t] != 0:
                if not "." in str(self.reg[s]) and not "." in str(self.reg[t]):
                    es_entero = True
                self.reg[r] = self.reg[s] / self.reg[t]
            else:
                return STEPRESULT.ZERODIVIDE
        elif currentinstruction.iop == Nemonico.LD:
            self.reg[r] = self.dMem[m]
        elif currentinstruction.iop == Nemonico.ST:
            # print(str(s))
            if str(s) == '5':
                self.getKey2(k)

                # print(k," ",d[cve].nombre," ",d[cve].tipo)
                if es_entero and d[cve][0] == "int":
                    # print("op1")
                    self.dMem[m] = int(self.reg[r])
                    es_entero = False
                elif es_entero and d[cve][0] == "real":
                    # print("op2")
                    self.dMem[m] = float(self.reg[r])
                    es_entero = False
                elif d[cve][0] == "int":
                    if "." in str(self.reg[r]):
                        print("Error de asigancion! 1")
                        return STEPRESULT.ERROROP
                    else:
                        self.dMem[m] = int(self.reg[r])
                elif d[cve][0] == "boolean":
                    if str(self.reg[r]) != "0" and str(self.reg[r]) != "1":
                        print("Error de asigancion! 2")
                        return STEPRESULT.ERROROP
                    else:
                        self.dMem[m] = int(self.reg[r])
                else:
                    self.dMem[m] = float(self.reg[r])
            else:
                if "." in str(self.reg[r]):
                    self.dMem[m] = float(self.reg[r])
                else:
                    self.dMem[m] = int(self.reg[r])
        elif currentinstruction.iop == Nemonico.LDA:
            self.reg[r] = m
        elif currentinstruction.iop == Nemonico.LDC:
            self.reg[r] = currentinstruction.arg2
        elif currentinstruction.iop == Nemonico.JLT:
            if self.reg[r] < 0:
                self.reg[PC_REG] = m
        elif currentinstruction.iop == Nemonico.JLE:
            if self.reg[r] <= 0:
                self.reg[PC_REG] = m
        elif currentinstruction.iop == Nemonico.JGT:
            if self.reg[r] > 0:
                self.reg[PC_REG] = m
        elif currentinstruction.iop == Nemonico.JGE:
            if self.reg[r] >= 0:
                self.reg[PC_REG] = m
        elif currentinstruction.iop == Nemonico.JEQ:
            if self.reg[r] == 0:
                self.reg[PC_REG] = m
        elif currentinstruction.iop == Nemonico.JNE:
            if self.reg[r] != 0:
                self.reg[PC_REG] = m
        return STEPRESULT.OKAY

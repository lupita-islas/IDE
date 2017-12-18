import sys
from Maquina import *
archivoMaquina = sys.argv[1]
archivoTabla = sys.argv[2]

maquinita501 = Maquina(archivoMaquina,archivoTabla)
maquinita501.correr()
#based on: http://paulmouzas.github.io/2014/12/31/implementing-a-hash-table.html
import os
class HashMap(object):
    #Crea la tabla hash de un tamano de 256
    nombreError=""

    def __init__(self):
        self.hashmap = [[] for i in range(256)]

    def insert(self, key, ty, memory, line, value):
        #Crea la llave hash
        hash_key = hash(key) % len(self.hashmap)
        key_exists = False
        #Guarda el contenido de esa localidad de la tabla hash
        bucket = self.hashmap[hash_key]
        # Ciclo donde itera en lo contenido
        for i, ntmlv in enumerate(bucket):
            n, t, m, l, v = ntmlv
            if key == n:
                key_exists = True
                break
        #si ya existe solo se le agrega la linea donde se encontro
        if key_exists:
            bucket[i][3].append(line)
            #bucket[i][4]=value
            #bucket[i] = ((key, type, memory, line, value))
        #si no existe el valor lo agrega de forma normal
        else:
            bucket.append([key, ty, memory, [line], value])

    def retrieve(self, key):
        hash_key = hash(key) % len(self.hashmap)
        bucket = self.hashmap[hash_key]
        for i, ntmlv in enumerate(bucket):
            n, t, m, l, v = ntmlv
            return v
        return 0

    def errorDec(self,nombre):
        global nombreError
        nombreError=nombre

        if os.path.exists(nombreError):
            os.remove(nombreError)
        archivoError = open(nombreError, "w+")

        for bucket in self.hashmap:
            for i, ntmlv in enumerate(bucket):
                n, t, m, l, v = ntmlv
                if t=='':
                    archivoError.write("Variable '"+str(n)+"' no declarada en "+l[0]+"\n")

        archivoError.close()

    def imprimirTabla(self):
        nombreTabla="ejemplo.table"
        if os.path.exists(nombreTabla):
            os.remove(nombreTabla)
        
        archivo= open(nombreTabla,"w+")
        print ("Nombre  Tipo    LocMem  Valor   Lineas")
        for bucket in self.hashmap:
            for i, ntmlv in enumerate(bucket):
                 n, t, m, l, v = ntmlv
                 print (n,t,m,v,l)
                 lineaPritn =str(n)+"|"+str(t)+"|"+str(m)+"|"+str(v)+"|"+str(l)+"\n"
                 archivo.write(lineaPritn)
        archivo.close()

    def instValTable(self,nombre, valor,memory,line):
        #Crea la llave hash
        hash_key = hash(nombre) % len(self.hashmap)
        key_exists = False
        ty=""
        #Guarda el contenido de esa localidad de la tabla hash
        bucket = self.hashmap[hash_key]
        # Ciclo donde itera en lo contenido
        for i, ntmlv in enumerate(bucket):
            n, t, m, l, v = ntmlv
            ty=t
            if nombre == n:
                #line=l
                key_exists = True
                break
        #si ya existe solo se le agrega la linea donde se encontro
        if key_exists:
            if(isinstance(valor,str) ):
                if(ty=="real" and  ("." not in valor)):
                    bucket[i][4]=float(valor)
                else:    
                    bucket[i][4]=valor
                #if(ty=="int" and ("." in valor) and ("true"  in valor or "false"  in valor)) or (ty=="real" and  ("true"  in valor or "false"  in valor)) or (ty=="boolean" and ("true" not in valor or "false" not in valor) ):
                if(ty=="int" and "." in valor ):
                    self.errorTipo(ty,line,nombre)
                
            else:
                if(ty=="real" and isinstance(valor,int)):
                    bucket[i][4]=float(valor)
                else:    
                    bucket[i][4]=valor
                if(ty=="int" and not isinstance(valor,int)) or (ty=="real" and not isinstance(valor,float) and not isinstance(valor,int)) or (ty=="boolean" and ("true" not in valor or "false" not in valor)):
                    self.errorTipo(ty,line,nombre)       
            #bucket[i] = ((key, type, memory, line, value))
        #si no existe el valor lo agrega de forma normal
        else:
            bucket.append([nombre, ty, memory, [line], valor])

    def errorTipo(self,tipo,linea,variable):
        global nombreError
        archivoError= open(nombreError,"a")
        archivoError.write("No coincide el tipo "+tipo+" variable "+variable+" en linea: "+str(linea)+"\n")
        archivoError.close()


#tabla hash debe contener
#nombre, tipo, localidad memoria, num linea (lista), valor
#controlar colisiones ???

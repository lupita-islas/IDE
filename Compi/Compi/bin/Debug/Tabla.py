#based on: http://paulmouzas.github.io/2014/12/31/implementing-a-hash-table.html
import os
class HashMap(object):
    #Crea la tabla hash de un tamano de 256
    nombreError=""

    def __init__(self):
        self.hashmap = [[] for i in range(256)]

    def abrir(self,nombre):
        global nombreError
        nombreError=nombre

    #funcion que inserta en la tabla hash, recibe como parametros el nombre de la variable (key), el tipo, espacio de memoria, linea y valor
    def insert(self, key, ty, memory, line, value,padre):
        #Crea la llave hash
        hash_key = hash(key) % len(self.hashmap)
        key_exists = False
        #Guarda el contenido de esa localidad de la tabla hash
        bucket = self.hashmap[hash_key]
        # Ciclo donde itera en lo contenido
        for i, ntmlv in enumerate(bucket):
            n, t, m, l, v = ntmlv
            if key == n:
                lineno=l
                type=t
                key_exists = True
                break
        #si ya existe solo se le agrega la linea donde se encontro
        if key_exists:
            if ((padre=="ListVar" and lineno.__contains__(line) ) or (padre=="ListVar" and type!=ty)):
                archivoError= open(nombreError,"a")
                archivoError.write("Variable "+key+" doblemente declarada en linea: "+str(line)+"\n")
                archivoError.close()
            bucket[i][3].append(line)
            #if lineno==l:
             #   self.errorTipo(ty,line,key)
            #bucket[i][4]=value
            #bucket[i] = ((key, type, memory, line, value))
        #si no existe el valor lo agrega de forma normal
        else:
            bucket.append([key, ty, memory, [line], value])

    #Funcion que regresa el valor de una variable en la tabla hash, recibe de parametro la variable (key)
    #Utilizada al momento de hacer el paso de valores para obtener el valor previo de la variable
    def retrieve(self, key):
        hash_key = hash(key) % len(self.hashmap)
        bucket = self.hashmap[hash_key]
        for i, ntmlv in enumerate(bucket):
            n, t, m, l, v = ntmlv
            return v
        return 0

    def retrieveT(self, key):
        hash_key = hash(key) % len(self.hashmap)
        bucket = self.hashmap[hash_key]
        for i, ntmlv in enumerate(bucket):
            n, t, m, l, v = ntmlv
            return t
        return 0

    def retrieveM(self, key):
        hash_key = hash(key) % len(self.hashmap)
        bucket = self.hashmap[hash_key]
        for i, ntmlv in enumerate(bucket):
            n, t, m, l, v = ntmlv
            return m
        return 0

    #Itera en la tabla hash para detectar las variables que no fueron declaradas y que se encontraron despues en el codigo
    #Para esto verifica cuales estan vacias es el atributo de tipo
    def errorDec(self,nombre):
        global nombreError
        archivoError= open(nombreError,"a")

        for bucket in self.hashmap:
            for i, ntmlv in enumerate(bucket):
                n, t, m, l, v = ntmlv
                if t=='':
                    archivoError.write("Variable '"+str(n)+"' no declarada en "+l[0]+"\n")

        archivoError.close()

    #Itera por la tabla hash para mostrar su contenido
    def imprimirTabla(self,file):
        nombreTabla=file
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

    #Función utilizada cuando se hace el paso de valores
    #Recibe el ID e identifica si ya existe, si ya existe solo le va a agregar el nuevo valor pero debe verificar
    #que el nuevo valor conincida con el tipo que debe recibir
    def instValTable(self,nombre, valor,memory,line):
        global nombreError
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
                if(ty=="int" and not isinstance(valor,int)) or (ty=="real" and not isinstance(valor,float) and not isinstance(valor,int)) or (ty=="boolean" and (1 not in valor or 2 not in valor)):
                #if(ty=="int" and not isinstance(valor,int)) or (ty=="real" and not isinstance(valor,float) and not isinstance(valor,int)) or (ty=="boolean" and ("true" not in valor or "false" not in valor)):
                    self.errorTipo(ty,line,nombre)       
            #bucket[i] = ((key, type, memory, line, value))
        #si no existe el valor lo agrega de forma normal
        else:
            bucket.append([nombre, ty, memory, [line], valor])
            archivoError= open(nombreError,"a")
            archivoError.write("No coincide el tipo "+ty+" variable "+nombre+" en linea: "+str(line)+"\n")
            archivoError.close()

    def errorTipo(self,tipo,linea,variable):
        global nombreError
        archivoError= open(nombreError,"a")
        archivoError.write("No coincide el tipo "+tipo+" variable "+variable+" en linea: "+str(linea)+"\n")
        archivoError.close()


#tabla hash debe contener
#nombre, tipo, localidad memoria, num linea (lista), valor
#controlar colisiones ???

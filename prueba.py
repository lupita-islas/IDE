from anytree  import *
tiposPermitidos=["Tipo","ListVar","ID"]
Padre = Node("Padre",tipo="OP",value="",nombre="-")
hijo1=Node("Hijo1",parent=Padre,type="int", tipo="ENTERO",value=3,nombre="3")
hijo2=Node("Hijo2",parent=Padre,tipo="ENTERO",value=1,nombre="1")


#for node in PostOrderIter(Padre):#Lista variable,Identificador
#    if(tiposPermitidos.__contains__(node.tipo)):
#        if(node.siblings!=None):
#            node.siblings[0].type=node.type
        
def recorridoPosValor (mainNode):
    permitidos=["ID","ASSIGN","EXP","EXPSIMP","TERM","FACT","REAL","ENTERO"]
    
    for node in PostOrderIter(mainNode):
        
        if(permitidos.__contains__(node.tipo) and node.siblings and band):
        
            if(node.parent.nombre=='+'):
                node.parent.value=node.value+node.siblings[0].value
            elif (node.parent.nombre=='*'):
                node.parent.value=node.value*node.siblings[0].value 
            elif(node.parent.nombre=='/'):
                node.parent.value=node.value/node.siblings[0].value      
            elif(node.parent.nombre=='-'):
                node.parent.value=node.value-node.siblings[0].value     
        #node.parent.value=node.value

    print(RenderTree(mainNode,style=AbstractStyle("","","")))        

recorridoPosValor(Padre)
  
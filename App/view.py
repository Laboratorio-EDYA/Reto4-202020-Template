"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
from DISClib.ADT import map as m
assert config
from time import process_time
from DISClib.DataStructures import listiterator as it

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________




tripfile = '201801-1-citibike-tripdata.csv'
#tripfile = '201801-4-citibike-tripdata.csv'


initialStation = None
recursionLimit = 30000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("-"*75)
    print("Bienvenido")
    print("1- Inicializar analizador y Carga archivo CSV")
    print("2- Cantidad de Clusters de viajes")
    print("3- Ruta turística Circular")
    print("4- Estaciones críticas")
    print("5- Ruta turística por resistencia")
    print("6- Recomendador de rutas")
    print("7- Ruta de interés turístico")
    print('8- Indentificación de estaciones para publicidad')
    print('9- Identificacion de bicicletas para mantenimiento')
    print("0- Salir")
    print("-"*75)


def cargaDatos(cont):
    print("\nCargando información de CitiBike ....")
    controller.loadFile(cont, tripfile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStation(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    controller.cantidadClusters(cont, '0','0')
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))
    # controller.cantidadClusters(cont, '','')

def cantidadClusters(cont): #REQ 1
    estacion1= input('Dijite la primera estación: ')
    estacion2 = input('Dijite la segunda estación: ')
    data  = controller.cantidadClusters(cont, estacion1, estacion2)
    if data == -1:
        print('No existe alguna de las estaciones','-'*75)
    else:
        print('Hay ',data[0]['size'], ' clusters dentro del gráfo')
        if data[1] == True:
            print('La estacion ',estacion1, ' y la estacion ',estacion2, ' están en el mismo clúster')
        else:
            print('La estacion ',estacion1, ' y la estacion ',estacion2, ' no están en el mismo clúster')

def rutaTuristicaCircular(cont): #REQ 2
    print('Use estos nodos segun el archivo cargado (sugerencia) --> 1: 119,2: 195: ,3: 440,4: 3654')
    inicio = input('Dijite el inicio del rango en minutos: ')
    final = input('Dijite el final del rango en minutos: ')
    estacion = input('Digite el identificador de la estación de inicio: ')
    data = controller.rutaTuristicaCircular(cont, (inicio,final), estacion)
    if data == -1:
        print('No se halló ningun resultado','-'*75)
    else:
        if data != -1 and data[0] != 0:
            print('Se hallaron', data[0],' rutas posibles: ')
            for i in range(1,len(data)):
                string = []
                reves = []
                iterator = it.newIterator(data[i][0])
                while it.hasNext(iterator):
                    current = it.next(iterator)
                    string.append('vertice '+current['vertexA']+' -> vertice '+current['vertexB'])
                    reves.insert(0,'vertice '+current['vertexB']+' -> vertice '+current['vertexA'])
                string = ", ".join(string)
                reves = ", ".join(reves)
                print('Ruta número ',i,' de duración', data[i][1],'minutos: ', string,' -> ', reves)
        elif data == -1:
            print('No existe la estación','-'*75)
        elif data[0] == 0:
            print('No hay rutas','-'*75) 

def optionFive(cont): #REQ 3
    data = controller.estacionesCriticas(cont)
    print('TOP 1: Los vertices a los que más llegan ciclas: ')
    print('1. ',data['top1'][0][0],' con ',data['top1'][0][1],' ciclas')
    print('2. ',data['top1'][1][0],' con ',data['top1'][1][1],' ciclas')
    print('3. ',data['top1'][2][0],' con ',data['top1'][2][1],' ciclas')
    print('TOP 2: Los vertices de los que más salen ciclas: ')
    print('1. ',data['top2'][0][0],' con ',data['top2'][0][1],' ciclas')
    print('2. ',data['top2'][1][0],' con ',data['top2'][1][1],' ciclas')
    print('3. ',data['top2'][2][0],' con ',data['top2'][2][1],' ciclas')
    print('TOP 3: Los vertices menos visitados: ')
    print('1. ',data['top3'][0][0],' con ',data['top3'][0][1],' ciclas')
    print('2. ',data['top3'][1][0],' con ',data['top3'][1][1],' ciclas')
    print('3. ',data['top3'][2][0],' con ',data['top3'][2][1],' ciclas')
        
def rutaTuristicaResistencia(cont):   #REQ. 4
    time = int(input('Digita el tiempo límite (minutos): '))
    idstation = int(input('Digita la estación de inicio: '))
    data = controller.rutaTuristicaResistencia(cont, time, idstation)
    print('En el tiempo limite de ', time, ' minutos, se encontraron los siguientes recorridos: ')
    for each_trip in data:
        fin = each_trip
        peso = data[each_trip]
        print(str(idstation) + ' ---> ' + str(fin) + ' _______ Tiempo: ' , peso , 'minutos')

def recomendadorRutas(cont):   # REQ. 5
    edad = int(input('Digita la edad: '))
    data = controller.recomendadorRutas(cont, edad)
    if data[0] != '-1':
        print('-> La estación en la que más inician viajes las personas del rango de ',edad,' años es la número: ',data[0])
        print('-> Desde la estación ',data[0], ', la mayoría de las personas terminan en la estación ',data[1])
        if len(data[2]) == 1:
            print('-> Existe una ruta directa entre la estación ',data[0],' y la estación ',data[1],'\n')
        else:
            print('-> Iniciando desde la estación ',data[0],' para llegar a la estación',data[1],' se deben pasar por la estaciones: ')
            for each_vertex in data[2]:
                print(str(each_vertex))
    else: 
        print('No se encontraron datos en el rango de ' , edad, ' años')
        

def optionSeven(cont):
    if cont ==None:
        print('Digite bien el archivo')
    else:
        latlocal=input('Digite la latitud actual')
        longlocal=input('Digite la longotud local')
        latfinal=input('digite la latitud del sitio turístico')
        longfinal=input('Digite la longitud del sitio turístico')
        data=controller.rutaInteresTuristico(cont,latlocal,longlocal,latfinal,longfinal)
        print('La estación más cercana a usted es: ', data[0])
        print('La estación más cercana a su sitio de interés es: ', data[1])
        print('La duración de su viaje es de: ', data[2])
        lista=data[3]
        iterator=it.newIterator(lista)
        print('Las estaciones que encontrará en su viaje son:')
        while it.hasNext(iterator):
            print(it.next(iterator))
def optionEight(cont):
    if cont == None:
        print('Digite bien el archivo')
    else:
 
        print('1: 0-10')
        print('2: 11-20')
        print('3: 21-30')
        print('4: 31-40')
        print('5: 41-50')
        print('6: 51-60')
        print('7: 60+')
        rango=input('Digite el rango:')
        if rango=='1':
            res=controller.estacionesPublicidad(cont,10)
            print('Las estaciones más usadas por este rango de edad es:')
            for i in res:
                print(i)
        elif rango=='2':
            res=controller.estacionesPublicidad(cont,20)
            print('Las estaciones más usadas por este rango de edad es:')
            for i in res:
                print(i)
        elif rango=='3':
            res=controller.estacionesPublicidad(cont,30)
            print('Las estaciones más usadas por este rango de edad es:')
            for i in res:
                print(i)
        elif rango=='4':
            res=controller.estacionesPublicidad(cont,40)
            print('Las estaciones más usadas por este rango de edad es:')
            for i in res:
                print(i)
        elif rango=='5':
            res=controller.estacionesPublicidad(cont,50)
            """Las estaciones más usadas por este rango de edad es:"""
            for i in res:
                print(i)
        elif rango=='6':
            res=controller.estacionesPublicidad(cont,60)
            print('Las estaciones más usadas por este rango de edad es:')
            for i in res:
                print(i)
        elif rango=='7':
            res=controller.estacionesPublicidad(cont,100)
            print('Las estaciones más usadas por este rango de edad es:')
            for i in res:
                print(i)
            
        else:
            print('Digitó mal')
"""

#def optionSix():
    

#def optionSeven():
    
"""


def main():
    cont = None
    while True:
        printMenu()
        inputs = int(input('Seleccione una opción para continuar\n-> '))

        if inputs == 1:   #Inicio y carga
            t1_start = process_time() #tiempo inicial
            print("\nInicializando.....")
            tamaño = int(input("Digita el tamaño de las tablas de hash: "))
            carga = float(input("Digita el factor de carga: "))
            cont = controller.init(tamaño, carga)
            cargaDatos(cont)
            t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")

        elif inputs == 2:   #Req. 1
            print("\nCantidad de Clusters de viajes")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                t1_start = process_time() #tiempo inicial
                cantidadClusters(cont)
                t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")

        elif inputs == 3:   #Req. 2
            print("\nRuta turística Circular")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                t1_start = process_time() #tiempo inicial
                rutaTuristicaCircular(cont)
                t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")
        
        elif inputs == 4:   #Req. 3
            print("\nEstaciones críticas")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                t1_start = process_time() #tiempo inicial
                optionFive(cont)
                t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")
        
        
        elif inputs == 5:   #Req. 4
            print("\nRuta turística por resistencia")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                rutaTuristicaResistencia(cont)

        elif inputs == 6:   #Req. 5
            print("\nRecomendador de rutas")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                t1_start = process_time() #tiempo inicial
                recomendadorRutas(cont)
                t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")

        elif inputs == 7:   #Req. 6
            print("\nRuta de interés turístico")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                
                optionSeven(cont)
            
        
        elif inputs == 8:   #Req. 7*
            print('\nIndentificación de estaciones para publicidad')
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                optionEight(cont)
        
        elif inputs == 9:   #Req. 8*
            print('\nIdentificacion de bicicletas para mantenimiento')
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                print('lolalisimo xd')
        
        elif inputs == 0:   #Salir
            print('Cerrando el programa ...')
            sys.exit(0)
        else:
            print('Opción incorrecta .....')
main()

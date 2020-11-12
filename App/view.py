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
initialStation = None
recursionLimit = 30000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("-"*75)
    print("Bienvenido")
    print("1- Inicializar Analizador y cargar archivo CSV")
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


def optionTwo(cont):
    print("\nCargando información de CitiBike ....")
    controller.loadFile(cont, tripfile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStation(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    controller.cantidadClusters(cont, 0,0)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))
    # controller.cantidadClusters(cont, '','')

def optionThree(cont):
    estacion1= input('Dijite la primera estación: ')
    estacion2 = input('Dijite la segunda estación: ')
    data  = controller.cantidadClusters(cont, estacion1, estacion2)
    print('Hay ',data[0], ' clusters dentro del gráfo')
    if data[1] == True:
        print('La estacion ',estacion1, ' y la estacion ',estacion2, ' están en el mismo clúster')
    else:
         print('La estacion ',estacion1, ' y la estacion ',estacion2, ' no están en el mismo clúster')

"""
def optionFour():
    controller.minimumCostPaths(cont, initialStation)


def optionFive():
    haspath = controller.hasPath(cont, destStation)
    print('Hay camino entre la estación base : ' +
          'y la estación: ' + destStation + ': ')
    print(haspath)


def optionSix():
    path = controller.minimumCostPath(cont, destStation)
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            print(stop)
    else:
        print('No hay camino')


def optionSeven():
    maxvert, maxdeg = controller.servedRoutes(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))
"""


def main():
    while True:
        printMenu()
        inputs = int(input('Seleccione una opción para continuar\n->'))

        if inputs == 1:   #Inicio y carga
            t1_start = process_time() #tiempo inicial
            print("\nInicializando....")
            tamaño = int(input("Digite el tamaño de la tabla de hash: "))
            carga = float(input("Digita el factor de carga: "))
            cont = controller.init(tamaño, carga)
            t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")

        elif inputs == 2: 
            print("\nCantidad de Clusters de viajes")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                optionTwo(cont)

        elif inputs == 3:   #Req. 1
            print("\nRuta turística Circular")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                t1_start = process_time() #tiempo inicial
                optionThree(cont)
                t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")

        elif inputs == 4:   #Req. 2
            print("\nEstaciones críticas")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                
                msg = "Estación Base: BusStopCode-ServiceNo (Ej: 75009-10): "
            initialStation = input(msg)
            executiontime = timeit.timeit(optionFour, number=1)
            print("Tiempo de ejecución: " + str(executiontime))

        elif inputs == 5:   #Req. 4
            print("\nRuta turística por resistencia")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                
                destStation = input("Estación destino (Ej: 15151-10): ")
            executiontime = timeit.timeit(optionFive, number=1)
            print("Tiempo de ejecución: " + str(executiontime))

        elif inputs == 6:   #Req. 5
            print("\nRecomendador de rutas")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                
                destStation = input("Estación destino (Ej: 15151-10): ")
            executiontime = timeit.timeit(optionSix, number=1)
            print("Tiempo de ejecución: " + str(executiontime))

        elif inputs == 7:   #Req. 6
            print("\nRuta de interés turístico")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                
                executiontime = timeit.timeit(optionSeven, number=1)
            print("Tiempo de ejecución: " + str(executiontime))
        
        elif inputs == 8:   #Req. 7*
            print('\nIndentificación de estaciones para publicidad')
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                print('lolazo xd')
        
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

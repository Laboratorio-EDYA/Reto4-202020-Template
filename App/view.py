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

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


tripfile = '201801-3-citibike-tripdata.csv'
initialStation = None
recursionLimit = 30000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("-"*75)
    print("Bienvenido")
    print("1- Inicializar Analizador y cargar archivos CSV")
    print("2- Cantidad de Clusters en viajes")
    print("3- Ruta turística Circular")
    print("4- Ruta turística de menor tiempo")
    print("5- Ruta turística por resistencia ")
    print("6- Ruta más corta entre estaciones ")
    print("7- Ruta de interés turístico ")
    print("8- Identificación de estaciones para publcidad")
    print("9- Identificación de bicis para mantenimiento")
    print("0- Salir")
    print("-"*75)


def optionTwo():
    print("\nCargando información de CitiBike ....")
    controller.loadFile(cont, tripfile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStation(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))
    controller.cantidadClusters(cont, '','')




"""
Menu principal
"""
while True:
    printMenu()
    inputs = int(input('Selecciona una opción para continuar\n-->'))

    if inputs == 1:
        print("\nInicializando....")

        # cont es el controlador que se usará de acá en adelante
        tamaño = int(input("Digite el tamaño de la tabla de hash: "))
        carga = float(input("Digita el factor de carga: "))
        cont = controller.init(tamaño, carga)

    elif int(inputs[0]) == 2:
        cont = controller.init()
        print("\nCargando información de CitiBike ....")
        controller.loadServices(cont, bikefile)
        numedges = controller.totalConnections(cont)
        numvertex = controller.totalStops(cont)
        print('Número de vertices: ' + str(numvertex))
        print('Número de arcos: ' + str(numedges))
        print('El limite de recursión actual: ' + str(sys.getrecursionlimit()))
        sys.setrecursionlimit(recursionLimit)
        print('El limite de recursión se ajusta a: ' + str(recursionLimit))

    elif inputs == 2:

        executiontime = timeit.timeit(optionTwo, number=1)
        id1=input("Digite la id inicial")
        id2=input("Digite la id final")
        x=controller.cantidadDeClusteres(cont,id1,id2)
        print("Tiempo de ejecución: " + str(executiontime))

    elif inputs == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif inputs == 4:
        msg = "Estación Base: BusStopCode-ServiceNo (Ej: 75009-10): "
        initialStation = input(msg)
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif inputs == 5:
        destStation = input("Estación destino (Ej: 15151-10): ")
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif inputs == 6:
        destStation = input("Estación destino (Ej: 15151-10): ")
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif inputs == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    """elif inputs == 8:

    elif inputs == 9:

    elif inputs == 0:
        sys.exit(0)
    
    else:
        print("Opción incorrecta .....")
"""
main()

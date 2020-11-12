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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo
def newAnalyzer(tamaño, carga):
    """ Inicializa el analizador

   stations: Tabla de hash para guardar los vertices del grafo
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {'graph': None,
                    'stations': None,
                    'paths': None}
                    
        analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                        directed=True,
                        size=1000,
                        comparefunction=compareStations)

        analyzer['stations'] = m.newMap(numelements=tamaño,
                                     maptype='CHAINING',
                                     loadfactor=carga,
                                     comparefunction=compareStations)

        analyzer['paths'] = m.newMap(numelements=tamaño,
                                     maptype='CHAINING',
                                     loadfactor=carga,
                                     comparefunction=compareroutes)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo



def addTrip(analyzer, trip):
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    addConnection(analyzer, origin, destination, duration)
    addRouteStation(analyzer, trip)



def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['graph'], stationid):
            gr.insertVertex(analyzer['graph'], stationid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStation')


def addRouteStation(analyzer, trip):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    entry = m.get(analyzer['stations'], trip['start station id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)

        lt.addLast(lstroutes, trip['end station id'])
        m.put(analyzer['stations'], trip['start station id'], lstroutes)
    else:
        lstroutes = entry['value']
        info = trip['end station id']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer


def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['graph'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['graph'], origin, destination, duration)
    return analyzer

# ==============================
# R E Q U E R I M I E N T O S
# ==============================

def cantidadClusters(analyzer, id1 , id2):
    var = scc.KosarajuSCC(analyzer['graph'])
    vertices = gr.vertices(analyzer['graph'])
    clusters = {'size': 0}
    iterator = it.newIterator(vertices)
    while it.hasNext(iterator):
        current = it.next(iterator)
        cod = m.get(var['idscc'], current)['value']
        if cod not in clusters:
            clusters[cod] = lt.newList()
            clusters['size'] += 1
        lt.addLast(clusters[cod],current)
    print(clusters['size'])

# ==============================
# Funciones de consulta
# ==============================


def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['stations'] = scc.KosarajuSCC(analyzer['stations'])
    return scc.connectedComponents(analyzer['stations'])


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['graph'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStation(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])


def numberStations(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stations'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stations'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg


# ==============================
# Funciones Helper
# ==============================


def formatVertex(station):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = station['start station id']
    return name


# ==============================
# Funciones de Comparacion
# ==============================


def compareStations(station, keyvaluestation):
    stationcode = keyvaluestation['key']
    if (station == stationcode):
        return 0
    elif (station > stationcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1


def compareConnections(connection1, connection2):

    if (connection1 == connection2):
        return 0
    elif (connection1 > connection2):
        return 1
    else:
        return -1

# ==============================
# Requerimientos
# ==============================

def cantidadClusters(cont,id1,id2):   #Req. 1
    iterator=djk.Dijkstra(cont,id1)
    minimuncostpath= minimumCostPath(cont,id1)
    print(minimuncostpath)
    cont=0
    #while hasPath(iterator,id2):
    #    cont+=1

"""
def rutaTuristicaCircular(analyzer, time, startStation):   #Req. 2

def estacionesCriticas(analyzer):   #Req. 3

def rutaTuristicaResistencia(analyzer, time, idstation):   #Req. 4

def recomendadorRutas(analyzer, edades):   #Req. 5

def rutaInteresTuristico(analyzer, latlocal, longlocal, latfinal, longfinal):   #Req. 6

def estacionesPublicidad(analyzer, rango):   #Req. 7*

def bicicletasMantenimmiento(analyzer, idbike, fecha):   #Req. 8*"""

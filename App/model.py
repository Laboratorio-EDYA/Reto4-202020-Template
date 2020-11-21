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
import operator
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config
import obspy.geodetics as og
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
# Funciones de consulta
# ==============================


def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['stations'] = scc.KosarajuSCC(analyzer['graph'])
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

def cantidadClusters(analyzer, id1 , id2):
    """
    ----------REQUERIMIENTO 1------------
    OUTPUTS:
        TUPLE: (1,2)
            1: Clusters
            2: Sí dos nodos están en el mismo clúster
            3: Variable del algoritmo
    """
    try:
        var = scc.KosarajuSCC(analyzer['graph'])
        vertices = gr.vertices(analyzer['graph'])
        clusters = {'size': 0}
        iterator = it.newIterator(vertices)
        while it.hasNext(iterator):
            current = it.next(iterator)
            cod = m.get(var['idscc'], current)['value']
            if cod not in clusters:
                clusters[cod] = lt.newList(cmpfunction=compareStations)
                clusters['size'] += 1
            lt.addLast(clusters[cod],current)
        conected = False
        if m.get(var['idscc'],id1) != None and m.get(var['idscc'],id2) != None:
            conected = scc.stronglyConnected(var,id1,id2)
        return (clusters,conected,var)
    except:
        return -1

def rutaTuristicaCircular(analizador, time, startStation):   #Req. 2
    try:
        analyzer = analizador.copy()
        clusters = cantidadClusters(analyzer,'1','2')
        cluster = clusters[0][m.get(clusters[2]['idscc'],startStation)['value']]
        vecinos = gr.adjacents(analyzer['graph'],startStation)
        caminos = [0]
        iterator = it.newIterator(vecinos)
        while it.hasNext(iterator):
            current = it.next(iterator)
            if current != startStation and current in str(cluster):
                gr.removeVertex(analyzer['graph'],startStation)
                dijkstra = djk.Dijkstra(analyzer['graph'],current)
                path = djk.pathTo(dijkstra,startStation)
                if path != None:
                    trip = djk.distTo(dijkstra,startStation) + 20*(lt.size(path))
                    if trip > int(time[0]) and trip < int(time[1]) and lt.size(path) >= 3:
                        caminos[0] += 1
                        caminos.append((path,trip))   
                analyzer = analizador.copy()
        return caminos
    except:
        return -1    

"""def caminosx(analyzer,startStation,current,paths,lst):
    vecinos = gr.adjacents(analyzer['graph'],current)
    dijkstra = djk.Dijkstra(analyzer['graph'],current)
    iterator = it.newIterator(vecinos)
    while it.hasNext(iterator):
        actual = it.next(iterator)
        adyacentes = gr.adjacents(analyzer['graph'],actual)
        if startStation in str(adyacentes):
            lt.addLast(paths,lst)
            lst = lt.newList()
        elif djk.pathTo(dijkstra,startStation) != None:
            lt.addLast(lst,actual)
            caminos(analyzer,startStation,actual,paths,lst)"""
"""

"""
def estacionesCriticas(analyzer):   #Req. 3
    estaciones_de_llegada_pre_R={}
    estaciones_de_salida_pre_R={}
    estaciones={}
    lista=m.keySet(analyzer['stations'])
    iterator=it.newIterator(lista)
    while it.hasNext(iterator):
        actual=it.next(iterator)
        salida=gr.indegree(analyzer['graph'],actual)
        estaciones_de_llegada_pre_R[actual]=salida
        entrada=gr.outdegree(analyzer['graph'],actual)
        todo=gr.degree(analyzer['graph'],actual)
        estaciones[actual]=todo
        estaciones_de_salida_pre_R[actual]=entrada
    estaciones_de_salida_R=sorted(estaciones_de_salida_pre_R.items(),key=operator.itemgetter(1),reverse=True)
    estaciones_de_llegada_R=sorted(estaciones_de_llegada_pre_R.items(),key=operator.itemgetter(1),reverse=True)
    estaciones_R=sorted(estaciones.items(),key=operator.itemgetter(1),reverse=False)
    """la función sorted devuelve una lista de tuplas donde tupla[0] es la clave y tupla[1] es el valor"""
    eds={}
    edl={}
    em={}
    cont1=False
    cont2=False
    cont3=False
    
    while len(edl)<4:
        if cont1==False:
            for i in estaciones_de_llegada_R: #Donde i es una tupla de la lista de tuplas
                edl[i]=i
                if len(edl)==3:
                    cont1=True
    while len(eds)<4:
        if cont2==False:
            for i in estaciones_de_salida_R: #Donde i es una tupla de la lista de tuplas
                eds[i]=i
                if len(eds)==3:
                    cont2=True
    while len(em)<4: 
        if cont3==False:
            for i in estaciones_R: #Donde i es una tupla de la lista de tuplas
                em[i]=i
                if len(em)==3:
                    cont3=True
    return (eds,edl,em) #donde eds es estaciones de salida, edl estaciones de llegada, em estaciones menos usadas


def gradosAkilometros(data):
    dato=og.degrees2kilometers(data)
    return dato
def distanceBetween(latlocal,latfinal,longlocal,longfinal,longlst,latlst):
    """
    Sea longlst y latlst la longitud y la latitud de la lista 
    """
def rutaInteresTuristico(analyzer, latlocal, longlocal, latfinal, longfinal):   #Req. 6
    coordtuple=(m.keySet(analyzer['start station latitude']),m.keySet(analyzer['start station longitud']))
    """
    sea coortuple como t
    t[0] son las latitudes iniciales y t[1] son las longitudes iniciales de las estaciones 
    """
    iterator1=it.newIterator(coordtuple[0])
    iterator2=it.newIterator(coordtuple[1])
    while it.hasNext(iterator1):
        actual1=it.next(iterator1)

    while it.hasNext(iterator2):    
        actual2=it.next(iterator2)
"""    
def rutaTuristicaResistencia(analyzer, time, idstation):   #Req. 4

def recomendadorRutas(analyzer, edades):   #Req. 5

def rutaInteresTuristico(analyzer, latlocal, longlocal, latfinal, longfinal):   #Req. 6

def estacionesPublicidad(analyzer, rango):   #Req. 7*

def bicicletasMantenimmiento(analyzer, idbike, fecha):   #Req. 8*"""

"""mayor = [0,0,0,0]
    lt.addLast(clusters[cod],current)
    if lt.size(clusters[cod]) > mayor[1]:
        mayor[0] = cod
        mayor[1] = lt.size(clusters[cod])
iterator = it.newIterator(clusters[mayor[0]])
while it.hasNext(iterator):
    actual = it.next(iterator)
    if mayor[2] < gr.degree(analyzer['graph'],actual):
        mayor[2] = gr.degree(analyzer['graph'],actual)
        mayor[3] = actual
print(str(mayor[3]))"""
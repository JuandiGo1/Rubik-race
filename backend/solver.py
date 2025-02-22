# -*- coding: utf-8 -*-
"""Copia de 24-Puzzle.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IObA8ssn2h_LIKKHUyoMTrH_EIGwfDDP

# Librerías
"""

from queue import PriorityQueue
import copy
import os
import json


"""# Lectura y Validación de Archivo"""

def leer_estado(nombre_archivo):
    """
    Lee el estado desde un archivo de texto.

    Args:
        nombre_archivo (str): Nombre del archivo a leer.

    Returns:
        str: Estado como un string, o None si hay un error.
    """
    try:
        with open(nombre_archivo, 'r') as archivo:
            estado = "".join(line.strip() for line in archivo)  # Leer y concatenar las líneas
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no se encuentra.")
        return None
    except Exception as e:
        print(f"Error al leer el archivo '{nombre_archivo}': {e}")
        return None

    estado = estado.replace(" ", "")  # Eliminar espacios
    return estado

def validar_archivo_inicial(estado):
    """
    Valida el estado inicial: longitud, caracter '*', caracteres válidos y cantidad de colores.

    Args:
        estado (str): El estado inicial como string.

    Returns:
        bool: True si el estado es válido, False en caso contrario.
    """
    if estado is None:
        return False

    if len(estado) != 25:
        print("Error: El estado inicial debe tener 25 caracteres.")
        return False

    if '*' not in estado:
        print("Error: El estado inicial debe contener el carácter '*'.")
        return False

    caracteres_validos = set("*BRVNAZ")
    if not all(caracter in caracteres_validos for caracter in estado):
        print("Error: El estado inicial contiene caracteres inválidos.")
        return False

    conteo_colores = {color: estado.count(color) for color in caracteres_validos}
    for color, cantidad in conteo_colores.items():
        if color != '*' and cantidad != 4:
            print(f"Error: El archivo inicial debe contener exactamente 4 caracteres del color {color}.")
            return False

    return True

def validar_archivo_meta(estado):
    """
    Valida el estado meta: longitud, caracteres válidos y cantidad de colores.

    Args:
        estado (str): El estado meta como string.

    Returns:
        bool: True si el estado es válido, False en caso contrario.
    """
    if estado is None:
        return False

    if len(estado) != 9:
        print("Error: El estado meta debe tener 9 caracteres.")
        return False

    caracteres_validos = set("BRVNAZ")
    if not all(caracter in caracteres_validos for caracter in estado):
        print("Error: El estado meta contiene caracteres inválidos.")
        return False

    conteo_colores = {color: estado.count(color) for color in caracteres_validos}
    for color, cantidad in conteo_colores.items():
        if cantidad > 4:
            print(f"Error: El archivo meta no debe contener más de 4 caracteres del color {color}.")
            return False

    return True

"""# Operadores de movimiento"""

def encontrar_casilla_vacia(estado):
    """
    Encuentra las coordenadas (fila, columna) de la casilla vacía '*' en el estado.

    Args:
        estado (str): El estado del juego como un string.

    Returns:
        tuple: Una tupla (fila, columna) con las coordenadas de la casilla vacía,
               o None si no se encuentra la casilla vacía.
    """
    try:
        indice = estado.index('*')
        fila = indice // 5
        columna = indice % 5
        return fila, columna
    except ValueError:
        return None

def mover_arriba(estado):
    """
    Mueve la casilla vacía hacia arriba, intercambiándola con la ficha de arriba.

    Args:
        estado (str): El estado del juego como un string.

    Returns:
        str: El nuevo estado (string) después del movimiento, o None si el movimiento no es válido.
    """
    vacia = encontrar_casilla_vacia(estado)
    if vacia is None or vacia[0] == 0:  # No se puede mover arriba desde la primera fila
        return None

    fila, columna = vacia
    nuevo_indice = (fila - 1) * 5 + columna  # Calcular el índice del nuevo lugar de la casilla vacía
    indice_vacia = fila * 5 + columna

    # Crear una lista para poder modificar los caracteres del string
    estado_lista = list(estado)
    estado_lista[indice_vacia], estado_lista[nuevo_indice] = estado_lista[nuevo_indice], estado_lista[indice_vacia]
    return "".join(estado_lista) #Unir los caracteres en un string


def mover_abajo(estado):
  #Implementar funcion
    vacia = encontrar_casilla_vacia(estado)
    if vacia is None or vacia[0] == 4:  # No se puede mover arriba desde la primera fila
        return None

    fila, columna = vacia
    nuevo_indice = (fila + 1) * 5 + columna  # Calcular el índice del nuevo lugar de la casilla vacía
    indice_vacia = fila * 5 + columna

    # Crear una lista para poder modificar los caracteres del string
    estado_lista = list(estado)
    estado_lista[indice_vacia], estado_lista[nuevo_indice] = estado_lista[nuevo_indice], estado_lista[indice_vacia]
    return "".join(estado_lista) #Unir los caracteres en un string

def mover_izquierda(estado):
    #Implementar funcion
    vacia = encontrar_casilla_vacia(estado)
    if vacia is None or vacia[1] == 0:  # No se puede mover arriba desde la primera fila
        return None

    fila, columna = vacia
    nuevo_indice = fila * 5 + columna - 1  # Calcular el índice del nuevo lugar de la casilla vacía
    indice_vacia = fila * 5 + columna

    # Crear una lista para poder modificar los caracteres del string
    estado_lista = list(estado)
    estado_lista[indice_vacia], estado_lista[nuevo_indice] = estado_lista[nuevo_indice], estado_lista[indice_vacia]
    return "".join(estado_lista) #Unir los caracteres en un string

def mover_derecha(estado):
    #Implementar funcion
    vacia = encontrar_casilla_vacia(estado)
    if vacia is None or vacia[1] == 4:  # No se puede mover arriba desde la primera fila
        return None

    fila, columna = vacia
    nuevo_indice = fila * 5 + columna + 1  # Calcular el índice del nuevo lugar de la casilla vacía
    indice_vacia = fila * 5 + columna

    # Crear una lista para poder modificar los caracteres del string
    estado_lista = list(estado)
    estado_lista[indice_vacia], estado_lista[nuevo_indice] = estado_lista[nuevo_indice], estado_lista[indice_vacia]
    return "".join(estado_lista) #Unir los caracteres en un string

def movimiento(estado):
    """
    Genera una lista de movimientos válidos.

    Args:
        estado (str): Estado del tablero.

    Returns:
        list: Lista de movimientos válidos (1-4).
    """
    movimientos = [i for i, move_func in enumerate([mover_arriba, mover_abajo, mover_izquierda, mover_derecha], 1)
                  if move_func(estado) is not None]
    return movimientos

def sucesor(estado, movimiento_numero):
    """
    Aplica un movimiento al estado.

    Args:
        estado (str): Estado del tablero.
        movimiento_numero (int): Número del movimiento (1-4).

    Returns:
        str: Nuevo estado, o None si el movimiento es inválido.
    """
    if movimiento_numero == 1:
        return mover_arriba(estado)
    elif movimiento_numero == 2:
        return mover_abajo(estado)
    elif movimiento_numero == 3:
        return mover_izquierda(estado)
    elif movimiento_numero == 4:
        return mover_derecha(estado)
    return None



def calcular_heuristica_manhattan(estado_actual, estado_meta):
    """
    Calcula la heurística de Manhattan.

    Args:
        estado_actual (str): Estado actual del juego.
        estado_meta (str): Estado meta del juego.

    Returns:
        int: Valor heurístico de Manhattan.
    """
    distancia_total = 0
    for i in range(len(estado_meta)):
        meta = estado_meta[i]
        fila_meta = i // 3
        columna_meta = i % 3

        distancia_min = 120
        for j in range(len(estado_actual)):
            if estado_actual[j] == meta:
                fila_actual = (j // 5) - 1
                columna_actual = (j % 5) - 1

                # Asegurarse de comparar solo con las casillas centrales
                if 0 <= fila_actual <= 2 and 0 <= columna_actual <= 2:
                    distance = abs(fila_actual - fila_meta) + abs(columna_actual - columna_meta)
                    distancia_min = min(distancia_min, distance)
        distancia_total += distancia_min
    return distancia_total



def meta(estado_actual, estado_meta):
    """
    Verifica si el centro 3x3 del estado actual coincide con el estado meta.

    Args:
        estado_actual (str): Estado actual del tablero.
        estado_meta (str): Estado meta del tablero.

    Returns:
        bool: True si el estado meta se ha alcanzado, False en caso contrario.
    """
    centro = (estado_actual[6:9] + estado_actual[11:14] + estado_actual[16:19])
    return centro == estado_meta

class Nodo:
    """Representa un nodo en el árbol de búsqueda."""
    def __init__(self, estado, costo_g, costo_h=0, padre=None, movimiento=None):
        """
        Inicializa un nuevo nodo.

        Args:
            estado (str): Estado del tablero.
            costo_g (int): Costo del camino desde el inicio.
            costo_h (int): Valor heurístico (por defecto 0).
            padre (Nodo): Nodo padre (por defecto None).
            movimiento (int): Movimiento realizado para llegar a este nodo (por defecto None).
        """
        self.estado = estado
        self.costo_g = costo_g
        self.costo_h = costo_h
        self.costo_f = self.costo_g + self.costo_h
        self.padre = padre
        self.movimiento = movimiento

    def __lt__(self, otro):
        """
        Compara nodos para la cola de prioridad.

        Args:
            otro (Nodo): Otro nodo a comparar.

        Returns:
            bool: True si este nodo tiene menor prioridad.
        """
        if self.costo_f != otro.costo_f:
            return self.costo_f < otro.costo_f
        return self.costo_h < otro.costo_h



def reconstruir_camino(nodo_meta):
    """
    Reconstruye el camino desde el estado inicial al estado meta.

    """
    camino = []
    nodo_actual = nodo_meta
    while nodo_actual is not None and nodo_actual.movimiento is not None:
        tablero_matriz = [list(nodo_actual.estado[i:i+5]) for i in range(0, 25, 5)]
        camino.append({
            "heuristica": nodo_actual.costo_h,
            "movimiento": nodo_actual.movimiento,
            "cantidad_movimientos": nodo_actual.costo_g,
            "tablero": tablero_matriz
        })
        nodo_actual = nodo_actual.padre
    return camino[::-1]

def a_estrella(estado_inicial, estado_meta, heuristica=calcular_heuristica_manhattan, archivo_salida="uploads/salida.json"):
    """
    Implementa el algoritmo A* para encontrar una solución al juego.

    Args:
        estado_inicial (str): Estado inicial del juego.
        estado_meta (str): Estado meta del juego.
        heuristica (function): Función heurística a usar (por defecto, Manhattan).
        archivo_salida (str): Archivo para guardar la solución.

    Returns:
        bool: True si se encuentra una solución, False en caso contrario.
    """

    cola_prioridad = PriorityQueue() #Cola de prioridad
    nodo_inicial = Nodo(estado_inicial, 0, heuristica(estado_inicial, estado_meta)) #Nodo inicial
    cola_prioridad.put((nodo_inicial.costo_f, nodo_inicial)) #Añadir nodo a la cola

    estados_visitados = {estado_inicial} #Conjunto de estados visitados

    solucion_json = [] #Lista de pasos de la solución

    while not cola_prioridad.empty(): #Iterar mientras haya nodos en la cola
        costo_f, nodo_actual = cola_prioridad.get() #Obtener nodo con menor costo f

        if meta(nodo_actual.estado, estado_meta): #Si es el estado meta, reconstruir el camino
            print("¡Solución encontrada!")
            solucion_json = reconstruir_camino(nodo_actual)

            with open(archivo_salida, "w") as archivo: #Guardar camino en el archivo
                json.dump({"solucion": solucion_json}, archivo, indent=4)
            return archivo_salida

        for num_movimiento in movimiento(nodo_actual.estado): #Iterar sobre los movimientos posibles
            nuevo_estado = sucesor(nodo_actual.estado, num_movimiento)

            if nuevo_estado and nuevo_estado not in estados_visitados: #Verificar que el movimiento es válido y no se ha visitado el estado
                costo_g = nodo_actual.costo_g + 1 #Calcular costo g
                costo_h = heuristica(nuevo_estado, estado_meta) #Calcular heurística
                nuevo_nodo = Nodo(nuevo_estado, costo_g, costo_h, nodo_actual, num_movimiento) #Crear nuevo nodo

                cola_prioridad.put((nuevo_nodo.costo_f, nuevo_nodo)) #Añadir a la cola de prioridad
                estados_visitados.add(nuevo_estado) #Añadir a los estados visitados

    #Si no se encuentra una solución
    print("No se encontró una solución.")
    with open(archivo_salida, "w") as archivo:
        json.dump({"solucion": []}, archivo, indent=4)
    return archivo_salida



"""# __name__ == "__main__"
"""

def resolver_rubik_race(archivo_inicial, archivo_meta):
    estado_inicial = leer_estado(archivo_inicial)
    estado_meta = leer_estado(archivo_meta)
    
    if estado_inicial and estado_meta:
        archivo_salida = os.path.join("uploads", "salida.json")
        archivo_salida = a_estrella(estado_inicial, estado_meta, calcular_heuristica_manhattan, archivo_salida)
        #archivo_salida = a_estrella(estado_inicial, estado_meta, calcular_heuristica_manhattan)
        return archivo_salida
    else:
        return None
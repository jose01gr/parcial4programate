import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpStatus, value
from munkres import Munkres

def resolver_problema_asignacion():
    # Solicitar el tamaño de la matriz de costos
    while True:
        try:
            filas = int(input("Ingrese el número de filas de la matriz de costos: "))
            columnas = int(input("Ingrese el número de columnas de la matriz de costos: "))
            if filas <= 0 or columnas <= 0:
                raise ValueError
            break
        except ValueError:
            print("Los valores deben ser enteros positivos.")

    # Solicitar los costos
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(int(input(f"Ingrese el costo de la fila {i + 1} y la columna {j + 1}: ")))
        matriz.append(fila)

    # Crear una instancia del algoritmo Munkres
    algoritmo = Munkres()
    asignacion = algoritmo.compute(matriz)

    # Calcular el costo total
    asignacion_final = []
    costo_final = 0
    for fila, columna in asignacion:
        costo = matriz[fila][columna]
        asignacion_final.append((fila, columna))
        costo_final += costo

    return asignacion_final, costo_final

def resolver_problema_transporte():
    origen_count = int(input("Ingrese el número de ciudades de origen: "))
    destino_count = int(input("Ingrese el número de ciudades de destino: "))

    origenes = [input(f"Ingrese el nombre de la ciudad de origen {i + 1}: ") for i in range(origen_count)]
    destinos = [input(f"Ingrese el nombre de la ciudad de destino {i + 1}: ") for i in range(destino_count)]

    oferta = {ciudad: int(input(f"Ingrese la oferta de la ciudad {ciudad}: ")) for ciudad in origenes}
    demanda = {ciudad: int(input(f"Ingrese la demanda de la ciudad {ciudad}: ")) for ciudad in destinos}

    costos = {}
    for origen in origenes:
        costos[origen] = {}
        for destino in destinos:
            costos[origen][destino] = int(input(f"Ingrese el costo de envío de {origen} a {destino}: "))

    problema = LpProblem('Problema_de_Transporte', LpMinimize)
    variables = LpVariable.dicts('Envio', (origenes, destinos), 0)

    problema += lpSum(variables[origen][destino] * costos[origen][destino] for origen in origenes for destino in destinos)
    for destino in destinos:
        problema += lpSum(variables[origen][destino] for origen in origenes) == demanda[destino]
    for origen in origenes:
        problema += lpSum(variables[origen][destino] for destino in destinos) <= oferta[origen]

    problema.solve()
    print("Estado:", LpStatus[problema.status])

    if LpStatus[problema.status] == 'Optimal':
        for origen in origenes:
            for destino in destinos:
                if variables[origen][destino].varValue > 0:
                    print(f"Enviar {variables[origen][destino].varValue} unidades desde {origen} a {destino}")
        print('El costo mínimo es:', value(problema.objective))
    else:
        print("No se encontró una solución óptima.")

if __name__ == "__main__":
    while True:
        seleccion = input('Seleccione un tipo de problema\n  1) Problema de transporte\n  2) Problema de asignación\n  0) Salir\n')
        if seleccion == '1':
            resolver_problema_transporte()
        elif seleccion == '2':
            asignacion, costo = resolver_problema_asignacion()
            print("\nAsignación óptima:", asignacion)
            print("Costo total:", costo, '\n')
        elif seleccion == '0':
            break
        else:
            print(f'{seleccion} No es un comando válido, intente nuevamente')

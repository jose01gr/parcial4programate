from munkres import Munkres

def metodo_hungaro(matriz_costos):
    # Instanciar el algoritmo de Munkres
    algoritmo = Munkres()

    # Aplicar el algoritmo a la matriz de costos
    resultado = algoritmo.compute(matriz_costos)

    # Calcular el costo total y las asignaciones óptimas
    asignaciones = []
    costo_total = 0
    for fila, columna in resultado:
        costo = matriz_costos[fila][columna]
        asignaciones.append((fila, columna))
        costo_total += costo

    return asignaciones, costo_total

# Ejemplo
matriz = [
    [6, 9, 3, 4],
    [7, 8, 5, 1],
    [8, 4, 6, 7],
    [5, 2, 9, 3]
]

asignaciones, costo = metodo_hungaro(matriz)

print("Asignaciones óptimas:", asignaciones)
print("Costo total:", costo)

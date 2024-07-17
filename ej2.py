from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value

# Datos
origenes = ['P', 'Q', 'R']
destinos = ['E', 'F', 'G', 'H']

ofertas = {'P': 1500, 'Q': 1500, 'R': 1500}
demandas = {'E': 1000, 'F': 1200, 'G': 1500, 'H': 1000}

costos = {
    'P': {'E': 80, 'F': 100, 'G': 85, 'H': 90},
    'Q': {'E': 95, 'F': 85, 'G': 80, 'H': 100},
    'R': {'E': 90, 'F': 80, 'G': 95, 'H': 90}
}

# Problema
problema = LpProblem('Distribucion', LpMinimize)
envios = LpVariable.dicts('Envio', (origenes, destinos), 0)

# Función objetivo
problema += lpSum(envios[origen][destino] * costos[origen][destino] for origen in origenes for destino in destinos), "Costo_Total"

# Restricciones de demanda
for destino in destinos:
    problema += lpSum(envios[origen][destino] for origen in origenes) == demandas[destino], f"Demanda_{destino}"

# Restricciones de oferta
for origen in origenes:
    problema += lpSum(envios[origen][destino] for destino in destinos) <= ofertas[origen], f"Oferta_{origen}"

# Resolver
problema.solve()
print("Estado del problema:", LpStatus[problema.status])

# Resultados
if LpStatus[problema.status] == 'Optimal':
    for origen in origenes:
        for destino in destinos:
            if envios[origen][destino].varValue > 0:
                print(f"Enviar {envios[origen][destino].varValue} unidades desde {origen} a {destino}")

    print('El costo total mínimo es:', value(problema.objective))
else:
    print("No se encontró una solución óptima.")

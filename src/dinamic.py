import sys
import os
import numpy as np

# Agrega el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from src.data.data import load_from_xlsx  # No parece ser necesario en el contexto actual

# Cargar el archivo .npy en la variable dist
dist = np.load("C:/Users/oscar/OneDrive/Escritorio/UAB-Hackaton-2024/data/2_1.npy")

# Número de nodos
n = dist.shape[0]

# Matriz de memoización
memo = np.full((n+1, 1 << (n+1)), -1)

def fun(i, mask):
    # Caso base
    if mask == ((1 << i) | 3):
        return dist[0][i]

    # Memoización
    if memo[i][mask] != -1:
        return memo[i][mask]

    # Resultado del subproblema
    res = np.inf

    # Calcular el costo de viajar a todos los nodos en mask y terminar en el nodo i
    for j in range(1, n):
        if (mask & (1 << j)) != 0 and j != i and j != 0:
            res = min(res, fun(j, mask & (~(1 << i))) + dist[j][i])
    
    # Almacenar el valor mínimo en memo
    memo[i][mask] = res
    return res

# Programa principal para probar la lógica
ans = np.inf
final_mask = (1 << n) - 1

for i in range(1, n):
    ans = min(ans, fun(i, final_mask) + dist[i][0])

print("The cost of most efficient tour = " + str(ans))

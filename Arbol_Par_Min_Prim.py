import pygame
import heapq
import time
import random

# -----------------------------
# CONFIGURACIONES GENERALES
# -----------------------------
TAM_CELDA = 30
COLOR_FONDO = (30, 30, 30)

COLOR_INICIO = (0, 255, 0)
COLOR_OBSTACULO = (0, 0, 0)
COLOR_MST = (0, 255, 255)
COLOR_FRONTERA = (255, 255, 0)
COLOR_VISITADO = (100, 100, 255)
COLOR_VACIO = (200, 200, 200)

# Parámetros de pesos aleatorios
PESO_MIN = 1
PESO_MAX = 20

# -----------------------------
# AUXILIAR ARISTAS
# -----------------------------
def edge_key(u, v):
    return (u, v) if u <= v else (v, u)

# -----------------------------
# DIBUJAR TABLERO SIN PESOS
# -----------------------------
def dibujar_tablero(ventana, tablero, inicio, en_mst, frontera, visitados):
    ventana.fill(COLOR_FONDO)

    filas = len(tablero)
    columnas = len(tablero[0])

    for i in range(filas):
        for j in range(columnas):
            x = j * TAM_CELDA
            y = i * TAM_CELDA

            if (i, j) == inicio:
                color = COLOR_INICIO
            elif tablero[i][j] == float("inf"):
                color = COLOR_OBSTACULO
            elif (i, j) in en_mst:
                color = COLOR_MST
            elif (i, j) in frontera:
                color = COLOR_FRONTERA
            elif (i, j) in visitados:
                color = COLOR_VISITADO
            else:
                color = COLOR_VACIO

            pygame.draw.rect(ventana, color, (x, y, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(ventana, (50, 50, 50), (x, y, TAM_CELDA, TAM_CELDA), 1)

    pygame.display.update()
    pygame.time.delay(90)

# -----------------------------
# ALGORITMO DE PRIM (con pesos ocultos)
# -----------------------------
def prim_pygame(ventana, tablero, inicio, edge_weights):
    filas = len(tablero)
    columnas = len(tablero[0])

    en_mst = set()
    frontera = set()
    visitados = set()
    parent = {}
    min_key = {}
    mst_edges = []
    total_cost = 0

    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] != float("inf"):
                min_key[(i, j)] = float("inf")

    min_key[inicio] = 0
    pq = [(0, inicio)]

    print("Ejecutando Prim con pesos aleatorios ocultos...\n")

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        key, nodo = heapq.heappop(pq)

        if nodo in en_mst:
            continue

        en_mst.add(nodo)
        visitados.add(nodo)

        if nodo in parent:
            total_cost += edge_weights[edge_key(nodo, parent[nodo])]
            mst_edges.append((nodo, parent[nodo]))

        f, c = nodo
        for df, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nf, nc = f + df, c + dc
            vecino = (nf, nc)

            if (
                0 <= nf < filas and 0 <= nc < columnas and
                tablero[nf][nc] != float("inf") and
                vecino not in en_mst
            ):
                w = edge_weights[edge_key(nodo, vecino)]
                if w < min_key[vecino]:
                    min_key[vecino] = w
                    parent[vecino] = nodo
                    frontera.add(vecino)
                    heapq.heappush(pq, (w, vecino))

        dibujar_tablero(ventana, tablero, inicio, en_mst, frontera, visitados)

    print("Árbol Parcial Mínimo completado.")
    print(f"Costo total del APM (pesos ocultos): {total_cost}")

# -----------------------------
# GENERAR PESOS ALEATORIOS
# -----------------------------
def generar_edge_weights(tablero, peso_min, peso_max):
    filas = len(tablero)
    columnas = len(tablero[0])
    edge_weights = {}

    for r in range(filas):
        for c in range(columnas):
            if tablero[r][c] == float("inf"):
                continue

            u = (r, c)
            if c + 1 < columnas and tablero[r][c+1] != float("inf"):
                v = (r, c+1)
                edge_weights[edge_key(u, v)] = random.randint(peso_min, peso_max)

            if r + 1 < filas and tablero[r+1][c] != float("inf"):
                v = (r+1, c)
                edge_weights[edge_key(u, v)] = random.randint(peso_min, peso_max)

    return edge_weights

# -----------------------------
# MAIN
# -----------------------------
def main():
    pygame.init()

    ALTO = 10
    ANCHO = 20
    INICIO = (5, 12)

    OBSTACULOS = (
        [(3, i) for i in range(0, 15) if i not in (3,8)] +
        [(6, i) for i in range(5, 20)] +
        [(i, 14) for i in range(4, 6)]
    )

    tablero = [[0 for _ in range(ANCHO)] for _ in range(ALTO)]
    for obs in OBSTACULOS:
        tablero[obs[0]][obs[1]] = float("inf")

    edge_weights = generar_edge_weights(tablero, PESO_MIN, PESO_MAX)
    print(f"Pesos aleatorios generados para {len(edge_weights)} aristas.\n")

    ventana = pygame.display.set_mode((ANCHO * TAM_CELDA, ALTO * TAM_CELDA))
    pygame.display.set_caption("Árbol Parcial Mínimo (Prim) - Pesos Ocultos")

    prim_pygame(ventana, tablero, INICIO, edge_weights)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()

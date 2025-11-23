import pygame
import heapq
import time

# -----------------------------
# CONFIGURACIONES GENERALES
# -----------------------------
TAM_CELDA = 30
COLOR_FONDO = (30, 30, 30)

COLOR_INICIO = (0, 255, 0)
COLOR_OBSTACULO = (0, 0, 0)
COLOR_MST = (0, 255, 255)        # parte del árbol parcial mínimo
COLOR_FRONTERA = (255, 255, 0)   # nodos candidatos en la frontera
COLOR_VISITADO = (100, 100, 255)
COLOR_VACIO = (200, 200, 200)

# -----------------------------
# DIBUJAR TABLERO EN PYGAME
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
    pygame.time.delay(100)

# -----------------------------
# ALGORITMO DE PRIM
# -----------------------------
def prim_pygame(ventana, tablero, inicio):
    filas = len(tablero)
    columnas = len(tablero[0])

    en_mst = set()
    frontera = set()
    visitados = set()
    mst_parent = {}

    pq = []
    heapq.heappush(pq, (0, inicio, None))  # (peso, nodo, padre)

    while pq:
        # eventos de pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        peso, nodo, padre = heapq.heappop(pq)

        if nodo in en_mst:  
            continue

        visitados.add(nodo)

        # agregar al mst
        en_mst.add(nodo)
        if padre is not None:
            mst_parent[nodo] = padre

        f, c = nodo

        # EXPANDIR A LOS VECINOS
        for df, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nf, nc = f + df, c + dc

            if 0 <= nf < filas and 0 <= nc < columnas:
                if tablero[nf][nc] != float("inf") and (nf, nc) not in en_mst:
                    frontera.add((nf, nc))
                    heapq.heappush(pq, (1, (nf, nc), nodo))

        # actualizar animación
        dibujar_tablero(ventana, tablero, inicio, en_mst, frontera, visitados)

    print("Árbol Parcial Mínimo completado.")


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

    ventana = pygame.display.set_mode((ANCHO * TAM_CELDA, ALTO * TAM_CELDA))
    pygame.display.set_caption("Visualización del Árbol Parcial Mínimo (Prim)")

    prim_pygame(ventana, tablero, INICIO)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()

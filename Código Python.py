"""Actividad 2.1/2.2: modelado de problemas y espacios de búsqueda.
Instalar: python -m pip install networkx matplotlib
Ejecutar: python actividad_2_1_busqueda.py
"""
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# Problema 1: rutas de entrega, con costo en kilómetros.
RUTAS = [
    ("Almacén", "Centro", 4), ("Almacén", "Norte", 7),
    ("Centro", "Hospital", 5), ("Centro", "Parque", 3),
    ("Norte", "Parque", 2), ("Norte", "Hospital", 8),
    ("Parque", "Hospital", 2)
]

def crear_grafo_rutas():
    g = nx.DiGraph()
    for origen, destino, km in RUTAS:
        g.add_edge(origen, destino, weight=km)
    return g

def dibujar_rutas(g):
    pos = {"Almacén": (0,1), "Centro": (1,2), "Norte": (1,0),
           "Parque": (2,.4), "Hospital": (3,1)}
    plt.figure(figsize=(9,5))
    nx.draw_networkx(g, pos, node_size=2200, node_color="lightblue", arrows=True)
    labels = {(u,v): f"{d['weight']} km" for u,v,d in g.edges(data=True)}
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    plt.title("Ruta de entrega: pesos en kilómetros")
    plt.axis("off"); plt.tight_layout()
    plt.savefig("grafo_rutas_entrega.png", dpi=180); plt.close()

# Problema 2: robot en una cuadrícula 4x4 con dos obstáculos.
FILAS, COLUMNAS = 4, 4
INICIO, META = (0,0), (3,3)
OBSTACULOS = {(1,1), (2,1)}

def vecinos_validos(estado):
    f,c = estado
    candidatos = [(f-1,c),(f+1,c),(f,c-1),(f,c+1)]
    return [(a,b) for a,b in candidatos if 0 <= a < FILAS and 0 <= b < COLUMNAS
            and (a,b) not in OBSTACULOS]

def crear_grafo_robot():
    g = nx.DiGraph()
    for f in range(FILAS):
        for c in range(COLUMNAS):
            if (f,c) not in OBSTACULOS:
                g.add_node((f,c))
    for estado in list(g.nodes):
        for siguiente in vecinos_validos(estado):
            g.add_edge(estado, siguiente, weight=1)
    return g

def resolver_bfs(g, inicio, meta):
    cola = deque([inicio]); padres = {inicio: None}
    while cola:
        actual = cola.popleft()
        if actual == meta: break
        for sig in g.successors(actual):
            if sig not in padres:
                padres[sig] = actual; cola.append(sig)
    if meta not in padres: return None
    ruta=[]; actual=meta
    while actual is not None:
        ruta.append(actual); actual=padres[actual]
    return list(reversed(ruta))

def dibujar_robot(g, ruta):
    pos = {n:(n[1],-n[0]) for n in g.nodes}
    plt.figure(figsize=(7,6))
    nx.draw_networkx(g, pos, node_size=900, node_color="lightgreen", arrows=True)
    if ruta:
        nx.draw_networkx_edges(g,pos,edgelist=list(zip(ruta[:-1],ruta[1:])),
                               edge_color="red",width=2.5,arrows=True)
        nx.draw_networkx_nodes(g,pos,nodelist=ruta,node_color="gold",node_size=900)
    plt.title("Robot en cuadrícula: rojo = ruta encontrada")
    plt.axis("off"); plt.tight_layout()
    plt.savefig("grafo_robot.png", dpi=180); plt.close()

def main():
    g1=crear_grafo_rutas()
    ruta=nx.shortest_path(g1,"Almacén","Hospital",weight="weight")
    costo=nx.shortest_path_length(g1,"Almacén","Hospital",weight="weight")
    print("PROBLEMA 1 — Ruta:", " -> ".join(ruta), "| costo:", costo, "km")
    dibujar_rutas(g1)
    g2=crear_grafo_robot(); ruta2=resolver_bfs(g2,INICIO,META)
    print("PROBLEMA 2 — Estados:",g2.number_of_nodes(),"Transiciones:",g2.number_of_edges())
    print("Ruta del robot:",ruta2,"| movimientos:",len(ruta2)-1 if ruta2 else "sin solución")
    dibujar_robot(g2,ruta2)
    print("Diagramas creados: grafo_rutas_entrega.png y grafo_robot.png")

if __name__ == "__main__":
    main()

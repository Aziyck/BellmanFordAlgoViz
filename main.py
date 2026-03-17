import math
import networkx as nx
import matplotlib.pyplot as plt

def bellman_ford_between(edges, start, end, mode="min"):
    # determinam nodurile automat
    nodes = set()
    for u, v, _ in edges:
        nodes.add(u)
        nodes.add(v)

    # initializare distante si predecesori
    # Distanta de la primul nod este 0 iar toate celalte sunt infinit
    if mode == "min":
        dist = {node: math.inf for node in nodes}
    else:
        dist = {node: -math.inf for node in nodes}

    dist[start] = 0

    # pana cand nu avem nici un drum deci matrice predecesurilor este None
    # mai tarziu o sa o folosim sa recosntituim drumul
    predecessor = {node: None for node in nodes}

    print("Predecesorii initiali:", end="")
    print_arr(predecessor)
    print("Distantele initiale:  ", end="")
    print_arr(dist)

    n = len(nodes)

    # relaxare muchii de n-1 ori
    # Algoritmul se va repeta de n-1 ori
    for i in range(n - 1):
        updated = False
        # u = nodul de plecare
        # v = nodul de sosire
        # w = costul muchiei
        print(f"\n\nIteratia {i}:") 
        for u, v, w in edges:
            # Daca pot ajunge la u si drumul este mai scurt decat ce de pana acum 
            # atunci actualizam drumul si predecesorul
            if mode == "min":
                if dist[u] != math.inf and dist[u] + w < dist[v]:
                    print("") 
                    
                    dist[v] = dist[u] + w
                    predecessor[v] = u
                    print("Predecesorii:", end="")
                    print_arr(predecessor)
                    print("Distantele:  ", end="")
                    print_arr(dist)
                    updated = True

            else:
                if dist[u] != math.inf and dist[u] + w > dist[v]:
                    print("") 
                    
                    dist[v] = dist[u] + w
                    predecessor[v] = u
                    print("Predecesorii:", end="")
                    print_arr(predecessor)
                    print("Distantele:  ", end="")
                    print_arr(dist)
                    updated = True
            
        if not updated:
            print("Nu mai sunt schimbari\n")
            break

    # Am terminat dupa n-1 iteratii si acum mai verificam daca:

    # 1. daca nodul final nu e accesibil
    if dist[end] == math.inf:
        print("Nu exista drum intre noduri")
        return None, None

    # Daca tot e ok reconstituim drummul
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessor[current]

    path.reverse()

    return dist[end], path

def print_arr(arr):
    print("|", end="")
    for node in arr:
        print(f" {node} : {str(arr[node]):^5} |", end="")
    print("")


def draw_graph_step_bf(G, pos, tree_edges, current_edge, dist, mode="min"):
    plt.clf()

    # verificam daca fereastra a fost inchisa
    if not plt.fignum_exists(plt.gcf().number):
        print("Fereastra inchisa, oprim vizualizarea.")
        plt.close('all')
        return True  # semnal ca trebuie oprit

    # noduri colorate daca au distanta finita
    node_colors = []
    for n in G.nodes():
        if (mode=="min" and dist[n] != math.inf) or (mode=="max" and dist[n] != -math.inf):
            node_colors.append("lightgreen")
        else:
            node_colors.append("lightblue")

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors)

    # colorare muchii
    edge_colors = []
    for u, v in G.edges():
        if (u, v) in tree_edges:
            edge_colors.append("red")       # muchii din arbore
        elif current_edge and (u, v) == current_edge:
            edge_colors.append("orange")    # muchia verificata
        else:
            edge_colors.append("gray")

    nx.draw_networkx_edges(
        G, pos,
        width=2,
        edge_color=edge_colors,
        arrows=True,
        arrowstyle='-|>', 
        arrowsize=20 
    )

    # etichete noduri
    labels = {}
    for n in G.nodes():
        if (mode=="min" and dist[n] == math.inf) or (mode=="max" and dist[n] == -math.inf):
            labels[n] = f"{n}\n∞"
        else:
            labels[n] = f"{n}\n{dist[n]}"

    nx.draw_networkx_labels(G, pos, labels, font_size=11, font_weight="bold")

    # etichete muchii
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title(f"Bellman-Ford - Drum {'minim' if mode=='min' else 'maxim'}")
    plt.axis("off")
    plt.draw()

    # asteptam tasta; daca fereastra inchisa -> return True
    try:
        plt.waitforbuttonpress()
    except:
        return True

    return False

def bellman_ford_visual(edges, start, end, time=1.2, seed=200, k=2.0, mode="min"):

    print("-" * 30)

    G = nx.DiGraph()
    nodes = set()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
        nodes.add(u)
        nodes.add(v)

    pos = nx.spring_layout(G, seed=seed, k=k)

    dist = {node: (math.inf if mode=="min" else -math.inf) for node in nodes}
    predecessor = {node: None for node in nodes}
    dist[start] = 0

    print("Predecesorii initiali:", end="")
    print_arr(predecessor)
    print("Distantele initiale:  ", end="")
    print_arr(dist)

    tree_edges = []

    plt.ion()
    stop = draw_graph_step_bf(G, pos, tree_edges, None, dist, mode)
    if stop: return

    n = len(nodes)
    for i in range(n - 1):
        print(f"\nIteratia {i+1}")
        updated = False

        for u, v, w in edges:
            stop = draw_graph_step_bf(G, pos, tree_edges, (u, v), dist, mode)
            if stop: return

            if dist[u] != (math.inf if mode=="min" else -math.inf):
                if (mode=="min" and dist[u]+w < dist[v]) or (mode=="max" and dist[u]+w > dist[v]):
                    dist[v] = dist[u]+w
                    predecessor[v] = u
                    updated = True

                    # afisam pe consola
                    print("Predecesorii:", end="")
                    print_arr(predecessor)
                    print("Distantele:  ", end="")
                    print_arr(dist)
                    print()

                    # reconstruim arborele de drum
                    tree_edges.clear()
                    for node in predecessor:
                        if predecessor[node] is not None:
                            tree_edges.append((predecessor[node], node))

                    stop = draw_graph_step_bf(G, pos, tree_edges, (u, v), dist, mode)
                    if stop: return

        if not updated:
            break

    # verificam existenta drumului
    if end not in dist or (mode=="min" and dist[end]==math.inf) or (mode=="max" and dist[end]==-math.inf):
        print("Nu exista drum intre noduri")
        plt.ioff()
        plt.show()
        return

    # reconstruim drumul final
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessor[current]
    path.reverse()

    print(f"\nDistanta {'minima' if mode=='min' else 'maxima'}:", dist[end])
    print(f"Drumul {'minim' if mode=='min' else 'maxim'}:", path)

    # drum optim ca muchii
    optimal_edges = list(zip(path, path[1:]))

    # desen final
    plt.clf()
    node_colors = ["lightgreen" for _ in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors)

    edge_colors = []
    for u, v in G.edges():
        if (u, v) in optimal_edges:
            edge_colors.append("blue")      # DRUMUL OPTIM
        elif (u, v) in tree_edges:
            edge_colors.append("red")
        else:
            edge_colors.append("gray")

    nx.draw_networkx_edges(
        G, pos,
        width=3,
        edge_color=edge_colors,
        arrows=True,
        arrowstyle='-|>',
        arrowsize=20
    )

    labels = {n: f"{n}\n{dist[n]}" for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=11, font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title(f"Drumul optim (albastru) - {'minim' if mode=='min' else 'maxim'}")
    plt.axis("off")
    plt.ioff()
    plt.show()

def reorder_edges_by_rank(edges, start):
    """
    Reordoneaza nodurile dupa rang (hop de la start) si returneaza muchiile cu noile indexuri consecutive
    """
    import networkx as nx
    from collections import deque

    # construim graful
    G = nx.DiGraph()
    nodes = set()
    for u, v, w in edges:
        G.add_edge(u, v)
        nodes.add(u)
        nodes.add(v)

    # calculam rangul (hop-uri) pentru fiecare nod
    # pentru fiecare nod o sa salvam rank-ul in rank
    rank = {node: None for node in nodes}
    rank[start] = 0
    queue = deque([start])

    while queue:
        u = queue.popleft()
        for v in G.successors(u):
            if rank[v] is None or rank[v] > rank[u] + 1:
                rank[v] = rank[u] + 1
                queue.append(v)

    # sortam nodurile dupa rang
    ordered_nodes = sorted(rank.keys(), key=lambda n: rank[n])

    # cream mapping de la nodul original la nod consecutiv
    node_map = {old: new for new, old in enumerate(ordered_nodes, start=1)}  # 1,2,3...
    
    # reordonam muchiile cu noile indexuri
    new_edges = [(node_map[u], node_map[v], w) for u, v, w in edges]

    return new_edges, node_map, rank


if __name__ == "__main__":
    edges = [
    (1, 2, 2),
    (1, 3, 4),
    (2, 3, 1),
    (2, 5, 3),
    (2, 4, 5),
    (3, 4, 2),
    (3, 5, 1),
    (4, 5, 1),
    (4, 6, 2),
    (5, 6, 7)

    

    # (5, 1, 2),
    # (5, 6, 4),
    # (1, 6, 1),
    # (1, 2, 3),
    # (1, 3, 5),
    # (6, 3, 2),
    # (6, 2, 1),
    # (3, 2, 1),
    # (3, 4, 2),
    # (2, 4, 7)

    # (1,2,4),
    # (1,3,3),
    # (2,5,8),
    # (3,4,12),
    # (3,6,4),
    # (4,6,2),
    # (4,7,20),
    # (4,8,15),
    # (5,7,17),
    # (6,8,22),
    # (7,8,9)

    # (7,8,9),
    # (6,8,22),
    # (5,7,17),
    # (4,8,15),
    # (4,7,20),
    # (4,6,2),
    # (3,6,4),
    # (3,4,12),
    # (2,5,8),
    # (1,3,3),
    # (1,2,4)
]

# new_edges, node_map, ranks = reorder_edges_by_rank(edges, start=5)

# print("Muchii noi:", new_edges)
# print("Mapping noduri:", node_map)
# print("Ranguri:", ranks)

# distance, path = bellman_ford_between(edges, 1, 6, mode="min")
# distance, path = bellman_ford_between(new_edges, 1, 6, mode="min")

# print("Distanta minima:", distance)
# print("Drumul minim:", path)



# bellman_ford_visual(new_edges, 1, 6, time=1.1, seed=110, k=5.5, mode="min")

bellman_ford_visual(edges, 1, 6, time=1.1, seed=110, k=5.5, mode="min")

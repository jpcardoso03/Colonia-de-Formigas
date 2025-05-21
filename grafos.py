import numpy as np
import random
import logging
import matplotlib.pyplot as plt
import networkx as nx

logging.basicConfig(level=logging.INFO, format="%(message)s")


def carregar_matriz_distancias(arquivo):
    try:
        with open(arquivo, "r") as f:
            linhas = [linha.strip() for linha in f.readlines() if linha.strip() and not linha.startswith("#")]

        matriz = np.array([list(map(int, linha.split())) for linha in linhas])

        validar_matriz(matriz)
        return matriz

    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo: {e}")
        return None


def validar_matriz(matriz):
    if matriz.shape[0] != matriz.shape[1]:
        raise ValueError("A matriz de distâncias não é quadrada.")
    if not np.all(np.diag(matriz) == 0):
        raise ValueError("A diagonal principal da matriz deve conter apenas zeros.")
    if np.any(matriz < 0):
        raise ValueError("A matriz contém valores negativos.")


class AlgoritmoFormigas:
    def __init__(self, distancias, iteracoes=100, alfa=1, beta=5, evaporacao=0.5, Q=100):
        self.distancias = distancias
        self.num_nos = len(distancias)
        self.num_formigas = self.num_nos  
        self.iteracoes = iteracoes
        self.alfa = alfa  
        self.beta = beta  
        self.evaporacao = evaporacao
        self.Q = Q  
        self.feromonios = np.full((self.num_nos, self.num_nos), 1e-6)  # τ₀ = 10⁻⁶

    def rodar(self):
        melhor_caminho = None
        menor_distancia = float('inf')

        for iteracao in range(self.iteracoes):
            caminhos, distancias = zip(*[self.construir_caminho() for _ in range(self.num_formigas)])

            min_dist = min(distancias)
            if min_dist < menor_distancia:
                menor_distancia = min_dist
                melhor_caminho = caminhos[distancias.index(min_dist)]

            self.atualizar_feromonios(caminhos, distancias)
            logging.info(f"Iteração {iteracao+1}: Menor distância = {menor_distancia}")

        return melhor_caminho, menor_distancia

    def construir_caminho(self):
        no_inicial = random.randint(0, self.num_nos - 1)
        caminho = [no_inicial]
        visitadas = {no_inicial}
        no_atual = no_inicial
        distancia_total = 0

        while len(caminho) < self.num_nos:
            proximo_no = self.escolher_proximo_no(no_atual, visitadas)
            caminho.append(proximo_no)
            visitadas.add(proximo_no)
            distancia_total += self.distancias[no_atual, proximo_no]
            no_atual = proximo_no

        distancia_total += self.distancias[no_atual, no_inicial]  
        caminho.append(no_inicial)
        return caminho, distancia_total

    def escolher_proximo_no(self, no_atual, visitadas):
        nos_nao_visitados = np.array([no for no in range(self.num_nos) if no not in visitadas])

        feromonios = self.feromonios[no_atual, nos_nao_visitados] ** self.alfa
        heuristicas = (1 / np.maximum(self.distancias[no_atual, nos_nao_visitados], 1e-10)) ** self.beta  # Evita div/0
        probabilidades = feromonios * heuristicas
        total = probabilidades.sum()

        if total == 0:
            return random.choice(nos_nao_visitados)

        probabilidades /= total  
        return np.random.choice(nos_nao_visitados, p=probabilidades)

    def atualizar_feromonios(self, caminhos, distancias):
        """Atualiza os feromônios com base nos caminhos percorridos."""
        self.feromonios *= (1 - self.evaporacao)  
        for caminho, distancia in zip(caminhos, distancias):
            delta = self.Q / distancia
            for i in range(len(caminho) - 1):
                self.feromonios[caminho[i], caminho[i + 1]] += delta
                self.feromonios[caminho[i + 1], caminho[i]] += delta  

    def desenhar_grafo(self, melhor_caminho):
        """Desenha o grafo com o melhor caminho encontrado."""
        grafo = nx.Graph()
        grafo.add_nodes_from(range(self.num_nos))
        edges = [(melhor_caminho[i], melhor_caminho[i + 1]) for i in range(len(melhor_caminho) - 1)]
        for edge in edges:
            grafo.add_edge(*edge, weight=self.distancias[edge])

        pos = nx.circular_layout(grafo)
        plt.figure(figsize=(8, 6))
        nx.draw(grafo, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=10)
        nx.draw_networkx_edges(grafo, pos, edgelist=edges, edge_color='blue', width=2)
        edge_labels = {(u, v): f"{self.distancias[u, v]}" for u, v in edges}
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, font_size=8)
        plt.title("Melhor Rota Encontrada")
        plt.show()


if __name__ == "__main__":
    distancias = carregar_matriz_distancias("lau15_dist.txt")
    if distancias is not None:
        algoritmo = AlgoritmoFormigas(distancias)
        melhor_caminho, menor_distancia = algoritmo.rodar()
        logging.info(f"Melhor caminho encontrado: {melhor_caminho}")
        logging.info(f"Menor distância: {menor_distancia}")
        algoritmo.desenhar_grafo(melhor_caminho)

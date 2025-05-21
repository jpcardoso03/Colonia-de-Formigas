# 🐜 Colônia de Formigas — Otimização de Caminhos em Grafos

Este projeto foi desenvolvido como parte de um trabalho da disciplina de **Grafos**, e implementa uma abordagem inspirada na **colônia de formigas** (*Ant Colony Optimization*) para encontrar caminhos ótimos em grafos.

## 📌 Descrição

A ideia central do algoritmo é simular o comportamento coletivo das formigas ao buscar alimentos, onde cada formiga:

- Explora caminhos em um grafo.
- Deixa uma trilha de **feromônio** pelo caminho percorrido.
- Escolhe probabilisticamente caminhos com base na **quantidade de feromônio** e **distância**.
- Quanto mais feromônio em um caminho, maior a chance de outras formigas o seguirem.

Com o passar das iterações, os caminhos mais curtos (ou mais eficientes) acumulam mais feromônio, levando a uma **convergência para a melhor solução**.

## 🧠 Aplicação em Grafos

O grafo é representado com vértices e arestas (com pesos), e o objetivo pode ser:

- Encontrar o **menor caminho entre dois vértices**.
- Resolver o **problema do caixeiro viajante (TSP)**.
- Simular comportamento cooperativo em redes.

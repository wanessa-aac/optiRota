import os
import json
import random
import logging
import argparse
import networkx as nx
from networkx.readwrite import json_graph

from src.algorithms import precompute_distances

DEFAULT_GRAPH = "data/graph.json"
OUT = "data/distances.csv"

def load_graph(path: str):
    if not os.path.exists(path):
        raise SystemExit(f"Arquivo {path} não encontrado. Gere-o antes de rodar este script.")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    G = json_graph.node_link_graph(data, directed=True, multigraph=False, edges="links")
    # Converte IDs para str (se forem int, por ex) para compatibilidade com CSV
    G = nx.relabel_nodes(G, lambda x: str(x))
    return G

def parse_args():
    p = argparse.ArgumentParser(description="Pré-calcula distâncias (A*) e salva em CSV.")
    p.add_argument("--graph", default=DEFAULT_GRAPH, help="Caminho do grafo (JSON).")
    p.add_argument("--out", default=OUT, help="Caminho do distances.csv de saída.")
    p.add_argument("--k", type=int, default=20, dest="k_sample", help="Quantidade de nós da amostra (se nodes não for passado).")
    p.add_argument("--seed", type=int, default=None, help="Semente para amostragem determinística.")
    p.add_argument("--no-resume", action="store_false", help="Ignora o CSV existente.")
    #opicional: permitir lista fixa de nós via arquivo texto (um id por linha)
    p.add_argument("--nodes-file", default=None, help="Arquivo com IDs de nós (um por linha). Se passado, ignora --k/--seed.")
    return p.parse_args()

def load_nodes_from_file(path: str):
    def coerce(s: str):
        s = s.strip()
        # tenta converter para int se for numérico
        return int(s) if s.lstrip("-").isdigit() else s
    with open(path, "r", encoding="utf-8") as f:
        return [coerce(line) for line in f if line.strip()]

def main():
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    
    G = load_graph(args.graph)

    # Define o conjunto de nós e pré-computar
    if args.nodes_file:
        nodes = load_nodes_from_file(args.nodes_file)
        logging.info(f"Usando %d nós do arquivo: %s", len(nodes), args.nodes_file)
        k_sample = None # não usado/ignora k_sample
    else:
        nodes = None
        k_sample = args.k_sample
        if args.seed is not None:
            random.seed(args.seed) # deixa amostra reprodutivel

    # Chama sua função de pré-cálculo
    new_lines = precompute_distances(
        G,
        nodes=nodes,        # None => a função/suporte faz amostra de k_sample nós
        k_sample=k_sample,  # 20 por padrão
        out_path=args.out,  # CSV
        resume= not args.no_resume  # Reaproveita cache se existir
    )
    print(f"Novas linhas escritas: {new_lines}")
    print(f"Arquivo CSV gerado: {args.out}")

if __name__ == "__main__":
    main()
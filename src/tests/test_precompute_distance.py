import os
import pytest
from src.tools.run_precompute import load_graph
from src.algorithms import precompute_distances

OUT_PATH = "data/test_distances.csv"

def test_precomute_distante_creates_file():
    """Testa se o precumpute gera um CSV com distâncias"""
    G = load_graph("data/graph.json")
    if os.path.exists(OUT_PATH):
        os.remove(OUT_PATH)

    lines_written = precompute_distances(G, k_sample=5, out_path=OUT_PATH, resume=False)
    assert lines_written > 0
    assert os.path.exists(OUT_PATH)

def test_precompute_resume():
    """Testa se o precumpute resspeita cache (resume=True)"""
    G = load_graph("data/graph.json")
    before_size = os.path.getsize(OUT_PATH)

    lines_written = precompute_distances(G, k_sample=5, out_path=OUT_PATH, resume=True)
    after_size = os.path.getsize(OUT_PATH)

    #Como o arquivo já existe, não deve crescer muito (pode crescer se houver pares novos)
    assert lines_written >= 0
    assert after_size >= before_size

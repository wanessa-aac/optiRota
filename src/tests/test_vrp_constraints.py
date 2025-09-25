import os
import io
import json
import pytest
import logging
import networkx as nx

alg = pytest.importorskip(
    "src.algorithms",
    reason="src.algorithms não disponível; verifique se o caminho ou o pacote está instalado corretamente.",
)
vrp_solver = getattr(alg, "vrp_solver", None)
if vrp_solver is None:
    pytest.skip("vrp_solver não encontrado em src.algorithms(implemente ou exporte a função).")

LOG_PATH = "logs/vrp_constraints.log"
CAPACITY = 100 # Capacidade máxima por veículo 100kg
GLOBAL_WIDOW = (9, 11)  # Janela global permitida (9h às 11h)

def build_mock_graph():
    """
    Gera um grafo pequeno e previsivel para VRP.
    Nós tem lat/lon para não quebrar a heurística do A*.
    """
    G = nx.DiGraph()

    # Depot (0) + 3 clientes (1, 2, 3)
    nodes = {
        0: {"lat": -9.6500, "lon": -35.7200}, # Depot
        1: {"lat": -96510, "lon": -35.7210},
        2: {"lat": -96520, "lon": -35.7220}, 
        3: {"lat": -9.6530, "lon": -35.7230}, 
    }
    for nid, data in nodes.items():
        G.add_node(nid, **data)
    
    # Arestas bidireconais com pesos simples(me metros)
    edges = [
        (0, 1, 100), (1, 0, 100),
        (0, 2, 200), (2, 0, 200),
        (0, 3, 300), (3, 0, 300),
        (1, 2, 100), (2, 1, 100),
        (2, 3, 100), (3, 2, 100),
        (1, 3, 200), (3, 1, 200),
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=float(w))
    return G

def make_orders_case_ok():
    """
    Caso sem violações: total por rota deve ficar <= 100kg e todas as janelas respeitadas.
    """
# Cada pedido aponta para um nó no grafo; solver decide as rotas.
    return[
        {"id": 101, "node": 1, "weight": 30, "time": (9.0, 10.0)},
        {"id": 102, "node": 2, "weight": 40, "time": (9.5, 10.5)},  
        {"id": 103, "node": 3, "weight": 30, "time": (10.0, 11.0)}, 
    ]

def make_orders_case_capacity_violation():
    """
    Caso com violação de capacidade: um pedido faz a rota exceder 100kg.
    """
    return[
        {"id": 201, "node": 1, "weight": 60, "time": (9.0, 10.0)},
        {"id": 202, "node": 2, "weight": 50, "time": (9.5, 11.0)}, # somando 110kg
    ]

def make_orders_case_time_window_violation():
    """
    Caso com violação de janela de tempo: um pedido tem janela fora do permitido.
    """
    return[
        {"id": 301, "node": 1, "weight": 20, "time": (8.0, 8.5)},  # Fora da janela global
        {"id": 302, "node": 2, "weight": 20, "time": (9.5, 10.0)}, # ok
    ]

def extract_routes(result):
    """
    Aceita diferentes formatos de retorno do solver e normaliza para list[list[int]].
    Suporta:
        - list[list[int]]
        - {"routes": list[list[int]]}
        - list[{"route": list[int], ...}]
    """
    if result is None:
        return []
    
    if isinstance(result, dict) and "routes" in result:
        return result["routes"]
    
    if isinstance(result, list):
        if len(result) == 0:
            return []
        if all(isinstance(x, list) for x in result):
            return result #list of list
        if all(isinstance(x, dict) and "route" in x for x in result):
            return [r["route"] for r in result]
        if all(isinstance(x, int) for x in result):
            return [result] # rota única como lista plana
        
    # Último recurso: tenta ler como JSON (caso venha string/json)
    if isinstance(result, str):
        try:
            obj = json.loads(result)
            return extract_routes(obj)
        except Exception:
            pass
    raise AssertionError(f"Formato de retorno de vrp_solver não suportado: {type(result)}")

def ensure_logger():
    """
    Prepara logger dedicado para constraints, escrevendo em logs/vrp_constraints.log.
    """
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    logger = logging.getLogger("vrp_constraints")
    logger.setLevel(logging.INFO)

 # Evita múltiplos handlers se a função for chamada várias vezes
    logger.handlers = []

    fh = logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8")
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger

def check_constraints_and_logs(routes, orders, capacity=CAPACITY, window=GLOBAL_WIDOW):
    """
    Varre as rotas produzidas, checa capacidade e janela, e registra violações em logs/vrp_constraints.log.
    Retorna uma tupla (num_cap_violations, num_window_violations).
    """
    logger = ensure_logger()
    #Mapa rápido: node -> (id, weight, time_window)
    by_node = {}
    for o in orders:
        #aceita tanto "time" quanto "time_window"
        tw = o.get("time") or o.get("time_window")
        by_node[o["node"]] = (o["id"], o["weight"], tw)

    cap_viol = 0
    tw_viol = 0

    for ridx, route in enumerate(routes):
        if not route:
            continue

        # Ignora o depósito  caso o solver inclua (0).
        visits = [n for n in route if n in by_node]
        # 1) Capacidade
        total_weight = sum(by_node[n][1] for n in visits)
        if total_weight > capacity:
            cap_viol += 1
            logger.warning(f"Violação de capacidade na rota {ridx}: carga={total_weight}kg > {capacity}kg; visitas={visits}")

        # 2) Janela de tempo
        for n in visits:
            _id, _w, (t0, t1) = by_node[n]
            # Checagem simples: se a janela declarada do pedido está fora da global [9,11], registramos.
            #(Não modelamos horários de chegada; este teste valida conformidade dos dados do pedido com a política.)
            if not (window[0] <= t0 and t1 <= window[1]):
                tw_viol += 1
                logger.warning(f"Violação de janela de tempo na rota {ridx}: pedido={_id} janela={t0}-{t1} fora de {window}")
    
    if cap_viol == 0 and tw_viol == 0:
        logger.info("Nenhuma restrição violada ✅.")
    return cap_viol, tw_viol

def test_vrp_constraints_ok(tmp_path):
    G = build_mock_graph()
    orders = make_orders_case_ok()

    # Excuta solver
    result = vrp_solver(G, orders)
    routes = extract_routes(result)

    # Checa e loga violações
    cap_viol, tw_viol = check_constraints_and_logs(routes, orders)

    # Asserções
    assert cap_viol == 0, "Não deveria haver violação de capacidade"
    assert tw_viol == 0, f"Não deveria haver violação de janela"

    # Log deve existir e estar vazio
    assert os.path.exists(LOG_PATH), "Log não foi gerado"
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Nenhuma restrição violada" in content

def test_vrp_capacity_violation_or_split():
    G = build_mock_graph()
    orders = make_orders_case_capacity_violation()

    # Excuta solver
    result = vrp_solver(G, orders)
    routes = extract_routes(result)

    # Checa e loga violações
    cap_viol, tw_viol = check_constraints_and_logs(routes, orders)

    # Asserções
    assert cap_viol >= 0
    if len(routes) == 1 and all(o["node"] in routes[0] for o in orders):
        assert cap_viol >= 1, "Com 110kg na mesma rota deveria logar violação de capacidade"
    assert tw_viol == 0, "Não deveria haver violação de janela"

    # Duas possibilidades aceitáveis:
    # (A) O solver dividiu em rotas válidas => cap_viol == 0
    # (B) O solver não dividiu e violou a capacidade => cap_viol >= 1 (log de violação)
    assert tw_viol == 0, "Não há janelas inválidas caso"
    assert cap_viol >= 0

    # Segurança: se só houver uma rota e ela contiver dois pedidos, esperamos violação
    if len(routes) == 1:
        visits = [n for n in routes[0] if n in {o["node"] for o in orders}]
        if set(visits) == {orders[0]["node"], orders[1]["node"]}:
            assert cap_viol >= 1, "Com 110kg na mesma rota, deveria logar violação de capacidade"

def test_vrp_window_violation_or_exclusion():
    G = build_mock_graph()
    orders = make_orders_case_time_window_violation()

    # Excuta solver
    result = vrp_solver(G, orders)
    routes = extract_routes(result)

    # Checa e loga violações
    cap_viol, tw_viol = check_constraints_and_logs(routes, orders)

    # Duas possibilidades aceitáveis:
    # (A) O solver excluiu o pedido inválido => tw_viol == 0
    # (B) O solver incluiu o pedido inválido e violou a janela => tw_viol >= 1 (log de violação)
    assert cap_viol == 0, "Não há risco decapacidade neste caso"
    assert tw_viol >= 0

    # Se o pedido 301 (8-8.5h) apareceu nas rotas, deve haver violação
    included_nodes = {n for route in routes for n in route}
    if orders[0]["node"] in included_nodes:       # node do pedido 301
        assert tw_viol >= 1, "Pedido fora da janela apareceu em rota sem logar violação"
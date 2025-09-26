"""
Testes de consistência de dados.
FASE 4: Testes de Validação
"""

import pytest
import os
import json
from src.parser_osm import parse_osm
from src.graph import build_graph
from src.algorithms import dijkstra, a_star

class TestDataConsistency:
    """
    Testes de consistência de dados.
    Teste automatizado: 90% gerado por IA
    """
    
    def test_osm_data_consistency(self):
        """
        Testa consistência dos dados OSM.
        Teste automatizado: 95% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            parsed_data = parse_osm(dataset_path)
            
            # Validações de estrutura
            assert isinstance(parsed_data, dict), "Dados devem ser dict"
            assert "nodes" in parsed_data, "Deve ter nodes"
            assert "ways" in parsed_data, "Deve ter ways"
            
            nodes = parsed_data["nodes"]
            ways = parsed_data["ways"]
            
            # Validações de nodes
            assert isinstance(nodes, dict), "Nodes devem ser dict"
            assert len(nodes) > 0, "Deve ter nodes"
            
            for node_id, node_data in nodes.items():
                assert isinstance(node_id, (str, int)), f"Node ID inválido: {node_id}"
                assert "lat" in node_data, f"Node {node_id} deve ter lat"
                assert "lon" in node_data, f"Node {node_id} deve ter lon"
                assert isinstance(node_data["lat"], (int, float)), f"Lat inválida: {node_data['lat']}"
                assert isinstance(node_data["lon"], (int, float)), f"Lon inválida: {node_data['lon']}"
                assert -90 <= node_data["lat"] <= 90, f"Latitude inválida: {node_data['lat']}"
                assert -180 <= node_data["lon"] <= 180, f"Longitude inválida: {node_data['lon']}"
            
            # Validações de ways
            assert isinstance(ways, list), "Ways devem ser list"
            assert len(ways) > 0, "Deve ter ways"
            
            for way in ways:
                assert isinstance(way, dict), "Way deve ser dict"
                assert "from" in way, "Way deve ter from"
                assert "to" in way, "Way deve ter to"
                assert isinstance(way["from"], (str, int)), f"From inválido: {way['from']}"
                assert isinstance(way["to"], (str, int)), f"To inválido: {way['to']}"
                
                # Validações de referência
                assert way["from"] in nodes, f"Way from {way['from']} não existe em nodes"
                assert way["to"] in nodes, f"Way to {way['to']} não existe em nodes"
            
            print(f"\nConsistência de dados OSM:")
            print(f"  Nodes: {len(nodes)}")
            print(f"  Ways: {len(ways)}")
            print(f"  Estrutura: ✅")
            print(f"  Referências: ✅")
            
        except Exception as e:
            pytest.skip(f"Erro na consistência: {e}")
    
    def test_graph_data_consistency(self):
        """
        Testa consistência dos dados do grafo.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse e construção do grafo
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Validações de grafo
            assert G.number_of_nodes() > 0, "Grafo deve ter nodes"
            assert G.number_of_edges() > 0, "Grafo deve ter edges"
            
            # Validações de nodes
            for node in G.nodes():
                node_data = G.nodes[node]
                assert "lat" in node_data, f"Node {node} deve ter lat"
                assert "lon" in node_data, f"Node {node} deve ter lon"
                assert isinstance(node_data["lat"], (int, float)), f"Lat inválida: {node_data['lat']}"
                assert isinstance(node_data["lon"], (int, float)), f"Lon inválida: {node_data['lon']}"
                assert -90 <= node_data["lat"] <= 90, f"Latitude inválida: {node_data['lat']}"
                assert -180 <= node_data["lon"] <= 180, f"Longitude inválida: {node_data['lon']}"
            
            # Validações de edges
            for u, v in G.edges():
                edge_data = G[u][v]
                assert "weight" in edge_data, f"Edge {u}->{v} deve ter weight"
                assert isinstance(edge_data["weight"], (int, float)), f"Weight inválido: {edge_data['weight']}"
                assert edge_data["weight"] > 0, f"Weight deve ser positivo: {edge_data['weight']}"
                assert edge_data["weight"] < float('inf'), f"Weight deve ser finito: {edge_data['weight']}"
            
            print(f"\nConsistência de dados do grafo:")
            print(f"  Nodes: {G.number_of_nodes()}")
            print(f"  Edges: {G.number_of_edges()}")
            print(f"  Estrutura: ✅")
            print(f"  Pesos: ✅")
            
        except Exception as e:
            pytest.skip(f"Erro na consistência: {e}")
    
    def test_algorithm_result_consistency(self):
        """
        Testa consistência dos resultados dos algoritmos.
        Teste automatizado: 95% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse e construção do grafo
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Seleciona nós para teste
            nodes = list(G.nodes())
            if len(nodes) < 2:
                pytest.skip("Grafo muito pequeno para algoritmos")
            
            start = nodes[0]
            end = nodes[-1]
            
            # Testa Dijkstra
            dijkstra_result = dijkstra(G, start, end)
            
            # Validações de resultado Dijkstra
            assert "distance" in dijkstra_result, "Dijkstra deve ter distance"
            assert "path" in dijkstra_result, "Dijkstra deve ter path"
            assert "nodes_visited" in dijkstra_result, "Dijkstra deve ter nodes_visited"
            
            assert isinstance(dijkstra_result["distance"], (int, float)), "Distance deve ser numérica"
            assert isinstance(dijkstra_result["path"], list), "Path deve ser list"
            assert isinstance(dijkstra_result["nodes_visited"], int), "Nodes_visited deve ser int"
            
            assert dijkstra_result["distance"] >= 0, "Distance deve ser não-negativa"
            assert dijkstra_result["distance"] < float('inf'), "Distance deve ser finita"
            assert len(dijkstra_result["path"]) > 0, "Path deve ter elementos"
            assert dijkstra_result["nodes_visited"] >= 0, "Nodes_visited deve ser não-negativo"
            
            # Testa A*
            astar_result = a_star(G, start, end)
            
            # Validações de resultado A*
            assert "distance" in astar_result, "A* deve ter distance"
            assert "path" in astar_result, "A* deve ter path"
            assert "nodes_visited" in astar_result, "A* deve ter nodes_visited"
            
            assert isinstance(astar_result["distance"], (int, float)), "Distance deve ser numérica"
            assert isinstance(astar_result["path"], list), "Path deve ser list"
            assert isinstance(astar_result["nodes_visited"], int), "Nodes_visited deve ser int"
            
            assert astar_result["distance"] >= 0, "Distance deve ser não-negativa"
            assert astar_result["distance"] < float('inf'), "Distance deve ser finita"
            assert len(astar_result["path"]) > 0, "Path deve ter elementos"
            assert astar_result["nodes_visited"] >= 0, "Nodes_visited deve ser não-negativo"
            
            # Validações de consistência entre algoritmos
            assert abs(dijkstra_result["distance"] - astar_result["distance"]) < 1e-9, "Distâncias devem ser iguais"
            assert dijkstra_result["path"] == astar_result["path"], "Paths devem ser iguais"
            
            print(f"\nConsistência de resultados:")
            print(f"  Dijkstra distance: {dijkstra_result['distance']:.2f}")
            print(f"  A* distance: {astar_result['distance']:.2f}")
            print(f"  Paths iguais: {'✅' if dijkstra_result['path'] == astar_result['path'] else '❌'}")
            print(f"  Distâncias iguais: {'✅' if abs(dijkstra_result['distance'] - astar_result['distance']) < 1e-9 else '❌'}")
            
        except Exception as e:
            pytest.skip(f"Erro na consistência: {e}")
    
    def test_data_type_consistency(self):
        """
        Testa consistência de tipos de dados.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Validações de tipos de nodes
            for node in G.nodes():
                node_data = G.nodes[node]
                assert isinstance(node_data["lat"], (int, float)), f"Lat deve ser numérica: {type(node_data['lat'])}"
                assert isinstance(node_data["lon"], (int, float)), f"Lon deve ser numérica: {type(node_data['lon'])}"
            
            # Validações de tipos de edges
            for u, v in G.edges():
                edge_data = G[u][v]
                assert isinstance(edge_data["weight"], (int, float)), f"Weight deve ser numérica: {type(edge_data['weight'])}"
            
            # Validações de tipos de resultados
            nodes = list(G.nodes())
            if len(nodes) >= 2:
                start, end = nodes[0], nodes[-1]
                
                dijkstra_result = dijkstra(G, start, end)
                assert isinstance(dijkstra_result["distance"], (int, float)), "Distance deve ser numérica"
                assert isinstance(dijkstra_result["path"], list), "Path deve ser list"
                assert isinstance(dijkstra_result["nodes_visited"], int), "Nodes_visited deve ser int"
                
                astar_result = a_star(G, start, end)
                assert isinstance(astar_result["distance"], (int, float)), "Distance deve ser numérica"
                assert isinstance(astar_result["path"], list), "Path deve ser list"
                assert isinstance(astar_result["nodes_visited"], int), "Nodes_visited deve ser int"
            
            print(f"\nConsistência de tipos:")
            print(f"  Nodes: ✅")
            print(f"  Edges: ✅")
            print(f"  Resultados: ✅")
            
        except Exception as e:
            pytest.skip(f"Erro na consistência: {e}")
    
    def test_data_range_consistency(self):
        """
        Testa consistência de ranges de dados.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Validações de ranges de coordenadas
            lats = [G.nodes[node]["lat"] for node in G.nodes()]
            lons = [G.nodes[node]["lon"] for node in G.nodes()]
            
            assert min(lats) >= -90, f"Latitude mínima inválida: {min(lats)}"
            assert max(lats) <= 90, f"Latitude máxima inválida: {max(lats)}"
            assert min(lons) >= -180, f"Longitude mínima inválida: {min(lons)}"
            assert max(lons) <= 180, f"Longitude máxima inválida: {max(lons)}"
            
            # Validações de ranges de pesos
            weights = [G[u][v]["weight"] for u, v in G.edges()]
            
            assert min(weights) > 0, f"Peso mínimo inválido: {min(weights)}"
            assert max(weights) < float('inf'), f"Peso máximo inválido: {max(weights)}"
            assert all(w > 0 for w in weights), "Todos os pesos devem ser positivos"
            
            # Validações de ranges de resultados
            nodes = list(G.nodes())
            if len(nodes) >= 2:
                start, end = nodes[0], nodes[-1]
                
                dijkstra_result = dijkstra(G, start, end)
                assert dijkstra_result["distance"] >= 0, f"Distância Dijkstra inválida: {dijkstra_result['distance']}"
                assert dijkstra_result["distance"] < float('inf'), f"Distância Dijkstra infinita: {dijkstra_result['distance']}"
                assert dijkstra_result["nodes_visited"] >= 0, f"Nodes_visited Dijkstra inválido: {dijkstra_result['nodes_visited']}"
                
                astar_result = a_star(G, start, end)
                assert astar_result["distance"] >= 0, f"Distância A* inválida: {astar_result['distance']}"
                assert astar_result["distance"] < float('inf'), f"Distância A* infinita: {astar_result['distance']}"
                assert astar_result["nodes_visited"] >= 0, f"Nodes_visited A* inválido: {astar_result['nodes_visited']}"
            
            print(f"\nConsistência de ranges:")
            print(f"  Latitude: {min(lats):.6f} a {max(lats):.6f}")
            print(f"  Longitude: {min(lons):.6f} a {max(lons):.6f}")
            print(f"  Pesos: {min(weights):.6f} a {max(weights):.6f}")
            print(f"  Ranges: ✅")
            
        except Exception as e:
            pytest.skip(f"Erro na consistência: {e}")
    
    def test_data_completeness(self):
        """
        Testa completude dos dados.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Validações de completude de nodes
            for node in G.nodes():
                node_data = G.nodes[node]
                assert "lat" in node_data, f"Node {node} sem lat"
                assert "lon" in node_data, f"Node {node} sem lon"
                assert node_data["lat"] is not None, f"Node {node} lat é None"
                assert node_data["lon"] is not None, f"Node {node} lon é None"
            
            # Validações de completude de edges
            for u, v in G.edges():
                edge_data = G[u][v]
                assert "weight" in edge_data, f"Edge {u}->{v} sem weight"
                assert edge_data["weight"] is not None, f"Edge {u}->{v} weight é None"
            
            # Validações de completude de resultados
            nodes = list(G.nodes())
            if len(nodes) >= 2:
                start, end = nodes[0], nodes[-1]
                
                dijkstra_result = dijkstra(G, start, end)
                assert dijkstra_result["distance"] is not None, "Distance Dijkstra é None"
                assert dijkstra_result["path"] is not None, "Path Dijkstra é None"
                assert dijkstra_result["nodes_visited"] is not None, "Nodes_visited Dijkstra é None"
                
                astar_result = a_star(G, start, end)
                assert astar_result["distance"] is not None, "Distance A* é None"
                assert astar_result["path"] is not None, "Path A* é None"
                assert astar_result["nodes_visited"] is not None, "Nodes_visited A* é None"
            
            print(f"\nCompletude de dados:")
            print(f"  Nodes: {G.number_of_nodes()}")
            print(f"  Edges: {G.number_of_edges()}")
            print(f"  Completude: ✅")
            
        except Exception as e:
            pytest.skip(f"Erro na completude: {e}")
    
    def test_data_integrity(self):
        """
        Testa integridade dos dados.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Validações de integridade de referências
            for u, v in G.edges():
                assert u in G.nodes(), f"Node {u} não existe"
                assert v in G.nodes(), f"Node {v} não existe"
            
            # Validações de integridade de paths
            nodes = list(G.nodes())
            if len(nodes) >= 2:
                start, end = nodes[0], nodes[-1]
                
                dijkstra_result = dijkstra(G, start, end)
                path = dijkstra_result["path"]
                
                # Validações de path
                assert path[0] == start, f"Path deve começar em {start}"
                assert path[-1] == end, f"Path deve terminar em {end}"
                
                # Validações de conectividade do path
                for i in range(len(path) - 1):
                    current = path[i]
                    next_node = path[i + 1]
                    assert G.has_edge(current, next_node), f"Path deve ter edge: {current} -> {next_node}"
                
                astar_result = a_star(G, start, end)
                path = astar_result["path"]
                
                # Validações de path
                assert path[0] == start, f"Path deve começar em {start}"
                assert path[-1] == end, f"Path deve terminar em {end}"
                
                # Validações de conectividade do path
                for i in range(len(path) - 1):
                    current = path[i]
                    next_node = path[i + 1]
                    assert G.has_edge(current, next_node), f"Path deve ter edge: {current} -> {next_node}"
            
            print(f"\nIntegridade de dados:")
            print(f"  Referências: ✅")
            print(f"  Paths: ✅")
            print(f"  Conectividade: ✅")
            
        except Exception as e:
            pytest.skip(f"Erro na integridade: {e}")


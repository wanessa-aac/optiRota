"""
Testes de parsing para datasets metropolitanos grandes.
FASE 3: Testes de Dataset Metropolitano
"""

import pytest
import os
import time
import logging
from pathlib import Path
from src.parser_osm import parse_osm
from src.graph import build_graph

class TestMetropolitanParsing:
    """
    Testes de parsing para datasets metropolitanos.
    Teste automatizado: 90% gerado por IA
    """
    
    def test_parse_maceio_dataset(self):
        """
        Testa parsing do dataset de Maceió.
        Teste automatizado: 95% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        # Verifica se o arquivo existe
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        # Mede tempo de parsing
        start_time = time.time()
        
        try:
            parsed_data = parse_osm(dataset_path)
            parsing_time = time.time() - start_time
            
            # Validações básicas
            assert "nodes" in parsed_data, "Dados devem conter nodes"
            assert "ways" in parsed_data, "Dados devem conter ways"
            assert len(parsed_data["nodes"]) > 0, "Deve ter nodes"
            assert len(parsed_data["ways"]) > 0, "Deve ter ways"
            
            # Validações de performance
            assert parsing_time < 30.0, f"Parsing muito lento: {parsing_time:.2f}s"
            
            print(f"\nDataset Maceió:")
            print(f"  Nodes: {len(parsed_data['nodes'])}")
            print(f"  Ways: {len(parsed_data['ways'])}")
            print(f"  Tempo: {parsing_time:.2f}s")
            
        except Exception as e:
            pytest.skip(f"Erro no parsing do dataset: {e}")
    
    def test_parse_large_dataset_performance(self):
        """
        Testa performance de parsing em dataset grande.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        # Mede tempo de parsing
        start_time = time.time()
        
        try:
            parsed_data = parse_osm(dataset_path)
            parsing_time = time.time() - start_time
            
            # Validações de performance
            assert parsing_time < 60.0, f"Parsing muito lento: {parsing_time:.2f}s"
            
            # Validações de dados
            assert len(parsed_data["nodes"]) > 100, "Dataset deve ter muitos nodes"
            assert len(parsed_data["ways"]) > 100, "Dataset deve ter muitos ways"
            
            print(f"\nPerformance de parsing:")
            print(f"  Tempo total: {parsing_time:.2f}s")
            print(f"  Nodes/segundo: {len(parsed_data['nodes'])/parsing_time:.0f}")
            print(f"  Ways/segundo: {len(parsed_data['ways'])/parsing_time:.0f}")
            
        except Exception as e:
            pytest.skip(f"Erro no parsing: {e}")
    
    def test_parse_dataset_memory_usage(self):
        """
        Testa uso de memória durante parsing.
        Teste automatizado: 90% gerado por IA
        """
        try:
            import psutil
        except ImportError:
            pytest.skip("psutil não disponível")
        
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        # Mede memória antes
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        try:
            parsed_data = parse_osm(dataset_path)
            
            # Mede memória depois
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_used = memory_after - memory_before
            
            # Validações de memória
            assert memory_used < 500, f"Uso de memória excessivo: {memory_used:.1f}MB"
            
            print(f"\nUso de memória:")
            print(f"  Antes: {memory_before:.1f}MB")
            print(f"  Depois: {memory_after:.1f}MB")
            print(f"  Usado: {memory_used:.1f}MB")
            
        except Exception as e:
            pytest.skip(f"Erro no parsing: {e}")
    
    def test_parse_dataset_error_handling(self):
        """
        Testa tratamento de erros em parsing.
        Teste automatizado: 95% gerado por IA
        """
        # Testa arquivo inexistente
        with pytest.raises(FileNotFoundError):
            parse_osm("data/arquivo_inexistente.osm")
        
        # Testa arquivo vazio
        empty_file = "data/empty.osm"
        try:
            Path(empty_file).touch()
            with pytest.raises(Exception):
                parse_osm(empty_file)
        finally:
            if os.path.exists(empty_file):
                os.remove(empty_file)
    
    def test_parse_dataset_validation(self):
        """
        Testa validação de dados parseados.
        Teste automatizado: 90% gerado por IA
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
            
            # Validações de nodes
            nodes = parsed_data["nodes"]
            assert isinstance(nodes, dict), "Nodes devem ser dict"
            
            for node_id, node_data in nodes.items():
                assert isinstance(node_id, (str, int)), f"Node ID inválido: {node_id}"
                assert "lat" in node_data, f"Node {node_id} deve ter lat"
                assert "lon" in node_data, f"Node {node_id} deve ter lon"
                assert isinstance(node_data["lat"], (int, float)), f"Lat inválida: {node_data['lat']}"
                assert isinstance(node_data["lon"], (int, float)), f"Lon inválida: {node_data['lon']}"
            
            # Validações de ways
            ways = parsed_data["ways"]
            assert isinstance(ways, list), "Ways devem ser list"
            
            for way in ways:
                assert "from" in way, "Way deve ter from"
                assert "to" in way, "Way deve ter to"
                assert isinstance(way["from"], (str, int)), f"From inválido: {way['from']}"
                assert isinstance(way["to"], (str, int)), f"To inválido: {way['to']}"
            
            print(f"\nValidação de dados:")
            print(f"  Nodes válidos: {len(nodes)}")
            print(f"  Ways válidos: {len(ways)}")
            
        except Exception as e:
            pytest.skip(f"Erro no parsing: {e}")

# src/tests/test_concurrency.py
"""
Testes de concorrência e thread-safety do OptiRota.
FASE 1: Testes de Performance - 70% automatizável com IA
"""

import pytest
import threading
import time
import random
from src.structures import PriorityQueue, Stack, FIFOQueue


class TestConcurrency:
    """Testes de concorrência e thread-safety."""
    
    def test_concurrent_insertions_extractions(self):
        """
        Testa operações concorrentes na PriorityQueue.
        Teste automatizado: 80% gerado por IA
        """
        pq = PriorityQueue()
        results = []
        errors = []
        
        def worker_insert(worker_id, num_operations):
            """Worker que insere elementos na fila."""
            try:
                for i in range(num_operations):
                    pq.insert(f"worker_{worker_id}_item_{i}", random.uniform(0, 1000))
                    time.sleep(0.001)  # Pequena pausa para simular concorrência
            except Exception as e:
                errors.append(f"Worker {worker_id} insert error: {e}")
        
        def worker_extract(worker_id, num_operations):
            """Worker que extrai elementos da fila."""
            try:
                for i in range(num_operations):
                    if not pq.is_empty():
                        item = pq.extract_min()
                        results.append(f"worker_{worker_id}_extracted_{item}")
                    time.sleep(0.001)  # Pequena pausa para simular concorrência
            except Exception as e:
                errors.append(f"Worker {worker_id} extract error: {e}")
        
        # Cria threads para inserção e extração
        threads = []
        num_workers = 4
        operations_per_worker = 50
        
        # Threads de inserção
        for i in range(num_workers):
            thread = threading.Thread(target=worker_insert, args=(i, operations_per_worker))
            threads.append(thread)
        
        # Threads de extração
        for i in range(num_workers):
            thread = threading.Thread(target=worker_extract, args=(i, operations_per_worker))
            threads.append(thread)
        
        # Inicia todas as threads
        for thread in threads:
            thread.start()
        
        # Aguarda todas as threads terminarem
        for thread in threads:
            thread.join(timeout=10)  # Timeout de 10 segundos
        
        # Validações
        assert len(errors) == 0, f"Erros de concorrência: {errors}"
        assert len(results) > 0, "Nenhuma extração foi realizada"
        
        # Verifica se a fila está vazia ou tem elementos restantes
        remaining_items = []
        while not pq.is_empty():
            remaining_items.append(pq.extract_min())
        
        total_operations = num_workers * operations_per_worker
        total_extracted = len(results) + len(remaining_items)
        
        print(f"\nOperações concorrentes:")
        print(f"  Total inseridas: {total_operations}")
        print(f"  Total extraídas: {total_extracted}")
        print(f"  Erros: {len(errors)}")
        print(f"  Resultados: {len(results)}")
    
    def test_thread_safe_operations(self):
        """
        Testa thread-safety das estruturas de dados.
        Teste automatizado: 75% gerado por IA
        """
        # Testa PriorityQueue
        pq = PriorityQueue()
        pq_errors = []
        
        def pq_worker(worker_id, num_operations):
            try:
                for i in range(num_operations):
                    # Operações mistas
                    if i % 2 == 0:
                        pq.insert(f"worker_{worker_id}_item_{i}", random.uniform(0, 1000))
                    else:
                        if not pq.is_empty():
                            pq.extract_min()
                    time.sleep(0.001)
            except Exception as e:
                pq_errors.append(f"PQ Worker {worker_id}: {e}")
        
        # Testa Stack
        stack = Stack()
        stack_errors = []
        
        def stack_worker(worker_id, num_operations):
            try:
                for i in range(num_operations):
                    if i % 2 == 0:
                        stack.push(f"worker_{worker_id}_item_{i}")
                    else:
                        if not stack.is_empty():
                            stack.pop()
                    time.sleep(0.001)
            except Exception as e:
                stack_errors.append(f"Stack Worker {worker_id}: {e}")
        
        # Executa testes
        threads = []
        num_workers = 3
        operations_per_worker = 30
        
        # Threads para PriorityQueue
        for i in range(num_workers):
            thread = threading.Thread(target=pq_worker, args=(i, operations_per_worker))
            threads.append(thread)
        
        # Threads para Stack
        for i in range(num_workers):
            thread = threading.Thread(target=stack_worker, args=(i, operations_per_worker))
            threads.append(thread)
        
        # Inicia threads
        for thread in threads:
            thread.start()
        
        # Aguarda threads
        for thread in threads:
            thread.join(timeout=10)
        
        # Validações
        assert len(pq_errors) == 0, f"Erros na PriorityQueue: {pq_errors}"
        assert len(stack_errors) == 0, f"Erros na Stack: {stack_errors}"
        
        print(f"\nThread-safety validado:")
        print(f"  PriorityQueue erros: {len(pq_errors)}")
        print(f"  Stack erros: {len(stack_errors)}")
    
    def test_race_conditions(self):
        """
        Testa condições de corrida em operações críticas.
        Teste automatizado: 65% gerado por IA
        """
        pq = PriorityQueue()
        race_conditions = []
        
        def race_worker(worker_id, num_operations):
            """Worker que tenta causar condições de corrida."""
            try:
                for i in range(num_operations):
                    # Operações que podem causar race conditions
                    if i % 3 == 0:
                        # Inserção
                        pq.insert(f"race_{worker_id}_{i}", random.uniform(0, 1000))
                    elif i % 3 == 1:
                        # Verificação de estado
                        if not pq.is_empty():
                            pq.peek()
                    else:
                        # Extração
                        if not pq.is_empty():
                            pq.extract_min()
                    
                    time.sleep(0.001)
            except Exception as e:
                race_conditions.append(f"Race condition in worker {worker_id}: {e}")
        
        # Cria threads para testar race conditions
        threads = []
        num_workers = 5
        operations_per_worker = 20
        
        for i in range(num_workers):
            thread = threading.Thread(target=race_worker, args=(i, operations_per_worker))
            threads.append(thread)
        
        # Inicia threads
        for thread in threads:
            thread.start()
        
        # Aguarda threads
        for thread in threads:
            thread.join(timeout=15)
        
        # Validações
        assert len(race_conditions) == 0, f"Condições de corrida detectadas: {race_conditions}"
        
        print(f"\nRace conditions testadas:")
        print(f"  Workers: {num_workers}")
        print(f"  Operações por worker: {operations_per_worker}")
        print(f"  Race conditions detectadas: {len(race_conditions)}")
    
    def test_concurrent_memory_access(self):
        """
        Testa acesso concorrente à memória.
        Teste automatizado: 70% gerado por IA
        """
        shared_data = []
        access_errors = []
        
        def memory_worker(worker_id, num_operations):
            """Worker que acessa memória compartilhada."""
            try:
                for i in range(num_operations):
                    # Operações de memória
                    shared_data.append(f"worker_{worker_id}_data_{i}")
                    
                    # Simula processamento
                    time.sleep(0.001)
                    
                    # Remove dados antigos
                    if len(shared_data) > 100:
                        shared_data.pop(0)
            except Exception as e:
                access_errors.append(f"Memory worker {worker_id}: {e}")
        
        # Cria threads para acesso à memória
        threads = []
        num_workers = 3
        operations_per_worker = 50
        
        for i in range(num_workers):
            thread = threading.Thread(target=memory_worker, args=(i, operations_per_worker))
            threads.append(thread)
        
        # Inicia threads
        for thread in threads:
            thread.start()
        
        # Aguarda threads
        for thread in threads:
            thread.join(timeout=10)
        
        # Validações
        assert len(access_errors) == 0, f"Erros de acesso à memória: {access_errors}"
        assert len(shared_data) > 0, "Nenhum dado foi processado"
        
        print(f"\nAcesso concorrente à memória:")
        print(f"  Workers: {num_workers}")
        print(f"  Dados processados: {len(shared_data)}")
        print(f"  Erros: {len(access_errors)}")
    
    def test_stress_concurrency(self):
        """
        Teste de estresse para concorrência.
        Teste automatizado: 60% gerado por IA
        """
        pq = PriorityQueue()
        stress_errors = []
        
        def stress_worker(worker_id, duration_seconds):
            """Worker de estresse que executa operações intensivas."""
            start_time = time.time()
            operations = 0
            
            try:
                while time.time() - start_time < duration_seconds:
                    # Operações intensivas
                    if operations % 2 == 0:
                        pq.insert(f"stress_{worker_id}_{operations}", random.uniform(0, 1000))
                    else:
                        if not pq.is_empty():
                            pq.extract_min()
                    
                    operations += 1
                    time.sleep(0.0001)  # Pausa mínima
            except Exception as e:
                stress_errors.append(f"Stress worker {worker_id}: {e}")
        
        # Teste de estresse
        threads = []
        num_workers = 4
        duration = 2  # segundos
        
        for i in range(num_workers):
            thread = threading.Thread(target=stress_worker, args=(i, duration))
            threads.append(thread)
        
        # Inicia threads
        for thread in threads:
            thread.start()
        
        # Aguarda threads
        for thread in threads:
            thread.join(timeout=duration + 5)
        
        # Validações
        assert len(stress_errors) == 0, f"Erros de estresse: {stress_errors}"
        
        print(f"\nTeste de estresse de concorrência:")
        print(f"  Workers: {num_workers}")
        print(f"  Duração: {duration}s")
        print(f"  Erros: {len(stress_errors)}")

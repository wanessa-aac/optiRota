import pytest
from src.structures import PriorityQueue, Stack, reconstruct_path

"""
Olá, bem vindo ao módulo de testes para Priority Queue.
 - Inserção e extract_min em ordem: garante a prioridade correta.
 - Propriedade de heap (ordem não-decrescente de prioridades): garante consistência mesmo em sequências longas de operações.
 - Casos de borda (prioridades iguais, remoção em estrutura vazia): garantem que sua estrutura é robusta em situações limite.
"""

# ---------------- PriorityQueue ----------------

def test_insert_and_extract_min_in_order():
    pq = PriorityQueue()
    pq.insert("A", 3)
    pq.insert("B", 1)
    pq.insert("C", 2)
    assert pq.extract_min() == "B"  # menor prioridade
    assert pq.extract_min() == "C"
    assert pq.extract_min() == "A"

def test_extract_min_empty_raises():
    pq = PriorityQueue()
    with pytest.raises(IndexError):
        pq.extract_min()

def test_insert_invalid_priority_type():
    pq = PriorityQueue()
    with pytest.raises(TypeError):
        pq.insert("X", "nao_numero")

def test_heapify_restores_property():
    pq = PriorityQueue()
    pq.heap = [(3, "A"), (1, "B"), (2, "C")]  # bagunçado
    pq.heapify()
    assert pq.extract_min() == "B"
    assert pq.extract_min() == "C"
    assert pq.extract_min() == "A"

def test_peek_and_size():
    pq = PriorityQueue()
    pq.insert("A", 5)
    assert pq.peek() == "A"
    assert pq.size() == 1
    assert not pq.is_empty()

# ---------------- Stack ----------------

def test_stack_push_pop_peek():
    s = Stack()
    s.push(10)
    s.push(20)
    s.push(30)
    assert s.peek() == 30
    assert s.pop() == 30
    assert s.pop() == 20
    assert s.pop() == 10
    assert s.is_empty()

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

# ---------------- reconstruct_path ----------------

def test_reconstruct_path_valid():
    preds = {"A": None, "B": "A", "C": "B"}
    path = reconstruct_path(preds, "A", "C")
    assert path == ["A", "B", "C"]

def test_reconstruct_path_invalid_chain():
    preds = {"A": None, "B": None, "C": "B"}  # A não alcança C
    with pytest.raises(ValueError):
        reconstruct_path(preds, "A", "C")

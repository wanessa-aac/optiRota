import pytest

alg = pytest.importorskip("src.structures", reason = "src.structures não disponível ou não encontrado(verifique os requisitos).")
PriorityQueue = getattr(alg, "PriorityQueue")
Stack = getattr(alg, "Stack")
FIFOQueue = getattr(alg, "FIFOQueue")
reconstruct_path = getattr(alg, "reconstruct_path")

def test_priority_queue_basic_ops():
    pq = PriorityQueue()
    pq.insert("a", 5); pq.insert("b", 1); pq.insert("c", 3)
    assert pq.peek() == "b"
    assert pq.extract_min() == "b"
    assert pq.extract_min() == "c"
    assert pq.extract_min() == "a"
    assert pq.is_empty() and pq.size() == 0

def test_stack_ops_and_errors():
    s = Stack()
    s.push(1); s.push(2)
    assert s.peek() == 2
    assert s.pop() == 2
    assert s.pop() == 1
    with pytest.raises(IndexError):
        s.pop()
    
def test_fifo_queue_ops():
    q = FIFOQueue()
    q.enqueue("x"); q.enqueue("y")
    assert not q.is_empty() and q.size() == 2
    assert q.dequeue() == "x"
    assert q.dequeue() == "y"
    assert q.is_empty()

def test_reconstruct_path_valid_and_invalid():
    preds = {"A": None, "B": "A", "C": "B"}
    assert reconstruct_path(preds, "A", "C") == ["A", "B", "C"]
    bad = {"A": None, "B": None}
    with pytest.raises(ValueError):
        reconstruct_path(bad, "A", "B")
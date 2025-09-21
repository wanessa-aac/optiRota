import heapq
import logging
import time
import queue
import threading
from typing import Generic, List, Optional, TypeVar, Dict

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PriorityQueue:
    """
    Implementação de uma fila de prioridade usando heap binário.
    
    Características:
    - Inserção e extração em O(log n)
    - Usa tuplas (prioridade, valor) no heap
    - Método heapify() interno para manutenção da propriedade de heap
    - Logging para depuração
    
    Exemplo de uso:
        pq = PriorityQueue()
        pq.insert(10, 1.0)  # valor=10, prioridade=1.0
        pq.insert(20, 0.5)  # valor=20, prioridade=0.5
        value = pq.extract_min()  # retorna 20 (menor prioridade)
    """
    
    def __init__(self):
        """
        Inicializa uma fila de prioridade vazia.
        
        O heap é implementado como uma lista de tuplas (prioridade, valor).
        """
        self.heap = []
        logging.info("PriorityQueue inicializada")
    
    def insert(self, value, priority):
        """
        Insere um valor na fila com a prioridade especificada.
        
        Complexidade: O(log n)
        
        Args:
            value: O valor a ser inserido
            priority: A prioridade do valor (menor valor = maior prioridade)
        """
        start_time = time.time()
        
        # Validação de entrada
        if not isinstance(priority, (int, float)):
            logging.error("Prioridade deve ser numérica, recebido: %s", type(priority))
            raise TypeError(f"Prioridade deve ser numérica, recebido: {type(priority)}")
        
        # Insere tupla (prioridade, valor) no heap
        heapq.heappush(self.heap, (priority, value))
        
        # Logging para depuração
        elapsed = time.time() - start_time
        logging.info("Inserindo: %s com prioridade %s (tempo: %.6fs)", value, priority, elapsed)
        
        # Verifica propriedade de heap após inserção
        self._verify_heap_property()
    
    def extract_min(self):
        """
        Remove e retorna o valor com menor prioridade.
        
        Complexidade: O(log n)
        
        Returns:
            O valor com menor prioridade
            
        Raises:
            IndexError: Se a fila estiver vazia
        """
        start_time = time.time()
        
        if not self.heap:
            logging.warning("Tentativa de extract_min em PriorityQueue vazia")
            raise IndexError("extract_min from empty priority queue")
        
        # Extrai o elemento com menor prioridade
        priority, value = heapq.heappop(self.heap)
        
        # Logging para depuração
        elapsed = time.time() - start_time
        logging.info("Extraindo: %s com prioridade %s (tempo: %.6fs)", value, priority, elapsed)
        
        # Verifica propriedade de heap após extração
        self._verify_heap_property()
        
        return value
    
    def heapify(self):
        """
        Reconstrói o heap mantendo a propriedade de heap.
        
        Complexidade: O(n)
        
        Este método é chamado internamente quando necessário para garantir
        que a propriedade de heap seja mantida.
        """
        start_time = time.time()
        
        if not self.heap:
            logging.info("Heapify chamado em heap vazio")
            return
        
        # Reconstrói o heap usando heapq.heapify
        heapq.heapify(self.heap)
        
        elapsed = time.time() - start_time
        logging.info("Heapify executado em %d elementos (tempo: %.6fs)", len(self.heap), elapsed)
        
        # Verifica propriedade de heap após heapify
        self._verify_heap_property()
    
    def _verify_heap_property(self):
        """
        Verifica se a propriedade de heap está sendo mantida.
        
        Para um heap min, cada nó pai deve ser menor ou igual aos seus filhos.
        """
        for i in range(len(self.heap)):
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            
            # Verifica filho esquerdo
            if left_child < len(self.heap):
                if self.heap[i][0] > self.heap[left_child][0]:
                    logging.error("Propriedade de heap violada: pai[%d]=%s > filho_esq[%d]=%s", 
                                i, self.heap[i], left_child, self.heap[left_child])
                    raise ValueError("Propriedade de heap violada")
            
            # Verifica filho direito
            if right_child < len(self.heap):
                if self.heap[i][0] > self.heap[right_child][0]:
                    logging.error("Propriedade de heap violada: pai[%d]=%s > filho_dir[%d]=%s", 
                                i, self.heap[i], right_child, self.heap[right_child])
                    raise ValueError("Propriedade de heap violada")
    
    def peek(self):
        """
        Retorna o valor com menor prioridade sem removê-lo.
        
        Returns:
            O valor com menor prioridade ou None se a fila estiver vazia
        """
        if self.heap:
            return self.heap[0][1]  # Retorna o valor (segundo elemento da tupla)
        return None
    
    def is_empty(self):
        """
        Verifica se a fila está vazia.
        
        Returns:
            True se a fila estiver vazia, False caso contrário
        """
        return len(self.heap) == 0
    
    def size(self):
        """
        Retorna o número de elementos na fila.
        
        Returns:
            Número de elementos na fila
        """
        return len(self.heap)
    
    def __repr__(self):
        """Representação string da fila."""
        return f"PriorityQueue({len(self.heap)} elementos)"


# Tipos genéricos para Stack/Queue
T = TypeVar("T")


class Stack(Generic[T]):
    """
    Implementação simples de uma Pilha (LIFO) usando lista Python.

    - push: adiciona elemento ao topo
    - pop: remove o elemento do topo
    - peek: consulta o elemento do topo sem remover
    - is_empty / size: utilitários
    """

    def __init__(self) -> None:
        self._data: List[T] = []
        logging.info("Stack inicializada")

    def push(self, value: T) -> None:
        self._data.append(value)
        logging.debug("Stack.push: %s (tam=%d)", value, len(self._data))

    def pop(self) -> T:
        if not self._data:
            logging.warning("Tentativa de pop em Stack vazia")
            raise IndexError("pop from empty stack")
        value = self._data.pop()
        logging.debug("Stack.pop: %s (tam=%d)", value, len(self._data))
        return value

    def peek(self) -> Optional[T]:
        if not self._data:
            return None
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({len(self._data)} elementos)"

class FIFOQueue(Generic[T]):
    """
    Implementação de uma fila FIFO (First In, First Out) usando queue.Queue.

    - enqueue: adiciona no final
    - dequeue: remove do início
    - is_empty / size: utilitários
    """

    def __init__(self, maxsize: int = 0) -> None:
        """
        Cria uma fila FIFO.

        Args:
            maxsize (int): Tamanho máximo da fila. Se 0, é ilimitada.
        """
        self._queue = queue.Queue(maxsize=maxsize)
        self._lock = threading.Lock()
        logging.info("FIFOQueue inicializada (maxsize=%d)", maxsize)

    def enqueue(self, item: T) -> None:
        """Adiciona um item ao final da fila."""
        with self._lock:
            self._queue.put(item)
            logging.debug("FIFOQueue.enqueue: %s (tam=%d)", item, self.size())

    def dequeue(self) -> T:
        """
        Remove e retorna o item do início da fila.
        Se a fila estiver vazia, levanta queue.Empty.
        """
        with self._lock:
            item = self._queue.get_nowait()
            logging.debug("FIFOQueue.dequeue: %s (tam=%d)", item, self.size())
            return item

    def is_empty(self) -> bool:
        """Retorna True se a fila estiver vazia."""
        return self._queue.empty()

    def size(self) -> int:
        """Retorna o número de elementos na fila."""
        return self._queue.qsize()

    def __repr__(self) -> str:
        return f"FIFOQueue({self.size()} elementos)"

def reconstruct_path_with_stack(predecessors: Dict[T, Optional[T]], start: T, end: T) -> List[T]:
    """
    Reconstrói o caminho de start -> end usando uma Pilha (LIFO) e o mapa de predecessores.

    - Segue ponteiros de predecessor a partir de end até alcançar start, empilhando nós.
    - Desempilha para produzir a sequência na ordem correta (start -> ... -> end).

    Raises:
        ValueError: se a cadeia de predecessores não alcança start a partir de end.
    """
    stack: Stack[T] = Stack()

    current: Optional[T] = end
    steps = 0
    max_hops = len(predecessors) + 1  # trava de segurança

    while current is not None and steps <= max_hops:
        stack.push(current)
        if current == start:
            break
        current = predecessors.get(current)
        steps += 1

    if stack.is_empty() or stack.peek() != start:
        raise ValueError("Cadeia de predecessores não alcança o nó inicial para reconstrução do caminho")

    path: List[T] = []
    while not stack.is_empty():
        path.append(stack.pop())

    return path


def reconstruct_path(predecessors: Dict[T, Optional[T]], start: T, end: T) -> List[T]:
    """
    Versão pública simples para reconstruir caminho utilizando uma Pilha (LIFO).

    Implementada com list.append/pop via `Stack`, tratando casos de pilha vazia
    e cadeias inválidas de predecessores.
    """
    try:
        return reconstruct_path_with_stack(predecessors, start, end)
    except IndexError as exc:
        # Propaga erro de pilha vazia com mensagem amigável
        raise ValueError("Falha ao reconstruir caminho: pilha vazia") from exc
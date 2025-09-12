import heapq
import logging
import time

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
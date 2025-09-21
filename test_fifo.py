from src.structures import FIFOQueue

fila = FIFOQueue()
fila.enqueue("pedido1")
fila.enqueue("pedido2")
fila.enqueue("pedido3")

print(fila.dequeue())  # esperado: pedido1
print(fila.dequeue())  # esperado: pedido2
print(fila.dequeue())  # esperado: pedido3

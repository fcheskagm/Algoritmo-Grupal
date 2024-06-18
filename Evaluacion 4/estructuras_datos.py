class Pila:
    def __init__(self):
        self.elementos = []

    def push(self, elemento):
        self.elementos.append(elemento)

    def pop(self):
        return self.elementos.pop()

    def peek(self):
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0


class Cola:
    def __init__(self):
        self.elementos = []

    def encolar(self, elemento):
        self.elementos.append(elemento)

    def desencolar(self):
        return self.elementos.pop(0)

    def esta_vacia(self):
        return len(self.elementos) == 0
    
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaEntrelazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
        else:
            current = self.cabeza
            while current.siguiente:
                current = current.siguiente
            current.siguiente = Nodo(valor)

    def insertar(self, posicion, valor):
        nuevo_nodo = Nodo(valor)
        if posicion == 0:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        else:
            current = self.cabeza
            for _ in range(posicion - 1):
                if current.siguiente:
                    current = current.siguiente
                else:
                    break
            nuevo_nodo.siguiente = current.siguiente
            current.siguiente = nuevo_nodo

    def recorrer(self):
        current = self.cabeza
        while current:
            yield current.valor
            current = current.siguiente

    def eliminar(self, valor):
        if self.cabeza is None:
            return

        if self.cabeza.valor == valor:
            self.cabeza = self.cabeza.siguiente
            return

        current = self.cabeza
        while current.siguiente:
            if current.siguiente.valor == valor:
                current.siguiente = current.siguiente.siguiente
                return
            current = current.siguiente

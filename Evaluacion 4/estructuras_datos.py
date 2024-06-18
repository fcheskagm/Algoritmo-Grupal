class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class Pila:
    def __init__(self):
        self.cabeza = None

    def pop(self):
        if self.cabeza is None:
            return None
        valor = self.cabeza.valor
        self.cabeza = self.cabeza.siguiente
        return valor
    
    def push(self, valor):
        nuevo_nodo = Nodo(valor)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo

    def peek(self):
        if self.cabeza is None:
            raise IndexError("No se puede acceder al elemento superior de una pila vacía")
        return self.cabeza.valor

    def esta_vacia(self):
        return self.cabeza is None

    def mostrar_tareas(self):
        actual = self.cabeza
        while actual:
            print(actual.valor)
            actual = actual.siguiente

    def buscar(self, id):
        actual = self.cabeza
        while actual is not None:
            if actual.valor.id == id:
                return actual.valor
            actual = actual.siguiente
        return None
    
    def eliminar(self, nodo):
        if self.cabeza == nodo:
            self.cabeza = nodo.siguiente
        else:
            anterior = self.cabeza
            while anterior.siguiente != nodo:
                anterior = anterior.siguiente
            anterior.siguiente = nodo.siguiente

class Cola:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def encolar(self, elemento):
        if elemento is None:
            raise ValueError("No se puede agregar un valor None a la cola")
        nodo = Nodo(elemento)
        if self.cabeza is None:
            self.cabeza = nodo
            self.cola = nodo
        else:
            self.cola.siguiente = nodo
            self.cola = nodo

    def desencolar(self):
        if self.cabeza is None:
            raise IndexError("No se puede sacar un elemento de una cola vacía")
        valor = self.cabeza.valor
        self.cabeza = self.cabeza.siguiente
        if self.cabeza is None:
            self.cola = None
        return valor

    def esta_vacia(self):
        return self.cabeza is None
    
    def eliminar(self, valor):
        if self.esta_vacia():
            raise ValueError("La cola está vacía")

        if self.cabeza.valor == valor:
            self.desencolar()
            return

        nodo_actual = self.cabeza
        while nodo_actual.siguiente:
            if nodo_actual.siguiente.valor == valor:
                nodo_actual.siguiente = nodo_actual.siguiente.siguiente
                return
            nodo_actual = nodo_actual.siguiente

        raise ValueError("El valor no se encontró en la cola")

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


    def esta_vacia(self):
        return self.cabeza is None


    def buscar(self, id):
        actual = self.cabeza
        while actual is not None:
            if actual.valor.id == id:
                return actual.valor
            actual = actual.siguiente
        return None

    def actualizar(self, valor_antiguo, valor_nuevo):
        current = self.cabeza
        while current:
            if current.valor == valor_antiguo:
                current.valor = valor_nuevo
                return
            current = current.siguiente
        raise ValueError("Valor no encontrado en la lista")

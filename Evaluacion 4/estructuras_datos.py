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
        return self.cabeza.tarea

    def esta_vacia(self):
        return self.cabeza is None

    def mostrar_tareas(self):
        actual = self.cabeza
        while actual:
            print(actual.tarea)
            actual = actual.siguiente

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

class ListaEntrelazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, valor):
        if valor is None:
            raise ValueError("No se puede agregar un valor None a la lista")
        nodo = Nodo(valor)
        if self.cabeza is None:
            self.cabeza = nodo
        else:
            current = self.cabeza
            while current.siguiente:
                current = current.siguiente
            current.siguiente = nodo

    def recorrer(self):
        current = self.cabeza
        while current:
            yield current.valor
            current = current.siguiente

    def esta_vacia(self):
        return self.cabeza is None

    def eliminar(self, id):
        if self.esta_vacia():
            raise ValueError("La lista está vacía")
        if self.cabeza.valor.id == id:
            self.cabeza = self.cabeza.siguiente
            return
        current = self.cabeza
        while current.siguiente:
            if current.siguiente.valor.id == id:
                current.siguiente = current.siguiente.siguiente
                return
            current = current.siguiente
        raise ValueError("ID no encontrado en la lista")

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
    def insertar(self, posicion, elemento):
        if posicion == 0:
            nuevo_nodo = Nodo(elemento)
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            for _ in range(posicion - 1):
                if actual is None:
                    raise IndexError("Posición fuera de rango")
                actual = actual.siguiente
            if actual is None:
                raise IndexError("Posición fuera de rango")
            nuevo_nodo = Nodo(elemento)
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
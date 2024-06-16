class Cola:
    def __init__(self):
        self.elementos = []

    def encolar(self, elemento):
        self.elementos.insert(0, elemento)

    def desencolar(self):
        return self.elementos.pop()

    def esta_vacia(self):
        return len(self.elementos) == 0
class Proyecto:
    def __init__(self, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado, empresa, gerente, equipo):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.empresa = empresa
        self.gerente = gerente
        self.equipo = equipo
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

class Tarea:
    def __init__(
        self,
        id,
        nombre,
        empresa_cliente,
        descripcion,
        fecha_inicio,
        fecha_vencimiento,
        estado,
        porcentaje,
    ):
        self.id = id
        self.nombre = nombre
        self.empresa_cliente = empresa_cliente
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.porcentaje = porcentaje
        self.subtareas = []

    def agregar_subtarea(self, subtarea):
        self.subtareas.append(subtarea)


class Subtarea:
    def __init__(self, id, nombre, descripcion, estado):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado


class ProyectoManager:
    def __init__(self):
        self.lista_proyectos = [Proyecto("001", "Investigacion Modulo", "Realizar investigacion de lo que se encarga el modulo", "16-06-2024", "20-06-2024", "activo", "Restaurant", "Franchesca", "M: Inventario"), 
                                Proyecto("002", "Desarrollo Modulo", "Empezar el backend y fronted del modulo", "20-06-2024", "28-06-2024", "sin empezar", "Restaurant", "Franchesca", "M: Inventario")]
    
    def buscar_proyecto(self, criterio, valor):
        for proyecto in self.lista_proyectos:
            if getattr(proyecto, criterio) == valor:
                return proyecto
        return None

    def crear_proyecto(self):
        # Solicitar al usuario los datos del proyecto
        id = input("Ingrese el ID del proyecto: ")
        nombre = input("Ingrese el nombre del proyecto: ")
        descripcion = input("Ingrese la descripción del proyecto: ")
        fecha_inicio = input("Ingrese la fecha de inicio del proyecto (dd-mm-aaaa): ")
        fecha_vencimiento = input("Ingrese la fecha de vencimiento del proyecto (dd-mm-aaaa): ")
        estado = input("Ingrese el estado actual del proyecto: ")
        empresa = input("Ingrese la empresa del proyecto: ")
        gerente = input("Ingrese el gerente del proyecto: ")
        equipo = input("Ingrese el equipo del proyecto: ")

        # Crear una instancia de la clase Proyecto
        nuevo_proyecto = Proyecto(id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado, empresa, gerente, equipo)

        # Agregar el nuevo proyecto a la lista
        self.lista_proyectos.append(nuevo_proyecto)

        print("Proyecto creado con éxito.")
        return nuevo_proyecto

    def modificar_proyecto(self):
        criterio = input("Introduzca el criterio de búsqueda (nombre, descripción, etc.): ")
        valor = input("Introduzca el valor del criterio: ")
        proyecto = self.buscar_proyecto(criterio.lower(), valor)
        if proyecto:
            accion = input("Indique qué desea modificar (nombre, descripcion, fechaInicio, fechaVencimiento, estado, empresa, gerente, equipo): ")
            if accion == "nombre":
                proyecto.nombre = input("Ingrese el nuevo nombre del proyecto: ")
            elif accion == "descripcion":
                proyecto.descripcion = input("Ingrese la nueva descripción del proyecto: ")
            elif accion == "fechaInicio":
                proyecto.fecha_inicio = input("Ingrese la nueva fecha de inicio del proyecto (dd/mm/aaaa): ")
            elif accion == "fechaVencimiento":
                proyecto.fecha_vencimiento = input("Ingrese la nueva fecha de vencimiento del proyecto (dd/mm/aaaa): ")
            elif accion == "estado":
                proyecto.estado = input("Ingrese el nuevo estado del proyecto: ")
            elif accion == "empresa":
                proyecto.empresa = input("Ingrese el nombre de la nueva empresa: ")
            elif accion == "gerente":
                proyecto.gerente = input("Ingrese el nombre del nuevo gerente: ")
            elif accion == "equipo":
                proyecto.equipo = input("Ingrese el nuevo nombre del equipo: ")
            else:
                print("Opción no válida")
            print("Proyecto modificado con éxito.")
        else:
            print("Proyecto no encontrado")

    def consultar(self):
        criterio = input("Introduzca el criterio de búsqueda (nombre, descripción, etc.): ")
        valor = input("Introduzca el valor del criterio: ")
        proyecto = self.buscar_proyecto(criterio.lower(), valor)
        if proyecto:
            print("-"*30)
            print(f"ID: {proyecto.id}")
            print(f"Nombre: {proyecto.nombre}")
            print(f"Descripción: {proyecto.descripcion}")
            print(f"Fecha de Inicio: {proyecto.fecha_inicio}")
            print(f"Fecha de Vencimiento: {proyecto.fecha_vencimiento}")
            print(f"Estado: {proyecto.estado}")
            print(f"Empresa: {proyecto.empresa}")
            print(f"Gerente: {proyecto.gerente}")
            print(f"Equipo: {proyecto.equipo}")
            print("Proyecto consultado con éxito.")
        else:
            print("Proyecto no encontrado")

    def eliminar(self):
        nombre = input("Indique el nombre del proyecto a eliminar: ")
        for proyecto in self.lista_proyectos:
            if proyecto.nombre == nombre:
                self.lista_proyectos.remove(proyecto)
                print("Proyecto eliminado con éxito")
                return
        print("Proyecto no encontrado")

    def listar_nombres_proyectos(self):
        if not self.lista_proyectos:
            print("No hay proyectos para listar.")
            return

        for i, proyecto in enumerate(self.lista_proyectos, start=1):
            print(f"{i}. {proyecto.nombre}")

    def menu(self):
        while True:
            print("-"*30)
            print("Menú de Gestión de Proyectos")
            print("1. Crear Proyecto")
            print("2. Modificar Proyecto")
            print("3. Consultar Proyecto")
            print("4. Eliminar Proyecto")
            print("5. Listar Proyectos")
            print("6. Salir")
            print("-"*30)

            opcion = input("Seleccione una opción (1-6): ")

            if opcion == '1':
                self.crear_proyecto()
            elif opcion == '2':
                self.modificar_proyecto()
            elif opcion == '3':
                self.consultar()
            elif opcion == '4':
                self.eliminar()
            elif opcion == '5':
                self.listar_nombres_proyectos()
            elif opcion == '6':
                print("Saliendo del menú...")
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")


manager = ProyectoManager()
manager.menu()
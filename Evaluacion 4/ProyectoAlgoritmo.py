from datetime import datetime
import json

class Configuracion:
    def __init__(self, archivo_config):
        with open(archivo_config, "r") as archivo:
            self.datos = archivo.readlines()
            self.ruta_datos = self.datos[0].strip()
            self.ruta_subtareas = self.datos[1].strip()

    def cargar_datos_desde_json(self):
        proyectos = []
        with open(self.ruta_datos, "r") as archivo:
            datos = json.load(archivo)
            for proyecto_data in datos["proyectos"]:
                proyecto = Proyecto(
                    str(proyecto_data["id"]),
                    proyecto_data["nombre"],
                    proyecto_data["descripcion"],
                    datetime.strptime(proyecto_data["fecha_inicio"], "%Y-%m-%d"),
                    datetime.strptime(proyecto_data["fecha_vencimiento"], "%Y-%m-%d"),
                    proyecto_data["estado"],
                    proyecto_data["empresa"],
                    proyecto_data["gerente"],
                    proyecto_data["equipo"],
                )
                for tarea_data in proyecto_data["tareas"]:
                    tarea = Tarea(
                        str(tarea_data["id"]),
                        tarea_data["nombre"],
                        tarea_data["empresa_cliente"],
                        tarea_data["descripcion"],
                        datetime.strptime(tarea_data["fecha_inicio"], "%Y-%m-%d"),
                        datetime.strptime(tarea_data["fecha_vencimiento"], "%Y-%m-%d"),
                        tarea_data["estado"],
                        tarea_data["porcentaje"],
                    )
                    proyecto.agregar_tarea(tarea)
                proyectos.append(proyecto)
        return proyectos

    def cargar_subtareas_desde_json(self, proyectos):
        with open(self.ruta_subtareas, "r") as archivo_subtareas:
            subtareas_data = json.load(archivo_subtareas)
            for proyecto in proyectos:
                for tarea in proyecto.tareas:
                    if str(proyecto.id) in subtareas_data:
                        if str(tarea.id) in subtareas_data[str(proyecto.id)]["tareas"]:
                            for subtarea_data in subtareas_data[str(proyecto.id)]["tareas"][str(tarea.id)]:
                                subtarea = Subtarea(
                                    str(subtarea_data["id"]),
                                    subtarea_data["nombre"],
                                    subtarea_data["descripcion"],
                                    subtarea_data["estado"],
                                )
                                tarea.agregar_subtarea(subtarea)

    def mostrar_datos(self):
        proyectos = self.cargar_datos_desde_json()
        self.cargar_subtareas_desde_json(proyectos)
        for proyecto in proyectos:
            print(f"Proyecto: {proyecto.nombre}")
            for tarea in proyecto.tareas:
                print(f"    Tarea: {tarea.nombre}")
                for subtarea in tarea.subtareas:
                    print(f"        Subtarea: {subtarea.nombre}")
        return proyectos 

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
    def __init__(self, proyectos):
        self.lista_proyectos = proyectos
    
    def buscar_proyecto(self, criterio, valor):
        encontrado = False
        for proyecto in self.lista_proyectos:
            try:
                if getattr(proyecto, criterio) == valor:
                    return proyecto
                encontrado = True
            except AttributeError:
                pass
        if not encontrado:
            print(f"\nError: El criterio ' {criterio} ' no existe")
            print("Los criterios existentes son: \n[id, nombre, descripción, fecha_inicio, fecha_vencimiento, estado, empresa, gerente, equipo]")
        return None

    def crear_proyecto(self):
        # Solicitar al usuario los datos del proyecto
        id = input("Ingrese el ID del proyecto: ")
        nombre = input("Ingrese el nombre del proyecto: ")
        descripcion = input("Ingrese la descripción del proyecto: ")
        fecha_inicio = input("Ingrese la fecha de inicio del proyecto (aaaa-mm-dd): ")
        fecha_vencimiento = input("Ingrese la fecha de vencimiento del proyecto (aaaa-mm-dd): ")
        estado = input("Ingrese el estado actual del proyecto: ")
        empresa = input("Ingrese la empresa del proyecto: ")
        gerente = input("Ingrese el gerente del proyecto: ")
        equipo = input("Ingrese el equipo del proyecto: ")

        nuevo_proyecto = Proyecto(id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado, empresa, gerente, equipo)
        self.lista_proyectos.append(nuevo_proyecto)
        print("\nProyecto creado con éxito.")

    def modificar_proyecto(self):
        criterio = input("Introduzca el criterio de búsqueda: ")
        valor = input("Introduzca el valor del criterio: ")
        proyecto = self.buscar_proyecto(criterio.lower(), valor)
        if proyecto:
            accion = input("Indique qué desea modificar (nombre, descripcion, fechaInicio, fechaVencimiento, estado, empresa, gerente, equipo): ")
            if accion == "nombre":
                proyecto.nombre = input("Ingrese el nuevo nombre del proyecto: ")
            elif accion == "descripcion":
                proyecto.descripcion = input("Ingrese la nueva descripción del proyecto: ")
            elif accion == "fechaInicio":
                proyecto.fecha_inicio = input("Ingrese la nueva fecha de inicio del proyecto (aaaa-mm-dd): ")
            elif accion == "fechaVencimiento":
                proyecto.fecha_vencimiento = input("Ingrese la nueva fecha de vencimiento del proyecto (aaaa-mm-dd): ")
            elif accion == "estado":
                proyecto.estado = input("Ingrese el nuevo estado del proyecto: ")
            elif accion == "empresa":
                proyecto.empresa = input("Ingrese el nombre de la nueva empresa: ")
            elif accion == "gerente":
                proyecto.gerente = input("Ingrese el nombre del nuevo gerente: ")
            elif accion == "equipo":
                proyecto.equipo = input("Ingrese el nuevo nombre del equipo: ")
            else:
                print("\nOpción no válida")
            print("\nProyecto modificado con éxito.")
        else:
            print("\nProyecto no encontrado")

    def consultar(self):
        criterio = input("Introduzca el criterio de búsqueda: ")
        valor = input("Introduzca el valor del criterio: ")
        proyecto = self.buscar_proyecto(criterio.lower(), valor)
        if proyecto:
            print("-"*30)
            print(f"ID: {proyecto.id}")
            print(f"Nombre: {proyecto.nombre}")
            print(f"Descripción: {proyecto.descripcion}")
            print(f"Fecha de Inicio: {proyecto.fecha_inicio.date()}")
            print(f"Fecha de Vencimiento: {proyecto.fecha_vencimiento.date()}")
            print(f"Estado: {proyecto.estado}")
            print(f"Empresa: {proyecto.empresa}")
            print(f"Gerente: {proyecto.gerente}")
            print(f"Equipo: {proyecto.equipo}")
            print("\nProyecto consultado con éxito.")
        else:
            print("\nProyecto no encontrado")

    def eliminar(self):
        criterio = input("Introduzca el criterio de búsqueda: ")
        valor = input("Introduzca el valor del criterio: ")
        proyecto = self.buscar_proyecto(criterio.lower(), valor)
        if proyecto:
            self.lista_proyectos.remove(proyecto)
            print("\nProyecto eliminado con éxito")
            return
        else:
            print("\nProyecto no encontrado")

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
                print("\nOpción no válida. Por favor, intente de nuevo.")




pro = Configuracion("C:/Users/fches/OneDrive/Documents/Python/Algoritmo/Evaluacion 4/config.txt")
pross = pro.mostrar_datos()

manager = ProyectoManager(pross)
manager.menu()
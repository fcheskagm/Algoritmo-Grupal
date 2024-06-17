from datetime import datetime
import json
from estructuras_datos import Pila, Cola

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
        self.tareas_prioritarias = Pila()
        self.tareas_proximas_a_vencer = Cola()

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
            
    #Funciones subMenu: menu_tareas
    def agregar_tarea(self, proyecto):
        id = input("Ingrese el ID de la tarea: ")
        nombre = input("Ingrese el nombre de la tarea: ")
        empresa_cliente = input("Ingrese la empresa cliente de la tarea: ")
        descripcion = input("Ingrese la descripción de la tarea: ")
        fecha_inicio = input("Ingrese la fecha de inicio de la tarea (aaaa-mm-dd): ")
        fecha_vencimiento = input("Ingrese la fecha de vencimiento de la tarea (aaaa-mm-dd): ")
        estado = input("Ingrese el estado actual de la tarea: ")
        porcentaje = input("Ingrese el porcentaje de la tarea: ")

        nueva_tarea = Tarea(id, nombre, empresa_cliente, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje)
        proyecto.tareas.append(nueva_tarea)
        print("\nTarea agregada con éxito.")

    def insertar_tarea(self, proyecto):
        id = input("Ingrese el ID de la tarea: ")
        nombre = input("Ingrese el nombre de la tarea: ")
        empresa_cliente = input("Ingrese la empresa cliente de la tarea: ")
        descripcion = input("Ingrese la descripción de la tarea: ")
        fecha_inicio = input("Ingrese la fecha de inicio de la tarea (aaaa-mm-dd): ")
        fecha_vencimiento = input("Ingrese la fecha de vencimiento de la tarea (aaaa-mm-dd): ")
        estado = input("Ingrese el estado actual de la tarea: ")
        porcentaje = input("Ingrese el porcentaje de la tarea: ")
        posicion = int(input("Ingrese la posición donde insertar la tarea: "))

        nueva_tarea = Tarea(id, nombre, empresa_cliente, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje)
        proyecto.tareas.insert(posicion, nueva_tarea)
        print("\nTarea insertada con éxito.")

    def eliminar_tarea(self, proyecto):
        id = input("Ingrese el ID de la tarea a eliminar: ")
        for tarea in proyecto.tareas:
            if tarea.id == id:
                proyecto.tareas.remove(tarea)
                print("\nTarea eliminada con éxito.")
                return
        print("\nTarea no encontrada.")

    def buscar_tarea(self, proyecto):
        criterio = input("Ingrese el criterio de búsqueda (ID, nombre, empresa cliente, etc.): ")
        valor = input("Ingrese el valor del criterio: ")
        for tarea in proyecto.tareas:
            if getattr(tarea, criterio) == valor:
                print("\nTarea encontrada:")
                print(f"ID: {tarea.id}")
                print(f"Nombre: {tarea.nombre}")
                print(f"Empresa cliente: {tarea.empresa_cliente}")
                print(f"Descripción: {tarea.descripcion}")
                print(f"Fecha de inicio: {tarea.fecha_inicio.date()}")
                print(f"Fecha de vencimiento: {tarea.fecha_vencimiento.date()}")
                print(f"Estado: {tarea.estado}")
                print(f"Porcentaje: {tarea.porcentaje}")
                return
        print("\nTarea no encontrada.")

    def actualizar_tarea(self, proyecto):
        id = input("Ingrese el ID de la tarea a actualizar: ")
        for tarea in proyecto.tareas:
            if tarea.id == id:
                tarea.nombre = input("Ingrese el nuevo nombre de la tarea: ")
                tarea.empresa_cliente = input("Ingrese la nueva empresa cliente de la tarea: ")
                tarea.descripcion = input("Ingrese la nueva descripción de la tarea: ")
                tarea.fecha_inicio = input("Ingrese la nueva fecha de inicio de la tarea (aaaa-mm-dd): ")
                tarea.fecha_vencimiento = input("Ingrese la nueva fecha de vencimiento de la tarea (aaaa-mm-dd): ")
                tarea.estado = input("Ingrese el nuevo estado actual de la tarea: ")
                tarea.porcentaje = input("Ingrese el nuevo porcentaje de la tarea: ")
                print("\nTarea actualizada con éxito.")
                return
        print("\nTarea no encontrada.")

    def mostrar_tareas(self, proyecto):
        if proyecto.tareas:
            print("Tareas del proyecto:")
            for i, tarea in enumerate(proyecto.tareas, start=1):
                print(f"{i}. {tarea.nombre}")
                for subtarea in tarea.subtareas:
                    print(f"  - {subtarea.nombre}")
        else:
            print("No hay tareas en el proyecto")

        #Funciones del menu: "menu_tareas_prioritarias"
    def agregar_tarea_prioritaria(self, proyecto):
        id = input("Ingrese el ID de la tarea: ")
        nombre = input("Ingrese el nombre de la tarea: ")
        empresa_cliente = input("Ingrese la empresa cliente de la tarea: ")
        descripcion = input("Ingrese la descripción de la tarea: ")
        fecha_inicio = input("Ingrese la fecha de inicio de la tarea (dd-mm-aaaa): ")
        fecha_vencimiento = input("Ingrese la fecha de vencimiento de la tarea (dd-mm-aaaa): ")
        estado = input("Ingrese el estado actual de la tarea: ")
        porcentaje = int(input("Ingrese el porcentaje de la tarea: "))

        tarea = Tarea(id, nombre, empresa_cliente, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje)
        proyecto.tareas_prioritarias.push(tarea)

    def eliminar_tarea_prioritaria(self, proyecto):
        if not proyecto.tareas_prioritarias.esta_vacia():
            return proyecto.tareas_prioritarias.pop()
        return None

    def consultar_tarea_prioritaria(self, proyecto):
        if not proyecto.tareas_prioritarias.esta_vacia():
            return proyecto.tareas_prioritarias.peek()
        return None

    def tiempo_total_tareas_prioritarias(self, proyecto):
        tiempo_total = 0
        for tarea in proyecto.tareas_prioritarias.elementos:
            tiempo_total += tarea.fecha_vencimiento - tarea.fecha_inicio
        return tiempo_total
    
    
    def menu(self):
        while True:
            print("-"*30)
            print("Menú de Gestión de Proyectos")
            print("1. Crear Proyecto")
            print("2. Modificar Proyecto")
            print("3. Consultar Proyecto")
            print("4. Eliminar Proyecto")
            print("5. Listar Proyectos")
            print("6. Gestionar Tareas de un Proyecto")
            print("7. Salir")
            print("-"*30)

            opcion = input("Seleccione una opción (1-7): ")

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
                proyecto_id = input("Ingrese el ID del proyecto: ")
                self.menu_tareas(proyecto_id)
            elif opcion == '7':
                print("Saliendo del menú...")
                break
            else:
                print("\nOpción no válida. Por favor, intente de nuevo.")

    def menu_tareas(self, proyecto_id):
        proyecto = self.buscar_proyecto("id", proyecto_id)
        if proyecto:
            while True:
                print("-"*30)
                print("Menú de Gestión de Tareas")
                print("1. Agregar Tarea")
                print("2. Insertar Tarea")
                print("3. Eliminar Tarea")
                print("4. Buscar Tarea")
                print("5. Actualizar Tarea")
                print("6. Mostrar Tareas")
                print("7. Pila de Tareas Prioritarias")
                print("8. Salir")
                print("-"*30)

                opcion = input("Seleccione una opción (1-8): ")

                if opcion == '1':
                    self.agregar_tarea(proyecto)
                elif opcion == '2':
                    self.insertar_tarea(proyecto)
                elif opcion == '3':
                    self.eliminar_tarea(proyecto)
                elif opcion == '4':
                    self.buscar_tarea(proyecto)
                elif opcion == '5':
                    self.actualizar_tarea(proyecto)
                elif opcion == '6':
                    self.mostrar_tareas(proyecto)
                elif opcion == '7':
                    self.menu_tareas_prioritarias(proyecto)
                elif opcion == '8':
                    print("Saliendo del menú...")
                    break
                else:
                    print("\nOpción no válida. Por favor, intente de nuevo.")
        else:
            print("\nProyecto no encontrado")

    def menu_tareas_prioritarias(self, proyecto):
        while True:
            print("-"*30)
            print("Menú de Gestión de Tareas Prioritarias")
            print("1. Agregar Tarea Prioritaria")
            print("2. Eliminar Tarea Prioritaria")
            print("3. Consultar Tarea Prioritaria")
            print("4. Tiempo Total de Tareas Prioritarias")
            print("5. Salir")
            print("-"*30)

            opcion = input("Seleccione una opción (1-5): ")

            if opcion == '1':
                self.agregar_tarea_prioritaria(proyecto)
            elif opcion == '2':
                self.eliminar_tarea_prioritaria(proyecto)
            elif opcion == '3':
                self.consultar_tarea_prioritaria(proyecto)
            elif opcion == '4':
                self.tiempo_total_tareas_prioritarias(proyecto)
            elif opcion == '5':
                print("Saliendo del menú...")
                break
            else:
                print("\nOpción no válida. Por favor, intente de nuevo.")





pro = Configuracion("C:/Users/Acer Aspire3/Documents/Algoritmo-Grupal/Evaluacion 4/config.txt")
pross = pro.mostrar_datos()

manager = ProyectoManager(pross)
manager.menu()
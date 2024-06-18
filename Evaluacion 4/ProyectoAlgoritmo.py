from datetime import datetime
import json
<<<<<<< HEAD
from estructuras_datos import Pila, Cola, Nodo, ListaEntrelazada
=======
from estructuras_datos import Pila, Cola
>>>>>>> 5f476e446e605599cbcacfbbdb24ee28c2b9ef45

#Clase para la lectura de los datos, lee las rutas dentro del config.txt, para despues cargar los datos de los json
class Configuracion:
    def __init__(self, archivo_config):

        #Guarda ambas rutas encontradas en el txt 
        with open(archivo_config, "r", encoding='utf-8') as archivo:
            self.datos = archivo.readlines()
            self.ruta_datos = self.datos[0].strip()
            self.ruta_subtareas = self.datos[1].strip()

    def cargar_datos_desde_json(self):

        #Guarda los datos del primer archivo, creandolo como un constructor de la clase proyecto, al igual que las tareas, y los agrega a la lista de proyectos
        proyectos = []
        with open(self.ruta_datos, "r", encoding='utf-8') as archivo:
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
        with open(self.ruta_subtareas, "r", encoding='utf-8') as archivo_subtareas:
            subtareas_data = json.load(archivo_subtareas)
            for proyecto in proyectos:
                for tarea in proyecto.tareas.recorrer():
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
        #Unificar los datos
        proyectos = self.cargar_datos_desde_json()
        self.cargar_subtareas_desde_json(proyectos)
        return proyectos 

class Proyecto:
    #Se declaran los atributos que conforman al proyecto
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
<<<<<<< HEAD
        self.tareas = ListaEntrelazada()
=======
        self.tareas = []
>>>>>>> 5f476e446e605599cbcacfbbdb24ee28c2b9ef45
        self.tareas_prioritarias = Pila()
        self.tareas_proximas_a_vencer = Cola()

    #Hecemos el metodo para agregar las tareas a la lista 
    def agregar_tarea(self, tarea):
        self.tareas.agregar(tarea)

class Tarea:
    #Se declaran los atributos que conforman la tarea
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

    #Hecemos el metodo para agregar las subtareas a la lista
    def agregar_subtarea(self, subtarea):
        self.subtareas.append(subtarea)


class Subtarea:
    #Se declaran los atributos que conforman la subtarea
    def __init__(self, id, nombre, descripcion, estado):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado


class ProyectoManager:
    #Clase para gestionar los proyectos
    def __init__(self, proyectos):
        self.lista_proyectos = proyectos
        self.tareas_prioritarias = Pila()
        self.tareas_proximas_a_vencer = Cola()
        
    
    #Metodo para buscar un proyecto segun un criterio y valor dado
    def buscar_proyecto(self, criterio, valor):
        encontrado = False
        criterios_map = {
            "id": "id",
            "nombre": "nombre",
            "descripcion": "descripcion",
            "fecha inicio": "fecha_inicio",
            "fecha vencimiento": "fecha_vencimiento",
            "estado": "estado",
            "empresa": "empresa",
            "gerente": "gerente",
            "equipo": "equipo",
        }
        for proyecto in self.lista_proyectos:
            try:
                if criterio in ["fecha inicio", "fecha vencimiento"]:
                    valor = datetime.strptime(valor, "%Y-%m-%d")
                if getattr(proyecto, criterios_map[criterio]) == valor:
                    return proyecto
                encontrado = True
            except AttributeError:
                pass
        if not encontrado:
            print(f"\nError: El criterio ' {criterio} ' no existe")
            print("Los criterios existentes son: \n[id, nombre, descripción, fecha inicio, fecha vencimiento, estado, empresa, gerente, equipo]")
        return None

    def crear_proyecto(self):
        # Solicitar al usuario los datos del proyecto para agregarlo a la kista de proyectos
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
        #Pedimos que nos ingrese el criterio y valor para buscar el proyecto y, se pregunta que se quiere modificar
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
        #Pedimos que nos ingrese el criterio y valor para buscar el proyecto a consultar
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
        #Pedimos que nos ingrese el criterio y valor para buscar el proyecto a eliminar
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
        #Listamos todos los proyectos
        if not self.lista_proyectos:
            print("No hay proyectos para listar.")
            return
        for i, proyecto in enumerate(self.lista_proyectos, start=1):
            print(f"{i}. {proyecto.nombre}")
<<<<<<< HEAD
    #Funciones subMenu: menu_tareas
    

    def agregar_tarea(self, proyecto_selec):
        tarea_id = int(input("Ingrese el ID de la tarea: "))
        tarea_nombre = input("Ingrese el nombre de la tarea: ")
        empresa_cliente = input("Ingrese la empresa cliente: ")
        descripcion = input("Ingrese la descripción de la tarea: ")

        # Pedir la fecha de inicio y vencimiento en formato dd/mm/yyyy
        fecha_inicio_str = input("Ingrese la fecha de inicio de la tarea (yyyy-mm-dd): ")
        fecha_vencimiento_str = input("Ingrese la fecha de vencimiento de la tarea (yyyy-mm-dd): ")

        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d")

        estado = input("Ingrese el estado de la tarea (pendiente/realizada): ")
        porcentaje = input("Ingrese el porcentaje de avance de la tarea: ")

        tarea = Tarea(tarea_id, tarea_nombre, empresa_cliente, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje)
        proyecto_selec.tareas.agregar(tarea)
        print("\nTarea agregada con éxito.")
        

    def insertar_tarea(self, proyecto_selec):
        id = input("Ingrese el ID de la tarea: ")
        nombre = input("Ingrese el nombre de la tarea: ")
        empresa_cliente = input("Ingrese el nombre de la empresa cliente: ")
        descripcion = input("Ingrese la descripción de la tarea: ")
        fecha_inicio_str = input("Ingrese la fecha de inicio de la tarea (yyyy-mm-dd): ")
        fecha_vencimiento_str = input("Ingrese la fecha de vencimiento de la tarea (yyyy-mm-dd): ")
        estado = input("Ingrese el estado de la tarea (pendiente/realizada): ")
        porcentaje = input("Ingrese el porcentaje de avance de la tarea: ")
        
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d")
        
        tarea = Tarea(id, nombre, empresa_cliente, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje)
        posicion = int(input("Ingrese la posición en la que desea insertar la tarea: "))
        proyecto_selec.tareas.insertar(posicion, tarea)
        print("\nTarea insertada con éxito.")

    def eliminar_tarea(self, proyecto_selec):
        tarea_id = input("Ingrese el ID de la tarea que desea eliminar: ")
        tarea = proyecto_selec.tareas.buscar(tarea_id)
        if tarea:
            proyecto_selec.tareas.eliminar(tarea_id)
            print("\nTarea eliminada con éxito.")
        else:
            print("\nTarea no encontrada.")

    def buscar_tarea(self, proyecto_selec):
        tarea_id = input("Ingrese el ID de la tarea que desea buscar: ")
        tarea = proyecto_selec.tareas.buscar(tarea_id)
        if tarea:
            print("\nTarea encontrada:")
            print(f"ID: {tarea.id}")
            print(f"Nombre: {tarea.nombre}")
            print(f"Empresa cliente: {tarea.empresa_cliente}")
            print(f"Descripción: {tarea.descripcion}")
            print(f"Fecha de inicio: {tarea.fecha_inicio.strftime('%Y-%m-%d')}")
            print(f"Fecha de vencimiento: {tarea.fecha_vencimiento.strftime('%Y-%m-%d')}")
            print(f"Estado: {tarea.estado}")
            print(f"Porcentaje de avance: {tarea.porcentaje}")
        else:
            print("\nTarea no encontrada.")

    def actualizar_tarea(self, proyecto_selec):
        tarea_id = input("Ingrese el ID de la tarea que desea actualizar: ")
        tarea = proyecto_selec.tareas.buscar(tarea_id)
        if tarea:
            tarea.nombre = input("Ingrese el nuevo nombre de la tarea: ")
            tarea.empresa_cliente = input("Ingrese la nueva empresa cliente: ")
            tarea.descripcion = input("Ingrese la nueva descripción de la tarea: ")
            fecha_inicio_str = input("Ingrese la nueva fecha de inicio de la tarea (yyyy-mm-dd): ")
            fecha_vencimiento_str = input("Ingrese la nueva fecha de vencimiento de la tarea (yyyy-mm-dd): ")
            tarea.estado = input("Ingrese el nuevo estado de la tarea (pendiente/realizada): ")
            tarea.porcentaje = input("Ingrese el nuevo porcentaje de avance de la tarea: ")
            
            tarea.fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            tarea.fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d")
            
            print("\nTarea actualizada con éxito.")
        else:
            print("\nTarea no encontrada.")

        #Funciones del menu: "menu_tareas_prioritarias"
    def agregar_tarea_prioritaria(self):
=======
            
    #Funciones subMenu: menu_tareas
    def agregar_tarea(self, proyecto):
>>>>>>> 5f476e446e605599cbcacfbbdb24ee28c2b9ef45
        id = input("Ingrese el ID de la tarea: ")
        nombre = input("Ingrese el nombre de la tarea: ")
        empresa_cliente = input("Ingrese la empresa cliente de la tarea: ")
        descripcion = input("Ingrese la descripción de la tarea: ")
<<<<<<< HEAD
        fecha_inicio_str = input("Ingrese la fecha de inicio de la tarea (yyyy-mm-dd): ")
        fecha_vencimiento_str = input("Ingrese la fecha de vencimiento de la tarea (yyyy-mm-dd): ")
        estado = input("Ingrese el estado actual de la tarea: ")
        porcentaje = int(input("Ingrese el porcentaje de la tarea: "))

        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d")

        tarea = Tarea(id, nombre, empresa_cliente, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje)
        self.tareas_prioritarias.push(tarea)

    def eliminar_tarea_prioritaria(self):
        if not self.tareas_prioritarias.esta_vacia():
            tarea_eliminar = self.tareas_prioritarias.pop()
            print("Tarea prioritaria eliminada:")
            print("ID:", tarea_eliminar.id)
            print("Nombre:", tarea_eliminar.nombre)
            print("Empresa cliente:", tarea_eliminar.empresa_cliente)
            print("Descripción:", tarea_eliminar.descripcion)
            print("Fecha de inicio:", tarea_eliminar.fecha_inicio.strftime("%Y-%m-%d"))
            print("Fecha de vencimiento:", tarea_eliminar.fecha_vencimiento.strftime("%Y-%m-%d"))
            print("Estado:", tarea_eliminar.estado)
            print("Porcentaje:", tarea_eliminar.porcentaje)
        else:
            print("No hay tareas prioritarias para eliminar.")

    def consultar_tarea_prioritaria(self):
        if not self.tareas_prioritarias.esta_vacia():
            tarea = self.tareas_prioritarias.peek()
            print("Tarea prioritaria:")
            print("ID:", tarea.id)
            print("Nombre:", tarea.nombre)
            print("Empresa cliente:", tarea.empresa_cliente)
            print("Descripción:", tarea.descripcion)
            print("Fecha de inicio:", tarea.fecha_inicio.strftime("%Y-%m-%d"))
            print("Fecha de vencimiento:", tarea.fecha_vencimiento.strftime("%Y-%m-%d"))
            print("Estado:", tarea.estado)
            print("Porcentaje:", tarea.porcentaje)
        else:
            print("No hay tareas prioritarias.")

    def tiempo_total_tareas_prioritarias(self):
        tiempo_total = 0
        pila_copia = Pila()  # Crea una nueva pila
        pila_temporal = Pila()  # Crea una pila temporal
        while self.tareas_prioritarias.cabeza:
            tarea = self.tareas_prioritarias.pop()
            pila_temporal.push(tarea)  # Push el elemento a la pila temporal
            pila_copia.push(tarea)  # Push el elemento a la nueva pila
        while pila_copia.cabeza:
            tarea = pila_copia.pop()
            delta = tarea.fecha_vencimiento - tarea.fecha_inicio
            tiempo_total += delta.days
        print("Tiempo total de tareas prioritarias:", tiempo_total, "días")
        while pila_temporal.cabeza:  # Devuelve los elementos a la pila original
            tarea = pila_temporal.pop()
            self.tareas_prioritarias.push(tarea)
            
        #colas

    def agregar_tareas_proximas_automatico(self):
        today = datetime.today()
        for proyecto in self.lista_proyectos:
            for tarea in proyecto.tareas.recorrer():
                tiempo_restante = (tarea.fecha_vencimiento - today).days
                if tiempo_restante < 15:
                    self.tareas_proximas_a_vencer.encolar(tarea)
    
    def agregar_tareas_proximas_a_vencer(self, proyecto_selec):
        tarea_id = input("Ingrese el ID de la tarea que desea agregar: ")
        tarea = proyecto_selec.tareas.buscar(tarea_id)
        if tarea is not None:
            self.tareas_proximas_a_vencer.encolar(tarea)
            print(f"Se agregó la tarea '{tarea.nombre}'")
        else:
            print("No se encontró la tarea especificada")
        
    def eliminar_tarea_proxima_vencer(self):
        return
    def consultar_tarea_proxima_vencer(self):
        if not self.tareas_proximas_a_vencer.esta_vacia():
            tarea_actual = self.tareas_proximas_a_vencer.cabeza
            while tarea_actual is not None:
                tarea = tarea_actual.valor
                print("Tarea próxima a vencer:")
                print("ID:", tarea.id)
                print("Nombre:", tarea.nombre)
                print("Empresa cliente:", tarea.empresa_cliente)
                print("Descripción:", tarea.descripcion)
                print("Fecha de inicio:", tarea.fecha_inicio.strftime("%Y-%m-%d"))
                print("Fecha de vencimiento:", tarea.fecha_vencimiento.strftime("%Y-%m-%d"))
                print("Estado:", tarea.estado)
                print("Porcentaje:", tarea.porcentaje)
                print("")  # Agregué un espacio en blanco entre cada tarea
                tarea_actual = tarea_actual.siguiente
        else:
            print("No hay tareas próximas a vencer.")
    def tiempo_total_tareas_proximas_vencer(self):
        tiempo_total = 0
        cola_copia = Cola()  # Crea una nueva cola
        cola_temporal = Cola()  # Crea una cola temporal
        while self.tareas_proximas_a_vencer.cabeza:
            tarea = self.tareas_proximas_a_vencer.desencolar()
            cola_temporal.encolar(tarea)  # Enqueue el elemento a la cola temporal
            cola_copia.encolar(tarea)  # Enqueue el elemento a la nueva cola
        while cola_copia.cabeza:
            tarea = cola_copia.desencolar()
            delta = tarea.fecha_vencimiento - tarea.fecha_inicio
            tiempo_total += delta.days
        print("Tiempo total de tareas próximas a vencer:", tiempo_total, "días")
        while cola_temporal.cabeza:  # Devuelve los elementos a la cola original
            tarea = cola_temporal.desencolar()
            self.tareas_proximas_a_vencer.encolar(tarea)

#DESDE AQUIIIII CLASE MODULO 3

    def consultar_tareas_por_estado(self, id_proyecto, estado):
        tareas_encontradas = []
        proyecto_encontrado = None
        for proyecto in self.lista_proyectos:
            if proyecto.id == id_proyecto:
                proyecto_encontrado = proyecto
                break
        if proyecto_encontrado:
            for tarea in proyecto_encontrado.tareas.recorrer(): 
                if tarea.estado == estado:
                    tareas_encontradas.append(tarea)
            self.mostrar_tareas(tareas_encontradas)
        else:
            print(f"\nNo se encontró el proyecto con id {id_proyecto}.")

    def mostrar_tareas(self, tareas):
        if tareas:
            print("\nTareas encontradas:")
            for tarea in tareas:
                print(f"\nID: {tarea.id}, Nombre: {tarea.nombre}, \n   Descripción: {tarea.descripcion}, "
                    f"\n   Estado: {tarea.estado}, \n   Fecha de Inicio: {tarea.fecha_inicio}, "
                    f"\n   Fecha de Vencimiento: {tarea.fecha_vencimiento}")
        else:
            print("\nNo se encontraron tareas.")

    def filtrar_tareas_por_fecha_inicio(self, fecha_inicio_desde, fecha_inicio_hasta):
        tareas_encontradas = ListaEntrelazada()
        for proyecto in self.lista_proyectos:
            for tarea in proyecto.tareas.recorrer():
                if fecha_inicio_desde <= tarea.fecha_inicio <= fecha_inicio_hasta:      #arreglar para mostrar en ambos caso no solo estado
                    tareas_encontradas.agregar(tarea)
                """for subtarea in tarea.subtareas.recorrer():
                    if fecha_inicio_desde <= subtarea.fecha_inicio <= fecha_inicio_hasta:
                        tareas_encontradas.agregar(subtarea)"""
        self.mostrar_tareas(tareas_encontradas.recorrer())

    def filtrar_tareas_por_fecha_vencimiento(self, fecha_vencimiento_desde, fecha_vencimiento_hasta):
        tareas_encontradas = ListaEntrelazada()
        for proyecto in self.lista_proyectos.recorrer():
            for tarea in proyecto.tareas.recorrer():
                if fecha_vencimiento_desde <= tarea.fecha_vencimiento <= fecha_vencimiento_hasta:       #arreglar
                    tareas_encontradas.agregar(tarea)
                for subtarea in tarea.subtareas.recorrer():
                    if fecha_vencimiento_desde <= subtarea.fecha_vencimiento <= fecha_vencimiento_hasta:
                        tareas_encontradas.agregar(subtarea)
        self.mostrar_tareas(tareas_encontradas.recorrer())

    def filtrar_tareas_por_fecha_inicio_antes(self, fecha_inicio):
        tareas_encontradas = ListaEntrelazada()
        for proyecto in self.lista_proyectos.recorrer():
            for tarea in proyecto.tareas.recorrer():
                if tarea.fecha_inicio < fecha_inicio:      #arreglar
                    tareas_encontradas.agregar(tarea)
                for subtarea in tarea.subtareas.recorrer():
                    if subtarea.fecha_inicio < fecha_inicio:
                        tareas_encontradas.agregar(subtarea)
        self.mostrar_tareas(tareas_encontradas.recorrer())

    def filtrar_tareas_por_fecha_inicio_despues(self, fecha_inicio):
        tareas_encontradas = ListaEntrelazada()
        for proyecto in self.lista_proyectos.recorrer():
            for tarea in proyecto.tareas.recorrer():  #arreglar
                if tarea.fecha_inicio > fecha_inicio:
                    tareas_encontradas.agregar(tarea)
                for subtarea in tarea.subtareas.recorrer():
                    if subtarea.fecha_inicio > fecha_inicio:
                        tareas_encontradas.agregar(subtarea)
        self.mostrar_tareas(tareas_encontradas.recorrer())

    def filtrar_proyectos_por_criterio(self):
        print("\n          Filtrar proyectos por criterio")
        print("     "+"-"*55)
        print("       1. Filtrar por fecha de inicio")
        print("       2. Filtrar por fecha de vencimiento")
        print("       3. Filtrar por estado")
        print("       4. Filtrar por empresa")
        print("       5. Salir al menu principal")

        criterio = None
        valor = None

        while criterio not in ["fecha_inicio", "fecha_vencimiento", "estado", "empresa"]:
            op = int(input("       Seleccione una opción (1-4): "))
            if op == 1:
                criterio = "fecha_inicio"
                valor = datetime.strptime(input("Ingrese la fecha de inicio (yyyy-mm-dd): "), "%Y-%m-%d")
            elif op == 2:
                criterio = "fecha_vencimiento"
                valor = datetime.strptime(input("Ingrese la fecha de vencimiento (yyyy-mm-dd): "), "%Y-%m-%d")
            elif op == 3:
                criterio = "estado"
                valor = input("Ingrese el estado: ")
            elif op == 4:
                criterio = "empresa"
                valor = input("Ingrese la empresa: ")
            elif op == 5:
                print("\n          Saliendo del menu...")
                return
            else:
                print("\n          Opción no válida. Por favor, intente de nuevo.")

        proyectos_filtrados = []
        for proyecto in self.lista_proyectos:
            if criterio == "fecha_inicio":
                if proyecto.fecha_inicio == valor:
                    proyectos_filtrados.append(proyecto)
            elif criterio == "fecha_vencimiento":
                if proyecto.fecha_vencimiento == valor:
                    proyectos_filtrados.append(proyecto)
            elif criterio == "estado":
                if proyecto.estado == valor:
                    proyectos_filtrados.append(proyecto)
            elif criterio == "empresa":
                if proyecto.empresa == valor:
                    proyectos_filtrados.append(proyecto)

        if proyectos_filtrados:
            print("\n          Proyectos filtrados:")
            for proyecto in proyectos_filtrados:
                print(f"  - {proyecto.nombre} ({proyecto.estado})")
        else:
            print("\n          No se encontraron proyectos que coincidan con el criterio.")

#HASTA AQUI VER SI SE PUEDE METER A CLASE PARA NO SER TANTO CODIGO
=======
        fecha_inicio = input("Ingrese la fecha de inicio de la tarea (aaaa-mm-dd): ")
        fecha_vencimiento = input("Ingrese la fecha de vencimiento de la tarea (aaaa-mm-dd): ")
        estado = input("Ingrese el estado actual de la tarea: ")
        porcentaje = input("Ingrese el porcentaje de la tarea: ")
>>>>>>> 5f476e446e605599cbcacfbbdb24ee28c2b9ef45

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
<<<<<<< HEAD
            print("\n                 Menú de Gestión de Proyectos")
            print("-"*60)
            print("  1. Crear Proyecto")
            print("  2. Modificar Proyecto")
            print("  3. Consultar Proyecto")
            print("  4. Eliminar Proyecto")
            print("  5. Listar Proyectos")
            print("  6. Listar Proyectos por filtro")
            print("  7. Seleccionar proyecto para gestion de tareas")     
            print("  8. Consultar todas las tarear por estado")
            print("  9. Filtrar tareas por fechas")
            print("  10. Salir")
            print("-"*60)
            n = int(input("Seleccione una opción (1-9): "))

            if n == 1:
=======
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
>>>>>>> 5f476e446e605599cbcacfbbdb24ee28c2b9ef45
                self.crear_proyecto()

            elif n == 2:
                self.modificar_proyecto()

            elif n == 3:
                self.consultar()

            elif n == 4:
                self.eliminar()

            elif n == 5:
                self.listar_nombres_proyectos()
<<<<<<< HEAD
            
            elif n == 6:
                self.filtrar_proyectos_por_criterio()

            elif n == 7:
                t = True
                self.listar_nombres_proyectos()
                f = input("\nSeleccione el proyecto por id o nombre: ")
                proyecto_selec = self.buscar_proyecto("id",f)
                while t:
                    print(f"\n          Gestión de Tareas del Proyecto: {proyecto_selec.nombre}")
                    print("     "+"-"*55)
                    print("       1. Listar todas las tareas y subtareas de forma jerarquica")
                    print("       2. Agregar tarea")
                    print("       3. Insertar tarea en una posicion especifica")
                    print("       4. Eliminar tarea")
                    print("       5. Buscar tarea")
                    print("       6. Actualizar informacion tarea")
                    print("       7. Tareas Prioritarias")
                    print("       8. Tareas Por Terminar")
                    print("       9. Consultar todas las tarear por estado")
                    print("       10. Salir al menu principal")

                    op = int(input("       Seleccione una opción (1-9): "))
                    if op == 1:
                        self.mostrar_tareas(proyecto_selec)
                    elif op == 2:
                        self.agregar_tarea(proyecto_selec)
                    elif op == 3:
                        self.insertar_tarea(proyecto_selec)
                    elif op == 4:
                        self.eliminar_tarea(proyecto_selec)
                    elif op == 5:
                        self.buscar_tarea(proyecto_selec)
                    elif op == 6:
                        self.actualizar_tarea(proyecto_selec)
                    elif op == 7:
                        cc = True
                        while cc:
                            print("\n                         Tareas Prioritarias")
                            print("          "+"-"*50)
                            print("            1. Agregar Tarea Prioritaria")
                            print("            2. Eliminar Tarea Prioritaria")
                            print("            3. Consultar Tarea Prioritaria")
                            print("            4. Tiempo Total de Tareas Prioritarias")
                            print("            5. Salir al menu anterior")
                            print("          "+"-"*50)
                            op = int(input("          Seleccione una opción (1-5): "))
                            if op == 1:
                                self.agregar_tarea_prioritaria()
                            elif op == 2:
                                self.eliminar_tarea_prioritaria()
                            elif op == 3:
                                self.consultar_tarea_prioritaria()
                            elif op == 4:
                                self.tiempo_total_tareas_prioritarias()
                            elif op == 5:
                                print("\n          Saliendo del menu...")
                                cc = False
                            else:
                                print("\n          Opción no válida. Por favor, intente de nuevo.")
                    elif op == 8:
                        cf = True
                        while cf:
                            print("\n                         Tareas Por Finalizar")
                            print("          "+"-"*50)
                            print("            1. Agregar Tarea ")
                            print("            2. Eliminar Tarea ")
                            print("            3. Consultar Tarea ")
                            print("            4. Tiempo Total de Tareas ")
                            print("            5. Salir al menu anterior")
                            print("          "+"-"*50)
                            op = int(input("       Seleccione una opción (1-5): "))
                            self.agregar_tareas_proximas_automatico()
                            if op == 1:
                                self.agregar_tareas_proximas_a_vencer(proyecto_selec)
                            elif op == 2:
                                self.eliminar_tarea_proxima_vencer()
                            elif op == 3:
                                self.consultar_tarea_proxima_vencer()
                            elif op == 4:
                                self.tiempo_total_tareas_proximas_vencer()
                            elif op == 5:
                                print("\n          Saliendo del menu...")
                                cf = False
                            else:
                                print("\n          Opción no válida. Por favor, intente de nuevo.")
                    elif op == 9:
                        estado = input("Ingrese el estado a consultar en las tareas")
                        print("")
                        self.consultar_tareas_por_estado(f, estado)
                    
                    elif op == 10:
                        print("\n       Saliendo del menu...")
                        t = False
                    else:
                        print("\n       Opción no válida. Por favor, intente de nuevo.")
                    
            elif n == 8:
                return
            elif n == 9:
                
                print("\n          Filtrar tareas por fechas")
                print("     "+"-"*55)
                print("       1. Filtrar tareas por fecha de inicio")
                print("       2. Filtrar tareas por fecha de vencimiento")
                print("       3. Filtrar tareas por fecha de inicio antes de")
                print("       4. Filtrar tareas por fecha de inicio después de")
                print("       5. Salir al menu principal")

                op = int(input("       Seleccione una opción (1-5): "))
                if op == 1:
                    fecha_inicio_desde = datetime.strptime(input("Ingrese la fecha de inicio desde (yyyy-mm-dd): "), "%Y-%m-%d")
                    fecha_inicio_hasta = datetime.strptime(input("Ingrese la fecha de inicio hasta (yyyy-mm-dd): "), "%Y-%m-%d")
                    self.filtrar_tareas_por_fecha_inicio(fecha_inicio_desde, fecha_inicio_hasta)
                elif op == 2:
                    fecha_vencimiento_desde = datetime.strptime(input("Ingrese la fecha de vencimiento desde (yyyy-mm-dd): "), "%Y-%m-%d")
                    fecha_vencimiento_hasta = datetime.strptime(input("Ingrese la fecha de vencimiento hasta (yyyy-mm-dd): "), "%Y-%m-%d")
                    self.filtrar_tareas_por_fecha_vencimiento(fecha_vencimiento_desde, fecha_vencimiento_hasta)
                elif op == 3:
                    fecha_inicio = datetime.strptime(input("Ingrese la fecha de inicio antes de (yyyy-mm-dd): "), "%Y-%m-%d")
                    self.filtrar_tareas_por_fecha_inicio_antes(fecha_inicio)
                elif op == 4:
                    fecha_inicio = datetime.strptime(input("Ingrese la fecha de inicio después de (yyyy-mm-dd): "), "%Y-%m-%d")
                    self.filtrar_tareas_por_fecha_inicio_despues(fecha_inicio)
                elif op == 5:
                    print("\n          Saliendo del menu...")
                else:
                    print("\n          Opción no válida. Por favor, intente de nuevo.")

            elif n == 10:

                print("\nSaliendo del programa...")
=======
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
>>>>>>> 5f476e446e605599cbcacfbbdb24ee28c2b9ef45
                break
                

            else:
                print("\nOpción no válida. Por favor, intente de nuevo.")
                

#Luego veo si lo optimizo, lo importante es que funcione :D

<<<<<<< HEAD
pro = Configuracion("C:/Users/Acer Aspire3/Desktop/Algoritmo-Grupal/Evaluacion 4/config.txt") #Metan los archivos .json y .txt en la misma carpeta del proyecto y cambien las rutas
=======



pro = Configuracion("C:/Users/Acer Aspire3/Documents/Algoritmo-Grupal/Evaluacion 4/config.txt")
>>>>>>> 5f476e446e605599cbcacfbbdb24ee28c2b9ef45
pross = pro.mostrar_datos()

manager = ProyectoManager(pross)
manager.menu()
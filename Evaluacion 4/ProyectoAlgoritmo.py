from datetime import datetime
import json
from estructuras_datos import Pila, Cola, Nodo, ListaEntrelazada

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
    
    def guardar_datos(self, proyectos):

        datos_proyectos = []
        for proyecto in proyectos:
            datos_proyecto = {
                "id": proyecto.id,
                "nombre": proyecto.nombre,
                "descripcion": proyecto.descripcion,
                "fecha_inicio": proyecto.fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_vencimiento": proyecto.fecha_vencimiento.strftime("%Y-%m-%d"),
                "estado": proyecto.estado,
                "empresa": proyecto.empresa,
                "gerente": proyecto.gerente,
                "equipo": proyecto.equipo,
                "tareas": [],
                "subtareas": []
            }
            for tarea in proyecto.tareas.recorrer():
                datos_tarea = {
                    "id": tarea.id,
                    "nombre": tarea.nombre,
                    "empresa_cliente": tarea.empresa_cliente,
                    "descripcion": tarea.descripcion,
                    "fecha_inicio": tarea.fecha_inicio.strftime("%Y-%m-%d"),
                    "fecha_vencimiento": tarea.fecha_vencimiento.strftime("%Y-%m-%d"),
                    "estado": tarea.estado,
                    "porcentaje": tarea.porcentaje,
                    "subtareas": []
                }
                for subtarea in tarea.subtareas:
                    datos_subtarea = {
                        "id": subtarea.id,
                        "nombre": subtarea.nombre,
                        "descripcion": subtarea.descripcion,
                        "estado": subtarea.estado
                    }
                    datos_tarea["subtareas"].append(datos_subtarea)
                datos_proyecto["tareas"].append(datos_tarea)
            datos_proyectos.append(datos_proyecto)

        with open(self.ruta_datos, "w", encoding="utf-8") as archivo:
            json.dump(datos_proyectos, archivo, ensure_ascii=False, indent=4)


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
        self.tareas = ListaEntrelazada()
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
    
    #Metodo para buscar un proyecto segun un criterio y valor dado
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
            print("Los criterios existentes son: \n[id, nombre, descripción, fecha inicio, fecha vencimiento, estado, empresa, gerente, equipo]")
        return None

    def crear_proyecto(self):
        # Solicitar al usuario los datos del proyecto para agregarlo a la kista de proyectos
        id = input("Ingrese el ID del proyecto: ")
        nombre = input("Ingrese el nombre del proyecto: ")
        descripcion = input("Ingrese la descripción del proyecto: ")
        fecha_inicio = input("Ingrese la fecha de inicio del proyecto (aaaa-mm-dd): ")
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_vencimiento = input("Ingrese la fecha de vencimiento del proyecto (aaaa-mm-dd): ")
        fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
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
            accion = input("Indique qué desea modificar (nombre, descripcion, fecha inicio, fecha vencimiento, estado, empresa, gerente, equipo): ")
            if accion == "nombre":
                proyecto.nombre = input("Ingrese el nuevo nombre del proyecto: ")
            elif accion == "descripcion":
                proyecto.descripcion = input("Ingrese la nueva descripción del proyecto: ")
            elif accion == "fecha inicio":
                fecha_inicio = input("Ingrese la nueva fecha de inicio del proyecto (aaaa-mm-dd): ")
                proyecto.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            elif accion == "fecha vencimiento":
                fecha_vencimiento = input("Ingrese la nueva fecha de vencimiento del proyecto (aaaa-mm-dd): ")
                proyecto.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
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

    def consultar_proyecto(self):
        #Pedimos que nos ingrese el criterio y valor para buscar el proyecto a consultar
        criterio = input("\nIntroduzca el criterio de búsqueda: ")
        valor = input("Introduzca el valor del criterio: ")
        proyecto = self.buscar_proyecto(criterio.lower(), valor)
        if proyecto:
            print("-"*60)
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

    def consultar(self, proyectos):
 
        for proyecto in proyectos:
            print(f"\tNombre: {proyecto.nombre}")
            print(f"\tDescripción: {proyecto.descripcion}")
            print(f"\tFecha de Inicio: {proyecto.fecha_inicio.date()}")
            print(f"\tFecha de Vencimiento: {proyecto.fecha_vencimiento.date()}")
            print(f"\tEstado: {proyecto.estado}")
            print(f"\tEmpresa: {proyecto.empresa}")
            print(f"\tGerente: {proyecto.gerente}")
            print(f"\tEquipo: {proyecto.equipo}")
            print("\n")
        



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
        print("\n\t\t\tLista de Proyectos")
       
        print("\t"+"-"*42+"\t")
        print("\t       ID. Nombre Proyecto")
        for proyecto in self.lista_proyectos:
            print(f"\t\t{proyecto.id}. {proyecto.nombre}")
        print("\t"+"-"*42+"\t")

    def buscar_proyecto_filtro(self, criterio, valor):
        proyectos_encontrados = []
        for proyecto in self.lista_proyectos:
            try:
                if getattr(proyecto, criterio) == valor:
                    proyectos_encontrados.append(proyecto)
            except AttributeError:
                pass
        if not proyectos_encontrados:
            print(f"\nError: El criterio ' {criterio} ' no existe")
            print("Los criterios existentes son: \n[id, nombre, descripción, fecha inicio, fecha vencimiento, estado, empresa, gerente, equipo]")
        return proyectos_encontrados
    
    def filtrar_todas_tareas_por_estado(self):
        tareas_filtradas = []
        estado_tarea = input("\nIngrese el estado de las tareas: ")
        for proyecto in self.lista_proyectos:
            for tarea in proyecto.tareas.recorrer():
                if estado_tarea == tarea.estado:
                    tareas_filtradas.append(tarea)
        print(f"\n\t     Todas las tareas con estado: {estado_tarea}")
        print("\t"+"-"*51)
        for tarea in tareas_filtradas:
            print(f"\t      ID:{tarea.id}, Nombre: {tarea.nombre}, \n\t      Fecha inicio:{tarea.fecha_inicio.date()}, \n\t      Fecha vencimiento: {tarea.fecha_vencimiento.date()}\n")


    #Funciones subMenu: menu_tareas
    def agregar_nuevatarea(self, proyecto):
        id = input("\n       Ingrese el ID de la tarea: ")
        nombre = input("       Ingrese el nombre de la tarea: ")
        empresa_cliente = input("       Ingrese la empresa cliente de la tarea: ")
        descripcion = input("       Ingrese la descripción de la tarea: ")
        fecha_inicio = input("       Ingrese la fecha de inicio de la tarea (aaaa-mm-dd): ")
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_vencimiento = input("       Ingrese la fecha de vencimiento de la tarea (aaaa-mm-dd): ")
        fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        estado = input("       Ingrese el estado actual de la tarea: ")
        porcentaje = input("       Ingrese el porcentaje de la tarea: ")

        nueva_tarea = Tarea(id, nombre, empresa_cliente, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje)
        proyecto.tareas.agregar(nueva_tarea)
        print("\n       Tarea agregada con éxito.")

    def insertar_tarea(self, proyecto):
        id = input("\n       Ingrese el ID de la tarea: ")
        nombre = input("       Ingrese el nombre de la tarea: ")
        empresa_cliente = input("       Ingrese la empresa cliente de la tarea: ")
        descripcion = input("       Ingrese la descripción de la tarea: ")
        fecha_inicio = input("       Ingrese la fecha de inicio de la tarea (aaaa-mm-dd): ")
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_vencimiento = input("       Ingrese la fecha de vencimiento de la tarea (aaaa-mm-dd): ")
        fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        estado = input("       Ingrese el estado actual de la tarea: ")
        porcentaje = input("       Ingrese el porcentaje de la tarea: ")
        posicion = int(input("       Ingrese la posición donde insertar la tarea: "))

        nueva_tarea = Tarea(id, nombre, empresa_cliente, descripcion, fecha_inicio, fecha_vencimiento, estado, porcentaje)
        proyecto.tareas.insertar(posicion, nueva_tarea)
        print("\n       Tarea insertada con éxito.")

    def buscar_tarea(self, proyecto, criterio, valor):
        encontrado = False
        for tarea in proyecto.tareas.recorrer():
            try:
                if getattr(tarea, criterio) == valor:
                    return tarea
                encontrado = True
            except AttributeError:
                pass
        if not encontrado:
            print(f"\n       Error: El criterio '{criterio} 'o existe")
            print("       Los criterios existentes son: \n[id, nombre, descripción, fecha_inicio, fecha_vencimiento, estado, empresa_cliente, porcentaje]")
        return None

    def consultar_tarea(self, proyecto):
        # Pedimos que nos ingrese el criterio y valor para buscar la tarea a consultar
        criterio = input("\n       Introduzca el criterio de búsqueda: ")
        valor = input("       Introduzca el valor del criterio: ")
        tarea = self.buscar_tarea(proyecto, criterio.lower(), valor)
        if tarea:
            print("\t"+"-"*42+"\t")
            print(f"\tID: {tarea.id}")
            print(f"\tNombre: {tarea.nombre}")
            print(f"\tDescripción: {tarea.descripcion}")
            print(f"\tFecha de Inicio: {tarea.fecha_inicio.date()}")
            print(f"\tFecha de Vencimiento: {tarea.fecha_vencimiento.date()}")
            print(f"\tEstado: {tarea.estado}")
            print(f"\tEmpresa cliente: {tarea.empresa_cliente}")
            print(f"\tPorcentaje: {tarea.porcentaje}")
            print("\t"+"-"*42+"\t")
        else:
            print("\n\tTarea no encontrada")


    def eliminar_tarea(self, proyecto):
        id = input("       Ingrese el ID de la tarea a eliminar: ")
        for tarea in proyecto.tareas.recorrer():
            if tarea.id == id:
                proyecto.tareas.eliminar(tarea)
                print("\n       Tarea eliminada con éxito.")
                return
        print("\n       Tarea no encontrada.")


    def actualizar_tarea(self, proyecto):
        criterio = input("\n       Introduzca el criterio de búsqueda: ")
        valor = input("       Introduzca el valor del criterio: ")
        tarea_encontrada = self.buscar_tarea(proyecto, criterio, valor)
        if tarea_encontrada:
            print("\n       Tarea encontrada. Ingrese los nuevos valores:")
            tarea_encontrada.nombre = input("       Nombre: ")
            tarea_encontrada.empresa_cliente = input("       Empresa cliente: ")
            tarea_encontrada.descripcion = input("       Descripción: ")
            fecha_inicio = input("       Fecha de inicio (aaaa-mm-dd): ")
            tarea_encontrada.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_vencimiento = input("       Fecha de vencimiento (aaaa-mm-dd): ")
            tarea_encontrada.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
            tarea_encontrada.estado = input("       Estado actual: ")
            tarea_encontrada.porcentaje = input("       Porcentaje: ")
            print("\n       Tarea actualizada con éxito.")
        else:
            print("\n       Tarea no encontrada.")

        #Funciones del menu: "menu_tareas_prioritarias"
    def agregar_tarea_prioritaria(self, proyecto):
        tarea_id = input("\nIngrese el ID de la tarea que desea agregar: ")
        tarea = proyecto.tareas.buscar(tarea_id)
        if tarea is not None:
            tarea_prioritaria = proyecto.tareas_prioritarias.buscar(tarea_id)
            if tarea_prioritaria is None:
                proyecto.tareas_prioritarias.push(tarea)
                print(f"\nSe agregó la tarea '{tarea.nombre}'")
            else:
                print("\nLa tarea ya se encuentra en la lista de tareas prioritarias.")
        else:
            print("\nNo se encontró la tarea especificada")
        

    def eliminar_tarea_prioritaria(self, proyecto):
        if not proyecto.tareas_prioritarias.esta_vacia():
            tarea_id = input("\nIngrese el ID de la tarea que desea eliminar: ")
            tarea_eliminar = None
            actual = proyecto.tareas_prioritarias.cabeza
            while actual is not None:
                if actual.valor.id == tarea_id:
                    tarea_eliminar = actual
                    break
                actual = actual.siguiente
            if tarea_eliminar is not None:
                proyecto.tareas_prioritarias.eliminar(tarea_eliminar)
                print("\nTarea prioritaria eliminada:")
                print("ID:", tarea_eliminar.valor.id)
                print("Nombre:", tarea_eliminar.valor.nombre)
                print("Empresa cliente:", tarea_eliminar.valor.empresa_cliente)
                print("Descripción:", tarea_eliminar.valor.descripcion)
                print("Fecha de inicio:", tarea_eliminar.valor.fecha_inicio.strftime("%Y-%m-%d"))
                print("Fecha de vencimiento:", tarea_eliminar.valor.fecha_vencimiento.strftime("%Y-%m-%d"))
                print("Estado:", tarea_eliminar.valor.estado)
                print("Porcentaje:", tarea_eliminar.valor.porcentaje)
            else:
                print("\nNo se encontró la tarea especificada")
        else:
            print("\nNo hay tareas prioritarias para eliminar.")

    def consultar_tarea_prioritaria(self, proyecto):
        if not proyecto.tareas_prioritarias.esta_vacia():
            tarea = proyecto.tareas_prioritarias.peek()
            print("\nTarea prioritaria:")
            print("ID:", tarea.id)
            print("Nombre:", tarea.nombre)
            print("Empresa cliente:", tarea.empresa_cliente)
            print("Descripción:", tarea.descripcion)
            print("Fecha de inicio:", tarea.fecha_inicio.strftime("%Y-%m-%d"))
            print("Fecha de vencimiento:", tarea.fecha_vencimiento.strftime("%Y-%m-%d"))
            print("Estado:", tarea.estado)
            print("Porcentaje:", tarea.porcentaje)
        else:
            print("\nNo hay tareas prioritarias.")

    def tiempo_total_tareas_prioritarias(self, proyecto):
        if not proyecto.tareas_prioritarias.esta_vacia():
            tareas_prioritarias = []
            while not proyecto.tareas_prioritarias.esta_vacia():
                tarea = proyecto.tareas_prioritarias.pop()
                tareas_prioritarias.append(tarea)
            tarea_duraciones = [(tarea.fecha_vencimiento - tarea.fecha_inicio).days for tarea in tareas_prioritarias]
            total_tiempo = sum(tarea_duraciones)
            print(f"\nTiempo total de tareas prioritarias: {total_tiempo} días")
            for tarea in tareas_prioritarias:
                proyecto.tareas_prioritarias.push(tarea)
        else:
            print("\nNo hay tareas prioritarias para calcular el tiempo total.")
            
        #colas

    def agregar_tareas_proximas_automatico(self):
        today = datetime.today()
        for proyecto in self.lista_proyectos:
            for tarea in proyecto.tareas.recorrer():
                tiempo_restante = (tarea.fecha_vencimiento - today).days
                if tiempo_restante < 15:
                    self.tareas_proximas_a_vencer.encolar(tarea)
    
    def agregar_tareas_proximas_a_vencer(self, proyecto):
        tarea_id = input("\nIngrese el ID de la tarea que desea agregar: ")
        tarea = proyecto.tareas.buscar(tarea_id)
        if tarea is not None:
            proyecto.tareas_proximas_a_vencer.encolar(tarea)
            print(f"\nSe agregó la tarea '{tarea.nombre}'")
        else:
            print("\nNo se encontró la tarea especificada")
            
    def eliminar_tarea_proxima_vencer(self, proyecto):
        if not proyecto.tareas_proximas_a_vencer.esta_vacia():
            tarea_id = input("\nIngrese el ID de la tarea que desea eliminar: ")
            tarea_eliminar = None
            tarea_actual = proyecto.tareas_proximas_a_vencer.cabeza
            while tarea_actual is not None:
                tarea = tarea_actual.valor
                if tarea.id == tarea_id:
                    tarea_eliminar = tarea
                    break
                tarea_actual = tarea_actual.siguiente
            if tarea_eliminar is not None:
                proyecto.tareas_proximas_a_vencer.eliminar(tarea_eliminar)
                print(f"\nSe eliminó la tarea '{tarea_eliminar.nombre}'")
            else:
                print("\nNo se encontró la tarea especificada")
        else:
            print("\nNo hay tareas próximas a vencer.")
    
    def consultar_tarea_proxima_vencer(self, proyecto):
        if not proyecto.tareas_proximas_a_vencer.esta_vacia():
            tarea_actual = proyecto.tareas_proximas_a_vencer.cabeza
            while tarea_actual is not None:
                tarea = tarea_actual.valor
                print("\nTarea próxima a vencer:")
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
            print("\nNo hay tareas próximas a vencer.")

    def tiempo_total_tareas_proximas_vencer(self, proyecto):
        tiempo_total = 0
        cola_copia = Cola()  # Crea una nueva cola
        cola_temporal = Cola()  # Crea una cola temporal
        while proyecto.tareas_proximas_a_vencer.cabeza:
            tarea = proyecto.tareas_proximas_a_vencer.desencolar()
            cola_temporal.encolar(tarea)  # Enqueue el elemento a la cola temporal
            cola_copia.encolar(tarea)  # Enqueue el elemento a la nueva cola
        while cola_copia.cabeza:
            tarea = cola_copia.desencolar()
            delta = tarea.fecha_vencimiento - tarea.fecha_inicio
            tiempo_total += delta.days
        print("\nTiempo total de tareas próximas a vencer:", tiempo_total, "días")
        while cola_temporal.cabeza:  # Devuelve los elementos a la cola original
            tarea = cola_temporal.desencolar()
            proyecto.tareas_proximas_a_vencer.encolar(tarea)
    
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
            self.mostrar_tareas(tareas_encontradas, estado)
        else:
            print(f"\nNo se encontró el proyecto con id {id_proyecto}.")

    def mostrar_tareas(self, tareas):
        if tareas:
            for tarea in tareas:
                print(f"       ID: {tarea.id}, Nombre: {tarea.nombre}, \n          Descripción: {tarea.descripcion}, "
                    f"\n          Estado: {tarea.estado}, \n          Fecha de Inicio: {tarea.fecha_inicio.date()}, "
                    f"\n          Fecha de Vencimiento: {tarea.fecha_vencimiento.date()}")
        else:
            print(f"\nNo se encontraron tareas con estado ")
    
    def ordenar_tareas_por_fecha_inicio(self, proyecto):
        tareas_ordenadas = []
        for tarea in proyecto.tareas.recorrer():
            tareas_ordenadas.append(tarea)
        tareas_ordenadas.sort(key=lambda x: x.fecha_inicio)
        for tarea in tareas_ordenadas:
            print(f"  {tarea.nombre} - {tarea.fecha_inicio.date()}")
            for subtarea in tarea.subtareas:
                print(f"    {subtarea.nombre} - {subtarea.estado}")

    def filtrar_tareas_por_fecha_inicio(self, fecha_inicio_desde, fecha_inicio_hasta):
        tareas_encontradas = [tarea for proyecto in self.lista_proyectos for tarea in proyecto.tareas.recorrer() 
                            if fecha_inicio_desde <= tarea.fecha_inicio <= fecha_inicio_hasta]
        tareas_encontradas.sort(key=lambda x: x.fecha_inicio)
        print(f"\n\t\t\t  Filtrar tareas entre \n\t\t\t{fecha_inicio_desde.date()} y {fecha_inicio_hasta.date()}")
        print("          "+"-"*50)
        self.mostrar_tareas(tareas_encontradas)
        print("          "+"-"*50)

    def filtrar_tareas_por_fecha_vencimiento(self, fecha_vencimiento_desde, fecha_vencimiento_hasta):
        tareas_encontradas = [tarea for proyecto in self.lista_proyectos for tarea in proyecto.tareas.recorrer() 
                            if fecha_vencimiento_desde <= tarea.fecha_vencimiento <= fecha_vencimiento_hasta]
        tareas_encontradas.sort(key=lambda x: x.fecha_vencimiento)
        print(f"\n\t\t\t  Filtrar tareas entre \n\t\t\t{fecha_vencimiento_desde.date()} y {fecha_vencimiento_hasta.date()}")
        print("          "+"-"*50)
        self.mostrar_tareas(tareas_encontradas)
        print("          "+"-"*50)

    def filtrar_tareas_por_fecha_inicio_antes(self, fecha_inicio):
        tareas_encontradas = [tarea for proyecto in self.lista_proyectos for tarea in proyecto.tareas.recorrer() 
                            if tarea.fecha_inicio < fecha_inicio]
        tareas_encontradas.sort(key=lambda x: x.fecha_inicio)
        print(f"\n\t\t  Filtrar tareas antes del {fecha_inicio.date()}")
        print("          "+"-"*50)
        self.mostrar_tareas(tareas_encontradas)
        print("          "+"-"*50)

    def filtrar_tareas_por_fecha_inicio_despues(self, fecha_inicio):
        tareas_encontradas = [tarea for proyecto in self.lista_proyectos for tarea in proyecto.tareas.recorrer() 
                            if tarea.fecha_inicio > fecha_inicio]
        tareas_encontradas.sort(key=lambda x: x.fecha_inicio)
        print(f"\n\t\t  Filtrar tareas despues del {fecha_inicio.date()}")
        print("          "+"-"*50)
        self.mostrar_tareas(tareas_encontradas)
        print("          "+"-"*50)

    #SOLO DE LAS TAREAS DE UN PROYECTO
    def filtrar_tareas_por_fecha_inicio_proy(self, proyecto, fecha_inicio_desde, fecha_inicio_hasta):
        tareas_encontradas = [tarea for tarea in proyecto.tareas.recorrer() 
                            if fecha_inicio_desde <= tarea.fecha_inicio <= fecha_inicio_hasta]
        tareas_encontradas.sort(key=lambda x: x.fecha_inicio)
        print(f"\n\t\t\t  Filtrar tareas entre \n\t\t\t{fecha_inicio_desde.date()} y {fecha_inicio_hasta.date()} \n\t\t    para el proyecto {proyecto.nombre}")
        print("          "+"-"*50)
        self.mostrar_tareas(tareas_encontradas)
        print("          "+"-"*50)

    def filtrar_tareas_por_fecha_vencimiento_proy(self, proyecto, fecha_vencimiento_desde, fecha_vencimiento_hasta):
        tareas_encontradas = [tarea for tarea in proyecto.tareas.recorrer() 
                            if fecha_vencimiento_desde <= tarea.fecha_vencimiento <= fecha_vencimiento_hasta]
        tareas_encontradas.sort(key=lambda x: x.fecha_vencimiento)
        print(f"\n\t\t\t  Filtrar tareas entre \n\t\t\t{fecha_vencimiento_desde.date()} y {fecha_vencimiento_hasta.date()} \n\t\t    para el proyecto {proyecto.nombre}")
        print("          "+"-"*50)
        self.mostrar_tareas(tareas_encontradas)
        print("          "+"-"*50)

    def filtrar_tareas_por_fecha_inicio_antes_proy(self, proyecto, fecha_inicio):
        tareas_encontradas = [tarea for tarea in proyecto.tareas.recorrer() 
                            if tarea.fecha_inicio < fecha_inicio]
        tareas_encontradas.sort(key=lambda x: x.fecha_inicio)
        print(f"\n\t\t  Filtrar tareas antes del {fecha_inicio.date()} \n\t\t    para el proyecto {proyecto.nombre}")
        print("          "+"-"*50)
        self.mostrar_tareas(tareas_encontradas)
        print("          "+"-"*50)

    def filtrar_tareas_por_fecha_inicio_despues_proy(self, proyecto, fecha_inicio):
        tareas_encontradas = [tarea for tarea in proyecto.tareas.recorrer() 
                            if tarea.fecha_inicio > fecha_inicio]
        tareas_encontradas.sort(key=lambda x: x.fecha_inicio)
        print(f"\n\t\t  Filtrar tareas despues del {fecha_inicio.date()} \n\t\t    para el proyecto {proyecto.nombre}")
        print("          "+"-"*50)
        self.mostrar_tareas(tareas_encontradas)
        print("          "+"-"*50)


    
#HASTA AQUI VER SI SE PUEDE METER A CLASE PARA NO SER TANTO CODIGO

    def menu(self):

        while True:
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
            n = input("Seleccione una opción (1-10): ")

            if n == "1":
                self.crear_proyecto()

            elif n == "2":
                self.modificar_proyecto()

            elif n == "3":
                self.consultar_proyecto()

            elif n == "4":
                self.eliminar()

            elif n == "5":
                self.listar_nombres_proyectos()
            
            elif n == "6":
                criterio = input("\nIntroduzca el criterio de búsqueda: ")
                valor = input("Introduzca el valor del criterio: ")
                print(f"\n\tLista de Proyecto por {criterio}: {valor}")
                print("-"*60)
                proyectos = self.buscar_proyecto_filtro(criterio, valor)
                self.consultar(proyectos)

            elif n == "7":
                t = True
                self.listar_nombres_proyectos()
                f = input("\nSeleccione el proyecto si es por id o nombre: ")
                if f == "id":
                    s = input("Ingrese el id del proyecto: ")
                    proyecto_selec = self.buscar_proyecto("id",s)
                elif f == "nombre":
                    s = input("Ingrese el nombre del proyecto: ")
                    proyecto_selec = self.buscar_proyecto("nombre",s)
                else:
                    print("\n       Opción no válida. Por favor, intente de nuevo.")
                    return
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
                    print("       9. Filtrar tareas por fechas")
                    print("       10. Consultar todas las tarear por estado") #tal vez se queda
                    print("       11. Salir al menu principal")

                    op = input("       Seleccione una opción (1-10): ")
                    print("")
                    if op == "1":
                        self.ordenar_tareas_por_fecha_inicio(proyecto_selec)
                    elif op == "2":
                        self.agregar_nuevatarea(proyecto_selec)
                        print(f"\n              Tareas del Proyecto: {proyecto_selec.nombre}")
                        print("     "+"-"*55)
                        tareas = proyecto_selec.tareas.recorrer()
                        self.mostrar_tareas(tareas)
                        print("     "+"-"*55)
                    elif op == "3":
                        self.insertar_tarea(proyecto_selec)
                        print(f"\n              Tareas del Proyecto: {proyecto_selec.nombre}")
                        print("     "+"-"*55)
                        tareas = proyecto_selec.tareas.recorrer()
                        self.mostrar_tareas(tareas)
                        print("     "+"-"*55)

                    elif op == "4":
                        self.eliminar_tarea(proyecto_selec)
                        print(f"\n              Tareas del Proyecto: {proyecto_selec.nombre}")
                        print("     "+"-"*55)
                        tareas = proyecto_selec.tareas.recorrer()
                        self.mostrar_tareas(tareas)
                        print("     "+"-"*55)
                    elif op == "5":
                        self.consultar_tarea(proyecto_selec)
                    elif op == "6":
                        self.actualizar_tarea(proyecto_selec)
                        print(f"\n              Tareas del Proyecto: {proyecto_selec.nombre}")
                        print("     "+"-"*55)
                        tareas = proyecto_selec.tareas.recorrer()
                        self.mostrar_tareas(tareas)
                        print("     "+"-"*55)

                    elif op == "7":
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
                            op = input("          Seleccione una opción (1-5): ")
                            if op == "1":
                                self.agregar_tarea_prioritaria(proyecto_selec)
                            elif op == "2":
                                self.eliminar_tarea_prioritaria(proyecto_selec)
                            elif op == "3":
                                self.consultar_tarea_prioritaria(proyecto_selec)
                            elif op == "4":
                                self.tiempo_total_tareas_prioritarias(proyecto_selec)
                            elif op == "5":
                                print("\n          Saliendo del menu...")
                                cc = False
                            else:
                                print("\n          Opción no válida. Por favor, intente de nuevo.")
                    elif op == "8":
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
                            op = input("       Seleccione una opción (1-5): ")
                            if op == "1":
                                self.agregar_tareas_proximas_a_vencer(proyecto_selec)
                            elif op == "2":
                                self.eliminar_tarea_proxima_vencer(proyecto_selec)
                            elif op == "3":
                                self.consultar_tarea_proxima_vencer(proyecto_selec)
                            elif op == "4":
                                self.tiempo_total_tareas_proximas_vencer(proyecto_selec)
                            elif op == "5":
                                print("\n          Saliendo del menu...")
                                cf = False
                            else:
                                print("\n          Opción no válida. Por favor, intente de nuevo.")
                    
                    elif op == "9":
                        print(f"\n           Filtrar tareas del {proyecto_selec.nombre} por fechas")
                        print("     "+"-"*55)
                        print("       1. Filtrar tareas por fecha de inicio")
                        print("       2. Filtrar tareas por fecha de vencimiento")
                        print("       3. Filtrar tareas por fecha de inicio antes de")
                        print("       4. Filtrar tareas por fecha de inicio después de")
                        print("       5. Salir al menu principal")
                        print("     "+"-"*55)

                        op = input("       Seleccione una opción (1-5): ")
                        if op == "1":
                            fecha_inicio_desde = datetime.strptime(input("          Ingrese la fecha de inicio desde (yyyy-mm-dd): "), "%Y-%m-%d")
                            fecha_inicio_hasta = datetime.strptime(input("          Ingrese la fecha de inicio hasta (yyyy-mm-dd): "), "%Y-%m-%d")
                            self.filtrar_tareas_por_fecha_inicio_proy(proyecto_selec, fecha_inicio_desde, fecha_inicio_hasta)
                        elif op == "2":
                            fecha_vencimiento_desde = datetime.strptime(input("          Ingrese la fecha de vencimiento desde (yyyy-mm-dd): "), "%Y-%m-%d")
                            fecha_vencimiento_hasta = datetime.strptime(input("          Ingrese la fecha de vencimiento hasta (yyyy-mm-dd): "), "%Y-%m-%d")
                            self.filtrar_tareas_por_fecha_vencimiento_proy(proyecto_selec, fecha_vencimiento_desde, fecha_vencimiento_hasta)
                        elif op == "3":
                            fecha_inicio = datetime.strptime(input("          Ingrese la fecha de inicio antes de (yyyy-mm-dd): "), "%Y-%m-%d")
                            self.filtrar_tareas_por_fecha_inicio_antes_proy(proyecto_selec, fecha_inicio)
                        elif op == "4":
                            fecha_inicio = datetime.strptime(input("          Ingrese la fecha de inicio después de (yyyy-mm-dd): "), "%Y-%m-%d")
                            self.filtrar_tareas_por_fecha_inicio_despues_proy(proyecto_selec, fecha_inicio)
                        elif op == "5":
                            print("\n          Saliendo del menu...")
                        else:
                            print("\n          Opción no válida. Por favor, intente de nuevo.")

                    elif op == "10":
                        estado = input("Ingrese el estado a consultar en las tareas")
                        print("")
                        self.consultar_tareas_por_estado(f, estado)

                    elif op == "11":
                        print("\n       Saliendo del menu...")
                        t = False
                    else:
                        print("\n       Opción no válida. Por favor, intente de nuevo.")
                    
            elif n == "8":
                self.filtrar_todas_tareas_por_estado()
            elif n == "9":
                
                print("\n                   Filtrar tareas por fechas")
                print("     "+"-"*55)
                print("       1. Filtrar tareas por fecha de inicio")
                print("       2. Filtrar tareas por fecha de vencimiento")
                print("       3. Filtrar tareas por fecha de inicio antes de")
                print("       4. Filtrar tareas por fecha de inicio después de")
                print("       5. Salir al menu principal")
                print("     "+"-"*55)

                op = input("       Seleccione una opción (1-5): ")
                if op == "1":
                    fecha_inicio_desde = datetime.strptime(input("          Ingrese la fecha de inicio desde (yyyy-mm-dd): "), "%Y-%m-%d")
                    fecha_inicio_hasta = datetime.strptime(input("          Ingrese la fecha de inicio hasta (yyyy-mm-dd): "), "%Y-%m-%d")
                    self.filtrar_tareas_por_fecha_inicio(fecha_inicio_desde, fecha_inicio_hasta)
                elif op == "2":
                    fecha_vencimiento_desde = datetime.strptime(input("          Ingrese la fecha de vencimiento desde (yyyy-mm-dd): "), "%Y-%m-%d")
                    fecha_vencimiento_hasta = datetime.strptime(input("          Ingrese la fecha de vencimiento hasta (yyyy-mm-dd): "), "%Y-%m-%d")
                    self.filtrar_tareas_por_fecha_vencimiento(fecha_vencimiento_desde, fecha_vencimiento_hasta)
                elif op == "3":
                    fecha_inicio = datetime.strptime(input("          Ingrese la fecha de inicio antes de (yyyy-mm-dd): "), "%Y-%m-%d")
                    self.filtrar_tareas_por_fecha_inicio_antes(fecha_inicio)
                elif op == "4":
                    fecha_inicio = datetime.strptime(input("          Ingrese la fecha de inicio después de (yyyy-mm-dd): "), "%Y-%m-%d")
                    self.filtrar_tareas_por_fecha_inicio_despues(fecha_inicio)
                elif op == "5":
                    print("\n          Saliendo del menu...")
                else:
                    print("\n          Opción no válida. Por favor, intente de nuevo.")

            elif n =="10":
                return

            elif n == "11":

                print("\nSaliendo del programa...")
                break
                

            else:
                print("\nOpción no válida. Por favor, intente de nuevo.")
                

#Luego veo si lo optimizo, lo importante es que funcione :D

pro = Configuracion("C:/Users/fches/OneDrive/Documents/Python/Algoritmo/Evaluacion 4/config.txt") #Metan los archivos .json y .txt en la misma carpeta del proyecto y cambien las rutas
pross = pro.mostrar_datos()

manager = ProyectoManager(pross)
manager.menu()
pross = manager.lista_proyectos

#pro.guardar_datos(pross)
# --- Módulos ---
import numpy as np  # Para manejar matrices y operaciones numéricas
import os  # Para operaciones del sistema, como limpiar la pantalla
import heapq  # Para implementar una cola de prioridad en el algoritmo de Dijkstra

# --- Clase Grafo ---
class Grafo:
    def __init__(self):
        """Inicializa el grafo con nodos vacíos y matrices de conexión y peso vacías."""
        self.nodos = []  # Lista para almacenar los nombres de los nodos
        self.matriz_conexion = np.array([])  # Matriz para representar la conexión entre nodos
        self.matriz_peso = np.array([])  # Matriz para representar el peso de los arcos
        self._actualizar_matrices()  # Llama a la función para inicializar matrices vacías

    def _actualizar_matrices(self):
        """Actualiza las matrices de conexión y peso según la cantidad de nodos."""
        n = len(self.nodos)  # Obtiene el número de nodos
        self.matriz_conexion = np.zeros((n, n), dtype=int)  # Inicializa la matriz de conexiones con ceros
        self.matriz_peso = np.full((n, n), float('inf'))  # Inicializa la matriz de pesos con infinito
        np.fill_diagonal(self.matriz_peso, 0)  # La distancia a sí mismo es 0

    def agregar_arcos(self):
        """Permite al usuario agregar arcos al grafo, creando nodos si es necesario."""
        while True:
            origen = input("\nIngrese el nodo de origen: ").strip()  # Solicita el nodo de origen
            destino = input("Ingrese el nodo de destino: ").strip()  # Solicita el nodo de destino

            # Agrega el nodo de origen si no existe
            if origen not in self.nodos:
                print(f"\nEl nodo '{origen}' no existe. Se agregará automáticamente.")
                self.nodos.append(origen)  # Añade el nodo a la lista de nodos
                self._actualizar_matrices()  # Actualiza las matrices

            # Agrega el nodo de destino si no existe
            if destino not in self.nodos:
                print(f"El nodo '{destino}' no existe. Se agregará automáticamente.")
                self.nodos.append(destino)  # Añade el nodo a la lista de nodos
                self._actualizar_matrices()  # Actualiza las matrices

            # Obtiene los índices de los nodos en la lista
            i, j = self.nodos.index(origen), self.nodos.index(destino)

            # Verifica si ya existe el arco
            if self.matriz_conexion[i][j] == 1:
                print(f"\nEl arco de {origen} a {destino} ya existe.")
            elif self.matriz_conexion[j][i] == 1:
                print(f"\nNo se pueden agregar arcos inversos. El arco de {destino} a {origen} ya existe.")
            else:
                peso = float(input("Ingrese el peso del arco: ").strip())  # Solicita el peso del arco
                if peso < 0:
                    print("\nEl peso debe ser un valor no negativo.")  # Valida que el peso no sea negativo
                    continue
                self.matriz_conexion[i][j] = 1  # Marca la conexión en la matriz
                self.matriz_peso[i][j] = peso  # Establece el peso en la matriz
                print(f"\nArco de {origen} a {destino} con peso {peso} agregado correctamente.")

            # Pregunta si desea agregar otro arco
            if input("\n¿Desea agregar otro arco? (s/n): ").strip().lower() != 's':
                break  # Sale del bucle si el usuario no desea agregar más arcos

    def modificar_nodo_y_peso(self):
        """Permite al usuario modificar el nombre de un nodo o el peso de un arco existente."""
        while True:
            # Pregunta al usuario qué desea modificar
            accion = input("\n¿Desea modificar (N)ombre de nodo o (P)eso de arco? (n/p): ").strip().lower()
            if accion == 'n':  # Modificación de nombre de nodo
                nombre_actual = input("\nIngrese el nombre del nodo a modificar: ").strip()  # Solicita el nombre del nodo actual
                if nombre_actual in self.nodos:  # Verifica si el nodo existe
                    nuevo_nombre = input("\nIngrese el nuevo nombre para el nodo: ").strip()  # Solicita el nuevo nombre
                    self.nodos[self.nodos.index(nombre_actual)] = nuevo_nombre  # Cambia el nombre en la lista
                    print(f"\nNombre del nodo '{nombre_actual}' cambiado a '{nuevo_nombre}'.")
                    self._actualizar_matrices()  # Actualiza las matrices
                else:
                    print("\nEl nodo no existe.")  # Informa que el nodo no fue encontrado

            elif accion == 'p':  # Modificación de peso de arco
                nodo_origen = input("\nIngrese el nodo de origen del arco a modificar: ").strip()  # Solicita el origen del arco
                nodo_destino = input("Ingrese el nodo de destino del arco a modificar: ").strip()  # Solicita el destino del arco

                if nodo_origen in self.nodos and nodo_destino in self.nodos:  # Verifica si ambos nodos existen
                    i, j = self.nodos.index(nodo_origen), self.nodos.index(nodo_destino)  # Obtiene los índices
                    if self.matriz_conexion[i][j] == 1:  # Verifica si existe el arco
                        nuevo_peso = float(input(f"\nIngrese el nuevo peso para el arco de {nodo_origen} a {nodo_destino}: ").strip())  # Solicita el nuevo peso
                        self.matriz_peso[i][j] = nuevo_peso  # Actualiza el peso en la matriz
                        print(f"\nPeso del arco de {nodo_origen} a {nodo_destino} modificado a {nuevo_peso}.")
                    else:
                        print(f"\nNo existe un arco de {nodo_origen} a {nodo_destino}.")  # Informa que no hay arco
                else:
                    print("\nUno o ambos nodos no existen.")  # Informa que uno de los nodos no fue encontrado
            else:
                print("\nOpción no válida.")  # Informa que la opción es inválida

            # Pregunta si desea realizar otra modificación
            if input("\n¿Desea realizar otra modificación? (s/n): ").strip().lower() != 's':
                break  # Sale del bucle si el usuario no desea más modificaciones

    def imprimir_matriz(self):
        """Imprime las matrices de adyacencia de conexión y peso del grafo."""
        print("\nMatriz de Adyacencia - Conexión:")
        print("   ", " ".join(self.nodos))  # Imprime los nombres de los nodos como encabezado
        for i, fila in enumerate(self.matriz_conexion):  # Itera sobre las filas de la matriz de conexión
            print(self.nodos[i], " ".join(map(str, fila)))  # Imprime cada fila con el nombre del nodo correspondiente
        
        print("\nMatriz de Adyacencia - Peso:")
        print("   ", " ".join(self.nodos))  # Imprime los nombres de los nodos como encabezado
        for i, fila in enumerate(self.matriz_peso):  # Itera sobre las filas de la matriz de peso
            print(self.nodos[i], " ".join(map(lambda x: f"{x:.1f}" if x != float('inf') else '∞', fila)))  # Imprime cada fila, mostrando '∞' para infinito

    def calcular_camino_mas_corto(self):
        """Calcula el camino más corto entre dos nodos usando el algoritmo de Dijkstra."""
        print("\nNodos ingresados:", ', '.join(self.nodos))  # Muestra los nodos ingresados
        origen = input("\nIngrese el nodo de origen: ").strip()  # Solicita el nodo de origen
        destino = input("Ingrese el nodo de destino: ").strip()  # Solicita el nodo de destino
        
        # Verifica si los nodos existen
        if origen not in self.nodos or destino not in self.nodos:
            print("\nEl nodo de origen o destino no existe.")  # Informa si alguno de los nodos no existe
            return
        
        print(f"\nCalculando el camino más corto de {origen} a {destino}...")
        num_nodos = len(self.nodos)  # Obtiene el número total de nodos
        distancias = {nodo: float('inf') for nodo in self.nodos}  # Inicializa distancias a infinito
        distancias[origen] = 0  # La distancia desde el origen a sí mismo es 0
        cola_prioridad = [(0, origen)]  # Cola de prioridad para almacenar los nodos a visitar
        camino = {nodo: None for nodo in self.nodos}  # Diccionario para rastrear el camino
        visitados = set()  # Conjunto para almacenar nodos visitados

        while cola_prioridad:  # Mientras haya nodos en la cola
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)  # Extrae el nodo con la distancia más corta
            if nodo_actual in visitados:  # Verifica si ya fue visitado
                continue  # Si fue visitado, pasa al siguiente

            visitados.add(nodo_actual)  # Marca el nodo como visitado
            
            # Recorre los nodos vecinos
            for i in range(num_nodos):
                if self.matriz_conexion[self.nodos.index(nodo_actual)][i] == 1:  # Verifica si hay conexión
                    peso = self.matriz_peso[self.nodos.index(nodo_actual)][i]  # Obtiene el peso del arco
                    distancia_nueva = distancia_actual + peso  # Calcula la nueva distancia
                    # Si la nueva distancia es menor que la registrada, actualiza
                    if distancia_nueva < distancias[self.nodos[i]]:
                        distancias[self.nodos[i]] = distancia_nueva  # Actualiza la distancia
                        camino[self.nodos[i]] = nodo_actual  # Actualiza el camino
                        heapq.heappush(cola_prioridad, (distancia_nueva, self.nodos[i]))  # Agrega el nodo a la cola

        distancia_final = distancias[destino]  # Obtiene la distancia final al nodo destino
        if distancia_final == float('inf'):
            print(f"\nNo hay un camino desde {origen} a {destino}.")  # Informa si no hay camino
        else:
            print(f"\nLa distancia más corta de {origen} a {destino} es {distancia_final:.1f}.")  # Muestra la distancia
            self._mostrar_camino(camino, origen, destino)  # Muestra el camino más corto

    def _mostrar_camino(self, camino, origen, destino):
        """Muestra el camino más corto desde el nodo de origen hasta el nodo de destino."""
        camino_recorrido = []  # Lista para almacenar el camino recorrido
        nodo_actual = destino  # Comienza desde el nodo destino
        while nodo_actual is not None:  # Mientras haya nodos en el camino
            camino_recorrido.append(nodo_actual)  # Agrega el nodo al camino recorrido
            nodo_actual = camino[nodo_actual]  # Avanza al nodo anterior en el camino
        camino_recorrido.reverse()  # Invierte el camino para mostrarlo desde origen a destino
        # Calcula el peso total del camino
        peso_total = sum(self.matriz_peso[self.nodos.index(camino_recorrido[i])][self.nodos.index(camino_recorrido[i + 1])] for i in range(len(camino_recorrido) - 1))
        print(" -> ".join(camino_recorrido), f"con un peso total de {peso_total:.1f}")  # Muestra el camino y el peso total

    def limpiar_pantalla_y_esperar(self):
        """Limpia la pantalla y espera que el usuario presione Enter para continuar."""
        input("\nPresione Enter para continuar...")  # Espera que el usuario presione Enter
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la pantalla según el sistema operativo

# --- Función del Menú ---
def menu():
    """Muestra el menú principal y gestiona las interacciones del usuario."""
    grafo = Grafo()  # Crea una instancia de la clase Grafo
    while True:
        print("\n=================== DIJKSTRA ==================\n")
        print("1. Mostrar matrices de adyacencia y gestionar grafo")
        print("2. Calcular camino más corto (Dijkstra)")
        print("3. Salir")

        opcion = input("Seleccione una opción: ").strip()  # Solicita la opción del menú
        
        if opcion == '1':  # Opción para mostrar matrices de adyacencia
            while True:
                grafo.imprimir_matriz()  # Muestra las matrices
                accion = input("\n¿Desea (A)gregar arcos, (M)odificar nodos y pesos o (S)alir? (a/m/s): ").strip().lower()
                if accion == 'a':
                    grafo.agregar_arcos()  # Llama a la función para agregar arcos
                elif accion == 'm':
                    grafo.modificar_nodo_y_peso()  # Llama a la función para modificar nodos y pesos
                elif accion == 's':
                    break  # Sale del bucle si el usuario elige salir
                else:
                    print("\nOpción no válida. Por favor, elija 'A', 'M' o 'S'.")  # Informa si la opción es inválida

                # Pregunta si desea ver las matrices después de cada modificación
                if input("\n¿Desea ver las matrices de nuevo? (s/n): ").strip().lower() == 's':
                    grafo.imprimir_matriz()  # Muestra las matrices nuevamente
                    grafo.limpiar_pantalla_y_esperar()  # Limpia la pantalla y espera a que el usuario continúe

        elif opcion == '2':  # Opción para calcular el camino más corto
            grafo.calcular_camino_mas_corto()  # Llama a la función para calcular el camino más corto
            grafo.limpiar_pantalla_y_esperar()  # Limpia la pantalla y espera a que el usuario continúe

        elif opcion == '3':  # Opción para salir
            print("\nSaliendo del programa...")  # Informa que se está saliendo
            break  # Sale del bucle principal

        else:
            print("\nOpción no válida. Por favor, seleccione una opción del 1 al 3.")  # Informa si la opción es inválida
            grafo.limpiar_pantalla_y_esperar()  # Limpia la pantalla y espera a que el usuario continúe

# --- Punto de entrada del programa ---
if __name__ == '__main__':
    menu()  # Llama a la función del menú para iniciar el programa

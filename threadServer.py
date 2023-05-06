# !/usr/bin/env python3

import socket
import sys
import threading

# Maneja todas las conexiones entrantes
def servirPorSiempre(socketTcp, listaconexiones):
    # Se ejecuta un bucle infinito
    try:
        while True:
            client_conn, client_addr = socketTcp.accept() # Espera a que los clientes se conecten
            print("Conectado a", client_addr) # Imprime que cliente se conectó
            listaconexiones.append(client_conn) # Lo agrega a la lista de conexiones

            # Para cada cliente que se conecta se crea un hilo
            #   Invoca la función recibir_datos() para manejar la comunicación de los datos
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
            thread_read.start()
            gestion_conexiones(listaConexiones) # Se llama para gestionar la lista de conexiones y eliminar las conexiones inactivas
    except Exception as e:
        print(e)

#Gestiona la lista de conexiones y elimina las conexiones inactivas
def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn) # Elimina las conexiones inactivas
    print("hilos activos:", threading.active_count()) # Imprimimos los hilos activos
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones)) # Imprimimos las conexiones que tenemos en el arreglo "listaconexiones"
    print(listaconexiones) # Imprime las conexiones

# Recibe los datos enviados por los clientes y se les envia una respuesta
def recibir_datos(conn, addr):
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name)) # Imprimimos que cliente nos lo esta enviando y con que hilo
        while True:
            data = conn.recv(1024) # Esperamos a recibir el dato
            response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
            if not data: # Si no se recibe ningun dato termina la cominicación
                print("Fin.")
                break
            conn.sendall(response) # Le envia un mensaje al cliente

    # Si ocurre alguna excepción durante la comunicación se cierra la conexión
    except Exception as e:
        print(e)
    finally:
        conn.close()


# Arreglo de la lista de conexiones
listaConexiones = []

# Aquí se le asigna el host y el puerto
host, port, numConn = sys.argv[1:4]

# Aquí nos muestra el host y puerto que se está usando
if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

# Aquí guardamos el host y el puertp
serveraddr = (host, int(port))

# Creamos un socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones)
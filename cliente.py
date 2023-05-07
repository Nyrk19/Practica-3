#!/Library/Frameworks/Python.framework/Versions/3.11/bin python3

import socket
import time
import json
import pickle

#HOST = "127.0.0.1"  # The server's hostname or IP address
#HOST = "192.168.0.110"

#   Defiimos el puerto
PORT = 65432  # The port used by the server
HOST = input("Ingresa el host: ")

#   Tamaño de buffer
buffer_size = 2048
principiante = (9, 9, 10)
avanzado = (16, 16, 40)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT)) # Connect necesita la información del nodo al que se va a conectar y el puerto
    print("Usuario conectado")
    #   Recibe la bienvenida y que nivel quiere el usuario
    data = TCPClientSocket.recv(buffer_size) # Se bloquea hasta que no se reciva algun dato
    print(data.decode())
    dificultad=str(input()) # Almacena en la variable dificultad la dificultad que quiere el usuario
    # Le envia la dificultad al servidor
    TCPClientSocket.sendall(dificultad.encode()) #   Encode() sirve para convertir una cadena de caracteres en un conjunto de bytes

    # En caso de que el cliente haya escogido el nivel principiante
    if dificultad == "p" or dificultad == "P":
        print("Dificultad principiante") # Imprime el nivel que escogio
        filas, columnas, minas = principiante # # Se asignara a fila = 9, columna = 9 y minas = 10

        #Declaramos variables
        gano = 0
        perdio = 0
        mismo = 0
        bandera = 0
        tiempo = time.time() # Esto nos permitira iniciar el tiempo, para al final cuanto tiempo duro el juego

        # Las instrucciones se repetiran hasta que la variable gano o perdio sean diferentes a 1
        while gano != 1 or perdio != 1:

            # El cliente recibe la matriz en forma de tablero
            data = TCPClientSocket.recv(buffer_size).decode()
            if mismo == 0:
                print(data) # Imprimimos el tablero
            else:
                mismo = 0


            #Imprimimos las instrucciones
            print("Ingresa la coordenada de la casilla que quiere abrir")

            # Guarda en la variable columna lo ingresado por el cliente
            columna = input("Ingresa la columna (puede ser: A B C D E F G H I): ")

            # Se envia al servidor lo ingresado por el cliente
            TCPClientSocket.sendall(columna.encode())

            # Imprimimos instrucciones y guarda en la variable fila lo ingresado por el cliente
            fila = input("Ingresa la fila (puede ser: 1, 2, 3, 4, 5, 7, 8, 9): ")

            # Se envia al servidor lo ingresado por el cliente
            TCPClientSocket.sendall(fila.encode())

            #mensaje = TCPClientSocket.recv(buffer_size)  # Se bloquea hasta que no se reciva algun dato
            #print(mensaje)

            # Se recibe una p, g o s para saber si gano perido o sigue el juego
            data = TCPClientSocket.recv(buffer_size).decode()
            # En caso de que el cliente haya perdido
            if data == "p":
                print("Perdiste")
                perdio = 1
                break
            elif data == "g":
                print("Ganaste")
                gano = 1
                break
            else:
                print("Sigue tu puedes!!")


    elif dificultad == "a" or dificultad == "A":
        filas, columnas, minas = principiante

        gano = 0
        perdio = 0
        mismo = 0
        bandera = 0
        tiempo = time.time()
        while gano != 1 or perdio != 1:

            # Recibe el tablero
            data = TCPClientSocket.recv(buffer_size).decode()
            if mismo == 0:
                print(data)  # Imprimimos el tablero
            else:
                mismo = 0

            print("Ingresa la coordenada de la casilla que quiere abrir")
            columna = input("Ingresa la columna (puede ser: A, B, C, D, E, F, G, H, I, J, K, L, M, N, Ñ, O): ")
            TCPClientSocket.sendall(columna.encode())

            fila = input("Ingresa la fila (puede ser: 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16) : ")
            TCPClientSocket.sendall(fila.encode())

            mensaje = TCPClientSocket.recv(buffer_size)  # Se bloquea hasta que no se reciva algun dato
            print(mensaje)

            data = TCPClientSocket.recv(buffer_size).decode()
            if data == "p":
                print("Perdiste")
                perdio = 1
                break
            elif data == "g":
                print("Ganaste")
                gano = 1
                break
            elif data == "m":
                print("Esta casilla ya fue abierta, escoja otra")
                mismo = 1
            else:
                print("Sigue tu puedes!!")

    else:
        print("Esta opción no existe")

    print("El juego ha terminado \n") # Imprimira que el juego ha terminado
    print("Duración del juego:", time.time() - tiempo, "segundos") # Se imprimira la duración del juego
    print("Gracias por jugar")
    TCPClientSocket.close()

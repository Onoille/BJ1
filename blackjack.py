import os
import random 

def existeArchivo(destinacion):
    if os.path.exists(destinacion):
        print("Archivo ya existe")
        return True
    return False

def crearArchivo(destinacion):
    with open(destinacion, "x"):
        pass
    return open(destinacion, "a")

def quitarLineasFantasma():
    with open("Usuarios.txt", "r") as archivo:
        lineas = [linea.strip() for linea in archivo.readlines() if linea.strip()]

    with open("Usuarios.txt", "w") as archivo:
        archivo.write("\n".join(lineas))

def registrarCuenta():
    nombre = input("Nombre de la cuenta: ")
    contra = input("Contra de la cuenta: ")

    with open("Usuarios.txt", "r") as usuarios:
        for line in usuarios.readlines():
            nombreE = line.split("/")[0]
            if nombre == nombreE:
                print("YA EXISTE UNA CUENTA CON ESE NOMBRE")
                return False

    with open("Usuarios.txt", "a") as usuarios:
        usuarios.write(f"\n{nombre}/{contra}/100/0/user")
    print("CUENTA CREADA!")
    return True

def iniciarSesion():
    nombre = input("Nombre de la cuenta: ")
    contra = input("Contra de la cuenta: ")

    quitarLineasFantasma()

    with open("Usuarios.txt", "r") as usuarios:
        for line in usuarios.readlines():
            nombreE, contraA = line.split("/")[:2]
            print(line, nombreE, contraA)
            if nombreE == nombre and contra == contraA:
                print("SESION INICIADA!")
                return nombreE

    print("NO EXISTE NINGUNA CUENTA CON ESE NOMBRE O LA CONTRASE;A ES INCORRECTA!")
    return False

def obtenerDatosCuenta(cuenta):
    with open("Usuarios.txt", "r") as usuarios:
        for line in usuarios.readlines():
            datos = line.strip().split("/")
            nombre = datos[0]
            if cuenta == nombre:
                return datos

def actualizarDatoCuenta(cuenta, indice, nuevo_valor):
    with open("Usuarios.txt", "r") as usuarios:
        lineas = usuarios.readlines()

    for i in range(len(lineas)):
        datos = lineas[i].strip().split("/")
        nombre = datos[0]
        if cuenta == nombre:
            datos[indice] = str(nuevo_valor)
            lineas[i] = "/".join(datos) + "\n"

    with open("Usuarios.txt", "w") as archivo:
        archivo.writelines(lineas)

def cambiarPrecioFichas(precio):
    with open("precio.txt", "w") as archivo:
        archivo.write(precio)

def precioFichas():
    with open("precio.txt", "r") as archivo:
        precio = int(archivo.readline())
    return precio

def actualizarFichas(cuenta, cantidad):
    nuevoDinero = int(dineroCuenta(cuenta)) - (cantidad * precioFichas())
    nuevasFichas = cantidad + int(fichasCuenta(cuenta))

    cambiarDinero(cuenta, nuevoDinero)
    cambiarFichas(cuenta, nuevasFichas)

    return True

def dineroCuenta(cuenta):
    return obtenerDatosCuenta(cuenta)[2]

def fichasCuenta(cuenta):
    return obtenerDatosCuenta(cuenta)[3]

def rolCuenta(cuenta):
    return obtenerDatosCuenta(cuenta)[4]

def cambiarDinero(cuenta, cantidad):
    actualizarDatoCuenta(cuenta, 2, cantidad)

def cambiarFichas(cuenta, cantidad):
    actualizarDatoCuenta(cuenta, 3, cantidad)

while not existeArchivo("Usuarios.txt"):
    crearArchivo("Usuarios.txt")

while not existeArchivo("precio.txt"):
    crearArchivo("precio.txt")

import random

class Partida:
    def __init__(self):
        self.Baraja = Baraja()
        self.Jugador = Jugador()
        self.Croupier = Croupier()
        self.PartidaAcabada = False
        self.Empate = False
        self.CasaGana = False
        self.Blackjack = False

        self.Baraja.Generar()
        self.Baraja.Mezclar()

        self.DarCarta(True)
        self.ActualizarEstado()
        self.DarEstado()

        self.DarCarta(False)
        self.ActualizarEstado()
        self.DarEstado()

    def DarCarta(self, AJugador: bool):
        Carta = self.Baraja.DarCarta()

        if AJugador:
            self.Jugador.Carta(Carta)
            print(f"Has sacado un {Carta}")
            return self.Jugador.Mano
        
        print(f"El croupier a sacado un {Carta}")
        self.Croupier.Carta(Carta)
        return self.Croupier.Mano
    
    def ActualizarEstado(self):
        self.Jugador.Actualizar()
        self.Croupier.Actualizar()
        self.Logica()

    def DarEstado(self):
        print(f"Jugador: {self.Jugador.Valor}\nCroupier: {self.Croupier.Valor}")

    def Logica(self):
        if self.Jugador.Valor == 21 and len(self.Jugador.Mano) == 2:
            self.CasaGana = False
            self.Blackjack = True
            self.PartidaAcabada = True
            return True

        if self.Jugador.Valor > 21:
            self.CasaGana = True
            self.Blackjack = False
            self.PartidaAcabada = True
            return False
        
        if self.Croupier.Valor == 21 and len(self.Croupier.Mano) == 2:
            self.CasaGana = True
            self.Blackjack = True
            self.PartidaAcabada = True
            return True
        
        if self.Croupier.Valor > 21:
            self.CasaGana = False
            self.Blackjack = False
            self.PartidaAcabada = True
            return True

        if self.Croupier.Valor >= 17 and self.Jugador.Valor > self.Croupier.Valor and self.Jugador.Valor <= 21:
            self.CasaGana = False
            self.Blackjack = False
            self.PartidaAcabada = True
            return True
        
        if self.Croupier.Valor >= 17 and self.Jugador.Valor < self.Croupier.Valor and self.Croupier.Valor <= 21:
            self.CasaGana = True
            self.Blackjack = False
            self.PartidaAcabada = True
            return False

        if self.Croupier.Valor >= 17 and self.Jugador.Valor == self.Croupier.Valor and self.Croupier.Valor <= 21:
            self.Empate = True
            self.PartidaAcabada = True
            return False
        
        return False

    def Vocal(self):
        if self.Empate:
            print("Empate!")
            return

        if not self.CasaGana and self.Blackjack:
            print("Has ganado con un blackjack!")
            return
        
        if self.CasaGana and self.Blackjack:
            print("Has perdido la casa tiene un blackjack!")
            return

        if self.CasaGana and not self.Blackjack:
            print("La casa gana!")
            return

        if not self.CasaGana and not self.Blackjack:
            print("Has ganado!")
            return

class Jugador:
    def __init__(self):
        self.Mano = []
        self.Valor = 0

    def Carta(self, Carta):
        self.Mano.append(Carta)
    
    def Actualizar(self):
        self.Valor = 0

        for Valor in self.Mano:
            self.Valor += Valor

        return self.Valor
    
class Croupier:
    def __init__(self):
        self.Mano = []
        self.Valor = 0
    
    def Carta(self, Carta):
        self.Mano.append(Carta)

    def Actualizar(self):
        self.Valor = 0

        for Valor in self.Mano:
            self.Valor += Valor
            
        return self.Valor

class Baraja():
    def __init__(self):
        self.Cartas = []

    def Generar(self):
        NumeroDeBarajas = random.randint(1, 8)
        NumeroDeCartas = 13
        TipoDeCartas = 4
        
        for i in range(NumeroDeBarajas):
            for j in range(TipoDeCartas):
                for k in range(NumeroDeCartas):
                    if (k + 2) > 11:
                        Valor = 10
                        self.Cartas.append(Valor)
                    else:
                        self.Cartas.append(k + 2)

        return self.Cartas
    
    def Mezclar(self):
        random.shuffle(self.Cartas)
        return self.Cartas
    
    def DarCarta(self):
        Carta = self.Cartas.pop(0)
        return Carta

existe = True
login = False
cuenta = ""

while existe:
    while not login:
        print("""
    
        L PARA INICIAR SESION EN UNA CUENTA
        R PARA CREAR UNA CUENTA
        E PARA SALIR

        """)
        eleccion = input("QUE QUIERES HACER?").lower()

        if eleccion == "e":
            existe = False

        if eleccion == "r":
            registrarCuenta()

        if eleccion == "l":
            cuenta = iniciarSesion()

            if cuenta != "":
                break

            if cuenta == False:
                existe = False
                break

            
    if not existe:
        break
    login = True

    # AQUI COMIENZA EL MENU
    rolUsuario = rolCuenta(cuenta)

    if rolUsuario == "admin":
        print("""
            
            J PARA EMPEZAR UNA PARTIDA
            M PARA MIRAR EL DINERO QUE TIENES
            F PARA MIRAR LAS FFICHAS QUE TIENES
            C PARA COMPRAR FICHAS
            P PARA CAMBIAR EL PRECIO DE LAS FICHAS
            E PARA SALIR

        """)
    elif rolUsuario == "user":
        print("""
            
            J PARA EMPEZAR UNA PARTIDA
            M PARA MIRAR EL DINERO QUE TIENES
            F PARA MIRAR LAS FFICHAS QUE TIENES
            C PARA COMPRAR FICHAS
            E PARA SALIR

        """)

    eleccion = input("QUE QUIERES HACER?").lower()

    if eleccion == "e":
        print(cuenta)
        existe = False

    if eleccion == "m":
        print(f"Tienes: {dineroCuenta(cuenta)}$ euros!")
    if eleccion == "f":
        print(f"Tienes: {fichasCuenta(cuenta)} fichas!")
    if eleccion == "p" and rolUsuario == "admin":
        nuevoPrecio = input("Elige un nuevo precio para las fichas: ")
        cambiarPrecioFichas(nuevoPrecio)
    if eleccion == "c":
        cantidad = int(input("Cuantas fichas quieres comprar?"))

        if (cantidad * precioFichas()) <= int(dineroCuenta(cuenta)):
            actualizarFichas(cuenta, cantidad)
            print("Gracias por comprar :)")
        else:
            print("No tienes suficiente dinero para comprar")

    if eleccion == "j":
        Partida = Partida()

        while not Partida.PartidaAcabada:
            print("""

                H Para una carta
                S Para parar

            """)

            eleccion = input("Que eliges?").lower()

            if eleccion == "h":
                Partida.DarCarta(True)
                Partida.ActualizarEstado()
                Partida.DarEstado()
                if Partida.PartidaAcabada:
                    Partida.Vocal()
                    
            elif eleccion == "s":
                while not Partida.PartidaAcabada:
                    Partida.DarCarta(False)

                    Partida.ActualizarEstado()
                    if Partida.PartidaAcabada: 
                        Partida.Vocal()
                        break

                    Partida.DarEstado()

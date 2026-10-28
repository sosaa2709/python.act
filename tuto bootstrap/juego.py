import random

class Personaje:
    def __init__(self, nombre, vida):
        self.nombre = nombre
        self.vida = vida

    def atacar(self, enemigo):
        daño = random.randint(10, 100)
        enemigo.vida -= daño
        print(f"{self.nombre} ataca a {enemigo.nombre} y hace {daño} de daño.")
        if enemigo.vida <= 0:
            enemigo.vida = 0
            print(f"{enemigo.nombre} quedó sin vida.")

    def mostrar_vida(self):
        print(f"{self.nombre}: {self.vida} vida")

jugador = Personaje("Maiton", 100)
enemigo = Personaje("Sosa", 100)

while jugador.vida > 0 and enemigo.vida > 0:
    jugador.atacar(enemigo)
    if enemigo.vida <= 0:
        break

    enemigo.atacar(jugador)
    jugador.mostrar_vida()
    enemigo.mostrar_vida()

if jugador.vida > 0:
    print("¡Ganaste!")
else:
    print("¡Perdiste!")
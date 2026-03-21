"""

Juego "Othello"

El estado se va a representar como una lista de 64 elementos, tal que

0  1   2  3  4  5  6  7
8  9  10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63

Y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del jugador 1 y -1
es una ficha del jugador 2.

Las acciones son (se deben cumplir ambas condiciones):
- Poner una ficha que sea adyacente a la ficha del oponente.
- Que en algun punto en alguna direccion en un numero n de casillas este una ficha del
mismo color.

Un estado terminal se podría dar en los siguientes casos:
- Cuando no hay fichas vacias.
- Ambos jugadores ya no tienen acciones legales.

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un empate.

"""

import juegos_simplificado as js
import minimax


class Otelo(js.JuegoZT2):
    def inicializa(self):
        s = [0 for _ in range(8*8)]

        s[27] = -1
        s[28] = 1
        s[35] = -1
        s[36] = 1

        return tuple(s)

    def jugadas_legales(self, s, j):
        jugadas = []
        oponente = -j
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),  # Arriba
            (0, -1), (0, 1),  # Lados
            (1, -1), (1, 0), (1, 1)  # Abajo
        ]

        for pos in range(64):
            if s[pos] != 0:
                continue

            fila = pos // 8
            col = pos % 8

            for df, dc in direcciones:
                f = fila + df
                c = col + dc
                contrarias = 0

                while 0 <= f < 8 and 0 <= c < 8 and s[f * 8 + c] == oponente:
                    contrarias += 1
                    f += df
                    c += dc

                if contrarias > 0 and 0 <= f < 8 and 0 <= c < 8 and s[f * 8 + c] == j:
                    jugadas.append(pos)
                    break

        return jugadas if jugadas else [None]

    def sucesor(self, s, a, j):
        s = list(s[:])
        for i in range(5, -1, -1):
            if s[a + 7 * i] == 0:
                s[a + 7 * i] = j
                break
        return tuple(s)

    def ganancia(self, s):
        total = sum(s)

        if total > 0:
            return 1

        if total < 0:
            return -1

        return 0

    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0


class InterfaceConecta4(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el estado del juego, se puede usar la función pprint_conecta4
        para mostrar el estado de forma más amigable

        """
        a = [' X ' if x == 1 else ' O ' if x == -1 else '   ' for x in s]
        print('\n 0 | 1 | 2 | 3 | 4 | 5 | 6')
        for i in range(6):
            print('|'.join(a[7 * i:7 * (i + 1)]))
            print('---+---+---+---+---+---+---\n')

    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego, se puede usar " XO"[g] para mostrar el
        ganador de forma más amigable

        """
        if g != 0:
            print("Gana el jugador " + " XO"[g])
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
        print("Jugador", " XO"[j])
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada


def ordena_centro(jugadas, jugador):
    """
    Ordena las jugadas de acuerdo a la distancia al centro
    """
    return sorted(jugadas, key=lambda x: abs(x - 3))


def nueva_estrategia(ventana):
    puntos = 0
    fichas1 = ventana.count(1)
    fichas2 = ventana.count(-1)
    vacias = ventana.count(0)

    if fichas1 == 3 and vacias == 1:
        puntos += 0.1
    elif fichas1 == 2 and vacias == 2:
        puntos += 0.02

    if fichas2 == 3 and vacias == 1:
        puntos -= 0.1
    elif fichas2 == 2 and vacias == 2:
        puntos -= 0.02

    return puntos


def evalua_3con(s):
    puntos = 0

    col = [s[3 + 7 * i] for i in range(6)]
    puntos += col.count(1) * 0.05
    puntos -= col.count(-1) * 0.05

    for i in range(6):
        for j in range(4):
            ventana = [s[7 * i + j + k] for k in range(4)]
            puntos += nueva_estrategia(ventana)
    for i in range(7):
        for j in range(3):
            ventana = [s[i + 7 * (j + k)] for k in range(4)]
            puntos += nueva_estrategia(ventana)
    for i in range(4):
        for j in range(3):
            ventana = [s[i + 7 * j + 8 * k] for k in range(4)]
            puntos += nueva_estrategia(ventana)
    for i in range(4):
        for j in range(3):
            ventana = [s[i + 7 * j + 3 + 6 * k] for k in range(4)]
            puntos += nueva_estrategia(ventana)

    if puntos >= 1.0: return 0.99
    if puntos <= -1.0: return -0.99

    return puntos


if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",  # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Negamax",  # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 6,
        "tiempo": 10,
        "ordena": ordena_centro,  # Puede ser None o una función f(jugadas, j) -> lista de jugadas ordenada
        "evalua": evalua_3con  # Puede ser None o una función f(estado) -> número entre -1 y 1
    }


    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        elif cadena == "Negamax":
            return minimax.JugadorNegamax(
                ordena=cfg["ordena"], d=cfg["profundidad máxima"], evalua=cfg["evalua"]
            )
        elif cadena == "Tiempo":
            return minimax.JugadorNegamaxIterativo(
                tiempo=cfg["tiempo"], ordena=cfg["ordena"], evalua=cfg["evalua"]
            )
        else:
            raise ValueError("Jugador no reconocido")


    interfaz = InterfaceConecta4(
        Conecta4(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("El Juego del Conecta 4 ")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])
    print()

    interfaz.juega()
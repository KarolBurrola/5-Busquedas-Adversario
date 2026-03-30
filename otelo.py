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
Donde:
- Jugador 1: Fichas negras  (1)   <- Es el que comienza el juego
- Jugador 2: Fichas blancas (-1)

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
        if a is None:
            return s

        tablero = list(s)

        tablero[a] = j
        oponente = -j

        fila = a // 8
        col = a % 8

        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for df, dc in direcciones:
            f = fila + df
            c = col + dc
            voltear = []

            while 0 <= f < 8 and 0 <= c < 8 and tablero[f * 8 + c] == oponente:
                voltear.append(f * 8 + c)
                f += df
                c += dc

            if len(voltear) > 0 and 0 <= f < 8 and 0 <= c < 8 and tablero[f * 8 + c] == j:

                for pos in voltear:
                    tablero[pos] = j

        return tuple(tablero)

    def ganancia(self, s):
        total = sum(s)

        if total > 0:
            return 1

        if total < 0:
            return -1

        return 0

    def terminal(self, s):
        # Si el tablero está completamente lleno -- ACABA
        if 0 not in s:
            return True

        # Si ninguno de los jugadores puede hacer un movimiento -- ACABA
        if self.jugadas_legales(s, 1) == [None] and self.jugadas_legales(s, -1) == [None]:
            return True

        return False


class InterfaceOtelo(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el estado del juego, en este caso, "Otelo"

        """
        a = [' ● ' if x == 1 else ' ○ ' if x == -1 else '   ' for x in s]

        print('\n   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |')
        print('---+---+---+---+---+---+---+---+---+')

        for i in range(8):
            fila_texto = f" {i} |" + "|".join(a[8 * i:8 * (i + 1)]) + "|"
            print(fila_texto)
            print('---+---+---+---+---+---+---+---+---+')

    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego, en este caso decidí colocar
        los símbolos (bolitas)

        """
        bolitas = {1: '1 (Fichas negras) ● ', -1: '2 (Fichas blancas) ○ '}

        if g != 0:
            print("Gana el jugador " + bolitas[g])
        else:
            print("Un asqueroso empate")


    def jugador_humano(self, s, j):
        jugadas = list(self.juego.jugadas_legales(s, j))

        if jugadas == [None]:
            print("\n Te quedaste sin más jugadas legales.")
            input("Presiona enter para ceder tu turno al siguiente oponente")
            return None

        print("\nJugador", "● (Negras)" if j == 1 else "○ (Blancas)")
        print("Jugadas legales:", jugadas)

        jugada = -1
        while jugada not in jugadas:
            try:
                jugada = int(input("Jugada: "))
            except ValueError:
                print("Por favor, ingresa un número válido.")

        return jugada

# Asignando pesos estratégicos a la matriz
pesos = [
        100, -20, 15, 5, 5, 15, -20, 100,
        -20, -30, -5, -5, -5, -5, -30, -20,
        15, -5, 10, 2, 2, 10, -5, 15,
        5, -5, 2, 1, 1, 2, -5, 5,
        5, -5, 2, 1, 1, 2, -5, 5,
        15, -5, 10, 2, 2, 10, -5, 15,
        -20, -30, -5, -5, -5, -5, -30, -20,
        100, -20, 15, 5, 5, 15, -20, 100
    ]

def ordena_otelo(jugadas, j):
    """
    Heurística que recibe la lista de movimientos legales y los ordena de mayor a menor valor
    estratégico observando la matriz de pesos y además optimiza el algoritmo donde la poda
    alfa-beta explora los mejores escenarios y descarta los peores
    """

    if None in jugadas:
        return jugadas

    jugadas = sorted(jugadas, key=lambda pos: pesos[pos], reverse=True)

    return jugadas


def evalua_otelo(s):
    """
    Heurística que calcula el estado del tablero usando una matriz de pesos donde cada casilla
    tiene un valor definido el cual penaliza las casillas adyacentes para no darle ventaja al
    oponente
    """

    score1 = 0
    score2 = 0

    for i in range(64):
        if s[i] == 1:
            score1 += pesos[i]
        elif s[i] == -1:
            score2 += pesos[i]

    diferencia = score1 - score2

    ms = 1000.0

    if diferencia == 0:
        return 0.0

    ev = diferencia / ms

    if ev >= 1.0: return 0.99
    if ev <= -1.0: return -0.99

    return ev


if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",  # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Negamax",  # Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 6,
        "tiempo": 10,
        "ordena": ordena_otelo,  # Puede ser None o una función f(jugadas, j) -> lista de jugadas ordenada
        "evalua": evalua_otelo  # Puede ser None o una función f(estado) -> número entre -1 y 1
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


    interfaz = InterfaceOtelo(
        Otelo(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("\n" + "-" * 40)
    print("          --- O T H E L L O ---")
    print("-" * 40)
    print("Jugador 1 (Negras):", cfg["Jugador 1"])
    print("Jugador 2 (Blancas):", cfg["Jugador 2"])
    print()

    interfaz.juega()
# -*- coding: utf-8 -*-
"""
CLUE-LITE (5 CASOS) - Consola
Autor: Equipo del curso / (Plantilla generada)
Licencia: MIT

Requisitos: Python 3.8+
Ejecución: python main.py

Descripción breve:
- Al iniciar, el juego elige ALEATORIAMENTE 1 de 5 casos predefinidos (culpable, arma, locación + narrativa).
- Puedes listar sospechosos, locaciones y armas.
- Comando "sugerir": propones una terna (sospechoso, arma, locación) y recibes una pista contextual de ese caso.
- Comando "acusar": si aciertas exactamente la terna correcta, ganas y aparece el final narrativo del caso.
- Tienes hasta 8 intentos (sugerencias + acusaciones). Una acusación incorrecta también consume intento.
- Comando "pistas": muestra las pistas que ya se revelaron.
- Comando "ayuda": muestra los comandos.
- Comando "salir": termina la partida.

Objetivo académico:
- Simular la mecánica básica de Clue con un conjunto finito (5) de historias/ﬁnales,
  enlazadas al caso elegido al azar al iniciar la partida.
"""
import random
import sys

SUSPECTOS = [
    "Dra. Valeria Cruz (Médica)",
    "Ing. Mateo Torres (Ingeniero)",
    "Chef Luna Martínez (Chef)",
    "Sr. Bruno Salgado (Empresario)",
    "Agente Sofía Ríos (Detective privada)"
]

LOCACIONES = [
    "Biblioteca",
    "Cocina",
    "Habitación del hotel",
    "Jardín",
    "Laboratorio"
]

ARMAS = [
    "Candelabro",
    "Cuchillo",
    "Llave inglesa",
    "Veneno",
    "Pistola"
]

# Definimos 5 CASOS (culpable, arma, locación, pistas[], final)
# Nota: Solo estos 5 combos son válidos para "acertar" en esta práctica.
CASOS = [
    {
        "id": 1,
        "culpable": "Dra. Valeria Cruz (Médica)",
        "arma": "Veneno",
        "locacion": "Laboratorio",
        "pistas": [
            "Se encontraron matraces con residuos ácidos en el fregadero, pero solo uno tenía restos de alcaloides.",
            "La víctima discutió con alguien que conocía bien de toxicología.",
            "Un par de guantes desechables faltan de la caja, y la bata tiene manchas que no son de sangre."
        ],
        "final": (
            "FINAL 1 — LA FORMULA AMARGA\n"
            "La Dra. Valeria Cruz manipuló una muestra en el laboratorio y añadió veneno al té de la víctima. "
            "Creyó que el amargor se ocultaría con azúcar, pero la cristalería con trazas la delató."
        )
    },
    {
        "id": 2,
        "culpable": "Ing. Mateo Torres (Ingeniero)",
        "arma": "Llave inglesa",
        "locacion": "Jardín",
        "pistas": [
            "En el césped quedaron marcas de rodilla y de una herramienta pesada.",
            "Un tornillo de acero inoxidable cayó cerca de la fuente; no pertenece al mobiliario del jardín.",
            "Alguien apagó la iluminación exterior desde el tablero auxiliar."
        ],
        "final": (
            "FINAL 2 — LA PALANCA SILENCIOSA\n"
            "El Ing. Mateo Torres salió al jardín con una llave inglesa. Cortó la iluminación del patio, "
            "sorprendió a la víctima junto a la fuente y la golpeó. El tornillo extraviado cerró el caso."
        )
    },
    {
        "id": 3,
        "culpable": "Chef Luna Martínez (Chef)",
        "arma": "Cuchillo",
        "locacion": "Cocina",
        "pistas": [
            "Un cuchillo de chef falta del taco de cuchillos y el paño de cocina huele a cloro.",
            "La cámara frigorífica registra una apertura breve justo a la hora del incidente.",
            "Harina en el suelo revela dos pares de pisadas, una se detiene en seco."
        ],
        "final": (
            "FINAL 3 — CORTE PERFECTO\n"
            "La Chef Luna Martínez confrontó a la víctima en la cocina. Tras la discusión, tomó su cuchillo "
            "favorito y la herida limpia delató un golpe decidido. El rastro en la harina la puso en la escena."
        )
    },
    {
        "id": 4,
        "culpable": "Sr. Bruno Salgado (Empresario)",
        "arma": "Pistola",
        "locacion": "Biblioteca",
        "pistas": [
            "Un libro cayó del estante al nivel de un escondite donde cabría una pistola compacta.",
            "En la alfombra hay partículas de cordita apenas perceptibles.",
            "La puerta de la biblioteca tiene marcas recientes de que fue cerrada por dentro."
        ],
        "final": (
            "FINAL 4 — PÁGINAS DE PÓLVORA\n"
            "El Sr. Bruno Salgado citó a la víctima en la biblioteca. Disparó a corta distancia y ocultó "
            "el arma tras un tomo hueco. La cordita en la alfombra contó el resto."
        )
    },
    {
        "id": 5,
        "culpable": "Agente Sofía Ríos (Detective privada)",
        "arma": "Candelabro",
        "locacion": "Habitación del hotel",
        "pistas": [
            "El candelabro del pasillo presenta una abolladura y cera reciente.",
            "El registro del ascensor indica subidas y bajadas en un lapso de dos minutos.",
            "El letrero de 'No molestar' se colocó al revés desde el interior."
        ],
        "final": (
            "FINAL 5 — SOMBRAS EN EL PISO 7\n"
            "La Agente Sofía Ríos atrajo a la víctima a la habitación del hotel. La golpeó con el candelabro "
            "y salió antes de que el pasillo se llenara. El letrero invertido la delató."
        )
    }
]

INTENTOS_MAX = 8

def banner():
    print("="*60)
    print("               C L U E  —  L I T E   (5 casos)")
    print("="*60)
    print("Comandos: lista, sugerir, acusar, pistas, ayuda, salir")
    print("- Usa 'lista' para ver sospechosos, locaciones y armas.")
    print("- 'sugerir' revela una pista contextual del caso en juego.")
    print("- 'acusar' evalúa si adivinaste exactamente la terna.")
    print("- Máximo de intentos (sugerencias + acusaciones):", INTENTOS_MAX)
    print("="*60)

def mostrar_listas():
    print("\nSospechosos:")
    for s in SUSPECTOS:
        print(" -", s)
    print("\nLocaciones:")
    for l in LOCACIONES:
        print(" -", l)
    print("\nArmas:")
    for a in ARMAS:
        print(" -", a)
    print()

def pedir_terna(tipo):
    print(f"\n[{tipo.upper()}] Escribe tal cual aparece en las listas.")
    sospe = input(" Sospechoso: ").strip()
    arma   = input(" Arma: ").strip()
    lugar  = input(" Locación: ").strip()
    return sospe, arma, lugar

def validar_terna(s, a, l):
    ok = True
    if s not in SUSPECTOS:
        print("  > Sospechoso no válido.")
        ok = False
    if a not in ARMAS:
        print("  > Arma no válida.")
        ok = False
    if l not in LOCACIONES:
        print("  > Locación no válida.")
        ok = False
    return ok

def comparar_terna(caso, s, a, l):
    # Devuelve (acierto_total, aciertos_parciales_dict)
    acierto_total = (s == caso["culpable"] and a == caso["arma"] and l == caso["locacion"])
    parciales = {
        "sospechoso": (s == caso["culpable"]),
        "arma": (a == caso["arma"]),
        "locacion": (l == caso["locacion"])
    }
    return acierto_total, parciales

def juego():
    random.seed()  # semilla por tiempo
    caso = random.choice(CASOS)
    pistas_reveladas = []  # índices de pistas ya dadas
    intentos = 0

    banner()
    # DEBUG opcional:
    # print(f"[DEBUG] Caso: {caso['culpable']} / {caso['arma']} / {caso['locacion']}")

    while True:
        if intentos >= INTENTOS_MAX:
            print("\nTe quedaste sin intentos. ¡Fin de la partida!")
            print("La solución era:")
            print(f"  Culpable:  {caso['culpable']}")
            print(f"  Arma:      {caso['arma']}")
            print(f"  Locación:  {caso['locacion']}")
            print("\nPuedes reiniciar el juego ejecutando nuevamente 'python main.py'")
            return

        cmd = input("\n> ").strip().lower()

        if cmd == "lista":
            mostrar_listas()

        elif cmd == "ayuda":
            banner()

        elif cmd == "pistas":
            if not pistas_reveladas:
                print("  (Sin pistas aún. Usa 'sugerir' para obtener una.)")
            else:
                print("\nPistas reveladas:")
                for i in pistas_reveladas:
                    print(f" - {caso['pistas'][i]}")

        elif cmd == "sugerir":
            s, a, l = pedir_terna("sugerir")
            if not validar_terna(s, a, l):
                continue
            intentos += 1
            acierto_total, parciales = comparar_terna(caso, s, a, l)

            # Elegimos una pista no repetida del caso (si quedan)
            idxs = [i for i in range(len(caso["pistas"])) if i not in pistas_reveladas]
            if idxs:
                nuevo = random.choice(idxs)
                pistas_reveladas.append(nuevo)
                pista = caso["pistas"][nuevo]
            else:
                pista = "No hay nuevas pistas; intenta 'acusar' si crees tener la solución."

            print("\nResultado de tu sugerencia:")
            print(f"  Sospechoso {'CORRECTO' if parciales['sospechoso'] else 'incorrecto'}")
            print(f"  Arma       {'CORRECTA' if parciales['arma'] else 'incorrecta'}")
            print(f"  Locación   {'CORRECTA' if parciales['locacion'] else 'incorrecta'}")
            print(f"  Pista: {pista}")

        elif cmd == "acusar":
            s, a, l = pedir_terna("acusar")
            if not validar_terna(s, a, l):
                continue
            intentos += 1
            acierto_total, parciales = comparar_terna(caso, s, a, l)
            if acierto_total:
                print("\n¡ACERTASTE LA TERNA!")
                print("-"*60)
                print(caso["final"])
                print("-"*60)
                print("Caso resuelto en", intentos, "intentos.")
                return
            else:
                print("\nTu acusación es incorrecta.")
                print("Sugerencia: usa 'sugerir' para obtener más pistas antes de acusar.")

        elif cmd == "salir":
            print("Gracias por jugar. ¡Hasta luego!")
            return

        else:
            print("Comando no reconocido. Escribe 'ayuda' para ver opciones.")

if __name__ == "__main__":
    try:
        juego()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
        sys.exit(0)

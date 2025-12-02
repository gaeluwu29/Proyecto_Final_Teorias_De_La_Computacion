def modo_afd():
    print("\n--- MODO AFD ---")

    alfabeto = [x.strip() for x in input("Alfabeto (a,b): ").split(',')]
    estados = [x.strip() for x in input("Estados (q0,q1): ").split(',')]
    inicio = input("Estado inicial: ").strip()
    finales = [x.strip() for x in input("Estados finales: ").split(',')]

    transiciones = {}
    print("Transiciones (q0,a,q1). Escribe 'fin' para terminar.")
    while True:
        t = input()
        if t == "fin":
            break

        partes = [x.strip() for x in t.split(',')]
        if len(partes) != 3:
            print("⚠ Formato incorrecto. Usa: origen,simbolo,destino")
            continue

        o, s, d = partes
        transiciones[(o, s)] = d

    while True:
        palabra = input("\nPalabra a probar (o 'salir'): ")
        if palabra == "salir":
            break

        estado = inicio
        valido = True

        for letra in palabra:
            if (estado, letra) in transiciones:
                estado = transiciones[(estado, letra)]
            else:
                valido = False
                break

        if valido and estado in finales:
            print(f"✓ '{palabra}' ES ACEPTADA")
        else:
            print(f"✗ '{palabra}' NO es aceptada")

def modo_gramatica_regular():
    print("\n--- MODO GRAMÁTICA REGULAR ---")

    producciones = {}
    print("Producciones (S->aA|b). Escribe 'fin' para terminar.")
    while True:
        p = input()
        if p == "fin":
            break

        if "->" not in p:
            print("⚠ Formato: S->aA|b")
            continue

        izq, der = p.split("->")
        producciones[izq.strip()] = [x.strip() for x in der.split('|')]

    while True:
        cad = input("\nCadena a probar (o 'salir'): ")
        if cad == "salir":
            break

        if pertenece_rg("S", producciones, cad):
            print(f"✓ '{cad}' PERTENECE")
        else:
            print(f"✗ '{cad}' NO pertenece")


def pertenece_rg(actual, producciones, objetivo):
    if actual == objetivo:
        return True

    if actual not in producciones:
        return False

    for prod in producciones[actual]:
        # Caso terminal solo
        if prod == objetivo:
            return True

        # Forma típica: aA
        if len(prod) >= 2 and prod[0].islower():
            if objetivo.startswith(prod[0]):
                return pertenece_rg(prod[1:], producciones, objetivo[1:])

    return False

def modo_glc():
    print("\n--- MODO GLC ---")

    producciones = {}
    print("Producciones (S->aSb|e). Escribe 'fin' para terminar.")
    while True:
        p = input()
        if p == "fin":
            break

        if "->" not in p:
            print("⚠ Formato: S->aSb|e")
            continue

        izq, der = p.split("->")
        producciones[izq.strip()] = [x.strip() for x in der.split('|')]

    while True:
        cadena = input("\nCadena a derivar (o 'salir'): ")
        if cadena == "salir":
            break

        print("\nDerivación por izquierda:")
        mostrar_derivacion("S", producciones)

        print("\nÁrbol sintáctico:")
        mostrar_arbol_simple(cadena)


def mostrar_derivacion(actual, producciones):
    print("→", actual)
    if actual in producciones:
        for prod in producciones[actual]:
            print("→", prod)


def mostrar_arbol_simple(cadena):
    # Solo imprime si es tipo a^n b^n
    if cadena.count("a") != cadena.count("b"):
        print("Árbol no disponible para esta cadena.")
        return

    print("    S")
    print("   / \\")
    print("  a   b")
    print("   \\ /")
    print("    S (simplificado)")

def modo_automata_pila():
    print("\n--- MODO AUTÓMATA DE PILA ---")

    estados = [x.strip() for x in input("Estados: ").split(',')]
    alfabeto = [x.strip() for x in input("Alfabeto: ").split(',')]
    inicio = input("Estado inicial: ").strip()
    pila_ini = input("Símbolo inicial pila: ").strip()
    finales = [x.strip() for x in input("Estados finales: ").split(',')]

    transiciones = []
    print("Transiciones (q0,a,Z,q1,aZ). Escribe 'fin'.")
    while True:
        t = input()
        if t == "fin":
            break

        partes = [x.strip() for x in t.split(',')]
        if len(partes) != 5:
            print("⚠ Formato incorrecto.")
            continue

        transiciones.append(partes)

    while True:
        cadena = input("\nCadena a simular (o 'salir'): ")
        if cadena == "salir":
            break

        simular_ap(inicio, cadena, pila_ini, transiciones, finales)


def simular_ap(estado, cadena, simb_pila, transiciones, finales):
    pila = [simb_pila]
    pos = 0

    print("\nSimulación:")
    while True:
        entrada = cadena[pos:] if pos < len(cadena) else "ε"
        print(f"Estado: {estado}, Entrada: {entrada}, Pila: {pila}")

        mov = None

        for q, leer, top, q2, rep in transiciones:

            cond_leer = (leer == "ε" or (pos < len(cadena) and leer == cadena[pos]))
            cond_pila = (pila and pila[-1] == top)

            if estado == q and cond_leer and cond_pila:
                mov = (q2, leer, rep)
                break

        if mov is None:
            break

        q2, leer, rep = mov
        if leer != "ε":
            pos += 1

        pila.pop()
        if rep != "ε":
            for s in reversed(rep):
                pila.append(s)

        estado = q2

        if pos > len(cadena) + 2:
            break

    if estado in finales:
        print("✓ CADENA ACEPTADA")
    else:
        print("✗ CADENA RECHAZADA")

def modo_maquina_turing():
    print("\n--- MÁQUINA DE TURING ---")

    estados = [x.strip() for x in input("Estados: ").split(',')]
    alfabeto = [x.strip() for x in input("Alfabeto: ").split(',')]
    inicio = input("Estado inicial: ").strip()
    blanco = input("Símbolo blanco: ").strip() or "_"
    finales = [x.strip() for x in input("Estados finales: ").split(',')]

    trans = {}
    print("Transiciones (q0,0,q1,1,R). Escribe 'fin'.")
    while True:
        t = input()
        if t == "fin":
            break

        partes = [x.strip() for x in t.split(',')]
        if len(partes) != 5:
            print("⚠ Formato incorrecto.")
            continue

        q, leer, q2, esc, mov = partes
        trans[(q, leer)] = (q2, esc, mov)

    while True:
        cad = input("\nCadena en cinta (o 'salir'): ")
        if cad == "salir":
            break

        simular_turing(inicio, cad, blanco, trans, finales)


def simular_turing(estado, cadena, blanco, trans, finales):
    cinta = list(cadena)
    pos = 0

    print("\nSimulación:")
    for paso in range(50):

        while pos >= len(cinta):
            cinta.append(blanco)

        vista = cinta.copy()
        vista[pos] = "[" + vista[pos] + "]"
        print("Paso", paso, "Estado:", estado, "Cinta:", "".join(vista))

        if estado in finales:
            print("✓ CADENA ACEPTADA")
            return

        s = cinta[pos]

        if (estado, s) not in trans:
            print("✗ SIN TRANSICIÓN → RECHAZADA")
            return

        q2, esc, mov = trans[(estado, s)]
        cinta[pos] = esc

        if mov == "R":
            pos += 1
        elif mov == "L":
            pos = max(0, pos - 1)

        estado = q2

    print("✗ LÍMITE DE PASOS")

def main():
    print("=== SISTEMA SIMPLE DE TEORÍA DE LA COMPUTACIÓN ===")

    while True:
        print("\n1. AFD")
        print("2. Gramática Regular")
        print("3. GLC")
        print("4. Autómata de Pila")
        print("5. Máquina de Turing")
        print("6. Salir")

        op = input("Opción: ")

        if op == "1": modo_afd()
        elif op == "2": modo_gramatica_regular()
        elif op == "3": modo_glc()
        elif op == "4": modo_automata_pila()
        elif op == "5": modo_maquina_turing()
        elif op == "6":
            print("Adiós.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()


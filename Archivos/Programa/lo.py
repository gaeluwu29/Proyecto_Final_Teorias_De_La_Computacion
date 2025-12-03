class Nodo:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.hijos = []

# esta parte sirve para imprimir los arboles
def imprimir_arbol(nodo, prefijo="", ultimo=True):
    rama = "└── " if ultimo else "├── "
    simbolo_mostrar = "λ" if nodo.simbolo == "" else nodo.simbolo
    print(prefijo + rama + simbolo_mostrar)
    prefijo += "    " if ultimo else "│   "
    for i, hijo in enumerate(nodo.hijos):
        imprimir_arbol(hijo, prefijo, i == len(nodo.hijos) - 1)


def parsear(simbolo, palabra, producciones, cache=None):
    if cache is None:
        cache = {}

    clave = (simbolo, palabra)
    if clave in cache:
        return cache[clave]

    nodo = Nodo(simbolo)

    if simbolo == "" or not simbolo.isupper():
        if simbolo == "":
            resultado = (nodo, palabra)
            cache[clave] = resultado
            return resultado
        elif palabra.startswith(simbolo):
            resultado = (nodo, palabra[len(simbolo):])
            cache[clave] = resultado
            return resultado
        cache[clave] = None
        return None

    for prod in producciones.get(simbolo, []):
        resto = palabra
        hijos = []
        ok = True

        for s in prod:
            resultado = parsear(s, resto, producciones, cache)
            if resultado is None:
                ok = False
                break
            hijo, resto = resultado
            hijos.append(hijo)

        if ok:
            nodo.hijos = hijos
            resultado = (nodo, resto)
            cache[clave] = resultado
            return resultado

    cache[clave] = None
    return None


def reemplazar_vacio(entrada):
    if entrada.strip().lower() in ["lambda", "λ", "@", "e", ""]:
        return ""
    return entrada


# Parte del automata finito
def modo_afd():
    print("\n---- Automata Finito ----")

    alfabeto_input = input("Alfabeto (ej: a,b): ").strip()
    alfabeto = [s.strip() for s in alfabeto_input.split(",") if s.strip()]

    estados_input = input("Estados (ej: q0,q1): ").strip()
    estados = [e.strip() for e in estados_input.split(",") if e.strip()]

    inicial = input("Estado inicial: ").strip()
    if inicial not in estados:
        print("No sirve: Estado inicial no valido")
        return

    finales_input = input("Estados de aceptacion (separados por comas): ").strip()
    finales = [f.strip() for f in finales_input.split(",") if f.strip()]

    print("\nTransiciones (estado,símbolo,estado, use @ para λ):")
    transiciones = {}
    while True:
        t = input("Transicion: ").strip()
        if t.lower() == 'fin':
            break

        partes = t.split(",")
        if len(partes) != 3:
            print("No sirve: Formato incorrecto")
            continue

        e1, s, e2 = [p.strip() for p in partes]
        transiciones[(e1, s)] = e2

    # Ahora evaluar palabras multiples veces
    print("\n--- EVALUAR PALABRAS ---")
    print("Escribe palabras para evaluar. Escribe 'fin' para volver al menu.")

    while True:
        palabra = input("\nPalabra a evaluar: ").strip()

        if palabra.lower() == 'fin':
            break

        # Evaluar la palabra
        estado_actual = inicial

        # Procesar transiciones λ iniciales
        while True:
            clave_vacio = (estado_actual, "@")
            if clave_vacio in transiciones:
                estado_actual = transiciones[clave_vacio]
            else:
                break

        i = 0
        aceptada = True

        while i < len(palabra):
            simbolo = palabra[i]

            if simbolo not in alfabeto:
                print(f"No sirve: Simbolo '{simbolo}' no en alfabeto")
                aceptada = False
                break

            clave = (estado_actual, simbolo)

            if clave not in transiciones:
                clave_vacio = (estado_actual, "@")
                if clave_vacio in transiciones:
                    estado_actual = transiciones[clave_vacio]
                    continue
                else:
                    aceptada = False
                    break

            estado_actual = transiciones[clave]
            i += 1

            while True:
                clave_vacio = (estado_actual, "@")
                if clave_vacio in transiciones:
                    estado_actual = transiciones[clave_vacio]
                else:
                    break

        if aceptada:

            while True:
                clave_vacio = (estado_actual, "@")
                if clave_vacio in transiciones:
                    estado_actual = transiciones[clave_vacio]
                else:
                    break

            if estado_actual in finales:
                print("Funciona uwu")
            else:
                print("No pos no funciona :c")
        else:
            print("No pos no funciona :c")


""" parte de la gramatica regular
psdt: Alan, agrega los titulos >:V"""

def modo_gr():
    print("\n---- GRAMÁTICA REGULAR ----")

    producciones = {}

    print("Producciones (A,aB, use @ para λ):")
    while True:
        p = input("> ").strip()
        if p.lower() == 'fin':
            break

        if "," not in p:
            print("No sirve: Formato incorrecto")
            continue

        izq, der = p.split(",", 1)
        izq = izq.strip()
        der = reemplazar_vacio(der.strip())

        if izq not in producciones:
            producciones[izq] = []
        producciones[izq].append(der)

    print("\n--- EVALUAR CADENAS ---")
    print("Escribe cadenas para evaluar. Escribe 'fin' para volver al menu.")

    while True:
        cadena = input("\nCadena a evaluar: ").strip()

        if cadena.lower() == 'fin':
            break

        actual = 'S' if 'S' in producciones else list(producciones.keys())[0]
        i = 0
        exitoso = True

        while i < len(cadena) or (i == len(cadena) and actual != ""):
            simbolo_actual = cadena[i] if i < len(cadena) else None

            if actual not in producciones:
                exitoso = False
                break

            encontrado = False

            for prod in producciones[actual]:
                if prod == "" and i == len(cadena):
                    actual = ""
                    encontrado = True
                    break
                elif prod and simbolo_actual and prod[0] == simbolo_actual:
                    if len(prod) > 1:
                        actual = prod[1:]
                    else:
                        actual = ""
                    i += 1
                    encontrado = True
                    break

            if not encontrado:
                exitoso = False
                break

        if exitoso and i == len(cadena) and actual == "":
            print("Cadena valida")
        else:
            print("Cadena no valida")


#  parte de gramatica libre de contexto
def modo_glc():
    print("\n---- GRAMÁTICA LIBRE DE CONTEXTO ----")

    # Configurar la gramática (una sola vez)
    producciones = {}

    print("Producciones (A,ab|aC, use @ para Vacio):")
    while True:
        p = input("> ").strip()
        if p.lower() == 'fin':
            break

        if "," not in p:
            print("No sirve: Formato incorrecto")
            continue

        izq, der = p.split(",", 1)
        izq = izq.strip()

        if izq not in producciones:
            producciones[izq] = []

        for prod in der.split("|"):
            prod = reemplazar_vacio(prod.strip())
            producciones[izq].append(prod)

    # Ahora derivar palabras multiples veces
    print("\n--- DERIVAR PALABRAS ---")
    print("Escribe palabras para derivar. Escribe 'fin' para volver al menu.")

    while True:
        palabra = input("\nPalabra a derivar: ").strip()

        if palabra.lower() == 'fin':
            break


        simbolo_inicial = 'S' if 'S' in producciones else list(producciones.keys())[0]
        resultado = parsear(simbolo_inicial, palabra, producciones)

        if resultado is None:
            print("No sirve :'c La palabra NO pertenece al lenguaje")
            continue

        arbol, restante = resultado

        if restante != "":
            print("No sirve :'c, La palabra NO pertenece al lenguaje")
            continue

        print("si funciona uwu, la palabra pertenece al lenguaje")
        print("\nArbol de derivacion:")
        imprimir_arbol(arbol)


# Parte de automatas de pila
def modo_ap():
    print("\n---- AUTÓMATA DE PILA ----")
    print("Formato: estado_actual, lee_entrada, lee_pila, nuevo_estado, escribe_pila")
    print("Ejemplo: q0,a,Z,q0,AZ")
    print("Use @ para vacío\n")



    transiciones = {}

    inicial = input("Estado inicial: ").strip()
    pila_inicial = input("Simbolo inicial de pila (Enter para Z): ").strip()
    if not pila_inicial:
        pila_inicial = "Z"

    finales_input = input("Estados finales (separados por comas): ").strip()
    finales = [f.strip() for f in finales_input.split(",") if f.strip()]

    print("\nTransiciones (escribe 'fin' para terminar):")
    while True:
        t = input("> ").strip()
        if t.lower() == 'fin':
            break

        partes = t.split(",")
        if len(partes) != 5:
            print("No sirve: Debe tener 5 partes separadas por coma")
            continue



        estado_actual, lee_entrada, lee_pila, nuevo_estado, escribe_pila = [x.strip() for x in partes]


        lee_entrada = "" if lee_entrada == "@" else lee_entrada
        lee_pila = "" if lee_pila == "@" else lee_pila
        escribe_pila = "" if escribe_pila == "@" else escribe_pila

        transiciones[(estado_actual, lee_entrada, lee_pila)] = (nuevo_estado, escribe_pila)

    print("\n--- PROCESANDO---")
    print("Escribe cadenas para procesar. Escribe 'fin' para volver al menu.")

    while True:
        cadena = input("\nCadena a procesar: ").strip()

        if cadena.lower() == 'fin':
            break

        estado = inicial
        pila = [pila_inicial]
        i = 0
        aceptada = True

        while i <= len(cadena):
            entrada_actual = cadena[i] if i < len(cadena) else ""
            tope_pila = pila[-1] if pila else ""

            transicion_aplicable = None

            if (estado, entrada_actual, tope_pila) in transiciones:
                transicion_aplicable = (estado, entrada_actual, tope_pila)
                i += 1
            elif (estado, "", tope_pila) in transiciones:
                transicion_aplicable = (estado, "", tope_pila)

            if not transicion_aplicable:
                aceptada = False
                break

            nuevo_estado, apilar = transiciones[transicion_aplicable]

            if tope_pila != "":
                pila.pop()

            if apilar != "":
                for simbolo in reversed(apilar):
                    pila.append(simbolo)

            estado = nuevo_estado

            if i == len(cadena) and not any((estado, "", top) in transiciones for top in (pila[-1] if pila else "")):
                break

        if aceptada:
            if finales:
                if estado in finales:
                    print("Funciona uwu")
                else:
                    print("No pos no :'c")
            else:
                if not pila:
                    print("Funciona uwu")
                else:
                    print("No pos no :'c")
        else:
            print("Rechazada")

#   esta es la maquina de turing- Funcionando(creo xd)
def modo_mt():
    print("\n---- MAQUINA DE TURING ----")
    print("Formato: estado,simbolo,nuevoEstado,escribir,movimiento")
    print("Movimientos: D (derecha), I (izquierda), P (parar)")
    print("Símbolo blanco: _\n")

    transiciones = {}

    inicial = input("Estado inicial: ").strip()

    finales_input = input("Estados de aceptacion (separados por comas): ").strip()
    finales = [f.strip() for f in finales_input.split(",") if f.strip()]

    print("\nTransiciones (escribe 'fin' para terminar):")
    while True:
        t = input("> ").strip()
        if t.lower() == 'fin':
            break

        partes = t.split(",")
        if len(partes) != 5:
            print("no sirve: Formato incorrecto")
            continue

        e, s, en, esc, mov = [x.strip() for x in partes]

        if mov not in ['D', 'I', 'P']:
            print("no sirve: Movimiento debe ser D, I o P")
            continue

        transiciones[(e, s)] = (en, esc, mov)

    print("\n--- Cintas ---")
    print("Escribe cintas para procesar. Escribe 'fin' para volver al menu.")

    while True:
        cinta_input = input("\nCinta inicial: ").strip()

        if cinta_input.lower() == 'fin':
            break

        if not cinta_input:
            cinta_input = "_"

        cinta = list(cinta_input)
        posicion = 0
        estado = inicial
        pasos = 0
        max_pasos = 1000
        aceptada = False
        detenida = False

        # Ejecutar
        while pasos < max_pasos and not detenida:
            pasos += 1

            if posicion < 0:
                cinta.insert(0, "_")
                posicion = 0
            elif posicion >= len(cinta):
                cinta.append("_")

            simbolo_actual = cinta[posicion]

            if (estado, simbolo_actual) not in transiciones:
                break

            nuevo_estado, escribir, movimiento = transiciones[(estado, simbolo_actual)]

            cinta[posicion] = escribir
            estado = nuevo_estado

            if movimiento == 'D':
                posicion += 1
            elif movimiento == 'I':
                posicion -= 1
            elif movimiento == 'P':
                detenida = True

            if estado in finales:
                aceptada = True

        if aceptada:
            print("funciona uwu")
        else:
            print("No pos no :'c")

#aqui ta el menu principal
def menu():
    while True:
        print("\n--------------Soluciones Alan's y su pandilla--------------")
        print("[1] AFD")
        print("[2] Gramatica Regular")
        print("[3] GLC")
        print("[4] Automata de Pila")
        print("[5] Maquina de Turing")
        print("[6] Salir")

        op = input("Opcion: ").strip()

        if op == "1":
            modo_afd()
        elif op == "2":
            modo_gr()
        elif op == "3":
            modo_glc()
        elif op == "4":
            modo_ap()
        elif op == "5":
            modo_mt()
        elif op == "6":
            print("Saliendo...")
            break
        else:
            print("No hay xd")


menu()
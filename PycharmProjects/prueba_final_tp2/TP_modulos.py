from TP_procesar_archivos import *
import random
from random import shuffle
import time

#DICCIONARIO PALABRAS
cantidad_repeticiones_palabra = 0
cantidad_letras_palabra = 1
palabra_usada = 2

#DICCIONARIO JUGADORES
orden_jugador = 0
puntaje_jugador = 1
palabra_actual = 2
palabra_a_adivinar = 3
palabra_oculta = 4
letras_acertadas = 5
letras_erradas = 6
ganador_ultima_partida = 7
jugador_eliminado = 8
hombrecito = 9
valor_partes_cuerpo = 10

#PARAMETROS_GENERALES
cant_separacion_entre_palabras = 100

def prorratear(valor):
    #autor: Mauro Cuquejo: Funcion generada para solventar el posible cambio de cantidad de errores. Como el dibujo del
    # hombrecito ahorcado estaba pensado para dibujarse a los siete errores, se decidió dividir el numero maximo de
    # errores por 7 y sacar el resto entero. A cada parte del cuerpo se le asigna el mismo valor entero, excepto a
    # una parte que se elige de forma aleatoria y a la cual se le suma el resto entero.

    lista_valores = [0,0,0,0,0,0,0]
    if valor >= 7:
        resto = valor % 7
        valor_neto = (valor - resto) / 7

        prorr_soga = valor_neto
        prorr_cabeza = valor_neto
        prorr_brazo_izq = valor_neto
        prorr_brazo_der = valor_neto
        prorr_torso = valor_neto
        prorr_pierna_izq = valor_neto
        prorr_pierna_der = valor_neto
        lista_valores = [prorr_soga, prorr_cabeza, prorr_brazo_izq, prorr_brazo_der, prorr_torso, prorr_pierna_izq,
                         prorr_pierna_der]
        valor_random = random.randint(0, len(lista_valores) - 1)
        lista_valores[valor_random] += resto
    elif valor < 7 and valor >= 1:
        final = 6 - valor
        for posicion in range(6, final, -1):
            lista_valores[posicion] = 1
    return(lista_valores)


def dibujar_hombrecito(nro_desaciertos,lista_valores_cuerpo):
    # Autor: Mauro Cuquejo. retorna el gráfico del hombrecito ahorcado, agregando las partes del cuerpo según la cantidad de desaciertos.
    # Se modifico la funcion para que solo dibuje el hombrecito considerando el valor por parte del cuerpo que recibe.
    # Ejemplo: Si una parte del cuerpo vale 2, se dibujara cuando el usuario se haya equivocado 2 veces.
    dibujo = ""
    suma_partes_cuerpo = 0
    posicion = 0
    hombrecito = ["\n | \n | \n", " 0\n", "/", "|", "\ \n", "/", " \ \n"]
    suma_partes_cuerpo += lista_valores_cuerpo[posicion]

    while nro_desaciertos > suma_partes_cuerpo:
        posicion += 1
        suma_partes_cuerpo += lista_valores_cuerpo[posicion]

    for parte_cuerpo in range(posicion+1):
        dibujo += "".join(hombrecito[parte_cuerpo])
    return dibujo


def formatear_palabra(palabra):
    # Autor: Luan Corrionero. recibe una palabra cualquiera y transforma las vocales con acento o las eñes. Retorna la palabra ya corregida.
    dic_a_reemplazar = {"Ñ": "NI", "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U"}
    palabra_vieja = palabra.upper()
    palabra_nueva = ''
    for letra in palabra_vieja:
        if letra not in dic_a_reemplazar:
            palabra_nueva += letra
        else:
            palabra_nueva += dic_a_reemplazar[letra]
    return palabra_nueva


def pausa_para_continuar():
    # Autor: Mauro Cuquejo. Se genera un input que se utilizará durante la partida, para poder visualizar mejor la información. Esto porque cada vez que cambie el turno de un jugador, se limpiará la pantalla.
    # No retorna datos.
    input("presiona Enter para continuar...")
    print("\n" * cant_separacion_entre_palabras)


def mostrar_palabras_ordenadas(diccionario_palabras):
    # Autor: Mauro Cuquejo. Imprime en pantalla el diccionario de palabras, ordenado alfabéticamente por clave. Se muestran en pantalla concatenaciones de cinco palabras, junto con sus repeticiones, cada 0.05 segundos.
    # Al finalizar la muestra,se imprime el excedente de palabras (ya que si no se llegaron a concatenar cinco palabras, no se muestra la concatenación).
    lista_palabras_ordenadas = sorted(diccionario_palabras.keys())
    print("PALABRAS DEL DICCIONARIO y CANTIDAD DE REPETICIONES:")
    auxiliar = ""
    for indice, palabra in enumerate(lista_palabras_ordenadas):
        auxiliar += "Palabras: {} - Cantidad de repeticiones: {} - ".format(palabra, diccionario_palabras[palabra][
            cantidad_repeticiones_palabra])
        if indice % 5 == 0:
            time.sleep(0.05)
            print(auxiliar)
            auxiliar = ""
    if auxiliar != "":
        print(auxiliar)


def generar_diccionario_palabras(long_palabra_min):
    # Autor: Dario Giménez. Se genera un diccionario de palabras con el siguiente formato:
    dic_palabras = {}
    with open(".\\palabras.txt", 'r') as archivo_palabras:
        palabra = leer_archivo(archivo_palabras)
        while palabra != "ZZZ":
            if palabra.isalpha() and len(palabra) >= long_palabra_min:
                if formatear_palabra(palabra) not in dic_palabras:
                    dic_palabras[palabra] = [1, len(palabra), False]
                else:
                    dic_palabras[palabra][cantidad_repeticiones_palabra] += 1
            palabra = leer_archivo(archivo_palabras)
    archivo_palabras.close()

    mostrar_diccionario = input("¿Queres ver las palabras del diccionario? (S/N): ")
    while not mostrar_diccionario.upper() in ("S", "N"):
        mostrar_diccionario = input("Opcion incorrecta. ¿Queres ver las palabras del diccionario? (S/N): ")

    if mostrar_diccionario.upper() == 'S':
        mostrar_palabras_ordenadas(dic_palabras)

    return dic_palabras


def solicitar_cantidad_jugadores(max_usuarios):
    # Autor: Agustin Ramirez. solicita la cantidad de jugadores verificando que este dentro de los parametros del juego.
    # Retorna la cantidad de jugadores.
    continuar = True
    cant_jugadores = input("Ingresa la cantidad de jugadores: ")
    while continuar:
        if not cant_jugadores.isdigit():
            print("Valor incorrecto. La cantidad de jugadores debe ser numérica.")
            cant_jugadores = input("Ingresa la cantidad de jugadores: ")
        elif int(cant_jugadores) < 1 or int(cant_jugadores) > max_usuarios:
            print("Valor incorrecto, la cantidad de jugadores minima es de un jugador y como máximo {}.".format(max_usuarios))
            cant_jugadores = input("Ingresa la cantidad de jugadores: ")
        else:
            continuar = False
    return int(cant_jugadores)


def solicitar_nombre_jugador():
    # Autor: Darío Giménez  solicita el nombre al jugador y verifica que no se usen caracteres incorrectos. Retorna nombre del jugador.
    nombre_jugador = input("Ingresa Nombre para el Jugador: ")
    while not nombre_jugador.replace(" ", "").isalpha():
        nombre_jugador = input("Nombre incorrecto. Ingresa Nombre Jugador: ")
    return nombre_jugador


def generar_diccionario_jugadores(cant_jugadores, max_desaciertos):
    # Autor: Mauro Cuquejo. Recibe cantidad de jugadores, se solicita dicha cantidad de veces el nombre de jugadores.
    # Se valida que los nombres no hayan sido utilizados ya en el diccionario.
    dic_jugadores = {}
    for numero_jugador in range(cant_jugadores):
        jugador = solicitar_nombre_jugador()
        if formatear_palabra(jugador) not in dic_jugadores:
            dic_jugadores[formatear_palabra(jugador)] = [0, 0, [], [], [], [], [], False, False, "", prorratear(max_desaciertos)]
        else:
            while formatear_palabra(jugador) in dic_jugadores:
                print("El nombre ingresado ya fue utilizado por otra persona. Ingresa un nombre distinto.")
                jugador = solicitar_nombre_jugador()
            dic_jugadores[formatear_palabra(jugador)] = [0, 0, [], [], [], [], [], False, False, "", prorratear(max_desaciertos)]
    return dic_jugadores


def otorgar_orden_jugadores_primera_ronda(dic_jugadores, lista_jugadores):
    # Autor: Darío Giménez. Recibe diccionario de jugadores y lista de jugadores. Actualiza el orden en el diccionario de
    # jugadores, para todos los jugadores de manera aleatoria. Se utiliza sólo si es la primera partida.
    # No retorna datos.
    for indice in range(len(lista_jugadores)):
        jugador = lista_jugadores.pop(random.randint(0, len(lista_jugadores) - 1))
        dic_jugadores[jugador][orden_jugador] = indice+1


def separar_ganador_anterior_partida(dic_jugadores, lista_jugadores):
    # Autor: Agustin Ramirez. Recibe diccionario de jugadores y lista de jugadores. Actualiza el diccionario de jugadores,
    # poniendo primero en orden al ganador de la partida anterior. Se utiliza a partir de la segunda partida.
    # No retorna datos.
    condicion = True
    cont = 0
    hubo_ganador = False
    while condicion and cont <= len(lista_jugadores) - 1:
        valor_jugador = lista_jugadores[cont]
        ganador_ult_partida = dic_jugadores[valor_jugador][ganador_ultima_partida]
        if ganador_ult_partida == True:
            dic_jugadores[valor_jugador][orden_jugador] = 1
            lista_jugadores.pop(cont)
            hubo_ganador = True
            condicion = False
        cont += 1
    return hubo_ganador


def otorgar_orden_jugadores_general(dic_jugadores, lista_jugadores, hubo_ganador):
    # Autor: Mauro Cuquejo. Recibe diccionario de jugadores y lista de jugadores. Si sólo juega un jugador, siempre estará
    # en la primera posición. Si juega más de un jugador, primero agrupa por puntaje de mayor a menor.
    # No retorna datos.
    if len(dic_jugadores) == 1:
        dic_jugadores[lista_jugadores[0]][orden_jugador] = 1

    else:

        dic_orden_preliminar = {}
        for indice, jugador in enumerate(lista_jugadores):

            if dic_jugadores[jugador][puntaje_jugador] not in dic_orden_preliminar:
                dic_orden_preliminar[dic_jugadores[jugador][puntaje_jugador]] = [jugador]
            else:
                dic_orden_preliminar[dic_jugadores[jugador][puntaje_jugador]].append(jugador)

        lista_preliminar_ordenada = sorted(dic_orden_preliminar.items(), reverse=True)
        if hubo_ganador:
            cont = 2
        else:
            cont = 1
        for lista_jugadores in lista_preliminar_ordenada:
            cant_jugadores_por_puntaje = len(lista_jugadores[1])
            if cant_jugadores_por_puntaje == 1:
                nombre_jugador = lista_jugadores[1][0]
                dic_jugadores[nombre_jugador][orden_jugador] = cont #reemplazo acá nombre_jugador[0] por nombre_jugador
                cont += 1
            else:
                shuffle(lista_jugadores[1])
                for v_nombre_jugador in lista_jugadores[1]:
                    dic_jugadores[v_nombre_jugador][orden_jugador] = cont
                    cont += 1


def otorgar_orden_jugadores(nro_partida, dic_jugadores):
    # Autor: Mauro Cuquejo
    # primera partida o no. No retorna datos.
    lista_jugadores = list(dic_jugadores.keys())
    if nro_partida == 1:
        otorgar_orden_jugadores_primera_ronda(dic_jugadores, lista_jugadores)
    else:
        hubo_ganador = separar_ganador_anterior_partida(dic_jugadores, lista_jugadores)
        if len(lista_jugadores) > 0:
            otorgar_orden_jugadores_general(dic_jugadores, lista_jugadores, hubo_ganador)


def generar_diccionario_partida(diccionario_partida, nro_partida):
    #Autor: Darío Giménez.
    diccionario_partida[nro_partida] = []
    return diccionario_partida


def almacenar_datos_partida(diccionario_partida, diccionario_jugadores):
    # Autor: Mauro Cuquejo. Espera una lista con los datos de cada jugador, al finalizar el turno y los almacena en la partida
    # Se modifica para que perita almacenar las palabras utilizadas. Las mismas serán utilizadas para generar el archivo
    # partida.csv.
    diccionario_jugadores_auxiliar = diccionario_jugadores.copy()
    #datos_partida = ["", "", "", "", []]
    for posicion, jugador in enumerate(diccionario_jugadores_auxiliar):
        jugador_actual = jugador
        puntaje_jugador_actual = diccionario_jugadores[jugador][puntaje_jugador]
        cant_aciertos_jugador_actual = len(diccionario_jugadores[jugador][letras_acertadas])
        cant_errores_jugador_actual = len(diccionario_jugadores[jugador][letras_erradas])
        datos_partida = [jugador_actual,puntaje_jugador_actual,cant_aciertos_jugador_actual,cant_errores_jugador_actual,[]]
        diccionario_partida.append(datos_partida)
        diccionario_partida[posicion][4].append("".join(diccionario_jugadores[jugador][palabra_actual]))


def elegir_palabra_aleatoria(lista_palabras):
    #Autor: Luan Corrionero.
    palabra_adivinar = lista_palabras.pop(random.randint(0, len(lista_palabras)-1))
    return palabra_adivinar


def otorgar_palabras_jugadores(diccionario_jugadores, lista_palabras):
    #Autor: Luan.Corrionero. Otorga a los jugadores una palabra y genera la palabra oculta
    lista_palabras_utilizadas = []
    for jugador in diccionario_jugadores:
        palabra_aleatoria = elegir_palabra_aleatoria(lista_palabras)
        lista_palabras_utilizadas.append(palabra_aleatoria)
        diccionario_jugadores[jugador][palabra_actual].extend(list(palabra_aleatoria))
        diccionario_jugadores[jugador][palabra_a_adivinar].extend(list(palabra_aleatoria))
        diccionario_jugadores[jugador][palabra_oculta].extend("_" * len(palabra_aleatoria))
    return lista_palabras_utilizadas


def actualizar_diccionario_palabras(diccionario_palabras, lista_palabras_utilizadas):
    #Autor: Luan Corrionero. Elimina las palabras usadas
    for palabra in lista_palabras_utilizadas:
        diccionario_palabras[palabra][palabra_usada] = True


def transformar_guiones_bajos(letraIngresada, jugador, diccionario_jugadores):
    #Autor: Agustin Ramirez. Segun la posicion en la que se encuentra la letra, la reemplaza donde estaba el "_"
    pos = diccionario_jugadores[jugador][palabra_a_adivinar].index(letraIngresada)
    diccionario_jugadores[jugador][palabra_a_adivinar][pos] = "_"
    diccionario_jugadores[jugador][palabra_oculta][pos] = diccionario_jugadores[jugador][palabra_actual][pos]


def ingresar_letra():
    #Autor: Agustin Ramirez. Verifica que la letra ingresada sea correcta para el juego
    while True:
        letra_ingresada = input("Ingresa una letra: ")
        print("\n")
        letra_ingresada = letra_ingresada.upper()
        if len(letra_ingresada) != 1 or not letra_ingresada.isalpha():
            print("Ingresaste un caracter invalido")
        else:
            return letra_ingresada


def generar_lista_palabras_por_cantidad_letras(dic_palabras, cant_jugadores, long_palabra_min):
    #Autor: Mauro Cuquejo. Genera una lista de palabras segun la cantidad de letras que decida el usuario
    lista_palabras = []
    while lista_palabras == [] or len(lista_palabras) < cant_jugadores:
        cant_letras = input("Ingresa la cantidad de letras de la palabra a adivinar, la palabra debe tener al menos {} letras: ".format(long_palabra_min))
        while not cant_letras.isdigit():
            cant_letras = input("Valor incorrecto. Tenes que ingresar un número. Ingresa la cantidad de letras de la palabra a adivinar: ")
        while cant_letras.isdigit() and int(cant_letras) < long_palabra_min:
            cant_letras = input("Recorda que tenes que elegir palabras de al menos {} letras. Intenta nuevamente: ".format(long_palabra_min))
            while not cant_letras.isdigit():
                cant_letras = input(
                    "Valor incorrecto. Tenes que ingresar un número. Ingresa la cantidad de letras de la palabra a adivinar: ")
        for clave in dic_palabras:
            if dic_palabras[clave][1] == int(cant_letras) and dic_palabras[clave][2] == False:
                lista_palabras.append(clave)
        if lista_palabras == [] or len(lista_palabras) < cant_jugadores:
            print("No se encontraron palabras suficientes con esa cantidad de letras para todos los jugadores.")
    return lista_palabras


def mostrar_datos_turno(diccionario_jugadores, jugador, nro_partida):
    #Autor: Luan Corrionero. Muestra los datos relevantes para el turno.
    jugador_esta_eliminado = diccionario_jugadores[jugador][jugador_eliminado]

    if not jugador_esta_eliminado:
        print("\n"*cant_separacion_entre_palabras)
        print("PARTIDA NRO: {}".format(nro_partida))
        print("-----------------------------------------")
        print("JUGADOR ACTUAL: {}".format(jugador))
        print("PUNTAJE: {} PUNTOS.".format(diccionario_jugadores[jugador][puntaje_jugador]))
    else:
        print("PERDISTE, {}. Tenés que esperar que acabe la partida para volver a jugar.".format(jugador))
        print("La palabra era: {}".format(" ".join(diccionario_jugadores[jugador][palabra_actual])))
    if len(diccionario_jugadores[jugador][letras_acertadas]) >= 0:
        print("CANTIDAD DE ACIERTOS: ", len(diccionario_jugadores[jugador][letras_acertadas]))
        print("INGRESASTE LAS SIGUIENTES LETRAS CORRECTAS: {}".format(", ".join(diccionario_jugadores[jugador][letras_acertadas])))
    if len(diccionario_jugadores[jugador][letras_erradas]) >= 0:
        print("CANTIDAD DE ERRORES: ", len(diccionario_jugadores[jugador][letras_erradas]))
        print("INGRESASTE LAS SIGUIENTES LETRAS INCORRECTAS: {}\n".format(", ".join(diccionario_jugadores[jugador][letras_erradas])))
    print(" ".join(diccionario_jugadores[jugador][palabra_oculta]))
    print("\n-----------------------------------------")
    print(diccionario_jugadores[jugador][hombrecito])
    print("-----------------------------------------\n")


def calcular_datos_partidas(diccionario_partida, jugador, nro_partida):
    diccionario_partida_auxiliar = diccionario_partida.copy()
    jugador_actual = ""
    puntaje_jugador_actual = 0
    cant_aciertos_jugador_actual = 0
    cant_errores_jugador_actual = 0
    palabras_usadas = ""
    for datos_jugador in diccionario_partida_auxiliar[nro_partida]:
        if datos_jugador[0] == jugador:
            jugador_actual = datos_jugador[0]
            puntaje_jugador_actual = datos_jugador[1]#[puntaje_jugador]
            cant_aciertos_jugador_actual = datos_jugador[2]#[letras_acertadas])
            cant_errores_jugador_actual = datos_jugador[3]#[letras_erradas])
            palabras_usadas += "".join(datos_jugador[4]) #palabras usadas
    return jugador_actual, puntaje_jugador_actual, cant_aciertos_jugador_actual,cant_errores_jugador_actual, palabras_usadas


def mostrar_datos_partida(diccionario_partida, nro_partida):
    # Autor: Darío Giménez. Muestra los datos de la partida en curso.
    diccionario_partida_auxiliar = diccionario_partida.copy()
    for datos_jugador in diccionario_partida_auxiliar[nro_partida]:
        jugador = datos_jugador[0]
        print("\n-----------------------------------------")
        print("DATOS DE LA PARTIDA {}:".format(nro_partida))
        v_nombre_jugador, v_puntaje_jugador, v_cant_aciertos_jugador, v_cant_errores_jugador, v_palabras_usadas = calcular_datos_partidas(diccionario_partida, jugador, nro_partida)
        print("NOMBRE JUGADOR: {}".format(v_nombre_jugador))
        print("INFORMACION PUNTAJE: {}".format(v_puntaje_jugador))
        print("INFORMACION CANTIDAD DE ACIERTOS: {}".format(v_cant_aciertos_jugador))
        print("INFORMACION CANTIDAD DE ERRORES: {}".format(v_cant_errores_jugador))
        print("-----------------------------------------\n")


def mostrar_datos_generales_partidas(diccionario_partida):
    # Autor: Agustin Ramirez. Muestra la estadística de las partidas jugadas.
    mostrar_datos_generales = input("¿Queres visualizar las estadísticas generales de las partidas jugadas? (S/N): ")
    while not mostrar_datos_generales.upper() in ("S", "N"):
        mostrar_datos_generales = input("Opcion incorrecta. ¿Queres visualizar las estadísticas generales de las partidas jugadas? (S/N): ")

    if mostrar_datos_generales.upper() == 'S':
        diccionario_partida_auxiliar = diccionario_partida
        print("\n" * cant_separacion_entre_palabras)
        print("\n-----------------------------------------")
        print("DATOS GENERALES DE LA PARTIDAS JUGADAS:")
        dic_datos_generales = {}
        for nro_partida in diccionario_partida_auxiliar:
            for datos_jugador in diccionario_partida_auxiliar[nro_partida]:
                jugador = datos_jugador[0]
                v_nombre_jugador, v_puntaje_jugador, v_cant_aciertos_jugador, v_cant_errores_jugador, v_palabras_usadas = calcular_datos_partidas(diccionario_partida, jugador, nro_partida)
                if v_nombre_jugador not in dic_datos_generales:
                    dic_datos_generales[v_nombre_jugador] =[v_puntaje_jugador,v_cant_aciertos_jugador, v_cant_errores_jugador]
                else:
                    dic_datos_generales[v_nombre_jugador][0] = v_puntaje_jugador
                    dic_datos_generales[v_nombre_jugador][1] += v_cant_aciertos_jugador
                    dic_datos_generales[v_nombre_jugador][2] += v_cant_errores_jugador
        for jugador in dic_datos_generales:
            print("\n-----------------------------------------")
            print("NOMBRE JUGADOR: {}".format(jugador))
            print("INFORMACION PUNTAJE TOTAL: {}".format(dic_datos_generales[jugador][0]))
            print("INFORMACION CANTIDAD DE ACIERTOS TOTALES: {}".format(dic_datos_generales[jugador][1]))
            print("INFORMACION CANTIDAD DE ERRORES TOTALES: {}".format(dic_datos_generales[jugador][2]))
        print("-----------------------------------------\n")

def generar_archivo_partida(diccionario_partida):
    #Autor: Mauro Cuquejo: recibe datos del diccionario de partidas y los agrupa de forma totalizada por jugador,
    # para generar el archivo partida.csv.
    diccionario_partida_auxiliar = diccionario_partida
    dic_datos_generales = {}
    for nro_partida in diccionario_partida_auxiliar:
        for datos_jugador in diccionario_partida_auxiliar[nro_partida]:
            jugador = datos_jugador[0]
            v_nombre_jugador, v_puntaje_jugador, v_cant_aciertos_jugador, v_cant_errores_jugador, v_palabras_usadas = calcular_datos_partidas(diccionario_partida, jugador, nro_partida)
            if v_nombre_jugador not in dic_datos_generales:
                dic_datos_generales[v_nombre_jugador] =[v_puntaje_jugador,v_cant_aciertos_jugador, v_cant_errores_jugador,v_palabras_usadas.split(" ")]
            else:
                dic_datos_generales[v_nombre_jugador][0] = v_puntaje_jugador
                dic_datos_generales[v_nombre_jugador][1] += v_cant_aciertos_jugador
                dic_datos_generales[v_nombre_jugador][2] += v_cant_errores_jugador
                dic_datos_generales[v_nombre_jugador][3].append(v_palabras_usadas)
    archivo_partida_csv = open(".\\partida.csv", "w")
    for jugador in dic_datos_generales:
        linea = "{},{},{},{},{}".format(jugador, dic_datos_generales[jugador][1], dic_datos_generales[jugador][2], dic_datos_generales[jugador][0]," ".join(dic_datos_generales[jugador][3]))
        salvar_datos(archivo_partida_csv, linea)
    archivo_partida_csv.close()


def limpiar_datos_jugadores_partida_anterior(diccionario_jugadores):
    # Autor: Luan Corrionero. Restaura los datos de los jugadores.
    for jugador in diccionario_jugadores:
        diccionario_jugadores[jugador][palabra_a_adivinar] = []
        diccionario_jugadores[jugador][palabra_actual] = []
        diccionario_jugadores[jugador][palabra_oculta] = []
        diccionario_jugadores[jugador][letras_acertadas] = []
        diccionario_jugadores[jugador][letras_erradas] = []
        diccionario_jugadores[jugador][jugador_eliminado] = False
        diccionario_jugadores[jugador][ganador_ultima_partida] = False
        diccionario_jugadores[jugador][hombrecito] = ""


def preguntar_continuar_juego():
    # Autor: Agustin Ramirez. Establece la continuación o finalización del juego.
    seguir_partida = True

    continuar = input("¿queres continuar jugando? (S/N): ")
    while not continuar.upper() in ("S", "N"):
        continuar = input("Opcion incorrecta. ¿queres continuar jugando? (S/N): ")

    if continuar.upper() == 'N':
        seguir_partida = False
    return seguir_partida


def procesar_letra_ingresada(diccionario_jugadores, jugador, letra_ingresada, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina):
    cont_aciertos = 0

    while letra_ingresada in diccionario_jugadores[jugador][palabra_a_adivinar]:
        diccionario_jugadores[jugador][letras_acertadas].append(letra_ingresada)
        transformar_guiones_bajos(letra_ingresada, jugador, diccionario_jugadores)
        diccionario_jugadores[jugador][puntaje_jugador] += puntos_aciertos
        cont_aciertos += 1

    if cont_aciertos == 0:
        diccionario_jugadores[jugador][puntaje_jugador] -= puntos_desaciertos
        diccionario_jugadores[jugador][letras_erradas].append(letra_ingresada)
        cantidad_de_errores = len(diccionario_jugadores[jugador][letras_erradas])
        lista_valores_cuerpo = diccionario_jugadores[jugador][valor_partes_cuerpo]
        diccionario_jugadores[jugador][hombrecito] = dibujar_hombrecito(cantidad_de_errores, lista_valores_cuerpo)

        if cantidad_de_errores == max_desaciertos:
            diccionario_jugadores[jugador][jugador_eliminado] = True
            resultado_turno = 'perder'
        else:
            resultado_turno = 'fallar'

    else:
        if diccionario_jugadores[jugador][palabra_oculta] == diccionario_jugadores[jugador][palabra_actual]:
            diccionario_jugadores[jugador][puntaje_jugador] += puntos_adivina
            diccionario_jugadores[jugador][ganador_ultima_partida] = True
            resultado_turno = 'ganar'
        else:
            resultado_turno = 'acertar'
    return resultado_turno


def mostrar_resultados_turno(resultado_turno, cant_jugadores, jugador, diccionario_jugadores,nro_partida):
    mostrar_datos_turno(diccionario_jugadores, jugador,nro_partida)
    if (resultado_turno == 'fallar'):
        if cant_jugadores > 1:
            print("FALLASTE, {}. LE TOCA AL SIGUIENTE JUGADOR.".format(jugador))
        else:
            print("FALLASTE, {}. OTRA VEZ SERÁ.".format(jugador))
    elif resultado_turno == 'perder':
        print("PERDISTE, {}. SE ACABÓ LA PARTIDA PARA VOS.".format(jugador))
    elif resultado_turno == 'ganar':
        print("GANASTE, {}. ESTA PARTIDA SE ACABA ACÁ.".format(jugador))
    else:
        if cant_jugadores > 1:
            print("ACERTASTE, {}. LE TOCA AL SIGUIENTE JUGADOR.".format(jugador))
        else:
            print("ACERTASTE, {}. PODÉS SEGUIR INGRESANDO LETRAS.".format(jugador))
    pausa_para_continuar()


def bienvenida():
    print("----------------------------------------------------------------------------------------------------")
    print("@@@@@@@@@@@.")
    print("@         #.")
    print("@         #.")
    print("@      `@@@@@:")
    print("@    `@       @                                  `@@@@+  @")
    print("@    ,'       @                                  @@      @")
    print("@     @+     @`                                   @@@@   @")
    print("@      +@++@@`                                   @@      @")
    print("@    +@.  #  @@                                  `@@@@+   @@@@#")
    print("@      #@;':@`")
    print("@        #@'")
    print("@         `#              :@@@@: @   @.  @@@#  ,@@@;   `@@@@@  .@@@+,  ,@@@,     @@@#'")
    print("@          @              @    @ @   @. @   @: @   @`  @@      @    @. @    ,@  @    @.")
    print("@          @              @@@@@@ @@@@@. @   @: +@@@@`  @@      @@@@@@. @    ,@  @    @`")
    print("@        `@ ::            @   `@ @   @. @   @: @   @   @@      @    @. @    @   @    @.")
    print("@        @   .@           @    @ +   @. `###'  @    @  ,@@@@@  @    @, `###,    `###@ ")
    print("@       @      @+")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("---------------------------------------------------------------------------------------------------")


def despedida():
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(":::::::::::::::::::::::::::::::::::::clc:::::::c::::::::::::::::::::::::::::::::")
    print("lddddcldl:::::::::::::::::ldl::odc:::lko;:::::dxc::odc:::::::::::::::::oocldddoc")
    print("cooooccxxc:::::::::::::::lkd:::ckx:::cxx:::::oko:::lkxc:::::::::::::::oko:looolc")
    print(":::::::lkx::::::::::::::cxx:::::odc:::cc::::oko:::::oko::::::::::::::lkd::::::::")
    print("::::::::lkd:::::::::::::lkd:::::::::::::::cxkl::::::ckd:::::::::::::ckxc::::::::")
    print(":::::::::oko::::::::::::lkd::::::::::::cldkdc:::::::ckd::::::::::::cxxc:::::::::")
    print("::::::::::dkl::::::::::::xxc::::::::codxxdc:::::::::oko::::::::::::dkl::::::::::")
    print(":::::::::::dd::::::::::::lkd::::::odddlc:::::::::::lkd::::::::::::lxo:::::::::::")
    print("::::::::::::cldddddddddc::lxl:::::cc:::::::::::::::odc::lddddddddolc::::::::::::")
    print("::::::::::::::ccccccccc:::::::::::::::::::::::::::::::::cccccccccc::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n")
    print("GANÓ COM.")
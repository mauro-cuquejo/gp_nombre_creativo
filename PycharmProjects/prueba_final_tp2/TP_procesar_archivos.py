from TP_modulos import *


def configuracion():
    LONG_PALABRA_MIN = 5
    MAX_USUARIOS = 10
    MAX_DESACIERTOS = 7
    PUNTOS_ACIERTOS = 2
    PUNTOS_DESACIERTOS = 1
    PUNTOS_ADIVINA = 30

    with open(".\\configuracion.txt", "r") as archivo_config: #EN RUTA HAY QUE PONER EL DIRECTORIO DEL ARCHIVO
        linea = leer_archivo(archivo_config)
        while linea != "ZZZ":
            tupla_config = tuple(obtener_texto(linea))
            if len(tupla_config) > 1:
                if tupla_config[0] == "LONG_PALABRA_MIN" and tupla_config[1] != "" and tupla_config[1].isdigit() and int(tupla_config[1]) > 0:
                    LONG_PALABRA_MIN = int(tupla_config[1])
                elif tupla_config[0] == "MAX_USUARIOS" and tupla_config[1] != "" and tupla_config[1].isdigit() and int(tupla_config[1]) > 0:
                    MAX_USUARIOS = int(tupla_config[1])
                elif tupla_config[0] == "MAX_DESACIERTOS" and tupla_config[1] != "" and tupla_config[1].isdigit() and int(tupla_config[1]) > 0:
                    MAX_DESACIERTOS = int(tupla_config[1])
                elif tupla_config[0] == "PUNTOS_ACIERTOS" and tupla_config[1] != "" and tupla_config[1].isdigit() and int(tupla_config[1]) > 0:
                    PUNTOS_ACIERTOS = int(tupla_config[1])
                elif tupla_config[0] == "PUNTOS_DESACIERTOS" and tupla_config[1] != "" and tupla_config[1].isdigit() and int(tupla_config[1]) > 0:
                    PUNTOS_DESACIERTOS = int(tupla_config[1])
                elif tupla_config[0] == "PUNTOS_ADIVINA" and tupla_config[1] != "" and tupla_config[1].isdigit() and int(tupla_config[1]) > 0:
                    PUNTOS_ADIVINA = int(tupla_config[1])

            linea = leer_archivo(archivo_config)
            tupla_variables = (LONG_PALABRA_MIN, MAX_USUARIOS, MAX_DESACIERTOS, PUNTOS_ACIERTOS, PUNTOS_DESACIERTOS, PUNTOS_ADIVINA)
    return tupla_variables


def parametros_mostrar(tupla_variables):
    LONG_PALABRA_MIN = tupla_variables[0]
    MAX_USUARIOS = tupla_variables[1]
    MAX_DESACIERTOS = tupla_variables[2]
    PUNTOS_ACIERTOS = tupla_variables[3]
    PUNTOS_DESACIERTOS = tupla_variables[4]
    PUNTOS_ADIVINA = tupla_variables[5]
    print("Bienvenido al juego del ahorcado! \nPara iniciar, tenes que elegir la cantidad de jugadores "
          "(como máximo, pueden jugar {} participantes).".format(MAX_USUARIOS))
    print("Luego, tenes que elegir la cantidad de letras de la palabra a adivinar, que no puede ser inferior a {} letras.".format(LONG_PALABRA_MIN))
    print("Cada jugador tiene un total de {} desaciertos máximos antes de perder.".format(MAX_DESACIERTOS))
    print("IMPORTANTE!!! El hombrecito ahorcado se va a dibujar segun cómo configures el maximo de desaciertos posibles. Si pones un desacierto, apenas te equivoques, se va a dibujar el hombrecito entero.")
    print("Por cada letra acertada, ganas {} punto/s y por cada letra desacertada, perdes {} punto/s.".format(PUNTOS_ACIERTOS, PUNTOS_DESACIERTOS))
    print("El jugador que logré adivinar la palabra, gana la partida y se lleva {} punto/s.".format(PUNTOS_ADIVINA))

def obtener_texto(texto):
    return texto.split(" ")


def leer_archivo(archivo):
    linea = archivo.readline()
    if linea:
        linea = linea.strip("\n")
    else:
        linea = "ZZZ"
    return linea


def salvar_datos(archivo, palabra):
    linea = "{}\n".format(palabra)
    archivo.write(linea)


def procesar_linea(linea_a_reemplazar):
    linea_reemplazada = linea_a_reemplazar

    with open(".\\reemplazar.csv", 'r') as archivo_reemplazar:
        linea = leer_archivo(archivo_reemplazar)
        while linea != "ZZZ":
            lista_reemplazo = linea.split(',')
            while (not lista_reemplazo[0].isdigit() and lista_reemplazo[0] in linea_reemplazada) or (lista_reemplazo[0].isdigit() and chr(int(lista_reemplazo[0])) in linea_reemplazada):
                if lista_reemplazo[0].isdigit():
                    linea_reemplazada = linea_reemplazada.replace(chr(int(lista_reemplazo[0])), lista_reemplazo[1])
                else:
                    linea_reemplazada = linea_reemplazada.replace(lista_reemplazo[0], lista_reemplazo[1])
            linea = leer_archivo(archivo_reemplazar)
        return linea_reemplazada.upper().strip(" ")


def procesar_archivo(ruta, configuracion):
    print("Procesando lista de palabras. Por favor espere un momento...")
    LONG_PALABRA_MIN = configuracion[0]
    with open(ruta, 'r+') as archivo:
        linea = leer_archivo(archivo)
        diccionario_palabras = {}
        while linea != "ZZZ":
            lista_palabras_auxiliar = obtener_texto(procesar_linea(linea))
            for palabra in lista_palabras_auxiliar:
                if len(palabra) >= int(LONG_PALABRA_MIN) and palabra not in diccionario_palabras:
                    diccionario_palabras[palabra] = [len(palabra)]
            linea = leer_archivo(archivo)
        return diccionario_palabras


def lista_palabras_ordenadas(diccionario_palabras):
    return sorted(diccionario_palabras.keys())


def generar_archivo_palabras(lista_archivos):
    tupla_variables = configuracion()
    for nro_archivo, archivo in enumerate(lista_archivos):
        lista_palabras = lista_palabras_ordenadas(procesar_archivo(archivo, tupla_variables))
        nombre_archivo_nuevo = ".\\palabras_texto_{}.txt".format(nro_archivo+1)
        archivo_nuevo =  open(nombre_archivo_nuevo,"w")
        for palabra in lista_palabras:
            salvar_datos(archivo_nuevo, palabra)
        archivo_nuevo.close()
        print("fin procesamiento archivo {}.".format(nro_archivo + 1))


def mezclar_palabras():
    print("Procesando archivo final. Por favor espere un momento...")
    archivo_1 = open(".\\palabras_texto_1.txt","r")
    archivo_2 = open(".\\palabras_texto_2.txt", "r")
    archivo_3 = open(".\\palabras_texto_3.txt", "r")
    archivo_final = open(".\\palabras.txt", "w")

    palabra_1 = leer_archivo(archivo_1)
    palabra_2 = leer_archivo(archivo_2)
    palabra_3 = leer_archivo(archivo_3)
    dic_palabras = {}
    dic_cant_letras_palabras = {}
    while palabra_1 != "ZZZ" or palabra_2 != "ZZZ" or palabra_3 != "ZZZ":
        menor = min(palabra_1, palabra_2, palabra_3)

        while palabra_1 == menor and palabra_1 != "ZZZ":
            if palabra_1 not in dic_palabras:
                dic_palabras[palabra_1] = 1
                salvar_datos(archivo_final, palabra_1)
                if len(palabra_1) not in dic_cant_letras_palabras:
                    dic_cant_letras_palabras[len(palabra_1)] = 1
                else:
                    dic_cant_letras_palabras[len(palabra_1)] += 1
            palabra_1 = leer_archivo(archivo_1)

        while palabra_2 == menor and palabra_2 != "ZZZ":
            if palabra_2 not in dic_palabras:
                dic_palabras[palabra_2] = 1
                salvar_datos(archivo_final, palabra_2)
                if len(palabra_2) not in dic_cant_letras_palabras:
                    dic_cant_letras_palabras[len(palabra_2)] = 1
                else:
                    dic_cant_letras_palabras[len(palabra_2)] += 1
            palabra_2 = leer_archivo(archivo_2)

        while palabra_3 == menor and palabra_3 != "ZZZ":
            if palabra_3 not in dic_palabras:
                dic_palabras[palabra_3] = 1
                salvar_datos(archivo_final, palabra_3)
                if len(palabra_3) not in dic_cant_letras_palabras:
                    dic_cant_letras_palabras[len(palabra_3)] = 1
                else:
                    dic_cant_letras_palabras[len(palabra_3)] += 1
            palabra_3 = leer_archivo(archivo_3)
    archivo_1.close()
    archivo_2.close()
    archivo_3.close()
    archivo_final.close()
    print("fin procesamiento archivo final.\n")
    print("RESULTADO PROCESAMIENTO ARCHIVO______________________________________________________________")
    for cant_letras in dic_cant_letras_palabras:
        print("Hay {} palabras de {} letras.".format(dic_cant_letras_palabras[cant_letras], cant_letras))
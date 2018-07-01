from TP_modulos import *

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

#PARAMETROS_GENERALES
cant_separacion_entre_palabras = 100

def iniciar_juego(long_palabra_min, max_usuarios, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina):
    seguir_juego = True
    nro_partida = 1

    while seguir_juego:
        diccionario_palabras = generar_diccionario_palabras(long_palabra_min)
        cant_jugadores = solicitar_cantidad_jugadores(max_usuarios)
        diccionario_jugadores = generar_diccionario_jugadores(cant_jugadores, max_desaciertos)
        diccionario_partida = {}
        seguir_juego = iniciar_partida(nro_partida, diccionario_partida, diccionario_jugadores, cant_jugadores, diccionario_palabras,long_palabra_min, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina)


def iniciar_partida(nro_partida, diccionario_partida, diccionario_jugadores, cant_jugadores, diccionario_palabras, long_palabra_min, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina):
    seguir_juego = True
    seguir_partida = True

    while seguir_partida:

        if nro_partida not in diccionario_partida:
            diccionario_partida = generar_diccionario_partida(diccionario_partida, nro_partida)

        otorgar_orden_jugadores(nro_partida, diccionario_jugadores)
        limpiar_datos_jugadores_partida_anterior(diccionario_jugadores)
        lista_palabras = generar_lista_palabras_por_cantidad_letras(diccionario_palabras, cant_jugadores, long_palabra_min)
        lista_palabras_usadas = otorgar_palabras_jugadores(diccionario_jugadores, lista_palabras)
        actualizar_diccionario_palabras(diccionario_palabras, lista_palabras_usadas)
        print("\n"*cant_separacion_entre_palabras)
        iniciar_ronda(nro_partida, diccionario_jugadores, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina)

        almacenar_datos_partida(diccionario_partida[nro_partida], diccionario_jugadores)
        mostrar_datos_partida(diccionario_partida, nro_partida)
        seguir_partida = preguntar_continuar_juego()
        if seguir_partida:
            nro_partida += 1
        else:
            seguir_juego = False
            mostrar_datos_generales_partidas(diccionario_partida)
            generar_archivo_partida(diccionario_partida)
    return seguir_juego

def iniciar_ronda(nro_partida, diccionario_jugadores, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina):
    seguir_ronda = True
    while seguir_ronda:
        seguir_ronda = iniciar_turno(nro_partida,diccionario_jugadores, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina)


def iniciar_turno(nro_partida, diccionario_jugadores, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina):
    seguir_turno = True
    seguir_ronda = True
    lista_jugadores_ordenada = [item[0] for item in
                                sorted(diccionario_jugadores.items(), key=lambda x: x[1][orden_jugador])]
    cant_jugadores = len(lista_jugadores_ordenada)
    cont_jugadores_eliminados = 0
    for jugador in diccionario_jugadores:
        if diccionario_jugadores[jugador][jugador_eliminado]:
            cont_jugadores_eliminados += 1

    if cont_jugadores_eliminados == cant_jugadores:
        despedida()
        pausa_para_continuar()
        seguir_turno = False
        seguir_ronda = False

    posicion = 0

    while seguir_turno:
        jugador = lista_jugadores_ordenada[posicion]
        continuar_buscando_letra = True

        if not diccionario_jugadores[jugador][jugador_eliminado]:
            while continuar_buscando_letra:
                mostrar_datos_turno(diccionario_jugadores, jugador, nro_partida)
                letra_ingresada = ingresar_letra()
                resultado_turno = procesar_letra_ingresada(diccionario_jugadores, jugador, letra_ingresada, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina)
                mostrar_resultados_turno(resultado_turno, cant_jugadores, jugador, diccionario_jugadores,nro_partida)
                if resultado_turno == 'perder':
                    continuar_buscando_letra = False
                    cont_jugadores_eliminados += 1
                elif resultado_turno == 'ganar':
                    continuar_buscando_letra = False
                    seguir_turno = False
                    seguir_ronda = False
                else:
                    continuar_buscando_letra = False
        posicion += 1
        if posicion > len(lista_jugadores_ordenada) - 1:
            seguir_turno = False
    return seguir_ronda
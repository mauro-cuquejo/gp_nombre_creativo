from TP_juego import iniciar_juego
from TP_modulos import *

tupla_variables = configuracion()

long_palabra_min = tupla_variables[0]
max_usuarios = tupla_variables[1]
max_desaciertos = tupla_variables[2]
puntos_aciertos = tupla_variables[3]
puntos_desaciertos = tupla_variables[4]
puntos_adivina = tupla_variables[5]

bienvenida()
parametros_mostrar(tupla_variables)
pausa_para_continuar()

lista_archivos = [".\\Cuentos.txt", ".\\La araña negra - tomo 1.txt", ".\\Las 1000 Noches y 1 Noche.txt"]

generar_archivo_palabras(lista_archivos)
mezclar_palabras()

iniciar_juego(long_palabra_min, max_usuarios, max_desaciertos, puntos_aciertos, puntos_desaciertos, puntos_adivina)

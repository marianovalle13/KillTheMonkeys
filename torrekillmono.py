#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random

TIEMPO = 6
fin_de_juego = False

pilas = pilasengine.iniciar()
pilas.fondos.Espacio()
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.rojo)
puntos.magnitud = 30
mono=pilas.actores.Mono()
pilas.actores.Sonido()

balas_simples = pilas.actores.Bala
monos =[]

def mono_destruido(disparo,enemigo):
    enemigo.eliminar()
    puntos.aumentar()
    disparo.eliminar()
    
def game_over(torreta, enemigo):
    global fin_de_juego
    torreta.eliminar()
    texto1=pilas.actores.Texto("Haz logrado %d puntos"% (puntos.obtener()))
    texto1.y=-150
    texto1.definir_color(pilas.colores.amarillo)
    texto2=pilas.actores.Texto("JUEGO TERMINADO")
    texto2.definir_color(pilas.colores.amarillo)
    texto2.y=150
    fin_de_juego=True
    
def crear_mono():
    enemigo = pilas.actores.Mono()
    tata=random.uniform(0.25,0.75) 
    enemigo.escala = (1,tata),.25
    enemigo.radio_de_colision = tata*50
    enemigo.aprender(pilas.habilidades.PuedeExplotar)

    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)
    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180
    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180
    enemigo.x = x
    enemigo.y = y

    tipo_interpolacion = ['lineal',
                            'aceleracion_gradual',
                            'desaceleracion_gradual',
                            'rebote_inicial',
                            'rebote_final']
    
    duracion = 1 +random.random()*4
    
    pilas.utils.interpolar(enemigo, 'x', 0, duracion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion)

    monos.append(enemigo)
    if fin_de_juego:
        return False
    else:
        return True


torreta = pilas.actores.Torreta(enemigos=monos, cuando_elimina_enemigo=mono_destruido)

pilas.colisiones.agregar(torreta, monos,game_over)
pilas.tareas.agregar(1, crear_mono)

pilas.ejecutar()

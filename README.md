Snake Pro - Desafío de Nivel Infinito
======================================

Este proyecto es un videojuego de Snake (culebrita) moderno y profesional 
desarrollado en Python con Pygame. Incluye un sistema de niveles 
procedurales, dificultad progresiva y guardado automático de progreso.

DESCRIPCIÓN
-----------

El jugador controla una serpiente que debe comer comida para crecer y 
acumular puntos. Cada 5 puntos, el juego sube de nivel, lo que aumenta 
la velocidad y genera nuevos obstáculos aleatorios en el mapa. El 
objetivo es alcanzar el nivel más alto posible y superar el récord 
mundial (High Score) guardado localmente.

FUNCIONALIDADES
---------------

- **Movimiento Fluido**: Control preciso con las flechas del teclado.
- **Niveles Infinitos**: Dificultad que escala sin límites.
- **Generación Procedural**: Cada nivel tiene una configuración de obstáculos única.
- **Guardado Automático**: Persistencia de récord y nivel mediante JSON.
- **Interfaz Moderna**: HUD limpio, menú principal y pantalla de Game Over.
- **Sistema de Pausa**: Tecla 'P' para detener la acción en cualquier momento.

REQUISITOS
----------

- Python 3.10 o superior
- Pygame 2.5.2 o superior

ESTRUCTURA DEL PROYECTO
-----------------------

snake_game/
  main.py              Punto de entrada, coordina el bucle principal.
  settings.py          Configuración global, colores y constantes.
  snake.py             Lógica de movimiento y colisiones de la serpiente.
  food.py              Gestión de generación de comida.
  obstacle.py          Clase para los bloques de obstáculos.
  level_manager.py     Generación procedural y escala de dificultad.
  save_system.py       Lógica de lectura/escritura de archivos JSON.
  ui.py                Interfaz de usuario durante el juego (HUD).
  menu.py              Menú principal y pantallas de Game Over.
  assets/              Carpeta para imágenes y sonidos (opcional). Por el momento no se utiliza.
  data/                Directorio de persistencia (save.json). Crea una carpeta para guardar el progreso del juego.
  requirements.txt     Dependencias del proyecto.
  README.md            Este archivo.

INSTALACIÓN Y EJECUCIÓN
-----------------------

### Windows
Abrir una terminal (cmd o PowerShell) en la carpeta del proyecto:

  python -m venv venv
  .\venv\Scripts\activate
  pip install -r requirements.txt
  python main.py

### Linux / macOS
Abrir una terminal en la carpeta del proyecto:

  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python main.py

NOTA SOBRE LOS ASSETS
---------------------

El juego incluye un sistema de renderizado de respaldo. Si no se encuentran
imágenes o sonidos en la carpeta `assets`, el juego utilizará gráficos
vectoriales de Pygame para garantizar que sea jugable de inmediato.

CRÉDITOS
--------

Desarrollado como proyecto de práctica y recordando conceptos avanzados en Python utilizando 
programación orientada a objetos y algoritmos de generación procedural. 

Layered range tree (box query)
El presente es un demo que permite comprender lo que es una consulta ortogonal sobre un Layered Range Tree

Comenzando
Estas instrucciones le permitirán obtener una copia del proyecto en funcionamiento en su máquina local para fines de desarrollo y prueba. Consulte la implementación para obtener ideas sobre cómo implementar el proyecto en un sistema en vivo.

Prerequisitos
- Python 3.6, Ir a la página oficial de Python: https://www.python.org/downloads/ y descargar la versión 3.6.x disponible, hacer una instalación convencional del producto.
- Kivy ultima versión, ir a la página de Kivy https://kivy.org/#download y descargar la última versión disponible, (El presente proyecto solo se ha probado en Windows), la siguiente página indica como hacer una instalación de Kivy en este sistema operativo: https://kivy.org/docs/installation/installation-windows.html

Corriendo el demo
Descargar los archivos LayeredRangeTree.py y main.py en un directorio local de tu máquina, ejecutar el archivo main.py y se abrirá la ventana principal del demo.

- Para llenar de puntos aleatorios ingresar un valor en el primer TextBox de la ventana (a la derecha del botón Graficar Aleatorio), y presionar el botón Graficar Aleatorio, por temas de performance, Kivy no soporta la generación de muchos puntos, es por eso que como máximo se soportan 275000, esperar a que se grafiquen los puntos ( En este paso se está construyendo el Layered Range Tree con los puntos generados).
- Para realizar consultas de click sobre 2 puntos aleatorios de la pantalla, recuerde que el origen de coordenadas es la esquina inferior izquierda, para que sus puntos sean un rango correcto el segundo punto debe ser mayor en ambas coordenadas al primer punto clickeado, luego de click sobre el botón Buscar (En los otros TextBox podemos ver los puntos seleccionados)

Construido con:
- Kivy - Framework de interfaz Gráfica usado
- Python - Lenguaje de programación utilizado

Autores
- Briggi Rivera Guillén
- Juan Marquinho Vilca Castro
- Josué Mateo Vilca Rivera (Jefe de Proyecto)

Licencia: No hay licencia, si les sirve usenlo.

Agradecimientos a Lizeth y Luciano nuestros profesores que nos pondrán 20 por el esfuerzo hecho!!!
 

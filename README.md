# PortScannerPy

Este es un script de Python que realiza un escaneo de puertos de una dirección IP o rango de direcciones IP a través de la libreria nmap. Fue confeccionado para un curso de ciberseguridad.  A continuación se detallan las funcionalidades:

1.  Importa las librerías necesarias para ejecutar el código: `pyfiglet`, `nmap`, `requests`, y `json`.
2.  Utiliza `pyfiglet` para imprimir un título en la consola.
3.  Pide al usuario que ingrese una dirección IP o rango de direcciones IP que se escaneará.
4.  Utiliza la biblioteca `nmap` para realizar el escaneo de puertos. El escaneo se realiza utilizando los siguientes argumentos: `-sS` para TCP SYN scan, `-sV` para la detección de versiones de servicios, `-sU` para la detección de puertos UDP, `-T4` para una intensidad de escaneo rápida, `-F` para un escaneo rápido de puertos, y `--version-intensity 0` para evitar la detección de versiones de servicios.
5.  Filtra y guarda solo las direcciones IP que están 'up' en una lista `listado_up`.
6.  Recorre la lista de direcciones IP y muestra en la consola la dirección IP, el hostname (si está disponible), los puertos y los servicios asociados. También actualiza la variable `resultado` con esta información en un formato JSON.
7.  Intenta enviar la variable `resultado` a una dirección URL utilizando el método HTTP POST.
8.  Guarda la variable `resultado` en un archivo JSON en el equipo del usuario.

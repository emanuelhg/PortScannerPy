#!/user/bin/python3
import pyfiglet
import nmap
import requests
import json

bienvenida = pyfiglet.figlet_format("PortScanner")
print(bienvenida)
print('. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .\n')

#Definimos la IP o rango donde se realizará el escaneo:
rangoIP = input("""\nIngrese la IP o rango a escanear y presione ENTER, formatos soportados:
        - IP única, ejemplo: 192.168.1.1
        - Rango con IP inicial - IP final, ejemplo: 192.168.1.1-254
        - Rango indicando una máscara, ejemplo: 192.168.1.0/24 \n""")

resultado = []
nm = nmap.PortScanner()
print("\n\033[1;33;40mEscaneando la IP o rango",rangoIP,"por favor aguarde el resultado.\033[0m\n")
nm.scan(rangoIP, arguments='-sS -sV -sU -T4 -F --version-intensity 0')

print("\n\033[1;33;40mEquipos detectados | Resultados:\033[0m\n")

#Tomamos la lista de hosts:
listado_host = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
listado_up = []

#Filtramos y guardamos solo los que están 'up':
for host, status in listado_host:
	if status in 'up':
        	listado_up.append(host)

# Recorremos el listado mostrando: IP | Hostname | Puertos - Estado y tipo de Servicio.
# Grabamos en la variable 'resultado' para exportar a JSON.
for h in listado_up:
		parcial = {}
		contador = 0
		print('\033[0;30;47mIP: {}\033[0m'.format(h))
		parcial.update({"IP":(h)})
		if nm[h].hostname() == '':
			print('No se pudo obtener el hostname')
			parcial.update({"hostname":"No se pudo obtener el hostname"})
		else:
			print('Hostname: {}'.format(nm[h].hostname()))
			parcial.update({"hostname":nm[h].hostname()})
		print('-----------------------')
		if nm[h].all_protocols() == []:
			print('\033[1;31;40m\n- no se detectó ningún protocolo -\033[0m')
			parcial.update({'Escaneo':'No se detectó ningún protocolo'})
		for proto in nm[h].all_protocols():
			try:
				print('\033[1;32;40mProtocolo: {proto}\033[0m'.format(proto=proto.upper()))
				lport = nm[h][proto].keys()
				for port in lport:
					contador += 1
					print('Puerto: %s\tEstado: %s\tServicio: %s - %s' % (port, nm[h][proto][port]['state'], nm[h][proto][port]['name'], nm[h][proto][port]['product']))
					parcial.update({'Puerto ' + proto.upper() + ' ' + str(contador):{'Puerto':port, 'Estado':nm[h][proto][port]['state'], 'Servicio': nm[h][proto][port]['product']}})
			except Exception as e:
				print('Ocurrió un error al escanear uno de los host, ver detalle:', e)
		print('\n=======================\n')
		resultado.append(parcial)

print('. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .\n')
print("\n\033[1;36;40mFin del escaneo.\033[0m\n")
#Simulamos el POST de la variable resultado a un servidor:
try:
	requests.post('http://127.0.0.1/example/fake_url.php', json=resultado, timeout=5)
except:
    print("Enviando resultados a la url \033[0;30;47mhttp://127.0.0.1/example/fake_url.php\033[0m. . . . \033[1;31;40m[FAIL]\033[0m")

#Convertimos la variable en un archivo JSON y guardamos en el equipo:
with open("resultado_nmap.json", "w") as f:
    json.dump(resultado, f)
print("Guardando el archivo \033[0;30;47mresultado_nmap.JSON\033[0m. . . . \033[1;32;40m[OK]\033[0m")

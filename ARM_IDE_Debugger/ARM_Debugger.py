import PySimpleGUI as sg
import subprocess
import pexpect

#Abrimos una ventana para seleccionar con interfaz grafica el archivo
#Que se quiere utilizar
ruta = sg.popup_get_file("Selecciona tu archivo ARM")

#Depuramos la cadena de texto con la ruta del archivo para quitar el .s
#Y asi evitar problemas cuando el script en shell quiera utilizar esta ruta
ruta = ruta[:-2]
nombreArchivo = ""

#Obtenemos el nombre del archivo para utilizarlo en el script shell para 
#Ejecutar en automatico el programa ARM del usuario 
for caracter in reversed(ruta):
	if caracter != "/":
		nombreArchivo = caracter + nombreArchivo 
	else:
		break

#Se pasa el comando en shell como una lista, un string y una variable
#Python ejecutara los comandos de esa lista 
Resultado_shell  =  subprocess.run(["./ejecARM.sh", ruta, nombreArchivo], capture_output=True, text=True)

#Imprimiemos lo obtenido en una ventana grafica para visualizar el resultado
#sg.Print(Resultado_shell.stdout, wait=True)

#Necesitamos usar GDB para que el programa pueda dar opciones de debug sencillas
#para esto usamos pexpect que ayuda a interactuar con programa de texto en 
#terminal como GDB, ya que usa bucles y no da respuestas directas como solo
#usar la terminal

#Iniciamos creando creando el proceso hijo, nuestro script(este) es el padre
#el GDB que usaremos desde aqui sera el proceso hijo
#-q es para evitar el mensaje del inicio
child = pexpect.spawn('gdb -q -ex "set style enabled off" factorial')	

child.expect("(gdb)")

#Desactivo displaced stepping que es una herramienta de gdb para manejar
#mejor el debugging, el problema es que en esta version de raspberry 
#genera error porque tiene un bug interno y esto se ve al intenta 
#usar la instruccion stepi. Una vez desactivada utilizar el metodo
#clasico y este funciona y no genera error solo podria generar error
#con codigos multhilo.

child.sendline('set displaced-stepping off')

child.expect('(gdb)')

child.sendline('l')

child.expect('(gdb)')

#Se guarda el programa ARM, el codigo 
codigo = child.before.decode('utf-8')

child.sendline('b 1')

child.expect('(gdb)')

child.sendline('r')

child.expect('(gdb)')

child.sendline('i r')

child.expect('(gdb)')

#Se guardan los registros en el estado inicial del debug
registros = child.before.decode('utf-8')

#sg.Print(resultado, wait=True)

#Prueba ventana persistente.
#Se crea lienzo
layout = [ 
	  [sg.Text('Pruea de ventana persistente c:')],
 	  [sg.Multiline(size=(40,20), key='s1',write_only=True), sg.Multiline(size=(40,20), key='s2'), sg.Button('Siguiente'),sg.Button('Cerrar')]
	 ]

#Se crea la ventana 
window = sg.Window('Debugger ARM v1.0', layout)

#Ciclo principal de ventana
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cerrar':
        break

    #Imprimimos el codigo del programa que seleccionamos y los registros
    #al iniciar el programa
    window['s1'].update("Codigo ARM: \n" + codigo)
    window['s2'].update("Lista de Registros: \n" + registros)

    if event == 'Siguiente':
        child.sendline('stepi')
        child.expect('(gdb)')
        child.sendline('i r')
        child.expect('(gdb)')
        registros = child.before.decode('utf-8')
        window['s1'].update("Codigo ARM: \n" + codigo)
        window['s2'].update("Lista de Registros: \n" + registros)

window.close()

#Cerramos pyexpect
child.sendline('exit')
child.close()

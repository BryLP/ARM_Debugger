#Programa para ensamblado,ligado y ejecucion de un programa en ensambladorARM
import PySimpleGUI as sg
import subprocess
import pexpect

sg.theme('LightBrown13')

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

texto = 'ARM ensamblador Version 1.0 - FI UNAM \n Ensamblando el archivo: ' + nombreArchivo + ".s"
#Se crea lienzo
layout = [ 
	  [sg.Text(texto)],
 	  [sg.Multiline(size=(40,20), key='s1',text_color='red',background_color='black'),
           sg.Button('Cerrar')]
	 ]

#Se crea la ventana 
window = sg.Window('Debugger ARM v1.0', layout)

#Ciclo principal de ventana
while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED or event == 'Cerrar':
        break
    else:
	#Imprimimos informacion al usuario y el resultado de su ejecucion
	window['s1'].update("Ensamblando el Codigo de tu archivo "+nombreArchivo+".s : \n" + Resultado_shell.stdout)

#    if event == 'Siguiente':

window.close()

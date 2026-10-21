#!/bin/bash
#Autor Bryan Mejia Ramos 
#Fecha 25 de marzo 2025
#Descipcion Programa para automatizar el ensamblado, ligado y ejecucion de
#           un progama en ensambador ARM.

#Seccion para recibir el nombre del archivo desde terminal solo ejecutando
#Este script en shell
#echo "Ingresa el nombre del programa que quieres ejecutar"
#read ruta

#Modificacion para recibir la ruta del archivo obtenida con PySimpleGUI 
#Utilizando una interfaz grafica
echo ""
ruta=$1
echo "Ruta de archivo seleccionado: $ruta"
echo ""

#Ensamblado, ligado y ejecucion
echo "Ensamblando ..."
echo ""
as -g -o $ruta.o $ruta.s #Agregue -g para que genere datos para debugger
echo "Ligado ..."
echo""
ld -o $ruta $ruta.o
echo "Ejecutando ..."
echo ""
echo "Resultado de ejecucion...."
$ruta ; echo $?


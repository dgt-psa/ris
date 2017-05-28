#!/bin/bash

###############################################################################

carpeta=$1
if [ -d "$carpeta" ]; then
	ruta_default="$(pwd)"
	echo "----------------------------------------"
	echo "Ingresando a la carpeta: $carpeta"
	echo "----------------------------------------"
	cd "$carpeta"
	for archivo in *.png
	do
		if [ "$archivo" != "*.jpg" ]; then
			echo "Procesando archivo: $archivo"
			convert "$archivo" "${archivo}.jpg"
		else
			echo "No hay archivos en esta carpeta. Saliendo..."
		fi
	done
	cd "$ruta_default"
	echo ""
else
	if [ -z "$carpeta" ]; then
		echo "Úsese: $0 <carpeta>"
	else
		echo "Carpeta inexistente. Saliendo..."
	fi
fi

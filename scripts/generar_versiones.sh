#!/bin/bash

###############################################################################

carpeta=$1
if [ -d "$carpeta" ]; then
	ruta_default="$(pwd)"
	echo "----------------------------------------"
	echo "Ingresando a la carpeta: $carpeta"
	echo "----------------------------------------"
	cd "$carpeta"
	for archivo in *.jpg
	do
		if [ "$archivo" != "*.jpg" ]; then
			echo "Procesando archivo: $archivo"
			#convert "$archivo" -flip "${archivo}_nohash_Flip.jpg"
			#convert "$archivo" -flop "${archivo}_nohash_Flop.jpg"
			convert "$archivo" -rotate 45 "${archivo}_nohash_Rot45.jpg"
			convert "$archivo" -rotate 90 "${archivo}_nohash_Rot90.jpg"
			#convert "$archivo" -rotate 135 "${archivo}_nohash_Rot135.jpg"
			convert "$archivo" -rotate 180 "${archivo}_nohash_Rot180.jpg"
			#convert "$archivo" -rotate 225 "${archivo}_nohash_Rot225.jpg"
			#convert "$archivo" -rotate 270 "${archivo}_nohash_Rot270.jpg"
			#convert "$archivo" -rotate 315 "${archivo}_nohash_Rot315.jpg"
			#convert "$archivo" -resize 25% "${archivo}_nohash_ResizeCuarto.jpg"
			convert "$archivo" -resize 50% "${archivo}_nohash_ResizeMitad.jpg"
			#convert "$archivo" -resize 200% "${archivo}_nohash_ResizeDoble.jpg"
			convert "$archivo" -quality 70 "${archivo}_nohash_Quality70.jpg"
			#convert "$archivo" -quality 85 "${archivo}_nohash_Quality85.pg"
			mv "$archivo" "${archivo}_nohash_Original.jpg"
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

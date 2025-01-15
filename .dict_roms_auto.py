# Solo para analizar directorio con ROMs
import zipfile
import hashlib as hash
import os
import sys

directorio_roms = "/home/imano-oh/Descargas/N64/zip/"

def calcular_md5(archivo_rom):
    if type(archivo_rom) != str:
        hash_md5 = hash.md5()
        for chunk in iter(lambda: archivo_rom.read(4096), b""):
            hash_md5.update(chunk)

    else:
        if not os.path.isfile(archivo_rom):
            return f"El archivo {archivo_rom} no es un archivo valido."

        try:
            hash_md5 = hash.md5()
            with open(archivo_rom, "rb") as a:
                for chunk in iter(lambda: a.read(4096), b""):
                    hash_md5.update(chunk)

        except Exception as e:
            return f"Error al procesar el archivo {a}: {e}"

    return hash_md5.hexdigest().upper()

def nombre_archivo_sin_ext(nombre_archivo):
    corte = False
    nombre = nombre_archivo

    while not corte:
        caracter = nombre[len(nombre) - 1]
        if caracter != ".":
            nombre = nombre[:len(nombre) - 1]
        else:
            nombre = nombre[:len(nombre) - 1]
            corte = True

    return nombre

resultados = []

for root, _, archivos in os.walk(directorio_roms):
    for a in archivos:
        archivo = directorio_roms + a
        print(f"Leyendo {archivo}")
        nombre = nombre_archivo_sin_ext(a)
        md5 = calcular_md5(archivo)

        resultados.append((nombre, md5))

print(" ")
for r in resultados:
    print("id_base = {")
    print(f"    'titulo': '{r[0]}',")
    print(f"    'md5': '{r[1]}',")
    print("    'portada': nombre_portada")
    print("}\n")

directorio_destino = "/home/imano-oh/"

nombre_archivo = "registro.txt"

if directorio_destino:
    ruta_archivo = f"{directorio_destino}/{nombre_archivo}"
    try:
        with open(ruta_archivo, 'w') as archivo:
            for r in resultados:
                linea1 = "id_base = {\n"
                linea2 = f"    'titulo': '{r[0]}',\n"
                linea3 = f"    'md5': '{r[1]}',\n"
                linea4 = "    'portada': 'nombre_portada'\n"
                linea5 = "}\n"
                linea6 = "\n"

                archivo.write(linea1)
                archivo.write(linea2)
                archivo.write(linea3)
                archivo.write(linea4)
                archivo.write(linea5)
                archivo.write(linea6)

            print(f"Texto guardado en '{ruta_archivo}' con éxito.")
    except Exception as e:
            print(f"Error al guardar el texto en '{ruta_archivo}': {str(e)}")
else:
    print("No se ha seleccionado una carpeta de destino.")





import os
import sys
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), 'covers'))

import parser_zip as pzip
import registro_juegos as reg

base_juegos = [
    value for name, value in vars(reg).items()
    if isinstance(value, dict)
][1:]

directorio_roms = "/home/imano-oh/ROMs/N64/"
directorio_covers = "/home/imano-oh/.var/app/com.github.Rosalie241.RMG/data/RMG/Covers/"

def nombre_archivo_con_ext(path_archivo):
    corte = True
    cadena = path_archivo
    nombre = " "
    while corte:
        caracter = cadena[len(cadena) - 1]
        if caracter != "/":
            nombre = caracter + nombre
            cadena = cadena[:len(cadena) - 1]
        else:
            corte = False

    return nombre[:-1]

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

def extension_archivo(path_archivo):
    corte = True
    cadena = path_archivo
    extension = " "
    while corte:
        caracter = cadena[len(cadena) - 1]
        if caracter != ".":
            extension = caracter + extension
            cadena = cadena[:len(cadena) - 1]
        else:
            corte = False

    return "." + extension

def verificar_portadas_en_rmg():
    covers = directorio_covers
    portadas_existentes = []

    for root, _, archivos in os.walk(covers):
        for cover in archivos:
            nombre = nombre_archivo_sin_ext(str(cover))
            portadas_existentes.append(nombre)

    return portadas_existentes

def omitir_juegos_con_portada(lista_juegos_directorio_roms):
    set_juegos_directorio_roms = set(lista_juegos_directorio_roms)
    set_juegos_con_portada = set(verificar_portadas_en_rmg())

    lista_juegos_final = list(set_juegos_directorio_roms - set_juegos_con_portada)

    return lista_juegos_final

def encontrar_juego(md5_rom):
    encontrado = False
    i = 0
    while not encontrado and i < len(base_juegos):
        if base_juegos[i]['md5'] != md5_rom.upper():
            i += 1
        else:
            encontrado = True

    if encontrado:
        return base_juegos[i], i
    else:
        return {}, -1 # Significa que no encontro el juego en la base

def analizar_directorio(dir_rom):
    lista_md5 = []
    for root, _, archivos in os.walk(dir_rom):
        for a in archivos:
            archivo = directorio_roms + a
            print(f"Leyendo {archivo}")
            # Analizar roms validas .z64 .n64 .v64
            if archivo.endswith(('.z64', 'n64', 'v64')):
                a_md5 = pzip.calcular_md5(archivo)
                # lista_md5.append(a_md5)
                lista_md5.append((nombre_archivo_con_ext(archivo), a_md5))
            # Analizar archivos .zip
            if archivo.endswith('.zip'):
                md5_roms = pzip.procesar_archivo_zip(archivo)
                if len(md5_roms) > 0:
                    for x in md5_roms:
                        # lista_md5.append(x[1])
                        lista_md5.append((x[0], x[1]))

    return lista_md5

def listar_portadas(lista_juegos):
    portadas = []
    md5_lista_juegos_roms = [x[1] for x in lista_juegos]

    lista_md5 = omitir_juegos_con_portada(md5_lista_juegos_roms)

    if len(lista_md5) != 0:
        for md5 in lista_md5:
            juego, indice = encontrar_juego(md5)
            if indice != -1:
                print(f"Encontrada portada para {juego['titulo']} {md5}")
                portadas.append((juego['portada'], md5))
            else:
                print(f"No hay juego para {md5} en la base")
    else:
        print("No hay portadas para cargar")

    return portadas

def copiar_portadas_destino(portadas):
    for p in portadas:
        portada = "covers/" + p[0]
        archivo_destino = os.path.join(directorio_covers, p[1] + ".jpg") # Se renombra la portada con el segundo parametro p[1] + ".jpg" cuando se copie a directorio_covers
        try:
            shutil.copy(portada, archivo_destino)
            print(f"Copiado {archivo_destino} en {directorio_covers}")
        except FileNotFoundError:
            print(f"No hay archivo de portada en base para {p[0]}")


# Prueba

resultados = analizar_directorio(directorio_roms)
for r in resultados:
    print(r)
print("\nCantidad de ROMs: ", len(resultados), "\n")

resultados_prueba = [
    ('Star Wars Episode  Racer.z64', '1EE8800A4003E7F9688C5A35F929D01B'),
    ('StarCraft 64.z64', 'B75945407D7DEA00A2A29AD24056A416'),
    ('Starshot - Space Circus Fever.z64', 'A9C393AA232B32798ADF378F4318F99F'),
    ('Super Bowling 64.z64', 'FA3A043997A3ACDF17337385B126BC04'),
    ('Super Mario 64 (USA).z64', '20B854B239203BAF6C961B850A4A51A2'),
    ('Turok 2 Seeds of Evil.z64', 'E5A39521FA954EB97B96AC2154A5FD7A')
]

# print(encontrar_juego("B75945407D7DEA00A2A29AD24056A416"))
cover = listar_portadas(resultados)
print(cover, "\n")

copiar_portadas_destino(cover)


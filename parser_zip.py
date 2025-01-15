import zipfile
import hashlib as hash
import os

def leer_zip(path_rom_zip):
    roms_validas = []
    archivo_sin_roms = False
    try:
        # print(f"Leyendo {path_rom_zip}")
        with zipfile.ZipFile(path_rom_zip, 'r') as rom_zip:
            for rom in rom_zip.namelist():
                if rom.endswith(('.z64', 'n64', 'v64')):
                    print(f"Encontrado {rom}")
                    roms_validas.append(rom)
            # roms_validas = [rom for rom in rom_zip.namelist() if rom.endswith(('.z64', 'n64', 'v64'))]

            if len(roms_validas) == 0:
                archivo_sin_roms = True
                print(f"No se encontraron ROMs validas en el archivo {path_rom_zip}")

        print(" ")
        return roms_validas, archivo_sin_roms

    except zipfile.BadZipFile:
        return "El archivo proporcionado no es un ZIP valido.", True

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

def procesar_archivo_zip(path_rom_zip):
    lista_roms, lista_vacia = leer_zip(path_rom_zip)
    md5_roms = []
    if not lista_vacia:
        with zipfile.ZipFile(path_rom_zip, 'r') as archivo_zip:
            for rom in lista_roms:
                with archivo_zip.open(rom) as archivo_rom:
                    rom_md5 = calcular_md5(archivo_rom)
                    md5_roms.append((rom, rom_md5))

    return md5_roms



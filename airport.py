import matplotlib.pyplot as plt


import matplotlib.pyplot as plt


class Airport:
    """Clase que representa un aeropuerto con su código, coordenadas y si pertenece al espacio Schengen."""

    def __init__(self, code, lat, lon):
        self.code = code  # Código ICAO de 4 caracteres
        self.lat = lat  # Latitud en grados decimales
        self.lon = lon  # Longitud en grados decimales
        self.schengen = False  # Por defecto, se inicializa como False


def IsSchengenAirport(code):
    """Recibe un código ICAO y verifica si pertenece a un país Schengen buscando su prefijo."""
    if code == "":
        return False

    # Lista de prefijos correspondientes a los países del acuerdo Schengen
    prefijos = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
                'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

    i = 0
    encontrado = False
    prefijo = code[:2]  # Extrae los 2 primeros caracteres del código ICAO

    # Recorre la lista de prefijos hasta encontrar una coincidencia o llegar al final
    while i < len(prefijos) and not encontrado:
        if prefijos[i] == prefijo:
            encontrado = True
        else:
            i = i + 1
            encontrado = False

    return encontrado


def SetSchengen(airport):
    """Actualiza el atributo schengen del objeto aeropuerto usando la función IsSchengenAirport."""
    airport.schengen = IsSchengenAirport(airport.code)


def PrintAirport(airport):
    """Imprime por consola los datos formateados de un aeropuerto."""
    print(f"Code: {airport.code}, Lat: {airport.lat:.6f}, Lon: {airport.lon:.6f}, Schengen: {airport.schengen}")


def LoadAirports(Filename):
    """Lee un archivo de texto, extrae los aeropuertos, convierte sus coordenadas y los devuelve en una lista."""
    airports = []
    try:
        # Abre el archivo en modo lectura
        F = open(Filename, "r")

        # Lee y descarta la primera línea (cabecera)
        F.readline()
        line = F.readline()  # Lee la primera línea de datos

        i = 1

        # Bucle que se ejecuta hasta que no queden más líneas por leer
        while line != "":
            # Divide la línea en palabras (separadas por espacios)
            parts = line.split()
            code = parts[0]
            lat = ConvertCoord(parts[1])  # Convierte el string de latitud a decimal
            lon = ConvertCoord(parts[2])  # Convierte el string de longitud a decimal

            # Crea el objeto aeropuerto y lo añade a la lista
            airport = Airport(code, lat, lon)
            SetSchengen(airport)
            airports.append(airport)

            # Lee la siguiente línea para la próxima iteración
            line = F.readline()

        F.close()

    # Si el archivo no existe, devuelve la lista vacía
    except FileNotFoundError:
        airports = []

    return airports


def SaveSchengenAirports(airports, filename):
    """Guarda en un archivo de texto solo los aeropuertos que pertenecen a la zona Schengen."""
    if len(airports) == 0:
        return -1  # Código de error si la lista está vacía

    # Abre el archivo en modo escritura (sobrescribe si ya existe)
    F = open(filename, "w")

    # Escribe la cabecera con el formato requerido
    F.write("CODE LAT LON\n")

    i = 0
    # Recorre toda la lista de aeropuertos
    while i < len(airports):
        # Si el aeropuerto es Schengen, escribe sus datos en el archivo
        if airports[i].schengen == True:
            F.write(f"{airports[i].code} {airports[i].lat} {airports[i].lon}\n")
        i = i + 1

    F.close()


def AddAirport(airports, airport):
    """Añade un aeropuerto a la lista solo si su código no existe ya en ella."""
    if airport.code == "":
        return

    i = 0
    encontrado = False

    # Bucle para comprobar si el código ya existe en la lista
    while i < len(airports) and not encontrado:
        if airports[i].code == airport.code:
            encontrado = True
        else:
            i = i + 1

    # Si terminamos de buscar y no lo encontramos, lo añadimos
    if not encontrado:
        airports.append(airport)


def RemoveAirport(airports, code):
    """Busca un aeropuerto por su código y lo elimina de la lista."""
    i = 0
    encontrado = False

    # Busca el índice del aeropuerto que coincide con el código
    while i < len(airports) and not encontrado:
        if airports[i].code == code:
            # Reconstruye la lista omitiendo el elemento en la posición 'i'
            airports[:] = airports[:i] + airports[i + 1:]
            encontrado = True
        else:
            i = i + 1

    # Devuelve un código de error si el aeropuerto no estaba en la lista
    if not encontrado:
        return -1


def ConvertCoord(coord):
    """Convierte una coordenada en formato string (ej: N412974) a grados decimales (float)."""
    direccion = coord[0]  # Extrae N, S, E o W

    # Lógica para separar grados, minutos y segundos dependiendo de si es Latitud (N/S) o Longitud
    if direccion == "N" or direccion == "S":
        degrees = int(coord[1:3])
        minutes = int(coord[3:5])
        seconds = int(coord[5:])
    else:
        degrees = int(coord[1:4])
        minutes = int(coord[4:6])
        seconds = int(coord[6:8])

    # Fórmula de conversión a decimal
    decimal = degrees + minutes / 60 + seconds / 3600

    # Si la dirección es Sur o Oeste, la coordenada debe ser negativa
    if direccion == 'S' or direccion == 'W':
        decimal = -decimal

    return decimal


def PlotAirports(airports):
    """Genera un gráfico de barras apiladas mostrando la cantidad de aeropuertos Schengen vs No Schengen."""
    i = 0
    schengen = 0

    # Cuenta cuántos aeropuertos son Schengen
    while i < len(airports):
        if airports[i].schengen == True:
            schengen = schengen + 1
        i = i + 1

    # El resto son No Schengen
    noschengen = len(airports) - schengen

    # Crea la figura de matplotlib
    fig, ax = plt.subplots()

    # Dibuja la barra inferior (Schengen) y la superior (No Schengen)
    ax.bar(['Aeropuertos'], [schengen], label='Schengen')
    ax.bar(['Aeropuertos'], [noschengen], bottom=[schengen], label='No Schengen')

    # Añade etiquetas y leyenda
    ax.set_ylabel('Cantidad')
    ax.set_title('Schengen airports')
    ax.legend()

    # Muestra el gráfico en pantalla
    plt.show()


def MapAirports(airports):
    """Genera un archivo KML para visualizar los aeropuertos en Google Earth con distintos colores."""
    try:
        # Abre (o crea) el archivo kml en modo escritura
        F = open("Airports.kml", "w")

        # Escribe las etiquetas iniciales obligatorias de un archivo KML
        F.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        F.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        F.write('<Document>\n')

        # Define el estilo visual (color verde) para aeropuertos Schengen
        F.write('<Style id="schengen">\n')
        F.write('<IconStyle>\n')
        F.write('<color>ff00ff00</color>\n')
        F.write('</IconStyle>\n')
        F.write('</Style>\n')

        # Define el estilo visual (color rojo) para aeropuertos No Schengen
        F.write('<Style id="nonschengen">\n')
        F.write('<IconStyle>\n')
        F.write('<color>ff0000ff</color>\n')
        F.write('</IconStyle>\n')
        F.write('</Style>\n')

        i = 0
        # Recorre la lista de aeropuertos para crear un 'Placemark' por cada uno
        while i < len(airports):
            airport = airports[i]

            # Asigna el estilo dependiendo del atributo schengen
            if airport.schengen:
                style = "#schengen"
            else:
                style = "#nonschengen"

            # Escribe los datos del aeropuerto en formato XML/KML si el código no está vacío
            if airport.code != "":
                F.write("<Placemark>\n")
                F.write(f"<name>{airport.code}</name>\n")
                F.write(f"<styleUrl>{style}</styleUrl>\n")
                F.write("<Point>\n")
                # KML usa el formato longitud,latitud,altitud
                F.write(f"<coordinates>{airport.lon},{airport.lat},0</coordinates>\n")
                F.write("</Point>\n")
                F.write("</Placemark>\n")

            i = i + 1

        # Cierra las etiquetas principales
        F.write('</Document>\n')
        F.write('</kml>\n')

        F.close()

    # Bloque de captura de errores por si hay fallos al escribir o leer datos
    except FileNotFoundError:
        print("No hay ficheros")
    except ValueError:
        print("Datos incorrectos")
    except IndexError:
        print("Datos incorrectos")

    # Ejecuta el archivo generado automáticamente (abre Google Earth si está instalado)
    import os
    os.startfile("Airports.kml")
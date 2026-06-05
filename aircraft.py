import matplotlib.pyplot as plt
from airport import LoadAirports


class Aircraft:
    """Clase que representa un avión/vuelo con su identificación, origen, hora de llegada, aerolínea, destino y salida."""

    def __init__(self, aircraft, origen, time, airline, destination="", departure=""):
        self.aircraft = str(aircraft)       # ID del avión
        self.origen = str(origen)           # Código ICAO origen
        self.time = str(time)               # Hora de llegada (hh:mm)
        self.airline = str(airline)         # Código ICAO aerolínea
        self.destination = str(destination) # Código ICAO destino
        self.departure = str(departure)     # Hora de salida (hh:mm)

def LoadArrivals(Filename):
    """Abre un archivo de llegadas, valida los datos de cada línea y devuelve una lista de objetos Aircraft."""
    aircrafts = []
    try:
        F = open(Filename, "r")
        F.readline()
        line = F.readline()
        i = 1

        # Lee hasta el final del archivo
        while line != "":
            # Elimina espacios en blanco al inicio/final y separa por columnas
            parts = line.strip().split()

            # Se asegura de que la línea tenga exactamente 4 elementos
            if len(parts) == 4:
                aircraft = parts[0]
                origen = parts[1]
                time = parts[2]
                airline = parts[3]

                # Separa la hora y los minutos usando ":" como delimitador
                parts_time = time.split(":")

                # Valida que el formato de tiempo sea correcto (tenga hora y minuto)
                if len(parts_time) == 2:
                    hora = int(parts_time[0])
                    minuto = int(parts_time[1])

                    # Comprueba que la hora (0-23) y minutos (0-59) sean lógicos
                    if 0 <= hora <= 23 and 0 <= minuto <= 59:
                        # Si todo es correcto, crea el objeto y lo añade a la lista
                        aircraft_obj = Aircraft(aircraft, origen, time, airline)
                        aircrafts.append(aircraft_obj)

            line = F.readline()

        F.close()

    except FileNotFoundError:
        aircrafts = []  # Si el archivo no existe, devuelve lista vacía
    except ValueError:
        pass  # Si hay un error de conversión (ej. letras en la hora), lo ignora y sigue

    return aircrafts


def PlotArrivals(aircrafts):
    """Muestra un gráfico de barras con la frecuencia de aterrizajes por cada hora del día."""
    # Crea una lista con 24 ceros, uno para cada hora del día (0 a 23)
    vuelos = [0] * 24

    if len(aircrafts) == 0:
        print("Error: lista vacía")
        return

    i = 0
    # Recorre todos los aviones para extraer su hora de llegada
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        time = aircraft.time
        # Extrae solo la parte de la hora y la convierte a entero
        hora = int(time.split(":")[0])
        # Suma 1 al contador de esa hora específica
        vuelos[hora] = vuelos[hora] + 1
        i = i + 1

    # Genera el gráfico
    plt.bar(range(24), vuelos)
    plt.xlabel("Horas")
    plt.ylabel("Número de vuelos")
    plt.title("Llegadas por hora")
    plt.show()


def SaveFlights(aircrafts, filename):
    """Guarda la información de la lista de aviones en un archivo de texto con el formato adecuado."""
    if len(aircrafts) == 0:
        return -1

    F = open(filename, "w")
    F.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")  # Cabecera

    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]

        # Validaciones: si algún campo está vacío, imprime un "-" en su lugar
        if aircraft.aircraft != "":
            aircraft_id = aircraft.aircraft
        else:
            aircraft_id = "-"

        if aircraft.origen != "":
            origin = aircraft.origen
        else:
            origin = "-"

        if aircraft.time != "":
            time = aircraft.time
        else:
            time = "-"

        if aircraft.airline != "":
            airline = aircraft.airline
        else:
            airline = "-"

        # Escribe la línea en el archivo
        F.write(f"{aircraft_id} {origin} {time} {airline}\n")
        i = i + 1

    F.close()


def PlotAirlines(aircrafts):
    """Muestra un gráfico de barras con el número de vuelos totales por cada aerolínea."""
    airlines = []  # Lista para guardar los nombres de aerolíneas únicas
    contador = []  # Lista para guardar el número de vuelos de cada aerolínea

    if len(aircrafts) == 0:
        print("Error")
        return

    i = 0
    # Bucle principal: recorre todos los vuelos
    while i < len(aircrafts):
        airline = aircrafts[i].airline
        encontrado = False
        j = 0

        # Bucle secundario: busca si la aerolínea ya está en nuestra lista de 'airlines'
        while j < len(airlines):
            if airlines[j] == airline:
                # Si la encuentra, suma 1 a su contador correspondiente
                contador[j] += 1
                encontrado = True
            j += 1

        # Si no la encuentra, es una aerolínea nueva: la añade y le pone contador 1
        if not encontrado:
            airlines.append(airline)
            contador.append(1)

        i += 1

    # Genera el gráfico (hace la figura más ancha para que quepan los nombres)
    plt.figure(figsize=(12, 6))
    plt.bar(airlines, contador)
    plt.xlabel("Aerolíneas")
    plt.ylabel("Número de vuelos")
    plt.title("Vuelos por aerolínea")
    plt.xticks(rotation=90)  # Rota el texto del eje X 90 grados para que se lea mejor
    plt.tight_layout()  # Ajusta los márgenes automáticamente
    plt.show()


def PlotFlightsType(aircrafts):
    """Muestra un gráfico de barras apiladas comparando vuelos origen Schengen vs No Schengen."""
    if len(aircrafts) == 0:
        print("Error: lista vacía")
        return

    # Lista de prefijos de países Schengen
    schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG',
                      'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP',
                      'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

    schengen = 0
    non_schengen = 0

    i = 0
    while i < len(aircrafts):
        origen = aircrafts[i].origen

        # Solo verifica si el código tiene al menos 2 caracteres
        if len(origen) >= 2:
            prefijo = origen[0:2]
            encontrado = False
            j = 0

            # Busca si el prefijo está en la lista Schengen
            while j < len(schengen_codes) and not encontrado:
                if schengen_codes[j] == prefijo:
                    encontrado = True
                j += 1

            if encontrado:
                schengen += 1
            else:
                non_schengen += 1
        else:
            non_schengen += 1  # Si el código está mal formado, va a No Schengen

        i += 1

    etiquetas = ['Tipo de Vuelos']
    plt.figure()

    # Dibuja la barra de Schengen primero, y la de No Schengen apilada encima (bottom=schengen)
    plt.bar(etiquetas, [schengen], label='Schengen', color='steelblue')
    plt.bar(etiquetas, [non_schengen], bottom=[schengen], label='No Schengen', color='lightcoral')

    plt.ylabel("Número de vuelos")
    plt.title("Llegadas: Schengen vs No Schengen")
    plt.legend()
    plt.show()


def MapFlights(aircrafts):
    """Genera un archivo KML que traza líneas en Google Earth desde el origen hasta LEBL."""
    try:
        if len(aircrafts) == 0:
            print("Error: lista vacía")
            return

        # Carga los datos de los aeropuertos para poder obtener sus coordenadas
        airports = LoadAirports("Airports.txt")

        # Coordenadas estáticas del aeropuerto de Barcelona El Prat (Destino)
        LEBL_LAT = 41.29
        LEBL_LON = 2.08

        schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED',
                          'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM',
                          'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

        # Abre el archivo KML
        F = open("flights.kml", "w")

        # Cabeceras XML y KML
        F.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        F.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        F.write('<Document>\n')

        # Estilo para líneas Schengen (verde, grosor 3)
        F.write('<Style id="schengen">\n')
        F.write('<LineStyle>\n')
        F.write('<color>ff00ff00</color>\n')
        F.write('<width>3</width>\n')
        F.write('</LineStyle>\n')
        F.write('</Style>\n')

        # Estilo para líneas No Schengen (rojo, grosor 3)
        F.write('<Style id="nonschengen">\n')
        F.write('<LineStyle>\n')
        F.write('<color>ff0000ff</color>\n')
        F.write('<width>3</width>\n')
        F.write('</LineStyle>\n')
        F.write('</Style>\n')

        i = 0
        while i < len(aircrafts):
            aircraft = aircrafts[i]
            airport = None
            encontrado = False
            j = 0

            # Busca el aeropuerto de origen en nuestra lista de 'airports' para sacar su lat y lon
            while j < len(airports) and not encontrado:
                if airports[j].code == aircraft.origen:
                    airport = airports[j]
                    encontrado = True
                else:
                    j += 1

            # Si encontramos el aeropuerto en la base de datos:
            if encontrado:
                prefijo = aircraft.origen[0:2]
                es_schengen = False
                k = 0

                # Verifica si es Schengen para asignarle color
                while k < len(schengen_codes) and not es_schengen:
                    if schengen_codes[k] == prefijo:
                        es_schengen = True
                    k += 1

                if es_schengen:
                    style = "#schengen"
                else:
                    style = "#nonschengen"

                # Escribe la línea ('LineString') desde Origen hasta LEBL
                F.write('<Placemark>\n')
                F.write(f'<name>{aircraft.aircraft}</name>\n')
                F.write(f'<styleUrl>{style}</styleUrl>\n')
                F.write('<LineString>\n')
                F.write('<coordinates>\n')
                # La estructura es Longitud,Latitud,Altitud. Punto 1 (Origen) y Punto 2 (LEBL)
                F.write(f'{airport.lon},{airport.lat},0 ')
                F.write(f'{LEBL_LON},{LEBL_LAT},0\n')
                F.write('</coordinates>\n')
                F.write('</LineString>\n')
                F.write('</Placemark>\n')

            i += 1

        # Cierra archivo
        F.write('</Document>\n')
        F.write('</kml>\n')
        F.close()

    except FileNotFoundError:
        print("No hay ficheros")
    except ValueError:
        print("Datos incorrectos")
    except IndexError:
        print("Datos incorrectos")

    # Intenta ejecutar el KML en el sistema operativo
    import os
    os.startfile("flights.kml")


def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia de círculo máximo entre dos puntos de la Tierra usando la fórmula Haversine.
    Los ángulos necesitan convertirse a radianes[cite: 554].
    """
    R = 6371  # Radio medio de la Tierra en kilómetros [cite: 549]
    import math

    # Conversión de grados a radianes
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # Fórmula matemática a [cite: 551]
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)

    # Fórmula matemática c [cite: 550]
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Retorna la distancia en km [cite: 542]
    return R * c


def LongDistanceArrivals(aircrafts):
    """Devuelve una lista con los aviones cuyo origen está a más de 2000 km de LEBL."""
    # Carga la base de aeropuertos para tener sus coordenadas
    airports = LoadAirports("Airports.txt")
    LEBL_LAT = 41.29
    LEBL_LON = 2.08

    result = []
    i = 0

    while i < len(aircrafts):
        aircraft = aircrafts[i]
        j = 0
        encontrado = False
        origen_airport = None

        # Busca el aeropuerto de origen de este vuelo concreto
        while j < len(airports) and not encontrado:
            if airports[j].code == aircraft.origen:
                origen_airport = airports[j]
                encontrado = True
            else:
                j += 1

        # Si lo encuentra, calcula la distancia
        if encontrado:
            dist = haversine(origen_airport.lat, origen_airport.lon, LEBL_LAT, LEBL_LON)

            # Si la distancia supera los 2000 km, requiere inspección y se añade a los resultados [cite: 217, 218]
            if dist > 2000:
                result.append(aircraft)

        i += 1

    return result


def LoadDepartures(filename):
    """Lee el fichero de salidas y devuelve una lista de Aircraft con origen y hora vacíos[cite: 387, 389]."""
    aircrafts = []
    try:
        F = open(filename, "r")
        F.readline()
        line = F.readline()

        while line != "":
            parts = line.strip().split()

            if len(parts) == 4:
                aircraft_id = parts[0]
                destination = parts[1]
                departure = parts[2]
                airline = parts[3]

                parts_time = departure.split(":")
                if len(parts_time) == 2:
                    # Creamos el objeto Aircraft dejando origen y time (llegada) vacíos
                    ac = Aircraft(aircraft_id, "", "", airline, destination, departure)
                    aircrafts.append(ac)

            line = F.readline()

        F.close()

    except FileNotFoundError:
        # Devuelve lista vacía y código de error si el archivo no existe [cite: 390]
        return [], -1

    return aircrafts


def MergeMovements(arrivals, departures):
    """Fusiona llegadas y salidas. Si hay ID coincidente y llegada < salida, se fusionan en el mismo objeto[cite: 398, 399]."""
    if len(arrivals) == 0 or len(departures) == 0:
        return -1  # Devuelve código de error si alguna lista está vacía [cite: 401]

    merged = []
    used_deps = [False] * len(departures)

    i = 0
    while i < len(arrivals):
        arr = arrivals[i]
        j = 0
        encontrado = False

        while j < len(departures) and not encontrado:
            dep = departures[j]
            # Si es el mismo avión y la salida no se ha usado
            if not used_deps[j] and arr.aircraft == dep.aircraft:

                # Comprobar tiempos para ver si son compatibles [cite: 399]
                if arr.time != "" and dep.departure != "":
                    arr_h = int(arr.time.split(":")[0])
                    arr_m = int(arr.time.split(":")[1])
                    dep_h = int(dep.departure.split(":")[0])
                    dep_m = int(dep.departure.split(":")[1])

                    arr_mins = arr_h * 60 + arr_m
                    dep_mins = dep_h * 60 + dep_m

                    if arr_mins < dep_mins:
                        # Tiempos compatibles, fusionar
                        new_ac = Aircraft(arr.aircraft, arr.origen, arr.time, arr.airline, dep.destination,
                                          dep.departure)
                        merged.append(new_ac)
                        used_deps[j] = True
                        encontrado = True

            j += 1

        if not encontrado:
            # Si no tiene salida asociada, se añade tal cual
            merged.append(arr)

        i += 1

    # Añadir las salidas que no tuvieron llegada (vuelos nocturnos) [cite: 400]
    j = 0
    while j < len(departures):
        if not used_deps[j]:
            merged.append(departures[j])
        j += 1

    return merged


def NightAircraft(aircrafts):
    """Filtra y devuelve solo los aviones que tienen salida pero información de llegada vacía[cite: 404]."""
    if len(aircrafts) == 0:
        return -1  # Código de error si lista vacía [cite: 405]

    night_flights = []
    i = 0
    while i < len(aircrafts):
        if aircrafts[i].time == "" and aircrafts[i].departure != "":
            night_flights.append(aircrafts[i])
        i += 1

    return night_flights
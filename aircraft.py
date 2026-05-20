import matplotlib.pyplot as plt
from airport import LoadAirports

class Aircraft:
    def __init__(self, aircraft, origen, time, airline):
        self.aircraft = str(aircraft)
        self.origen = str(origen)
        self.time = str(time)
        self.airline = str(airline)


def LoadArrivals(Filename):
    aircrafts = []
    try:
        F = open(Filename, "r")
        line = F.readline()
        i=1
        F

        while line!="":

            parts = line.strip().split()

            if len(parts) == 4:

                aircraft = parts[0]
                origen = parts[1]
                time = parts[2]
                airline = parts[3]
                parts_time = time.split(":")

                if len(parts_time) == 2:


                    hora = int(parts_time[0])
                    minuto = int(parts_time[1])

                    if 0 <= hora <= 23 and 0 <= minuto <= 59:
                        aircraft_obj = Aircraft(aircraft, origen, time, airline)
                        aircrafts.append(aircraft_obj)

            line=F.readline()
        F.close()
    except FileNotFoundError:
        aircrafts = []
    except ValueError:
        pass

    return aircrafts


def PlotArrivals(aircrafts):
    vuelos = [0] * 24
    if len(aircrafts) == 0:
        print("Error: lista vacía")
        return
    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        time = aircraft.time
        hora = int(time.split(":")[0])
        vuelos[hora] =vuelos[hora]+ 1
        i = i+1


    plt.bar(range(24), vuelos)
    plt.xlabel("Horas")
    plt.ylabel("Número de vuelos")
    plt.title("Llegadas por hora")
    plt.show()


def SaveFlights(aircrafts, filename):

    if len(aircrafts) == 0:
        return -1
    F=open(filename, "w")
    F.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
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
        F.write(f"{aircraft_id} {origin} {time} {airline}\n")
        i =i+ 1
    F.close()

def PlotAirlines(aircrafts):

    airlines = []
    contador = []

    if len(aircrafts) == 0:
        print("Error")
        return

    i = 0
    while i < len(aircrafts):
        airline = aircrafts[i].airline

        encontrado = False
        j = 0

        while j < len(airlines):
            if airlines[j] == airline:
                contador[j] += 1
                encontrado = True
            j += 1

        if not encontrado:
            airlines.append(airline)
            contador.append(1)

        i += 1
    plt.figure(figsize=(12,6))
    plt.bar(airlines, contador)
    plt.xlabel("Aerolíneas")
    plt.ylabel("Número de vuelos")
    plt.title("Vuelos por aerolínea")
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.show()



def PlotFlightsType(aircrafts):

    if len(aircrafts) == 0:
        print("Error: lista vacía")
        return

    schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG',
                      'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP',
                      'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

    schengen = 0
    non_schengen = 0

    i = 0
    while i < len(aircrafts):
        origen = aircrafts[i].origen

        if len(origen) >= 2:
            prefijo = origen[0:2]

            encontrado = False
            j = 0
            while j < len(schengen_codes) and not encontrado:
                if schengen_codes[j] == prefijo:
                    encontrado = True
                j += 1

            if encontrado:
                schengen += 1
            else:
                non_schengen += 1
        else:
            non_schengen += 1

        i += 1

    etiquetas = ['Tipo de Vuelos']

    plt.figure()

    plt.bar(etiquetas, [schengen], label='Schengen', color='steelblue')
    plt.bar(etiquetas, [non_schengen], bottom=[schengen], label='No Schengen', color='lightcoral')

    plt.ylabel("Número de vuelos")
    plt.title("Llegadas: Schengen vs No Schengen")
    plt.legend()
    plt.show()

def MapFlights(aircrafts):
    try:
        if len(aircrafts) == 0:
            print("Error: lista vacía")
            return
        airports = LoadAirports("airports.txt")

        LEBL_LAT = 41.29
        LEBL_LON = 2.08

        schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED',
                          'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM',
                          'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']

        F = open("flights.kml", "w")

        F.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        F.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        F.write('<Document>\n')


        F.write('<Style id="schengen">\n')
        F.write('<LineStyle>\n')
        F.write('<color>ff00ff00</color>\n')
        F.write('<width>3</width>\n')
        F.write('</LineStyle>\n')
        F.write('</Style>\n')


        F.write('<Style id="nonschengen">\n')
        F.write('<LineStyle>\n')
        F.write('<color>ff0000ff</color>\n')
        F.write('<width>3</width>\n')
        F.write('</LineStyle>\n')
        F.write('</Style>\n')

        i = 0
        while i < len(aircrafts):

            aircraft = aircrafts[i]
            airport=None
            encontrado = False
            j = 0

            while j < len(airports) and not encontrado:
                if airports[j].code == aircraft.origen:
                    airport = airports[j]
                    encontrado = True
                else:
                    j += 1

            if encontrado:

                prefijo = aircraft.origen[0:2]

                es_schengen = False
                k = 0

                while k < len(schengen_codes) and not es_schengen:
                    if schengen_codes[k] == prefijo:
                        es_schengen = True
                    k += 1

                if es_schengen:
                    style = "#schengen"
                else:
                    style = "#nonschengen"

                F.write('<Placemark>\n')
                F.write(f'<name>{aircraft.aircraft}</name>\n')
                F.write(f'<styleUrl>{style}</styleUrl>\n')
                F.write('<LineString>\n')
                F.write('<coordinates>\n')
                F.write(f'{airport.lon},{airport.lat},0 ')
                F.write(f'{LEBL_LON},{LEBL_LAT},0\n')
                F.write('</coordinates>\n')
                F.write('</LineString>\n')
                F.write('</Placemark>\n')

            i += 1

        F.write('</Document>\n')
        F.write('</kml>\n')

        F.close()
    except FileNotFoundError:
        print("No hay ficheros")
    except ValueError:
        print("Datos incorrectos")
    except IndexError:
        print("Datos incorrectos")
    import os
    os.startfile("flights.kml")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    import math
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


    return R * c


def LongDistanceArrivals(aircrafts):

    airports = LoadAirports("airports.txt")
    LEBL_LAT = 41.29
    LEBL_LON = 2.08

    result = []
    i = 0

    while i < len(aircrafts):
        aircraft = aircrafts[i]

        j = 0
        encontrado = False
        origen_airport = None

        while j < len(airports) and not encontrado:
            if airports[j].code == aircraft.origen:
                origen_airport = airports[j]
                encontrado = True
            else:
                j += 1

        if encontrado:
            dist = haversine(origen_airport.lat,origen_airport.lon,LEBL_LAT,LEBL_LON )

            if dist > 2000:
                result.append(aircraft)

        i += 1

    return result









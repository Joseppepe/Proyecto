import matplotlib.pyplot as plt

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



        while line!="":

            parts = line[i].strip().split()

            if len(parts) == 4:

                aircraft = parts[0]
                origen = parts[1]
                time = parts[2]
                airline = parts[3]

                encontrado = False
                j = 0

                while j < len(time) and not encontrado:
                    if time[j] == ":":
                        encontrado = True
                    else:
                        j = j + 1

                if encontrado:
                    aircraft_obj = Aircraft(aircraft, origen, time, airline)
                    aircrafts.append(aircraft_obj)
            line = F.readline()
        F.close()

    except FileNotFoundError:
        aircrafts = []

    return aircrafts


def PlotArrivals(aircrafts):
    vuelos = [0] * 24

    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        time = aircraft.time
        hora = int(time[0:2])
        vuelos[hora] =vuelos[hora]+ 1
        i = i+1

    if len(aircrafts) == 0:
        print("Error: lista vacía")
        return

    plt.bar(range(24), vuelos)
    plt.xlabel("Horas")
    plt.ylabel("Número de vuelos")
    plt.title("Llegadas por hora")
    plt.show()


def SaveFlights(aircrafts, filename):

    if len(aircrafts) == 0:
        print("Error: lista vacía")
        return
    F=open(filename, "w")
    F.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        if aircraft.aircraft != "":
            id = aircraft.aircraft
        else:
            id = "-"
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
        F.write(f"{id} {origin} {time} {airline}\n")
        i =i+ 1
    F.close()

    def PlotAirlines(aircrafts):
        airlines = []
        contador = []

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



    plt.bar(airlines, contador)
    plt.xlabel("Aerolíneas")
    plt.ylabel("Número de vuelos")
    plt.title("Vuelos por aerolínea")
    plt.xticks(rotation=45)
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

    plt.bar(etiquetas, [schengen], label='Schengen', color='steelblue')
    plt.bar(etiquetas, [non_schengen], bottom=[schengen], label='No Schengen', color='lightcoral')

    plt.ylabel("Número de vuelos")
    plt.title("Llegadas: Schengen vs No Schengen")
    plt.legend()
    plt.show()

def MapAirports(airports):

    try:
         F=open("airports.kml","w")

         F.write('<?xml version="1.0">\n')
         F.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
         F.write('<Document>\n')

         i=0
         while i<len(airports):

            airport = airports[i]

            F.write("<Placemark>\n")
            F.write(f"<name>{airport.code}</name>\n")
            F.write("<Point>\n")
            F.write(f"<coordinates>{airport.lon},{airport.lat},0</coordinates>\n")
            F.write("</Point>\n")
            F.write("</Placemark>\n")

            i=i+1

         F.write('</Document>\n')
         F.write('</kml>\n')

         F.close()
    except FileNotFoundError:
        print("No hay ficheros")
    except ValueError:
        print("Datos incorrectos")
    except IndexError:
        print("Datos incorrectos")

import math


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c



def LongDistanceArrivals(aircrafts):

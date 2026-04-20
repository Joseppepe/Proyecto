import matplotlib.pyplot as plt

class Aircraft:
    def __init__(self, aircraft, origen, time, airline):
        self.aircraft = str(aircraft)
        self.origen = str(origen)
        self.time = str(time)
        self.airline = str(airline)


def LoadArrivals(filename):
    aircrafts = []

    try:
        with open(filename, "r") as F:
            lines = F.readlines()

        i = 1  # saltar cabecera

        while i < len(lines):
            parts = lines[i].split()

            if len(parts) == 4:
                aircraft = parts[0]
                origen = parts[1]
                time = parts[2]
                airline = parts[3]

                if ":" in time:
                    obj = Aircraft(aircraft, origen, time, airline)
                    aircrafts.append(obj)

            i += 1

    except FileNotFoundError:
        print("Archivo no encontrado")

    return aircrafts


def PlotArrivals(aircrafts):
    vuelos = [0] * 24

    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        time = aircraft.time
        hora = int(time[0:2])
        vuelos[hora] += 1
        i += 1

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

    with open(filename, "w") as F:
        F.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")

        i = 0
        while i < len(aircrafts):
            aircraft = aircrafts[i]

            id = aircraft.aircraft if aircraft.aircraft != "" else "-"
            origin = aircraft.origen if aircraft.origen != "" else "-"
            time = aircraft.time if aircraft.time != "" else "-"
            airline = aircraft.airline if aircraft.airline != "" else "-"

            F.write(f"{id} {origin} {time} {airline}\n")
            i += 1


def PlotAirlines(aircrafts):
    airlines = []
    contador = []

    i = 0
    while i < len(aircrafts):
        airline = aircrafts[i].airline

        if airline in airlines:
            j = airlines.index(airline)
            contador[j] += 1
        else:
            airlines.append(airline)
            contador.append(1)

        i += 1

    plt.bar(airlines, contador)
    plt.xlabel("Aerolíneas")
    plt.ylabel("Número de vuelos")
    plt.title("Vuelos por aerolínea")
    plt.xticks(rotation=45)
    plt.show()
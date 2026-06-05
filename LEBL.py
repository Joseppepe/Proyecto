from airport import IsSchengenAirport


class BarcelonaAP:
    """Clase principal que representa el aeropuerto, conteniendo un código y una lista de terminales."""

    def __init__(self, code):
        self.code = code
        self.terminals = []


class Terminal:
    """Clase que representa una terminal del aeropuerto (ej. T1 o T2). Contiene áreas de embarque y aerolíneas que operan en ella."""

    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airline_codes = []

    def __str__(self):
        # Método para imprimir la terminal de forma legible
        return f"Terminal {self.name} | Areas: {len(self.boarding_areas)} | Airlines: {len(self.airline_codes)}"


class BoardingArea:
    """Clase que representa un área de embarque dentro de una terminal (ej. Área A). Define si es Schengen o no, y contiene puertas."""

    def __init__(self, name, area_type):
        self.name = name
        self.type = area_type  # "Schengen" o "non-Schengen"
        self.gates = []

    def __str__(self):
        return f"Area {self.name} ({self.type}) - Gates: {len(self.gates)}"


class Gate:
    """Clase que representa una puerta de embarque individual. Guarda su estado de ocupación y el avión asignado."""

    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = ""

    def __str__(self):
        status = f"Occupied by {self.aircraft_id}" if self.occupied else "Free"
        return f"Gate {self.name}: {status}"


def SetGates(area, init_gate, end_gate, prefix):
    """Genera las puertas de embarque para un área dada, desde un número inicial hasta uno final, y les asigna un prefijo."""
    # Validación: si el número final es menor o igual al inicial, hay un error en los datos
    if end_gate <= init_gate:
        return -1

    # Reinicia la lista de puertas por si ya tenía datos
    area.gates = []

    i = init_gate
    # Bucle para crear cada puerta en el rango especificado
    while i <= end_gate:
        # Crea el nombre concatenando el prefijo (ej. T1A) y el número (ej. 1) -> T1A1
        gate_name = prefix + str(i)

        gate = Gate(gate_name)
        gate.occupied = False
        gate.aircraft_id = ""

        # Añade la puerta recién creada a la lista del área
        area.gates.append(gate)

        i += 1


def LoadAirlines(terminal, t_name):
    """Lee el archivo de aerolíneas correspondiente a una terminal y guarda sus códigos ICAO en la clase Terminal."""
    # Decide qué archivo abrir basándose en el nombre de la terminal
    if t_name == "T1":
        filename = "T1_Airlines.txt"
    else:
        filename = "T2_Airlines.txt"

    try:
        F = open(filename, "r")
        airline_codes = []
        line = F.readline()

        while line != "":
            parts = line.split()

            # Asegura que la línea tenga suficientes elementos.
            # parts[2] asume que el código ICAO es la tercera palabra en el txt.
            if len(parts) >= 3:
                icao_code = parts[2]
                airline_codes.append(icao_code)

            line = F.readline()

        F.close()

        # Asigna la lista completada al objeto terminal
        terminal.airline_codes = airline_codes

    except FileNotFoundError:
        return -1


def LoadAirportStructure(filename):
    """Lee el archivo de estructura (ej. Terminals.txt) y construye toda la jerarquía de objetos del aeropuerto."""
    try:
        F = open(filename, "r")
    except:
        return ""  # Si falla, devuelve un string vacío (como indicador de error)

    # Crea el objeto principal del aeropuerto
    airport = BarcelonaAP("LEBL")

    # Crea las dos terminales estáticas
    t1 = Terminal("T1")
    t2 = Terminal("T2")

    t1.boarding_areas = []
    t2.boarding_areas = []

    line = F.readline()

    # Bucle principal de lectura del archivo de estructura
    while line != "":
        parts = line.split()

        # Si la línea describe un Área de embarque
        if len(parts) > 0 and parts[0] == "Area":
            area_name = parts[1]
            init_gate = int(parts[4])
            end_gate = int(parts[6])

            # Crea el objeto del Área (parts[2] será "Schengen" o "non-Schengen")
            area = BoardingArea(area_name, parts[2])

            # Clasifica el área en T1 o T2 según su letra
            if area_name == "A" or area_name == "B" or area_name == "C" or area_name == "D" or area_name == "E":
                prefix = "T1" + area_name
                SetGates(area, init_gate, end_gate, prefix)  # Genera sus puertas
                t1.boarding_areas.append(area)
            else:
                prefix = "T2" + area_name
                SetGates(area, init_gate, end_gate, prefix)  # Genera sus puertas
                t2.boarding_areas.append(area)

        line = F.readline()

    F.close()

    # Una vez montada la estructura, carga las aerolíneas de cada terminal
    LoadAirlines(t1, "T1")
    LoadAirlines(t2, "T2")

    # Añade las terminales completas al aeropuerto
    airport.terminals.append(t1)
    airport.terminals.append(t2)

    return airport


def GateOccupancy(bcn):
    """Recorre toda la jerarquía del aeropuerto y devuelve una lista con tuplas del estado de todas las puertas."""
    occupancy = []

    i = 0
    # Nivel 1: Recorre terminales
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]
        j = 0

        # Nivel 2: Recorre áreas de embarque dentro de la terminal
        while j < len(terminal.boarding_areas):
            area = terminal.boarding_areas[j]
            k = 0

            # Nivel 3: Recorre puertas dentro del área
            while k < len(area.gates):
                gate = area.gates[k]

                # Guarda una tupla con (nombre de puerta, si está ocupada, id del avión)
                gate_info = (gate.name, gate.occupied, gate.aircraft_id)
                occupancy.append(gate_info)

                k = k + 1
            j = j + 1
        i = i + 1

    return occupancy


def IsAirlineInTerminal(terminal, name):
    """Verifica si una aerolínea (por su código) opera en una terminal específica."""
    if name == "":
        return False

    if len(terminal.airline_codes) == 0:
        return False

    encontrado = False
    i = 0

    # Bucle de búsqueda lineal en la lista de aerolíneas de la terminal
    while i < len(terminal.airline_codes) and not encontrado:
        if terminal.airline_codes[i] == name:
            encontrado = True
        else:
            encontrado = False
        i = i + 1

    return encontrado


def SearchTerminal(bcn, name):
    """Busca en todas las terminales del aeropuerto y devuelve el nombre de la terminal donde opera la aerolínea."""
    i = 0

    # Recorre las terminales del aeropuerto
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        # Usa la función auxiliar para comprobar si la aerolínea está aquí
        if IsAirlineInTerminal(terminal, name):
            return terminal.name  # Si la encuentra, devuelve "T1" o "T2" y sale de la función

        i += 1

    return ""  # Si termina el bucle y no la encuentra, devuelve vacío


def AssignGate(bcn, aircraft):
    """
    Versión actualizada para V4: Asigna puerta. Si el vuelo es nocturno (origen vacío),
    comprueba el destino para saber si el área debe ser Schengen.
    """
    terminal_name = SearchTerminal(bcn, aircraft.airline)

    if terminal_name == "":
        return -1

    tipo = "Schengen"
    # Diferencia entre vuelo normal/llegada y vuelo nocturno (solo salida)
    if aircraft.origen != "":
        if not IsSchengenAirport(aircraft.origen):
            tipo = "non-Schengen"
    else:
        if not IsSchengenAirport(aircraft.destination):
            tipo = "non-Schengen"

    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        if terminal.name == terminal_name:
            j = 0
            while j < len(terminal.boarding_areas):
                area = terminal.boarding_areas[j]

                if area.type == tipo:
                    k = 0
                    while k < len(area.gates):
                        gate = area.gates[k]

                        if gate.occupied == False:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.aircraft
                            return gate.name

                        k += 1
                j += 1
        i += 1

    return -1


# Sección de prueba recomendada para comprobar las funciones de LEBL.py
if __name__ == "__main__":
    # Ejemplo de uso básico (asegúrate de tener LEBL.txt y los archivos de aerolíneas en la misma carpeta)
    pass


def AssignNightGates(bcn, aircrafts):
    """Asigna puerta a los aviones que hacen noche utilizando la nueva versión de AssignGate[cite: 408]."""
    if len(aircrafts) == 0:
        return -1

    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        # Verificar que sea solo un vuelo de salida (llegada vacía) [cite: 408]
        if ac.time == "" and ac.departure != "":
            AssignGate(bcn, ac)
        i += 1


def FreeGate(bcn, id):
    """Busca el id del avión en el estado del aeropuerto bcn y libera su puerta[cite: 410, 411]."""
    encontrado = False
    i = 0
    while i < len(bcn.terminals) and not encontrado:
        terminal = bcn.terminals[i]
        j = 0
        while j < len(terminal.boarding_areas) and not encontrado:
            area = terminal.boarding_areas[j]
            k = 0
            while k < len(area.gates) and not encontrado:
                gate = area.gates[k]
                if gate.occupied and gate.aircraft_id == id:
                    gate.occupied = False
                    gate.aircraft_id = ""
                    encontrado = True
                k += 1
            j += 1
        i += 1

    if not encontrado:
        return -1  # Error si el avión no es encontrado [cite: 412]


def AssignGatesAtTime(bcn, aircrafts, time):
    """Libera puertas de aviones que ya se fueron y asigna a los que llegan en el periodo de una hora[cite: 425]."""
    target_hour = int(time.split(":")[0])

    # 1. Liberar puertas (aviones cuya hora de salida es ANTERIOR a la hora a evaluar) [cite: 425]
    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]
        j = 0
        while j < len(terminal.boarding_areas):
            area = terminal.boarding_areas[j]
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]
                if gate.occupied:
                    ac_id = gate.aircraft_id

                    # Buscar a qué hora se va este avión
                    w = 0
                    found_ac = False
                    ac_dep_hour = -1

                    while w < len(aircrafts) and not found_ac:
                        if aircrafts[w].aircraft == ac_id:
                            if aircrafts[w].departure != "":
                                ac_dep_hour = int(aircrafts[w].departure.split(":")[0])
                            found_ac = True
                        w += 1

                    # Si encontramos su hora de salida y es estrictamente anterior a la hora actual, liberamos la puerta
                    if found_ac and ac_dep_hour != -1 and ac_dep_hour < target_hour:
                        FreeGate(bcn, ac_id)

                k += 1
            j += 1
        i += 1

    # 2. Asignar puertas a los que aterrizan en ESTE periodo de 1 hora [cite: 425]
    unassigned = 0
    x = 0
    while x < len(aircrafts):
        ac = aircrafts[x]
        if ac.time != "":
            arr_hour = int(ac.time.split(":")[0])
            if arr_hour == target_hour:
                res = AssignGate(bcn, ac)
                # Si AssignGate devuelve -1 significa que la puerta está llena
                if res == -1:
                    unassigned += 1
        x += 1

    return unassigned


def PlotDayOccupancy(bcn, aircrafts):
    """Simula todo el día, hora a hora, y muestra la ocupación por terminal y aviones no asignados[cite: 429, 431]."""
    import matplotlib.pyplot as plt

    horas = []
    ocupacion_t1 = []
    ocupacion_t2 = []
    no_asignados = []

    h = 0
    # Bucle de las 24 horas del día ("00:00" a "23:00")
    while h < 24:
        time_str = str(h) + ":00"
        if h < 10:
            time_str = "0" + str(h) + ":00"

        horas.append(time_str)

        # Asignar y liberar puertas en esta hora [cite: 431]
        unasigned_now = AssignGatesAtTime(bcn, aircrafts, time_str)
        no_asignados.append(unasigned_now)

        # Contar ocupación actual
        t1_occ = 0
        t2_occ = 0

        i = 0
        while i < len(bcn.terminals):
            terminal = bcn.terminals[i]
            occ_count = 0
            j = 0
            while j < len(terminal.boarding_areas):
                area = terminal.boarding_areas[j]
                k = 0
                while k < len(area.gates):
                    if area.gates[k].occupied:
                        occ_count += 1
                    k += 1
                j += 1

            if terminal.name == "T1":
                t1_occ = occ_count
            elif terminal.name == "T2":
                t2_occ = occ_count

            i += 1

        ocupacion_t1.append(t1_occ)
        ocupacion_t2.append(t2_occ)

        h += 1

    # Dibuja el gráfico [cite: 431]
    plt.figure(figsize=(12, 6))
    plt.plot(horas, ocupacion_t1, label="Ocupación T1", marker='o', color='blue')
    plt.plot(horas, ocupacion_t2, label="Ocupación T2", marker='x', color='green')
    plt.bar(horas, no_asignados, label="No Asignados", color='red', alpha=0.5)

    plt.xlabel("Hora del día")
    plt.ylabel("Número de Puertas / Aviones")
    plt.title("Ocupación diaria del aeropuerto LEBL")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
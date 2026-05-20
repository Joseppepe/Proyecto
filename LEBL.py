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
    """Lee el archivo de estructura (ej. LEBL.txt) y construye toda la jerarquía de objetos del aeropuerto."""
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
    Lógica principal de asignación:
    Busca la primera puerta libre en la terminal correcta y en el tipo de área correcto (Schengen/No Schengen).
    """
    # 1. Averigua a qué terminal va este avión
    terminal_name = SearchTerminal(bcn, aircraft.airline)

    # Si la aerolínea no está registrada, no puede asignar puerta
    if terminal_name == "":
        return -1

    # 2. Averigua el tipo de vuelo (Schengen o non-Schengen) usando la función importada
    tipo = "Schengen"
    if not IsSchengenAirport(aircraft.origen):
        tipo = "non-Schengen"

    i = 0
    # Nivel 1: Recorre terminales para buscar la que coincide
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        if terminal.name == terminal_name:
            j = 0

            # Nivel 2: Busca áreas dentro de esa terminal que coincidan con el 'tipo' (Schengen/non-Schengen)
            while j < len(terminal.boarding_areas):
                area = terminal.boarding_areas[j]

                if area.type == tipo:
                    k = 0

                    # Nivel 3: Busca la primera puerta que no esté ocupada
                    while k < len(area.gates):
                        gate = area.gates[k]

                        if gate.occupied == False:
                            # ¡Puerta encontrada! La marca como ocupada, guarda el avión y devuelve el nombre
                            gate.occupied = True
                            gate.aircraft_id = aircraft.aircraft
                            return gate.name

                        k += 1
                j += 1
        i += 1

    # Si recorre todo y no hay puertas libres (o no hay áreas de ese tipo), devuelve error
    return -1


# Sección de prueba recomendada para comprobar las funciones de LEBL.py
if __name__ == "__main__":
    # Ejemplo de uso básico (asegúrate de tener LEBL.txt y los archivos de aerolíneas en la misma carpeta)
    pass
from airport import IsSchengenAirport

class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airline_codes = []

    def __str__(self):
        return f"Terminal {self.name} | Areas: {len(self.boarding_areas)} | Airlines: {len(self.airline_codes)}"


class BoardingArea:
    def __init__(self, name, area_type,):
        self.name = name
        self.type = area_type
        self.gates = []

    def __str__(self):
        return f"Area {self.name} ({self.type}) - Gates: {len(self.gates)}"


class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = ""

    def __str__(self):
        status = f"Occupied by {self.aircraft_id}" if self.occupied else "Free"
        return f"Gate {self.name}: {status}"


def SetGates(area, init_gate, end_gate,prefix):
    if end_gate <= init_gate:
        return -1

    area.gates = []

    i = init_gate
    while i <= end_gate:
        gate_name = prefix + str(i)

        gate = Gate(gate_name)
        gate.occupied = False
        gate.aircraft_id = ""

        area.gates.append(gate)

        i += 1


def LoadAirlines(terminal, t_name):
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

            if len(parts) >= 3:
                icao_code = parts[2]
                airline_codes.append(icao_code)

            line = F.readline()

        F.close()

        terminal.airline_codes = airline_codes

    except FileNotFoundError:
        return -1

def LoadAirportStructure(filename):
    try:
        F = open(filename, "r")
    except:
        return ""

    airport = BarcelonaAP("LEBL")

    t1 = Terminal("T1")
    t2 = Terminal("T2")

    t1.boarding_areas = []
    t2.boarding_areas = []

    line = F.readline()

    while line != "":
        parts = line.split()

        if len(parts) > 0 and parts[0] == "Area":
            area_name = parts[1]

            init_gate = int(parts[4])
            end_gate = int(parts[6])

            area = BoardingArea(area_name, parts[2])

            if area_name == "A" or area_name == "B" or area_name == "C" or area_name == "D" or area_name == "E":
                prefix = "T1" + area_name
                SetGates(area, init_gate, end_gate, prefix)
                t1.boarding_areas.append(area)
            else:
                prefix = "T2" + area_name
                SetGates(area, init_gate, end_gate, prefix)
                t2.boarding_areas.append(area)

        line = F.readline()

    F.close()

    LoadAirlines(t1, "T1")
    LoadAirlines(t2, "T2")

    airport.terminals.append(t1)
    airport.terminals.append(t2)

    return airport

def GateOccupancy(bcn):
    occupancy=[]
    i=0
    while i<len(bcn.terminals):
        terminal=bcn.terminals[i]
        j=0

        while j<len(terminal.boarding_areas):
            area=terminal.boarding_areas[j]

            k=0

            while k<len(area.gates):
                gate=area.gates[k]

                gate_info=( gate.name,gate.occupied,gate.aircraft_id)


                occupancy.append(gate_info)
                k=k+1
            j=j+1
        i=i+1
    return occupancy


def IsAirlineInTerminal(terminal, name):

    if name=="":
        return False

    if len(terminal.airline_codes)==0:
        return False


    encontrado=False
    i=0

    while i<len(terminal.airline_codes) and not encontrado:
            if terminal.airline_codes[i]==name:
             encontrado=True
            else:
               encontrado=False

            i=i+1

    return encontrado

def SearchTerminal(bcn, name):
    i = 0

    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        if IsAirlineInTerminal(terminal, name):
            return terminal.name

        i += 1

    return ""

def AssignGate(bcn, aircraft):
    terminal_name = SearchTerminal(bcn, aircraft.airline)

    if terminal_name == "":
        return -1

    tipo="Schengen"
    if not IsSchengenAirport(aircraft.origen):
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

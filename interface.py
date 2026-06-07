from tkinter import *
# Importamos las funciones y clases de los módulos que has creado
from aircraft import *
from airport import *
from LEBL import *

# Variables globales
airports = []
aircrafts = []
lebl_airport = []

# --- COLORES AMIGABLES DE LA INTERFAZ ---
BG_COLOR = "#B0BEC5"
TEXT_COLOR = "#1A252C"
CONSOLE_BG = "#2E3440"
CONSOLE_FG = "#D8DEE9"
RESULT_BG = "#3B4252"
RESULT_FG = "#88C0D0"

# ==========================================
# FUNCIONES DE SONIDO (SONIDOS DEL SISTEMA)
# ==========================================

def play_click_sound():
    """Sonido del sistema suave (clic/notificación estándar de Windows)."""
    try:
        import winsound
        # SystemDefault es el sonido de navegación o clic por defecto del PC
        winsound.PlaySound("SystemDefault", winsound.SND_ALIAS | winsound.SND_ASYNC)
    except ImportError:
        window.bell()  # Plan B para Mac/Linux

def play_loading_sound():
    """Sonido un poco más largo/musical para indicar que se abre algo nuevo."""
    try:
        import winsound
        # SystemAsterisk es el sonido de "Información" (muy suave y agradable)
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
    except ImportError:
        window.bell()

# FUNCIONES AUXILIARES DE LA INTERFAZ

def log_message(title, message):
    console_text.config(state=NORMAL)
    console_text.insert(END, f"[{title}] {message}\n")
    console_text.see(END)
    console_text.config(state=DISABLED)

def clear_main_console():
    console_text.config(state=NORMAL)
    console_text.delete("1.0", END)
    console_text.config(state=DISABLED)

def result_message(message):
    results_text.config(state=NORMAL)
    results_text.delete("1.0", END)
    results_text.insert(END, message)
    results_text.config(state=DISABLED)

def show_file(filename):
    try:
        F = open(filename, "r")
        line = F.readline()
        log_message("File", f"Showing {filename} contents:")
        while line != "":
            log_message(filename, line.strip())
            line = F.readline()
        F.close()
    except FileNotFoundError:
        log_message("Error", f"Could not open '{filename}'. File not found.")

def DrawOccupancyWindow():
    map_window = Toplevel(window)
    map_window.title("Gate Occupancy")
    map_window.geometry("1200x600")
    canvas = Canvas(map_window, bg="white")
    canvas.pack(fill=BOTH, expand=True)
    occupancy = GateOccupancy(lebl_airport[0])

    canvas.create_rectangle(20, 40, 550, 60, fill="#0B5C7A")
    canvas.create_text(285, 20, text="T1", font=("Arial", 16, "bold"), fill=TEXT_COLOR)
    canvas.create_rectangle(650, 40, 1150, 60, fill="#0B5C7A")
    canvas.create_text(900, 20, text="T2", font=("Arial", 16, "bold"), fill=TEXT_COLOR)

    areas_x = {"T1A": 80, "T1B": 180, "T1C": 280, "T1D": 380, "T1E": 480,
               "T2M": 720, "T2R": 800, "T2S": 880, "T2U": 960, "T2W": 1040, "T2Y": 1120}

    for area in areas_x:
        x = areas_x[area]
        canvas.create_rectangle(x, 60, x + 18, 320, fill="#0B5C7A")
        canvas.create_text(x + 9, 340, text=area, font=("Arial", 9, "bold"), fill=TEXT_COLOR)

    posiciones = {}
    lado = {}
    for area in areas_x:
        posiciones[area] = 90
        lado[area] = 0

    i = 0
    while i < len(occupancy):
        gate_name = occupancy[i][0]
        occupied = occupancy[i][1]
        aircraft = occupancy[i][2]

        area = ""
        if gate_name.startswith("T1A"): area = "T1A"
        elif gate_name.startswith("T1B"): area = "T1B"
        elif gate_name.startswith("T1C"): area = "T1C"
        elif gate_name.startswith("T1D"): area = "T1D"
        elif gate_name.startswith("T1E"): area = "T1E"
        elif gate_name.startswith("T2M"): area = "T2M"
        elif gate_name.startswith("T2R"): area = "T2R"
        elif gate_name.startswith("T2S"): area = "T2S"
        elif gate_name.startswith("T2U"): area = "T2U"
        elif gate_name.startswith("T2W"): area = "T2W"
        elif gate_name.startswith("T2Y"): area = "T2Y"

        if area != "":
            x = areas_x[area]
            y = posiciones[area]
            color = "red" if occupied else "green"

            if lado[area] % 2 == 0:
                canvas.create_line(x, y, x - 20, y, width=2)
                canvas.create_rectangle(x - 30, y - 4, x - 20, y + 4, fill=color)
                if occupied:
                    canvas.create_text(x - 35, y, text=aircraft, anchor="e", font=("Arial", 6))
            else:
                canvas.create_line(x + 18, y, x + 38, y, width=2)
                canvas.create_rectangle(x + 38, y - 4, x + 48, y + 4, fill=color)
                if occupied:
                    canvas.create_text(x + 53, y, text=aircraft, anchor="w", font=("Arial", 6))
            lado[area] += 1
            posiciones[area] += 12
        i += 1

def DrawAirportWindow():
    map_window = Toplevel(window)
    map_window.title("Gate Assignment")
    map_window.geometry("1200x600")
    canvas = Canvas(map_window, bg="white")
    canvas.pack(fill=BOTH, expand=True)

    occupancy = GateOccupancy(lebl_airport[0])

    canvas.create_rectangle(20, 40,550, 60,fill="#0B5C7A")
    canvas.create_text(285,20,text="T1",font=("Arial", 16, "bold"), fill=TEXT_COLOR)
    canvas.create_rectangle(650, 40,1150, 60,fill="#0B5C7A")
    canvas.create_text(900,20,text="T2",font=("Arial", 16, "bold"), fill=TEXT_COLOR)

    areas_x = {"T1A": 80, "T1B": 180, "T1C": 280, "T1D": 380, "T1E": 480,
               "T2M": 720, "T2R": 800, "T2S": 880, "T2U": 960, "T2W": 1040, "T2Y": 1120}

    for area in areas_x:
        x = areas_x[area]
        canvas.create_rectangle(x,60,x + 18,320,fill="#0B5C7A")
        canvas.create_text(x + 9,340,text=area,font=("Arial", 9, "bold"), fill=TEXT_COLOR)

    posiciones = {}
    lado = {}
    for area in areas_x:
        posiciones[area] = 90
        lado[area] = 0

    i = 0
    while i < len(occupancy):
        gate_name = occupancy[i][0]
        occupied = occupancy[i][1]
        aircraft = occupancy[i][2]

        area = ""
        if gate_name.startswith("T1A"): area = "T1A"
        elif gate_name.startswith("T1B"): area = "T1B"
        elif gate_name.startswith("T1C"): area = "T1C"
        elif gate_name.startswith("T1D"): area = "T1D"
        elif gate_name.startswith("T1E"): area = "T1E"
        elif gate_name.startswith("T2M"): area = "T2M"
        elif gate_name.startswith("T2R"): area = "T2R"
        elif gate_name.startswith("T2S"): area = "T2S"
        elif gate_name.startswith("T2U"): area = "T2U"
        elif gate_name.startswith("T2W"): area = "T2W"
        elif gate_name.startswith("T2Y"): area = "T2Y"

        if area != "" and occupied == True:
            x = areas_x[area]
            y = posiciones[area]

            if lado[area] % 2 == 0:
                canvas.create_line(x,y,x - 20,y,width=2)
                canvas.create_rectangle(x - 30,y - 4,x - 20,y + 4,fill="green")
                canvas.create_text(x - 35,y,text=aircraft,anchor="e",font=("Arial", 6))
            else:
                canvas.create_line(x + 18,y,x + 38,y, width=2)
                canvas.create_rectangle(x + 38,y - 4,x + 48,y + 4,fill="green")
                canvas.create_text(x + 53,y,text=aircraft,anchor="w",font=("Arial", 6))

            lado[area] += 1
            posiciones[area] += 12
        i += 1


# FUNCIONES DE LOS BOTONES (VERSIÓN 1)

def EntrarClick():
    play_click_sound()
    clear_main_console()
    airports[:] = LoadAirports("Airports.txt")
    if len(airports) > 0:
        for airport in airports:
            log_message("Airport", f"{airport.code}   {airport.lat:.4f}   {airport.lon:.4f}   {airport.schengen}")
        result_message(f"Loaded airports: {len(airports)}")
    else:
        log_message("Error", "Could not load airports. Ensure 'Airports.txt' exists and is not empty.")
        result_message("No airports loaded")

def AClick():
    play_click_sound()
    clear_main_console()
    entrada = fraseEntry.get().strip()
    if not entrada:
        log_message("Error", "Input box is empty. Please enter data to add an airport.")
        log_message("Info", "Required format: CODE LAT LON (e.g., LEBL 41.29 2.07)")
        return

    try:
        datos = entrada.split()
        code = datos[0]
        lat = float(datos[1])
        lon = float(datos[2])
        antes = len(airports)

        airport = Airport(code, lat, lon)
        SetSchengen(airport)
        AddAirport(airports, airport)

        if len(airports) > antes:
            log_message("Success", f"Airport {code} added correctly.")
        else:
            log_message("Warning", f"Airport {code} already exists in the system.")
    except (ValueError, IndexError):
        log_message("Error", "Invalid format. Ensure you typed: CODE LAT LON (e.g., LEBL 41.29 2.07)")

def BClick():
    play_click_sound()
    clear_main_console()
    if len(airports) == 0:
        log_message("Error", "Cannot remove. The airport list is currently empty. Load or add airports first.")
        return

    entrada = fraseEntry.get().strip()
    if not entrada:
        log_message("Error", "Input box is empty. Type the CODE of the airport you want to remove (e.g. LEBL).")
        return

    antes = len(airports)
    code = entrada.split()[0]
    RemoveAirport(airports, code)

    if len(airports) < antes:
        log_message("Success", f"Airport {code} removed correctly.")
    else:
        log_message("Error", f"Airport '{code}' not found in the list.")

def CClick():
    play_loading_sound()
    if len(airports) > 0:
        schengen = sum(1 for a in airports if IsSchengenAirport(a.code))
        noschengen = len(airports) - schengen
        PlotAirports(airports)
        result_message(f"Schengen airports: {schengen}\nNon-Schengen airports: {noschengen}")
    else:
        log_message("Error", "Cannot plot. The airport list is empty. Please click 'Load Airports' first.")
        result_message("Action failed: No airports loaded")

def DClick():
    play_loading_sound()
    if len(airports) > 0:
        SaveSchengenAirports(airports, "SchengenAirports.txt")
        log_message("Save/Map", "File SchengenAirports.txt saved. Opening Map...")
        MapAirports(airports)
    else:
        log_message("Error", "Cannot save or map. The airport list is empty. Please 'Load Airports' first.")


# FUNCIONES DE LOS BOTONES (VERSIÓN 2)

def EClick():
    play_click_sound()
    clear_main_console()
    aircrafts[:] = LoadArrivals("Arrivals.txt")
    if len(aircrafts) > 0:
        for aircraft in aircrafts:
            log_message("Flight", f"{aircraft.aircraft}   {aircraft.origen}   {aircraft.time}   {aircraft.airline}")
        result_message(f"Flights loaded: {len(aircrafts)}")
    else:
        log_message("Error", "Could not load flights. Ensure 'Arrivals.txt' exists and is formatted correctly.")
        result_message("No flights loaded")

def FClick():
    play_loading_sound()
    if len(aircrafts) > 0:
        log_message("Plot", "Opening arrivals plot...")
        PlotArrivals(aircrafts)
        result_message(f"Flights loaded: {len(aircrafts)}")
    else:
        log_message("Error", "Cannot plot arrivals. No flights loaded. Please click 'Load Arrivals' first.")

def GClick():
    play_click_sound()
    clear_main_console()
    if len(aircrafts) > 0:
        SaveFlights(aircrafts, "saved_flights.txt")
        log_message("Success", "Flights saved correctly in 'saved_flights.txt'.")
        show_file("saved_flights.txt")
        result_message("Flights saved successfully")
    else:
        log_message("Error", "Cannot save flights. The flight list is empty. Please 'Load Arrivals' first.")

def HClick():
    play_loading_sound()
    if len(aircrafts) > 0:
        airlines = []
        for a in aircrafts:
            if a.airline not in airlines:
                airlines.append(a.airline)
        PlotAirlines(aircrafts)
        result_message(f"Airlines detected: {len(airlines)}")
    else:
        log_message("Error", "Cannot plot airlines. No flights loaded. Please click 'Load Arrivals' first.")

def IClick():
    play_loading_sound()
    if len(aircrafts) > 0:
        schengen = sum(1 for a in aircrafts if IsSchengenAirport(a.origen))
        non_schengen = len(aircrafts) - schengen
        log_message("Plot", "Opening Flights Type graph...")
        PlotFlightsType(aircrafts)
        result_message(f"Schengen flights: {schengen}\nNon-Schengen flights: {non_schengen}")
    else:
        log_message("Error", "Cannot plot flight types. No flights loaded. Please click 'Load Arrivals' first.")

def JClick():
    play_loading_sound()
    if len(aircrafts) > 0:
        MapFlights(aircrafts)
        log_message("Map", "Flights map generated correctly.")
        result_message("Flight routes mapped to Google Earth.")
    else:
        log_message("Error", "Cannot map flights. No flights loaded. Please click 'Load Arrivals' first.")

def KClick():
    play_click_sound()
    clear_main_console()
    if len(aircrafts) > 0:
        vuelos = LongDistanceArrivals(aircrafts)
        log_message("Long Distance", f"{len(vuelos)} long distance flights found (>2000km).")
        mensaje = "Long distance flights:\n"
        for v in vuelos:
            mensaje += f"{v.aircraft} {v.origen} {v.time} {v.airline}\n"
        result_message(mensaje)
    else:
        log_message("Error", "Cannot calculate long distances. No flights loaded. Please 'Load Arrivals' first.")


# FUNCIONES DE LOS BOTONES (VERSIÓN 3)

def LClick():
    play_click_sound()
    clear_main_console()
    airport = LoadAirportStructure("Terminals.txt")
    if airport != "":
        lebl_airport.clear()
        lebl_airport.append(airport)
        log_message("Success", "Airport structure loaded correctly.")
        show_file("Terminals.txt")
    else:
        log_message("Error", "Could not load airport structure. Ensure 'Terminals.txt' exists and is correct.")

def MClick():
    play_loading_sound()
    clear_main_console()
    if len(lebl_airport) > 0:
        occupancy = GateOccupancy(lebl_airport[0])
        occupied = 0
        free = 0
        log_message("Gate Occupancy", "Generating occupancy list:")
        for g in occupancy:
            if g[1]:
                estado = "Occupied by " + g[2]
                occupied += 1
            else:
                estado = "Free"
                free += 1
            log_message("Gate", f"{g[0]}: {estado}")
        result_message(f"Occupied gates: {occupied}\nFree gates: {free}")
        DrawOccupancyWindow()
    else:
        log_message("Error", "Cannot show occupancy. Please click 'Load Airport Structure' (Version 3) first.")

def NClick():
    play_loading_sound()
    clear_main_console()
    if len(lebl_airport) == 0:
        log_message("Error", "Missing Airport. Please click 'Load Airport Structure' (Version 3) first.")
        return
    if len(aircrafts) == 0:
        log_message("Error", "Missing Flights. Please click 'Load Arrivals' (Version 2) first.")
        return

    asignados = 0
    for a in aircrafts:
        gate = AssignGate(lebl_airport[0], a)
        if gate != -1:
            log_message("Assign Gate", f"Flight {a.aircraft} assigned to -> {gate}")
            asignados += 1

    result_message(f"Total flights successfully assigned: {asignados}")
    DrawAirportWindow()


# ==========================================
# FUNCIONES DE LOS BOTONES (VERSIÓN 4)
# ==========================================

def OClick():
    play_click_sound()
    clear_main_console()
    if len(aircrafts) == 0:
        log_message("Error", "Arrivals are missing. Please 'Load Arrivals' (Version 2) first before merging departures.")
        return

    deps = LoadDepartures("Departures.txt")
    if isinstance(deps, tuple):
        deps = deps[0]

    if len(deps) > 0:
        merged = MergeMovements(aircrafts, deps)
        if merged != -1:
            aircrafts[:] = merged
            log_message("Merge", f"Departures loaded and merged! Total flights to process: {len(aircrafts)}")
            result_message(f"Departures merged successfully.\nTotal Combined Flights: {len(aircrafts)}")
        else:
            log_message("Error", "Could not merge movements due to an internal error.")
    else:
        log_message("Error", "No departures loaded. Ensure 'Departures.txt' exists and has valid data.")

def PClick():
    play_click_sound()
    clear_main_console()
    if len(lebl_airport) == 0:
        log_message("Error", "Missing Airport. Please click 'Load Airport Structure' (Version 3) first.")
        return
    if len(aircrafts) == 0:
        log_message("Error", "Missing Flights. Please load and merge flights first.")
        return

    time_input = fraseEntry.get().strip()
    if time_input == "":
        log_message("Error", "Input box is empty. Please enter a time (e.g. 14:00) in the input box first.")
        return

    if ":" in time_input:
        unassigned = AssignGatesAtTime(lebl_airport[0], aircrafts, time_input)
        log_message("Assign Hour", f"Gates updated dynamically for {time_input}. Unassigned: {unassigned}")
        result_message(f"Dynamic Gate Assignment at {time_input}\nUnassigned flights: {unassigned}")
    else:
        log_message("Error", "Invalid time format. Please use HH:MM format (e.g. 14:00).")

def QClick():
    play_loading_sound()
    if len(lebl_airport) == 0:
        log_message("Error", "Missing Airport. Please click 'Load Airport Structure' (Version 3) first.")
        return
    if len(aircrafts) == 0:
        log_message("Error", "Missing Flights. Please load and merge flights first.")
        return

    log_message("Plot", "Simulating full day and generating occupancy plot...")
    PlotDayOccupancy(lebl_airport[0], aircrafts)
    result_message("Day occupancy plot generated successfully.")


# FUNCIONES DE LIMPIEZA (BOTONES ROJOS)

def ClearConsoleOnly():
    play_click_sound()
    clear_main_console()
    results_text.config(state=NORMAL)
    results_text.delete("1.0", END)
    results_text.config(state=DISABLED)
    fraseEntry.delete(0, END)
    log_message("System", "Window text cleared. Memory is intact.")

def ClearAllAndMemory():
    play_click_sound()
    airports.clear()
    aircrafts.clear()
    lebl_airport.clear()
    clear_main_console()
    results_text.config(state=NORMAL)
    results_text.delete("1.0", END)
    results_text.config(state=DISABLED)
    fraseEntry.delete(0, END)
    log_message("System", "WARNING: All text and data memory have been completely cleared.")


# CONFIGURACIÓN DE LA INTERFAZ GRÁFICA (GUI)

window = Tk()
window.title("Airport Management")
window.geometry("1600x1000")
window.configure(bg=BG_COLOR)

window.columnconfigure(0, weight=1, minsize=250)
window.columnconfigure(1, weight=5)
window.rowconfigure(2, weight=1)

# --- ENCABEZADO (BOTONES + TÍTULO) ---
header_frame = Frame(window, bg=BG_COLOR)
header_frame.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W, padx=10, pady=10)

red_buttons_frame = Frame(header_frame, bg=BG_COLOR)
red_buttons_frame.pack(side=LEFT, padx=(0, 20))

Button(red_buttons_frame, text="Clear Window Only", font=("Arial", 9, "bold"), bg='#ff3333', fg="white",
       command=ClearConsoleOnly, relief="raised", borderwidth=3).pack(side=LEFT, padx=5)
Button(red_buttons_frame, text="Clear Window & Memory", font=("Arial", 9, "bold"), bg='#990000', fg="white",
       command=ClearAllAndMemory, relief="raised", borderwidth=3).pack(side=LEFT, padx=5)

tituloLabel = Label(header_frame, text="Airport & Flight Management", font=("Helvetica", 22, "bold"),
                    bg=BG_COLOR, fg=TEXT_COLOR, relief="groove", borderwidth=2, padx=15, pady=8)
tituloLabel.pack(side=LEFT, fill=X, expand=True)

# --- BARRA LATERAL (BOTONES) ---
botones_frame = Frame(window, bg=BG_COLOR)
botones_frame.grid(row=1, column=0, rowspan=2, sticky=N + S + E + W, padx=10)

# Botones Versión 1 - Texto reducido y márgenes más ajustados
Label(botones_frame, text="Versión 1", font=("Arial", 10, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(2, 2), anchor=W)
Button(botones_frame, text="Load Airports", font=("Arial", 9, "bold"), bg='#46b446', fg="white", command=EntrarClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Add Airport", font=("Arial", 9, "bold"), bg='#379b37', fg="white", command=AClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Remove Airport", font=("Arial", 9, "bold"), bg='#288228', fg="white", command=BClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Plot Airports", font=("Arial", 9, "bold"), bg='#196919', fg="white", command=CClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Save & Map Airports", font=("Arial", 9, "bold"), bg='#0a500a', fg="white", command=DClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)

# Botones Versión 2 - Texto reducido y márgenes más ajustados
Label(botones_frame, text="Versión 2", font=("Arial", 10, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(8, 2), anchor=W)
Button(botones_frame, text="Load Arrivals", font=("Arial", 9, "bold"), bg='#4884d8', fg="white", command=EClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Plot Arrivals", font=("Arial", 9, "bold"), bg='#3c76c6', fg="white", command=FClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Save Flights", font=("Arial", 9, "bold"), bg='#3068b4', fg="white", command=GClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Plot Airlines", font=("Arial", 9, "bold"), bg='#245aa2', fg="white", command=HClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Plot Flights Type", font=("Arial", 9, "bold"), bg='#184c90', fg="white", command=IClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Map Flights", font=("Arial", 9, "bold"), bg='#0c3e7e', fg="white", command=JClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Long Dist. Arrivals", font=("Arial", 9, "bold"), bg='#00306c', fg="white", command=KClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)

# Botones Versión 3 - Texto reducido y márgenes más ajustados
Label(botones_frame, text="Versión 3", font=("Arial", 10, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(8, 2), anchor=W)
Button(botones_frame, text="Load Airport Structure", font=("Arial", 9, "bold"), bg='#8c50be', fg="white", command=LClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Show Gate Occupancy", font=("Arial", 9, "bold"), bg='#693796', fg="white", command=MClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Assign Gates", font=("Arial", 9, "bold"), bg='#461e6e', fg="white", command=NClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)

# Botones Versión 4 - Texto reducido y márgenes más ajustados
Label(botones_frame, text="Versión 4", font=("Arial", 10, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(8, 2), anchor=W)
Button(botones_frame, text="Load & Merge Departures", font=("Arial", 9, "bold"), bg='#e68a00', fg="white", command=OClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Assign Gates at Hour", font=("Arial", 9, "bold"), bg='#cc7a00', fg="white", command=PClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Plot Day Occupancy", font=("Arial", 9, "bold"), bg='#b36b00', fg="white", command=QClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)


# --- ÁREA PRINCIPAL DERECHA ---
entrada_frame = Frame(window, bg=BG_COLOR)
entrada_frame.grid(row=1, column=1, sticky=N + E + W, padx=10, pady=10)
Label(entrada_frame, text="Input (depends on selected action):", font=("Arial", 10, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(side=LEFT, padx=(0, 10))
fraseEntry = Entry(entrada_frame, font=("Arial", 12), width=40, bg="white", fg="black")
fraseEntry.pack(side=LEFT, fill=X, expand=True)

right_frame = Frame(window, bg=BG_COLOR)
right_frame.grid(row=2, column=1, sticky=N + S + E + W, padx=10, pady=(0, 10))
right_frame.rowconfigure(0, weight=5)
right_frame.rowconfigure(1, weight=1)
right_frame.columnconfigure(0, weight=1)

# Consola principal (Terminal)
console_frame = Frame(right_frame, bg=CONSOLE_BG, bd=2, relief="sunken")
console_frame.grid(row=0, column=0, sticky=N + S + E + W)
scrollbar = Scrollbar(console_frame)
scrollbar.pack(side=RIGHT, fill=Y)
console_text = Text(console_frame, bg=CONSOLE_BG, fg=CONSOLE_FG, font=("Consolas", 11), yscrollcommand=scrollbar.set, state=DISABLED)
console_text.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=console_text.yview)

# Consola inferior (Resultados rápidos)
results_frame = LabelFrame(right_frame, text="Results", font=("Arial", 11, "bold"), bg=BG_COLOR, fg=TEXT_COLOR, bd=2, relief="groove")
results_frame.grid(row=1, column=0, sticky=E + W, pady=(4, 0))
results_text = Text(results_frame, height=5, bg=RESULT_BG, fg=RESULT_FG, font=("Consolas", 10), state=DISABLED)
results_text.pack(fill=BOTH, expand=True, padx=5, pady=5)

# Mensaje inicial
log_message("System", "Welcome to Airport Management System. Ready to execute commands.")

# Arranca el bucle principal de la aplicación
window.mainloop()
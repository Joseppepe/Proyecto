from tkinter import *
# Importamos las funciones y clases de los módulos que has creado
from aircraft import *
from airport import *
from LEBL import *

# Variables globales para almacenar los datos en memoria mientras la app está abierta
airports = []
aircrafts = []
lebl_airport = []

# FUNCIONES AUXILIARES DE LA INTERFAZ

def log_message(title, message):
    """Escribe un mensaje en la consola virtual de estilo terminal (caja de texto grande)."""
    console_text.config(state=NORMAL)  # Habilita escritura
    console_text.insert(END, f"[{title}] {message}\n")  # Inserta el texto al final
    console_text.see(END)  # Hace scroll automático hacia abajo
    console_text.config(state=DISABLED)  # Deshabilita para que el usuario no escriba encima


def result_message(message):
    """Escribe un mensaje corto en el recuadro inferior de resultados, borrando lo anterior."""
    results_text.config(state=NORMAL)
    results_text.delete("1.0", END)  # Borra desde la línea 1, carácter 0 hasta el final
    results_text.insert(END, message)
    results_text.config(state=DISABLED)


def show_file(filename):
    """Lee un archivo de texto y muestra su contenido línea por línea en la consola virtual."""
    try:
        F = open(filename, "r")
        line = F.readline()
        log_message("File", f"Showing {filename} contents:")

        while line != "":
            log_message(filename, line.strip())
            line = F.readline()
        F.close()

    except FileNotFoundError:
        log_message("Error", f"{filename} file not found.")


# FUNCIONES DE LOS BOTONES (VERSIÓN 1)

def EntrarClick():
    """Botón 'Load Airports': Carga los aeropuertos desde Airports.txt y los muestra."""
    console_text.config(state=NORMAL)
    console_text.delete("1.0", END)  # Limpia la consola antes de cargar
    console_text.config(state=DISABLED)

    # Carga los datos usando la función de airport.py
    airports[:] = LoadAirports("Airports.txt")

    if len(airports) > 0:
        i = 0
        while i < len(airports):
            airport = airports[i]
            log_message("Airport", f"{airport.code}   {airport.lat:.4f}   {airport.lon:.4f}   {airport.schengen}")
            i += 1
        result_message(f"Loaded airports: {len(airports)}")
    else:
        result_message("No airports loaded")


def AClick():
    """Botón 'Add Airport': Lee la caja de texto (Entry) y añade un aeropuerto nuevo."""
    try:
        # Extrae los datos introducidos por el usuario separados por espacios
        datos = fraseEntry.get().split()
        code = datos[0]
        lat = float(datos[1])
        lon = float(datos[2])

        antes = len(airports)

        airport = Airport(code, lat, lon)
        SetSchengen(airport)
        AddAirport(airports, airport)

        if len(airports) > antes:
            log_message("Add", f"Airport {code} added correctly.")
        else:
            log_message("Warning", "Airport already exists.")
    except ValueError:
        log_message("Error", "Enter format: CODE LAT LON (e.g., LEBL 41 2)")
    except IndexError:
        log_message("Error", "Enter format: CODE LAT LON (e.g., LEBL 41 2)")


def BClick():
    """Botón 'Remove Airport': Lee el código de la caja de texto y lo elimina."""
    antes = len(airports)
    # Extrae solo la primera palabra (el código) introducida por el usuario
    code = fraseEntry.get().split()[0] if fraseEntry.get() else ""
    RemoveAirport(airports, code)

    if len(airports) < antes:
        log_message("Remove", f"Airport {code} removed correctly.")
    else:
        log_message("Warning", "Airport not found.")


def CClick():
    """Botón 'Plot Airports': Cuenta y muestra la gráfica de Schengen vs No Schengen."""
    if len(airports) > 0:
        schengen = 0
        i = 0
        while i < len(airports):
            if IsSchengenAirport(airports[i].code):
                schengen += 1
            i += 1
        noschengen = len(airports) - schengen

        PlotAirports(airports)  # Función de airport.py
        result_message(f"Schengen airports: {schengen}\nNon-Schengen airports: {noschengen}")
    else:
        result_message("No airports loaded")


def DClick():
    """Botón 'Save & Map Airports': Guarda los Schengen y genera el mapa KML."""
    if len(airports) > 0:
        SaveSchengenAirports(airports, "SchengenAirports.txt")
        log_message("Save/Map", "File SchengenAirports.txt saved. Opening Map...")
        MapAirports(airports)  # Función de airport.py
    else:
        log_message("Warning", "No airports to save or map.")


# FUNCIONES DE LOS BOTONES (VERSIÓN 2)

def EClick():
    """Botón 'Load Arrivals': Carga los vuelos desde Arrivals.txt."""
    aircrafts[:] = LoadArrivals("Arrivals.txt")

    console_text.config(state=NORMAL)
    console_text.delete("1.0", END)
    console_text.config(state=DISABLED)

    if len(aircrafts) > 0:
        i = 0
        while i < len(aircrafts):
            aircraft = aircrafts[i]
            log_message("Flight", f"{aircraft.aircraft}   {aircraft.origen}   {aircraft.time}   {aircraft.airline}")
            i += 1
        result_message(f"Flights loaded: {len(aircrafts)}")
    else:
        result_message("No flights loaded")


def FClick():
    """Botón 'Plot Arrivals': Muestra el gráfico de aterrizajes por hora."""
    if len(aircrafts) > 0:
        log_message("Plot", "Opening arrivals plot...")
        PlotArrivals(aircrafts)
        result_message(f"Flights loaded: {len(aircrafts)}")
    else:
        result_message("No aircraft loaded")


def GClick():
    """Botón 'Save Flights': Guarda los vuelos en un archivo nuevo."""
    if len(aircrafts) > 0:
        SaveFlights(aircrafts, "saved_flights.txt")

        console_text.config(state=NORMAL)
        console_text.delete("1.0", END)
        console_text.config(state=DISABLED)

        log_message("Save", "Flights saved correctly in saved_flights.txt.")
        show_file("saved_flights.txt")
        result_message("Flights saved successfully")
    else:
        log_message("Warning", "No aircraft to save.")


def HClick():
    """Botón 'Plot Airlines': Muestra la gráfica de vuelos por aerolínea."""
    if len(aircrafts) > 0:
        airlines = []
        i = 0
        while i < len(aircrafts):
            airline = aircrafts[i].airline
            encontrado = False
            j = 0
            while j < len(airlines) and not encontrado:
                if airlines[j] == airline:
                    encontrado = True
                else:
                    j += 1
            if not encontrado:
                airlines.append(airline)
            i += 1

        PlotAirlines(aircrafts)
        result_message(f"Airlines detected: {len(airlines)}")
    else:
        result_message("No aircraft loaded")


def IClick():
    """Botón 'Plot Flights Type': Muestra gráfica de vuelos origen Schengen vs No Schengen."""
    if len(aircrafts) > 0:
        schengen = 0
        i = 0
        while i < len(aircrafts):
            if IsSchengenAirport(aircrafts[i].origen):
                schengen += 1
            i += 1
        non_schengen = len(aircrafts) - schengen

        log_message("Plot", "Opening Flights Type graph...")
        PlotFlightsType(aircrafts)
        result_message(f"Schengen flights: {schengen}\nNon-Schengen flights: {non_schengen}")
    else:
        result_message("No aircraft loaded")


def JClick():
    """Botón 'Map Flights': Genera el KML de las rutas de vuelo en Google Earth."""
    if len(aircrafts) > 0:
        MapFlights(aircrafts)
        log_message("Map", "Flights map generated correctly.")
        result_message("Flight routes mapped to Google Earth.")
    else:
        log_message("Warning", "No aircraft loaded.")


def KClick():
    """Botón 'Long Dist. Arrivals': Calcula qué vuelos vienen de más de 2000km."""
    if len(aircrafts) > 0:
        vuelos = LongDistanceArrivals(aircrafts)
        log_message("Long Distance", f"{len(vuelos)} long distance flights found.")
        # Muestra en consola cuántos vuelos de larga distancia se han encontrado
        mensaje = "Long distance flights:\n"# Crea el texto inicial donde se guardará la información de los vuelos


        i = 0
        while i < len(vuelos):# Recorre todos los vuelos encontrados
            mensaje = mensaje + vuelos[i].aircraft + " " + vuelos[i].origen + " " + vuelos[i].time + " " + vuelos[i].airline + "\n"
            # Añade los datos del vuelo al mensaje
            i += 1

        result_message(mensaje)
    else:
        log_message("Warning", "Load aircraft first.")


# FUNCIONES DE LOS BOTONES (VERSIÓN 3)

def LClick():
    """Botón 'Load Airport Structure': Carga el árbol de terminales, áreas y puertas de LEBL."""
    airport = LoadAirportStructure("Terminals.txt")  # Nota: Asumiendo que el archivo es LEBL.txt según el enunciado

    if airport != "":
        lebl_airport.clear()
        lebl_airport.append(airport)
        log_message("Load Airport", " Airport structure loaded correctly.")
        # Opcional: mostrar archivo (si existe)
        show_file("Terminals.txt")
    else:
        log_message("Error", "Could not load airport structure")


def MClick():
    """Botón 'Show Gate Occupancy': Lista todas las puertas y su estado (libre/ocupada)."""
    if len(lebl_airport) > 0:
        occupancy = GateOccupancy(lebl_airport[0])

        occupied = 0
        free = 0

        log_message("Gate Occupancy", "Generating occupancy list:")

        i = 0
        while i < len(occupancy):
            g = occupancy[i]
            if g[1]:  # Si occupied es True
                estado = "Occupied by " + g[2]
                occupied += 1
            else:
                estado = "Free"
                free += 1

            log_message("Gate", g[0] + ": " + estado)
            i += 1
        result_message("Occupied gates: " + str(occupied) + "\nFree gates: " + str(free))
    else:
        log_message("Warning", "Load the airport structure first.")


def NClick():
    """Botón 'Assign Gates': Asigna puertas a los vuelos cargados."""
    # CORRECCIÓN: len(lebl_airport) en lugar de (lebl_airport)
    if len(lebl_airport) == 0:
        log_message("Warning", "Load airport structure first.")
        return

    if len(aircrafts) == 0:
        log_message("Warning", "Load flights first.")
        return

    i = 0
    asignados = 0

    while i < len(aircrafts):
        gate = AssignGate(lebl_airport[0], aircrafts[i])

        if gate != -1:
            log_message("Assign Gate", f"{aircrafts[i].aircraft} -> {gate}")
            asignados += 1
        i += 1

    result_message(f"Flights assigned: {asignados}")


# FUNCIONES DE LIMPIEZA

def ClearConsole():
    """Limpia la pantalla de texto principal y la de resultados."""
    console_text.config(state=NORMAL)
    console_text.delete("1.0", END)
    console_text.config(state=DISABLED)

    results_text.config(state=NORMAL)
    results_text.delete("1.0", END)
    results_text.config(state=DISABLED)
    fraseEntry.delete(0, END)


def ClearAll():
    """Limpia los datos en memoria y todas las pantallas de texto."""
    airports.clear()
    aircrafts.clear()
    lebl_airport.clear()

    fraseEntry.delete(0, END)

    ClearConsole()  # Reutiliza la función anterior para ahorrar código
    log_message("System", "All data and screens cleared.")


# CONFIGURACIÓN DE LA INTERFAZ GRÁFICA (GUI)

window = Tk()
window.title("Airport Management")
window.geometry("1600x1000")
window.configure(bg='#333333')

# Configuración del grid principal (para que sea responsivo)
window.columnconfigure(0, weight=1, minsize=250)  # Columna de botones
window.columnconfigure(1, weight=5)  # Columna de texto
window.rowconfigure(2, weight=1)

# Etiqueta de Título
tituloLabel = Label(window, text="Airport & Flight Management", font=("Helvetica", 22, "bold"), bg="#333333",
                    fg="white", relief="groove", borderwidth=4, padx=10, pady=10)
tituloLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

# Marco lateral izquierdo (Botones)
botones_frame = Frame(window, bg='#333333')
botones_frame.grid(row=1, column=0, rowspan=2, sticky=N + S + E + W, padx=10)

# Botones Versión 1
Label(botones_frame, text="Versión 1", font=("Arial", 12, "bold"), bg="#333333", fg="white").pack(pady=(10, 5),
                                                                                                  anchor=W)
Button(botones_frame, text="Load Airports", font=("Arial", 9, "bold"), bg='#46b446', fg="white", command=EntrarClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Add Airport", font=("Arial", 9, "bold"), bg='#379b37', fg="white", command=AClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Remove Airport", font=("Arial", 9, "bold"), bg='#288228', fg="white", command=BClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Plot Airports", font=("Arial", 9, "bold"), bg='#196919', fg="white", command=CClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Save & Map Airports", font=("Arial", 9, "bold"), bg='#0a500a', fg="white", command=DClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)

# Botones Versión 2
Label(botones_frame, text="Versión 2", font=("Arial", 12, "bold"), bg="#333333", fg="white").pack(pady=(15, 5),
                                                                                                  anchor=W)
Button(botones_frame, text="Load Arrivals", font=("Arial", 9, "bold"), bg='#4884d8', fg="white", command=EClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Plot Arrivals", font=("Arial", 9, "bold"), bg='#3c76c6', fg="white", command=FClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Save Flights", font=("Arial", 9, "bold"), bg='#3068b4', fg="white", command=GClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Plot Airlines", font=("Arial", 9, "bold"), bg='#245aa2', fg="white", command=HClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Plot Flights Type", font=("Arial", 9, "bold"), bg='#184c90', fg="white", command=IClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Map Flights", font=("Arial", 9, "bold"), bg='#0c3e7e', fg="white", command=JClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Long Dist. Arrivals", font=("Arial", 9, "bold"), bg='#00306c', fg="white", command=KClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)

# Botones Versión 3
Label(botones_frame, text="Versión 3", font=("Arial", 12, "bold"), bg="#333333", fg="white").pack(pady=(15, 5),
                                                                                                  anchor=W)
Button(botones_frame, text="Load Airport Structure", font=("Arial", 9, "bold"), bg='#8c50be', fg="white",
       command=LClick, relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Show Gate Occupancy", font=("Arial", 9, "bold"), bg='#693796', fg="white", command=MClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Assign Gates", font=("Arial", 9, "bold"), bg='#461e6e', fg="white", command=NClick,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)

# Botones Otros (Limpieza)
Label(botones_frame, text="Other Functions", font=("Arial", 12, "bold"), bg="#333333", fg="white").pack(pady=(15, 5),
                                                                                                        anchor=W)
Button(botones_frame, text="Clear Console", font=("Arial", 9, "bold"), bg='#c82828', fg="white", command=ClearConsole,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)
Button(botones_frame, text="Clear All", font=("Arial", 9, "bold"), bg='#821919', fg="white", command=ClearAll,
       relief="raised", borderwidth=3).pack(fill=X, pady=2)

# Marco superior derecho (Entrada de texto)
entrada_frame = Frame(window, bg='#333333')
entrada_frame.grid(row=1, column=1, sticky=N + E + W, padx=10, pady=10)
Label(entrada_frame, text="Input (depends on selected action):", font=("Arial", 10, "bold"), bg="#333333",
      fg="white").pack(side=LEFT, padx=(0, 10))
fraseEntry = Entry(entrada_frame, font=("Arial", 12), width=40)
fraseEntry.pack(side=LEFT, fill=X, expand=True)

# Marco inferior derecho (Consolas)
right_frame = Frame(window, bg="#333333")
right_frame.grid(row=2, column=1, sticky=N + S + E + W, padx=10, pady=(0, 10))
right_frame.rowconfigure(0, weight=5)  # Más espacio para la terminal principal
right_frame.rowconfigure(1, weight=1)  # Menos espacio para los resultados rápidos
right_frame.columnconfigure(0, weight=1)

# Consola principal (Terminal)
console_frame = Frame(right_frame, bg='#333333', bd=2, relief="sunken")
console_frame.grid(row=0, column=0, sticky=N + S + E + W)
scrollbar = Scrollbar(console_frame)
scrollbar.pack(side=RIGHT, fill=Y)
console_text = Text(console_frame, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 11), yscrollcommand=scrollbar.set,
                    state=DISABLED)
console_text.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=console_text.yview)

# Consola inferior (Resultados rápidos)
results_frame = LabelFrame(right_frame, text="Results", font=("Arial", 11, "bold"), bg="#333333", fg="white", bd=2,
                           relief="groove")
results_frame.grid(row=1, column=0, sticky=E + W, pady=(4, 0))
results_text = Text(results_frame, height=5, bg="#111111", fg="cyan", font=("Consolas", 10), state=DISABLED)
results_text.pack(fill=BOTH, expand=True, padx=5, pady=5)

# Mensaje inicial
log_message("System", "Welcome to Airport Management System. Ready to execute commands.")

# Arranca el bucle principal de la aplicación
window.mainloop()
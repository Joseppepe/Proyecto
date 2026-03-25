import matplotlib.pyplot as plt
class Airport:

    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.schengen = False


def IsSchengenAirport(code):

       prefijos= ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
               'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE','ES', 'LS']
       i=0
       encontrado=False
       prefijo=airport.code[:2]

       while i < len(prefijos) and not encontrado:
          if prefijos[i]==prefijo:
             encontrado = True
          else:
             i=i+1
             encontrado=False

       airport.schengen = encontrado

def SetSchengen(airport):IsSchengenAirport(airport)

def PrintAirport(airport):

    print(f"Code: {airport.code}, Lat: {airport.lat:.6f}, Lon: {airport.lon:.6f}, Schengen: {airport.schengen}")


airport = Airport ("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport (airport)

def LoadAirports(Filename):
    airports=[]
    try:
        F= open(Filename, "r")
        lines= F.readlines()
        F.close()
        i=1

        while i<len(lines):

            parts=lines[i].strip().split()
            code=parts[0]
            lat=ConvertCoord(parts[1])
            lon=ConvertCoord(parts[2])

            airport=Airport(code, lat, lon)
            airports.append(airport)


            i=i+1



    except FileNotFoundError:
        airport=[]

    return airports

def SaveSchengenAirports(airports, filename):

    if len(airports) == 0:
        return

    F = open(filename, "w")

    F.write("CODE LAT LON\n")

    i = 0
    while i < len(airports):

        if airports[i].schengen==True:
            F.write(f"{airports[i].code} {airports[i].lat} {airports[i].lon}\n")

        i = i + 1

    F.close()

def AddAirport(airports, airport):
    i = 0
    encontrado = False

    while i < len(airports) and not encontrado:
        if airports[i].code == airport.code:
            encontrado = True
        else:
            i=i+1

    if not encontrado:
        airports.append(airport)
def RemoveAirport(airports, code):

    i = 0
    encontrado = False

    while i < len(airports) and not encontrado:
        if airports[i].code == code:
            airports.pop(i)
            encontrado = True
        else:
            i = i + 1

def ConvertCoord(coord):
     direccion=coord[0]
     degrees = int(coord[1:3])
     minutes=int(coord[3:5])
     seconds=int(coord[5:])

     decimal=degrees+minutes/60+seconds/3600

     if direccion =='S'or direccion =='W':
         decimal= -decimal

def PlotAirports(airports):

    schengen = sum(1 for a in airports if a.schengen)
    noschengen = len(airports) - schengen

    fig,ax = plt.subplots()

    ax.bar(['Aeropuertos'], [schengen], label='Schengen')
    ax.bar(['Aeropuertos'], [noschengen], bottom=[schengen], label='No Schengen')

    ax.set_ylabel('Cantidad')
    ax.set_title('Schengen airports')
    ax.legend()

    plt.show()




import matplotlib.pyplot as plt
class Airport:

    def __init__(self, code, lat, lon):
        self.code = code
        self.lat = lat
        self.lon = lon
        self.schengen = False


def IsSchengenAirport(code):
       if code=="":
           return False

       prefijos= ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
               'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE','ES', 'LS']
       i=0
       encontrado=False
       prefijo=code[:2]

       while i < len(prefijos) and not encontrado:
          if prefijos[i]==prefijo:
             encontrado = True
          else:
             i=i+1
             encontrado=False

       return encontrado

def SetSchengen(airport):
    airport.schengen=IsSchengenAirport(airport.code)

def PrintAirport(airport):

    print(f"Code: {airport.code}, Lat: {airport.lat:.6f}, Lon: {airport.lon:.6f}, Schengen: {airport.schengen}")


def LoadAirports(Filename):
    airports=[]
    try:
        F= open(Filename, "r")

        F.readline()
        line= F.readline()


        i=1

        while line!="":

            parts=line.split()
            code=parts[0]
            lat=ConvertCoord(parts[1])
            lon=ConvertCoord(parts[2])

            airport=Airport(code, lat, lon)
            SetSchengen(airport)
            airports.append(airport)

            line= F.readline()

        F.close()



    except FileNotFoundError:
        airports =[]
    return airports


def SaveSchengenAirports(airports, filename):

    if len(airports) == 0:
        return -1

    F = open(filename, "w")

    F.write("CODE LAT LON\n")

    i = 0
    while i < len(airports):

        if airports[i].schengen==True:
            F.write(f"{airports[i].code} {airports[i].lat} {airports[i].lon}\n")

        i = i + 1

    F.close()


def AddAirport(airports, airport):
    if airport.code=="":
        return
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
            airports[:]=airports[:i]+airports[i+1:]
            encontrado = True
        else:
            i = i + 1
    if not encontrado:
        return -1

def ConvertCoord(coord):
     direccion=coord[0]
     if direccion == "N" or direccion == "S":
         degrees = int(coord[1:3])
         minutes=int(coord[3:5])
         seconds=int(coord[5:])
     else:
         degrees = int(coord[1:4])
         minutes = int(coord[4:6])
         seconds = int(coord[6:8])

     decimal=degrees+minutes/60+seconds/3600

     if direccion =='S' or direccion =='W':
         decimal= -decimal

     return decimal

def PlotAirports(airports):
    i=0
    schengen=0
    while i < len(airports):
        if airports[i].schengen==True:
            schengen=schengen+1
        i=i+1
    noschengen = len(airports) - schengen

    fig,ax = plt.subplots()

    ax.bar(['Aeropuertos'], [schengen], label='Schengen')
    ax.bar(['Aeropuertos'], [noschengen], bottom=[schengen], label='No Schengen')

    ax.set_ylabel('Cantidad')
    ax.set_title('Schengen airports')
    ax.legend()

    plt.show()

def MapAirports(airports):

    try:
         F=open("airports.kml", "w")

         F.write('<?xml version="1.0" encoding="UTF-8"?>\n')
         F.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
         F.write('<Document>\n')

         F.write('<Style id="schengen">\n')
         F.write('<IconStyle>\n')
         F.write('<color>ff00ff00</color>\n')
         F.write('</IconStyle>\n')
         F.write('</Style>\n')

         F.write('<Style id="nonschengen">\n')
         F.write('<IconStyle>\n')
         F.write('<color>ff0000ff</color>\n')
         F.write('</IconStyle>\n')
         F.write('</Style>\n')

         i=0
         while i<len(airports):

            airport = airports[i]
            if airport.schengen:
                style = "#schengen"
            else:
                style = "#nonschengen"

            if airport.code!="":
                F.write("<Placemark>\n")
                F.write(f"<name>{airport.code}</name>\n")
                F.write(f"<styleUrl>{style}</styleUrl>\n")
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
    import os
    os.startfile("airports.kml")













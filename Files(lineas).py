
try:
    in=open("personas.txt","r")
    out=open("mayores.txt","w")
    linea=in.readline()
    in.close()
    i=0
    while i<len(linea):
         linea=lineas[i]
         trozos=linea.split(" ")
         edad=int(trozos[1])
         if edad>=18:
             out.write(linea)
         i=i+1
    out.close()
except FileNotFoundError:
    print("No hay ficheros")
except ValueError:
    print("Datos incorrectos")
except IndexError:
    print("Datos incorrectos")



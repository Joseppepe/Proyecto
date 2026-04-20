try:
    in=open("personas.txt","r")
    out=open("mayores.txt","w")
    linea=in.readline()

    while linea!="":
         trozos=linea.split(" ")
         edad=int(trozos[1])
         if edad>=18:
             out.write(linea)
         linea=in.readline()
    in.close()
    out.close()
except FileNotFoundError:
    print("No hay ficheros")
except ValueError:
    print("Datos incorrectos")
except IndexError:
    print("Datos incorrectos")

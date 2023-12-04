import pandas as pd

def GeneradorPuntos(start, end, num_lineas, n):
    #La función depende del primer punto del rectángulo y del último, es decir, la arista superior izquierda y la inferior derecha.
    #La cantidad de lineas que se quiere en el rectángulo (que se traduce en el la distancia en micras entre línea y línea)
    #y n La cantidad de zurcos
    
    points = []
    paso = (end[0] - start[0]) / (num_lineas - 1) #Cuanto avanza cada vez que termina una línea del rectángulo
    y = True

    for s in range(n): 
        x_inicio = 0
        #Según en que zurco vayamos será el punto x en el que inicie. Cada zurco más la separación es de 400micras. 
        if s < 8:
            x_inicio = s * 400
        elif 8 <= s <= 12:
            x_inicio = (s - 1) * 400 + 710 + 70 #El primer defecto
        elif 20 >= s >= 12:
            x_inicio = (s - 2) * 400 + 1420 + 140 #El segundo defecto
        else:
            x_inicio = s * 400 + 1420

        for i in range(num_lineas): #Formato de guardado del csv para que el láser recorra en S
            x = start[0] + i * paso + x_inicio
            if i == num_lineas-1:
                points.append((x, end[1], 0.0)) 
                points.append((x, start[1], 0.0))
                points.append((x, start[1], 1.0))
                y = not(y)
            elif i == 0: 
                points.append((x, start[1], 1.0))
                points.append((x, start[1], 0.0))
                points.append((x, end[1], 0.0))
                y = not(y)
            else: 
                if y:
                    points.append((x, start[1], 0.0))
                    points.append((x, end[1], 0.0))
                else:
                    points.append((x, end[1], 0.0))
                    points.append((x, start[1], 0.0))
                y = not(y)
    return points

inicio = (1, 1.0)
final = (71, 2000.0)
num_lineas = 100

points = GeneradorPuntos(inicio, final, num_lineas, 21)

df = pd.DataFrame(points, columns=None)

df[0] = df[0]*1e-3
df[1] = df[1]*1e-3

df.to_csv("CristalMagnonico.csv", float_format="%.5e", header = False, index=False)
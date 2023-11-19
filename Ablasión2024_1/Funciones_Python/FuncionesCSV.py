#En este archivo se encuentras funciones para poder administrar mejor el archivo CSV. 

import pandas as pd
import csv

def F1(archivo, salida): #Función que crea intervalos. 
    
    with open(archivo, "r") as csvfile:
        
        dic = csv.DictReader(csvfile) #Definimos que las columnas del csv sea un diccionario.
        sorted_data = sorted(dic, key=lambda ren: (ren['Y'], float(ren['X']))) #Aquí decimos como queremos ordenas la información

    #variables para definir los intervalos
    intervalos = []
    intervalo_actual = None

    for ren in sorted_data: #Analizar renglón a renglón.
    
        #Definimos las variables del CSV
        x = float(ren['X']) 
        y = ren['Y']
        color = int(ren['Color'])

        #La estructura siguiente es para encontrar el máximo y minimo de x. 
        if intervalo_actual is None:
            intervalo_actual = {'xmin': x, 'xmax': x, 'y': y, 'color': color} 
            
        elif intervalo_actual['color'] != color or intervalo_actual['y'] != y:
            intervalos.append(intervalo_actual)
            intervalo_actual = {'xmin': x, 'xmax': x, 'y': y, 'color': color}
        else:
            intervalo_actual['xmax'] = x

    #Esto es para que no tengamos problema con el primer y último intervalo. 
    if intervalo_actual is not None:
        intervalos.append(intervalo_actual)

    #Para escribir el nuevo csv
    with open(salida, "w", newline='') as csvfile:
        columnas = ['xmin', 'xmax', 'color', 'y']
        writer = csv.DictWriter(csvfile, fieldnames=columnas)
        writer.writeheader()
        for intervalo in intervalos:
            writer.writerow(intervalo)
            
    return salida
            
def F2(archivo, salida1, salida2): #Función para acomodar max y mins
       
    original = pd.read_csv(archivo)
    original.columns = original.columns.str.strip()

    min = original[['xmin', 'y', 'color']]
    min.to_csv(salida1, index=False)

    max = original[['xmax', 'y', 'color']]
    max.to_csv(salida2, index=False)
    
    return salida1, salida2
            
def F3(archivo1, archivo2, salida): #Función para acomodar max y min
    
    with open(archivo1, 'r') as file1, open(archivo2, 'r') as file2, open(salida, 'w', newline='') as outfile:
        
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)
        writer = csv.writer(outfile)
        
        #Saltar los nombres de la columna
        next(reader1)  
        next(reader2) 

        writer.writerow(['X', 'Y', 'Color'])  #Nuevos nombres para las columnas

        for ren1, ren2 in zip(reader1, reader2):
            writer.writerow(ren1)
            writer.writerow(ren2)
            
    return salida
            
def F4(namecsv, finalcsv): #Función para dar la forma correcta al csv para que funcione con LabVIER
    
    Not = lambda x: 1 if x == 0 else 0

    df = pd.read_csv(namecsv)

    datos = []

    for i in range(0, len(df["X"])):
     
        x, y, binary_value = df["X"][i], df["Y"][i], df["Color"][i]
        
        if 0<i<len(df["Color"])-1: 
            
            x2, y2, binary2 = df["X"][i+1], df["Y"][i+1], df["Color"][i+1]
            
        if i == 0 or x == 1:
            
            if binary_value == 0:
        
                datos.append([x, y, Not(binary_value)])
                datos.append([x, y, binary_value])
                
            else:
                datos.append([x, y, binary_value])
                datos.append([x, y, binary_value])
        
        elif i == len(df["Color"]) - 1 or y != y2:
        
            if binary_value == 0:
            
                datos.append([x, y, binary_value])
                datos.append([x, y, Not(binary_value)])
            
            else:
            
                datos.append([x, y, binary_value])
                datos.append([x, y, binary_value])
    
        else:
      
            if binary_value != binary2 and y == y2:     
                if binary_value == 1: 
                    datos.append([x, y, binary_value])
                    datos.append([x2, y, binary_value])
                    datos.append([x2, y, binary2])
                else: 
                    datos.append([x, y, binary_value])
                    datos.append([x, y, Not(binary_value)])
                    
        
    df2 = pd.DataFrame(datos, columns=df.columns)
    df2 = df2.sort_values(by=['Y', 'X'])
    df2 = df2.reindex(columns=['Y','X', 'Color'])
    
    
    df2.to_csv(finalcsv, index=False)
    

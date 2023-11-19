import tkinter as tk
import pandas as pd
import csv, os, sys
from PIL import Image, ImageDraw
from FuncionesCSV import F1, F2, F3, F4

class VentanaDibujo:
    
    #Variables para que comience el programa. 
    def __init__(self, root):
        
        self.root = root
        
        self.white = "#F9F8F8"
        self.gray = "#CDD3CE"
        self.darkgreen = "#003844"
        self.green = "#006C67"
        self.red = "#A30B37"
        
        #Título de la ventana  
        self.root.title("Dibujo a CSV")
        self.root.configure(bg=self.gray)

        #Variables de dibujo
        self.celda = celdatam #Tamaño de la celda
        self.ancho = ancho #Ancho de la ventana
        self.altura = alto #Alto de la ventana

        self.canvas = tk.Canvas(self.root, bg=self.white, width=self.ancho, height=self.altura) #Color del fondo de la ventana
        self.canvas.pack(pady=20) #Distancia entre botones
        
        guardar_frame = tk.Frame(self.root)
        guardar_frame.pack(side="left", padx=20, pady=10)

        self.guardar_button = tk.Button(guardar_frame, text="Guardar CSV", command=self.guardado, bg=self.green, fg=self.white, width=20, height=4)
        self.guardar_button.pack(side="top")

        buttons_frame = tk.Frame(self.root, bg=self.gray)
        buttons_frame.pack(side="right", padx=20, pady=10)

        buttons_frame2 = tk.Frame(buttons_frame, bg=self.gray)
        buttons_frame2.pack(side="top", padx=20, pady=10)
        
        self.erase_button = tk.Button(buttons_frame2, text="Goma Off", command=self.toggle_eraser, bg=self.red, fg=self.white, width=17, height=2)
        self.erase_button.pack(side="right")
        
        self.erase_all = tk.Button(buttons_frame2, text="Borrar todo", command=self.erase_cells, bg=self.red, fg=self.white, width=17, height=2)
        self.erase_all.pack(side="right")

        self.shape_button = tk.Button(buttons_frame2, text="Draw Shapes", command=self.toggle_shape_mode, bg=self.red, fg=self.white, width=17, height=2)
        self.shape_button.pack(side="right")
        
        self.shapes_frame = tk.Frame(buttons_frame, bg=self.gray)
        self.shapes_frame.pack(side="bottom", padx=20, pady=5)

        self.image = Image.new('RGB', (self.ancho, self.altura), self.white) #Tamaño del área de dibujo y color
        self.draw = ImageDraw.Draw(self.image) #Sobre donde se dibujará
        
        self.draw_grid() #Hacer cuadrícula
        self.canvas.bind("<Button-1>", self.celda_pintada) #Dar un click pinta
        self.canvas.bind("<B1-Motion>", self.celda_pintada) #Dar un click y arrastrar el mouse también pinta

        self.d = 1e-3
        
        self.i = False
        self.erase_mode = False
        self.shape_mode = True
        self.shape_start = None
        self.draw_mode = "rectangle" 

    def toggle_eraser(self):
        self.erase_mode = not self.erase_mode  # Toggle erase mode
        button_text = "Eraser On" if self.erase_mode else "Eraser Off"
        button_bg = self.green if self.erase_mode else self.red
        button_fg = self.white if self.erase_mode else self.white
        self.erase_button.config(text=button_text, bg=button_bg, fg=button_fg)

    def toggle_shape_mode(self):
        self.shape_mode = not self.shape_mode
        self.shape_button.config(text="Draw Shapes On" if self.shape_mode else "Draw Shapes Off", bg=self.green if self.shape_mode else self.red)
        self.shape_start = None  # Reset the starting point when toggling shape mode
        if self.shape_mode:
            self.rectangle_button = tk.Button(self.shapes_frame, text="Rectangle Mode", command=lambda: self.set_draw_mode("rectangle"), bg=self.green, fg=self.white, width=15, height=2)
            self.rectangle_button.pack(side="right")
            self.oval_button = tk.Button(self.shapes_frame, text="Oval Mode", command=lambda: self.set_draw_mode("oval"), bg=self.green, fg=self.white, width=15, height=2)
            self.oval_button.pack(side="right")
            self.i = True
        elif self.i:
            self.rectangle_button.destroy()
            self.oval_button.destroy()
        
    def guardado(self):
        
        filename = nombrecsv #Nombre de la figura
    
        with open(filename, 'w', newline='') as file:
            
            writer = csv.writer(file) 
            writer.writerow(["X", "Y", "Color"]) #Nombres de las columnas en el csv
            
            for y in range(0, self.altura, self.celda): 
                for x in range(0, self.ancho, self.celda):

                    centro_x = x + self.celda // 2 #Para movernos al centro de la celda
                    centro_y = y + self.celda // 2
                
                    pixel_color = self.image.getpixel((centro_x, centro_y))
                
                    negro = 0 if pixel_color == (0, 0, 0) else 1 #Si esta pintada asignamos 1 al cvs o 0 si no
                    
                    celda_ren = x // self.celda #Indice del renglón
                    celda_col = y // self.celda #Indice de la columna
                
                    writer.writerow([celda_col+1, celda_ren+1, negro])
        
        x,y = F2(F1(nombrecsv,nombrecsv), "min.csv", "max.csv")   

        F4(F3(x, y, nombrecsv),nombrecsv)
        
        os.remove("min.csv")
        os.remove("max.csv")
        
        df = pd.read_csv(nombrecsv)

        df['X'] = df['X'] * self.d
        df['Y'] = df['Y'] * self.d
        df['Color'] = df['Color'] * 1e0

        df.to_csv(nombrecsv, float_format="%.5e", header = False, index=False)
        
        self.root.destroy()
                     
    def draw_grid(self):
        
        for i in range(0, self.ancho, self.celda):  # Lineas verticales
            self.canvas.create_line(i, 0, i, self.altura, fill=self.gray)
            
        for i in range(0, self.altura, self.celda):  # Lineas horizontales
            self.canvas.create_line(0, i, self.ancho, i, fill=self.gray)
            
    def set_draw_mode(self, mode):
        self.draw_mode = mode
        self.rectangle_button.config(bg=self.darkgreen, fg=self.white)
        self.oval_button.config(bg=self.darkgreen, fg=self.white)
        if mode == "rectangle":
            self.rectangle_button.config(bg=self.green, fg=self.white)
        elif mode == "oval":
            self.oval_button.config(bg=self.green, fg=self.white)        
            
    def celda_pintada(self, event): #Pintar toda la celda y no solo un pixel
        
        col = event.x // self.celda
        ren = event.y // self.celda

        x1 = col * self.celda
        y1 = ren * self.celda
        x2 = x1 + self.celda
        y2 = y1 + self.celda

        if self.erase_mode:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.white, outline=self.gray)
            self.draw.rectangle([x1, y1, x2, y2], fill=self.white)
        elif self.shape_mode:
            if self.shape_start is None:
                self.shape_start = (x1, y1)
            else:
                if self.draw_mode == "rectangle":
                    self.canvas.create_rectangle(self.shape_start[0], self.shape_start[1], x2, y2, fill="black", outline=self.gray)
                    self.draw.rectangle([self.shape_start[0], self.shape_start[1], x2, y2], fill="black")
                elif self.draw_mode == "oval":
                    self.canvas.create_oval(self.shape_start[0], self.shape_start[1], x2, y2, fill="black", outline=self.gray)
                    self.draw.ellipse([self.shape_start[0], self.shape_start[1], x2, y2], fill="black")
                self.shape_start = None
        
    def erase_cells(self):
        for y in range(0, self.altura, self.celda):
            for x in range(0, self.ancho, self.celda):
                x1 = x
                y1 = y
                x2 = x1 + self.celda
                y2 = y1 + self.celda

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.white, outline=self.gray)
                self.draw.rectangle([x1, y1, x2, y2], fill=self.white)

                     
if __name__ == "__main__":

    #dpi = root.winfo_fpixels('1i') #Determina automáticamente la cantidad de dpis

    ancho = int(sys.argv[1])
    alto = int(sys.argv[2])
    celdatam = int(sys.argv[3])
    nombrecsv = str(sys.argv[4]) + '.csv'

    #ancho = micras_a_pixel(ancho, dpi)
    #alto = micras_a_pixel(alto, dpi)
    
    root = tk.Tk()
    app = VentanaDibujo(root)
    
    root.mainloop()

#pip install opencv-python opencv-python-headless numpy pillow

import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

class MeasureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medición de Objetos")
        
        # Configurar la ventana de la GUI
        self.video_frame = Label(root)
        self.video_frame.pack()
        
        # Iniciar la captura de video
        self.cap = cv2.VideoCapture(0)
        self.update_frame()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        # Convertir el frame a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 50, 100)
        
        # Encontrar los contornos
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Tomar el contorno más grande
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 100:  # Umbral de área mínima para considerar el objeto
                # Obtener el cuadro delimitador
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Mostrar dimensiones
                cv2.putText(frame, f"W: {w}px H: {h}px", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Convertir el frame a formato PIL para Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_frame.imgtk = imgtk
        self.video_frame.configure(image=imgtk)
        
        self.root.after(10, self.update_frame)
    
    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = MeasureApp(root)
    root.mainloop()

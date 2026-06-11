import tkinter as tk
import random

# GLOBAL CONFIGURATIONS
ANCHO = 800
ALTO = 600
VELOCIDAD_JUGADOR = 20
VELOCIDAD_BALA = -12
VELOCIDAD_ENEMIGO = 3
BAJADA_ENEMIGO = 15

class SpaceInvaders:
    '''This is a clone of the classic arcade game Space Invaders, programmed in Python using the Tkinter graphics library'''
    def __init__(self, root):
        self.root = root
        self.root.title("Space Invaders-Project of RmC")
        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#0d0d1a")
        self.canvas.pack()
        self.botones_interfaz = []
        self.root.bind("<Left>", self.mover_izquierda)
        self.root.bind("<Right>", self.mover_derecha)
        self.root.bind("<space>", self.disparar)
        self.mostrar_pantalla_inicio()

    # INTERFACE
    def limpiar_pantalla(self):
        self.canvas.delete("all")
        for boton in self.botones_interfaz:
            boton.destroy()
        self.botones_interfaz = []

    def mostrar_pantalla_inicio(self):
        self.estado = "MENU"
        self.limpiar_pantalla()
        self.canvas.create_text(
            ANCHO // 2, ALTO // 3, text="SPACE INVADERS", fill="#00ff66", font=("Arial", 40, "bold")
        )
        
        btn_jugar = tk.Button(
            self.root, text="PLAY", font=("Arial", 16, "bold"), bg="#00ff66", fg="black",
            activebackground="#00cc55", width=12, command=self.iniciar_partida
        )
        btn_jugar_window = self.canvas.create_window(ANCHO // 2, ALTO // 2, window=btn_jugar)
        self.botones_interfaz.append(btn_jugar)
        
        btn_salir = tk.Button(
            self.root, text="EXIT", font=("Arial", 16, "bold"), bg="#ff0055", fg="white",
            activebackground="#cc0044", width=12, command=self.root.destroy
        )
        btn_salir_window = self.canvas.create_window(ANCHO // 2, ALTO // 2 + 60, window=btn_salir)
        self.botones_interfaz.append(btn_salir)

    def iniciar_partida(self):
        self.limpiar_pantalla()
        self.estado = "JUGANDO"
        self.puntaje = 0
        self.direccion_enemigos = 1
        self.enemigos = []
        self.balas = []
        self.crear_jugador()
        self.crear_enemigos()
        self.crear_marcador()
        self.actualizar_juego()

    def mostrar_pantalla_fin(self, mensaje, color):
        self.estado = "FIN"
        self.limpiar_pantalla()
        self.canvas.create_text(
            ANCHO // 2, ALTO // 3, text=mensaje, fill=color, font=("Arial", 32, "bold")
        )
        
        self.canvas.create_text(
            ANCHO // 2, ALTO // 3 + 60, text=f"Score: {self.puntaje}", fill="white", font=("Arial", 20)
        )
        
        btn_reintentar = tk.Button(
            self.root, text="REPLAY", font=("Arial", 14, "bold"), bg="#00ccff", fg="black",
            activebackground="#0099cc", width=16, command=self.iniciar_partida
        )
        
        self.canvas.create_window(ANCHO // 2, ALTO // 2 + 40, window=btn_reintentar)
        self.botones_interfaz.append(btn_reintentar)
        
        btn_salir = tk.Button(
            self.root, text="EXIT", font=("Arial", 14, "bold"), bg="#ff0055", fg="white",
            activebackground="#cc0044", width=16, command=self.root.destroy
        )
        
        self.canvas.create_window(ANCHO // 2, ALTO // 2 + 100, window=btn_salir)
        self.botones_interfaz.append(btn_salir)

    # GAME ELEMENTS
    def crear_jugador(self):
        puntos = [400, 530, 375, 560, 425, 560]
        self.jugador = self.canvas.create_polygon(puntos, fill="#00ff66", outline="#ffffff")

    def crear_enemigos(self):
        colores = ["#ff0055", "#ffcc00", "#00ccff", "#cc00ff"]
        for fila in range(4):
            for col in range(8):
                x1 = 50 + col * 70
                y1 = 50 + fila * 50
                x2 = x1 + 40
                y2 = y1 + 30
                enemigo = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colores[fila], outline="black")
                self.enemigos.append(enemigo)

    def crear_marcador(self):
        self.texto_puntaje = self.canvas.create_text(
            70, 25, text=f"Score: {self.puntaje}", fill="white", font=("Arial", 16, "bold")
        )

    # CONTROLS
    def mover_izquierda(self, event):
        if self.estado != "JUGANDO": return
        pos_izquierda = self.canvas.coords(self.jugador)[2]
        if pos_izquierda > 10:
            self.canvas.move(self.jugador, -VELOCIDAD_JUGADOR, 0)

    def mover_derecha(self, event):
        if self.estado != "JUGANDO": return
        pos_derecha = self.canvas.coords(self.jugador)[4]
        if pos_derecha < ANCHO - 10:
            self.canvas.move(self.jugador, VELOCIDAD_JUGADOR, 0)

    def disparar(self, event):
        if self.estado != "JUGANDO": return
        if len(self.balas) < 4:
            pos_nave = self.canvas.coords(self.jugador)
            centro_x = (pos_nave[0] + pos_nave[2]) / 2
            punta_y = pos_nave[1]
            bala = self.canvas.create_rectangle(centro_x - 2, punta_y - 10, centro_x + 2, punta_y, fill="#ffff00")
            self.balas.append(bala)

    # LOGIC & ANIMATIONS
    def actualizar_juego(self):
        if self.estado == "JUGANDO":
            self.mover_balas()
            self.mover_enemigos()
            self.verificar_colisiones()
            if not self.enemigos:
                self.mostrar_pantalla_fin("¡YOU WIN!", "#00ff66")
                return
            self.root.after(20, self.actualizar_juego)

    def mover_balas(self):
        for bala in self.balas[:]:
            self.canvas.move(bala, 0, VELOCIDAD_BALA)
            pos = self.canvas.coords(bala)
            if pos[1] < 0:
                self.canvas.delete(bala)
                self.balas.remove(bala)

    def mover_enemigos(self):
        tocar_borde = False
        for enemigo in self.enemigos:
            self.canvas.move(enemigo, VELOCIDAD_ENEMIGO * self.direccion_enemigos, 0)
            pos = self.canvas.coords(enemigo)
            if pos[2] >= ANCHO - 10 or pos[0] <= 10:
                tocar_borde = True
            if pos[3] >= 530:
                self.mostrar_pantalla_fin("GAME OVER", "#ff0055")
                return
        if tocar_borde:
            self.direccion_enemigos *= -1
            for enemigo in self.enemigos:
                self.canvas.move(enemigo, 0, BAJADA_ENEMIGO)

    def verificar_colisiones(self):
        for bala in self.balas[:]:
            pos_bala = self.canvas.coords(bala)
            if not pos_bala: continue
            for enemigo in self.enemigos[:]:
                pos_enemigo = self.canvas.coords(enemigo)
                if (pos_bala[2] >= pos_enemigo[0] and pos_bala[0] <= pos_enemigo[2] and
                    pos_bala[3] >= pos_enemigo[1] and pos_bala[1] <= pos_enemigo[3]):
                    self.canvas.delete(bala)
                    self.canvas.delete(enemigo)
                    if bala in self.balas: self.balas.remove(bala)
                    if enemigo in self.enemigos: self.enemigos.remove(enemigo)
                    self.puntaje += 10
                    self.canvas.itemconfig(self.texto_puntaje, text=f"Score: {self.puntaje}")
                    break

if __name__ == "__main__":
    root = tk.Tk()
    juego = SpaceInvaders(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controlador import Controlador

class Vista:
    def __init__(self, ventana):
        self.root = ventana
        self.root.title("Codificación Huffman / Shannon-Fano")
        self.controlador = Controlador()

        # --- Frame entrada y botones ---
        frame_entrada = tk.Frame(self.root)
        frame_entrada.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(frame_entrada, text="Texto:").pack(anchor='w')
        self.entrada = tk.Text(frame_entrada, height=5, width=60)
        self.entrada.pack(pady=5)

        botones_frame = tk.Frame(frame_entrada)
        botones_frame.pack()

        tk.Button(botones_frame, text="Codificar", command=self.codificar).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Decodificar", command=self.decodificar).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Comparar", command=self.comparar).pack(side=tk.LEFT, padx=5)
        tk.Button(botones_frame, text="Cargar archivo", command=self.cargar_archivo).pack(side=tk.LEFT, padx=5)

        # --- Resultados Codificación ---
        self.frame_res_cod = tk.Frame(self.root)
        self.label_huff = tk.Label(self.frame_res_cod, text="Resultado Huffman:")
        self.resultado_huff = scrolledtext.ScrolledText(self.frame_res_cod, height=5, width=60)

        self.label_shan = tk.Label(self.frame_res_cod, text="Resultado Shannon-Fano:")
        self.resultado_shan = scrolledtext.ScrolledText(self.frame_res_cod, height=5, width=60)

        # --- Resultado Decodificación ---
        self.frame_res_dec = tk.Frame(self.root)
        self.label_dec = tk.Label(self.frame_res_dec, text="Resultado Decodificación:")
        self.resultado_dec = scrolledtext.ScrolledText(self.frame_res_dec, height=5, width=60)

    def ocultar_resultados(self):
        self.frame_res_cod.pack_forget()
        self.frame_res_dec.pack_forget()

    def codificar(self):
        self.ocultar_resultados()

        texto = self.entrada.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Atención", "Ingrese texto para codificar.")
            return

        self.controlador.cargar_texto(texto)
        self.controlador.codificar()

        self.resultado_huff.delete("1.0", tk.END)
        self.resultado_shan.delete("1.0", tk.END)

        self.resultado_huff.insert(tk.END, self.controlador.cod_huffman)
        self.resultado_shan.insert(tk.END, self.controlador.cod_shannon)

        self.frame_res_cod.pack(padx=10, pady=5, fill=tk.X)
        self.label_huff.pack(anchor='w')
        self.resultado_huff.pack(pady=2)
        self.label_shan.pack(anchor='w')
        self.resultado_shan.pack(pady=2)

    def decodificar(self):
        self.ocultar_resultados()

        mensaje_cod = self.entrada.get("1.0", tk.END).strip()
        if not mensaje_cod:
            messagebox.showwarning("Atención", "Ingrese mensaje codificado para decodificar.")
            return

        dec_huff = self.controlador.decodificar(mensaje_cod, "huffman")
        dec_shan = self.controlador.decodificar(mensaje_cod, "shannon")

        self.resultado_dec.delete("1.0", tk.END)

        if dec_huff:
            self.resultado_dec.insert(tk.END, f"Decodificado con Huffman:\n{dec_huff}")
        elif dec_shan:
            self.resultado_dec.insert(tk.END, f"Decodificado con Shannon-Fano:\n{dec_shan}")
        else:
            self.resultado_dec.insert(tk.END, "No se pudo decodificar el mensaje con ninguno de los dos métodos.")

        self.frame_res_dec.pack(padx=10, pady=5, fill=tk.X)
        self.label_dec.pack(anchor='w')
        self.resultado_dec.pack(pady=5)

    def comparar(self):
        metricas = self.controlador.obtener_metricas()
        if not metricas:
            messagebox.showinfo("Comparar", "No hay codificación previa.")
            return

        algoritmos = ['Huffman', 'Shannon-Fano']
        tasa_compresion = [metricas['huffman']['tasa'], metricas['shannon']['tasa']]
        longitud_promedio = [metricas['huffman']['longitud_prom'], metricas['shannon']['longitud_prom']]
        bits_codificados = [metricas['huffman']['bits'], metricas['shannon']['bits']]

        fig, axs = plt.subplots(3, 1, figsize=(8, 10))

        axs[0].bar(algoritmos, tasa_compresion, color=['green', 'blue'])
        axs[0].set_title('Tasa de compresión')
        axs[0].set_ylim(0, max(tasa_compresion) * 1.2)

        axs[1].bar(algoritmos, longitud_promedio, color=['green', 'blue'])
        axs[1].set_title('Longitud promedio del código')
        axs[1].set_ylim(0, max(longitud_promedio) * 1.2)

        axs[2].bar(algoritmos, bits_codificados, color=['green', 'blue'])
        axs[2].set_title('Bits codificados')
        axs[2].set_ylim(0, max(bits_codificados) * 1.2)

        plt.tight_layout()

        ventana_grafico = tk.Toplevel(self.root)
        ventana_grafico.title("Comparación de Algoritmos")

        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

        

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()
                self.entrada.delete("1.0", "end")
                self.entrada.insert("1.0", contenido)


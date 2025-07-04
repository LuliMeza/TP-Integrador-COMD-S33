import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controlador import Controlador

class Vista:
    def __init__(self, ventana):
        self.root = ventana
        self.root.title("Codificación Huffman / Shannon-Fano")
        self.root.configure(bg='#f0f0f0')
        self.root.geometry("800x700")
        
        # Configurar estilo
        self.configurar_estilo()
        
        self.controlador = Controlador()

        # --- Título principal ---
        titulo_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        titulo_frame.pack(fill=tk.X, pady=(0, 20))
        titulo_frame.pack_propagate(False)
        
        titulo = tk.Label(titulo_frame, text="Codificación Huffman / Shannon-Fano", 
                         font=('Segoe UI', 16, 'bold'), fg='white', bg='#2c3e50')
        titulo.pack(expand=True)

        # --- Frame entrada y botones ---
        frame_entrada = tk.Frame(self.root, bg='white', relief='raised', bd=2)
        frame_entrada.pack(padx=20, pady=10, fill=tk.X)

        # Título de sección
        tk.Label(frame_entrada, text="Entrada de Texto", 
                font=('Segoe UI', 12, 'bold'), fg='#2c3e50', bg='white').pack(anchor='w', padx=15, pady=(15, 5))

        # Frame para el área de texto
        texto_frame = tk.Frame(frame_entrada, bg='white')
        texto_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(texto_frame, text="Texto a procesar:", 
                font=('Segoe UI', 10), fg='#34495e', bg='white').pack(anchor='w')
        
        # Área de texto con estilo
        self.entrada = tk.Text(texto_frame, height=6, width=70, 
                              font=('Consolas', 10), 
                              bg='#f8f9fa', fg='#2c3e50',
                              relief='solid', bd=1,
                              padx=10, pady=10)
        self.entrada.pack(pady=5, fill=tk.X)

        # Frame para botones
        botones_frame = tk.Frame(frame_entrada, bg='white')
        botones_frame.pack(pady=15)

        # Botones estilizados
        botones = [
            ("🔐 Codificar", self.codificar, '#27ae60'),
            ("🔓 Decodificar", self.decodificar, '#3498db'),
            ("📊 Comparar", self.comparar, '#e74c3c'),
            ("📁 Cargar archivo", self.cargar_archivo, '#9b59b6')
        ]

        for texto, comando, color in botones:
            btn = tk.Button(botones_frame, text=texto, command=comando,
                           font=('Segoe UI', 10, 'bold'),
                           bg=color, fg='white',
                           relief='flat', bd=0,
                           padx=20, pady=8,
                           cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
            
            # Efectos hover
            btn.bind('<Enter>', lambda e, b=btn, c=color: self.on_hover(b, c, True))
            btn.bind('<Leave>', lambda e, b=btn, c=color: self.on_hover(b, c, False))

        # --- Resultados Codificación ---
        self.frame_res_cod = tk.Frame(self.root, bg='white', relief='raised', bd=2)
        
        # Título de resultados
        self.titulo_huff = tk.Label(self.frame_res_cod, text="Resultados de Codificación", 
                                   font=('Segoe UI', 12, 'bold'), fg='#2c3e50', bg='white')
        
        # Frame para Huffman
        self.frame_huff = tk.Frame(self.frame_res_cod, bg='#e8f5e8', relief='solid', bd=1)
        self.label_huff = tk.Label(self.frame_huff, text="🔐 Codificación Huffman:", 
                                  font=('Segoe UI', 10, 'bold'), fg='#27ae60', bg='#e8f5e8')
        self.resultado_huff = scrolledtext.ScrolledText(self.frame_huff, height=4, width=70,
                                                       font=('Consolas', 9), 
                                                       bg='white', fg='#2c3e50',
                                                       relief='solid', bd=1)

        # Frame para Shannon-Fano
        self.frame_shan = tk.Frame(self.frame_res_cod, bg='#e8f4fd', relief='solid', bd=1)
        self.label_shan = tk.Label(self.frame_shan, text="🔐 Codificación Shannon-Fano:", 
                                  font=('Segoe UI', 10, 'bold'), fg='#3498db', bg='#e8f4fd')
        self.resultado_shan = scrolledtext.ScrolledText(self.frame_shan, height=4, width=70,
                                                       font=('Consolas', 9), 
                                                       bg='white', fg='#2c3e50',
                                                       relief='solid', bd=1)

        # --- Resultado Decodificación ---
        self.frame_res_dec = tk.Frame(self.root, bg='white', relief='raised', bd=2)
        self.titulo_dec = tk.Label(self.frame_res_dec, text="Resultado de Decodificación", 
                                  font=('Segoe UI', 12, 'bold'), fg='#2c3e50', bg='white')
        self.frame_dec = tk.Frame(self.frame_res_dec, bg='#fff3cd', relief='solid', bd=1)
        self.label_dec = tk.Label(self.frame_dec, text="🔓 Texto Decodificado:", 
                                 font=('Segoe UI', 10, 'bold'), fg='#f39c12', bg='#fff3cd')
        self.resultado_dec = scrolledtext.ScrolledText(self.frame_dec, height=4, width=70,
                                                      font=('Consolas', 9), 
                                                      bg='white', fg='#2c3e50',
                                                      relief='solid', bd=1)

    def configurar_estilo(self):
        """Configura el estilo general de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores de fondo
        self.root.configure(bg='#f0f0f0')

    def on_hover(self, button, color, entering):
        """Efecto hover para los botones"""
        if entering:
            # Hacer el color más claro
            r, g, b = self.root.winfo_rgb(color)
            lighter_color = f'#{min(255, int(r/256*1.2)):02x}{min(255, int(g/256*1.2)):02x}{min(255, int(b/256*1.2)):02x}'
            button.configure(bg=lighter_color)
        else:
            button.configure(bg=color)

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

        # Debug: imprimir tablas para verificar
        print("=== TABLAS DEBUG ===")
        print(f"Tabla Huffman: {self.controlador.tabla_huffman}")
        print(f"Tabla Shannon: {self.controlador.tabla_shannon}")
        print(f"Código Huffman: {self.controlador.cod_huffman}")
        print(f"Código Shannon: {self.controlador.cod_shannon}")
        print(f"Longitud Huffman: {len(self.controlador.cod_huffman)} bits")
        print(f"Longitud Shannon: {len(self.controlador.cod_shannon)} bits")
        print("===================")

        self.resultado_huff.delete("1.0", tk.END)
        self.resultado_shan.delete("1.0", tk.END)

        self.resultado_huff.insert(tk.END, self.controlador.cod_huffman)
        self.resultado_shan.insert(tk.END, self.controlador.cod_shannon)

        # Mostrar resultados con estilo
        self.frame_res_cod.pack(padx=20, pady=10, fill=tk.X)
        self.titulo_huff.pack(anchor='w', padx=15, pady=(15, 10))
        
        # Frame Huffman
        self.frame_huff.pack(fill=tk.X, padx=15, pady=5)
        self.label_huff.pack(anchor='w', padx=10, pady=(10, 5))
        self.resultado_huff.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        # Frame Shannon-Fano
        self.frame_shan.pack(fill=tk.X, padx=15, pady=5)
        self.label_shan.pack(anchor='w', padx=10, pady=(10, 5))
        self.resultado_shan.pack(padx=10, pady=(0, 10), fill=tk.X)

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

        # Mostrar resultado con estilo
        self.frame_res_dec.pack(padx=20, pady=10, fill=tk.X)
        self.titulo_dec.pack(anchor='w', padx=15, pady=(15, 10))
        self.frame_dec.pack(fill=tk.X, padx=15, pady=5)
        self.label_dec.pack(anchor='w', padx=10, pady=(10, 5))
        self.resultado_dec.pack(padx=10, pady=(0, 10), fill=tk.X)

    def comparar(self):
        metricas = self.controlador.obtener_metricas()
        if not metricas:
            messagebox.showinfo("Comparar", "No hay codificación previa.")
            return

        # Debug: imprimir métricas para verificar
        print("=== MÉTRICAS DEBUG ===")
        print(f"Huffman - Bits: {metricas['huffman']['bits']}, Tasa: {metricas['huffman']['tasa']:.4f}, Longitud prom: {metricas['huffman']['longitud_prom']:.4f}")
        print(f"Shannon - Bits: {metricas['shannon']['bits']}, Tasa: {metricas['shannon']['tasa']:.4f}, Longitud prom: {metricas['shannon']['longitud_prom']:.4f}")
        print(f"Original bits: {metricas['original_bits']}")
        print("=====================")

        algoritmos = ['Huffman', 'Shannon-Fano']
        tasa_compresion = [metricas['huffman']['tasa'], metricas['shannon']['tasa']]
        longitud_promedio = [metricas['huffman']['longitud_prom'], metricas['shannon']['longitud_prom']]
        bits_codificados = [metricas['huffman']['bits'], metricas['shannon']['bits']]

        # Configurar estilo de matplotlib
        plt.style.use('seaborn-v0_8')
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))
        fig.patch.set_facecolor('#f0f0f0')

        # Colores modernos
        colores = ['#27ae60', '#3498db']

        axs[0].bar(algoritmos, tasa_compresion, color=colores, alpha=0.8, edgecolor='white', linewidth=2)
        axs[0].set_title('Tasa de compresión', fontsize=14, fontweight='bold', color='#2c3e50')
        axs[0].set_ylim(0, max(tasa_compresion) * 1.2)
        axs[0].grid(True, alpha=0.3)

        axs[1].bar(algoritmos, longitud_promedio, color=colores, alpha=0.8, edgecolor='white', linewidth=2)
        axs[1].set_title('Longitud promedio del código', fontsize=14, fontweight='bold', color='#2c3e50')
        axs[1].set_ylim(0, max(longitud_promedio) * 1.2)
        axs[1].grid(True, alpha=0.3)

        axs[2].bar(algoritmos, bits_codificados, color=colores, alpha=0.8, edgecolor='white', linewidth=2)
        axs[2].set_title('Bits codificados', fontsize=14, fontweight='bold', color='#2c3e50')
        axs[2].set_ylim(0, max(bits_codificados) * 1.2)
        axs[2].grid(True, alpha=0.3)

        # Configurar estilo de los ejes
        for ax in axs:
            ax.set_facecolor('#f8f9fa')
            ax.tick_params(colors='#2c3e50')
            for spine in ax.spines.values():
                spine.set_color('#bdc3c7')

        plt.tight_layout()

        # Ventana del gráfico con estilo
        ventana_grafico = tk.Toplevel(self.root)
        ventana_grafico.title("Comparación de Algoritmos")
        ventana_grafico.configure(bg='#f0f0f0')
        ventana_grafico.geometry("900x700")

        # Título de la ventana
        titulo_graf = tk.Label(ventana_grafico, text="Análisis Comparativo de Algoritmos", 
                              font=('Segoe UI', 14, 'bold'), fg='#2c3e50', bg='#f0f0f0')
        titulo_graf.pack(pady=10)

        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=20, pady=10)

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    self.entrada.delete("1.0", "end")
                    self.entrada.insert("1.0", contenido)
                messagebox.showinfo("Éxito", f"Archivo cargado exitosamente: {archivo.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")


import modelo
from collections import Counter

class Controlador:
    def __init__(self):
        self.texto_original = ""
        self.cod_huffman = ""
        self.cod_shannon = ""
        self.arbol_huffman = None
        self.tabla_huffman = {}
        self.tabla_shannon = {}
        self.freqs = {}

    def cargar_texto(self, texto):
        self.texto_original = texto
        self.freqs = Counter(texto)

    def codificar(self):
        self.arbol_huffman = modelo.construir_arbol_huffman(self.freqs)
        self.tabla_huffman = modelo.generar_tabla_huffman(self.arbol_huffman)
        self.cod_huffman = modelo.codificar(self.texto_original, self.tabla_huffman)

        self.tabla_shannon = modelo.construir_tabla_shannon_fano(self.freqs)
        self.cod_shannon = modelo.codificar(self.texto_original, self.tabla_shannon)

    


    def obtener_metricas(self):
        original_bits = len(self.texto_original) * 8
        huff_bits = len(self.cod_huffman)
        shan_bits = len(self.cod_shannon)

        ent_h, lp_h, ef_h = modelo.calcular_metrica(self.freqs, self.tabla_huffman)
        ent_s, lp_s, ef_s = modelo.calcular_metrica(self.freqs, self.tabla_shannon)

        return {
            "original_bits": original_bits,
            "huffman": {
                "bits": huff_bits,
                "tasa": modelo.tasa_compresion(original_bits, huff_bits),
                "entropia": ent_h,
                "longitud_prom": lp_h,
                "eficiencia": ef_h
            },
            "shannon": {
                "bits": shan_bits,
                "tasa": modelo.tasa_compresion(original_bits, shan_bits),
                "entropia": ent_s,
                "longitud_prom": lp_s,
                "eficiencia": ef_s
            }
        }

    def decodificar(self, mensaje_codificado, algoritmo):
        # Solo intenta decodificar si el mensaje coincide con uno de los generados
        if algoritmo == "huffman" and mensaje_codificado == self.cod_huffman:
            return modelo.decodificar_huffman(mensaje_codificado, self.arbol_huffman)
        elif algoritmo == "shannon" and mensaje_codificado == self.cod_shannon:
            return modelo.decodificar_shannon_fano(mensaje_codificado, self.tabla_shannon)
        else:
            return None

    def codificar_huffman(self, texto):
        # Codifica solo con Huffman y retorna
        self.cargar_texto(texto)
        self.arbol_huffman = modelo.construir_arbol_huffman(self.freqs)
        self.tabla_huffman = modelo.generar_tabla_huffman(self.arbol_huffman)
        self.cod_huffman = modelo.codificar(self.texto_original, self.tabla_huffman)
        return self.cod_huffman

    def codificar_shannon(self, texto):
        # Codifica solo con Shannon-Fano y retorna
        self.cargar_texto(texto)
        self.tabla_shannon = modelo.construir_tabla_shannon_fano(self.freqs)
        self.cod_shannon = modelo.codificar(self.texto_original, self.tabla_shannon)
        return self.cod_shannon

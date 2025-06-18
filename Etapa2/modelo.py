import heapq
import math

class NodoHuffman:
    def __init__(self, simbolo=None, freq=0):
        self.simbolo = simbolo
        self.freq = freq
        self.izq = None
        self.der = None
    def __lt__(self, otro):
        return self.freq < otro.freq

def construir_arbol_huffman(freqs):
    heap = [NodoHuffman(s, f) for s, f in freqs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        nuevo = NodoHuffman(freq=n1.freq + n2.freq)
        nuevo.izq = n1
        nuevo.der = n2
        heapq.heappush(heap, nuevo)
    return heap[0]

def generar_tabla_huffman(nodo, codigo="", tabla=None):
    if tabla is None:
        tabla = {}
    if nodo.simbolo is not None:
        tabla[nodo.simbolo] = codigo or "0"
    else:
        generar_tabla_huffman(nodo.izq, codigo + "0", tabla)
        generar_tabla_huffman(nodo.der, codigo + "1", tabla)
    return tabla

def construir_tabla_shannon_fano(freqs):
    simbolos_freq = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    tabla = {}

    def dividir(simbolos, codigo=""):
        if len(simbolos) == 1:
            tabla[simbolos [0][0]] = codigo or "0"
            return

        total = sum(f for _, f in simbolos)
        best_diff = float("inf")
        best_index = 1
        acumulado = 0

        for i in range(1, len(simbolos)):
            acumulado += simbolos[i - 1][1]
            diferencia = abs((total - acumulado) - acumulado)
            if diferencia < best_diff:
                best_diff = diferencia
                best_index = i

        izquierda = simbolos[:best_index]
        derecha = simbolos[best_index:]

        dividir(izquierda, codigo + "0")
        dividir(derecha, codigo + "1")

    dividir(simbolos_freq)
    return tabla


def codificar(texto, tabla):
    return "".join(tabla[c] for c in texto)

def decodificar_huffman(codigo_bin, arbol):
    resultado = []
    nodo = arbol
    for bit in codigo_bin:
        nodo = nodo.izq if bit == "0" else nodo.der
        if nodo.simbolo is not None:
            resultado.append(nodo.simbolo)
            nodo = arbol
    return "".join(resultado)

def decodificar_shannon_fano(codigo_bin, tabla):
    inv_tabla = {v: k for k, v in tabla.items()}
    resultado = []
    buffer = ""
    for bit in codigo_bin:
        buffer += bit
        if buffer in inv_tabla:
            resultado.append(inv_tabla[buffer])
            buffer = ""
    return "".join(resultado)

def calcular_metrica(freqs, tabla):
    total = sum(freqs.values())
    longitudes = {s: len(tabla[s]) for s in tabla}
    longitud_prom = sum(freqs[s] * longitudes[s] for s in freqs) / total
    entropia = -sum((freqs[s] / total) * (math.log2(freqs[s] / total)) for s in freqs)
    eficiencia = entropia / longitud_prom if longitud_prom != 0 else 0
    return entropia, longitud_prom, eficiencia


def tasa_compresion(original_bits, codificado_bits):
    return codificado_bits / original_bits
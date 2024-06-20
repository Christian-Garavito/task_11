from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import numpy as np

# Definimos la sopa de letras y las palabras a buscar
sopa = [
    ['C', 'A', 'T', 'D', 'O', 'G'],
    ['X', 'Y', 'Z', 'A', 'B', 'C'],
    ['D', 'O', 'G', 'X', 'Y', 'Z'],
    ['A', 'B', 'C', 'D', 'E', 'F'],
    ['X', 'Y', 'Z', 'C', 'A', 'T'],
    ['T', 'C', 'A', 'T', 'D', 'O']
]

palabras = ['CAT', 'DOG']

# Función para buscar palabras en la sopa de letras
def buscar_palabras(sopa, palabras):
    filas = len(sopa)
    columnas = len(sopa[0])
    direcciones = [(0, 1), (1, 0), (1, 1), (1, -1)]
    encontrado = []

    def en_rango(x, y):
        return 0 <= x < filas and 0 <= y < columnas

    def buscar_palabra(palabra):
        for x in range(filas):
            for y in range(columnas):
                for dx, dy in direcciones:
                    nx, ny = x, y
                    for letra in palabra:
                        if en_rango(nx, ny) and sopa[nx][ny] == letra:
                            nx += dx
                            ny += dy
                        else:
                            break
                    else:
                        return (x, y, dx, dy)
        return None

    for palabra in palabras:
        resultado = buscar_palabra(palabra)
        if resultado:
            encontrado.append((palabra, resultado))
    return encontrado

# Generar el PDF con la sopa de letras y las palabras encontradas
def generar_pdf(sopa, palabras, resultados, nombre_archivo):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    # Dibujar la sopa de letras
    tamano_celda = 20
    x_inicial = 50
    y_inicial = height - 50

    for i, fila in enumerate(sopa):
        for j, letra in enumerate(fila):
            c.drawString(x_inicial + j * tamano_celda, y_inicial - i * tamano_celda, letra)

    # Destacar las palabras encontradas
    for palabra, (x, y, dx, dy) in resultados:
        c.setFillColor(colors.red)
        for i, letra in enumerate(palabra):
            c.drawString(x_inicial + (y + i * dy) * tamano_celda, y_inicial - (x + i * dx) * tamano_celda, letra)
        c.setFillColor(colors.black)

    # Dibujar la lista de palabras
    c.drawString(x_inicial, y_inicial - len(sopa) * tamano_celda - 20, "Palabras a buscar:")
    for i, palabra in enumerate(palabras):
        c.drawString(x_inicial, y_inicial - len(sopa) * tamano_celda - 40 - i * 20, palabra)

    c.save()

# Buscar palabras y generar el PDF
resultados = buscar_palabras(sopa, palabras)
generar_pdf(sopa, palabras, resultados, "sopa_de_letras.pdf")




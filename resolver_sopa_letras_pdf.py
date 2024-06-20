from reportlab.lib.pagesizes import letter  # Importa el tamaño de página 'letter' de reportlab
from reportlab.lib.styles import getSampleStyleSheet  # Importa una función para obtener estilos predeterminados
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer  # Importa elementos necesarios para crear un PDF
from reportlab.lib import colors  # Importa colores de reportlab
import json  # Importa el módulo json para trabajar con archivos JSON


# Lee el archivo JSON y lo convierte a un diccionario
def get_data(filename):
    with open(filename, "r") as file:  # Abre el archivo en modo lectura
        return json.loads(file.read()) or {}  # Lee el contenido y lo convierte a un diccionario


# Imprime la sopa de letras en la consola
def print_sopa(sopa_letras):
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in sopa_letras]))  # Formatea y imprime la sopa de letras


# Función para buscar una palabra en la matriz en una dirección específica
def buscar_palabra(matriz, palabra, direccion):
    tamaño = len(matriz)  # Obtiene el tamaño de la matriz
    longitud = len(palabra)  # Obtiene la longitud de la palabra
   
    for fila in range(tamaño):
        for columna in range(tamaño):
            # Verifica si la palabra cabe en la dirección actual
            fin_fila = fila + direccion[0] * (longitud - 1)
            fin_columna = columna + direccion[1] * (longitud - 1)
           
            if 0 <= fin_fila < tamaño and 0 <= fin_columna < tamaño:  # Verifica si los índices están dentro de los límites de la matriz
                encontrada = True
                for i in range(longitud):
                    nueva_fila = fila + i * direccion[0]
                    nueva_columna = columna + i * direccion[1]
                    if matriz[nueva_fila][nueva_columna] != palabra[i]:  # Verifica si la letra coincide
                        encontrada = False
                        break
                if encontrada:
                    return (fila, columna), (fin_fila, fin_columna)  # Devuelve las coordenadas de inicio y fin
    return None


# Función para resolver la sopa de letras
def resolver_sopa(matriz, palabras):
    direcciones = [
        (0, 1),    # Horizontal derecha
        (1, 0),    # Vertical abajo
        (1, 1),    # Diagonal abajo-derecha
        (1, -1),   # Diagonal abajo-izquierda
        (0, -1),   # Horizontal izquierda
        (-1, 0),   # Vertical arriba
        (-1, -1),  # Diagonal arriba-izquierda
        (-1, 1)    # Diagonal arriba-derecha
    ]
   
    resultados = {}
    for palabra in palabras:
        for direccion in direcciones:
            resultado = buscar_palabra(matriz, palabra, direccion)  # Busca la palabra en la dirección especificada
            if resultado:
                resultados[palabra] = resultado  # Si se encuentra, agrega el resultado al diccionario
                break
    return resultados


# Función para colorear las celdas de la matriz donde se encuentran las palabras
def colorear_matriz(matriz, resultados):
    tamaño = len(matriz)  # Obtiene el tamaño de la matriz
    colores = [colors.yellow, colors.lightgreen, colors.lightblue, colors.orange, colors.pink]  # Define una lista de colores
    matriz_coloreada = [['' for _ in range(tamaño)] for _ in range(tamaño)]  # Inicializa la matriz coloreada

    for idx, (palabra, coordenadas) in enumerate(resultados.items()):
        (fila_inicio, columna_inicio), (fila_fin, columna_fin) = coordenadas
        direccion_fila = 1 if fila_fin > fila_inicio else -1 if fila_fin < fila_inicio else 0
        direccion_columna = 1 if columna_fin > columna_inicio else -1 if columna_fin < columna_inicio else 0

        for i in range(len(palabra)):
            fila_actual = fila_inicio + i * direccion_fila
            columna_actual = columna_inicio + i * direccion_columna
            matriz_coloreada[fila_actual][columna_actual] = (matriz[fila_actual][columna_actual], colores[idx % len(colores)])  # Colorea la celda correspondiente
   
    for fila in range(tamaño):
        for columna in range(tamaño):
            if not matriz_coloreada[fila][columna]:  # Si la celda no está coloreada
                matriz_coloreada[fila][columna] = (matriz[fila][columna], colors.white)  # Asigna el color blanco
   
    return matriz_coloreada


# Función para crear un PDF con la respuesta de la sopa de letras
def crear_pdf(matriz, resultados, archivo_pdf="resultado_sopa_de_letras.pdf"):
    doc = SimpleDocTemplate(archivo_pdf, pagesize=letter)  # Crea un documento PDF con tamaño de página 'letter'
    elements = []
    styles = getSampleStyleSheet()  # Obtiene los estilos predeterminados

    # Título
    elements.append(Paragraph("Resultado de la Sopa de Letras", styles['Title']))  # Agrega un título al PDF
    elements.append(Spacer(1, 12))  # Agrega un espacio

    # Crear la matriz coloreada
    matriz_coloreada = colorear_matriz(matriz, resultados)  # Colorea la matriz
    data = [[f"{letra}" for letra, _ in fila] for fila in matriz_coloreada]  # Prepara los datos para la tabla
   
    # Crear la tabla
    table = Table(data)  # Crea una tabla con los datos
   
    # Estilos de la tabla
    estilo = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                         ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                         ('FONTSIZE', (0, 0), (-1, -1), 10),
                         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                         ('BOX', (0, 0), (-1, -1), 0.25, colors.black)])
   
    for fila in range(len(matriz_coloreada)):
        for columna in range(len(matriz_coloreada[0])):
            estilo.add('BACKGROUND', (columna, fila), (columna, fila), matriz_coloreada[fila][columna][1])  # Colorea las celdas de la tabla
   
    table.setStyle(estilo)  # Aplica el estilo a la tabla
    elements.append(table)  # Agrega la tabla a los elementos del PDF
   
    # Espacio antes de la lista de palabras
    elements.append(Spacer(1, 12))  # Agrega un espacio
   
    # Añadir lista de palabras encontradas
    elements.append(Paragraph("Palabras encontradas:", styles['Heading2']))  # Agrega un encabezado
    for palabra in resultados:
        elements.append(Paragraph(palabra, styles['Normal']))  # Agrega cada palabra encontrada
        elements.append(Spacer(1, 12))  # Agrega un espacio entre las palabras
   
    doc.build(elements)  # Construye el PDF


# Función principal para resolver la sopa de letras y generar el PDF
def sopa(matriz, palabras):
    resultados = resolver_sopa(matriz, palabras)  # Resuelve la sopa de letras
    for palabra, coordenadas in resultados.items():
        print(f"La palabra '{palabra}' se encuentra desde {coordenadas[0]} hasta {coordenadas[1]}")  # Imprime las coordenadas de las palabras encontradas
    crear_pdf(matriz, resultados)  # Crea el PDF con los resultados


def main():
    """Esta es la funcion principal"""
    vector_respuesta = get_data("vector-solucion.json")  
    sopa_letras = get_data("sopa-letras-llena.json")  
    print(vector_respuesta)  
    print_sopa(sopa_letras)  
    print("===========================================")
    sopa(sopa_letras, vector_respuesta) 


if __name__ == "__main__":
    main()  





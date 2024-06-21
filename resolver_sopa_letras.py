# Importacion de liberias a utilizar
import json



# Lee el archivo JSON y lo convierte a un diccionario
def get_data(filename):
    with open(filename, "r") as file:
        # en js seria JSON.parse
        return json.loads(file.read()) or {}

def print_sopa(sopa_letras):
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in sopa_letras]))

# Función para buscar una palabra en la matriz en una dirección específica
def buscar_palabra(matriz, palabra, direccion):
    tamaño = len(matriz)
    longitud = len(palabra)
    
    for fila in range(tamaño):
        for columna in range(tamaño):
            # Check if the word fits in the current direction
            fin_fila = fila + direccion[0] * (longitud - 1)
            fin_columna = columna + direccion[1] * (longitud - 1)
            
            if 0 <= fin_fila < tamaño and 0 <= fin_columna < tamaño:
                encontrada = True
                for i in range(longitud):
                    nueva_fila = fila + i * direccion[0]
                    nueva_columna = columna + i * direccion[1]
                    if matriz[nueva_fila][nueva_columna] != palabra[i]:
                        encontrada = False
                        break
                if encontrada:
                    return (fila, columna), (fin_fila, fin_columna)
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
            resultado = buscar_palabra(matriz, palabra, direccion)
            if resultado:
                resultados[palabra] = resultado
                break
    return resultados

def sopa(matriz,palabras):
    resultados = resolver_sopa(matriz, palabras)
    for palabra, coordenadas in resultados.items():
        print(f"La palabra '{palabra}' se encuentra desde {coordenadas[0]} hasta {coordenadas[1]}")

def main():
    """Esta es la funcion principal"""
    # snake case
    vector_respuesta = get_data("vector-solucion-cobos.json")
    sopa_letras= get_data("palabras-cobos.json")
    print(vector_respuesta)
    print_sopa(sopa_letras)
    print("===========================================")

    sopa(sopa_letras,vector_respuesta)



    





    
    
    
    





if __name__ == "__main__":
    main()
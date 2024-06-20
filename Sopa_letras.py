import json
from itertools import chain
import urllib3
from urllib3.exceptions import RequestError, ConnectionError, HTTPError
import random
import string

# Convierte el diccionario a JSON y lo guarda en un archivo
def save_data(filename, resultados):
    with open(filename, "w") as file:
        # en js seria JSON.stringify
        file.write(json.dumps(resultados))


def get_info_apis(url):
    try:
        http = urllib3.PoolManager()
        res = http.request(method="GET", url=url)
        response = json.loads(res.data.decode())
        return response
    except RequestError as ex:
        print("error1", ex)
    except ConnectionError as ex:
        print("error2", ex)
    except HTTPError as ex:
        print("error3", ex)
    except Exception as ex:
        print("name_error", type(ex).__name__)
        print("error4", ex)


def get_info_api_1():
    response = get_info_apis("https://jsonplaceholder.typicode.com/users")

    names = []
    try:
        for i in range(3):
            names.append(response[i]["username"].lower())

        return names
    except KeyError as key_error:
        print("No se obtubo el valor debido a:", key_error)


def get_info_api_2():
    response = get_info_apis("https://dummyjson.com/recipes")

    recetas = response["recipes"]

    names_meal_type = []
    try:
        for receta in recetas:
            names_meal_type.extend(receta["mealType"])

        return [meal.lower() for meal in names_meal_type][0:3]
    except KeyError as key_error:
        print("No se obtubo el valor debido a:", key_error)


def get_info_api_3():
    response = get_info_apis("https://www.omdbapi.com/?apikey=3923e2e&page=1&s=marvel")

    peliculas = response["Search"]

    movie_types = []
    try:
        for pelicula in peliculas:
            movie_types.append(pelicula["Type"].lower())

        return list(set(movie_types))[0:3]
    except KeyError as key_error:
        print("No se obtubo el valor debido a:", key_error)


def print_sopa(sopa_letras):
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in sopa_letras]))


def letra_aleatoria():
    return random.choice(string.ascii_lowercase) #upper


def disponible_horizontal(linea_sopa, palabra):
    espacio_disponible_x = len(linea_sopa) - len(palabra)

    for index in range(espacio_disponible_x, len(linea_sopa)):
        if linea_sopa[index] != "":
            return False
        
    return True

    # [
    #     [0, 1], 
    #     [2, 3]
    # ]

def llenar_sopa(sopa_letras, palabras):
    palabras_aleatorias = [*palabras]
    random.shuffle(palabras_aleatorias)
    print("****************************")
    print(palabras_aleatorias)
    print("****************************")

    # movimiento en x (->)
    index_x = 0
    #                 (|)
    # movimiento en y (v)
    index_y = 0

    for palabra in palabras_aleatorias:
        horizontal = bool(random.randint(0, 1))
        if horizontal:
            desp_x = random.randint(index_x, len(sopa_letras[0]) - len(palabra))
            for letra in palabra:
                sopa_letras[index_y][desp_x] = letra
                desp_x += 1
            
            index_y += 1
        else:
            desp_y = random.randint(index_y, len(sopa_letras) - len(palabra))
            for letra in palabra:
                sopa_letras[desp_y][index_x] = letra
                desp_y += 1
            
            index_x += 1

    return [[*fila] for fila in sopa_letras]


def llenar_sopa_mas_random(sopa_letras, palabras):
    palabras_aleatorias = [*palabras]
    random.shuffle(palabras_aleatorias)
    print("****************************")
    print(palabras_aleatorias)
    print("****************************")

    

    # movimiento en x (->)
    index_x = random.choice([0, len(sopa_letras[0]) - 1])
    index_x_ini = index_x
    # print(index_x_ini)
    #                 (|)
    # movimiento en y (v)
    index_y = random.choice([0, len(sopa_letras) - 1])
    index_y_ini = index_y
    # print(index_y_ini)

    step_x = 1 if index_x == 0 else -1
    step_y = 1 if index_y == 0 else -1

    def calc_desp_x():
        if index_x_ini == 0:
            return random.randint(index_x, len(sopa_letras[0]) - len(palabra))
        else:
            return random.randint(0, index_x - len(palabra))
    def calc_desp_y():
        if index_y_ini == 0:
            return random.randint(index_y, len(sopa_letras) - len(palabra))
        else:
            return random.randint(0, index_y - len(palabra))

    for palabra in palabras_aleatorias:
        # print(palabra)
        horizontal = bool(random.randint(0, 1))
        if horizontal:
            desp_x = calc_desp_x()
            for letra in palabra:
                sopa_letras[index_y][desp_x] = letra
                desp_x += 1
            
            index_y += step_y
        else:
            desp_y = calc_desp_y()
            for letra in palabra:
                sopa_letras[desp_y][index_x] = letra
                desp_y += 1
            
            index_x += step_x

    return [[*fila] for fila in sopa_letras]


def main():
    """Esta es la funcion principal"""
    palabras = list(
        chain.from_iterable(
            [
                get_info_api_1(),
                get_info_api_2(),
                get_info_api_3(),
            ]
        )
    )

    print(palabras)

    sopa_vacia = [[letra_aleatoria() for _ in range(15)] for _ in range(15)]

    print_sopa(sopa_vacia)

    sopa_llena = llenar_sopa_mas_random(sopa_vacia, palabras)

    print("========================================")

    print_sopa(sopa_llena)

    save_data("vector-solucion.json", palabras)  # Guarda el estado final de la copa en un archivo
    save_data("sopa-letras-llena.json",sopa_llena)  # Guarda los equipos ganadores en otro archivo





if __name__ == "__main__":
    main()

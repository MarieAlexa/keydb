import redis

client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)


def agregar_receta():
    receta_id = client.incr("receta:id")  # Generar un nuevo ID único
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos: ")

    key = f"receta:{receta_id}"
    receta = {
        "nombre": nombre,
        "ingredientes": ingredientes,
        "pasos": pasos
    }

    resultado = client.hset(key, mapping=receta)
    if resultado:
        print(f"Receta agregada con éxito. ID: {receta_id}")
    else:
        print("Error al agregar la receta.")

def ver_recetas():
    print("\nListado de Recetas:")
    keys = client.keys("receta:*")
    for key in keys:
        receta_id = key.split(":")[1]
        nombre = client.hget(key, "nombre")
        print(f"ID: {receta_id} | Nombre: {nombre}")
    print()

def buscar_receta():
    receta_id = input("ID de la receta a buscar: ")
    key = f"receta:{receta_id}"

    if client.exists(key):
        receta = client.hgetall(key)
        print(f"\nNombre: {receta['nombre']}")
        print(f"Ingredientes: {receta['ingredientes']}")
        print(f"Pasos: {receta['pasos']}\n")
    else:
        print("No se encontró una receta con ese ID.")

def actualizar_receta():
    ver_recetas()
    receta_id = input("ID de la receta a actualizar: ")
    key = f"receta:{receta_id}"

    if client.exists(key):
        receta = client.hgetall(key)
        print("Ingrese los nuevos valores (deje en blanco para mantener el actual):")
        nombre = input(f"Nombre [{receta['nombre']}]: ") or receta['nombre']
        ingredientes = input(f"Ingredientes [{receta['ingredientes']}]: ") or receta['ingredientes']
        pasos = input(f"Pasos [{receta['pasos']}]: ") or receta['pasos']

        nuevos_datos = {
            "nombre": nombre,
            "ingredientes": ingredientes,
            "pasos": pasos
        }

        client.hset(key, mapping=nuevos_datos)
        print("Receta actualizada con éxito.")
    else:
        print("No se encontró una receta con ese ID.")

def eliminar_receta():
    ver_recetas()
    receta_id = input("ID de la receta a eliminar: ")
    key = f"receta:{receta_id}"

    resultado = client.delete(key)
    if resultado:
        print("Receta eliminada con éxito.")
    else:
        print("No se encontró una receta con ese ID.")


def menu():
    print("\n--- Libro de Recetas ---")
    print("1. Agregar nueva receta")
    print("2. Actualizar receta existente")
    print("3. Eliminar receta existente")
    print("4. Ver listado de recetas")
    print("5. Buscar receta por ID")
    print("6. Salir")


def main():
    while True:
        menu()
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            agregar_receta()
        elif opcion == '2':
            actualizar_receta()
        elif opcion == '3':
            eliminar_receta()
        elif opcion == '4':
            ver_recetas()
        elif opcion == '5':
            buscar_receta()
        elif opcion == '6':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == '__main__':
    main()

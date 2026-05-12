import random


PERSONAJES = [
    'Caterina "La Viuda" Moretti',
    "El Marqués de la Seta",
    "Elias Vann",
    "Bella / Isabella Dupont",
    "Elena Varela",
    "Don Fernando",
    "La Marquesa Isolda de Azul Real",
    "Will",
]

ARMAS = [
    "Almohada",
    "Cuchillo",
    "Abre cartas",
    "Manguera",
    "Cizalla",
    "Maceta",
    "Trofeo",
    "Candelabro",
    "Pistola",
    "Veneno",
    "Puño americano",
    "Bate de béisbol",
    "Martillo"
]

ESTANCIAS = [
    "Habitación principal",
    "Habitación de sirvientes",
    "Cocina",
    "Salón",
    "Sala secreta",
    "Jardín",
    "Piscina",
    "Biblioteca",
]


def numero_aleatorio(limite: int) -> int:
    """Devuelve un número aleatorio entre 0 y limite - 1."""
    if limite <= 0:
        raise ValueError("El límite debe ser mayor que 0.")

    return random.randrange(limite)


def elegir_elemento(elementos: list[str]) -> str:
    indice = numero_aleatorio(len(elementos))
    return elementos[indice]


def elegir_personaje(personajes_disponibles: list[str]) -> str:
    indice = numero_aleatorio(len(personajes_disponibles))
    return personajes_disponibles.pop(indice)


def seleccionar_misterio(
    personajes: list[str],
    armas: list[str],
    estancias: list[str],
) -> dict[str, str]:
    if len(personajes) < 3:
        raise ValueError("Necesitás al menos 3 personajes para asignar los roles.")

    if not armas:
        raise ValueError("Necesitás al menos 1 arma.")

    if not estancias:
        raise ValueError("Necesitás al menos 1 estancia.")

    personajes_disponibles = personajes.copy()

    muerto = elegir_personaje(personajes_disponibles)
    asesino = elegir_personaje(personajes_disponibles)
    complice = elegir_personaje(personajes_disponibles)
    arma = elegir_elemento(armas)
    habitacion = elegir_elemento(estancias)

    return {
        "muerto": muerto,
        "asesino": asesino,
        "complice": complice,
        "arma": arma,
        "habitacion": habitacion,
    }


if __name__ == "__main__":
    misterio = seleccionar_misterio(PERSONAJES, ARMAS, ESTANCIAS)

    print("Misterio inicial:")
    print(f"Muerto: {misterio['muerto']}")
    print(f"Asesino: {misterio['asesino']}")
    print(f"Cómplice: {misterio['complice']}")
    print(f"Arma: {misterio['arma']}")
    print(f"Habitación del muerto: {misterio['habitacion']}")


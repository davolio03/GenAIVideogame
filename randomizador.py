from os import urandom


PERSONAJES = [
    "Caterina \"La Viuda\" Moretti",
    "El Marqués de la Seta",
    "Elias Vann",
    "Bella / Isabella Dupont",
    "Elena Varela",
    "Don Fernando",
    "La Marquesa Isolda de Azul Real",
    "Will",
]


def numero_aleatorio(limite: int) -> int:
    """Devuelve un número aleatorio entre 0 y limite - 1."""
    if limite <= 0:
        raise ValueError("El límite debe ser mayor que 0.")

    return int.from_bytes(urandom(4), "big") % limite


def elegir_personaje(personajes_disponibles: list[str]) -> str:
    indice = numero_aleatorio(len(personajes_disponibles))
    return personajes_disponibles.pop(indice)


def seleccionar_roles(personajes: list[str]) -> dict[str, str]:
    if len(personajes) < 3:
        raise ValueError("Necesitás al menos 3 personajes para asignar los roles.")

    disponibles = personajes.copy()

    muerto = elegir_personaje(disponibles)
    asesino = elegir_personaje(disponibles)
    complice = elegir_personaje(disponibles)

    return {
        "muerto": muerto,
        "asesino": asesino,
        "complice": complice,
    }


if __name__ == "__main__":
    roles = seleccionar_roles(PERSONAJES)

    print("Roles del misterio:")
    print(f"Muerto: {roles['muerto']}")
    print(f"Asesino: {roles['asesino']}")
    print(f"Cómplice: {roles['complice']}")

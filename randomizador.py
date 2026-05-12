import json
import random
import re
from pathlib import Path
from typing import Any


CARPETA_PROYECTO = Path(__file__).parent
RUTA_PREGUNTAS = CARPETA_PROYECTO / "Preguntas.md"
RUTA_MISTERIO = CARPETA_PROYECTO / "misterio.json"


PERSONAJES = [
    'Caterina "La Viuda" Moretti',
    "El Marques de la Seta",
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
    "Puno americano",
    "Bate de beisbol",
    "Martillo",
]

ESTANCIAS = [
    "Habitacion principal",
    "Habitacion de sirvientes",
    "Cocina",
    "Salon",
    "Sala secreta",
    "Jardin",
    "Piscina",
    "Biblioteca",
]


def cargar_preguntas() -> list[str]:
    contenido = RUTA_PREGUNTAS.read_text(encoding="utf-8")
    preguntas = []

    for linea in contenido.splitlines():
        linea = linea.strip()
        coincidencia = re.match(r"^\d+\.\s+(.*)$", linea)
        if coincidencia:
            preguntas.append(coincidencia.group(1))

    return preguntas


def numero_aleatorio(limite: int) -> int:
    """Devuelve un numero aleatorio entre 0 y limite - 1."""
    if limite <= 0:
        raise ValueError("El limite debe ser mayor que 0.")

    return random.randrange(limite)


def elegir_elemento(elementos: list[str]) -> str:
    indice = numero_aleatorio(len(elementos))
    return elementos[indice]


def elegir_personaje(personajes_disponibles: list[str]) -> str:
    indice = numero_aleatorio(len(personajes_disponibles))
    return personajes_disponibles.pop(indice)


def distribuir_armas(armas: list[str], estancias: list[str]) -> dict[str, str]:
    return {arma: elegir_elemento(estancias) for arma in armas}


def distribuir_personajes(
    personajes: list[str],
    estancias: list[str],
    muerto: str,
    habitacion_muerto: str,
) -> dict[str, str]:
    posiciones = {
        personaje: elegir_elemento(estancias)
        for personaje in personajes
    }

    posiciones[muerto] = habitacion_muerto

    return posiciones


def seleccionar_preguntas_por_personaje(
    personajes: list[str],
    muerto: str,
    preguntas: list[str],
    cantidad: int = 4,
) -> dict[str, list[str]]:
    if len(preguntas) < cantidad:
        raise ValueError(f"Necesitas al menos {cantidad} preguntas.")

    return {
        personaje: random.sample(preguntas, cantidad)
        for personaje in personajes
        if personaje != muerto
    }


def seleccionar_misterio(
    personajes: list[str],
    armas: list[str],
    estancias: list[str],
    preguntas: list[str],
) -> dict[str, Any]:
    if len(personajes) < 3:
        raise ValueError("Necesitas al menos 3 personajes para asignar los roles.")

    if not armas:
        raise ValueError("Necesitas al menos 1 arma.")

    if not estancias:
        raise ValueError("Necesitas al menos 1 estancia.")

    personajes_disponibles = personajes.copy()

    muerto = elegir_personaje(personajes_disponibles)
    asesino = elegir_personaje(personajes_disponibles)
    complice = elegir_personaje(personajes_disponibles)
    arma = elegir_elemento(armas)
    habitacion = elegir_elemento(estancias)

    ubicaciones_armas = distribuir_armas(armas, estancias)
    ubicaciones_personajes = distribuir_personajes(
        personajes,
        estancias,
        muerto,
        habitacion,
    )
    preguntas_personajes = seleccionar_preguntas_por_personaje(
        personajes,
        muerto,
        preguntas,
    )

    ubicaciones_armas[arma] = habitacion

    return {
        "muerto": muerto,
        "asesino": asesino,
        "complice": complice,
        "arma": arma,
        "habitacion": habitacion,
        "ubicaciones_armas": ubicaciones_armas,
        "ubicaciones_personajes": ubicaciones_personajes,
        "preguntas_personajes": preguntas_personajes,
    }


def guardar_misterio_json(misterio: dict[str, Any]) -> None:
    misterio_json = json.dumps(misterio, ensure_ascii=False, indent=4)
    RUTA_MISTERIO.write_text(misterio_json, encoding="utf-8")
    print(misterio_json)
    print(f"Misterio guardado en: {RUTA_MISTERIO}")


if __name__ == "__main__":
    preguntas = cargar_preguntas()
    misterio = seleccionar_misterio(PERSONAJES, ARMAS, ESTANCIAS, preguntas)
    guardar_misterio_json(misterio)

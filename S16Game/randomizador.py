"""Generador aleatorio de misterio para S16Game.

Provee los datos que build_prompt.py necesita:
- PERSONAJES, ARMAS, ESTANCIAS
- seleccionar_misterio() -> game_state con asesino, complice, muerto, etc.
- cargar_preguntas() -> lista de preguntas para entrevista
"""

import json
import random
from pathlib import Path
from typing import Any

# ─── Constantes ───────────────────────────────────────────────────────────────

PERSONAJES = [
    "Elias Vann",
    "Caterina",
    "Isabella",
    "Blanco Crema",
    "Don Fernando",
    "Elena Varela",
    "La Marquesa Isolda",
    "Will",
]

ARMAS = [
    "Pistola",
    "Trofeo",
    "Maceta",
    "Cizalla",
    "Manguera",
    "Almohada",
    "Cuchillo",
    "Abrecartas",
    "Candelabro",
    "Bate de Beisbol",
    "Puno Americano",
    "Veneno",
    "Martillo",
]

ESTANCIAS = [
    "Salon",
    "Dormitorio Principal",
    "Habitacion de Invitados",
    "Cocina",
    "Jardin",
    "Piscina",
    "Biblioteca",
    "Habitacion Oculta",
]

# La Habitacion Oculta esta dentro de la Biblioteca en el mapa del juego.
ESTANCIAS_VISITABLES = ESTANCIAS[:7]  # sin Habitacion Oculta

# ─── Preguntas de entrevista ───────────────────────────────────────────────────

PREGUNTAS_BASE = [
    "Donde estaba usted la noche del crimen?",
    "Noto algo extrano ultimamente en la mansion?",
    "Como describiria su relacion con la victima?",
    "Quien cree que pudo haber cometido este crimen?",
    "Vio u oyo algo sospechoso cerca de la hora del crimen?",
    "Conoce a alguien que quisiera hacer dano a la victima?",
    "Hay algo que no me este contando?",
    "Que opina de los otros invitados esta noche?",
    "Sabia usted de la existencia de alguna habitacion oculta en la mansion?",
    "La victima tenia enemigos? De que tipo?",
    "Ha notado algun comportamiento extrano en alguien esta noche?",
    "Donde estaba cada persona despues de la cena?",
    "Conoce el paradero exacto de la victima antes de su muerte?",
    "Que cree que ocurrio realmente esta noche?",
]


def cargar_preguntas() -> list[str]:
    """Devuelve la lista de preguntas disponibles para entrevistas."""
    return list(PREGUNTAS_BASE)


# ─── Generacion de misterio ────────────────────────────────────────────────────


def seleccionar_misterio(
    personajes: list[str],
    armas: list[str],
    estancias: list[str],
    preguntas: list[str],
) -> dict[str, Any]:
    """Genera aleatoriamente los parametros del misterio.

    Devuelve game_state con:
        asesino, complice, muerto, arma, habitacion,
        ubicaciones_personajes, ubicaciones_armas, preguntas_personajes
    """
    disponibles = list(personajes)
    random.shuffle(disponibles)

    muerto = disponibles[0]
    asesino = disponibles[1]
    # El complice no puede ser el asesino ni el muerto
    complice = disponibles[2]

    # Asignar ubicaciones a los 7 personajes vivos (excluye al muerto)
    vivos = [p for p in personajes if p != muerto]
    estancias_visitables = [e for e in estancias if e != "Habitacion Oculta"]
    ubicaciones_asignadas = list(estancias_visitables)
    random.shuffle(ubicaciones_asignadas)

    ubicaciones_personajes: dict[str, str] = {}
    for i, personaje in enumerate(vivos):
        ubicaciones_personajes[personaje] = ubicaciones_asignadas[i % len(ubicaciones_asignadas)]

    # Arma del crimen
    arma = random.choice(armas)

    # Escena del crimen: seleccionar entre las estancias visitables
    habitacion = random.choice(estancias_visitables)

    # Ubicar armas en distintas estancias
    ubicaciones_armas: dict[str, str] = {}
    armas_restantes = list(armas)
    random.shuffle(armas_restantes)
    # Repartir armas entre todas las estancias
    todas_estancias = list(estancias)  # incluye Habitacion Oculta
    for i, arma_item in enumerate(armas_restantes):
        ubicaciones_armas[arma_item] = todas_estancias[i % len(todas_estancias)]

    # Asignar preguntas a cada personaje vivo (4 por personaje)
    preguntas_personajes: dict[str, list[str]] = {}
    preguntas_disponibles = list(preguntas)
    random.shuffle(preguntas_disponibles)

    for personaje in vivos:
        # Tomar 4 preguntas sin repetir (o menos si no hay suficientes)
        if len(preguntas_disponibles) < 4:
            preguntas_disponibles = list(preguntas)
            random.shuffle(preguntas_disponibles)
        asignadas = preguntas_disponibles[:4]
        preguntas_disponibles = preguntas_disponibles[4:]
        preguntas_personajes[personaje] = asignadas

    return {
        "asesino": asesino,
        "complice": complice,
        "muerto": muerto,
        "arma": arma,
        "habitacion": habitacion,
        "ubicaciones_personajes": ubicaciones_personajes,
        "ubicaciones_armas": ubicaciones_armas,
        "preguntas_personajes": preguntas_personajes,
    }


def guardar_misterio_json(misterio: dict[str, Any], ruta: Path | None = None) -> None:
    """Guarda el misterio generado como JSON para referencia."""
    if ruta is None:
        ruta = Path(__file__).parent / "misterio_generado.json"
    ruta.write_text(
        json.dumps(misterio, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ─── Mapeos de utilidad ────────────────────────────────────────────────────────

# Nombres de personaje (espanol) -> ID interno del juego
PERSONAJE_A_ID: dict[str, str] = {
    "Elias Vann": "elias",
    "Caterina": "caterina",
    "Isabella": "isabella",
    "Blanco Crema": "blanco",
    "Don Fernando": "fernando",
    "Elena Varela": "elena",
    "La Marquesa Isolda": "isolda",
    "Will": "will",
}

# Nombre de estancia (espanol) -> ID interno del juego
ESTANCIA_A_ID: dict[str, str] = {
    "Salon": "salon",
    "Dormitorio Principal": "master_bedroom",
    "Habitacion de Invitados": "guest_quarters",
    "Cocina": "kitchen",
    "Jardin": "garden",
    "Piscina": "pool",
    "Biblioteca": "library",
    "Habitacion Oculta": "hidden_room",
}

# Nombre de arma (espanol) -> nombre interno (usado en WEAPON_DATA)
ARMA_A_INTERNO: dict[str, str] = {
    "Pistola": "Pistol",
    "Trofeo": "Trophy",
    "Maceta": "Flowerpot",
    "Cizalla": "Shears",
    "Manguera": "Hose",
    "Almohada": "Pillow",
    "Cuchillo": "Knife",
    "Abrecartas": "Letter Opener",
    "Candelabro": "Candelabra",
    "Bate de Beisbol": "Baseball Bat",
    "Puno Americano": "Brass Knuckles",
    "Veneno": "Poison",
    "Martillo": "Hammer",
}

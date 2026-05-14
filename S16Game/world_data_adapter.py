"""Adaptador de formato: convierte world_data.json al formato que espera script.rpy.

Traduce los datos generados por build_prompt.py al diccionario llm_data
que el juego Ren'Py utiliza para poblar dialogos, descripciones y pistas.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from randomizador import (
    ARMA_A_INTERNO,
    ESTANCIA_A_ID,
    PERSONAJE_A_ID,
)

# ─── Constantes ───────────────────────────────────────────────────────────────

NOMBRE_JUGADOR = "Detective"

# Textos de fallback por si faltan armas o resultados
FALLBACK_WEAPON_TEXT = "Examinas el arma con atencion. No parece haber nada fuera de lo comun."

FALLBACK_OUTCOMES: dict[str, str] = {
    "correct": (
        "Unes las piezas de la evidencia. Las contradicciones. Las pistas.\n\n"
        "Reunes a todos en el salon. Tus deducciones trazan una cadena irrefutable de acontecimientos.\n\n"
        "El asesino — confrontado con la verdad — finalmente se derrumba.\n\n"
        "\"Si. Lo hice.\" La confesion resuena por toda la mansion silenciosa.\n\n"
        "Se hace justicia. El caso esta cerrado."
    ),
    "wrong_murderer": (
        "Presentas tu acusacion con confianza.\n\n"
        "Pero la persona que has nombrado da un paso al frente con una coartada solida — corroborada por otros dos testigos.\n\n"
        "La sala queda en silencio. Sientes cada par de ojos sobre ti.\n\n"
        "Vuelta a la investigacion. El verdadero asesino sigue en esta casa."
    ),
    "wrong_weapon": (
        "Levantas la supuesta arma del crimen.\n\n"
        "El forense niega con la cabeza. \"El patron de la herida no coincide. Ni de lejos.\"\n\n"
        "Un murmullo recorre la sala. Tu teoria se desmorona.\n\n"
        "Debes reconsiderar las pruebas."
    ),
    "wrong_location": (
        "Declaras la escena del crimen con autoridad.\n\n"
        "Pero algo no cuadra. Las pruebas fisicas no coinciden con tu teoria.\n\n"
        "\"Detective, ¿esta seguro?\" Alguien pregunta. La duda en su voz es inconfundible.\n\n"
        "Te equivocaste sobre donde ocurrio. ¿En que mas te habras equivocado?"
    ),
    "wrong_accomplice": (
        "Señalas al supuesto complice.\n\n"
        "El acusado parece genuinamente desconcertado — y varios testigos confirman su paradero.\n\n"
        "Puede que aun haya una conspiracion... pero esta persona no forma parte de ella.\n\n"
        "La investigacion debe continuar."
    ),
    "all_wrong": (
        "Tu acusacion se desmorona casi de inmediato.\n\n"
        "Cada elemento — sospechoso, arma, lugar, complice — es contradicho por las pruebas.\n\n"
        "Los invitados intercambian miradas inquietas. Su confianza en ti se ha evaporado.\n\n"
        "Has fallado. El asesino queda libre, y el oscuro secreto de la mansion permanece enterrado."
    ),
}


# ─── Funcion principal de adaptacion ──────────────────────────────────────────


def adaptar_world_data(world_data: dict[str, Any]) -> dict[str, Any]:
    """Convierte world_data (formato build_prompt.py) a llm_data (formato juego).

    El diccionario devuelto tiene las claves:
        opening_narrative, locations, npcs, weapons, accusation_outcomes
    """
    return {
        "opening_narrative": _adaptar_intro(world_data),
        "locations": _adaptar_habitaciones(world_data),
        "npcs": _adaptar_personajes(world_data),
        "weapons": _adaptar_armas(world_data),
        "accusation_outcomes": _adaptar_resultados(world_data),
    }


def cargar_y_adaptar(ruta_world_data: str | Path) -> dict[str, Any]:
    """Carga world_data.json desde disco y devuelve llm_data listo para el juego."""
    with open(ruta_world_data, "r", encoding="utf-8") as f:
        world_data = json.load(f)
    return adaptar_world_data(world_data)


# ─── Adaptadores individuales ─────────────────────────────────────────────────


def _adaptar_intro(world_data: dict[str, Any]) -> str:
    intro = world_data.get("intro", "")
    if not intro:
        return "Es tarde en la noche. La lluvia cae a cantaros. Un crimen ha ocurrido en la mansion Montemayor."
    return intro


def _adaptar_habitaciones(world_data: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Convierte la lista de habitaciones a un dict claveado por ID interno del juego."""
    locations: dict[str, dict[str, str]] = {}
    habitaciones = world_data.get("habitaciones", [])

    for hab in habitaciones:
        nombre_es = hab.get("nombre", "")
        loc_id = ESTANCIA_A_ID.get(nombre_es)
        if loc_id is None:
            continue

        # Descripcion: combinar descripcion ambiental + cuerpo (si existe)
        descripcion = hab.get("descripcion", "")
        cuerpo = hab.get("cuerpo")
        if cuerpo:
            descripcion += "\n\n" + cuerpo

        # Añadir placeholder para NPC presente
        descripcion += "\n\nVes a [npc_here_name] aqui."

        # Pista: combinar todos los objetos inspeccionables
        objetos = hab.get("objetos", [])
        if objetos:
            pista = "Examinas la habitacion detenidamente:\n\n"
            for obj in objetos:
                nombre_obj = obj.get("nombre", "")
                desc_obj = obj.get("descripcion", "")
                pista += f"- {nombre_obj}: {desc_obj}\n"
        else:
            pista = "No encuentras nada significativo."

        locations[loc_id] = {
            "description": descripcion,
            "clue": pista,
        }

    return locations


def _adaptar_personajes(world_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Convierte la lista de personajes a un dict claveado por ID interno del juego."""
    npcs: dict[str, dict[str, Any]] = {}
    personajes = world_data.get("personajes", [])

    for pj in personajes:
        nombre_es = pj.get("nombre", "")
        npc_id = PERSONAJE_A_ID.get(nombre_es)
        if npc_id is None:
            continue

        mood = pj.get("primera_impresion", "")
        respuestas = pj.get("respuestas", {})

        # Convertir {pregunta: respuesta} a [{"question": ..., "answer": ...}]
        dialogues = []
        for pregunta, respuesta in respuestas.items():
            dialogues.append({
                "question": pregunta,
                "answer": respuesta,
            })

        # El juego espera exactamente 4 dialogos. Rellenar con fallback si faltan.
        while len(dialogues) < 4:
            dialogues.append({
                "question": "Hay algo mas que quiera decirme?",
                "answer": "Por ahora no, detective. Tengo que pensar.",
            })

        npcs[npc_id] = {
            "mood": mood,
            "dialogues": dialogues,
        }

    return npcs


def _adaptar_armas(world_data: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Convierte la lista de armas a un dict claveado por nombre interno del juego."""
    weapons: dict[str, dict[str, str]] = {}
    armas = world_data.get("armas", [])

    for arma in armas:
        if isinstance(arma, dict):
            nombre_es = arma.get("nombre", "")
            texto = arma.get("texto_inspeccion", FALLBACK_WEAPON_TEXT)
        else:
            continue

        nombre_interno = ARMA_A_INTERNO.get(nombre_es)
        if nombre_interno is None:
            continue

        weapons[nombre_interno] = {"inspect_text": texto}

    # Rellenar armas faltantes con texto generico
    for nombre_es, nombre_interno in ARMA_A_INTERNO.items():
        if nombre_interno not in weapons:
            weapons[nombre_interno] = {"inspect_text": FALLBACK_WEAPON_TEXT}

    return weapons


def _adaptar_resultados(world_data: dict[str, Any]) -> dict[str, str]:
    """Adapta los textos de resultado de acusacion, rellenando los que falten."""
    resultados = world_data.get("resultados_acusacion", {})
    if not isinstance(resultados, dict):
        resultados = {}

    merged: dict[str, str] = dict(FALLBACK_OUTCOMES)
    for clave in FALLBACK_OUTCOMES:
        if clave in resultados and resultados[clave]:
            merged[clave] = resultados[clave]

    return merged

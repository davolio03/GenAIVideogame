import json
import os
import re
from pathlib import Path
from typing import Any

from api import MercuryAPIError, ask_mercury
from randomizador import (
    ARMA_A_INTERNO,
    ARMAS,
    ESTANCIA_A_ID,
    ESTANCIAS,
    PERSONAJE_A_ID,
    PERSONAJES,
    cargar_preguntas,
    guardar_misterio_json,
    seleccionar_misterio,
)


CARPETA_PROYECTO = Path(__file__).parent
RUTA_PERSONAJES = CARPETA_PROYECTO / "Personajes.md"
RUTA_WORLD_DATA = CARPETA_PROYECTO / "world_data.json"
RUTA_ULTIMA_RESPUESTA = CARPETA_PROYECTO / "last_mercury_response.txt"


def guardar_respuesta_mercury(texto: str) -> None:
    separador = "\n\n" + "=" * 80 + "\n\n"
    with RUTA_ULTIMA_RESPUESTA.open("a", encoding="utf-8") as archivo:
        if RUTA_ULTIMA_RESPUESTA.stat().st_size > 0:
            archivo.write(separador)
        archivo.write(texto)


def limpiar_json_respuesta(texto: str) -> Any:
    guardar_respuesta_mercury(texto)

    limpio = re.sub(r"```json\s*", "", texto)
    limpio = re.sub(r"```\s*", "", limpio).strip()

    try:
        return json.loads(limpio)
    except json.JSONDecodeError:
        inicio = limpio.find("{")
        fin = limpio.rfind("}")
        if inicio == -1 or fin == -1:
            raise
        try:
            return json.loads(limpio[inicio : fin + 1])
        except json.JSONDecodeError as segundo_error:
            raise ValueError(
                "Mercury devolvio JSON invalido. "
                f"Respuesta guardada en {RUTA_ULTIMA_RESPUESTA}"
            ) from segundo_error


def llamar_mercury_json(
    user_prompt: str,
    *,
    system_prompt: str,
    max_tokens: int = 6000,
    temperature: float = 0.6,
) -> Any:
    ultimo_error: Exception | None = None

    for intento in range(1, 4):
        try:
            respuesta = ask_mercury(
                user_prompt,
                system_prompt=(
                    f"{system_prompt}\n"
                    "IMPORTANTE: devuelve JSON valido, compacto y cerrado. "
                    "No escribas frases largas. No dejes strings sin cerrar."
                ),
                temperature=temperature,
                max_tokens=max_tokens,
                response_mime_type="application/json",
            )
            return limpiar_json_respuesta(respuesta)
        except MercuryAPIError as error:
            ultimo_error = error
            print(f"Error de Mercury. Reintentando ({intento}/3): {error}")
        except (json.JSONDecodeError, ValueError) as error:
            ultimo_error = error
            print(f"Respuesta JSON invalida. Reintentando ({intento}/3)...")

    raise ValueError(
        "Mercury devolvio JSON invalido despues de 3 intentos. "
        f"Ultima respuesta guardada en {RUTA_ULTIMA_RESPUESTA}"
    ) from ultimo_error


def cargar_fichas_personajes() -> dict[str, str]:
    contenido = RUTA_PERSONAJES.read_text(encoding="utf-8")
    bloques = re.split(r"(?=^## .+$)", contenido, flags=re.MULTILINE)
    fichas: dict[str, str] = {}

    for bloque in bloques:
        match = re.match(r"^##\s+(.+)$", bloque.strip(), flags=re.MULTILINE)
        if not match:
            continue
        titulo = match.group(1).strip()
        fichas[titulo] = bloque.strip()

    return fichas


def buscar_ficha(personaje: str, fichas: dict[str, str]) -> str:
    if personaje in fichas:
        return fichas[personaje]

    for titulo, ficha in fichas.items():
        if personaje in titulo or titulo in personaje:
            return ficha

    nombre_base = personaje.split("/")[0].strip()
    for titulo, ficha in fichas.items():
        if nombre_base in titulo or titulo in nombre_base:
            return ficha

    return f"## {personaje}\nNo hay ficha especifica. Mantener tono coherente y sobrio."


def rol_de_personaje(personaje: str, game_state: dict[str, Any]) -> str:
    if personaje == game_state["asesino"]:
        return "ASESINO"
    if personaje == game_state["complice"]:
        return "COMPLICE"
    if personaje == game_state["muerto"]:
        return "MUERTO"
    return "INOCENTE"


def personajes_en_habitacion(game_state: dict[str, Any], habitacion: str) -> list[str]:
    return [
        personaje
        for personaje, ubicacion in game_state["ubicaciones_personajes"].items()
        if ubicacion == habitacion
    ]


def armas_en_habitacion(game_state: dict[str, Any], habitacion: str) -> list[str]:
    return [
        arma
        for arma, ubicacion in game_state["ubicaciones_armas"].items()
        if ubicacion == habitacion
    ]


def canon_basico(game_state: dict[str, Any]) -> dict[str, Any]:
    return {
        "muerto": game_state["muerto"],
        "asesino": game_state["asesino"],
        "complice": game_state["complice"],
        "arma": game_state["arma"],
        "habitacion": game_state["habitacion"],
        "ubicaciones_personajes": game_state["ubicaciones_personajes"],
        "ubicaciones_armas": game_state["ubicaciones_armas"],
    }


def generar_misterio() -> dict[str, Any]:
    preguntas = cargar_preguntas()
    misterio = seleccionar_misterio(PERSONAJES, ARMAS, ESTANCIAS, preguntas)
    guardar_misterio_json(misterio)
    return misterio


def generar_intro_y_mapa(game_state: dict[str, Any]) -> dict[str, Any]:
    system_prompt = """Eres disenador narrativo de un juego tipo Cluedo.
Genera solo JSON valido. No uses markdown.
Tu objetivo es crear una intro y un mapa privado de coherencia para que otras llamadas generen habitaciones y dialogos sin contradicciones."""

    user_prompt = f"""ESTADO SECRETO:
{json.dumps(canon_basico(game_state), ensure_ascii=False, indent=2)}

Genera exactamente este JSON:
{{
  "intro": "Parrafo inicial para el jugador. No reveles solucion.",
  "mapa_pistas": {{
    "descripcion": "Camino privado para deducir asesino, arma y habitacion."
  }}
}}
"""

    intro_y_mapa = llamar_mercury_json(user_prompt, system_prompt=system_prompt, max_tokens=1200)
    mapa_pistas = intro_y_mapa.get("mapa_pistas", {})
    intro_y_mapa["mapa_pistas"] = {"descripcion": mapa_pistas.get("descripcion", "")}
    return intro_y_mapa


def generar_habitacion(
    habitacion: str,
    game_state: dict[str, Any],
    mapa_pistas: dict[str, Any],
) -> dict[str, Any]:
    datos_habitacion = {
        "nombre": habitacion,
        "es_habitacion_crimen": habitacion == game_state["habitacion"],
        "muerto": game_state["muerto"] if habitacion == game_state["habitacion"] else None,
        "personajes_presentes": personajes_en_habitacion(game_state, habitacion),
        "armas_presentes": armas_en_habitacion(game_state, habitacion),
        "arma_crimen": game_state["arma"],
    }

    system_prompt = """Eres disenador de escenarios para un juego de misterio.
Genera solo JSON valido. No uses markdown.
No reveles directamente el arma del crimen ni el asesino. Las pistas deben ser implicitas y coherentes con el mapa privado."""

    user_prompt = f"""CANON SECRETO:
{json.dumps(canon_basico(game_state), ensure_ascii=False, indent=2)}

MAPA PRIVADO DE COHERENCIA:
{json.dumps(mapa_pistas, ensure_ascii=False, indent=2)}

DATOS DE ESTA HABITACION:
{json.dumps(datos_habitacion, ensure_ascii=False, indent=2)}

Genera exactamente este JSON:
{{
  "nombre": "{habitacion}",
  "descripcion": "Descripcion de la habitacion al entrar.",
  "cuerpo": "Descripcion del cuerpo solo si corresponde; si no, null.",
  "objetos": [
    {{
      "nombre": "Nombre exacto del objeto presente",
      "descripcion": "Descripcion inspeccionable con posibles pistas implicitas."
    }}
  ]
}}
"""

    habitacion_generada = llamar_mercury_json(
        user_prompt, system_prompt=system_prompt, max_tokens=1500
    )
    habitacion_generada["nombre"] = habitacion
    habitacion_generada.setdefault("descripcion", "")
    habitacion_generada.setdefault("cuerpo", None)
    habitacion_generada.setdefault("objetos", [])
    return habitacion_generada


def generar_personaje(
    personaje: str,
    game_state: dict[str, Any],
    mapa_pistas: dict[str, Any],
    ficha_personaje: str,
) -> dict[str, Any]:
    preguntas = game_state["preguntas_personajes"].get(personaje, [])
    datos_personaje = {
        "nombre": personaje,
        "rol_secreto": rol_de_personaje(personaje, game_state),
        "habitacion_inicial": game_state["ubicaciones_personajes"][personaje],
        "preguntas_asignadas": preguntas,
    }

    system_prompt = """Eres guionista de dialogos para un juego de misterio.
Genera solo JSON valido. No uses markdown.
ANTI-ALUCINACION:
- Usa solo datos del canon, el mapa privado y la ficha del personaje.
- No inventes nuevas habitaciones, personajes, armas ni preguntas.
- Responde todas y solo las preguntas asignadas, copiando la pregunta exacta como clave.
- Mantene la personalidad de la ficha en cada respuesta.
- El asesino y el complice pueden mentir, pero sus mentiras deben coincidir con el mapa privado.
- Los inocentes no mienten sobre el crimen, pero pueden ocultar un secreto menor."""

    user_prompt = f"""CANON SECRETO:
{json.dumps(canon_basico(game_state), ensure_ascii=False, indent=2)}

MAPA PRIVADO DE COHERENCIA:
{json.dumps(mapa_pistas, ensure_ascii=False, indent=2)}

DATOS DEL PERSONAJE:
{json.dumps(datos_personaje, ensure_ascii=False, indent=2)}

FICHA DEL PERSONAJE:
{ficha_personaje}

Genera exactamente este JSON:
{{
  "nombre": "{personaje}",
  "primera_impresion": "Como lo encuentra el jugador. Debe reflejar su personalidad.",
  "respuestas": {{
    "pregunta exacta asignada": "Respuesta de 2-4 frases, coherente con rol, canon y personalidad."
  }}
}}
"""

    personaje_generado = llamar_mercury_json(
        user_prompt, system_prompt=system_prompt, max_tokens=2500
    )
    personaje_generado["nombre"] = personaje
    personaje_generado.setdefault("primera_impresion", "")
    personaje_generado.setdefault("respuestas", {})
    return personaje_generado


def generar_armas(
    game_state: dict[str, Any],
    mapa_pistas: dict[str, Any],
) -> list[dict[str, Any]]:
    """Genera textos de inspeccion para cada una de las 13 armas."""
    system_prompt = """Eres perito forense en un juego de misterio.
Genera solo JSON valido. No uses markdown.
El arma del crimen debe mostrar pistas forenses contundentes. Las demas armas deben tener descripciones normales pero con algun detalle intrigante menor."""

    canon = canon_basico(game_state)
    arma_asesina = canon["arma"]
    # Solo pasamos las armas que existen en el canon (lista de ARMAS)
    armas_a_generar = list(ARMAS)

    user_prompt = f"""CANON SECRETO:
{json.dumps(canon, ensure_ascii=False, indent=2)}

MAPA PRIVADO:
{json.dumps(mapa_pistas, ensure_ascii=False, indent=2)}

Arma del crimen: {arma_asesina}

Genera un array JSON con texto de inspeccion para cada una de estas armas:
{json.dumps(armas_a_generar, ensure_ascii=False)}

Formato exacto:
[
  {{{{
    "nombre": "Nombre exacto del arma",
    "texto_inspeccion": "2-3 frases. Si es el arma del crimen, incluye detalles forenses contundentes. Si no, describe el arma con un detalle intrigante menor."
  }}}}
]

IMPORTANTE: genera todas las armas de la lista, sin excepcion."""
    user_prompt = user_prompt.replace("{{{{", "{").replace("}}}}", "}")

    armas_generadas = llamar_mercury_json(
        user_prompt, system_prompt=system_prompt, max_tokens=2500
    )

    if not isinstance(armas_generadas, list):
        raise ValueError("La API no devolvio un array de armas.")

    for i, arma in enumerate(armas_generadas):
        if isinstance(arma, dict) and "nombre" not in arma:
            arma["nombre"] = ARMAS[i] if i < len(ARMAS) else f"Arma {i}"

    return armas_generadas


def generar_resultados_acusacion(
    game_state: dict[str, Any],
    mapa_pistas: dict[str, Any],
) -> dict[str, str]:
    """Genera los textos para cada resultado posible de la acusacion final."""
    system_prompt = """Eres narrador de un juego de misterio estilo Cluedo.
Genera solo JSON valido. No uses markdown.
Cada texto describe el desenlace de una acusacion. Estilo dramatico, espanol sobrio."""

    canon = canon_basico(game_state)

    user_prompt = f"""CANON SECRETO:
{json.dumps(canon, ensure_ascii=False, indent=2)}

MAPA PRIVADO:
{json.dumps(mapa_pistas, ensure_ascii=False, indent=2)}

Genera exactamente este JSON con textos dramaticos (2-4 frases cada uno):
{{{{
  "correcto": "Cuando TODOS los elementos son correctos: asesino, complice, arma y lugar. El detective resuelve el caso. Final triunfal.",
  "asesino_incorrecto": "Cuando el ASESINO elegido es incorrecto. La persona acusada tiene coartada solida.",
  "arma_incorrecta": "Cuando el ARMA elegida es incorrecta. La evidencia forense no coincide.",
  "lugar_incorrecto": "Cuando el LUGAR elegido es incorrecto. Las pruebas fisicas contradicen la teoria.",
  "complice_incorrecto": "Cuando el COMPLICE elegido es incorrecto. La persona muestra desconcierto genuino.",
  "todo_incorrecto": "Cuando TODO es incorrecto. Fracaso total. El asesino queda libre."
}}}}
"""
    user_prompt = user_prompt.replace("{{{{", "{").replace("}}}}", "}")

    resultados = llamar_mercury_json(
        user_prompt, system_prompt=system_prompt, max_tokens=1500
    )

    # Normalizar claves al formato esperado por el juego
    mapeo_claves = {
        "correcto": "correct",
        "asesino_incorrecto": "wrong_murderer",
        "arma_incorrecta": "wrong_weapon",
        "lugar_incorrecto": "wrong_location",
        "complice_incorrecto": "wrong_accomplice",
        "todo_incorrecto": "all_wrong",
    }

    normalizado: dict[str, str] = {}
    for clave_llm, clave_juego in mapeo_claves.items():
        normalizado[clave_juego] = resultados.get(clave_llm, "Tu acusacion ha sido registrada. Pero la verdad sigue siendo esquiva.")

    return normalizado


def validar_world_data(world_data: dict[str, Any], game_state: dict[str, Any]) -> None:
    personajes_vivos = set(game_state["preguntas_personajes"].keys())
    personajes = world_data.get("personajes", [])
    for indice, personaje in enumerate(personajes):
        if "nombre" not in personaje:
            raise ValueError(f"Personaje generado sin nombre en indice {indice}: {personaje}")
    generados = {p["nombre"] for p in personajes}

    faltantes = personajes_vivos - generados
    if faltantes:
        raise ValueError(f"Faltan personajes en world_data: {sorted(faltantes)}")

    habitaciones_esperadas = set(game_state["ubicaciones_personajes"].values()) | set(
        game_state["ubicaciones_armas"].values()
    )
    habitaciones = world_data.get("habitaciones", [])
    for indice, habitacion in enumerate(habitaciones):
        if "nombre" not in habitacion:
            raise ValueError(f"Habitacion generada sin nombre en indice {indice}: {habitacion}")
    habitaciones_generadas = {h["nombre"] for h in habitaciones}

    faltan_habitaciones = habitaciones_esperadas - habitaciones_generadas
    if faltan_habitaciones:
        raise ValueError(f"Faltan habitaciones en world_data: {sorted(faltan_habitaciones)}")


def generar_world_data(output_path: Path = RUTA_WORLD_DATA) -> dict[str, Any]:
    _lock_path = CARPETA_PROYECTO / ".generating.lock"
    _lock_path.write_text(str(os.getpid()))

    RUTA_ULTIMA_RESPUESTA.write_text("", encoding="utf-8")
    game_state = generar_misterio()
    fichas = cargar_fichas_personajes()

    print("Fase 1/5: intro y mapa de pistas...")
    intro_y_mapa = generar_intro_y_mapa(game_state)
    mapa_pistas = intro_y_mapa["mapa_pistas"]

    habitaciones = sorted(
        set(game_state["ubicaciones_personajes"].values())
        | set(game_state["ubicaciones_armas"].values())
    )

    print("Fase 2/5: habitaciones...")
    habitaciones_generadas = []
    for habitacion in habitaciones:
        print(f"  - {habitacion}")
        habitaciones_generadas.append(generar_habitacion(habitacion, game_state, mapa_pistas))

    print("Fase 3/5: personajes...")
    personajes_generados = []
    for personaje in game_state["preguntas_personajes"]:
        print(f"  - {personaje}")
        ficha = buscar_ficha(personaje, fichas)
        personajes_generados.append(
            generar_personaje(personaje, game_state, mapa_pistas, ficha)
        )

    print("Fase 4/5: armas...")
    armas_generadas = generar_armas(game_state, mapa_pistas)

    print("Fase 5/5: resultados de acusacion...")
    resultados_acusacion = generar_resultados_acusacion(game_state, mapa_pistas)

    parametros = {
        "victima": game_state["muerto"],
        "victima_id": PERSONAJE_A_ID.get(game_state["muerto"], ""),
        "asesino": game_state["asesino"],
        "asesino_id": PERSONAJE_A_ID.get(game_state["asesino"], ""),
        "complice": game_state["complice"],
        "complice_id": PERSONAJE_A_ID.get(game_state["complice"], ""),
        "arma": game_state["arma"],
        "arma_id": ARMA_A_INTERNO.get(game_state["arma"], ""),
        "escena": game_state["habitacion"],
        "escena_id": ESTANCIA_A_ID.get(game_state["habitacion"], ""),
        "ubicaciones_personajes": game_state["ubicaciones_personajes"],
        "ubicaciones_armas": game_state["ubicaciones_armas"],
        "preguntas_personajes": game_state["preguntas_personajes"],
    }

    world_data = {
        "intro": intro_y_mapa["intro"],
        "habitaciones": habitaciones_generadas,
        "personajes": personajes_generados,
        "armas": armas_generadas,
        "resultados_acusacion": resultados_acusacion,
        "mapa_pistas": mapa_pistas,
        "parametros": parametros,
    }

    validar_world_data(world_data, game_state)

    # Atomic write: temp file first, then rename (prevents corruption)
    _tmp_path = output_path.with_suffix(".json.tmp")
    _tmp_path.write_text(
        json.dumps(world_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _tmp_path.replace(output_path)
    print(f"World data guardado en: {output_path}")

    # Clean up lock file
    try:
        _lock_path.unlink(missing_ok=True)
    except Exception:
        pass

    return world_data


if __name__ == "__main__":
    generar_world_data()


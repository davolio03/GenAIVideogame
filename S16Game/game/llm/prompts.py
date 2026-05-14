SYSTEM_PROMPT = """Eres el Director de Juego de una novela visual de misterio y asesinato. Tu tarea es generar contenido COMPLETO del juego basado en los parametros del caso proporcionados. Cada vez que generes contenido, debes crear una historia DIFERENTE y UNICA — nunca repitas las mismas descripciones, dialogos o pistas entre una partida y otra.

## Ambientacion
- Epoca: Noche cerrada, tormenta con lluvia torrencial
- Lugar: Una mansion señorial con 8 habitaciones
- Victima: Don Alejandro Montemayor, un adinerado magnate
- El jugador es un detective investigando el asesinato
- Todos los textos deben estar en ESPAÑOL

## Formato de Salida
Devuelve SOLAMENTE un objeto JSON valido (sin markdown, sin explicaciones). El JSON debe seguir esta estructura exacta:

{
  "opening_narrative": "string — texto de apertura (2-3 parrafos)",
  "locations": {
    "salon": {"description": "string — descripcion de la habitacion + linea de presencia del NPC con marcador {npc_name}", "clue": "string — lo que el detective encuentra al examinar esta habitacion"},
    "master_bedroom": {"description": "string", "clue": "string"},
    "guest_quarters": {"description": "string", "clue": "string"},
    "kitchen": {"description": "string", "clue": "string"},
    "garden": {"description": "string", "clue": "string"},
    "pool": {"description": "string", "clue": "string"},
    "library": {"description": "string", "clue": "string"},
    "hidden_room": {"description": "string — esta habitacion es un cuarto secreto detras de una estanteria en la biblioteca, paredes cubiertas de fotos e hilos rojos", "clue": "string"}
  },
  "npcs": {
    "elias": {"mood": "string — estado emocional del NPC en español", "dialogues": [{"question": "string", "answer": "string"}, ... 4 en total]},
    "caterina": {"mood": "string", "dialogues": [{"question": "string", "answer": "string"}, ... 4 en total]},
    "isabella": {"mood": "string", "dialogues": [{"question": "string", "answer": "string"}, ... 4 en total]},
    "blanco": {"mood": "string", "dialogues": [{"question": "string", "answer": "string"}, ... 4 en total]},
    "fernando": {"mood": "string", "dialogues": [{"question": "string", "answer": "string"}, ... 4 en total]},
    "elena": {"mood": "string", "dialogues": [{"question": "string", "answer": "string"}, ... 4 en total]},
    "isolda": {"mood": "string", "dialogues": [{"question": "string", "answer": "string"}, ... 4 en total]},
    "will": {"mood": "string", "dialogues": [{"question": "string", "answer": "string"}, ... 4 en total]}
  },
  "weapons": {
    "Pistol": {"inspect_text": "string"},
    "Trophy": {"inspect_text": "string"},
    "Flowerpot": {"inspect_text": "string"},
    "Shears": {"inspect_text": "string"},
    "Hose": {"inspect_text": "string"},
    "Pillow": {"inspect_text": "string"},
    "Knife": {"inspect_text": "string"},
    "Letter Opener": {"inspect_text": "string"},
    "Candelabra": {"inspect_text": "string"},
    "Baseball Bat": {"inspect_text": "string"},
    "Brass Knuckles": {"inspect_text": "string"},
    "Poison": {"inspect_text": "string"},
    "Hammer": {"inspect_text": "string"}
  },
  "accusation_outcomes": {
    "correct": "string — texto de victoria cuando las 4 elecciones son correctas",
    "wrong_murderer": "string — cuando el asesino es incorrecto",
    "wrong_weapon": "string — cuando el arma es incorrecta",
    "wrong_location": "string — cuando la ubicacion es incorrecta",
    "wrong_accomplice": "string — cuando el complice es incorrecto",
    "all_wrong": "string — cuando todo es incorrecto"
  }
}
"""


def build_case_prompt(victim_name, murderer_name, weapon_name, crime_scene_name,
                      accomplice_name, npc_data, npc_location):
    """Build the user prompt with case parameters injected. All in Spanish."""

    # Build NPC profile list
    npc_lines = []
    for nid, nname, _ in npc_data:
        loc = npc_location.get(nid, "unknown")
        role_desc = _get_npc_role(nid, nname, loc)
        npc_lines.append(role_desc)

    location_names = {
        "salon": "Salon", "master_bedroom": "Dormitorio Principal",
        "guest_quarters": "Habitacion de Invitados", "kitchen": "Cocina",
        "garden": "Jardin", "pool": "Piscina",
        "library": "Biblioteca", "hidden_room": "Habitacion Oculta (cuarto secreto tras la estanteria)"
    }

    return """## Parametros del Caso (GENERADOS ALEATORIAMENTE — NO LOS CAMBIES)

**Victima:** {victim} (la persona fallecida — este NPC NO aparece en el juego)
**Asesino:** {murderer}
**Arma del Crimen:** {weapon}
**Escena del Crimen:** {scene}
**Complice:** {accomplice}

## Perfiles de los NPC (sobrevivientes — cada uno en su ubicacion actual)

{npc_profiles}

## Reglas de Resaltado en Rojo

Usa etiquetas <red>...</red> para marcar palabras/frases que deben aparecer en ROJO en el juego. Son vitales para la jugabilidad — son las pistas que el jugador debe notar.

**Reglas de colocacion de etiquetas:**
- Respuestas del asesino: 1-2 etiquetas <red> por respuesta. Deben revelar contradicciones, fallos en la coartada, explicaciones excesivas o inconsistencias factuales que un detective perspicaz detectaria.
- Respuestas del complice: 1-2 etiquetas <red> por respuesta. Deben revelar lenguaje encubridor, respuestas ensayadas, evasion de temas o conocimiento que no deberian tener.
- Escena del crimen (la habitacion donde ocurrio el asesinato): 2-3 etiquetas <red> en AMBOS campos description Y clue. Deben ser pistas forenses (patrones de sangre, signos de lucha, objetos desplazados).
- inspect_text del arma del crimen: 1-2 etiquetas <red>. Hallazgos forenses clave (huellas, marcas de desgaste, residuos).
- Respuestas de NPC inocentes: 0-1 etiquetas <red> como maximo. Pueden ser observaciones veraces y utiles — no pistas falsas.
- Ubicaciones que NO son la escena del crimen: 0-1 etiquetas <red>. Pistas secundarias como maximo.
- Cada etiqueta <red>: 2-8 palabras solamente. Sin anidamiento. Sin fragmentos de multiples oraciones.

**Ejemplos de etiquetas rojas:**
- Correcto: "Estuve en la <red>biblioteca toda la noche</red> leyendo."
- Correcto: "La <red>empunadura tiene rasgunos recientes</red> cerca de la guarda."
- INCORRECTO: "Estaba <red>en la biblioteca</red> y luego <red>fui a la cocina</red>." (demasiadas etiquetas en una respuesta — max 2)
- INCORRECTO: "El <red>candelabro. Era pesado y de bronce y el brazo</red> estaba doblado." (etiqueta demasiado larga — mantenla en 2-8 palabras)

## Directrices Adicionales

- Haz que el misterio sea coherente. El motivo del asesino debe conectar con las pistas en sus dialogos.
- Las 4 preguntas de cada NPC deben sentirse como un interrogatorio natural de detective. Las preguntas deben indagar sobre: coartada, relaciones, observaciones, sospechas.
- Las respuestas deben ser de 2-4 oraciones. Da a los NPC voces distintivas y personalidades unicas.
- La escena del crimen debe sentirse como el corazon de la investigacion.
- La habitacion oculta contiene evidencia que conecta con el asesino.
- El complice debe proteger sutilmente al asesino en sus respuestas, sin ser obvio.
- Haz que los resaltados <red> se sientan organicos — no forzados. Deben ser el tipo de detalle que un jugador podria pasar por alto si no presta atencion.
- **IMPORTANTE: Cada partida debe ser DIFERENTE.** No repitas las mismas frases, descripciones o pistas. Inventa nuevos dialogos, nuevas pistas, nuevas dinamicas entre personajes. Cambia los motivos, las coartadas, los secretos. Se creativo e impredecible.
- Todos los textos deben estar en ESPAÑOL, incluyendo preguntas, respuestas, descripciones y estados de animo.

## Nombres de Ubicaciones para Referencia
{location_ref}

Genera el JSON completo ahora. Emite SOLAMENTE el objeto JSON.""".format(
        victim=victim_name,
        murderer=murderer_name,
        weapon=weapon_name,
        scene=crime_scene_name,
        accomplice=accomplice_name,
        npc_profiles="\n".join(npc_lines),
        location_ref="\n".join("- {}: {}".format(k, v) for k, v in location_names.items())
    )


def _get_npc_role(nid, nname, loc):
    """Get a brief role description for each NPC ID. In Spanish."""
    roles = {
        "elias":     "- **Elias Vann** (elias): Mayordomo desde hace 20 anios. Actualmente en: {}".format(loc),
        "caterina":  "- **Caterina** (caterina): La viuda de la victima. Actualmente en: {}".format(loc),
        "isabella":  "- **Isabella** (isabella): La hija de la victima. Actualmente en: {}".format(loc),
        "blanco":    "- **Blanco Crema** (blanco): Invitado con asuntos pendientes. Actualmente en: {}".format(loc),
        "fernando":  "- **Don Fernando** (fernando): Noble, socio comercial. Actualmente en: {}".format(loc),
        "elena":     "- **Elena Varela** (elena): Consultora de arte. Actualmente en: {}".format(loc),
        "isolda":    "- **La Marquesa Isolda** (isolda): Marquesa, vieja amiga de la victima. Actualmente en: {}".format(loc),
        "will":      "- **Will** (will): Amigo de la familia que oyo una discusion. Actualmente en: {}".format(loc),
    }
    return roles.get(nid, "- **{}** ({})".format(nname, nid))

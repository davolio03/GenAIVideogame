# Audio
define audio.bgm1 = "audio/Clave_de_Humo.mp3"
define audio.bgm2 = "audio/La_Mansion_Cerrada_1.mp3"
define audio.bgm3 = "audio/La_Mansion_Cerrada_2.mp3"

init python:
    def play_random_bgm():
        tracks = ["audio/Clave_de_Humo.mp3", "audio/La_Mansion_Cerrada_1.mp3", "audio/La_Mansion_Cerrada_2.mp3"]
        renpy.music.play(renpy.random.choice(tracks))

# Character definitions
define detective = Character("Detective", color="#c8c8ff")

define elias = Character("Elias Vann", color="#ffcc99")
define caterina = Character("Caterina", color="#ff9999")
define isabella = Character("Isabella", color="#ff99cc")
define blanco = Character("Blanco Crema", color="#cc99ff")
define fernando = Character("Don Fernando", color="#99ccff")
define elena = Character("Elena Varela", color="#99ff99")
define isolda = Character("La Marquesa Isolda", color="#ffcc66")
define will = Character("Will", color="#cccc99")

# Portrait images
image elias_portrait = "images/sprites/Elias Vann.png"
image caterina_portrait = "images/sprites/Caterina .png"
image isabella_portrait = "images/sprites/Isabella.png"
image blanco_portrait = "images/sprites/Blanco Crema.png"
image fernando_portrait = "images/sprites/Don Fernando.png"
image elena_portrait = "images/sprites/Elena Varela.png"
image isolda_portrait = "images/sprites/La marquesa Isolda.png"
image will_portrait = "images/sprites/Will.png"

# Narrator
define narrator = Character(None)

# NPC data for randomization: (id, display_name, portrait_path)
define NPC_DATA = [
    ("elias", "Elias Vann", "images/sprites/Elias Vann.png"),
    ("caterina", "Caterina", "images/sprites/Caterina .png"),
    ("isabella", "Isabella", "images/sprites/Isabella.png"),
    ("blanco", "Blanco Crema", "images/sprites/Blanco Crema.png"),
    ("fernando", "Don Fernando", "images/sprites/Don Fernando.png"),
    ("elena", "Elena Varela", "images/sprites/Elena Varela.png"),
    ("isolda", "La Marquesa Isolda", "images/sprites/La marquesa Isolda.png"),
    ("will", "Will", "images/sprites/Will.png"),
]

define LOCATIONS_FOR_NPC = ["salon", "master_bedroom", "guest_quarters", "kitchen", "garden", "pool", "library"]

define NPC_POSITIONS = {
    "salon": (588, 720),
    "master_bedroom": (1426, 736),
    "guest_quarters": (684, 783),
    "kitchen": (669, 757),
    "garden": (672, 636),
    "pool": (736, 743),
    "library": (1131, 752),
}

define NPC_NAMES = {
    "elias": "Elias Vann",
    "caterina": "Caterina",
    "isabella": "Isabella",
    "blanco": "Blanco Crema",
    "fernando": "Don Fernando",
    "elena": "Elena Varela",
    "isolda": "La Marquesa Isolda",
    "will": "Will",
}

# Weapon data: (display_name, image_path)
define WEAPON_DATA = [
    ("Pistol", "images/weapons/Pistola.png"),
    ("Trophy", "images/weapons/Trofeo.png"),
    ("Flowerpot", "images/weapons/Maceta.png"),
    ("Shears", "images/weapons/Cizalla.png"),
    ("Hose", "images/weapons/Manguera.png"),
    ("Pillow", "images/weapons/Almohada.png"),
    ("Knife", "images/weapons/Cuchillo.png"),
    ("Letter Opener", "images/weapons/Abre cartas.png"),
    ("Candelabra", "images/weapons/Candelabro.png"),
    ("Baseball Bat", "images/weapons/Bate de beisbol.png"),
    ("Brass Knuckles", "images/weapons/Puno americano.png"),
    ("Poison", "images/weapons/Veneno.png"),
    ("Hammer", "images/weapons/Martillo.png"),
]

define WEAPON_DESCRIPTIONS = [
    "Una pistola semiautomatica elegante. El numero de serie ha sido limado. Un leve olor a polvora aun impregna el cañon.",
    "Un pesado trofeo dorado, deslucido por el paso del tiempo. La base esta abollada — como si hubiera sido usado para golpear algo. O a alguien.",
    "Una gran maceta de terracota. La tierra sigue humeda. Hay marcas de aranazos recientes en el borde.",
    "Un par de tijeras de jardineria pesadas. Las hojas estan afiladas y limpias — quizas demasiado limpias. Ni una mota de oxido.",
    "Una manguera de goma gruesa, sorprendentemente pesada. Marcas de lazo en la superficie sugieren que fue atada en un nudo recientemente.",
    "Una almohada de plumas mullida. La tela esta arrugada en el centro, como si hubiera sido presionada con gran fuerza.",
    "Un cuchillo de chef del bloque de cocina. La hoja esta impecable, pero una tenue marca rojiza persiste donde el mango se une al acero.",
    "Un abrecartas de plata ornamentado. Elegante pero terriblemente afilado. Un monograma en el mango dice 'A.M.'",
    "Un pesado candelabro de bronce. Un brazo esta doblado en un angulo extrano. Cera seca gotea por el costado como lagrimas congeladas.",
    "Un bate de beisbol de madera desgastado. La cinta de agarre se esta despegando. Hay marcas de rozaduras cerca del extremo del barril.",
    "Un juego de punos americanos, frios y solidos. El metal esta rayado — evidencia de uso previo.",
    "Un pequeno frasco de vidrio sin etiqueta. El liquido en su interior es transparente e inodoro. Una sola gota podria ser letal.",
    "Un martillo de carpintero estandar. La cabeza esta limpia, pero el mango tiene leves marcas oscuras.",
]

# Weapon positions: bottom-anchored coordinates per location
define WEAPON_SLOTS = {
    "kitchen":        [(104, 637), (1495, 210)],
    "guest_quarters": [(293, 161)],
    "library":        [(977, 396), (1387, 562)],
    "master_bedroom": [(337, 641), (1027, 702)],
    "salon":          [(211, 634), (1300, 398)],
    "garden":         [(206, 433), (1067, 600)],
    "pool":           [(1211, 592), (1625, 436)],
    "hidden_room":    [(1040, 657)],
}

default weapon_placements = {}  # {weapon_num: (loc, x, y)}
default weapon_type = {}       # {weapon_num: index into WEAPON_DATA}

# Game state
default current_location = "salon"
default current_location_name = "Salon"
default hidden_room_found = False
default victim_id = ""
default victim_name = ""
default time_left = 600
default accusation_manual = False
default accusation_active = False
default accusation_char = None
default accusation_weapon = None
default accusation_location = None
default accusation_accomplice = None
default inspecting_weapon = 0
default npc_location = {}
default npc_portrait_map = {}

# Case solution (randomly generated)
default murderer_id = ""
default murderer_name = ""
default weapon_id = 0
default weapon_name_str = ""
default crime_scene_id = ""
default crime_scene_name = ""
default accomplice_id = ""
default accomplice_name = ""

# LLM data
default llm_data = None
default llm_error = False
default npc_here_name = ""
default talking_to_npc = ""
default debug_reasoning = ""

# Location data
init python:
    locations = {
        "salon":          {"name": "Salon",              "image": "images/lugares/4_Salon.png"},
        "master_bedroom": {"name": "Dormitorio Principal", "image": "images/lugares/1_Habitacion_Principal.png"},
        "guest_quarters": {"name": "Habitacion de Invitados", "image": "images/lugares/2_Habitacion_Sirvientes.png"},
        "kitchen":        {"name": "Cocina",             "image": "images/lugares/3_Cocina.png"},
        "garden":         {"name": "Jardin",             "image": "images/lugares/6_Jardines.png"},
        "pool":           {"name": "Piscina",            "image": "images/lugares/7_Piscina.png"},
        "library":        {"name": "Biblioteca",         "image": "images/lugares/8_Biblioteca.png"},
        "hidden_room":    {"name": "Habitacion Oculta",  "image": "images/lugares/5_Habitacion_Secreta.png"},
    }

    def npc_id_at(loc):
        for nid, l in store.npc_location.items():
            if l == loc:
                return nid
        return None

    def _get_npc_char(npc_id):
        """Get the Character object for an NPC ID."""
        char_map = {
            "elias": store.elias,
            "caterina": store.caterina,
            "isabella": store.isabella,
            "blanco": store.blanco,
            "fernando": store.fernando,
            "elena": store.elena,
            "isolda": store.isolda,
            "will": store.will,
        }
        return char_map.get(npc_id, store.narrator)

# Game start
label splashscreen:
    $ renpy.movie_cutscene("video/opening.webm")
    return

label start:
    $ play_random_bgm()

    python:
        import json

        # ── Add parent dir to import path ──
        _parent_dir = os.path.dirname(renpy.config.gamedir)
        if _parent_dir not in sys.path:
            sys.path.insert(0, _parent_dir)

        # ── Try to load pre-generated world_data.json ──
        _world_data = None
        _world_data_path = os.path.join(_parent_dir, "world_data.json")
        try:
            with open(_world_data_path, "r", encoding="utf-8") as _f:
                _world_data = json.loads(_f.read())
        except Exception as _e:
            try:
                _log_path = os.path.join(_parent_dir, "load_error.log")
                with open(_log_path, "w", encoding="utf-8") as _lf:
                    _lf.write(f"Error loading world_data.json: {_e}\n")
                    _lf.write(f"Path tried: {_world_data_path}\n")
                    _lf.write(f"Gamedir: {renpy.config.gamedir}\n")
                    _lf.write(f"File exists: {os.path.exists(_world_data_path)}\n")
            except Exception:
                pass

        if _world_data:
            # ═══════════════════════════════════════════════════════════════
            # Build pipeline mode: use pre-generated world_data.json
            # ═══════════════════════════════════════════════════════════════
            from world_data_adapter import adaptar_world_data
            store.llm_data = adaptar_world_data(_world_data)
            store.llm_error = False

            _params = _world_data.get("parametros", {})

            # Victim
            store.victim_id = _params.get("victima_id", "")
            store.victim_name = _params.get("victima", "")

            # Murderer
            store.murderer_id = _params.get("asesino_id", "")
            store.murderer_name = _params.get("asesino", "")

            # Accomplice
            store.accomplice_id = _params.get("complice_id", "")
            store.accomplice_name = _params.get("complice", "")

            # Crime scene
            store.crime_scene_id = _params.get("escena_id", "")
            store.crime_scene_name = _params.get("escena", "")

            # Murder weapon - find matching index in WEAPON_DATA
            _arma_id = _params.get("arma_id", "")
            store.weapon_id = 0
            store.weapon_name_str = _arma_id
            for _i, (_wname, _wimg) in enumerate(WEAPON_DATA):
                if _wname == _arma_id:
                    store.weapon_id = _i
                    store.weapon_name_str = _wname
                    break

            # NPC locations (from world_data Spanish names -> internal IDs)
            from randomizador import PERSONAJE_A_ID, ESTANCIA_A_ID
            _ubicaciones = _params.get("ubicaciones_personajes", {})
            store.npc_location = {}
            for _nombre_es, _hab_es in _ubicaciones.items():
                _nid = PERSONAJE_A_ID.get(_nombre_es)
                _loc = ESTANCIA_A_ID.get(_hab_es)
                if _nid and _loc:
                    store.npc_location[_nid] = _loc

            # NPC portrait map (all NPCs, including victim for accusation screen)
            for _nid, _nname, _nportrait in NPC_DATA:
                store.npc_portrait_map[_nid] = _nportrait

            # Weapon placements (random local UI positions)
            _all_slots = []
            for _wloc, _positions in WEAPON_SLOTS.items():
                for _pos in _positions:
                    _all_slots.append((_wloc, _pos[0], _pos[1]))
            renpy.random.shuffle(_all_slots)
            _selected = _all_slots[:13]

            _wtype_indices = list(range(len(WEAPON_DATA)))
            renpy.random.shuffle(_wtype_indices)

            store.weapon_placements = {}
            store.weapon_type = {}
            for _i, (_wloc, _wx, _wy) in enumerate(_selected):
                store.weapon_placements[_i + 1] = (_wloc, _wx, _wy)
                store.weapon_type[_i + 1] = _wtype_indices[_i]

            # Debug reasoning from mapa_pistas
            _mapa = _world_data.get("mapa_pistas", {})
            store.debug_reasoning = _mapa.get("descripcion", (
                "Compara las pistas resaltadas en rojo en los dialogos de los NPC "
                "y los examenes de las habitaciones. Las inconsistencias te señalaran "
                "al asesino, el arma y la ubicacion del crimen."
            ))

            # Save log
            try:
                _save_llm_log(
                    main_response="Generado en segundo plano durante la sesion anterior",
                    reasoning_response=store.debug_reasoning,
                    case_info={
                        "victima": store.victim_name,
                        "asesino": store.murderer_name,
                        "arma": store.weapon_name_str,
                        "escena": store.crime_scene_name,
                        "complice": store.accomplice_name,
                    }
                )
            except Exception:
                pass

        else:
            # ═══════════════════════════════════════════════════════════════
            # Fallback mode: randomize locally + static content
            # ═══════════════════════════════════════════════════════════════
            npc_pool = list(NPC_DATA)
            renpy.random.shuffle(npc_pool)

            victim_id_data, victim_name_data, _vic_portrait = npc_pool[0]
            store.victim_id = victim_id_data
            store.victim_name = victim_name_data
            alive = npc_pool[1:]

            for nid, nname, nportrait in NPC_DATA:
                npc_portrait_map[nid] = nportrait

            locs = list(LOCATIONS_FOR_NPC)
            renpy.random.shuffle(locs)

            npc_location = {}
            for i, (nid, nname, nportrait) in enumerate(alive):
                npc_location[nid] = locs[i]

            murderer_idx = renpy.random.randint(0, len(alive) - 1)
            store.murderer_id = alive[murderer_idx][0]
            store.murderer_name = alive[murderer_idx][1]

            remaining_for_accomplice = [n for n in alive if n[0] != store.murderer_id]
            acc_idx = renpy.random.randint(0, len(remaining_for_accomplice) - 1)
            store.accomplice_id = remaining_for_accomplice[acc_idx][0]
            store.accomplice_name = remaining_for_accomplice[acc_idx][1]

            store.weapon_id = renpy.random.randint(0, len(WEAPON_DATA) - 1)
            store.weapon_name_str = WEAPON_DATA[store.weapon_id][0]

            scene_locs = list(LOCATIONS_FOR_NPC)
            scene_idx = renpy.random.randint(0, len(scene_locs) - 1)
            store.crime_scene_id = scene_locs[scene_idx]
            store.crime_scene_name = locations[scene_locs[scene_idx]]["name"]

            all_slots = []
            for wloc, positions in WEAPON_SLOTS.items():
                for pos in positions:
                    all_slots.append((wloc, pos[0], pos[1]))
            renpy.random.shuffle(all_slots)
            selected = all_slots[:13]

            wtype_indices = list(range(len(WEAPON_DATA)))
            renpy.random.shuffle(wtype_indices)

            weapon_placements = {}
            weapon_type = {}
            for i, (wloc, wx, wy) in enumerate(selected):
                weapon_placements[i + 1] = (wloc, wx, wy)
                weapon_type[i + 1] = wtype_indices[i]

            from llm.fallback import get_fallback_data
            store.llm_data = get_fallback_data(store.victim_name)
            store.llm_error = True
            store.debug_reasoning = (
                "Contenido estatico de reserva. La generacion automatica con IA "
                "fallo. Verifica que MERCURY_API_KEY este configurada en .env "
                "y que haya conexion a internet."
            )

        # ── Generate next world_data.json in background for next playthrough ──
        # Skip if another generation is already running (lock file check)
        _lock_path = os.path.join(_parent_dir, ".generating.lock")
        if not os.path.exists(_lock_path):
            import subprocess
            import shutil
            _python_exe = shutil.which("python") or shutil.which("python3") or sys.executable
            _build_script = os.path.join(_parent_dir, "build_prompt.py")
            try:
                subprocess.Popen(
                    [_python_exe, _build_script],
                    cwd=_parent_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass
        else:
            # Lock file exists — check if it's stale (>10 min old)
            try:
                _lock_age = os.path.getmtime(_lock_path)
                if _lock_age < 0 or (time.time() - _lock_age) > 600:
                    import subprocess
                    import shutil
                    os.remove(_lock_path)
                    _python_exe = shutil.which("python") or shutil.which("python3") or sys.executable
                    _build_script = os.path.join(_parent_dir, "build_prompt.py")
                    try:
                        subprocess.Popen(
                            [_python_exe, _build_script],
                            cwd=_parent_dir,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                    except Exception:
                        pass
            except Exception:
                pass

    # ── Opening ──
    scene black
    with fade

    if llm_data:
        $ opening_text = llm_data["opening_narrative"]
        "[opening_text]"
    else:
        "Es tarde en la noche. La lluvia cae a cantaros.\n\nUn telefono suena de forma estridente, rompiendo el silencio de la oficina.\n\nEl reconocido magnate Don Alejandro Montemayor ha sido hallado muerto en la biblioteca de su propia mansion.\n\nComo el detective mas celebre de la ciudad, te convocan a la escena de inmediato.\n\nOcho personas estaban en la mansion esa noche — pero ahora, solo quedan siete.\n\n[victim_name] esta muerto. Asesinado.\n\nDebes descubrir la verdad."

    jump salon


# ──── Generic location entry ────
label location_entry(loc_id):
    scene expression Transform(locations[loc_id]["image"], xysize=(1920, 1080), fit="cover")
    with fade
    $ current_location = loc_id
    $ current_location_name = locations[loc_id]["name"]
    show screen quick_nav
    show screen location_npcs
    show screen countdown_timer
    show screen hands_display
    show screen weapons_display

    $ npc_here_name = NPC_NAMES.get(npc_id_at(loc_id), "")

    $ desc = _get_loc_desc(loc_id)
    "[desc]"
    jump location_wait

init python:
    def _get_loc_desc(loc_key):
        """Get location description from llm_data."""
        if store.llm_data is None:
            return "Observas la habitacion a tu alrededor."
        loc_data = store.llm_data.get("locations", {}).get(loc_key, {})
        desc = loc_data.get("description", "Observas la habitacion a tu alrededor.")
        # Replace fallback placeholder with actual NPC name
        desc = desc.replace("[npc_here_name]", store.npc_here_name)
        return desc

    def _get_loc_clue(loc_key):
        """Get location clue from llm_data."""
        if store.llm_data is None:
            return "No encuentras nada significativo."
        loc_data = store.llm_data.get("locations", {}).get(loc_key, {})
        return loc_data.get("clue", "No encuentras nada significativo.")

    def _get_weapon_inspect(weapon_name):
        """Get weapon inspection text from llm_data."""
        if store.llm_data is None:
            return "Examinas el arma " + weapon_name + " con atencion."
        weapons = store.llm_data.get("weapons", {})
        wp_data = weapons.get(weapon_name, {})
        return wp_data.get("inspect_text", "Examinas el arma " + weapon_name + " con atencion.")

    def _get_npc_dialogues(npc_id):
        """Get NPC dialogues from llm_data."""
        if store.llm_data is None:
            return [], ""
        npc_data = store.llm_data.get("npcs", {}).get(npc_id, {})
        return npc_data.get("dialogues", []), npc_data.get("mood", "")

    def _save_llm_log(main_response, reasoning_response, case_info):
        """Save LLM responses to a timestamped text file for review."""
        import os
        import datetime
        log_dir = os.path.join(renpy.config.gamedir, "llm_logs")
        try:
            os.makedirs(log_dir)
        except Exception:
            pass
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(log_dir, timestamp + ".txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write("=== DATOS DEL CASO ===\n")
                for k, v in case_info.items():
                    f.write("{}: {}\n".format(k, v))
                f.write("\n=== RESPUESTA PRINCIPAL ===\n")
                f.write(main_response if main_response else "(sin respuesta)")
                f.write("\n\n=== RAZONAMIENTO ===\n")
                f.write(reasoning_response if reasoning_response else "(sin respuesta)")
        except Exception:
            pass

    def _check_accusation():
        """Check the player's accusation against the truth. Returns outcome key."""
        correct_murderer = (store.accusation_char == store.murderer_id)
        correct_weapon = (store.weapon_type.get(store.accusation_weapon, -1) == store.weapon_id)
        correct_location = (store.accusation_location == store.crime_scene_id)
        correct_accomplice = (store.accusation_accomplice == store.accomplice_id) if store.accomplice_id else (store.accusation_accomplice is None)

        if correct_murderer and correct_weapon and correct_location and correct_accomplice:
            return "correct"
        if not correct_murderer and not correct_weapon and not correct_location and not correct_accomplice:
            return "all_wrong"
        if not correct_murderer:
            return "wrong_murderer"
        if not correct_weapon:
            return "wrong_weapon"
        if not correct_location:
            return "wrong_location"
        if not correct_accomplice:
            return "wrong_accomplice"
        return "all_wrong"


# ──── Locations ────

label salon:
    call location_entry("salon")
    jump location_wait

label master_bedroom:
    call location_entry("master_bedroom")
    jump location_wait

label guest_quarters:
    call location_entry("guest_quarters")
    jump location_wait

label kitchen:
    call location_entry("kitchen")
    jump location_wait

label garden:
    call location_entry("garden")
    jump location_wait

label pool:
    call location_entry("pool")
    jump location_wait

label library:
    call location_entry("library")
    jump location_wait

label hidden_room:
    call location_entry("hidden_room")
    jump location_wait


# ──── Look Around labels ────

label salon_look:
    $ clue = _get_loc_clue("salon")
    "[clue]"
    jump salon

label master_bedroom_look:
    $ clue = _get_loc_clue("master_bedroom")
    "[clue]"
    jump master_bedroom

label guest_quarters_look:
    $ clue = _get_loc_clue("guest_quarters")
    "[clue]"
    jump guest_quarters

label kitchen_look:
    $ clue = _get_loc_clue("kitchen")
    "[clue]"
    jump kitchen

label garden_look:
    $ clue = _get_loc_clue("garden")
    "[clue]"
    jump garden

label pool_look:
    $ clue = _get_loc_clue("pool")
    "[clue]"
    jump pool

label library_look:
    $ clue = _get_loc_clue("library")
    "[clue]"

    if not hidden_room_found:
        "Mientras inspeccionas la estanteria, notas algo extrano en un ejemplar de 'El Sabueso de los Baskerville'.\n\nAlargas la mano hacia el. El libro no se mueve. Empujas con mas fuerza --\n\nClic. ¡Toda la estanteria se abre girando, revelando una habitacion oculta!"
        $ hidden_room_found = True
        $ current_location = "library"
    else:
        "La entrada a la habitacion oculta permanece abierta de par en par -- el mecanismo de la estanteria ahora es evidente."
    jump library

label hidden_room_look:
    $ clue = _get_loc_clue("hidden_room")
    "[clue]"
    jump hidden_room


# ──── Location wait loop ────

label location_wait:
    pause
    jump location_wait


# ──── Weapon Inspection ────

label inspect_weapon:
    $ wtype_idx = weapon_type.get(inspecting_weapon, 0)
    $ wname, wimg = WEAPON_DATA[wtype_idx]

    show expression Transform(wimg, xsize=300, fit="contain") at truecenter with dissolve
    "Observas mas de cerca [wname]."

    if llm_data:
        $ wdesc = _get_weapon_inspect(wname)
        "[wdesc]"
    else:
        $ wdesc = WEAPON_DESCRIPTIONS[wtype_idx]
        "[wdesc]"

    hide expression Transform(wimg, xsize=300, fit="contain") with dissolve
    jump expression current_location


# ──── Talk to NPC ────

label talk_npc:
    python:
        nid = talking_to_npc
        nname = NPC_NAMES.get(nid, "")
        nportrait = npc_portrait_map.get(nid, "")
        dialogues, mood = _get_npc_dialogues(nid)
        nchar = _get_npc_char(nid)
        # Extract 4 dialogues (with fallback defaults)
        d0 = dialogues[0] if len(dialogues) > 0 else {"question": "Tell me about yourself.", "answer": "There is not much to tell, Detective."}
        d1 = dialogues[1] if len(dialogues) > 1 else {"question": "Where were you last night?", "answer": "I was in my room."}
        d2 = dialogues[2] if len(dialogues) > 2 else {"question": "Did you see anything unusual?", "answer": "Nothing out of the ordinary."}
        d3 = dialogues[3] if len(dialogues) > 3 else {"question": "Who do you suspect?", "answer": "I would rather not say."}

    show expression Transform(nportrait, xsize=360, ysize=540, fit="contain") as npc_talk:
        xalign 0.85 yalign 0.5

    $ renpy.say(nchar, "Buenas noches, detective. " + mood + ".")

    menu:
        "[d0['question']]":
            $ renpy.say(nchar, d0["answer"])
        "[d1['question']]":
            $ renpy.say(nchar, d1["answer"])
        "[d2['question']]":
            $ renpy.say(nchar, d2["answer"])
        "[d3['question']]":
            $ renpy.say(nchar, d3["answer"])
        "Eso es todo por ahora.":
            pass

    hide npc_talk
    jump expression current_location


# ──── Accusation Result ────

label accusation_result:
    hide screen accusation_screen
    hide screen quick_nav
    hide screen location_npcs
    hide screen weapons_display
    hide screen hands_display
    hide screen countdown_timer

    if accusation_char is None or accusation_weapon is None or accusation_location is None:
        "No has seleccionado todos los elementos requeridos.\n\nAsegurate de haber elegido un culpable, un complice, un arma y un lugar."
        jump location_wait

    python:
        outcome = _check_accusation()
        outcomes = llm_data.get("accusation_outcomes", {})
        result_text = outcomes.get(outcome, "Your accusation has been registered. But the truth remains elusive.")

    if outcome == "correct":
        # ── Victoria ──
        stop music
        scene black with fade
        show expression Transform("images/pantallavictoria.png", xysize=(1920, 1080), fit="contain") at truecenter with dissolve
        "[result_text]"
        "FIN -- Has resuelto el caso."
        $ renpy.full_restart()
    else:
        # ── Derrota ──
        stop music
        scene black with fade
        show expression Transform("images/pantalladerrota.png", xysize=(1920, 1080), fit="contain") at truecenter with dissolve
        "[result_text]"
        "FIN -- El caso queda sin resolver."
        $ renpy.full_restart()

    return

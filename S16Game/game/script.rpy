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
    "A sleek semi-automatic pistol. The serial number has been filed off. A faint smell of gunpowder still clings to the barrel.",
    "A heavy golden trophy, tarnished with age. The base is dented — as if it was used to strike something. Or someone.",
    "A large terracotta flowerpot. The soil is still damp. There are fresh scratch marks along the rim.",
    "A pair of heavy-duty garden shears. The blades are sharp and clean — perhaps too clean. Not a speck of rust.",
    "A thick rubber garden hose, surprisingly heavy. Loop marks on the surface suggest it was recently tied into a knot.",
    "A plush down pillow. The fabric is creased in the middle, as if pressed down with great force.",
    "A chef's knife from the kitchen block. The blade is spotless, but a faint reddish stain lingers where the handle meets the steel.",
    "An ornate silver letter opener. Elegant but wickedly sharp. A monogram on the handle reads 'B.J.'",
    "A heavy brass candelabra. One arm is bent at an odd angle. Dried wax drips down the side like frozen tears.",
    "A well-worn wooden baseball bat. The grip tape is peeling. There are scuff marks near the barrel end.",
    "A set of brass knuckles, cold and solid. The metal is scratched — evidence of past use.",
    "A small unlabeled glass vial. The liquid inside is clear and odorless. A single drop could be lethal.",
    "A standard claw hammer. The head is clean, but the handle bears faint dark smears.",
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

# Location data
init python:
    locations = {
        "salon":          {"name": "Salon",           "image": "images/lugares/4_Salon.png"},
        "master_bedroom": {"name": "Master Bedroom",  "image": "images/lugares/1_Habitacion_Principal.png"},
        "guest_quarters": {"name": "Guest Quarters",  "image": "images/lugares/2_Habitacion_Sirvientes.png"},
        "kitchen":        {"name": "Kitchen",         "image": "images/lugares/3_Cocina.png"},
        "garden":         {"name": "Garden",          "image": "images/lugares/6_Jardines.png"},
        "pool":           {"name": "Pool",            "image": "images/lugares/7_Piscina.png"},
        "library":        {"name": "Library",         "image": "images/lugares/8_Biblioteca.png"},
        "hidden_room":    {"name": "Hidden Room",     "image": "images/lugares/5_Habitacion_Secreta.png"},
    }

    def npc_id_at(loc):
        for nid, l in store.npc_location.items():
            if l == loc:
                return nid
        return None

# Game start
label splashscreen:
    $ renpy.movie_cutscene("video/opening.webm")
    return

label start:
    $ play_random_bgm()

    python:
        npc_pool = list(NPC_DATA)
        renpy.random.shuffle(npc_pool)

        victim_id, victim_name, _vic_portrait = npc_pool[0]
        alive = npc_pool[1:]

        for nid, nname, nportrait in NPC_DATA:
            npc_portrait_map[nid] = nportrait

        locs = list(LOCATIONS_FOR_NPC)
        renpy.random.shuffle(locs)

        npc_location = {}
        for i, (nid, nname, nportrait) in enumerate(alive):
            npc_location[nid] = locs[i]

        # Weapon placement: 13 weapons in 14 possible slots
        all_slots = []
        for loc, positions in WEAPON_SLOTS.items():
            for pos in positions:
                all_slots.append((loc, pos[0], pos[1]))
        renpy.random.shuffle(all_slots)
        selected = all_slots[:13]

        wtype_indices = list(range(len(WEAPON_DATA)))
        renpy.random.shuffle(wtype_indices)

        weapon_placements = {}
        weapon_type = {}
        for i, (loc, x, y) in enumerate(selected):
            weapon_placements[i + 1] = (loc, x, y)
            weapon_type[i + 1] = wtype_indices[i]

    scene black
    with fade
    "Late at night. Rain pours down in sheets.\n\nA shrill telephone ring shatters the silence of the office.\n\nRenowned tycoon Bai Jingtian has been found dead in the library of his own mansion.\n\nAs the most celebrated detective in town, you are summoned to the scene immediately.\n\nEight people were in the mansion that night — but now, only seven remain.\n\n[victim_name] is dead. Murdered.\n\nYou must uncover the truth."
    jump salon

# ========== Salon ==========
label salon:
    scene expression Transform(locations["salon"]["image"], xysize=(1920, 1080), fit="cover")
    with fade
    $ current_location = "salon"
    $ current_location_name = locations["salon"]["name"]
    show screen quick_nav
    show screen location_npcs
    show screen countdown_timer
    show screen hands_display
    show screen weapons_display

    $ npc_here = NPC_NAMES.get(npc_id_at("salon"), "")
    if npc_here:
        "Salon -- Spacious and grand, a massive crystal chandelier hangs from the center of the ceiling.\n\nThe marble floor gleams like a mirror, reflecting the dim glow of the chandelier.\n\nBeside the spiral staircase leading upstairs, a dark reddish stain has been hastily wiped clean.\n\n[npc_here] stands near the fireplace, arms crossed, watching you intently."
    jump location_wait

# ========== Master Bedroom ==========
label master_bedroom:
    scene expression Transform(locations["master_bedroom"]["image"], xysize=(1920, 1080), fit="cover")
    with fade
    $ current_location = "master_bedroom"
    $ current_location_name = locations["master_bedroom"]["name"]
    show screen quick_nav
    show screen location_npcs
    show screen countdown_timer
    show screen hands_display
    show screen weapons_display

    $ npc_here = NPC_NAMES.get(npc_id_at("master_bedroom"), "")
    if npc_here:
        "Master Bedroom -- Deep crimson velvet curtains block out most of the windows.\n\nA faint scent of perfume lingers in the air.\n\nOn the nightstand sits a half-finished glass of red wine and an open book.\n\n[npc_here] is here, glancing nervously toward the door."
    jump location_wait

# ========== Guest Quarters ==========
label guest_quarters:
    scene expression Transform(locations["guest_quarters"]["image"], xysize=(1920, 1080), fit="cover")
    with fade
    $ current_location = "guest_quarters"
    $ current_location_name = locations["guest_quarters"]["name"]
    show screen quick_nav
    show screen location_npcs
    show screen countdown_timer
    show screen hands_display
    show screen weapons_display

    $ npc_here = NPC_NAMES.get(npc_id_at("guest_quarters"), "")
    if npc_here:
        "Guest Quarters -- Plain and tidy, as if rarely used.\n\nThe bed is made with hotel-like precision. The bedside lamp is still on.\n\nA travel suitcase covered in luggage tags from around the world sits on the windowsill.\n\n[npc_here] lingers by the window, silhouetted against the rain."
    jump location_wait

# ========== Kitchen ==========
label kitchen:
    scene expression Transform(locations["kitchen"]["image"], xysize=(1920, 1080), fit="cover")
    with fade
    $ current_location = "kitchen"
    $ current_location_name = locations["kitchen"]["name"]
    show screen quick_nav
    show screen location_npcs
    show screen countdown_timer
    show screen hands_display
    show screen weapons_display

    $ npc_here = NPC_NAMES.get(npc_id_at("kitchen"), "")
    if npc_here:
        "Kitchen -- A sprawling modern kitchen fitted with top-of-the-line appliances.\n\nA pot from last night's cooking still sits on the stove, its contents long since congealed.\n\nThere is a faint, bitter scent of almonds in the air.\n\n[npc_here] leans against the counter, staring at the congealed pot."
    jump location_wait

# ========== Garden ==========
label garden:
    scene expression Transform(locations["garden"]["image"], xysize=(1920, 1080), fit="cover")
    with fade
    $ current_location = "garden"
    $ current_location_name = locations["garden"]["name"]
    show screen quick_nav
    show screen location_npcs
    show screen countdown_timer
    show screen hands_display
    show screen weapons_display

    $ npc_here = NPC_NAMES.get(npc_id_at("garden"), "")
    if npc_here:
        "Garden -- Carefully trimmed hedges cast eerie shadows under the moonlight.\n\nThe roses are in full bloom, but a patch of soil near the far wall looks recently disturbed.\n\nIn the distance, an owl calls out into the night.\n\n[npc_here] paces slowly along the hedge path, deep in thought."
    jump location_wait

# ========== Pool ==========
label pool:
    scene expression Transform(locations["pool"]["image"], xysize=(1920, 1080), fit="cover")
    with fade
    $ current_location = "pool"
    $ current_location_name = locations["pool"]["name"]
    show screen quick_nav
    show screen location_npcs
    show screen countdown_timer
    show screen hands_display
    show screen weapons_display

    $ npc_here = NPC_NAMES.get(npc_id_at("pool"), "")
    if npc_here:
        "Pool -- The water is perfectly still, a mirror reflecting the scattered stars above.\n\nA damp towel is draped over one of the lounge chairs.\n\nThe door to the changing room at the corner stands slightly ajar.\n\n[npc_here] sits on one of the lounge chairs, staring at the water's surface."
    jump location_wait

# ========== Library ==========
label library:
    scene expression Transform(locations["library"]["image"], xysize=(1920, 1080), fit="cover")
    with fade
    $ current_location = "library"
    $ current_location_name = locations["library"]["name"]
    show screen quick_nav
    show screen location_npcs
    show screen countdown_timer
    show screen hands_display
    show screen weapons_display

    $ npc_here = NPC_NAMES.get(npc_id_at("library"), "")
    if npc_here:
        "Library -- Bai Jingtian's private sanctuary. Bookshelves line every wall from floor to ceiling.\n\nA mahogany desk is covered in documents and ledgers.\n\nOn the floor, a chalk outline marks where the body fell.\n\nThis -- is the scene of the crime.\n\n[npc_here] stands at the edge of the room, unable to look away from the chalk outline on the floor."
    jump location_wait

# ========== Hidden Room ==========
label hidden_room:
    scene expression Transform(locations["hidden_room"]["image"], xysize=(1920, 1080), fit="cover")
    with fade
    $ current_location = "hidden_room"
    $ current_location_name = locations["hidden_room"]["name"]
    show screen quick_nav
    show screen location_npcs
    show screen countdown_timer
    show screen hands_display
    show screen weapons_display

    "Hidden Room -- Cramped and dim, lit only by a single flickering bulb.\n\nThe walls are covered with photographs and newspaper clippings, connected by a web of red string.\n\nIn the corner stands an old metal cabinet, thick with dust."
    jump location_wait



label salon_look:
    "You pace slowly through the salon, examining every corner with care.\n\nThe stair railing bears no fingerprints. A small scorch mark mars the edge of the carpet.\n\nIn the family portrait above the fireplace, Bai Jingtian's eyes seem to betray a deep unease."
    jump salon

label master_bedroom_look:
    "You scan the master bedroom. Rows of expensive decor line the shelves in perfect order.\n\nInside the cabinet drawer, you find a letter. The handwriting is erratic -- it reads like a threat.\n\nA faint scratch mark runs across the floor, from the doorway all the way to the window."
    jump master_bedroom

label guest_quarters_look:
    "You open the suitcase. Nothing inside but ordinary clothes and toiletries.\n\nUnder the pillow lies a diary, but most of its pages have been torn out.\n\nIn the wastebasket, a crumpled piece of paper bears a single smudged phone number."
    jump guest_quarters

label kitchen_look:
    "You check the refrigerator and pantry. Everything is meticulously organized.\n\nIn the trash bin, a broken wine glass. Dried red residue clings to the shards.\n\nUnder the sink, an unlabeled brown glass bottle is tucked behind cleaning supplies."
    jump kitchen

label garden_look:
    "You approach the disturbed soil. A metal box has been buried here.\n\nThe box is empty, but dried blood stains its interior.\n\nAmong the flower beds, you spot a partial footprint -- roughly a size 10."
    jump garden

label pool_look:
    "You circle the pool, scanning for anything out of place.\n\nA single leaf floats on the water, but otherwise the pool seems undisturbed.\n\nInside the changing room, a soaked shirt hangs from a hook. In its pocket, a water-damaged note.\n\nMuddy footprints dot the tiles near the pool's edge -- someone came through here from the garden."
    jump pool

label library_look:
    "You examine the desk closely. The last page of a notebook has been torn out.\n\nA wall safe hangs open, containing nothing but a stack of empty folders."
    if not hidden_room_found:
        "While inspecting the bookshelf, you notice something odd about a copy of 'The Complete Sherlock Holmes'.\n\nYou reach for it. The book won't budge. You push harder --\n\nClick. The entire bookcase swings open, revealing a hidden room!"
        $ hidden_room_found = True
        $ current_location = "library"
    else:
        "The entrance to the hidden room remains wide open -- the mechanism in the bookshelf now plain to see."
    jump library

label hidden_room_look:
    "You study the web of clues on the wall.\n\nThe photographs include Bai Jingtian, his business partners, his family -- and faces you don't recognize.\n\nThe metal cabinet holds a stack of letters and an unsigned contract.\n\nThis room holds too many secrets to count..."
    jump hidden_room

label location_wait:
    pause
    jump location_wait

# ========== Weapon Inspection ==========
label inspect_weapon:
    $ wtype_idx = weapon_type.get(inspecting_weapon, 0)
    $ wname, wimg = WEAPON_DATA[wtype_idx]
    $ wdesc = WEAPON_DESCRIPTIONS[wtype_idx]

    show expression Transform(wimg, xsize=300, fit="contain") at truecenter with dissolve
    "You take a closer look at the [wname]."

    "[wdesc]"

    hide expression Transform(wimg, xsize=300, fit="contain") with dissolve
    jump expression current_location

# ========== Talk Labels ==========
label talk_elias:
    show elias_portrait:
        xalign 0.85  yalign 0.5  xsize 360  ysize 540  fit "contain"
    elias "Good evening, Detective. I have served this family for twenty years."
    menu:
        "Where were you on the night of the murder?":
            elias "I was in the kitchen preparing the evening tea. The routine of this house does not stop for anyone."
        "Did you notice anything strange lately?":
            elias "The master had been receiving threatening letters. He burned most of them in the fireplace."
        "Tell me about your relationship with the victim.":
            elias "I served him faithfully for twenty years. He was... a complicated man. Generous to some, ruthless to others."
        "Who do you think could have done this?":
            elias "I have my suspicions, Detective. But it is not my place to accuse. Look closely at the guests."
    hide elias_portrait
    jump expression current_location

label talk_caterina:
    show caterina_portrait:
        xalign 0.85  yalign 0.5  xsize 360  ysize 540  fit "contain"
    caterina "Detective, have you found anything yet? I need justice for my husband."
    menu:
        "When did you last see your husband alive?":
            caterina "At dinner. He seemed preoccupied, barely touched his food. Then he left for the library."
        "Was your husband having trouble with anyone?":
            caterina "Bai Jingtian had rivals everywhere. Business, politics... even within these walls."
        "Who stands to gain from his death?":
            caterina "The inheritance is... substantial. But I would trade every penny to have him back."
        "Do you know about the hidden room behind the bookshelf?":
            caterina "Hidden room? I... no. My husband kept many things from me, Detective."
    hide caterina_portrait
    jump expression current_location

label talk_isabella:
    show isabella_portrait:
        xalign 0.85  yalign 0.5  xsize 360  ysize 540  fit "contain"
    isabella "Detective... I still cannot believe my father is gone."
    menu:
        "Were you close with your father?":
            isabella "We were. But lately he had been distant. He looked over his shoulder constantly."
        "Did your father have any enemies?":
            isabella "He was a powerful man. Power attracts enemies like honey attracts flies."
        "Where were you when it happened?":
            isabella "I was in the garden. I like to walk among the roses when I cannot sleep."
        "What do you know about the other guests?":
            isabella "Everyone here has secrets. Even me, Detective. But none worth killing for."
    hide isabella_portrait
    jump expression current_location

label talk_blanco:
    show blanco_portrait:
        xalign 0.85  yalign 0.5  xsize 360  ysize 540  fit "contain"
    blanco "Ah, Detective. I was hoping we could talk."
    menu:
        "What brings you to the mansion?":
            blanco "Bai Jingtian and I had... business to discuss. Unfinished business."
        "Where were you at the time of the murder?":
            blanco "I was in the guest quarters, going over some documents. Alone, unfortunately."
        "How well did you know the victim?":
            blanco "We were partners once. Then rivals. Then something in between. It is... complicated."
        "Is there anything you are not telling me?":
            blanco "Detective, everyone in this house is hiding something. The question is — whose secret was worth killing for?"
    hide blanco_portrait
    jump expression current_location

label talk_fernando:
    show fernando_portrait:
        xalign 0.85  yalign 0.5  xsize 360  ysize 540  fit "contain"
    fernando "Detective, I trust the investigation is proceeding well?"
    menu:
        "Where were you on the night of the murder?":
            fernando "I was in my room, reading. The Count of Monte Cristo. Rather appropriate, given the circumstances."
        "What was your relationship with Bai Jingtian?":
            fernando "We moved in the same circles. I respected him as a businessman — not necessarily as a man."
        "Have you noticed anything unusual tonight?":
            fernando "The butler was not himself at dinner. Nervous. He dropped a tray of glasses."
        "What do you make of the other guests?":
            fernando "Let us just say I have seen better company at a funeral. And worse."
    hide fernando_portrait
    jump expression current_location

label talk_elena:
    show elena_portrait:
        xalign 0.85  yalign 0.5  xsize 360  ysize 540  fit "contain"
    elena "Detective... this house feels so cold tonight."
    menu:
        "How did you know Bai Jingtian?":
            elena "We met through business. I was his art consultant for many years."
        "Where were you when it happened?":
            elena "I was in the salon, by the window. Watching the rain. Waiting."
        "Waiting for what?":
            elena "Waiting for something to end. I did not expect it to end like this."
        "Did you see anyone pass through the salon?":
            elena "I saw a figure heading toward the library. But the chandelier was dim — I could not make out who."
    hide elena_portrait
    jump expression current_location

label talk_isolda:
    show isolda_portrait:
        xalign 0.85  yalign 0.5  xsize 360  ysize 540  fit "contain"
    isolda "I hope you are not wasting time, Detective."
    menu:
        "What was your relationship with the deceased?":
            isolda "Bai Jingtian and I were old friends. I knew him before the money, before the mansion."
        "Do you believe someone in this house killed him?":
            isolda "Of course. Murder is almost always personal. And almost always comes from within."
        "Where were you during the murder?":
            isolda "I was in the master bedroom, resting. At my age, one needs frequent rest."
        "Is there anything else I should know?":
            isolda "The gardener did not show up today. First time in ten years. Make of that what you will."
    hide isolda_portrait
    jump expression current_location

label talk_will:
    show will_portrait:
        xalign 0.85  yalign 0.5  xsize 360  ysize 540  fit "contain"
    will "Detective. I have been meaning to speak with you."
    menu:
        "What did you overhear last night?":
            will "An argument. Raised voices coming from the library. Then silence. Terrible silence."
        "Did you recognize the voices?":
            will "One was definitely Bai Jingtian. The other... I am not certain. It was muffled."
        "What is your role in this household?":
            will "I am a family friend. Or I was. I came for the week and ended up in a crime scene."
        "Is there anyone you suspect?":
            will "I do not want to point fingers. But the widow's grief seems... rehearsed."
    hide will_portrait
    jump expression current_location

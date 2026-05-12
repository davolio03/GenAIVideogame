# Character definitions
define detective = Character("Detective", color="#c8c8ff")

define butler = Character("Elias Vann", color="#ffcc99")
define madam = Character("Caterina La Viuda Moretti", color="#ff9999")
define daughter = Character("Isabella Bella Dupont", color="#ff99cc")
define chef = Character("Chef Li", color="#99ff99")
define gardener = Character("Gardener Chen", color="#99cc66")
define driver = Character("Driver Zhou", color="#cccc99")
define guest = Character("El Marqués de la Seta", color="#cc99ff")

# Portrait images
image madam_portrait = "images/sprites/Caterina La Viuda Moretti.png"
image guest_portrait = "images/sprites/El Marqués de la Seta (Blanco Crema).png"
image butler_portrait = "images/sprites/Elias Vann.png"
image daughter_portrait = "images/sprites/Isabella Bella Dupont.png"
image chef_portrait = "images/sprites/char_noname_1.png"
image gardener_portrait = "images/sprites/char_noname_2.png"
image driver_portrait = "images/sprites/char_noname_3.png"

# Narrator
define narrator = Character(None)

# Game state
default current_location = "hall"
default current_location_name = "Hall"
default hidden_room_found = False

# Location data
init python:
    location_colors = {
        "hall": "#8B7355",
        "master_bedroom": "#8B0000",
        "guest_bedroom": "#4A6E4A",
        "kitchen": "#CD853F",
        "garden": "#556B2F",
        "pool": "#4682B4",
        "study": "#6B3A2E",
        "hidden_room": "#2F2F2F",
    }
    location_names = {
        "hall": "Hall",
        "master_bedroom": "Master Bedroom",
        "guest_bedroom": "Guest Bedroom",
        "kitchen": "Kitchen",
        "garden": "Garden",
        "pool": "Pool",
        "study": "Study",
        "hidden_room": "Hidden Room",
    }

# Game start
label start:
    scene Solid("#000000")
    with fade
    "Late at night. Rain pours down in sheets.\n\nA shrill telephone ring shatters the silence of the office.\n\nRenowned tycoon Bai Jingtian has been found dead in the study of his own mansion.\n\nAs the most celebrated detective in town, you are summoned to the scene immediately.\n\nSeven people were in the mansion that night. Each one holds a secret...\n\nYou must uncover the truth."
    jump hall

# ========== Hall ==========
label hall:
    $ current_location = "hall"
    $ current_location_name = "Hall"
    scene Solid(location_colors["hall"])
    with fade
    show screen quick_nav
    "Hall -- Spacious and grand, a massive crystal chandelier hangs from the center of the ceiling.\n\nThe marble floor gleams like a mirror, reflecting the dim glow of the chandelier.\n\nBeside the spiral staircase leading upstairs, a dark reddish stain has been hastily wiped clean."
    menu:
        "Look Around":
            "You pace slowly through the hall, examining every corner with care.\n\nThe stair railing bears no fingerprints. A small scorch mark mars the edge of the carpet.\n\nIn the family portrait above the fireplace, Bai Jingtian's eyes seem to betray a deep unease."
            jump hall
        "Open Map":
            call screen map_screen
            jump hall

# ========== Master Bedroom ==========
label master_bedroom:
    $ current_location = "master_bedroom"
    $ current_location_name = "Master Bedroom"
    scene Solid(location_colors["master_bedroom"])
    with fade
    show screen quick_nav
    "Master Bedroom -- Deep crimson velvet curtains block out most of the windows.\n\nA faint scent of perfume lingers in the air.\n\nOn the nightstand sits a half-finished glass of red wine and an open book."
    menu:
        "Look Around":
            "You open the wardrobe. Rows of expensive clothing hang in perfect order.\n\nInside the nightstand drawer, you find a letter. The handwriting is erratic -- it reads like a threat.\n\nA faint scratch mark runs across the floor, from the doorway all the way to the window."
            jump master_bedroom
        "Open Map":
            call screen map_screen
            jump master_bedroom

# ========== Guest Bedroom ==========
label guest_bedroom:
    $ current_location = "guest_bedroom"
    $ current_location_name = "Guest Bedroom"
    scene Solid(location_colors["guest_bedroom"])
    with fade
    show screen quick_nav
    "Guest Bedroom -- Plain and tidy, as if rarely used.\n\nThe bed is made with hotel-like precision. The bedside lamp is still on.\n\nA travel suitcase covered in luggage tags from around the world sits on the windowsill."
    menu:
        "Look Around":
            "You open the suitcase. Nothing inside but ordinary clothes and toiletries.\n\nUnder the pillow lies a diary, but most of its pages have been torn out.\n\nIn the wastebasket, a crumpled piece of paper bears a single smudged phone number."
            jump guest_bedroom
        "Open Map":
            call screen map_screen
            jump guest_bedroom

# ========== Kitchen ==========
label kitchen:
    $ current_location = "kitchen"
    $ current_location_name = "Kitchen"
    scene Solid(location_colors["kitchen"])
    with fade
    show screen quick_nav
    "Kitchen -- A sprawling modern kitchen fitted with top-of-the-line appliances.\n\nA pot from last night's cooking still sits on the stove, its contents long since congealed.\n\nThere is a faint, bitter scent of almonds in the air."
    menu:
        "Look Around":
            "You check the refrigerator and pantry. Everything is meticulously organized.\n\nIn the trash bin, a broken wine glass. Dried red residue clings to the shards.\n\nUnder the sink, an unlabeled brown glass bottle is tucked behind cleaning supplies."
            jump kitchen
        "Open Map":
            call screen map_screen
            jump kitchen

# ========== Garden ==========
label garden:
    $ current_location = "garden"
    $ current_location_name = "Garden"
    scene Solid(location_colors["garden"])
    with fade
    show screen quick_nav
    "Garden -- Carefully trimmed hedges cast eerie shadows under the moonlight.\n\nThe roses are in full bloom, but a patch of soil near the far wall looks recently disturbed.\n\nIn the distance, an owl calls out into the night."
    menu:
        "Look Around":
            "You approach the disturbed soil. A metal box has been buried here.\n\nThe box is empty, but dried blood stains its interior.\n\nAmong the flower beds, you spot a partial footprint -- roughly a size 10."
            jump garden
        "Open Map":
            call screen map_screen
            jump garden

# ========== Pool ==========
label pool:
    $ current_location = "pool"
    $ current_location_name = "Pool"
    scene Solid(location_colors["pool"])
    with fade
    show screen quick_nav
    "Pool -- The water is perfectly still, a mirror reflecting the scattered stars above.\n\nA damp towel is draped over one of the lounge chairs.\n\nThe door to the changing room at the corner stands slightly ajar."
    menu:
        "Look Around":
            "You circle the pool, scanning for anything out of place.\n\nA single leaf floats on the water, but otherwise the pool seems undisturbed.\n\nInside the changing room, a soaked shirt hangs from a hook. In its pocket, a water-damaged note.\n\nMuddy footprints dot the tiles near the pool's edge -- someone came through here from the garden."
            jump pool
        "Open Map":
            call screen map_screen
            jump pool

# ========== Study ==========
label study:
    $ current_location = "study"
    $ current_location_name = "Study"
    scene Solid(location_colors["study"])
    with fade
    show screen quick_nav
    "Study -- Bai Jingtian's private sanctuary. Bookshelves line every wall from floor to ceiling.\n\nA mahogany desk is covered in documents and ledgers.\n\nOn the floor, a chalk outline marks where the body fell.\n\nThis -- is the scene of the crime."
    menu:
        "Look Around":
            "You examine the desk closely. The last page of a notebook has been torn out.\n\nA wall safe hangs open, containing nothing but a stack of empty folders."
            if not hidden_room_found:
                "While inspecting the bookshelf, you notice something odd about a copy of 'The Complete Sherlock Holmes'.\n\nYou reach for it. The book won't budge. You push harder --\n\nClick. The entire bookcase swings open, revealing a hidden room!"
                $ hidden_room_found = True
                $ current_location = "study"
            else:
                "The entrance to the hidden room remains wide open -- the mechanism in the bookshelf now plain to see."
            jump study
        "Open Map":
            call screen map_screen
            jump study

# ========== Hidden Room ==========
label hidden_room:
    $ current_location = "hidden_room"
    $ current_location_name = "Hidden Room"
    scene Solid(location_colors["hidden_room"])
    with fade
    show screen quick_nav
    "Hidden Room -- Cramped and dim, lit only by a single flickering bulb.\n\nThe walls are covered with photographs and newspaper clippings, connected by a web of red string.\n\nIn the corner stands an old metal cabinet, thick with dust."
    menu:
        "Look Around":
            "You study the web of clues on the wall.\n\nThe photographs include Bai Jingtian, his business partners, his family -- and faces you don't recognize.\n\nThe metal cabinet holds a stack of letters and an unsigned contract.\n\nThis room holds too many secrets to count..."
            jump hidden_room
        "Open Map":
            call screen map_screen
            jump hidden_room


# ========== Talk Labels ==========
label talk_madam:
    show madam_portrait:
        xalign 0.85  yalign 0.5  xsize 360
    madam "Detective, have you found anything yet? I need justice for my husband."
    detective "I am still piecing everything together. I promise I will find the truth."
    madam "Please hurry. The longer this takes, the more restless everyone becomes."
    hide madam_portrait
    jump expression current_location

label talk_guest:
    show guest_portrait:
        xalign 0.85  yalign 0.5  xsize 360
    guest "Ah, Detective. I was hoping we could talk."
    detective "You seem eager. Is there something you want to tell me?"
    guest "Let us just say... not everyone in this house is as innocent as they claim."
    hide guest_portrait
    jump expression current_location

label talk_butler:
    show butler_portrait:
        xalign 0.85  yalign 0.5  xsize 360
    butler "Good evening, Detective. I have served this family for twenty years."
    detective "Then you must know all of their secrets."
    butler "I know enough to keep my mouth shut and my eyes open."
    hide butler_portrait
    jump expression current_location

label talk_daughter:
    show daughter_portrait:
        xalign 0.85  yalign 0.5  xsize 360
    daughter "Detective... I still cannot believe my father is gone."
    detective "I am sorry for your loss. Were you close with your father?"
    daughter "We were. But lately... he had been hiding something from all of us."
    hide daughter_portrait
    jump expression current_location

label talk_chef:
    show chef_portrait:
        xalign 0.85  yalign 0.5  xsize 360
    chef "Dinner was served at eight, as always. No one skipped... except the master."
    detective "Did you notice anything unusual about last night's meal?"
    chef "The master's wine had a slightly different color. I assumed it was a new vintage."
    hide chef_portrait
    jump expression current_location

label talk_gardener:
    show gardener_portrait:
        xalign 0.85  yalign 0.5  xsize 360
    gardener "I was trimming the hedges until sunset. I did not see anything unusual."
    detective "The disturbed soil near the wall -- can you explain that?"
    gardener "I was... planting new roses. That is all."
    hide gardener_portrait
    jump expression current_location

label talk_driver:
    show driver_portrait:
        xalign 0.85  yalign 0.5  xsize 360
    driver "I spent the whole night in the garage. The car needed maintenance."
    detective "So you did not hear anything? The walls are thick, but a gunshot..."
    driver "This mansion hides many sounds. If there was a shot... I would not be surprised."
    hide driver_portrait
    jump expression current_location

# S16Game - Murder Mystery Visual Novel

Ren'Py visual novel project. Player takes on the role of a detective investigating a murder in a mansion.

## Language

ALL game content (dialogue, narration, UI labels, location names, menu options) MUST be in SPANISH. This includes all LLM-generated text and fallback content.

## LLM Logging

LLM responses are saved to `game/llm_logs/` with timestamp filenames (format: `YYYYMMDD_HHMMSS.txt`). Each file contains case info, main response, and reasoning response.

## Key Rules

- The accomplice (complice) ALWAYS exists — every case has a murderer AND an accomplice
- Every playthrough generates DIFFERENT content (high temperature, uniqueness emphasis in prompts)
- All LLM responses must be in Spanish

## Conversation Log

Every exchange between the user and Claude MUST be appended to `F:\Files_Nuevos\RenPyFiles\S16Game\对话.txt` in the following format:

```
【用户】user's message

【助手】Claude's response
```

This must be done at the end of each turn.

## Project Structure

```
S16Game/
  game/
    script.rpy    -- Characters, locations, game logic
    screens.rpy   -- Custom screens (quick_nav, talk_screen, map_screen)
    options.rpy   -- Game configuration
    gui.rpy       -- GUI styling
    images/
      sprites/    -- 8 character portraits
      lugares/    -- 8 location background images
    audio/        -- Audio assets
```

## Game Architecture

### Characters (9 total: 1 player + 8 NPCs)

- **Detective** (player) -- The protagonist, no portrait
- **Elias Vann** -- Butler (`images/sprites/Elias Vann.png`)
- **Caterina** -- Widow (`images/sprites/Caterina .png`)
- **Isabella** -- Daughter (`images/sprites/Isabella.png`)
- **Blanco Crema** -- Guest (`images/sprites/Blanco Crema.png`)
- **Don Fernando** -- Nobleman (`images/sprites/Don Fernando.png`)
- **Elena Varela** -- (`images/sprites/Elena Varela.png`)
- **La Marquesa Isolda** -- Marquise (`images/sprites/La marquesa Isolda.png`)
- **Will** -- (`images/sprites/Will.png`)

### Locations (8)

Each location uses a background image from `images/lugares/`:

| Location        | Image                                    | Label            | Map Coords      |
|-----------------|------------------------------------------|------------------|-----------------|
| Salon           | 4_Salon.png                             | `salon`          | (227,322) 404x187 |
| Master Bedroom  | 1_Habitacion_Principal.png              | `master_bedroom` | (716,91) 234x160  |
| Guest Quarters  | 2_Habitacion_Sirvientes.png             | `guest_quarters` | (335,91) 106x132  |
| Kitchen         | 3_Cocina.png                            | `kitchen`        | (159,90) 165x215  |
| Garden          | 6_Jardines.png                          | `garden`         | (298,583) 346x76  |
| Pool            | 7_Piscina.png                           | `pool`           | (916,442) 245x183 |
| Library         | 8_Biblioteca.png                        | `library`        | (453,91) 240x159  |
| Hidden Room     | 5_Habitacion_Secreta.png                | `hidden_room`    | (647,267) 94x70   |

The Hidden Room is inside the Library. It is unlocked by choosing "Look Around" in the Library.
Once discovered, it appears on the map.

### Navigation

- `quick_nav` screen: Always-visible panel on the right side showing current location + "Map" + "Talk" buttons
- `map_screen` screen: Modal overlay with transparent hotspots on `gui/map/mini_map_bg.png`. Hidden Room only appears after discovery.
- `talk_screen` screen: Modal overlay showing 8 character portraits in a 4x2 grid
- Navigation between locations uses `Jump()` actions with fade transitions

### Key Variables

- `current_location` -- Internal location ID string
- `current_location_name` -- Display name shown in quick_nav
- `hidden_room_found` -- Boolean, set to True when hidden room is discovered

## Resolution

1920x1080

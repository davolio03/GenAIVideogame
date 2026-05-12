# S16Game - Murder Mystery Visual Novel

Ren'Py visual novel project. Player takes on the role of a detective investigating a murder in a mansion.

## Language

ALL in-game content (dialogue, narration, UI labels, location names, character names, menu options) MUST be in English.

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
    screens.rpy   -- Custom screens (quick_nav, map_screen)
    options.rpy   -- Game configuration
    gui.rpy       -- GUI styling
    images/       -- Image assets (currently unused, using Solid colors)
    audio/        -- Audio assets
```

## Game Architecture

### Characters (8)
- **Detective** (player) -- The protagonist
- **Butler Wang** -- Head servant
- **Madam Lin** -- Wife of the deceased
- **Miss Bai** -- Daughter of the deceased
- **Chef Li** -- Family cook
- **Gardener Chen** -- Groundskeeper
- **Driver Zhou** -- Family chauffeur
- **Mr. Zhao** -- House guest

### Locations (8)
Each location uses a `Solid("#color")` background instead of image assets:

| Location          | Color    | Label            |
|-------------------|----------|------------------|
| Hall              | #8B7355  | `hall`           |
| Master Bedroom    | #8B0000  | `master_bedroom` |
| Guest Bedroom     | #4A6E4A  | `guest_bedroom`  |
| Kitchen           | #CD853F  | `kitchen`        |
| Garden            | #556B2F  | `garden`         |
| Pool              | #4682B4  | `pool`            |
| Study             | #6B3A2E  | `study`          |
| Hidden Room       | #2F2F2F  | `hidden_room`    |

The Hidden Room is inside the Study. It is unlocked by choosing "Look Around" in the Study.
Once discovered, it appears on the map.

### Navigation
- `quick_nav` screen: Always-visible panel on the right side showing current location and a "Map" button
- `map_screen` screen: Modal overlay with a 3x3 grid of location buttons. Hidden Room only appears after discovery.
- Navigation between locations uses `Jump()` actions with fade transitions

### Key Variables
- `current_location` -- Internal location ID string
- `current_location_name` -- Display name shown in quick_nav
- `hidden_room_found` -- Boolean, set to True when hidden room is discovered

## Resolution
1920x1080

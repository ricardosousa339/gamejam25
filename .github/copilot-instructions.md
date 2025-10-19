# River Cleanup Game - AI Coding Agent Instructions

## Project Overview

A Pygame-based 2D river cleanup game where players collect floating trash and dispose of it in appropriate bins. Built for Game Jam 2025, this project emphasizes cross-platform distribution with PyInstaller bundling.

## Architecture & Key Concepts

### Entry Point Flow
- `main.py` → `game.py` (Game class) → entities (`FloatingObject`, `TrashCan`)
- Single-file executable philosophy: All resources must work with PyInstaller's `_MEIPASS` temporary folder

### Critical Pattern: Resource Path Resolution
**Always use `resource_path()` from `utils.py` when loading assets:**

```python
# ❌ WRONG - Breaks in bundled executable
image = pygame.image.load('assets/rio.png')

# ✅ CORRECT - Works in dev and PyInstaller bundle
from utils import resource_path
image = pygame.image.load(resource_path('assets/rio.png'))
```

**Why**: PyInstaller extracts assets to `sys._MEIPASS` temp folder at runtime. Direct paths fail in production.

### Sprite Architecture
- All game entities inherit from `pygame.sprite.Sprite`
- Two main sprite groups in `game.py`: `all_sprites` (rendering) and `floating_objects` (logic)
- Objects self-manage movement via `update()` - no centralized physics engine

### River Flow System
The river uses a **dual-layer parallax effect**:
1. `rio.png` - Animated water texture (moves with `rio_x_offset`)
2. `margens.png` - Static riverbank overlay (no offset)

Both images tile horizontally to fill screen. Spawning logic adapts to flow direction (`RIVER_FLOW_SPEED` in `config.py`).

**Key coordinates**: Objects spawn within `river_band_top` to `river_band_bottom` (scaled from image space to screen space in `Game.__init__`).

## Configuration Philosophy

### Central Config Pattern
`config.py` is the single source of truth for:
- Game constants (`SCREEN_WIDTH`, `FPS`, `RIVER_FLOW_SPEED`)
- Object type definitions via `OBJECT_TYPES` dict mapping object keys to `ObjectType(type, image_path, scale)`
- Color palette and spawn rates

**When adding features**: Extract magic numbers to `config.py` immediately. Don't hardcode values in entity classes.

### Object Type System
```python
# config.py defines trash categories
OBJECT_TYPES = {
    "bottle": ObjectType("plastic", "./assets/lixo/garrafa.png", 1),
    "can": ObjectType("metal", "./assets/lixo/lata.png", 0.9),
    # type: category for trash can validation
    # image: path for loading
    # scale: size multiplier
}
```

To add new trash: Add entry to `OBJECT_TYPES`, place sprite in `assets/lixo/`, reference key in spawn logic.

## Build & Distribution Workflow

### Local Development
```bash
source venv/bin/activate  # Always activate first
python main.py            # Run game directly
```

### Building Executables
```bash
./build.sh                # Interactive build with auto-cleanup
# OR
pyinstaller --clean RiverCleanup.spec  # Manual build
```

**Critical**: `RiverCleanup.spec` is version controlled (`.gitignore` exception). Contains:
- `datas=[('assets', 'assets')]` - Bundles entire assets folder
- `console=False` - No terminal window on launch
- `onedir` mode - Executable + `_internal/` folder structure

### CI/CD Pipeline (GitHub Actions)
- **Trigger**: Push tags matching `v*` (e.g., `v1.0.0`)
- **Architecture**: Parallel Windows + Linux builds → Unified release job
- **Permissions**: Workflow needs `contents: write` to create releases
- **Artifacts**: Both platforms bundled into single GitHub release

**Creating a release**:
```bash
git tag v1.0.1
git push --tags  # Triggers .github/workflows/build.yml
```

## Development Conventions

### Import Organization
```python
# 1. Standard library
import pygame, random, sys

# 2. Local modules
from config import *  # Wildcard import for constants only
from utils import resource_path
```

### Coordinate System
- **Screen space**: 0,0 = top-left, positive Y goes down
- **River band**: Vertical slice where objects are allowed to spawn (not full screen height)
- Conversion: Image pixel coordinates → screen pixels via `self.scale_factor` in `game.py`

### Asset Management
- Background layers: `assets/rio.png`, `assets/margens.png`
- Trash sprites: `assets/lixo/*.png` (referenced in `config.py`)
- Unused assets exist (`crocodilo.png`, `pegador_*.png`) - planned features

## Common Pitfalls

1. **Asset paths**: Always wrap in `resource_path()`. Breaking this breaks PyInstaller builds.
2. **Sprite groups**: Objects must be added to both `floating_objects` AND `all_sprites` for proper lifecycle.
3. **River bounds**: Don't spawn outside `river_band_top`/`river_band_bottom` - objects will appear on riverbanks.
4. **Flow direction**: Check `RIVER_FLOW_SPEED` sign when implementing movement. Negative = left, positive = right.
5. **Build testing**: Run `pyinstaller --clean` before committing spec changes. Test actual executable, not just Python runtime.

## Testing & Debugging

No formal test suite exists. Manual validation:
```bash
# Test executable works post-build
cd dist/RiverCleanup/
./RiverCleanup  # Linux
# RiverCleanup.exe on Windows
```

Check for:
- Assets loading correctly (no missing textures)
- Objects spawning within river bounds
- Proper animation of water layer
- No console window appearing (windowed mode)

## Future Architecture Notes

Current TODO items indicate planned systems not yet implemented:
- **Trash can interactions**: `trash_can.py` has validation logic (`accepts_type()`) but no pickup system
- **Scoring penalties**: Framework exists but not connected to gameplay
- **Menu screens**: Single-state game (no scene manager)

When implementing these, maintain the pattern of entity self-sufficiency (update logic in entity classes, not centralized in `game.py`).

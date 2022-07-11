# Game
FPS: int = 30
ANIMATION_SPEED: int = 40  # how many frames per action

# Screen
SCREEN_WIDTH: int = 1080
SCREEN_HEIGHT: int = 720
CELL_MIN_PX_SIZE: int = 20
CELL_MAX_PX_SIZE: int = 80

# Animation
MIN_ANIMATION_SPEED = 10
MAX_ANIMATION_SPEED = 60
ANIMATION_SPEED_CHANGE = 2

# Colors
BLACK: tuple[int, int, int] = (0, 0, 0)
LIGHT_BLUE: tuple[int, int, int] = (138, 219, 239)

# Events
MOVE_SCREEN_BY_CLICK = 50
ZOOM_SCREEN_BY_CLICK = 5

# Algae
ALGA_SURFACING_STEPS: int = 15
ALGA_ENERGY_VALUE: int = 15
HOW_OFTEN_CYCLES_MAKING_ALGAE: int = 5

# Fish
FISH_VITALITY_SPOIL_RATE: int = 1

# Worm
WORM_FALLING_STEPS: int = 15
WORM_BOUNCE_STEPS: int = 20
WORM_ENERGY_VALUE: int = 15
NUM_OF_NEW_WORMS_AT_CYCLE: int = 3
HOW_OFTEN_CYCLES_MAKING_WORMS: int = 5

# Algae maker
MIN_ALGAE_TO_CREATE: int = 1
MAX_ALGAE_TO_CREATE: int = 3

# Fish
FISH_MIN_SPEED: int = 5
FISH_MAX_SPEED: int = 10
FISH_MIN_SIZE: int = 5
FISH_MAX_SIZE: int = 10
FISH_NEED_MULTI_VITALITY_TO_BREED: int = 2
MIN_FISH_TO_BIRTH: int = 1
MAX_FISH_TO_BIRTH: int = 2

# Evolution
EVOLUTION_DEVIATION_DIV: int = 10
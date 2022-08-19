# Game
FPS: int = 30

# Settings
SCREEN_DIMENSIONS: tuple[str, str, str] = ('1920x1080', '1080x720', '720x480')

# Screen
CELL_MIN_PX_SIZE: int = 20
CELL_MAX_PX_SIZE: int = 80

# Animation
START_ANIMATION_SPEED: int = 40
MIN_ANIMATION_SPEED: int = 5
MAX_ANIMATION_SPEED: int = 60
ANIMATION_SPEED_CHANGE: int = 3

# Colors
BLACK: tuple[int, int, int] = (0, 0, 0)
LIGHT_BLUE: tuple[int, int, int] = (138, 219, 239)
GRAY: tuple[int, int, int] = (220, 220, 220)

# Events
SCREEN_MOVE_CHANGE: int = 50
SCREEN_ZOOM_CHANGE: int = 5

# Algae
ALGA_SURFACING_STEPS: int = 15
ALGA_DEFAULT_ENERGY_VALUE: int = 15
ALGA_INTENSITY: int = 1
CHANCE_TO_PRODUCE_ALGAE: float = 0.30

# Worm
WORM_FALLING_STEPS: int = 15
WORM_BOUNCE_STEPS: int = 20
WORM_DEFAULT_ENERGY_VALUE: int = 30
CHANCE_TO_PRODUCE_WORMS: float = 0.80
WORM_INTENSITY: int = 1

# Fish
FISH_MIN_SPEED: int = 2
FISH_MAX_SPEED: int = 10
FISH_MIN_SIZE: int = 5
FISH_MAX_SIZE: int = 50
FISH_MIN_EYESIGHT: int = 1
FISH_MAX_EYESIGHT: int = 30
FISH_NEED_MULTI_VITALITY_TO_BREED: int = 3
MIN_FISH_REPRODUCE_AMOUNT: int = 1
MAX_FISH_REPRODUCE_AMOUNT: int = 2
FISH_VITALITY_SPOIL_COEFF: int = 5
CHANCE_TO_GET_PARENT_TRAIT: float = 0.90
CHANCE_TO_GET_NEW_TRAIT: float = 0.20
CHANCE_TO_BE_SMART: float = 0.70
CHANCE_TO_BE_PREDATOR: float = 0.20
PREDATOR_CHANCE_TO_DEFENCE: float = 0.5
CHANCE_SMART_FISH_DOES_RANDOM_MOVE: float = 0.05
CHANCE_FISH_GOES_TO_BOTTOM_FOR_FOOD: float = 0.65
CHANCE_FISH_GOES_FOR_FOOD: float = 0.80
CHANCE_FISH_DOES_NOT_RUN: float = 0.10
CNT_FISH_DIV: int = 20
EVOLUTION_DEVIATION_DIV: int = 10

# UI
UI_SCALE: float = 0.6
NUM_OF_SQUARES_IN_PANEL: int = 12
CURRENT_OBJ_IDX: int = 1
CYCLE_COUNT_IDX: int = 11
EDGE_UI_HEIGHT_RATIO: float = 0.08
TEXT_SIZE_RATIO: float = 0.4
TEXT_Y_OFFSET_RATIO: float = 0.1
EMPTY_SQUARES: set[int] = {2, 6, 9}

# Event Emitter
LEFT_MOUSE_BUTTON: int = 1

# Game
FPS: int = 30

# Screen
CELL_MIN_PX_SIZE: int = 20
CELL_MAX_PX_SIZE: int = 80

# Animation
ANIMATION_SPEED: int = 40  # how many frames per action
MIN_ANIMATION_SPEED = 5  # TODO: to jest troche mylące, bo im MIN_ANIMATION_SPEED jest mniejsze tym animacja może być szybsza
MAX_ANIMATION_SPEED = 60
ANIMATION_SPEED_CHANGE = 3

# Colors
BLACK: tuple[int, int, int] = (0, 0, 0)
LIGHT_BLUE: tuple[int, int, int] = (138, 219, 239)
GRAY: tuple[int, int, int] = (220, 220, 220)

# Events
SCREEN_MOVE_CHANGE = 50
SCREEN_ZOOM_CHANGE = 5

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
CHANCE_TO_PRODUCE_WORMS: int = 10  # in %

# Algae maker
MIN_ALGAE_TO_CREATE: int = 1
MAX_ALGAE_TO_CREATE: int = 3
CHANCE_TO_PRODUCE_ALGAE: int = 10  # in %

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

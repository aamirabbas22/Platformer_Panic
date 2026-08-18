from settings import * # Import game settings
from level import Level # Import the Level class
from pytmx.util_pygame import load_pygame # Load Tiled map files (tmx) with pygame compatability
from os.path import join # Safely construct file paths
from support import *
from data import Data
from ui import UI

class Gameplay: 
    def __init__(self, level_index=0):
        pygame.init() # Initialize all Pygame modules
        self.clock = pygame.time.Clock() # Create a clock to manage frame rate
        self.import_assets()
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.level_index = level_index

        # Pick level-specific music
        music_file = f'level_music_{level_index}.mp3'
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)  # Loop level music

        # Load a list of TMX tile maps and store it in a dictionary. (More will be added later)
        self.tmx_maps = {
            0: load_pygame(join('..', 'data', 'levels', 'test.tmx')),
            1: load_pygame(join('..', 'data', 'levels', '1.tmx')),
            1.5: load_pygame(join('..', 'data', 'levels', '1.5.tmx')),
            2: load_pygame(join('..', 'data', 'levels', '2.tmx')),
            2.5: load_pygame(join('..', 'data', 'levels', '2.5.tmx')),
            3: load_pygame(join('..', 'data', 'levels', '3.tmx')),
            3.5: load_pygame(join('..', 'data', 'levels', '3.5.tmx')),
            4: load_pygame(join('..', 'data', 'levels', '4.tmx')),
            4.5: load_pygame(join('..', 'data', 'levels', '4.5.tmx')),
            5: load_pygame(join('..', 'data', 'levels', '5.tmx')),
            5.5: load_pygame(join('..', 'data', 'levels', '5.5.tmx'))
            }
        # Create a Level instance using the loaded TMX map
        self.current_stage = Level(self.tmx_maps[level_index], self.level_frames, self.data, self.check_game_over, self.audio_files, self.level_index)
        
    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('..', 'graphics', 'level', 'flag'),
            'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('..', 'graphics', 'enemies', 'floor_spikes'),
            'palms': import_sub_folders('..', 'graphics', 'level', 'palms'),
            'candle': import_folder('..', 'graphics','level', 'candle'),
            'window': import_folder('..', 'graphics','level', 'window'),
            'big_chain': import_folder('..', 'graphics','level', 'big_chains'),
            'small_chain': import_folder('..', 'graphics','level', 'small_chains'),
            'candle_light': import_folder('..', 'graphics','level', 'candle light'),
            'player': import_sub_folders('..', 'graphics','player'),
            'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'saw_chain': import_image('..',  'graphics', 'enemies', 'saw', 'saw_chain'),
            'mover': import_folder('..', 'graphics', 'level', 'helicopter'),
            'boat': import_folder('..',  'graphics', 'objects', 'boat'),
            'spike': import_image('..',  'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('..',  'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'spider': import_folder('..', 'graphics','enemies', 'spider', 'run'),
            'clown': import_sub_folders('..', 'graphics','enemies', 'clown'),
            'pearl': import_image('..',  'graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('..', 'graphics', 'items'),
            'particle': import_folder('..', 'graphics', 'effects', 'particle'),
            'water_top': import_folder('..', 'graphics', 'level', 'water', 'top'),
            'water_body': import_image('..', 'graphics', 'level', 'water', 'body'),
            'bg_tiles': import_folder_dict('..', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('..', 'graphics','level', 'clouds', 'small'),
            'cloud_large': import_image('..', 'graphics','level', 'clouds', 'large_cloud')
        }

        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart': import_folder('..', 'graphics', 'ui', 'heart'), 
            'coin':import_image('..', 'graphics', 'ui', 'coin')
        }

        self.audio_files = {
            'coin': pygame.mixer.Sound(join('..', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('..', 'audio', 'attack.wav')),
            'jump': pygame.mixer.Sound(join('..', 'audio', 'jump.wav')), 
            'damage': pygame.mixer.Sound(join('..', 'audio', 'damage.wav')),
            'pearl': pygame.mixer.Sound(join('..', 'audio', 'pearl.wav')),
        }

    def check_game_over(self):
        from menu import game_over_screen, Game
        if self.data.health <= 0:
            final_score = self.data.coins # Based on coins since health = 0
            result = game_over_screen(final_score)

            if result == "retry":
                # Start the same level again
                self.__init__(self.level_index)  # re-init the Gameplay instance
                self.run()
            elif result == "menu":
                Game.run(self)
            else:
                pygame.quit()
                sys.exit()

    def run(self): 
        while True: # Core game loop
            dt = self.clock.tick() / 1000 # Time in seconds since last frame (used for movement/animations)
            for event in pygame.event.get(): # Event handling loop
                if event.type == pygame.QUIT: # If the window is closed
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(dt) # Run the current stage's logic and rendering
            self.ui.update(dt)
            self.check_game_over()

            pygame.display.update() # Update the full display surface to the screen
     
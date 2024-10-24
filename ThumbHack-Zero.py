import thumby
import random
import time
import math

# Constants
SCREEN_WIDTH = 72
SCREEN_HEIGHT = 40
FPS = 30

# Initialize
thumby.display.setFPS(FPS)

class VisualEffects:
    @staticmethod
    def draw_scanlines():
        for y in range(0, SCREEN_HEIGHT, 2):
            thumby.display.drawLine(0, y, SCREEN_WIDTH, y, 1)
    
    @staticmethod
    def draw_glitch_rect(x, y, width, height):
        if random.random() < 0.2:  # 20% chance of glitch
            offset = random.randint(-2, 2)
            width_mod = random.randint(-2, 2)
            thumby.display.drawRectangle(x + offset, y, 
                                       width + width_mod, height, 1)
    
    @staticmethod
    def draw_noise(intensity=0.1):
        for _ in range(int(SCREEN_WIDTH * SCREEN_HEIGHT * intensity)):
            x = random.randint(0, SCREEN_WIDTH-1)
            y = random.randint(0, SCREEN_HEIGHT-1)
            thumby.display.setPixel(x, y, 1)
    
    @staticmethod
    def draw_matrix_rain(offset):
        for x in range(0, SCREEN_WIDTH, 4):
            if random.random() < 0.3:
                y = (offset + x) % SCREEN_HEIGHT
                thumby.display.drawText("1", x, y, 1)
    
    @staticmethod
    def draw_hacking_border():
        # Draw corners with random binary
        for corner in [(0,0), (SCREEN_WIDTH-8,0), 
                      (0,SCREEN_HEIGHT-8), (SCREEN_WIDTH-8,SCREEN_HEIGHT-8)]:
            digit = "1" if random.random() > 0.5 else "0"
            thumby.display.drawText(digit, corner[0], corner[1], 1)

class MatrixEffect:
    def __init__(self):
        self.streams = []
        self.setup_streams()
        self.display_time = 180  # About 3 seconds at 60 FPS
        
    def setup_streams(self):
        for x in range(0, SCREEN_WIDTH, 6):
            self.streams.append({
                'x': x,
                'y': random.randint(-SCREEN_HEIGHT, 0),
                'length': random.randint(8, 16),
                'speed': random.randint(1, 2)
            })
    
    def update(self):
        for stream in self.streams:
            stream['y'] += stream['speed']
            if stream['y'] > SCREEN_HEIGHT:
                stream['y'] = random.randint(-SCREEN_HEIGHT, -10)
                stream['length'] = random.randint(8, 16)
                stream['speed'] = random.randint(1, 2)
    
    def draw(self):
        thumby.display.fill(0)
        for stream in self.streams:
            for i in range(stream['length']):
                y_pos = int(stream['y']) - (i * 6)
                if 0 <= y_pos < SCREEN_HEIGHT:
                    digit = '1' if random.random() > 0.5 else '0'
                    thumby.display.drawText(digit, stream['x'], y_pos, 1)

class GameState:
    def __init__(self):
        self.current_level = 1
        self.game_complete = False
        self.lives = 3
        self.score = 0
        
class HackingMinigame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.sequence = []
        self.player_sequence = []
        self.cursor_pos = 0
        self.time_left = 0
        self.success = False
        
    def generate_sequence(self):
        length = 3 + self.difficulty
        self.sequence = [random.choice(['U', 'D', 'L', 'R']) for _ in range(length)]
        self.time_left = 150 - (self.difficulty * 20)
        
    def check_sequence(self):
        return self.player_sequence == self.sequence

class FirewallBreaker:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.grid = [[0 for _ in range(6)] for _ in range(4)]
        self.cursor_x = 0
        self.cursor_y = 0
        self.target_pattern = []
        self.success = False
        self.time_left = 200
        
    def generate_puzzle(self):
        self.target_pattern = [(0, random.randint(0, 3))]
        for _ in range(2 + self.difficulty):
            last_x, last_y = self.target_pattern[-1]
            new_x = last_x + 1
            new_y = random.randint(max(0, last_y-1), min(3, last_y+1))
            self.target_pattern.append((new_x, new_y))

class DataExtractor:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.data_streams = []
        self.cursor_pos = 0
        self.captured_data = 0
        self.required_data = 5 + difficulty
        self.success = False
        self.time_left = 300
        
    def generate_streams(self):
        self.data_streams = []
        for _ in range(4):
            stream = {
                'y': random.randint(0, SCREEN_HEIGHT-8),
                'speed': random.randint(1, 3),
                'is_data': random.random() < 0.3
            }
            self.data_streams.append(stream)
            
def show_matrix_intro():
    matrix = MatrixEffect()
    effects = VisualEffects()
    last_note_time = 0
    note_interval = 10
    notes = [523, 587, 659, 783, 880, 987, 1046, 1174]
    note_index = 0
    
    while matrix.display_time > 0:
        # Update and draw matrix effect
        matrix.update()
        matrix.draw()
        
        # Add additional effects
        if random.random() < 0.1:
            effects.draw_scanlines()
        if random.random() < 0.05:
            effects.draw_noise(0.02)
        effects.draw_hacking_border()
        
        # Play hacker-style sounds
        if matrix.display_time % note_interval == 0:
            thumby.audio.play(notes[note_index], 50)
            note_index = (note_index + 1) % len(notes)
        
        matrix.display_time -= 1
        thumby.display.update()
    
    # Transition effect to title screen
    for i in range(5):
        thumby.display.fill(i % 2)  # Flash screen
        thumby.display.update()
        thumby.audio.play(1200 - i * 100, 50)
        time.sleep(0.1)

def show_intro_sequence():
    effects = VisualEffects()
    messages = [
        "SYSTEM BREACH",
        "INITIATING...",
        "ACCESS DENIED",
        "BYPASSING...",
        "ACCESS GRANTED"
    ]
    
    for msg in messages:
        for frame in range(30):  # Show each message for 30 frames
            thumby.display.fill(0)
            
            # Add visual effects
            if frame % 15 == 0:
                effects.draw_scanlines()
            if random.random() < 0.1:
                effects.draw_noise(0.03)
            effects.draw_hacking_border()
            
            # Draw message with potential glitch
            x = (SCREEN_WIDTH - len(msg) * 6) // 2
            y = SCREEN_HEIGHT // 2 - 4
            if random.random() < 0.1:
                x += random.randint(-1, 1)
                y += random.randint(-1, 1)
            
            thumby.display.drawText(msg, x, y, 1)
            thumby.display.update()
            
            if frame % 10 == 0:
                thumby.audio.play(random.randint(800, 1200), 50)
            
            time.sleep(0.03)

def show_title_screen():
    effects = VisualEffects()
    frame_count = 0
    
    while not thumby.buttonA.pressed():
        thumby.display.fill(0)
        frame_count += 1
        
        # Draw background matrix rain
        effects.draw_matrix_rain(frame_count)
        
        # Draw title with "hacker" effect
        title = "ThumbHack"
        subtitle = "Zero"
        prompt = "Press A"
        
        # Main title with glitch effect
        x = (SCREEN_WIDTH - len(title) * 6) // 2
        y = 10
        
        # Severe glitch effect occasionally
        if random.random() < 0.05:  # 5% chance of major glitch
            for i in range(3):
                glitch_x = x + random.randint(-2, 2)
                glitch_y = y + random.randint(-1, 1)
                thumby.display.drawText(title, glitch_x, glitch_y, 1)
        else:
            thumby.display.drawText(title, x, y, 1)
        
        # Subtitle with minor glitch
        x = (SCREEN_WIDTH - len(subtitle) * 6) // 2
        if random.random() < 0.1:
            x += random.randint(-1, 1)
        thumby.display.drawText(subtitle, x, 20, 1)
        
        # Blinking prompt with scan effect
        if (frame_count // 30) % 2:
            x = (SCREEN_WIDTH - len(prompt) * 6) // 2
            thumby.display.drawText(prompt, x, 30, 1)
        
        # Add decorative elements
        effects.draw_hacking_border()
        if random.random() < 0.05:
            effects.draw_scanlines()
        effects.draw_noise(0.02)
        
        if thumby.buttonA.pressed():
            thumby.audio.play(1200, 100)
        
        thumby.display.update()

def run_level_one():
    """Password Sequence Hack"""
    game = HackingMinigame(1)
    game.generate_sequence()
    effects = VisualEffects()
    frame_count = 0
    
    while game.time_left > 0:
        thumby.display.fill(0)
        frame_count += 1
        
        # Add background effects
        if frame_count % 60 < 30:
            effects.draw_scanlines()
        if random.random() < 0.05:
            effects.draw_noise(0.02)
        
        # Draw timer with glitch effect
        timer_x = 2
        if random.random() < 0.1:
            timer_x += random.randint(-1, 1)
        thumby.display.drawText(str(game.time_left//30), timer_x, 2, 1)
        
        # Draw sequence to match
        for i, direction in enumerate(game.sequence):
            x = 10 + (i * 10)
            effects.draw_glitch_rect(x-1, 9, 8, 10)
            thumby.display.drawText(direction, x, 10, 1)
        
        # Draw player input with effects
        for i, direction in enumerate(game.player_sequence):
            x = 10 + (i * 10)
            if random.random() < 0.05:
                x += random.randint(-1, 1)
            thumby.display.drawText(direction, x, 25, 1)
        
        effects.draw_hacking_border()
        
        # Handle input
        if thumby.buttonU.pressed():
            if len(game.player_sequence) < len(game.sequence):
                game.player_sequence.append('U')
                thumby.audio.play(1200, 50)
        elif thumby.buttonD.pressed():
            if len(game.player_sequence) < len(game.sequence):
                game.player_sequence.append('D')
                thumby.audio.play(1200, 50)
        elif thumby.buttonL.pressed():
            if len(game.player_sequence) < len(game.sequence):
                game.player_sequence.append('L')
                thumby.audio.play(1200, 50)
        elif thumby.buttonR.pressed():
            if len(game.player_sequence) < len(game.sequence):
                game.player_sequence.append('R')
                thumby.audio.play(1200, 50)
        elif thumby.buttonB.pressed():
            if game.player_sequence:
                game.player_sequence.pop()
                thumby.audio.play(800, 50)
        
        # Check win condition
        if len(game.player_sequence) == len(game.sequence):
            if game.check_sequence():
                return True
            else:
                game.player_sequence = []
        
        game.time_left -= 1
        thumby.display.update()
    
    return False

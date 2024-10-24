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
        self.time_left = 150 - (self.difficulty * 20)  # Less time for harder levels
        
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
        # Create a pattern of nodes to connect
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
    last_note_time = 0
    note_interval = 10
    notes = [523, 587, 659, 783, 880, 987, 1046, 1174]
    note_index = 0
    
    while matrix.display_time > 0:
        # Update matrix effect
        matrix.update()
        matrix.draw()
        
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
    messages = [
        "SYSTEM BREACH",
        "INITIATING...",
        "ACCESS DENIED",
        "BYPASSING...",
        "ACCESS GRANTED"
    ]
    
    for msg in messages:
        thumby.display.fill(0)
        x = (SCREEN_WIDTH - len(msg) * 6) // 2
        y = SCREEN_HEIGHT // 2 - 4
        thumby.display.drawText(msg, x, y, 1)
        thumby.display.update()
        thumby.audio.play(random.randint(800, 1200), 50)
        time.sleep(0.5)
        
def show_title_screen():
    while not thumby.buttonA.pressed():
        thumby.display.fill(0)
        
        # Draw title with "hacker" effect
        title = "ThumbHack"
        subtitle = "Zero"
        prompt = "Press A"
        
        # Main title with glitch effect
        x = (SCREEN_WIDTH - len(title) * 6) // 2
        y = 10
        if random.random() < 0.1:  # Occasional glitch effect
            x += random.randint(-1, 1)
        thumby.display.drawText(title, x, y, 1)
        
        # Subtitle
        x = (SCREEN_WIDTH - len(subtitle) * 6) // 2
        thumby.display.drawText(subtitle, x, 20, 1)
        
        # Blinking prompt
        if (time.ticks_ms() // 500) % 2:  # Blink every half second
            x = (SCREEN_WIDTH - len(prompt) * 6) // 2
            thumby.display.drawText(prompt, x, 30, 1)
            
        # Random matrix-style characters in corners
        if random.random() < 0.3:
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            digit = '1' if random.random() > 0.5 else '0'
            thumby.display.drawText(digit, x, y, 1)
        
        thumby.display.update()

def run_level_one():
    """Password Sequence Hack"""
    game = HackingMinigame(1)
    game.generate_sequence()
    
    while game.time_left > 0:
        thumby.display.fill(0)
        
        # Draw timer
        thumby.display.drawText(str(game.time_left//30), 2, 2, 1)
        
        # Draw sequence to match
        for i, direction in enumerate(game.sequence):
            x = 10 + (i * 10)
            thumby.display.drawText(direction, x, 10, 1)
            
        # Draw player input
        for i, direction in enumerate(game.player_sequence):
            x = 10 + (i * 10)
            thumby.display.drawText(direction, x, 25, 1)
            
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

def run_level_two():
    """Firewall Node Connection"""
    game = FirewallBreaker(2)
    game.generate_puzzle()
    
    while game.time_left > 0:
        thumby.display.fill(0)
        
        # Draw timer
        thumby.display.drawText(str(game.time_left//30), 2, 2, 1)
        
        # Draw grid and nodes
        for x, y in game.target_pattern:
            screen_x = 10 + (x * 10)
            screen_y = 10 + (y * 8)
            thumby.display.drawRectangle(screen_x, screen_y, 4, 4, 1)
            
        # Draw cursor
        cursor_x = 10 + (game.cursor_x * 10)
        cursor_y = 10 + (game.cursor_y * 8)
        thumby.display.drawRectangle(cursor_x-1, cursor_y-1, 6, 6, 1)
        
        # Handle input
        if thumby.buttonU.pressed() and game.cursor_y > 0:
            game.cursor_y -= 1
            thumby.audio.play(1200, 50)
        elif thumby.buttonD.pressed() and game.cursor_y < 3:
            game.cursor_y += 1
            thumby.audio.play(1200, 50)
        elif thumby.buttonR.pressed() and game.cursor_x < 5:
            game.cursor_x += 1
            thumby.audio.play(1200, 50)
        elif thumby.buttonL.pressed() and game.cursor_x > 0:
            game.cursor_x -= 1
            thumby.audio.play(1200, 50)
            
        # Check win condition
        if (game.cursor_x, game.cursor_y) == game.target_pattern[-1]:
            return True
            
        game.time_left -= 1
        thumby.display.update()
    
    return False

def run_level_three():
    """Data Stream Capture"""
    game = DataExtractor(3)
    game.generate_streams()
    
    while game.time_left > 0:
        thumby.display.fill(0)
        
        # Draw timer and progress
        thumby.display.drawText(str(game.time_left//30), 2, 2, 1)
        thumby.display.drawText(f"{game.captured_data}/{game.required_data}", 40, 2, 1)
        
        # Update and draw data streams
        for stream in game.data_streams:
            stream['y'] += stream['speed']
            if stream['y'] > SCREEN_HEIGHT:
                stream['y'] = -8
                stream['is_data'] = random.random() < 0.3
            
            # Draw stream
            if stream['is_data']:
                thumby.display.drawText("$", game.cursor_pos, int(stream['y']), 1)
            else:
                thumby.display.drawText("0", game.cursor_pos, int(stream['y']), 1)
        
        # Handle input
        if thumby.buttonL.pressed() and game.cursor_pos > 0:
            game.cursor_pos -= 8
            thumby.audio.play(1200, 50)
        elif thumby.buttonR.pressed() and game.cursor_pos < SCREEN_WIDTH-8:
            game.cursor_pos += 8
            thumby.audio.play(1200, 50)
        elif thumby.buttonA.pressed():
            # Try to capture data
            for stream in game.data_streams:
                if (abs(stream['y'] - SCREEN_HEIGHT//2) < 4 and 
                    stream['is_data']):
                    game.captured_data += 1
                    thumby.audio.play(2000, 100)
                    stream['is_data'] = False
        
        # Draw capture zone
        thumby.display.drawLine(0, SCREEN_HEIGHT//2, 
                              SCREEN_WIDTH, SCREEN_HEIGHT//2, 1)
        
        # Check win condition
        if game.captured_data >= game.required_data:
            return True
            
        game.time_left -= 1
        thumby.display.update()
    
    return False

def show_game_over(success):
    thumby.display.fill(0)
    if success:
        msg = "HACK COMPLETE"
    else:
        msg = "HACK FAILED"
    
    x = (SCREEN_WIDTH - len(msg) * 6) // 2
    y = SCREEN_HEIGHT // 2 - 4
    thumby.display.drawText(msg, x, y, 1)
    thumby.display.update()
    time.sleep(2)

def show_level_complete(level):
    thumby.display.fill(0)
    thumby.display.drawText(f"LEVEL {level}", 15, 10, 1)
    thumby.display.drawText("COMPLETE", 12, 20, 1)
    thumby.display.update()
    time.sleep(2)

def main():
    while True:
        # Show Matrix intro first
        show_matrix_intro()
        
        # Then show title screen
        show_title_screen()
        
        # Start the game sequence
        show_intro_sequence()
        game_state = GameState()
        
        # Level 1: Password Sequence
        if run_level_one():
            show_level_complete(1)
            
            # Level 2: Firewall Nodes
            if run_level_two():
                show_level_complete(2)
                
                # Level 3: Data Extraction
                if run_level_three():
                    show_game_over(True)
                else:
                    show_game_over(False)
            else:
                show_game_over(False)
        else:
            show_game_over(False)
        
        # Wait a moment before allowing restart
        time.sleep(1)
        
        # Show "Press A to restart" message
        thumby.display.fill(0)
        msg = "Press A"
        x = (SCREEN_WIDTH - len(msg) * 6) // 2
        y = SCREEN_HEIGHT // 2 - 4
        thumby.display.drawText(msg, x, y, 1)
        thumby.display.update()
        
        # Wait for button press
        while not thumby.buttonA.pressed():
            time.sleep(0.1)
        
        # Play restart sound
        thumby.audio.play(1000, 100)
        time.sleep(0.2)

# Start the game
if __name__ == "__main__":
    main()

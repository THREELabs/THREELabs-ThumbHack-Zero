import thumby
import random
import time

# Constants
SCREEN_WIDTH = 72
SCREEN_HEIGHT = 40
FPS = 30

# Initialize the display
thumby.display.setFPS(FPS)

class MatrixEffect:
    def __init__(self):
        self.streams = []
        self.setup_streams()
        self.music_timer = 0
        self.note_index = 0
        # Direction of movement (default is up)
        self.direction = 'up'
        # Movement speeds
        self.speed_x = 0
        self.speed_y = -1  # Default upward movement
        
        # Cyberpunk-style musical notes (frequencies)
        self.music_notes = [
            523,  # C5
            587,  # D5
            659,  # E5
            783,  # G5
            880,  # A5
            987,  # B5
            1046, # C6
            1174  # D6
        ]
        
    def setup_streams(self):
        # Create streams of 1s and 0s
        for x in range(0, SCREEN_WIDTH, 6):
            self.streams.append({
                'x': x,
                'y': random.randint(-SCREEN_HEIGHT, 0),
                'length': random.randint(8, 16),
                'speed': random.randint(1, 2)
            })
    
    def handle_input(self):
        # Reset speeds
        self.speed_x = 0
        self.speed_y = 0
        
        # Check directional input
        if thumby.buttonU.pressed():
            self.speed_y = -1
            self.direction = 'up'
        elif thumby.buttonD.pressed():
            self.speed_y = 1
            self.direction = 'down'
        elif thumby.buttonL.pressed():
            self.speed_x = -1
            self.direction = 'left'
        elif thumby.buttonR.pressed():
            self.speed_x = 1
            self.direction = 'right'
        else:
            # Default movement (up) if no button is pressed
            self.speed_y = -1
            self.direction = 'up'
    
    def update_music(self):
        self.music_timer += 1
        if self.music_timer >= 10:
            self.music_timer = 0
            freq = self.music_notes[self.note_index]
            thumby.audio.play(freq, 50)
            self.note_index = (self.note_index + 1) % len(self.music_notes)
            if random.random() < 0.3:
                self.note_index = random.randint(0, len(self.music_notes) - 1)
    
    def update(self):
        self.handle_input()
        self.update_music()
        
        for stream in self.streams:
            # Update position based on current direction
            stream['x'] += self.speed_x * stream['speed']
            stream['y'] += self.speed_y * stream['speed']
            
            # Handle wrapping based on direction
            if self.direction == 'up':
                if stream['y'] + stream['length'] * 6 < 0:
                    stream['y'] = SCREEN_HEIGHT
                    stream['length'] = random.randint(8, 16)
                    stream['speed'] = random.randint(1, 2)
            elif self.direction == 'down':
                if stream['y'] > SCREEN_HEIGHT:
                    stream['y'] = -stream['length'] * 6
                    stream['length'] = random.randint(8, 16)
                    stream['speed'] = random.randint(1, 2)
            elif self.direction == 'left':
                if stream['x'] + 6 < 0:
                    stream['x'] = SCREEN_WIDTH
                    stream['y'] = random.randint(0, SCREEN_HEIGHT)
                    stream['length'] = random.randint(8, 16)
                    stream['speed'] = random.randint(1, 2)
            elif self.direction == 'right':
                if stream['x'] > SCREEN_WIDTH:
                    stream['x'] = -6
                    stream['y'] = random.randint(0, SCREEN_HEIGHT)
                    stream['length'] = random.randint(8, 16)
                    stream['speed'] = random.randint(1, 2)
    
    def draw(self):
        thumby.display.fill(0)
        for stream in self.streams:
            for i in range(stream['length']):
                if self.direction in ['up', 'down']:
                    x_pos = int(stream['x'])
                    y_pos = int(stream['y']) - (i * 6) if self.direction == 'up' else int(stream['y']) + (i * 6)
                else:  # left or right
                    x_pos = int(stream['x']) - (i * 6) if self.direction == 'left' else int(stream['x']) + (i * 6)
                    y_pos = int(stream['y'])
                
                if (0 <= x_pos < SCREEN_WIDTH and 0 <= y_pos < SCREEN_HEIGHT):
                    digit = '1' if random.random() > 0.5 else '0'
                    thumby.display.drawText(digit, x_pos, y_pos, 1)

def show_welcome():
    thumby.display.fill(0)
    text = "Welcome NEO"
    x = (SCREEN_WIDTH - len(text) * 6) // 2
    y = (SCREEN_HEIGHT - 8) // 2
    
    for freq in [400, 800, 1200]:
        thumby.display.fill(0)
        thumby.display.update()
        thumby.audio.play(freq, 100)
        time.sleep(0.2)
        thumby.display.drawText(text, x, y, 1)
        thumby.display.update()
        time.sleep(0.2)

def show_menu():
    selected = 0
    options = ["Enter Matrix", "Exit"]
    
    while True:
        thumby.display.fill(0)
        
        for i, option in enumerate(options):
            x = (SCREEN_WIDTH - len(option) * 6) // 2
            y = SCREEN_HEIGHT // 2 - 8 + (i * 16)
            if i == selected:
                thumby.display.drawRectangle(x-2, y-2, len(option) * 6 + 4, 12, 1)
            thumby.display.drawText(option, x, y, 1)
        
        thumby.display.update()
        
        if thumby.buttonU.pressed():
            if selected > 0:
                selected -= 1
                thumby.audio.play(1000, 50)
        elif thumby.buttonD.pressed():
            if selected < len(options) - 1:
                selected += 1
                thumby.audio.play(800, 50)
        elif thumby.buttonA.pressed():
            thumby.audio.play(1200, 100)
            return selected

def main():
    while True:
        choice = show_menu()
        
        if choice == 0:  # Enter Matrix
            show_welcome()
            
            matrix = MatrixEffect()
            while True:
                if thumby.buttonA.pressed() or thumby.buttonB.pressed():
                    thumby.audio.play(500, 100)
                    break
                    
                matrix.update()
                matrix.draw()
                thumby.display.update()
                
        else:  # Exit
            for freq in [1200, 800, 400]:
                thumby.audio.play(freq, 100)
                time.sleep(0.1)
            break

# Start the application
main()

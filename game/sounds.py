import pygame
import numpy as np

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.create_sounds()
    
    def create_sounds(self):
        """Create simple sound effects using numpy and pygame"""
        # Paddle hit sound (short beep)
        self.sounds['paddle_hit'] = self.generate_tone(440, 0.1, 'sine')
        
        # Wall bounce sound (lower tone)
        self.sounds['wall_bounce'] = self.generate_tone(330, 0.08, 'sine')
        
        # Score sound (ascending tone)
        self.sounds['score'] = self.generate_ascending_tone(220, 440, 0.3)
    
    def generate_tone(self, frequency, duration, wave_type='sine'):
        """Generate a simple tone"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            if wave_type == 'sine':
                wave = np.sin(frequency * 2 * np.pi * time)
            elif wave_type == 'square':
                wave = 1 if np.sin(frequency * 2 * np.pi * time) > 0 else -1
            else:
                wave = np.sin(frequency * 2 * np.pi * time)
            
            # Apply envelope to avoid clicks
            envelope = 1.0 if i < frames * 0.1 or i > frames * 0.9 else 0.8
            wave *= envelope
            
            arr[i] = [wave * 0.3, wave * 0.3]  # Stereo, lower volume
        
        return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
    
    def generate_ascending_tone(self, start_freq, end_freq, duration):
        """Generate an ascending tone for scoring"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            # Linear frequency sweep
            freq = start_freq + (end_freq - start_freq) * (time / duration)
            wave = np.sin(freq * 2 * np.pi * time)
            
            # Apply envelope
            envelope = 1.0 if i < frames * 0.2 or i > frames * 0.8 else 0.7
            wave *= envelope
            
            arr[i] = [wave * 0.3, wave * 0.3]
        
        return pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

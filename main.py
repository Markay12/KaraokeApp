import tkinter as tk
import pygame
import mido
import time
import threading

class KaraokeApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Setup pygame mixer
        pygame.init()
        pygame.mixer.init()

        # Initialize song state
        self.song_loaded = False

        # Setup GUI
        self.title('Karaoke App')
        self.geometry('600x600')

        # Create a text area for lyrics
        self.lyrics_text = tk.Text(self, width=50)
        self.lyrics_text.pack(pady=20)

        # Create Play, Pause, Stop buttons
        self.play_button = tk.Button(self, text="Play", command=self.play_song)
        self.play_button.pack(pady=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_song)
        self.stop_button.pack(pady=10)

    def load_song(self, midi_file):
        self.mid = mido.MidiFile(midi_file)
        pygame.mixer.music.load(midi_file)
        self.song_loaded = True

    def play_song(self):
        if not self.song_loaded:
            print("No song loaded!")
            return

        pygame.mixer.music.play()

        def run_lyrics():
            for msg in self.mid.play():
                if msg.type == 'lyrics':
                    self.lyrics_text.insert(tk.END, msg.text + '\n')
                    self.lyrics_text.see(tk.END)

        threading.Thread(target=run_lyrics).start()

    def stop_song(self):
        if not self.song_loaded:
            print("No song loaded!")
            return

        pygame.mixer.music.stop()


# Create and start the application
app = KaraokeApp()
app.load_song('AUD_HTX0525.mid')  # Make sure to replace this with your MIDI file
app.mainloop()

import tkinter as tk
from tkinter import filedialog
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class JK_MusicPlayer:
    def __init__(self, master):
        self.master = master
        master.title("JK Music Player")
        master.iconbitmap("JK.ico")
        master.geometry("400x300")
        #master.config(bg="#bdbdbd")

        # Initialize Pygame mixer for playing music
        pygame.mixer.init()

        # Create the user interface
        self.song_label = tk.Label(master, text="No song selected")
        self.song_label.pack()

        self.select_button = tk.Button(master, text="Select Song", command=self.select_song)
        self.select_button.pack()

        self.play_button = tk.Button(master, text="Play", command=self.play_song, state=tk.DISABLED)
        self.play_button.pack()

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_song, state=tk.DISABLED)
        self.pause_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_song, state=tk.DISABLED)
        self.stop_button.pack()

        self.loop_button = tk.Button(master, text="Loop", command=self.toggle_loop, state=tk.DISABLED)
        self.loop_button.pack()
                
        self.volume_slider = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack()

        #self.progress_bar = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
        #self.progress_bar.pack()

        self.loop_enabled = False
        
    def select_song(self):
        # Open a file dialog to select a song
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a Song", filetypes=[("Audio Files", "*.mp3;*.wav")])

        if file_path:
            # Update the label to show the selected song
            self.song_label.config(text=os.path.basename(file_path))

            # Save the file path for later use
            self.song_file_path = file_path

            # Enable the play button
            self.play_button.config(state=tk.NORMAL)

    def play_song(self):
        # Load and play the selected song using Pygame mixer
        pygame.mixer.music.load(self.song_file_path)
        pygame.mixer.music.play()

        # Enable and disable appropriate buttons
        self.play_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.loop_button.config(state=tk.NORMAL)

    def pause_song(self):
        # Pause or unpause the currently playing song
        if pygame.mixer.music.get_busy():
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.pause()
                self.paused = True
                self.pause_button.config(text="Resume")
            else:
                pygame.mixer.music.unpause()
                self.paused = False
                self.pause_button.config(text="Pause")


    def stop_song(self):
        # Stop the currently playing song
        pygame.mixer.music.stop()

        # Enable and disable appropriate buttons
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.loop_button.config(state=tk.DISABLED)
        self.loop_enabled = False

    def toggle_loop(self):
       # Toggle looping of the currently playing song
       if self.loop_enabled:
           pygame.mixer.music.set_endevent(pygame.constants.NOEVENT)
           self.loop_enabled = False
           self.loop_button.config(relief=tk.RAISED)
       else:
           pygame.mixer.music.set_endevent(pygame.USEREVENT)
           self.loop_enabled = True
           self.loop_button.config(relief=tk.SUNKEN)



    def set_volume(self, value):
        volume = float(value) / 100
        pygame.mixer.music.set_volume(volume)

    
root = tk.Tk()
music_player = JK_MusicPlayer(root)
root.mainloop()
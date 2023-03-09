import pygame
import tkinter as tk

# create a tkinter window
root = tk.Tk()

# create a progress bar widget
progress_bar = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
progress_bar.pack()

# load the music file
pygame.mixer.music.load("m.mp3")

# get the length of the music file
music_length = pygame.mixer.music.get_length()

# function to update the progress bar
def update_progress_bar():
    current_pos = pygame.mixer.music.get_pos() / 1000
    progress = current_pos / music_length * 100
    progress_bar.set(progress)
    root.after(100, update_progress_bar)  # call this function again after 100ms

# start playing the music
pygame.mixer.music.play()

# call the update_progress_bar() function
update_progress_bar()

# start the tkinter event loop
root.mainloop()

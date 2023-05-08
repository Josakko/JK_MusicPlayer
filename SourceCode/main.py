from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os
from mutagen.mp3 import MP3
from tkinter import ttk
import time
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


class JKMusicPlayer:
    def __init__(self, root):
        self.root = root

        window_width = 1000
        window_hight = 600

        monitor_width = self.root.winfo_screenwidth()
        monitor_hight = self.root.winfo_screenheight()

        x = (monitor_width / 2) - (window_width / 2)
        y = (monitor_hight / 2) - (window_hight / 2)

        self.root.geometry(f'{window_width}x{window_hight}+{int(x)}+{int(y)}')
        self.root.minsize(800, 600)
        self.root.iconbitmap("assets/JK.ico")
        self.root.title("JK MusicPlayer")
        self.root.config(bg="#dbdbdb")
        #self.root.resizable(False, False)
        self.font = ("Helvetica", 14)
        self.bg = "#bde6fb" #bg=self.bg
        self.fg = "#1e2529" #fg=self.fg
        self.playing = False
        pygame.mixer.init()

        self.list_frame = Frame(self.root)
        self.list_frame.pack(fill=Y, expand=True)

        self.y_scrollbar = Scrollbar(self.list_frame)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)
        
        #self.x_scrollbar = Scrollbar(self.list_frame, orient=HORIZONTAL)
        #self.x_scrollbar.pack(side=BOTTOM, fill=X)
        
        self.playlist = Listbox(self.list_frame, yscrollcommand=self.y_scrollbar.set, width=140, height=15, font=self.font, ) # xscrollcommand=self.x_scrollbar.set
        self.playlist.pack(fill=Y, expand=True)

        self.playlist.bind("<Button-1>", self.deselect)

        self.y_scrollbar.config(command=self.playlist.yview)
        #self.x_scrollbar.config(command=self.playlist.xview)

        self.load_btn = Button(self.root, text="Load Folder", command=self.open_folder, font=self.font, width=20)
        self.load_btn.pack()

        self.time_frame = Frame(self.root)
        self.time_frame.pack(fill=X)
        
        self.time_lbl = Label(self.time_frame, text="0:00 / 0:00", font=self.font)
        self.time_lbl.pack(side=RIGHT, padx=10)
        
        self.time_scale = ttk.Scale(self.time_frame, from_=0, state="disabled", value=0, command=self.len_scale)
        self.time_scale.pack(side=LEFT, fill=X, expand=True, padx=15)

        self.control_frame = Frame(root, bg="#1e2529")
        self.control_frame.pack(side=BOTTOM, fill=X)
        self.control_frame.columnconfigure([0, 2, 4], weight=1)
        self.control_frame.columnconfigure([1, 3], weight=0)

        self.pause_img = PhotoImage(file="assets/pause.png")
        self.resume_img = PhotoImage(file="assets/resume.png")
        self.next_img = PhotoImage(file="assets/next.png")
        self.prev_img = PhotoImage(file="assets/previous.png")

        self.status_lbl = Label(self.control_frame, text="", font=self.font, fg=self.bg, bg=self.fg)
        self.status_lbl.grid(row=0, column=0, padx=5, sticky=W)

        self.play_btn = Button(self.control_frame, text="Play", command=self.play, font=("Helvetica", 14, "bold"), width=15, bg=self.bg, fg=self.fg, state="disabled")
        self.play_btn.grid(row=1, column=0, padx=20, sticky=W)

        self.prev_btn = Button(self.control_frame, image=self.prev_img, state="disabled", bg=self.bg, command=self.prev)
        self.prev_btn.grid(row=1, column=1, sticky=E)

        self.toggle_pause_btn = Button(self.control_frame, text="Pause", image=self.pause_img, command=self.toggle_pause, font=self.font, state="disabled", bg=self.bg, fg=self.fg)
        self.toggle_pause_btn.grid(row=1, column=2, pady=30, ipadx=10)
        self.root.bind('<space>', self.space)

        self.next_btn = Button(self.control_frame, image=self.next_img, state="disabled", bg=self.bg, fg=self.fg, command=self.next)
        self.next_btn.grid(row=1, column=3, sticky=W)

        self.vol_scale = ttk.Scale(self.control_frame, command=self.vol, from_=0, to=1, value=1, length=200)
        self.vol_scale.grid(row=1, column=4, padx=15, sticky=E)

        #self.time_stamp = 0
        self.scale_time_stamp = 0
        
        
    def space(self, event):
        self.toggle_pause_btn.invoke()


    def deselect(self, event):
        self.playlist.selection_clear(0, END)


    def open_folder(self):
        initialdir = os.path.join('C:\\', 'Users', os.getlogin(), 'Music')
        self.dir = filedialog.askdirectory(initialdir=initialdir)
        if not self.dir:
            self.dir = self.path
            return
        pygame.mixer.music.stop()
        self.playlist.delete(0, END)
        self.status_lbl.configure(text="")
        for file in os.listdir(self.dir):
            if file.endswith(".mp3"): # or file.endswith(".wav")
                song = os.path.splitext(file)[0]
                self.playlist.insert(END, song)
        self.play_btn.configure(state="normal")
        self.path = self.dir
        
    def length(self):
        try:
            #print(self.time_stamp)
            self.time_stamp = pygame.mixer.music.get_pos() / 1000 + self.scale_time_stamp
            #print(self.time_stamp)
            self.time_scale.configure(value=self.time_stamp)
            time_ = time.strftime('%M:%S', time.gmtime(self.time_stamp))
            try:
                song = MP3(self.song)
                duration_ = song.info.length
                self.time_scale.configure(from_=0, to=duration_)
                self.duration = time.strftime("%M:%S", time.gmtime(duration_))
                
                self.time_lbl.configure(text=f"{time_} / {self.duration}")
            except Exception as e:
                #print(e)
                self.time_lbl.configure(text=f"{time_} / 0:00")
                pass

            #print(round(duration_),  round(time_stamp))
            #if round(duration_) == round(time_stamp):
            #    self.time_lbl.configure(text=f"{duration} / {duration}")
            #    self.time_scale.set(duration)
        except Exception as e:
            #print(e)
            pass
        #print(f"{time_}   {self.time_scale.get()}")
        self.time_lbl.after(1000, self.length)


    def len_scale(self, value):
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(self.song)
            pygame.mixer.music.play(loops=0, start=int(self.time_scale.get()))
            self.time_lbl.configure(text=f"{time.strftime('%M:%S', time.gmtime(pygame.mixer.music.get_pos() / 1000 + self.scale_time_stamp))} / {self.duration}")
        except Exception as e:
            #print(e)
            return
        self.scale_time_stamp = int(self.time_scale.get())
        #print(self.scale_time_stamp)



    def next(self):
        self.playing = self.playing + 1
        if self.playlist.get(self.playing) == "": 
            self.playing = self.playing - 1
            return
        self.song = f"{self.dir}\{self.playlist.get(self.playing)}.mp3"
        try:
            pygame.mixer.music.load(self.song)
        except:
            self.playing = self.playing - 1
            return
        self.deselect("x")
        self.playlist.selection_set(self.playing)
        self.status_lbl.configure(text=f"Playing: {self.playlist.get(self.playing)}")
        self.time_scale.set(0)
        pygame.mixer.music.play(loops=0)
  
  
    def prev(self):
        self.playing = self.playing - 1
        if self.playlist.get(self.playing) == "": 
            self.playing = self.playing + 1
            return
        self.song = f"{self.dir}\{self.playlist.get(self.playing)}.mp3"
        try:
            pygame.mixer.music.load(self.song)
        except:
            self.playing = self.playing + 1
            return
        self.deselect("x")
        self.playlist.selection_set(self.playing)
        self.status_lbl.configure(text=f"Playing: {self.playlist.get(self.playing)}")
        self.time_scale.set(0)
        pygame.mixer.music.play(loops=0)
        
        
    def play(self):
        if self.playlist.curselection():
            self.playing = self.playlist.curselection()[0]
            self.song = f"{self.dir}\{self.playlist.get(ACTIVE)}.mp3"
            try:
                pygame.mixer.music.load(self.song)
            except:
                messagebox.showerror("File Error", "File is invalid please make sure that file exists!")
                return
            self.time_scale.set(0)
            pygame.mixer.music.play(loops=0)
            self.length()
            self.status_lbl.configure(text=f"Playing: {self.playlist.get(ACTIVE)}")
            self.toggle_pause_btn.configure(state="normal")
            self.next_btn.configure(state="normal")
            self.prev_btn.configure(state="normal")
            self.time_scale.configure(state="normal")
            

    def toggle_pause(self):
        if self.toggle_pause_btn["text"] == "Pause":
            try:
                pygame.mixer.music.pause()
            except:
                return
            self.toggle_pause_btn.configure(text="Resume", image=self.resume_img)
            self.play_btn.configure(state="disabled")
            self.next_btn.configure(state="disabled")
            self.prev_btn.configure(state="disabled")
            self.time_scale.configure(state="disabled")
            text = self.status_lbl["text"].lstrip("Playing: ")
            self.status_lbl.configure(text=f"Paused: {text}")
        elif self.toggle_pause_btn["text"] == "Resume":
            try:
                pygame.mixer.music.unpause()
            except:
                return
            text = self.status_lbl["text"].lstrip("Paused: ")
            self.status_lbl.configure(text=f"Playing: {text}")
            self.toggle_pause_btn.configure(text="Pause", image=self.pause_img)
            self.play_btn.configure(state="normal")
            self.next_btn.configure(state="normal")
            self.prev_btn.configure(state="normal")
            self.time_scale.configure(state="normal")
        
    
    def vol(self, x):
        try:
            value = float(x)
            pygame.mixer.music.set_volume(value)
        except:
            return



root = Tk()
JKMusicPlayer(root)
root.mainloop()

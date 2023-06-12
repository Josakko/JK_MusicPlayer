from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os
from mutagen.mp3 import MP3
from tkinter import ttk
import time
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import json


class JKMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.playlist_list = []

        window_width = 1100
        window_hight = 700

        monitor_width = self.root.winfo_screenwidth()
        monitor_hight = self.root.winfo_screenheight()

        x = (monitor_width / 2) - (window_width / 2)
        y = (monitor_hight / 2) - (window_hight / 2)

        self.root.geometry(f"{window_width}x{window_hight}+{int(x)}+{int(y)}")
        self.root.minsize(900, 600)
        self.root.iconbitmap("assets/JK.ico")
        self.root.title("JK MusicPlayer")
        self.root.config(bg="#dbdbdb")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        #self.root.resizable(False, False)
        self.font = ("Helvetica", 14)
        self.bg = "#bde6fb" #bg=self.bg
        self.fg = "#1e2529" #fg=self.fg
        self.playing = False
        pygame.mixer.init()

        self.menubar = Menu(self.root)
        
        self.filemenu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Load Folder", command=self.open_folder)        
        
        self.root.config(menu=self.menubar)


        self.list_frame = Frame(self.root)
        self.list_frame.pack(fill=BOTH, expand=True, padx=20)

        self.y_scrollbar = Scrollbar(self.list_frame)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)
        
        #self.x_scrollbar = Scrollbar(self.list_frame, orient=HORIZONTAL)
        #self.x_scrollbar.pack(side=BOTTOM, fill=X)

        self.playlist = Listbox(self.list_frame, yscrollcommand=self.y_scrollbar.set, width=140, height=15, font=self.font, ) # xscrollcommand=self.x_scrollbar.set
        self.playlist.pack(fill=BOTH, expand=True)

        self.playlist.bind("<Button-1>", self.deselect)

        self.y_scrollbar.config(command=self.playlist.yview)
        #self.x_scrollbar.config(command=self.playlist.xview)

        #self.load_btn = Button(self.root, text="Load Folder", command=self.open_folder, font=self.font, width=20)
        #self.load_btn.pack()

        self.time_frame = Frame(self.root)
        self.time_frame.pack(fill=X)
        
        self.time_lbl = Label(self.time_frame, text="0:00 / 0:00", font=self.font)
        self.time_lbl.pack(side=RIGHT, padx=10)
        
        self.time_scale = ttk.Scale(self.time_frame, from_=0, state="disabled", value=0, command=self.len_scale)
        self.time_scale.pack(side=LEFT, fill=X, expand=True, padx=15)
        self.time_scale.bind("<ButtonRelease>", self.play_len)

        self.control_frame = Frame(root, bg="#1e2529")
        self.control_frame.pack(side=BOTTOM, fill=X)
        self.control_frame.columnconfigure([0, 2, 4], weight=1)
        self.control_frame.columnconfigure([1, 3], weight=0)

        self.pause_img = PhotoImage(file="assets/pause.png")
        self.resume_img = PhotoImage(file="assets/resume.png")
        self.next_img = PhotoImage(file="assets/next.png")
        self.prev_img = PhotoImage(file="assets/previous.png")

        self.status_lbl = Label(self.control_frame, text="", font=self.font, fg=self.bg, bg=self.fg) #   7.6 width 
        self.status_lbl.grid(row=0, column=0, padx=5, sticky=W, pady=5)

        self.play_btn = Button(self.control_frame, text="Play", command=self.play, font=("Helvetica", 14, "bold"), width=15, bg=self.bg, fg=self.fg, state="disabled")
        self.play_btn.grid(row=1, column=0, padx=20, sticky=W)

        #self.loop_btn = Button(self.control_frame, text="Loop", command=self.loop)
        #self.loop_btn.grid(row=1, column=0)

        #self.control_btns_frame = Frame(self.control_frame, bg="#1e2522")
        #self.control_btns_frame.pack()
        
        self.prev_btn = Button(self.control_frame, image=self.prev_img, state="disabled", bg=self.bg, command=self.prev)
        self.prev_btn.grid(row=1, column=1, sticky=E)

        self.toggle_pause_btn = Button(self.control_frame, text="Pause", image=self.pause_img, command=self.toggle_pause, font=self.font, state="disabled", bg=self.bg, fg=self.fg)
        self.toggle_pause_btn.grid(row=1, column=2, pady=30, ipadx=10)
        self.root.bind("<space>", self.space)

        self.next_btn = Button(self.control_frame, image=self.next_img, state="disabled", bg=self.bg, fg=self.fg, command=self.next)
        self.next_btn.grid(row=1, column=3, sticky=W)

        self.vol_scale = ttk.Scale(self.control_frame, command=self.vol, from_=0, to=1, value=1, length=200)
        self.vol_scale.grid(row=1, column=4, padx=15, sticky=E)

        
        #self.time_stamp = 0
        self.scale_time_stamp = 0
        self.loop = False
        #self.path = ""
    
        self.settings()
        
        
    def space(self, event):
        self.toggle_pause_btn.invoke()


    def deselect(self, event):
        self.playlist.selection_clear(0, END)

     
    def settings(self):
        settings = self.load_settings()
        folder = settings["folder"]
        self.vol_scale.set(settings["volume"])
        
        if folder:
            if os.path.exists(folder):
                try:
                    for file in os.listdir(folder):
                        if file.endswith(".mp3") or file.endswith(".wav"):
                            song = os.path.splitext(file)
                            self.playlist_list.append((song[0], song[1], f"{folder}/{file}"))
                            self.playlist.insert(END, song[0])
                except:
                    return
                self.play_btn.configure(state="normal")
                self.path = folder



    def open_folder(self):
        initialdir = os.path.join(os.path.expanduser("~"), "Music")
        dir = filedialog.askdirectory(initialdir=initialdir)
        if not dir or not os.path.exists(dir):
            dir = self.path
            return
        
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        self.time_scale.configure(value=0)
        self.time_lbl.configure(text="00:00 / 00:00")
        self.playlist.delete(0, END)
        self.status_lbl.configure(text="")
        self.playlist_list.clear()

        for file in os.listdir(dir):
            if file.endswith(".mp3") or file.endswith(".wav"):
                song = os.path.splitext(file)[0]
                self.playlist_list.append((song[0], song[1], f"{dir}/{file}"))
                self.playlist.insert(END, song)
                
        self.play_btn.configure(state="normal")
        self.path = dir
        
        
    def length(self):
        try:
            #print(self.time_stamp)
            self.time_stamp = pygame.mixer.music.get_pos() / 1000 + self.scale_time_stamp
            #print(self.time_stamp)
            self.time_scale.configure(value=self.time_stamp)
            time_ = time.strftime("%M:%S", time.gmtime(self.time_stamp))
            try:
                song = MP3(self.song)
                duration_ = song.info.length
                self.time_scale.configure(from_=0, to=duration_)
                self.duration = time.strftime("%M:%S", time.gmtime(duration_))
                
                self.time_lbl.configure(text=f"{time_} / {self.duration}")
            #except Exception as e:
            except:
                #print(e)
                self.time_lbl.configure(text=f"{time_} / 0:00")
                pass

            #print(int(duration_), int(self.time_stamp))
            
            if int(duration_) == int(self.time_stamp) or int(duration_) == int(self.time_stamp + 1): #if int(duration_) == int(self.time_stamp):
                #print("end of song")
                self.time_lbl.configure(text=f"{self.duration} / {self.duration}")
                if self.loop:
                    pass
                    #try:
                    #    #pygame.mixer.music.unload()
                    #    #pygame.mixer.music.load(self.song)
                    #    pygame.mixer.music.play(loops=0)
                    #    #self.time_scale.set(0)
                    #except:
                    #    return
                    
                    #self.song = f"{self.path}\{self.playlist.get(self.playing)}.mp3"
                    #try:
                    #    pygame.mixer.music.load(self.song)
                    #except:
                    #    pass
                    #pygame.mixer.music.play(loops=0)
                else:
                    #self.time_scale.set(duration_)#  self.time_scale.configure(value=duration_)
                    self.time_lbl.after(800)
                    self.next()
                    
        #except Exception as e:
        except:
            #print(e)
            pass
        #print(f"{time_}   {self.time_scale.get()}")
        self.time_lbl.after(1000, self.length)


    def play_len(self, event):
        try:
            pygame.mixer.music.load(self.song)
            pygame.mixer.music.play(loops=0, start=int(self.time_scale.get()))
        except:
            return
    

    def load_settings(self):
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
            return data
        except:
            return {
                "folder": "",
                "volume": 1
            }
            

    def save_settings(self, data):
        with open("config.json", "w") as f:
            json.dump(data, f, indent=4)

    
    def len_scale(self, value):
        pygame.mixer.music.stop()
        try:
            #pygame.mixer.music.load(self.song)
            #pygame.mixer.music.play(loops=0, start=int(self.time_scale.get()))
            #print(int(pygame.mixer.music.get_pos() / 1000))
            self.time_lbl.configure(text=f"{time.strftime('%M:%S', time.gmtime(self.scale_time_stamp))} / {self.duration}") #self.time_lbl.configure(text=f"{time.strftime('%M:%S', time.gmtime(pygame.mixer.music.get_pos() / 1000 + self.scale_time_stamp))} / {self.duration}")
        except:
            #print(e)
            return
        self.scale_time_stamp = int(self.time_scale.get())
        #print(self.scale_time_stamp)


    def next(self):
        self.playing = self.playing + 1
        if self.playlist.get(self.playing) == "": 
            self.playing = self.playing - 1
            return
        self.song = self.playlist_list[self.playing][2] #f"{self.path}\{self.playlist.get(self.playing)}.mp3"
        try:
            pygame.mixer.music.load(self.song)
        except:
            self.playing = self.playing - 1
            return
        self.deselect("x")
        self.playlist.selection_set(self.playing)
        self.status_lbl.configure(text=f"Playing: {self.shorten(self.playlist.get(self.playing))}")
        self.time_scale.set(0)
        pygame.mixer.music.play(loops=0)
  
  
    def prev(self):
        self.playing = self.playing - 1
        if self.playlist.get(self.playing) == "": 
            self.playing = self.playing + 1
            return
        self.song = self.playlist_list[self.playing][2] #f"{self.path}\{self.playlist.get(self.playing)}.mp3"
        try:
            pygame.mixer.music.load(self.song)
        except:
            self.playing = self.playing + 1
            return
        self.deselect("x")
        self.playlist.selection_set(self.playing)
        self.status_lbl.configure(text=f"Playing: {self.shorten(self.playlist.get(self.playing))}")
        self.time_scale.set(0)
        pygame.mixer.music.play(loops=0)
        
        
    def play(self):
        if 1:
            self.playing = self.playlist.curselection()[0]
            self.song = self.playlist_list[self.playing][2] #f"{self.path}\{self.playlist.get(ACTIVE)}.mp3"

            if os.path.exists(self.song):
                try:
                    pygame.mixer.music.load(self.song)
                except:
                    messagebox.showerror("Error", "File seams to be corrupted!")
                    return
            else: messagebox.showerror("File Error", "File is invalid please make sure that file exists!")

            self.time_scale.set(0)
            pygame.mixer.music.play(loops=0)
            self.length()
            self.status_lbl.configure(text=f"Playing: {self.shorten(self.playlist.get(ACTIVE))}")
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
        
    
    def vol(self, value):
        try:
            pygame.mixer.music.set_volume(float(value))
        except:
            return
        
    def shorten(self, text):
        if len(text) > 16: #MAX: 24
            shorten_text = f"{text[:13]}..."
            return shorten_text
        else:
            return text
        
    def quit(self):
        try:
            self.save_settings({"folder": self.path, "volume": self.vol_scale.get()})
        except:
            self.save_settings({"folder": "", "volume": self.vol_scale.get()})
        finally:
            self.root.destroy()
        
            
root = Tk()
JKMusicPlayer(root)
root.mainloop()


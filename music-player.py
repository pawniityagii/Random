import os
import pygame
from tkinter import *
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
from PIL import Image, ImageTk  # PIL for background image support

# Initialize Tkinter
root = Tk()
root.title("Professional Music Player")
root.geometry("600x450")  # Adjusted size for better UI
root.configure(bg="#1e1e1e")  # Dark mode background
root.resizable(True, True)

listofsongs = []
realnames = []

v = StringVar()
index = 0

# Load Background Image
bg_image = Image.open("mpi.png")  # Replace with your image path
bg_image = bg_image.resize((600, 450))  # Resize to window size
bg_photo = ImageTk.PhotoImage(bg_image)

# Set Background
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Full window background

def directorychooser():
    directory = askdirectory()
    os.chdir(directory)
    
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            song_title = audio.get('TIT2', [os.path.splitext(files)[0]])[0]
            realnames.append(song_title)
            listofsongs.append(files)
    
    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    pygame.mixer.music.play()

directorychooser()

def updatelabel():
    global index
    v.set(realnames[index])

def nextsong():
    global index
    index = (index + 1) % len(listofsongs)  # Loop back if at end
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def prevsong():
    global index
    index = (index - 1) % len(listofsongs)  # Loop back if at start
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def unpausesong():
    pygame.mixer.music.unpause()
    v.set("Playing: " + realnames[index])

def pausesong():
    pygame.mixer.music.pause()
    v.set("Paused: " + realnames[index])

def stopsong():
    pygame.mixer.music.stop()
    v.set("")

# Song Label (Glassmorphism Effect)
songlabel = Label(root, textvariable=v, font=("Segoe UI", 12, "bold"),
                  fg='white', bg='#2e2e2e', padx=10, pady=5, relief=FLAT, 
                  highlightthickness=1, highlightbackground="#555")
songlabel.pack(pady=10)

# Transparent Song Listbox using Canvas
canvas = Canvas(root, bg=root["bg"], highlightthickness=0)
canvas.pack(pady=10, padx=20, fill=X)

listbox = Listbox(canvas, bg=root["bg"], fg='white', font=("Segoe UI", 11),
                  highlightthickness=0, borderwidth=0, selectbackground="#444", selectforeground="white")
listbox.pack()

# Populate Songs in Listbox
realnames.reverse()
for items in realnames:
    listbox.insert(0, items)
realnames.reverse()

# Button Styling
button_style = {
    "font": ("Segoe UI", 11, "bold"),
    "fg": "white",
    "bg": "#444",
    "padx": 15,
    "pady": 8,
    "borderwidth": 0,
    "relief": FLAT,
    "width": 12,
    "highlightthickness": 1,
    "highlightbackground": "#555"
}

# Button Frame for Better Layout
button_frame = Frame(root, bg="#1e1e1e")
button_frame.pack(pady=10)

prevbutton = Button(button_frame, text="⏮ Previous", command=prevsong, **button_style)
prevbutton.grid(row=0, column=0, padx=5)

pausebutton = Button(button_frame, text="⏸ Pause", command=pausesong, **button_style)
pausebutton.grid(row=0, column=1, padx=5)

unpausebutton = Button(button_frame, text="▶ Play", command=unpausesong, **button_style)
unpausebutton.grid(row=0, column=2, padx=5)

nextbutton = Button(button_frame, text="⏭ Next", command=nextsong, **button_style)
nextbutton.grid(row=0, column=3, padx=5)

stopbutton = Button(root, text="⏹ Stop Music", command=stopsong, **button_style)
stopbutton.pack(pady=5)

root.mainloop()

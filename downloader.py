# Copyright (c) 2023, tsoumagas-benjamin
# All rights reserved.

# This source code is licensed under the GNU GPLv3 license found in the
# LICENSE file in the root directory of this source tree. 

import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo, showerror
from pytube import YouTube
import requests
import os

# Function to clear placeholder text from entry
def on_entry_click(event):
    if entry.get() == "https://www.youtube.com...":
        entry.delete(0, tk.END)

# Function to choose a directory and allow user to download
def specify_dir():
    folder_selected = filedialog.askdirectory()
    if folder_selected is not None:
        folder_button.configure(text=folder_selected)
        button.pack(pady=(0,50))

def fetch():
    # Get the URL from the entry boxes
    mp3_link = entry.get()
    fn = filename.get()
    folder = folder_button.cget("text")

    # Return errors in case URL, filename, or folder aren't correct
    if not mp3_link or mp3_link == "https://www.youtube.com...":
        return showerror(title="Error", message="Please enter the YouTube URL.")
    if not fn:
        return showerror(title="Error", message="Please enter a filename and try again.")
    if folder == "Choose Folder":
        return showerror(title="Error", message="Please choose a folder and try again.")
    
    # Validate URL
    r = requests.get(mp3_link)
    if "Video unavailable" in r.text or "https://www.youtube.com" not in mp3_link:
        return showerror(title="Error", message="Invalid link, please try again.")
    
    else:
        # Get rid of existing .mp3 and .mp4 files in this directory
        pwdir = os.getcwd()
        for item in os.listdir(pwdir):
            if item.endswith(".mp3") or item.endswith(".mp4"):
                os.remove(os.path.join(pwdir, item))
        try:
            # Extract and download the audio file               
            audio = YouTube(mp3_link)     
            output = audio.streams.get_audio_only().download(
                output_path=folder, 
                filename=fn
            )

            # Split the file into base and extension
            base, ext = os.path.splitext(output)

		    # Convert to mp3 and rename the file
            new_file = f"{base}.mp3"
            os.rename(output, new_file)

            # Let user know when download is successful
            showinfo(title="Download Complete", message=f"{fn}.mp3 has been downloaded to {folder}.")      
           
            # Clear entry boxes
            entry.delete(0, tk.END)
            filename.delete(0, tk.END)

        # Return error in case of any exceptions during download
        except:
            return showerror(title="Download Error", message="An error occurred while trying to " \
                    "download the MP3\nThe following could " \
                    "be the causes:\n->Invalid link\n->No internet connection\n"\
                     "Make sure you have stable internet connection and the MP3 link is valid.")

# Setup initial Tkinter window
window = tk.Tk()
window.geometry("640x480")
window.title("YouTube to MP3 Converter")
window.configure(background="black")

# Label and entry field for user to paste URL and filename
label = tk.Label(
    text="Paste your YouTube URL here:", 
    fg="grey",
    bg="black"
)

entry = tk.Entry(
    bg="grey",
    width=100,
    justify="center",
)

filename_label = tk.Label(
    text="Choose a file name:", 
    fg="grey",
    bg="black"
)

filename = tk.Entry(
    bg="grey",
    width=32,
    justify="center",
)

# Button to select target directory and download
folder_button = tk.Button(
    bg="grey",
    borderwidth=10,
    width=25,
    text="Choose Folder",
    command=specify_dir,
)

button = tk.Button(
    bg="green",
    borderwidth=10,
    width=25,
    text="Download",
    command=fetch,
)

# Layout of Tkinter widgets
label.pack(pady=(50,0))
entry.pack(pady=(0,50))
filename_label.pack()
filename.pack()
folder_button.pack(pady=(50,50))

# Handle placeholder text for entry
entry.insert(0, "https://www.youtube.com...")
entry.bind('<FocusIn>', on_entry_click)

window.mainloop()
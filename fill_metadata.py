import os, eyed3, csv, tkinter as tk
from shutil import copyfile
from tkinter import messagebox

def get_cover_path():
    cover_path = "./Input/Artwork"
    try:
        return cover_path + "/" + os.listdir(cover_path)[0]
    except:
        tk.messagebox.showerror(title="Error", message="No artwork added!")

def import_metadata():
    with open("metadata.csv") as file:
        reader = csv.DictReader(file)

        meta = {}
        for row in reader:
            key = row.pop('title')
            meta[key] = row
    return meta

def check_filenames(in_path, meta):
    # Check all track files are named 
    tofix = []
    for track in os.listdir(in_path):
        if track.split(" [")[0] not in meta.keys():
            tofix.append(track)

    if tofix:        
        tk.messagebox.showerror(title="Error", message="Incorrect filenames")
        lbox.insert(tk.END, "The following track filenames need to be fixed:")
        lbox.insert(tk.END, *tofix)
        lbox.pack()
        return False
    else:
        return True

def set_meta():
    in_path = "./Input/Tracks" 
    out_path = "./Output" 

    cover_path = get_cover_path()

    meta = import_metadata()

    if check_filenames(in_path, meta) == True:
        # Finally set tags
        for track in os.listdir(in_path):
            lbox.insert(tk.END, track)
            lbox.pack()

            # Grab tag values from csv
            title = track.split(" [")[0]
            tmp = meta[title]

            # Load MP3
            mp3 = eyed3.load(in_path + '/' + track) 
            
            # Initialize tags if not there
            if (mp3.tag == None):
                mp3.initTag() 

            # Set the tags
            mp3.tag.title = title
            mp3.tag.artist = tmp["artist"]  
            mp3.tag.album_artist = tmp["album_artist"]
            mp3.tag.non_std_genre = tmp["genre"]
            mp3.tag.composer = tmp["composer"]
            mp3.tag.album = tmp["album"]
            mp3.tag.images.set(3, open(cover_path,'rb').read(), 'image/png')
            mp3.tag.year = tmp["year"]

            if tmp["disc_num"]:
                mp3.tag.disc_num = tmp["disc_num"]
            if tmp["track_num"]:
                mp3.tag.track_num = tmp["track_num"]
    
            # Save tags
            mp3.tag.save()    

            # Save a renamed copy to the Output folder
            copyfile(in_path + '/' + track, out_path + '/' + title + " [" + tmp["artist"] + "].mp3")
        
        tk.messagebox.showinfo(title="Done!", message="All files have been processed")

# GUI

window = tk.Tk()
window.geometry("600x450")
window.title("Fill MP3 tags")
window.resizable(False, False)

container = tk.Frame(window)
container.pack(side=tk.TOP)

start_button = tk.Button(container,text="Start", command=set_meta)
start_button.pack(pady=20)

scrollbar = tk.Scrollbar(window)
scrollbar.pack(side = tk.RIGHT, fill = "y")

lbox = tk.Listbox(window, yscrollcommand = scrollbar.set)
lbox.config(width=400, height=300)

scrollbar.config(command = lbox.yview)

if __name__ == "__main__":
    window.mainloop()
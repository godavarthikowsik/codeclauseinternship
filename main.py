import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pygame
import time

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("700x800")

        pygame.init()
        pygame.mixer.init()

        self.playlist = []
        self.current_track = 0
        self.paused = False
        self.paused_position = 0

        self.load_button = ttk.Button(root, text="Load Music", command=self.load_music)
        self.load_button.pack(pady=10)

        self.play_button = ttk.Button(root, text="Play", command=self.play_music)
        self.play_button.pack(pady=5)

        self.pause_button = ttk.Button(root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=5)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=5)

        self.next_button = ttk.Button(root, text="Next", command=self.next_track)
        self.next_button.pack(pady=5)

        self.previous_button = ttk.Button(root, text="Previous", command=self.previous_track)
        self.previous_button.pack(pady=5)

        self.volume_scale = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200, command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack(pady=10)

        self.progress_scale = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=300, command=self.set_progress)
        self.progress_scale.pack(pady=10)

        self.playlist_box = tk.Listbox(root, selectbackground="lightblue", selectmode=tk.SINGLE)
        self.playlist_box.pack(padx=10, pady=5)

        self.current_song_label = tk.Label(root, text="Currently Playing: None")
        self.current_song_label.pack(pady=5)

        self.save_playlist_button = ttk.Button(root, text="Save Playlist", command=self.save_playlist)
        self.save_playlist_button.pack(pady=5)

        self.load_playlist_button = ttk.Button(root, text="Load Playlist", command=self.load_playlist)
        self.load_playlist_button.pack(pady=5)

        self.update_progress()

    def load_music(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            self.playlist.append(file_path)
            track_name = file_path.split("/")[-1]
            self.playlist_box.insert(tk.END, track_name)
            print(f"Loaded: {track_name}")

    def play_music(self):
        if self.playlist:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.load(self.playlist[self.current_track])
                pygame.mixer.music.play(start=self.paused_position)
                self.update_current_song_label()

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True
        self.paused_position = pygame.mixer.music.get_pos() // 1000

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)

    def set_progress(self, value):
        if self.playlist:
            progress = float(value) / 100
            track_length = pygame.mixer.Sound(self.playlist[self.current_track]).get_length()
            pygame.mixer.music.set_pos(progress * track_length)

    def update_progress(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            current_pos = pygame.mixer.music.get_pos() // 1000
            self.progress_scale.set(current_pos)
        self.root.after(1000, self.update_progress)

    def save_playlist(self):
        playlist_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Playlist Files", "*.txt")])
        if playlist_file:
            with open(playlist_file, "w") as file:
                for track in self.playlist:
                    file.write(track + "\n")

    def load_playlist(self):
        playlist_file = filedialog.askopenfilename(filetypes=[("Playlist Files", "*.txt")])
        if playlist_file:
            with open(playlist_file, "r") as file:
                self.playlist = [line.strip() for line in file]
            self.playlist_box.delete(0, tk.END)
            for track in self.playlist:
                track_name = track.split("/")[-1]
                self.playlist_box.insert(tk.END, track_name)
            print("Playlist loaded.")

    def next_track(self):
        if self.current_track < len(self.playlist) - 1:
            self.current_track += 1
            self.play_music()

    def previous_track(self):
        if self.current_track > 0:
            self.current_track -= 1
            self.play_music()

    def update_current_song_label(self):
        if self.playlist:
            track_name = self.playlist[self.current_track].split("/")[-1]
            self.current_song_label.config(text=f"Currently Playing: {track_name}")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("TButton", padding=10, font=("Helvetica", 10))
    music_player = MusicPlayer(root)
    root.mainloop()

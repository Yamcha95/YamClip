import os
import tkinter as tk
from tkinter import filedialog, messagebox
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import subprocess

# Fonction pour traiter la vidéo
def process_video(video_path):
    if not os.path.exists(video_path):
        messagebox.showerror("Erreur", f"Le fichier vidéo '{video_path}' est introuvable.")
        return

    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())

    print("Analyse de la vidéo...")
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()
    video_manager.release()

    if not scene_list:
        messagebox.showinfo("Résultat", "Aucune scène détectée.")
        return

    print(f"{len(scene_list)} scènes détectées.")

    output_dir = "clips"
    os.makedirs(output_dir, exist_ok=True)

    # Découpage avec ffmpeg
    for i, scene in enumerate(scene_list):
        start_time, end_time = scene
        output_file = os.path.join(output_dir, f"clip_{i+1}.mp4")
        command = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-ss", str(start_time.get_timecode()),
            "-to", str(end_time.get_timecode()),
            "-c:v", "libx264", "-c:a", "aac",
            output_file
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    messagebox.showinfo("Succès", f"{len(scene_list)} clips créés dans le dossier 'clips'.")

# Ouvrir le sélecteur de fichier
def open_file_dialog():
    video_path = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4;*.avi;*.mov")])
    if video_path:
        print(f"Vidéo sélectionnée : {video_path}")
        process_video(video_path)

# Interface graphique
root = tk.Tk()
root.title("Découpeur Vidéo Automatique")
root.geometry("400x200")

label = tk.Label(root, text="Découpeur de scènes vidéo", font=("Arial", 14))
label.pack(pady=20)

btn_open = tk.Button(root, text="Importer une vidéo", command=open_file_dialog, width=20, height=2)
btn_open.pack(pady=20)

root.mainloop()

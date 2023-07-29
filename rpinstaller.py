import os
import shutil
import tkinter as tk
from tkinter import filedialog
import ctypes
import git

def update_from_github(repo_url, repo_path):
    if os.path.exists(repo_path):
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.fetch()
        origin.pull()
    else:
        git.Repo.clone_from(repo_url, repo_path)

def set_app_window_style():
    if os.name == "nt":
        app_id = "MyMinecraftResourcepackInstaller"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

def select_resourcepack():
    file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
    resourcepack_entry.delete(0, tk.END)
    resourcepack_entry.insert(0, file_path)

def list_resourcepacks():
    resourcepacks_list.delete(0, tk.END)
    resourcepacks_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "resourcepacks")
    if os.path.exists(resourcepacks_folder):
        resourcepacks = os.listdir(resourcepacks_folder)
        for pack in resourcepacks:
            resourcepacks_list.insert(tk.END, pack)

def install_resourcepack():
    selected_pack = resourcepacks_list.get(resourcepacks_list.curselection())
    source_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "resourcepacks", selected_pack)
    destination_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "resourcepacks")
    
    if os.path.exists(source_path) and os.path.exists(destination_path):
        try:
            shutil.copy(source_path, destination_path)
            status_label.config(text="Resourcepack installed successfully!", fg="#4CAF50")
        except Exception as e:
            status_label.config(text="Error while installing the resourcepack.", fg="#F44336")
    else:
        status_label.config(text="Invalid source or destination path.", fg="#F44336")

repo_url = "https://github.com/RivioxGaming/RPInstaller.git"
repo_path = "repo\\github"

update_from_github(repo_url, repo_path)

root = tk.Tk()
root.title("Minecraft Resourcepack Installer")
root.geometry("500x450")

icon_path = "icon.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

root.configure(bg="#1E1E1E")
root.option_add("*foreground", "white")
root.option_add("*background", "#1E1E1E")

title_label = tk.Label(root, text="Resourcepack Installer", font=("Helvetica", 24), bg="#1E1E1E", fg="white")
title_label.pack(pady=10)

resourcepacks_frame = tk.Frame(root, bg="#1E1E1E")
resourcepacks_frame.pack(pady=10)
resourcepacks_label = tk.Label(resourcepacks_frame, text="Installed Resourcepacks:", bg="#1E1E1E", fg="white")
resourcepacks_label.pack(side=tk.LEFT, padx=10)
resourcepacks_list = tk.Listbox(resourcepacks_frame, width=40, height=5, bg="#2E2E2E", fg="white", selectbackground="#3E3E3E")
resourcepacks_list.pack(side=tk.LEFT, padx=10)
resourcepacks_list.bind("<ButtonRelease-1>", lambda event: resourcepack_entry.delete(0, tk.END) if not resourcepacks_list.curselection() else None)
refresh_button = tk.Button(resourcepacks_frame, text="Refresh", command=list_resourcepacks, bg="#3E3E3E", fg="white")
refresh_button.pack(side=tk.LEFT, padx=10)

resourcepack_entry_frame = tk.Frame(root, bg="#1E1E1E")
resourcepack_entry_frame.pack(pady=10)
resourcepack_entry_label = tk.Label(resourcepack_entry_frame, text="Select Resourcepack (ZIP):", bg="#1E1E1E", fg="white")
resourcepack_entry_label.pack(side=tk.LEFT, padx=10)
resourcepack_entry = tk.Entry(resourcepack_entry_frame, width=40, bg="#2E2E2E", fg="white")
resourcepack_entry.pack(side=tk.LEFT)
resourcepack_button = tk.Button(resourcepack_entry_frame, text="Browse", command=select_resourcepack, bg="#3E3E3E", fg="white")
resourcepack_button.pack(side=tk.LEFT, padx=10)

install_button = tk.Button(root, text="Install Resourcepack", command=install_resourcepack, bg="#4CAF50", fg="white")
install_button.pack(pady=15)

status_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#1E1E1E", fg="white")
status_label.pack()

made_by_label = tk.Label(root, text="Made by .riviox", font=("Helvetica", 10), bg="#1E1E1E", fg="white")
made_by_label.pack(side=tk.BOTTOM)

list_resourcepacks()

root.mainloop()

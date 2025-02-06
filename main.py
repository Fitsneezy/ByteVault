import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import zipfile
import json
import requests
import subprocess

# Define the directory where packages will be installed
INSTALL_DIR = 'installed_packages'

def download_and_install(package_url):
    package_name = package_url.split("/")[-1].replace(".zip", "")
    zip_path = f"{package_name}.zip"

    try:
        # Download the package
        response = requests.get(package_url, stream=True)
        response.raise_for_status()

        # Save the ZIP file
        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Install the package
        install(package_name, zip_path)
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to download package: {e}")

def install(package_name, zip_path=None):
    if not zip_path:
        zip_path = f"{package_name}.zip"

    if not os.path.exists(zip_path):
        messagebox.showerror("Error", f"Package file '{zip_path}' not found.")
        return

    if not os.path.exists(INSTALL_DIR):
        os.makedirs(INSTALL_DIR)

    extract_dir = os.path.join(INSTALL_DIR, package_name)
    if os.path.exists(extract_dir):
        messagebox.showinfo("Info", f"Package '{package_name}' is already installed.")
        return

    # Extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # Check for 'run.py' and execute it
    run_script_path = os.path.join(extract_dir, "run.py")
    if os.path.exists(run_script_path):
        subprocess.run(["python", run_script_path], check=True)  # Run the script
        
    messagebox.showinfo("Info", f"Package '{package_name}' installed and executed.")

    os.remove(zip_path)  # Clean up the downloaded ZIP
    update_package_list()

def update_package_list():
    package_listbox.delete(0, tk.END)
    if not os.path.exists(INSTALL_DIR):
        return

    packages = [item for item in os.listdir(INSTALL_DIR) if os.path.isdir(os.path.join(INSTALL_DIR, item))]
    
    if not packages:
        package_listbox.insert(tk.END, "No packages installed.")
    else:
        for package in packages:
            package_listbox.insert(tk.END, package)

def remove():
    selected_item = package_listbox.get(tk.ACTIVE)
    if not selected_item or selected_item == "No packages installed.":
        return

    package_dir = os.path.join(INSTALL_DIR, selected_item)
    if os.path.exists(package_dir):
        for root, dirs, files in os.walk(package_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(package_dir)
        messagebox.showinfo("Success", f"Package '{selected_item}' removed successfully.")
        update_package_list()

def update_package():
    selected_item = package_listbox.get(tk.ACTIVE)
    if not selected_item or selected_item == "No packages installed.":
        return
    
    messagebox.showinfo("Update", f"Package '{selected_item}' updated successfully. (Placeholder)")

# GUI Setup
root = tk.Tk()
root.title("ByteVault Package Manager")
root.geometry("500x350")

# Package Listbox
package_listbox = tk.Listbox(root, height=10, width=60)
package_listbox.pack(pady=5)
update_package_list()

# Buttons
tk.Button(root, text="Install Package", command=lambda: install(simpledialog.askstring("Install", "Enter package name:"))).pack(pady=5)
tk.Button(root, text="Install from URL", command=lambda: download_and_install(simpledialog.askstring("Install from URL", "Enter package URL:"))).pack(pady=5)
tk.Button(root, text="Remove Package", command=remove).pack(pady=5)
tk.Button(root, text="Update Package", command=update_package).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

root.mainloop()

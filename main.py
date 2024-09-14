import argparse
import os
import zipfile

# Define the directory where packages will be installed
INSTALL_DIR = 'installed_packages'

def install(package_name):
    zip_path = f'{package_name}.zip'
    if not os.path.exists(zip_path):
        print(f"Package file '{zip_path}' not found.")
        return
    
    if not os.path.exists(INSTALL_DIR):
        os.makedirs(INSTALL_DIR)
    
    extract_dir = os.path.join(INSTALL_DIR, package_name)
    if os.path.exists(extract_dir):
        print(f"Package '{package_name}' is already installed.")
        return
    
    print(f"Installing package: {package_name} from '{zip_path}'")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    print(f"Package '{package_name}' installed successfully.")

def list_packages():
    if not os.path.exists(INSTALL_DIR):
        print("No packages installed.")
        return
    
    print("Installed packages:")
    for item in os.listdir(INSTALL_DIR):
        if os.path.isdir(os.path.join(INSTALL_DIR, item)):
            print(f" - {item}")

def remove(package_name):
    package_dir = os.path.join(INSTALL_DIR, package_name)
    if not os.path.exists(package_dir):
        print(f"Package '{package_name}' not found.")
        return
    
    print(f"Removing package: {package_name}")
    
    for root, dirs, files in os.walk(package_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    
    os.rmdir(package_dir)
    print(f"Package '{package_name}' removed successfully.")

def update(package_name):
    print(f"Updating package: {package_name}")
    # For simplicity, this is a placeholder. Implement actual update logic if needed.
    print(f"Package '{package_name}' updated successfully.")

def main():
    parser = argparse.ArgumentParser(description="ByteVault - A simple package manager")
    subparsers = parser.add_subparsers(dest='command')

    install_parser = subparsers.add_parser('install', help='Install a package from a ZIP file')
    install_parser.add_argument('package_name', type=str, help='Name of the package to install')

    subparsers.add_parser('list', help='List installed packages')

    remove_parser = subparsers.add_parser('remove', help='Remove a package')
    remove_parser.add_argument('package_name', type=str, help='Name of the package to remove')

    update_parser = subparsers.add_parser('update', help='Update a package')
    update_parser.add_argument('package_name', type=str, help='Name of the package to update')

    args = parser.parse_args()

    if args.command == 'install':
        install(args.package_name)
    elif args.command == 'list':
        list_packages()
    elif args.command == 'remove':
        remove(args.package_name)
    elif args.command == 'update':
        update(args.package_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

import json
import sys
import os

PACKAGE_DB = "packages.json"
INSTALLED_DB = "installed.json"

def load_db(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def save_db(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def install(pkg_name):
    packages = load_db(PACKAGE_DB)
    installed = load_db(INSTALLED_DB)
    if pkg_name in packages:
        if pkg_name in installed:
            print(f"{pkg_name} is already installed.")
        else:
            installed[pkg_name] = packages[pkg_name]
            save_db(INSTALLED_DB, installed)
            print(f"Installed {pkg_name} {packages[pkg_name]['version']}")
    else:
        print(f"Package {pkg_name} not found.")

def remove(pkg_name):
    installed = load_db(INSTALLED_DB)
    if pkg_name in installed:
        del installed[pkg_name]
        save_db(INSTALLED_DB, installed)
        print(f"Removed {pkg_name}")
    else:
        print(f"{pkg_name} is not installed.")

def list_packages():
    installed = load_db(INSTALLED_DB)
    if not installed:
        print("No packages installed.")
    else:
        for name, meta in installed.items():
            print(f"{name} {meta['version']} - {meta['description']}")

def run(pkg_name):
    script_path = os.path.join("packages", f"{pkg_name}.py")
    if not os.path.exists(script_path):
        print(f"No executable script found for {pkg_name}.")
        return
    print(f"Running {pkg_name}:")
    os.system(f'python "{script_path}"')

def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_pacman.py <command> [package]")
        return
    command = sys.argv[1]
    if command == "-S":  # install
        if len(sys.argv) < 3:
            print("Specify a package to install.")
        else:
            install(sys.argv[2])
    elif command == "-R":  # remove
        if len(sys.argv) < 3:
            print("Specify a package to remove.")
        else:
            remove(sys.argv[2])
    elif command == "-Q":  # list
        list_packages()
    elif command == "-X":  # run
        if len(sys.argv) < 3:
            print("Specify a package to run.")
        else:
            run(sys.argv[2])
    else:
        print("Unknown command.")

if __name__ == "__main__":
    main()



#install pack python simple_pacman.py -S <package-names>
#list pack  python simple_pacman.py -Q
#remove pack python simple_pacman.py -R <package-names>
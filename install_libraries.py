import sys
import subprocess

# Библиотеки, необходимые для работы проекта
LIST_LIBRARIES = ['uvicorn', 'FastApi', 'requests']

def install_packages(package_list):
    for package in package_list:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_packages(LIST_LIBRARIES)

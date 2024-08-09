import os
import subprocess

# Please change venv_path to suit your development environment.
venv_path = r'C:\Development\project_files\minecraft_soundreplacer\.venv'

python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')

# run setup.py --------------------------------------------
subprocess.call([python_executable, 'setup.py', 'build'])

# make blank directory ------------------------------------
os.makedirs('build\\minecraft_soundreplacer\\image_user')
os.makedirs('build\\minecraft_soundreplacer\\temp')

print('complate building !')

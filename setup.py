from cx_Freeze import setup, Executable

runfile = 'minecraft_soundreplacer.py'
icon = 'image\\icon_frame.ico'

setup(
    name='minecraft_soundreplacer',
    version='0.1',
    description='',
    executables=[Executable(runfile, icon=icon, base='Win32GUI')],
    options={
        'build_exe': {
            'build_exe': 'build\\minecraft_soundreplacer',
            'packages': ['source'],
            'include_files': ['url.csv',
                              'Vanilla_Resource_Pack_1.21.0\\',
                              'Vanilla_Resource_Pack_1.21_JE\\',
                              'image\\',
                              'ffmpeg-7.0.1-essentials_build\\']
        }
    }
)

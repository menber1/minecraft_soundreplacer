from cx_Freeze import setup, Executable

runfile = 'soundreplacer.py'
icon = 'image\\icon_frame.ico'

setup(
    name='soundreplacer',
    version='0.1',
    description='',
    executables=[Executable(runfile, icon=icon, base='Win32GUI')],
    options={
        'build_exe': {
            'build_exe': 'build\\soundreplacer',
            'packages': ['source'],
            'include_files': ['url.csv',
                              'Vanilla_Resource_Pack_BE\\',
                              'Vanilla_Resource_Pack_JE\\',
                              'image\\',
                              'ffmpeg-7.0.1-essentials_build\\']
        }
    }
)

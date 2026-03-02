import yt_dlp as yd
from pathlib import Path
import os
import sys
import platform

if platform.system() == 'Windows':#Make sure to change the directory according to your file and folder location before using
    dir_out = r'E:\Python_projects\downloaded_stuff\songs\%(title)s.%(ext)s'#for Windows Powershell
else:
    dir_out = r'/mnt/e/Python_projects/downloaded_stuff/songs/%(title)s.%(ext)s'#for WSL

def video_downloader():
    url = input('Enter the url: ')
    configs = {
        'format': 'bestvideo[height<=1080]',
        'outtmpl': dir_out,
        'nonplaylist': True
    }
    with yd.YoutubeDL(configs) as somth:
        somth.download([url])


def audio_dl():
    url = input('Enter the url: ')
    
    configs = {
        'format': 'bestaudio/best',
        'outtmpl': dir_out,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }
        ]
    }
    
    with yd.YoutubeDL(configs) as aud_dl:# same as aud_dl = yd.YoutubeDL(configs)

        info = aud_dl.extract_info(url, download=True)
        file_name = aud_dl.prepare_filename(info)
        name = os.path.splitext(file_name)[0]
        file = Path(name+'.mp3')

    while True:
        title_changer = input('Do you want to change the title? y/n: ')
        if title_changer == 'y':
            user = input('Enter the new name: ')
            file.rename(file.with_name(f'{user}.mp3'))
            break
        elif title_changer == 'n': sys.exit('Successfully stopped the program!')
        else: 
            print('Uknown command!')
            continue

commands = {
    'video': video_downloader,
    'audio': audio_dl
}

command = commands.get(sys.argv[1])

def main():
    if len(sys.argv) < 2:
        sys.exit('Not enough arguments on the terminal')
    if command: command()
    else: sys.exit('Error')

if __name__ == '__main__':
    main()
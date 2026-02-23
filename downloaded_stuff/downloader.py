import yt_dlp as yd
import sys

def video_downloader():
    url = input('Enter the url: ')
    configs = {
        'format': 'bestvideo[height<=1080]',
        'outtmpl': r'E:\Python_projects\downloaded_stuff\videos\%(title)s.%(ext)s',
        'nonplaylist': True
    }
    with yd.YoutubeDL(configs) as somth:
        somth.download([url])


def audio_dl():
    url = input('Enter the url: ')
    configs = {
        'format': 'bestaudio/best',
        'outtmpl': r'E:\Python_projects\downloaded_stuff\songs\%(title)s.%(ext)s',#the directory on which the downloaded item will be saved
        'ffmpeg_location': r'C:\Users\User\AppData\Local\Microsoft\WinGet\Links',#if I download a video and I want its audio this will automatically send it to songs folder
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }
        ]
    }
    with yd.YoutubeDL(configs) as aud_dl:# same as aud_dl = yd.YoutubeDL(configs)
        aud_dl.download([url])

commands = {
    'video': video_downloader,
    'audio': audio_dl
}

command = commands.get(sys.argv[1])
def main():
    if len(sys.argv) < 2:
        sys.exit('Not enough arguments on the terminal')
    if command:
        command()
    else:
        sys.exit('Error')

if __name__ == '__main__':
    main()
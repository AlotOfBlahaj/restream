import subprocess
from subprocess import PIPE
from config import quailty, rtmp_link


def get_hls(video_dict):
    if video_dict['Provide'] == 'Youtube':
        commond = ['streamlink', '--stream-url', video_dict['Target'], quailty]
        # commond = ['youtube-dl', '-g', '-f', 'best[height<=480]', '--no-playlist', video_dict['Target']]
        p = subprocess.run(commond, stdout=PIPE, stderr=PIPE, universal_newlines=False, encoding='utf-8')
        hls_link = p.stdout
        hls_link = hls_link.replace('\n', '')
        return hls_link
    elif video_dict['Provide'] == 'Twitcasting':
        hls_link = video_dict['Ref']
        return hls_link


def push_streaming(hls_link, rtmp_link):
    commond = ['ffmpeg', '-i', f'{hls_link}', '-vcodec', 'copy', '-acodec', 'aac', '-f', 'flv', rtmp_link]
    print(commond)
    subprocess.run(commond)


def process_video(video_dict):
    hls = get_hls(video_dict)
    push_streaming(hls, rtmp_link)

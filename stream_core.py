import subprocess
from subprocess import PIPE
from config import quailty, rtmp_link


def get_hls(video_dict):
    if video_dict['Provide'] == 'Youtube':
        commond = ['streamlink', '--stream-link', video_dict['target'], quailty]
        p = subprocess.run(commond, stdout=PIPE, stderr=PIPE, universal_newlines=True, encoding='utf-8')
        hls_link = p.stdout
        return hls_link
    elif video_dict['Provide'] == 'Twitcasting':
        hls_link = video_dict['Ref']
        return hls_link


def push_streaming(hls_link, rtmp_link):
    commond = ['ffmpeg', '-i', hls_link, '-vcodec', 'copy', '-acodec', 'aac', '-f', 'flv', rtmp_link]
    print(f'hls: {hls_link}\nrtmp: {rtmp_link}')
    subprocess.run(commond)


def process_video(video_dict):
    hls = get_hls(video_dict)
    push_streaming(hls, rtmp_link)
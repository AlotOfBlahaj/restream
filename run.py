from youtube import Youtube
from twitcasting import Twitcasting
from config import youtube_channel, twitcasting_id

y = Youtube(youtube_channel)
y.start()
t = Twitcasting(twitcasting_id)
t.start()

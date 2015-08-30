import telnetlib
import json
import ConfigParser

settings = ConfigParser.ConfigParser()
settings.read('config.ini')


def play_music():

    tn = telnetlib.Telnet(settings.get('Music', 'SPOP_TELNET_HOST'), settings.get('Music', '6602'))
    tn.read_some()

    # Try to get the correct playlist
    try:
        tn.write("ls\n")
        playlistinfo = tn.read_until("}]}")
        playlist_json = json.loads(playlistinfo)
        for playlist in playlist_json['playlists']:
            if(playlist['name'] == settings.get('Music', 'SPOTIFY_PLAYLIST')):
                playlist_index= playlist['index']
    except:
        # Telnet error: lets use a hardcoded index
        playlist_index = 5

    # Check if shuffle setting is as set
    try:
        tn.write("status\n")
        status = tn.read_until("}")
        status_json = json.loads(status)
        if(not status_json['shuffle'] == settings.getboolean('Music', 'SPOTIFY_SHUFFLE')):
            tn.write("shuffle\n")
    except:
        pass

    # Start playlist
    tn.write("play " + str(playlist_index) + "\n")


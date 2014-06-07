import urllib2
import urllib
import ast
import soundcloud
import sys
import os
from threading import Thread


def get_all_tracks():
    response = urllib2.urlopen("http://poolsideapi2.herokuapp.com/tracks")
    tracks = ast.literal_eval(response.read())
    return tracks


def download_song(stream_url, song_name):
    url = urllib.urlopen(stream_url)
    # print url.getcode()
    if url.getcode() == 200:
        track_dir = "PoolSideTracks\%s" % song_name + ".mp3"
        urllib.urlretrieve(stream_url, track_dir)


def download_track_list(track_list):

    client = soundcloud.Client(client_id='CLIENT_ID')

    track_no = 1
    num_of_tracks = len(track_list)

    for track in track_list:
        try:
            song_name = "%s - %s" % (track['title'], track['artist'])
            print "Downloading: %d/%d -- %s" %(track_no, num_of_tracks, song_name)
            the_track = client.get('/tracks/%s' % track['scId'])
            stream_url = client.get(the_track.stream_url, allow_redirects=False)
            thread = Thread(target=download_song, args=[stream_url.location, song_name])
            thread.start()
            thread.join()
        except:
            pass

        track_no += 1


def get_tracks_to_download(track_diff, get_tracks):
    tracks_to_download = []
    for track in get_tracks:
        if track["title"].strip() + " - " + track["artist"].strip() in track_diff:
            tracks_to_download.append(track)
    return tracks_to_download


def main():
    curr_tracks = [track.strip("\n.mp3") for track in os.listdir('C:\Users\Gary\Music\Poolside.fm')]
    get_tracks = get_all_tracks()
    new_tracks = [track["title"].strip() + " - " + track["artist"].strip() for track in get_tracks]
    track_diff = list(set(new_tracks) - set(curr_tracks))

    tracks_to_download = get_tracks_to_download(track_diff, get_tracks)
    download_track_list(tracks_to_download)

if __name__ == "__main__":
    main()

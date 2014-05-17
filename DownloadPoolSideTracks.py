__author__ = 'gary'

import urllib2
import urllib
import ast
import soundcloud
import sys
import curses
from threading import Thread

def download_song(stream_url, song_name):
    url = urllib.urlopen(stream_url)
    # print url.getcode()
    if url.getcode() == 200:
        track_dir = "PoolSideTracks/%s" % song_name + ".mp3"
        urllib.urlretrieve(stream_url, track_dir)

def get_all_tracks():
    response = urllib2.urlopen("http://poolsideapi2.herokuapp.com/tracks")
    tracks = ast.literal_eval(response.read())
    return tracks

def update_progress(progress, cur_num, total_num, dataString):
    stdscr = curses.initscr()
    stdscr.clear()
    sys.stdout.write('\rProcessed: {0}/{1} -- [{2}] {3}% ({4})'.format(cur_num, total_num, '#'*(progress/10), progress, dataString))
    sys.stdout.flush()

def main():

    # outFile = open('poolSideTracks.txt', 'w')
    client = soundcloud.Client(client_id='CLIENT_ID')

    all_tracks = get_all_tracks()

    track_no = 1
    num_of_tracks = len(all_tracks)

    for track in all_tracks:
        try:
            the_track = client.get('/tracks/%s' % track['scId'])
            stream_url = client.get(the_track.stream_url, allow_redirects=False)
            song_name = "%s - %s" % (track['title'], track['artist'])
            thread = Thread(target=download_song, args=[stream_url.location, song_name])
            thread.start()
            thread.join()
            # outFile.write("%s,%s\n" % (stream_url.location, song_name))
            update_progress(int((float(track_no)/num_of_tracks)*100), track_no, num_of_tracks, song_name)
            # print "%s -- Found track: %s\n" % (track_no, track['scId'])
        except:
            # print "%s -- Could not find track: %s\n" % (track_no, track['scId'])
            # For tracks that cannot be found ie. 404
            pass

        track_no += 1

    # outFile.close()

    # print "Complete."

if __name__ == "__main__":
    main()

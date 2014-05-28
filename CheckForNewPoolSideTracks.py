import urllib2
import ast

def get_all_tracks():
    response = urllib2.urlopen("http://poolsideapi2.herokuapp.com/tracks")
    tracks = ast.literal_eval(response.read())
    return tracks

def main():
  outa = open("curr_tracks.txt", "w")
  outb = open("new_tracks.txt", "w")

  f = open('poolSideTrackList.txt', 'r')
  curr_tracks = [track.strip("\n.mp3") for track in f.readlines()]
  new_tracks = [track["title"].strip() + " - " + track["artist"].strip() for track in get_all_tracks()]
  track_diff = list(set(new_tracks) - set(curr_tracks))
  f.close()

  # new_tracks = get_all_tracks()

  print len(curr_tracks)
  print len(new_tracks)
  print len(track_diff)

  for track in sorted(curr_tracks):
    outa.write(track + "\n")

  for track in sorted(new_tracks):
    outb.write(track + "\n")
    
  for track in track_diff:
    print track

  # for track in new_tracks:
  #   print track

  outa.close()
  outb.close()

if __name__ == "__main__":
  main()

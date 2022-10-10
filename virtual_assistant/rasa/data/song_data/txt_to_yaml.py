import random

length = 50

templates = [
    "could you play [SONG_HERE](song) by [ARTIST_HERE](music_artist)",
    "can you play [SONG_HERE](song) by [ARTIST_HERE](music_artist)",
    "could you please play [SONG_HERE](song) by [ARTIST_HERE](music_artist)",
    "can you please play [SONG_HERE](song) by [ARTIST_HERE](music_artist)",
    "play [SONG_HERE](song) by [ARTIST_HERE](music_artist)",
    "play [SONG_HERE](song) by [ARTIST_HERE](music_artist)",
    "play the song [SONG_HERE](song) by [ARTIST_HERE](music_artist)",
    "could you play [SONG_HERE](song)",
    "could you play the song [SONG_HERE](song)",
    "can you play [SONG_HERE](song)",
    "can you play the song [SONG_HERE](song)",
    "could you please play [SONG_HERE](song)",
    "could you please play the song [SONG_HERE](song)",
    "can you please play [SONG_HERE](song)",
    "can you please play the song [SONG_HERE](song)",
    "play the song [SONG_HERE](song)",
    "play the song [SONG_HERE](song)",
    "play [SONG_HERE](song)"
]

text  = 'version: "3.1"\n\n'
text += 'nlu:\n'
text += f'- intent: play_song\n'
text += '  examples: |\n'

with open('songs.txt', 'r', encoding='utf-8') as f:
    for line in f:
        song, artist = line.strip().split(';', 1)
        entry = random.choice(templates).replace('SONG_HERE', song).replace('ARTIST_HERE', artist)
        text += '    - ' + entry + '\n'

        length -= 1
        if length <= 0:
            break

with open('song_data.yml', 'w', encoding='utf-8') as f:
    f.write(text)
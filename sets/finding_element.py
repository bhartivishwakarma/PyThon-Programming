allowed_tags = ['pop', 'hip-hop', 'rap', 'dance', 
                'electronic', 'latin', 'indie', 
                'alternative rock', 'classical', 'k-pop', 
                'country', 'rock', 'metal', 'jazz', 
                'exciting', 'sad', 'happy', 'upbeat', 
                'party', 'synth', 'rhythmic', 'emotional',
                 'relationship', 'warm', 'guitar',
                  'fiddle', 'romance', 'chill', 'swing']

song_data_users = {'Retro Words': ['pop', 'explosion',
                                    'hammer', 'bomb', 'warm', 
                                    'due', 'writer', 'happy', 
                                    'horrible', 'electric', 
                                    'mushroom', 'shed']}


tag_set =set(song_data_users["Retro Words"])
bad_tags = []
for tag in tag_set:
  if tag not in allowed_tags:
       bad_tags.append(tag)
for bad in bad_tags:
  tag_set.discard(bad)
song_data_users={"Retro Words":tag_set}
print(song_data_users)

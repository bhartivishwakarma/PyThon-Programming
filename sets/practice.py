music_tags = {'pop', 'warm', 'happy', 'electronic', 'synth', 'dance', 'upbeat'}


my_tags=frozenset({'pop','electronic','relaxing','slow','synth'})
frozen_tag_union=my_tags | music_tags
regular_tag_intersect= music_tags & my_tags
frozen_tag_difference=my_tags - music_tags
regular_tag_sd=music_tags ^ my_tags

song_data_users = {'Retro Words': ['pop', 'onion', 'warm', 'helloworld', 'happy', 'spam', 'electric']}


tag_set=set(song_data_users["Retro Words"])
tag_set.remove("onion")
tag_set.remove("helloworld")
tag_set.remove("spam")
song_data_users={"Retro Words":tag_set}
print(song_data_users)
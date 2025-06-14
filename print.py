from datetime import datetime

def print_user_playlists(user_playlists_dict):
    max_name = len(max(user_playlists_dict, key=len)) + 2
    max_number = len(str(max(user_playlists_dict.values()))) + \
        len(" tracks") + 1

    print("User playlists")
    print("".join([char*(max_name + max_number + 1) for char in "_"]))
    for key, value in user_playlists_dict.items():
        name_part = key + \
            "".join([char*((max_name - 1) - len(key)) for char in " "])
        number_part = f"{value} tracks" + \
            "".join([char*((max_number - 1) - len(str(f"{value} tracks")))
                    for char in " "])
        print(f"{number_part} | {name_part}")
    print("".join([char*(max_name + max_number + 1) for char in "‾"]))


def print_artists_from_liked_songs(artists_dict, following_artists):
    now = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
    filename = f'artists_from_liked_songs_{now}.txt'
    f = open(filename, "w")
    f.write('Artists from liked songs\n\n')
    f.close()
    # Sort dict by liked songs quantity
    artists_dict = dict(sorted(artists_dict.items(), key=lambda item: (-item[1], item[0][0].casefold())))
    print(f'\nThere are {len(artists_dict)} artists\n')
    print(f'{artists_dict}')
    following_text = ""
    for artist, saved in artists_dict.items():
        if artist[1] in following_artists:
            following_text = "Following"
        else:
            following_text = "Not following"
        print(f"{saved} saved from {artist[0]} ({following_text})")
        try:
            f = open(filename, "a")
            f.write(f"{saved} saved from {artist[0]} ({following_text})\n")
            f.close()
        except:
            print(f"{saved} saved from ###   ({following_text})\n")
            f.close()
    print(f'{filename} created at root project!\n')


def print_top(list_top, range):
    now = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
    filename = f'top_songs_{range}_{now}.txt'
    with open(filename, 'w') as f:
        f.write('Top songs\n\n')
        for line in list_top:
            f.write(f"{line})\n")
        
    f.close
            
    print(f'{filename} created at root project!\n')

    #print(f"\nTop 50 {list_top[-1]}\n")
    #index = 1

    #for i in list_top[:-1]:
    #    print(f"Top {index} - {i}")
    #    index += 1
    print()


def print_followed_people(following_artists, sort_type):
    if (sort_type == "artist"):
        following_artists = dict(
            sorted(following_artists.items(), key=lambda item: item[0]))
    else:
        following_artists = dict(
            sorted(following_artists.items(), key=lambda item: item[1], reverse=True))

    max_name = len(max(following_artists, key=len)) + 2
    max_number = len(str(max(following_artists.values()))) + \
        len(" followers") + 2

    print("\nFollowed people\n")
    print("".join([char*(max_name + max_number + 1) for char in "_"]))
    for key, value in following_artists.items():
        name_part = key + \
            "".join([char*((max_name - 1) - len(key)) for char in " "])
        number_part = str(value) + " followers" +\
            "".join([char*((max_number - 1) - len(str(value)))
                    for char in " "])
        print(f"{name_part} | {number_part}")
    print("".join([char*(max_name + max_number + 1) for char in "‾"]))
    print()


def print_recently_played(recently_played):
    print("\nRecently played:\n")
    for i in recently_played:
        print(i)
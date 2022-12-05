from geckify import Geckify
import constant


def authorize_new_user():
    from authorize import Authorize
    authorize = Authorize()
    authorization_url = authorize.begin_authorization()
    print('Please go here and authorize: ', authorization_url)

    redirect_response = input(
        '\n\nPaste the full redirect URL here: ')
    access_token = authorize.get_token(redirect_response)

    return access_token


def print_user_playlists(user_playlists_dict):
    max_name = len(max(user_playlists_dict, key=len)) + 2
    max_number = len(str(max(user_playlists_dict.values()))) + \
        len(" tracks") + 1

    print("User playlists")
    print("".join([char*(max_name + max_number + 1) for char in "_"]))
    for key, value in user_playlists_dict.items():
        name_part = key + \
            "".join([char*((max_name - 1) - len(key)) for char in " "])
        number_part = "{} tracks".format(value) + \
            "".join([char*((max_number - 1) - len(str("{} tracks".format(value))))
                    for char in " "])
        print("{} | {}".format(number_part, name_part))
    print("".join([char*(max_name + max_number + 1) for char in "‾"]))


def print_artists_from_liked_songs(artists_dict, following_artists):
    print("Artists from liked songs\n")
    artists_dict = dict(sorted(artists_dict.items(),
                        key=lambda item: item[1], reverse=True))

    following_text = ""
    for artist, saved in artists_dict.items():
        if artist[1] in following_artists:
            following_text = "Following"
        else:
            following_text = "Not following"

        print("{} saved from {} ({})".format(
            saved, artist[0], following_text))
    print()


def print_top(list_top):
    print("\nTop 50 {}\n".format(list_top[-1]))
    index = 1

    for i in list_top[:-1]:
        print("Top {} - {}".format(index, i))
        index += 1
    print()


def print_followed_people(following_artists, sort_type):
    if (sort_type == "artist"):
        following_artists = dict(
            sorted(following_artists.items(), key=lambda item: item[1], reverse=True))
    else:
        following_artists = dict(
            sorted(following_artists.items(), key=lambda item: item[0]))

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
        print("{} | {}".format(name_part, number_part))
    print("".join([char*(max_name + max_number + 1) for char in "‾"]))
    print()


if __name__ == "__main__":
    geckify = Geckify()
    while True:
        print("0. Exit")
        print("1. Login with my account")
        print("2. Login with other account")
        try:
            option = int(input(constant.CHOOSE_OPTION))
            print()
            match option:
                case 0:
                    print("See ya!")
                    exit()
                case 1:
                    break
                case 2:
                    access_token = authorize_new_user()
                    geckify.set_spotify_token(access_token)
                    break
                case _:
                    print(constant.WRONG_INPUT)
                    print()
            print()
        except ValueError:
            print("Wrong input")
            print()
    while True:
        print("GECKIFY")
        print("MENU")
        print("0. Exit")
        print("1. Print my playlists")
        print("2. Check artists from my Liked Songs")
        print("3. Check top artists")
        print("4. Check top songs")
        print("5. Check followed people")
        try:
            option = int(input(constant.CHOOSE_OPTION))
            print()
            match option:
                case 0:
                    print("See ya!")
                    break
                case 1:
                    print_user_playlists(geckify.get_user_playlists())
                case 2:
                    artists = geckify.get_artists_on_user_tracks()
                    following = geckify.following_people("id-name")
                    print_artists_from_liked_songs(artists, following)
                case 3:
                    print("1. Short range (~1 month)")
                    print("2. Medium range (6 months)")
                    print("3. Long range (All-time)")
                    option_range = int(input(constant.CHOOSE_OPTION))
                    print()
                    match option_range:
                        case 1:
                            print_top(geckify.get_top_user(
                                "artists", "short_term"))
                        case 2:
                            print_top(geckify.get_top_user(
                                "artists", "medium_term"))
                        case 3:
                            print_top(geckify.get_top_user(
                                "artists", "long_term"))
                        case _:
                            print(constant.WRONG_INPUT)
                            print()
                case 4:
                    print("1. Short range (~1 month)")
                    print("2. Medium range (6 months)")
                    print("3. Long range (All-time)")
                    option_range = int(input(constant.CHOOSE_OPTION))
                    print()
                    match option_range:
                        case 1:
                            print_top(geckify.get_top_user(
                                "tracks", "short_term"))
                        case 2:
                            print_top(geckify.get_top_user(
                                "tracks", "medium_term"))
                        case 3:
                            print_top(geckify.get_top_user(
                                "tracks", "long_term"))
                        case _:
                            print(constant.WRONG_INPUT)
                            print()
                case 5:
                    print("1. Order by artist name")
                    print("2. Order by followers quantity")
                    option_range = int(input(constant.CHOOSE_OPTION))
                    print()
                    match option_range:
                        case 1:
                            print_followed_people(
                                geckify.following_people("name-followers"), "artist")
                        case 2:
                            print_followed_people(
                                geckify.following_people("name-followers"), "followers")
                        case _:
                            print(constant.WRONG_INPUT)
                            print()
                case _:
                    print(constant.WRONG_INPUT)
                    print()
            print()
        except ValueError:
            print("Wrong input")
            print()

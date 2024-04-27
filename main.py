from geckify import Geckify
from constant import CHOOSE_OPTION, WRONG_INPUT
from dotenv import load_dotenv
from datetime import datetime

# Login part
def login():
    while True:
        try:
            login_menu()
            option = int(input(CHOOSE_OPTION))
            print()
            res = login_manage_option(option)
            if res:
                break
            print()
        except ValueError:
            print("Wrong input")
            print()

# Print login menu 
def login_menu():
    print("0. Exit")

# Manage the option selected of the login menu
def login_manage_option(option):
    match option:
        case 0:
            print("See ya!")
            exit()
        case 1:
            response = check_user()
            if response != 0:
                return True
        case 2:
            response = new_user_login()
            if response != 0:
                return True
        case _:
            print(WRONG_INPUT)
            print()

# Check if the user 
def check_user():
    from data_store import check_has_items, load_data
    if check_has_items():
        users = load_data()
        user = select_user(users["users"])
        response = test_user(user["access_token"])
        if type(response) is dict:   
            set_values_to_geckify(user)
            return response
        if response[0] == "0":
            print(f"Error while trying to get user profile: {response[1:]}.")
            if response[1:] == "The access token expired":
                res = do_refresh_token(user["refresh_token"])
                return res
            return 0

    else:
        print("Oops, looks like no accounts are saved\nGoing to new user login...")
        response = new_user_login()
        return response


def select_user(users):
    user = ""
    while True:
        index = 1
        for i in users:
            print(f"{index} - {i['display_name']} (id: {i['id']})")
            index += 1

        try:
            option_user = int(input(CHOOSE_OPTION))
            print()
            if (option_user > 0) and (option_user <= len(users)):
                print(
                    f"User {users[option_user-1]['display_name']} (id: {users[option_user-1]['id']}) selected.\n")
                user = users[option_user-1]
                break
            else:
                print(f"Oops, {option_user} is not an available option!")
        except TypeError:
            print("Wrong input")
            print()

    return user


def new_user_login():
    while True:
        access_token, refresh_token = authorize_new_user()
        if access_token != 0:
            break
        print("Returning to login...")

    response = test_user(access_token)
    if type(response) is dict:
        user = {
            "id": response["id"],
            "display_name": response["display_name"],
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        print(user)
        res = manage_spotify_token(user)
        if res == 0:
            return 0
        set_values_to_geckify(user)
        return 1
    if response[0] != "0":
        print(f"Error while trying to get user profile: {response[1:]}.")
        res = ""
        if response[1:] == "The access token expired":
            res = do_refresh_token(user["refresh_token"])
            return res
        return 0
    print("Error")
    return 0


def test_user(access_token):
    return geckify.get_user_profile(access_token)


def set_values_to_geckify(user):
    geckify.set_spotify_token(user["access_token"])
    geckify.set_user_id(user["id"])
    geckify.set_display_name(user['display_name'])
    print(f"Hi, {geckify.get_display_name()}!\n")


def authorize_new_user():
    from authorize import Authorize
    authorize = Authorize()
    authorization_url = authorize.begin_authorization()
    print('Please go here and authorize: ', authorization_url)

    redirect_response = input(
        '\n\nPaste the full redirect URL here: ')
    access_token, refresh_token = authorize.get_token(redirect_response)
    print(f"Access Token: {access_token}\nRefresh Token: {refresh_token}")

    return access_token, refresh_token


def manage_spotify_token(user, type: str = "None"):
    from data_store import check_user_exists, add_data, replace_access_token

    if type == "None":
        if check_user_exists(user["id"]):
            print("Looks like the user is already added, next time you can login with the saved accounts to save time =D")
            add_data(user)
        else:
            add_data(user)
        return
    if type == "refresh":
        if check_user_exists(user["id"]):
            print(f'Ya existe')
            replace_access_token(user)
        else:
            print("Cannot replace, user is not saved.")
            return 0
    else:
        print(f"Parameter {type} is not controlled.")
        return 0


def do_refresh_token(refresh_token):
    print("Token expired. Refreshing...\n")
    new_access_token = geckify.refresh_spotify_token(refresh_token)
    response = test_user(new_access_token)
    if type(response) is dict:
        return 1
    if response[0] == "0":
        user = {
            "id": response["id"],
            "display_name": response["display_name"],
            "access_token": new_access_token,
            "refresh_token": refresh_token
        }
        res = manage_spotify_token(user, "refresh")
        if res == 0:
            return 0
        set_values_to_geckify(user)
        return 1


def app():
    while True:
        try:
            app_print_menu()
            option = int(input(CHOOSE_OPTION))
            print()
            app_manage_option(option)
            print()
        except ValueError:
            print("Wrong input")
            print()


def app_print_menu():
    print("GECKIFY")
    print("MENU")
    print("0. Exit")
    print("1. Print my playlists")
    print("2. Check artists from my Liked Songs")
    print("3. Check top artists")
    print("4. Check top songs")
    print("5. Check followed people")
    print("6. Check recently played songs")


def app_manage_option(option):
    match option:
        case 0:
            print("See ya!")
            exit()
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
            option_range = int(input(CHOOSE_OPTION))
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
                    print(WRONG_INPUT)
                    print()
        case 4:
            print("1. Short range (~1 month)")
            print("2. Medium range (6 months)")
            print("3. Long range (All-time)")
            option_range = int(input(CHOOSE_OPTION))
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
                    print(WRONG_INPUT)
                    print()
        case 5:
            print("1. Order by artist name")
            print("2. Order by followers quantity")
            option_range = int(input(CHOOSE_OPTION))
            print()
            match option_range:
                case 1:
                    print_followed_people(
                        geckify.following_people("name-followers"), "artist")
                case 2:
                    print_followed_people(
                        geckify.following_people("name-followers"), "followers")
                case _:
                    print(WRONG_INPUT)
                    print()
        case 6:
            print_recently_played(geckify.get_recently_played())
        case _:
            print(WRONG_INPUT)
            print()


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
    with open(filename, 'w') as f:
        f.write('Artists from liked songs\n\n')

        # Sort dict by liked songs quantity
        artists_dict = dict(sorted(artists_dict.items(),
                        key=lambda item: (-item[1], item[0][0].casefold())))

        following_text = ""
        for artist, saved in artists_dict.items():
            if artist[1] in following_artists:
                following_text = "Following"
            else:
                following_text = "Not following"

            f.write(f"{saved} saved from {artist[0]} ({following_text})\n")
            
    print(f'{filename} created at root project!\n')


def print_top(list_top):
    print(f"\nTop 50 {list_top[-1]}\n")
    index = 1

    for i in list_top[:-1]:
        print(f"Top {index} - {i}")
        index += 1
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


if __name__ == "__main__":
    load_dotenv()
    geckify = Geckify()

    login()
    app()

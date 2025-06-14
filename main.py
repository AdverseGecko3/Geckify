from geckify import Geckify
from dotenv import load_dotenv
from constant import CHOOSE_OPTION, WRONG_INPUT


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
    print("1. Login with my saved accounts")
    print("2. Login with new account")

# Manage the option selected of the login menu
def login_manage_option(option):
    match option:
        # Exit
        case 0:
            print("See ya!")
            exit()
        # Login with saved accounts
        case 1:
            response = check_user()
            return True if response != 0 else False
        # Login with new account
        case 2:
            response = new_user_login()
            return True if response != 0 else False
        case _:
            print(WRONG_INPUT)
            print()

# Load available users
def check_user():
    from data_store import check_has_items, load_data
    # Check if there are saved users
    if check_has_items():
        # Load the saved users
        users = load_data()
        # Select a user
        user = select_user(users["users"])
        # Test the user is available
        if user == 0:
            return 0
        response = test_user(user["access_token"])
        # If the response is a user set the values to Geckify
        if type(response) is dict:   
            set_values_to_geckify(user)
            return response
        # If the response is not a user try to refresh the token
        if response[0] == "0":
            print(f"Error while trying to get user profile: {response[1:]}.")
            if response[1:] == "The access token expired":
                res = do_refresh_token(user["refresh_token"])
                return res
            return 0
    # If there are no saved users, redirect to the new user flow
    else:
        print("Oops, looks like no accounts are saved\nGoing to new user login...")
        response = new_user_login()
        return response

# Print the given users and select one of them
def select_user(users):
    user = ""
    while True:
        index = 1
        # Print the given users
        print("0 - Go back")
        for i in users:
            print(f"{index} - {i['display_name']} (id: {i['id']})")
            index += 1

        try:
            # Get the user value
            option_user = int(input(CHOOSE_OPTION))
            print()
            # Check the value is between the available options
            if option_user == 0:
                user = 0
                break
            if option_user > 0 and option_user <= len(users):
                print(
                    f"User {users[option_user-1]['display_name']} (id: {users[option_user-1]['id']}) selected.\n")
                # Set the selected user
                user = users[option_user-1]
                break
            else:
                print(f"Oops, {option_user} is not an available option!")
        except TypeError:
            print("Wrong input")
            print()

    return user

# Flow of new user
def new_user_login():
    while True:
        # Start the flow of creating and authorizating a new user
        access_token, refresh_token = authorize_new_user()
        # If access token has a value, continue
        if access_token != 0 and refresh_token != 0:
            break
        return 0

    # Test the user is available
    response = test_user(access_token)
    # If the response is a user set the values to Geckify
    if type(response) is dict:
        user = {
            "id": response["id"],
            "display_name": response["display_name"],
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        print(user)
        # Save the user
        res = manage_spotify_token(user)
        if res == 0:
            return 0
        set_values_to_geckify(user)
        return 1
    # If the response is not a user try to refresh the token
    if response[0] != "0":
        print(f"Error while trying to get user profile: {response[1:]}.")
        res = ""
        if response[1:] == "The access token expired":
            res = do_refresh_token(user["refresh_token"])
            return res
        return 0
    print("Error")
    return 0

# Test if the user is being resolved
def test_user(access_token):
    return geckify.get_user_profile(access_token)

# Save the fetched values to Geckify
def set_values_to_geckify(user):
    geckify.set_spotify_token(user["access_token"])
    geckify.set_user_id(user["id"])
    geckify.set_display_name(user['display_name'])
    print(f"Hi, {geckify.get_display_name()}!\n")

# Authorization process flow
def authorize_new_user():
    from authorize import Authorize
    # Initialize the Authorize class
    authorize = Authorize()
    # Create the authorization URL
    authorization_url = authorize.begin_authorization()
    print('Please go here and authorize: ', authorization_url)
    # Ask the user to enter the response of the URL
    redirect_response = input(
        '\n\nPaste the full redirect URL here: ')
    # Get the access token and refresh token from the URL
    access_token, refresh_token = authorize.get_token(redirect_response)
    if access_token == 0 and refresh_token == 0:
        return 0, 0
    print(f"Access Token: {access_token}\nRefresh Token: {refresh_token}")

    return access_token, refresh_token

# 
def manage_spotify_token(user, type: str = "None"):
    from data_store import check_user_exists, add_data, replace_access_token

    # Default type
    if type == "None":
        # If the user already exists, print an informative message
        if check_user_exists(user["id"]):
            print("Looks like the user is already added, next time you can login with the saved accounts to save time =D")
            #add_data(user)
        # If not, add the user to users.data
        else:
            add_data(user)
        return
    # Refresh type
    if type == "refresh":
        # If the user already exists, replace the access token
        if check_user_exists(user["id"]):
            print(f'The user already exists. Replacing access token...')
            replace_access_token(user)
        # If not, print an informative message
        else:
            print("Cannot replace, user is not saved.")
            return 0
    # Unexpeted type parameter
    else:
        print(f"Parameter {type} is not controlled.")
        return 0


def do_refresh_token(refresh_token):
    print("Token expired. Refreshing...\n")
    # Refresh the spotify token
    new_access_token = geckify.refresh_spotify_token(refresh_token)
    # Test the user is available
    response = test_user(new_access_token)
    if type(response) is dict:
        print(f"Token refreshed.")
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
    import print

    match option:
        case 0:
            print("See ya!")
            exit()
        case 1:
            print.print_user_playlists(geckify.get_user_playlists())
        case 2:
            artists = geckify.get_artists_on_user_tracks()
            following = geckify.following_people("id-name")
            print.print_artists_from_liked_songs(artists, following)
        case 3:
            print("1. Short range (~1 month)")
            print("2. Medium range (6 months)")
            print("3. Long range (All-time)")
            option_range = int(input(CHOOSE_OPTION))
            print()
            match option_range:
                case 1:
                    print.print_top(geckify.get_top_user(
                        "artists", "short_term"))
                case 2:
                    print.print_top(geckify.get_top_user(
                        "artists", "medium_term"))
                case 3:
                    print.print_top(geckify.get_top_user(
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
                    print.print_top(geckify.get_top_user(
                        "tracks", "short_term"), "short_term")
                case 2:
                    print.print_top(geckify.get_top_user(
                        "tracks", "medium_term"), "medium_term")
                case 3:
                    print.print_top(geckify.get_top_user(
                        "tracks", "long_term"), "long_term")
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
                    print.print_followed_people(
                        geckify.following_people("name-followers"), "artist")
                case 2:
                    print.print_followed_people(
                        geckify.following_people("name-followers"), "followers")
                case _:
                    print(WRONG_INPUT)
                    print()
        case 6:
            print.print_recently_played(geckify.get_recently_played())
        case _:
            print(WRONG_INPUT)
            print()

#main
if __name__ == "__main__":
    load_dotenv()
    geckify = Geckify()

    login()
    app()
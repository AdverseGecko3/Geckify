import pickle
from constant import USERS_DATA_FILE


'''
Adds a dict to the users array, where the new user has a "id", "display_name", "access_token"
'''

# Load the content of the data file
def load_data():
    try:
        input_file = USERS_DATA_FILE
        fd = open(input_file, 'rb')
        dataset = pickle.load(fd)
        fd.close()
        return dataset
    except FileNotFoundError:
        # If file is not found, create it
        print("users.data file not found. Creating file...")
        add_data("")
        print("File created!")
        return 0

# Add an item to the data file
def add_data(data):
    current_data = ""
    if data != "":
        current_data = load_data()
    else:
        print("Adding default data")
        current_data = {"users": []}

    if data != "":
        current_data["users"].append(data)

    output_file = USERS_DATA_FILE
    fw = open(output_file, 'wb')
    pickle.dump(current_data, fw)
    fw.close()

# Dump the passed data to the data file
def replace_data(data):
    output_file = USERS_DATA_FILE
    fw = open(output_file, 'wb')
    pickle.dump(data, fw)
    fw.close()

# Check if the  data file is not empty
def check_has_items():
    try:
        dataset = load_data()
        return True if len(dataset["users"]) != 0 else False
    except FileNotFoundError:
        # If file is not found, create it
        print("users.data file not found. Creating file...")
        add_data("")
        print("File created!")
        return False

# Check if the given user_id is in the data file
def check_user_exists(user_id):
    dataset = load_data()
    user_is_added = False
    if len(dataset["users"]) == 0:
        #cuidao
        print()
    for i in dataset["users"]:
        if i["id"] == user_id:
            user_is_added = True
            break
    return user_is_added

# Find the given user and replace the access_token, then replace the data
def replace_access_token(user):
    dataset = load_data()
    for i in dataset["users"]:
        if i["id"] == user["id"]:
            i["access_token"] = user["access_token"]
            break
    replace_data(dataset)

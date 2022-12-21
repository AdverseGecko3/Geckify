import pickle
from constant import USERS_DATA_FILE


class DataStore:
    def load_data(self):
        try:
            input_file = USERS_DATA_FILE
            fd = open(input_file, 'rb')
            dataset = pickle.load(fd).json()
            return dataset
        except FileNotFoundError:
            return 0

    def save_data(self, data):
        output_file = USERS_DATA_FILE
        fw = open(output_file, 'wb')
        pickle.dump(data, fw)
        fw.close()

    def delete_data(self):
        data = ""
        output_file = USERS_DATA_FILE
        fw = open(output_file, 'wb')
        pickle.dump(data, fw)
        fw.close()

    def check_has_items(self):
        input_file = USERS_DATA_FILE
        fd = open(input_file, 'rb')
        dataset = pickle.load(fd).json()
        if dataset != None:
            return True
        else:
            return False

    def check_user_exists(self, user_id):
        r = self.load_data()

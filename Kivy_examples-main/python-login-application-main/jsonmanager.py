from json import load, dump
from json.decoder import JSONDecodeError
from hashlib import sha256


def SHA256(text: str) -> str:
    return sha256(text.encode('utf-8')).hexdigest()


class JsonManager:
    def __init__(self) -> None:
        self.__FILE: str = 'data.json'    

    def load_file(self) -> dict:
        try:
            with open(self.__FILE, encoding='utf-8') as f:
                obj_json: dict = load(f)
        except (FileNotFoundError, JSONDecodeError):
            with open(self.__FILE, 'w+',encoding='utf-8') as file_error_json:
                RECOVER: dict = {'user': '',
                                 'email': '',
                                 'pass': ''}
                dump(RECOVER, file_error_json, indent=4)

        with open(self.__FILE, encoding='utf-8') as file_json:
            obj_json = load(file_json)
        return obj_json

    def insert(self, data: dict) -> None:
        data['user'] = SHA256(data['user'])
        data['email'] = SHA256(data['email'])
        data['pass'] = SHA256(data['pass'])

        with open(self.__FILE, 'w+', encoding='utf-8') as f:
           dump(data, f, indent=4)

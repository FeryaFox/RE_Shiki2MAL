import json
from ..dataclass.MALTokenDataclass import MALTokenInfo
import os


def convert_dataclass_to_dict(token_info: MALTokenInfo) -> dict:
    return {
        "token_type": token_info.token_type,
        "expires_in": token_info.expires_in,
        "access_token": token_info.access_token,
        "refresh_token": token_info.refresh_token
    }


def token_loader() -> MALTokenInfo | None:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir = os.path.abspath(os.path.join(current_dir, '../..', '..'))
        file_path = os.path.join(target_dir, 'token_mal.json')

        with open(file_path, 'r') as f:
            data = json.load(f)
        return MALTokenInfo(**data)
    except FileNotFoundError:
        return None

    # TODO надо сделать, чтобы как-то передавалось имя пользователя, чтобы сохранять несколько токенов
def token_saver(token_info: MALTokenInfo):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(current_dir, '../..', '..'))
    file_path = os.path.join(target_dir, 'token_mal.json')

    with open(file_path, 'w') as file:
        json.dump(convert_dataclass_to_dict(token_info), file, indent=4)

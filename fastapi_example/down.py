import os.path
import requests
from xdg import get_download_dir
from models import SendMediaReqModel
from ntchat.utils import generate_guid


def new_download_file():
    while True:
        path = os.path.join(get_download_dir(), generate_guid("temp"))
        if not os.path.isfile(path):
            return path


def get_local_path(model: SendMediaReqModel):
    if os.path.isfile(model.file_path):
        return model.file_path
    if not model.url:
        return None
    data = requests.get(model.url).content
    temp_file = new_download_file()
    with open(temp_file, 'wb') as fp:
        fp.write(data)
    return temp_file

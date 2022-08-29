import os.path
import time
import requests
from xdg import get_download_dir
from models import SendMediaReqModel


def get_local_path(model: SendMediaReqModel):
    if os.path.isfile(model.file_path):
        return model.file_path
    if not model.url:
        return None
    data = requests.get(model.url).content
    temp_file = os.path.join(get_download_dir(), str(time.time_ns()))
    with open(temp_file, 'wb') as fp:
        fp.write(data)
    return temp_file

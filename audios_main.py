import requests
from vk_api.audio import VkAudio
import vk_api
import data
import json


vk = None

def two_fact():
    code = input('Code? ')
    return code, True


def main():
    global vk
    login = data.LOGIN
    password = data.PASSWORD
    VK_SESSION = vk_api.VkApi(login, password, auth_handler=two_fact)
    vk = VK_SESSION


def auth_vk():
    global vk
    try:
        vk.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return


def get_session():
    global vk
    return vk


def update_audios(vk_session):
    """Обновление музыки"""
    data_audios = []
    urls_audio = []

    api = vk_session.get_api()
    vkaudio = VkAudio(vk_session)
    info = api.account.getProfileInfo()
    user_id = info['id']
    print(user_id)
    audios = vkaudio.get(owner_id=user_id)

    def get_dur(full_dur):
        min_dur = full_dur // 60
        sec_dur = full_dur % 60
        if sec_dur < 10:
            buf = sec_dur
            sec_dur = '0'+str(buf)
        return min_dur, sec_dur

    for audio in audios:
        dur = get_dur(audio['duration'])
        data_audios.append({'artist': audio['artist'],
                            'title': audio['title'],
                            'track_covers': audio['track_covers'],
                            'duration': dur})
        urls_audio.append({'url': audio['url']})

    """Загрузка словаря песен в json файл"""
    with open('data_audios.json', 'w') as write_file1:
        json.dump(data_audios, write_file1, sort_keys=True, indent=4)

    """Загрузка словаря urls песен в json файл"""
    with open('data_urls_audios.json', 'w') as write_file2:
        json.dump(urls_audio, write_file2, sort_keys=True, indent=4)


def download_audio(count):
    """Загрузка музыки"""
    with open("data_audios.json", "r") as rf:
        data = json.load(rf)

    with open('data_urls_audios.json', 'r') as jf:
        urls = json.load(jf)

    for i in range(0, count):
        _url = urls[i]['url']
        req = requests.get(_url, stream=True)
        if req.status_code == 200:
            with open(data[i]['artist'] + ' - ' + data[i]['title'] + '.mp3', 'wb') as a:
                a.write(req.content)


if __name__ == '__main__':
    main()

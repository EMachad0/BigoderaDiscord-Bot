import urllib.request
import json


def get_codeforces_user_info(handles):
    param = ''
    for handle in handles:
        param += handle + ';'
    with urllib.request.urlopen("https://codeforces.com/api/user.info?handles=" + param[:-1]) as url:
        codeforces_data = json.loads(url.read().decode())
        if codeforces_data['result'] == "FAILED":
            raise Exception("HANDLE NAO EXISTE")
        return codeforces_data['result']


def get_codeforces_user_maxRank(handles):
    users = {}
    for user in get_codeforces_user_info(handles):
        try:
            users[user['handle']] = {'maxRank': user['maxRank']}
        except KeyError as e:
            users[user['handle']] = {'maxRank': "unrated"}
    return users


if __name__ == "__main__":
    hds = get_codeforces_user_maxRank(['jvf', 'Machado', 'jnk'])
    for k, v in hds.items():
        print(k, v)

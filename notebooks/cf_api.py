import urllib.request
import json
import random

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

def get_codeforces_problem(handle, rating, tags):
    all_tags = ['2-sat', 'binary search', 'bitmasks', 'brute force', 'chinese remainder theory',
    'combinatorics','constructive algorithm','data strucutres','dfs and similar','divide and conquer',
    'dp','dsu','expression parsing','fft','flows','games','geometry','graph matchings','graphs','greedy',
    'hashing','implementations','interactive','math','matrices','meet-in-the-middle','number theory',
    'probabilities','schedules','shortest paths','sortings','string suffix strucutures','strings',
    'ternary search','trees','two pointers']
    correct_tags = ''
    for tag in tags:
        if tag in all_tags and tag not in correct_tags:
            correct_tags += tag + ';'
    problems = []
    solved = []
    if handle != '':
        with urllib.request.urlopen("https://codeforces.com/api/user.status?handle="+handle) as url:
            codeforces_data = json.loads(url.read().decode())
            for submission in codeforces_data['result']:
                if 'verdict' in submission and submission['verdict'] == 'OK':
                    solved.append([submission['problem']['contestId'],submission['problem']['index']])
    with urllib.request.urlopen("https://codeforces.com/api/problemset.problems?tags="+correct_tags) as url:
        codeforces_data = json.loads(url.read().decode())
        for problem in codeforces_data['result']['problems']:
            if 'rating' in problem and problem['rating'] == rating:
                problemId = [problem['contestId'],problem['index']]
                if problemId not in solved:
                    problems.append([problem['contestId'],problem['index']])
    if len(problems) == 0: return ''
    problem = problems[random.randint(0,len(problems)-1)]
    return 'https://codeforces.com/contest/'+str(problem[0])+'/problem/'+str(problem[1])


if __name__ == "__main__":
    hds = get_codeforces_user_maxRank(['jvf', 'Machado', 'jnk'])
    for k, v in hds.items():
        print(k, v)

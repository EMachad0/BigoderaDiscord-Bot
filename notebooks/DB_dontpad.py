from requests import post, get
from bs4 import BeautifulSoup
import os


class DB_dontpad:

    def __init__(self):
        self.contador_caga_pau = 0
        self.memes = []
        self.db_path = os.environ["DATABASE_DP_PATH"]
        self.load_data()
        print("DB do dontpad carregado")

    def load_data(self):
        try:
            data = self.pull(self.db_path)
            self.contador_caga_pau = int(data[0])
            self.memes = data[1:]
        except Exception as e:
            self.memes = ['caiu o dontpad']
            self.contador_caga_pau = 999999
            print(e)


    def save_data(self):
        try:
            data = str(self.contador_caga_pau) + '\n' + '\n'.join(self.memes)
            self.push(self.db_path, data)
        except Exception as e:
            print(e)

    def pull(self, path):
        data = get(url=path)
        soup = BeautifulSoup(data.text, "html.parser")
        old_text = soup.find('textarea').get_text()
        old_text = old_text.split('\n')

        return old_text

    def push(self, path, text):
        try:
            data = {'text': text}

            return post(url=path, data=data)
        except Exception as e:
            print(e)


db = DB_dontpad()

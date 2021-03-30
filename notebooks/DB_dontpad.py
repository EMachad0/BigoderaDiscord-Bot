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
        data = self.pull(self.db_path)
        self.contador_caga_pau = int(data[0])
        self.memes = data[1:]

    def save_data(self):
        data = str(self.contador_caga_pau) + '\n' + '\n'.join(self.memes)
        self.push(self.db_path, data)

    def pull(self, path):
        data = get(url=path)
        soup = BeautifulSoup(data.text, "html.parser")
        old_text = soup.find('textarea').get_text()
        old_text = old_text.split('\n')

        return old_text

    def push(self, path, text):
        data = {'text': text}

        return post(url=path, data=data)


db = DB_dontpad()

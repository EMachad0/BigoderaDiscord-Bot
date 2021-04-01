from discord.ext import commands, tasks
import random as r
from notebooks.DB_dontpad import db
from itertools import count, islice
from math import sqrt, gcd, log


class Meme(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        try:
            text = message.content
            print(text)
            res = ''
            if text.startswith('$meme'):
                res = meme()
            elif text.startswith('$addmeme'):
                res = add_meme(text)
            elif text.startswith('$contador_caga_pau'):
                res = contador_caga_pau()
            elif text.startswith('$roll'):
                res = roll(text)
            elif text.startswith('$par_ou_impar'):
                res = par_ou_impar()
            elif text.startswith('$primo'):
                res = primo(text)
            elif text.startswith('$calculadora'):
                res = calculadora(text)
            elif text.startswith('$fatorar'):
                res = fatorar(text)
            else:
                res = noncommand(message)
            if res:
                await message.channel.send(res)
        except Exception as e:
            print(f'Exception {e}: {e.args}')


def setup(bot):
    bot.add_cog(Meme(bot))


def meme():
    try:
        return r.choice(db.memes)
    except Exception as e:
        print(e)


def add_meme(text):
    try:
        db.load_data()
        new_meme = " ".join(text.split()[1:])
        if len(new_meme) < 5:
            return "Muito pequeno"
        else:
            db.memes.append(new_meme)
            db.save_data()
            return "Adicionado. Memes ativos: {}".format(len(db.memes))
    except Exception as e:
        print(e)


def par_ou_impar():
    if r.randrange(2):
        text = "Impar"
    else:
        text = "Par"
    return text


def contador_caga_pau():
    try:
        db.contador_caga_pau += 1
        db.save_data()
        return db.contador_caga_pau
    except Exception as e:
        print(e)


def noncommand(message):
    text = message.content.lower()
    ret = ""
    if "caga pau" in text:
        ret = "FELIPE WEISS"
    elif "felipe weiss" in text:
        ret = "caga pau"
    elif "sei la" in text:
        ret = "treze"
    elif "porra" in text or "caralho" in text:
        ret = "Ambiente Familiar"
    elif "bigod" in text and text[-1] == "?":
        ret = "sim"
    elif "gasp" in text and text[-1] == ".":
        ret = "cara é bom!"
    elif "cara" == text.split()[0]:
        carinhas = ["'-'", "'.'", "XD", "u.u", "@.@", ".-.", ":c"]
        ret = r.choice(carinhas)
    elif "bom dia" in text and text[-1] == "!":
        ret = "O sol nasceu na puta que pariu do horizonte, para iluminar a porra dos seus sonhos, bom dia filha da putaaa"
    elif "tchau" in text:
        ret = "Já vai tarde..."
    elif "melhor da vida" in text:
        quotes = [
            "pao de alho",
            "acordar cedo e lembrar que é sábado",
            "mijar apertado",
            "borda recheada de brinde",
            "quando chega o que vc comprou pela internet",
            "frete grátis",
            "achar dinheiro no bolso",
            "wifi grátis",
            "final da nacional",
        ]
        ret = r.choice(quotes)
    return ret


def roll(text):
    text = text.split()
    if len(text) > 1:
        times, limit = map(int, text[1:])
        if times < 100:
            res = "Rolando!\n\n"
            for dice in range(1, times + 1):
                res += str(r.randint(1, limit)) + "\n"
        else:
            res = "Vsf! Porrada de dado"
    else:
        res = str(r.randint(1, 6)) + "\n"
    return res


def primo(text):
    def isPrime(n):
        if n < 2:
            return False
        for number in islice(count(2), int(sqrt(n) - 1)):
            if n % number == 0:
                return False
        return True

    def co_prime(a, b):
        return gcd(a, b) == 1

    numbers = list(map(int, text.split()[1:]))
    if len(numbers) == 1:
        if numbers[0] > 10:
            text = "Sim" if isPrime(numbers[0]) else "Não"
        else:
            return "Ta de sacanagem né?"
    elif len(numbers) == 2:
        text = ""
        for n in numbers:
            if isPrime(n):
                text += str(n) + " é primo\n"
            else:
                text += str(n) + " não é primo\n"
        if co_prime(numbers[0], numbers[1]):
            text += "São coprimos"
        else:
            text += "Não são coprimos"
    else:
        text = "Mano, para de querer zoar"
    return text


def calculadora(text):
    def check_type(n):
        if int(n) == float(n):
            return int(n)
        else:
            return float(n)

    msg = text.split()[1:]
    try:
        number1 = float(msg[0])
        number2 = float(msg[2])
        operation = msg[1]

        text = ''
        if operation == '+':
            text = number1 + number2
        elif operation == '-':
            text = number1 - number2
        elif operation == '*':
            text = number1 * number2
        elif operation == '/':
            if number2 == 0:
                text = "Você quebrou as regras!"
            else:
                text = number1 / number2
        elif operation == '^':
            text = int(number1) ^ int(number2)
        elif operation == '**':
            text = number1 ** number2
        elif operation == '%':
            text = number1 % number2
        elif operation == 'log':
            text = log(number2, number1)
        elif operation == 'gcd':
            number1 = int(number1)
            number2 = int(number2)
            text = gcd(number1, number2)
    except Exception as e:
        print(e)
        text = 'hummm, n entendi'

    text = str(text)
    if text.isnumeric():
        text = str(check_type(text))

    return text


def fatorar(text):
    def verify_integer(x):
        try:
            int(x)
            return True
        except ValueError:
            return False

    def factorization(x):
        ans = ''
        aux = 3
        while x > 1:
            if not x % 2:
                ans += '2 '
                x = x // 2
                continue
            else:
                flag = False
                for i in range(aux, int(x ** (1 / 2)) + 1, 2):
                    if not x % i:
                        ans += str(i) + ' '
                        x = x // i
                        aux = i
                        flag = True
                        break
                if not flag:
                    ans += str(x) + ' '
                    break
        ans = ans[:len(ans) - 1]
        return ans

    numbers = text.split()[1:]
    if 10 >= len(numbers) > 0:
        text = ''
        for number in numbers:
            if not verify_integer(number):
                text += number + ' é estranho, me parece arriscado fatorar\n'

            else:
                number = int(number)
                if number < 1:
                    text += str(number) + ' é estranho, me parece arriscado fatorar\n'
                elif number == 1:
                    text += '1: 1\n'
                elif number > 2 ** 50:
                    text += str(number) + ' é muito grande pra mim\n'
                else:
                    text += str(number) + ': ' + factorization(number) + '\n'
        return text
    else:
        return 'Não exagera também'

import requests
import random
from bs4 import BeautifulSoup
import colorama
from colorama import Fore as col
import os
import multiprocessing
import sys


def parse():
    symbol_list = list('abcdefghiklmnopqrstvxyz123456789')

    session = requests.Session()
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    })

    while True:
        token = ''
        for i in range(0, random.randint(3,8)):
            token += random.choice(symbol_list)

        resp = session.get('https://prnt.sc/{}'.format(token))
        
        parsher = BeautifulSoup(resp.text, "html.parser")

        image_url = parsher.find('meta', attrs= {'property': 'og:image'})

        if not image_url:
            print(f'{col.RED}[+] Cloudflare block')
            continue     

        image_url = image_url['content']

        if 'http' not in image_url:
            print(f'{col.RED}[+] {col.LIGHTGREEN_EX}Nothing found by token {col.BLUE}{token}')
            continue 
        
        print(f'{col.YELLOW}[+] {col.LIGHTGREEN_EX}Image found for token {col.BLUE}{token}{col.LIGHTGREEN_EX}. Download...')

        img = session.get(image_url)
        with open(os.path.join('output', token + image_url[-4:]), 'wb') as file:
            file.write(img.content)
        
def main():
    banner =  '''
    ___       __    __       __          __                                       
   / (_)___ _/ /_  / /______/ /_  ____  / /_      ____  ____ ______________  _____
  / / / __ `/ __ \/ __/ ___/ __ \/ __ \/ __/_____/ __ \/ __ `/ ___/ ___/ _ \/ ___/
 / / / /_/ / / / / /_(__  ) / / / /_/ / /_/_____/ /_/ / /_/ / /  (__  )  __/ /    
/_/_/\__, /_/ /_/\__/____/_/ /_/\____/\__/     / .___/\__,_/_/  /____/\___/_/     
    /____/                                    /_/                                 

        {}https://github.com/deFiss/lightshot-parser
    '''.format(col.LIGHTBLUE_EX)

    print(col.CYAN+banner)
    try:
        os.mkdir('output')
    except FileExistsError:
        pass
    
    colorama.init()

    if len(sys.argv) == 2:
        proc_count = sys.argv[1]
    else:
        proc_count = input(f'{col.MAGENTA}[+] {col.YELLOW}Enter the number of processes: {col.LIGHTGREEN_EX}')
        
    process_list = []

    for i in range(0, int(proc_count)):
        proc = multiprocessing.Process(target=parse)
        process_list.append(proc)
        proc.start()
        print(f'{col.YELLOW}[+] {col.LIGHTGREEN_EX}Process {col.BLUE}{i+1} {col.LIGHTGREEN_EX}start')

if __name__ == "__main__":
    main()
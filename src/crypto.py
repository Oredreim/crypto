#!usr/bin/python3

from ast import Store, parse
from doctest import REPORT_CDIFF
from heapq import merge
from itertools import count
from sqlite3 import TimestampFromTicks
from sre_parse import Verbose
from urllib import request, response
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import signal
import sys
import time
import argparse
import tweepy
import csv
from pwn import *


def def_handler(sig, frame):
    print("\n [!] Saliendo... \n")
    time.sleep(2)
    sys.exit(1)

#Ctrl+C 
signal.signal(signal.SIGINT, def_handler)

# cadenas de autenticacion twitter
consumer_key = " "
consumer_secret = " "
access_token = " "
access_token_secret = " "

bearer_token = " "


diccionario_m = {"rate", "down", "low", "not", "stop", "dont", "inflation", "economic difficulties", "have to sell", "you must sell"}
diccionario_b = {"good", "up", "nice", "buy", "purchase", "you must buy", "have to buy", "use", "support"}
# autenticacion twitter
client = tweepy.Client(bearer_token=bearer_token)

#Variables Globales
url_bloques= "https://www.blockchain.com/es/btc/blocks"
result_bloques = requests.get(url_bloques )

url_charts="https://crypto.com/price"
result_charts = requests.get(url_charts )

url_untransactions="https://www.blockchain.com/btc/unconfirmed-transactions"
result_untransactions = requests.get(url_untransactions )

url_btc="https://crypto.com/price/bitcoin"
result_btc = requests.get(url_btc)

url_ethereum = "https://crypto.com/price/ethereum"
result_ethereum = requests.get(url_ethereum)

url_wrapped_bitcoin = "https://crypto.com/price/wrapped-bitcoin"
result_wrapped_bitcoin = requests.get(url_wrapped_bitcoin)

url_bnb = "https://crypto.com/price/bnb"
result_bnb = requests.get(url_bnb)

url_bitcoin_cash = "https://crypto.com/price/bitcoin-cash"
result_bitcoin_cash = requests.get(url_bitcoin_cash)

url_monero = "https://crypto.com/price/monero"
result_monero = requests.get(url_monero)

url_aave = "https://crypto.com/price/aave"
result_aave = requests.get(url_aave)

# lista los bloques de los ultimas compras y transferencias
def bloques():

    p1 = log.progress("Bloques")
    p1.status("Iniciando a buscar informacion sobre Hashes y Bloques")
    time.sleep(5)
    soup = BeautifulSoup(result_bloques.text, "html.parser")

    #soup de la altura
    article = soup.find_all('div' , class_='sc-1g6z4xm-0 hXyplo')[0:50]
    alturas = []
    count = 0
    for i in article:
        if count < 50:
            alturas.append(i.a.text)
        else:
            break
        count += 1
    
    # soup del hash
    article = soup.find_all('a', class_= 'sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk')
    ayuda = []
    for link in article:
        ayuda.append(link.get('href'))
    hashes = []
    for i in range(0,len(ayuda),3):
        hashes.append(ayuda[i])

    # soup del tiempos y tamanos
    article = soup.find_all('span', class_= 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
    ayuda = []
    for i in article:
        ayuda.append(i.text)
    
    # lista de tiempos
    tiempos = []
    for i in range(0,len(ayuda),2):
        tiempos.append(ayuda[i])

    # soup de tamanos
    tamanos = []
    for i in range(1,len(ayuda),2):
        tamanos.append(ayuda[i])

    p1.success("Busqueda terminada")
    tabla = pd.DataFrame({
        'alturas':alturas,
        'tamanos':tamanos,
        'tiempos':tiempos,
        'hashes':hashes
            }, index= list(range(0,50)))


    print ('Bloques principales con sus hashes')
    print (tabla)

def untransactions():
    p1 = log.progress("Transacciones")
    p1.status("Iniciando a buscar informacion sobre Transacciones")
    time.sleep(5)
    soup = BeautifulSoup(result_untransactions.text, "html.parser")
    article = soup.find_all('a' , class_='sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK')
    hashes = []
    count = 0
    for i in article:
        if count < 50:
            hashes.append(i.text)
        else:
            break
        count += 1
    article = soup.find_all('span', class_= 'sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
    ayuda = []
    for i in article:
        ayuda.append(i.text)
     # soup del tiempo
    tiempos = []
    for i in range(0,len(ayuda),3):
        tiempos.append(ayuda[i])


    amounts_btc = []
    for i in range(1,len(ayuda),3):
        amounts_btc.append(ayuda[i])
    
    amounts_usd = []
    for i in range(2,len(ayuda),3):
        amounts_usd.append(ayuda[i])


    p1.success("busqueda terminada")
    tabla = pd.DataFrame({
        'hashes':hashes,
        'tiempos':tiempos,
        'costo BTC':amounts_btc,
        'costo USD':amounts_usd
            }, index= list(range(0,50)))
    print(tabla)

def prices():
    p1 = log.progress("Precios")
    p1.status("Iniciando a buscar informacion sobre Los Costos de las crypto monedas")
    time.sleep(5)
    soup = BeautifulSoup(result_charts.content, "html.parser")
    # nombres
    article = soup.find_all('span', class_='chakra-text css-1mrk1dy')
    nombres = []
    for i in article:
        nombres.append(i.text)
    
    # precios
    ayuda = soup.find_all('div', class_='css-b1ilzc')
    precios = []
    for i in ayuda:
        precios.append(i.text)

    # cambios
    ayuda = soup.find_all('td' , class_='css-1b7j986')
    ayuda2 = []
    cambios = []
    for i in ayuda:
        ayuda2.append(i.text)
    for ele  in ayuda2:
        if ele.strip():
            cambios.append(ele)    

    p1.success("busqueda terminada")
    tabla = pd.DataFrame({
       'nombres':nombres,
       'precios':precios,
       'cambios':cambios,
           })
    print(tabla)

def btc():
    p1 = log.progress("BTC")
    p1.status("Iniciando a buscar informacion sobre BTC")
    time.sleep(5)
    query = "Bitcoin OR bitcoin OR BTC OR btc -is:retweet"
    response = client.search_recent_tweets(query=query, max_results=100, tweet_fields=['created_at', 'lang'], expansions=['author_id'])
    users = {u['id']: u for u in response.includes['users']}
    count_b = 0
    count_m = 0
    count = 1
    for tweet in response.data:
        p1.status("buscando el %s tweet" % (count))
        count += 1
        for palabra in diccionario_m:
            if palabra in tweet.text:
                count_m += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)
                    
        for palabra in diccionario_b:
            if palabra in tweet.text:
                count_b += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)

    p1.success("Tweets Terminados")
    
    if count_b <= count_m:
        print("\n \n[+] Analizando los ultimos tweets de las ultimas 24h, en este momento seria mejor no comprar Bitcoins")
    else:
        print("\n \n[+] Es tu momento, el dia de hoy seria buena opcion para comprar Bitcoins")
    soup = BeautifulSoup(result_btc.text, "html.parser")
    article = soup.find('span', class_ = 'chakra-text css-13hqrwd')
    print("\n[+] El precio del Bitcoin esta a: ", article.text)
    os.system("echo 3%s > btc" % (article.text))
            #print(tweet.text)
            #print(user.username)\
    


def ethereum():
    p1 = log.progress("Ethereum")
    p1.status("Iniciando a buscar informacion sobre Ethereum")
    time.sleep(5)
    query = "ethereum OR Ethereum OR ETHEREUM -is:retweet"
    response = client.search_recent_tweets(query=query, max_results=100, tweet_fields=['created_at', 'lang'], expansions=['author_id'])
    users = {u['id']: u for u in response.includes['users']}
    count_b = 0
    count_m = 0
    for tweet in response.data:
        for palabra in diccionario_m:
            if palabra in tweet.text:
                count_m += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)
                    
        for palabra in diccionario_b:
            if palabra in tweet.text:
                count_b += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)

    p1.success("Tweets Terminados")
    if count_b <= count_m:
        print("\n \n[+] Analizando los ultimos tweets de las ultimas 24h, en este momento seria mejor no comprar Ethereum")
    else:
        print("\n \n[+] Es tu momento, el dia de hoy seria buena opcion para comprar Ethereum")
    soup = BeautifulSoup(result_ethereum.text, "html.parser")
    article = soup.find('span', class_ = 'chakra-text css-13hqrwd')
    print("\n[+] El precio del Ethereum esta a: ", article.text)
    os.system("echo 2%s > ethereum" % (article.text))
            

def wrapped_bitcoin():
    p1 = log.progress("wrapped bitcoin")
    p1.status("Iniciando a buscar informacion sobre Wrapped Bitcoins")
    time.sleep(5)
    query = "wrapperbitcoin OR WrapperBitcoin OR WrapperBTC -is:retweet"
    response = client.search_recent_tweets(query=query, max_results=100, tweet_fields=['created_at', 'lang'], expansions=['author_id'])
    users = {u['id']: u for u in response.includes['users']}
    count_b = 0
    count_m = 0
    for tweet in response.data:
        for palabra in diccionario_m:
            if palabra in tweet.text:
                count_m += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)
                    
        for palabra in diccionario_b:
            if palabra in tweet.text:
                count_b += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)
    os.system("echo 3%s > wrapped" % (article.text))

    p1.success("Tweets Terminados")
    if count_b <= count_m:
        print("\n \n[+] Analizando los ultimos tweets de las ultimas 24h, en este momento seria mejor no comprar wrapped bitcoins")
    else:
        print("\n \n[+] Es tu momento, el dia de hoy seria buena opcion para comprar wrapped bitcoins")
    soup = BeautifulSoup(result_wrapped_bitcoin.text, "html.parser")
    article = soup.find('span', class_ = 'chakra-text css-13hqrwd')
    print("\n[+] El precio del Wrapped Bitcoin esta a: ", article.text)

def bnb():
    p1 = log.progress("BNB")
    p1.status("Iniciando a buscar informacion sobre Binance coins")
    time.sleep(5)
    query = "bnb OR BNB OR BNBcrypto OR bnbcrypto -is:retweet"
    response = client.search_recent_tweets(query=query, max_results=100, tweet_fields=['created_at', 'lang'], expansions=['author_id'])
    users = {u['id']: u for u in response.includes['users']}
    count_b = 0
    count_m = 0
    for tweet in response.data:
        for palabra in diccionario_m:
            if palabra in tweet.text:
                count_m += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)
                    
        for palabra in diccionario_b:
            if palabra in tweet.text:
                count_b += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)

    p1.success("Tweets Terminados")
    if count_b <= count_m:
        print("\n \n[+] Analizando los ultimos tweets de las ultimas 24h, en este momento seria mejor no comprar BNB")
    else:
        print("\n \n[+] Es tu momento, el dia de hoy seria buena opcion para comprar BNB")

    soup = BeautifulSoup(result_bnb.text, "html.parser")
    article = soup.find('span', class_ = 'chakra-text css-13hqrwd')
    print("\n[+] El precio del BNB esta a: ", article.text)
    os.system("echo 3%s > bnb" % (article.text))

def bitcoin_cash():
    p1 = log.progress("Bitcoin Cash")
    p1.status("Iniciando a buscar informacion sobre Bitcoin Cash")
    time.sleep(5)
    query = "bitcoincash OR BITCOINCASH OR BitcoinCash -is:retweet"
    response = client.search_recent_tweets(query=query, max_results=100, tweet_fields=['created_at', 'lang'], expansions=['author_id'])
    users = {u['id']: u for u in response.includes['users']}
    count_b = 0
    count_m = 0
    for tweet in response.data:
        for palabra in diccionario_m:
            if palabra in tweet.text:
                count_m += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)
                    
        for palabra in diccionario_b:
            if palabra in tweet.text:
                count_b += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)

    p1.success("Tweets Terminados")
    if count_b <= count_m:
        print("\n \n[+] Analizando los ultimos tweets de las ultimas 24h, en este momento seria mejor no comprar bitcoin cash")
    else:
        print("\n \n[+] Es tu momento, el dia de hoy seria buena opcion para comprar bitcoin cash")
    soup = BeautifulSoup(result_bitcoin_cash.text, "html.parser")
    article = soup.find('span', class_ = 'chakra-text css-13hqrwd')
    print("\n[+] El precio del Bitcoin Cash esta a: ", article.text)
    os.system("echo 3%s > bash" % (article.text))

def monero():
    p1 = log.progress("Monero")
    p1.status("Iniciando a buscar informacion sobre Monero")
    time.sleep(5)
    query = "monero OR monerocrypto OR MONEROCRYPTO OR moneroCRYPTO -is:retweet"
    response = client.search_recent_tweets(query=query, max_results=100, tweet_fields=['created_at', 'lang'], expansions=['author_id'])
    users = {u['id']: u for u in response.includes['users']}
    count_b = 0
    count_m = 0
    for tweet in response.data:
        for palabra in diccionario_m:
            if palabra in tweet.text:
                count_m += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)
                    
        for palabra in diccionario_b:
            if palabra in tweet.text:
                count_b += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)

    p1.success("Tweets Terminados")
    if count_b <= count_m:
        print("\n \n[+] Analizando los ultimos tweets de las ultimas 24h, en este momento seria mejor no comprar MONERO")
    else:
        print("\n \n[+] Es tu momento, el dia de hoy seria buena opcion para comprar MONERO")
    soup = BeautifulSoup(result_monero.text, "html.parser")
    article = soup.find('span', class_ = 'chakra-text css-13hqrwd')
    print("\n[+] El precio del Monero esta a: ", article.text)
    os.system("echo 3%s > monero" % (article.text))

def aave():
    p1 = log.progress("Aave")
    p1.status("Iniciando a buscar informacion sobre Aave")
    time.sleep(5)
    query = "Aave OR aavecrypto OR aave OR AaveCrypto OR aavecrypto OR AAVECRYPTO OR aaveCRYPTO -is:retweet"
    response = client.search_recent_tweets(query=query, max_results=100, tweet_fields=['created_at', 'lang'], expansions=['author_id'])
    users = {u['id']: u for u in response.includes['users']}
    count_b = 0
    count_m = 0
    for tweet in response.data:
        for palabra in diccionario_m:
            if palabra in tweet.text:
                count_m += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)
                    
        for palabra in diccionario_b:
            if palabra in tweet.text:
                count_b += 1
                if users[tweet.author_id]:
                    user = users[tweet.author_id]
                    print(tweet.text)
                    print(user.username)

    p1.success("Tweets Terminados")
    if count_b <= count_m:
        print("\n \n[+] Analizando los ultimos tweets de las ultimas 24h, en este momento seria mejor no comprar Aave")
    else:
        print("\n \n[+] Es tu momento, el dia de hoy seria buena opcion para comprar Aave")
    soup = BeautifulSoup(result_aave.text, "html.parser")
    article = soup.find('span', class_ = 'chakra-text css-13hqrwd')
    print("\n[+] El precio del Aave esta a: ", article.text)
    ayuda = article.text
    os.system("echo 1%s > aave" % (ayuda))

def usuario_moneda(moneda, usuario):
    p1 = log.progress("Buscando Palabras claves")
    p1.status("Iniciando a buscar informacion sobre " + moneda + " y " + usuario)
    time.sleep(5)
    query = moneda + " " + usuario + " -is:retweet"
    print(query)
    response = client.search_recent_tweets(query=query, max_results=20, tweet_fields=['created_at', 'lang'], expansions=['author_id'])
    users = {u['id']: u for u in response.includes['users']}
    for tweet in response.data:
        if users[tweet.author_id]:
            user = users[tweet.author_id]
            print(tweet.text)
            print(user.username)

def comparar(comparar):
    if comparar == 'btc':
        os.system("cat btc")
    if comparar == 'ethereum':
        os.system("cat ethereum")
    if comparar == 'wrapped':
        os.system("cat wrapped")
    if comparar == 'cash':
        os.system("cat cash")
    if comparar == 'bnb':
        os.system("cat bnb")
    if comparar == 'monero':
        os.system("cat monero")
    if comparar == 'aave':
        os.system("cat aave")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--blocks', dest='bloques', default=False, action='store_true', help="Listar los bloques")
    parser.add_argument('-p', '--prices', dest='prices', default=False, action='store_true', help="Listar los charts")
    parser.add_argument('-un', '--untransactions', dest='untransactions', default=False, action='store_true', help="Listar las transacciones aun no aprobadas")
    parser.add_argument('-btc', '--bitcoin', dest='btc', default=False, action='store_true', help="Informacion de Bitcoin")
    parser.add_argument('-eth', '--ethereum', dest='ethereum', default=False, action='store_true', help="Informacion de Ethereum")
    parser.add_argument('-wbtc', '--wrapped', dest='wrapped_ethereum', default=False, action='store_true', help="Informacion de Wrapped Bitcoin")
    parser.add_argument('-bnb', '--bnb', dest='bnb', default=False, action='store_true', help="Informacion de BNB")
    parser.add_argument('-btcc', '--bitcoincash', dest='bitcoincash', default=False, action='store_true', help="Informacion de Bitcoin Cash")
    parser.add_argument('-mon', '--monero', dest='monero', default=False, action='store_true', help="Informacion de Monero")
    parser.add_argument('-aav', '--aave', dest='aave', default=False, action='store_true', help="Informacion de Aave")
    parser.add_argument('-m','--moneda', dest='moneda', help="Buscar tweets de la MONEDA ingresada")
    parser.add_argument('-us','--usuario', dest='usuario', help="Buscar tweets del USUARIO ingresado")
    parser.add_argument('-com','--comparar', dest='comparar', help="Compara el valor de la divisa con su ultimo valor encontrado")
    
    if len(sys.argv) ==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    if args.bloques:
        bloques()
    elif args.prices:
        prices()
    elif args.untransactions:
        untransactions()
    elif args.btc:
        btc()
    elif args.ethereum:
        ethereum()
    elif args.wrapped_ethereum:
        wrapped_bitcoin()
    elif args.bnb:
        bnb()
    elif args.bitcoincash:
        bitcoin_cash()
    elif args.monero:
        monero()
    elif args.aave:
        aave()
    elif args.moneda and args.usuario:
        usuario_moneda(args.moneda, args.usuario)
    elif args.comparar:
        comparar(comparar)




    



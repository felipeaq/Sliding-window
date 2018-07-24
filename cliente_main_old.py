from cliente import *
from unicodedata import normalize

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def main():

    msg = remover_acentos(input())

    cli = ClienteUDP("127.0.0.1",5000,frame_tam=50)
    while True:
        cli.enviar (msg)
        msg = remover_acentos(input())

main()

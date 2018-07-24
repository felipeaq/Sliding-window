from cliente import *
from unicodedata import normalize
import time

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def main():
    f=open("1000k","r")
    msg =f.read()
    taxa_tempo=[]
    f.close()
    cli = ClienteUDP("127.0.0.1",5000,frame_tam=50)

    for i in range (100,1000,10):
        inicio =time.time()
        #msg=input()
        cli.frame_tam=i
        print (i)
        cli.enviar(msg)
        taxa_tempo.append((i,time.time()-inicio))
        time.sleep(0.5)

    f=open("taxa.csv","w")
    f.write("frame_tam,tempo\n")
    for i in taxa_tempo:
        f.write("{}, {}\n".format(i[0],i[1]))



main()

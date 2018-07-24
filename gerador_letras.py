import random
import string


def gera_arquivo(N,nome):
    f=open(nome,'w')
    for i in range(N):
        f.write(random.choice(string.ascii_letters))


if __name__=="__main__":
    gera_arquivo(10240,"10k")
    gera_arquivo(102400,"100k")
    gera_arquivo(1024000,"1000k")

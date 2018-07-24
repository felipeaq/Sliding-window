import socket
import hashlib
import time
import struct

class Servidor:
    def __init__(self,PORT,errar=0,tempo_max=5,max_erro=4):

        HOST = ''              # Endereco IP do Servidor
        self.PORT = PORT            # Porta que o Servidor esta
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #classe de comunicação como udp
        self.orig = (HOST, PORT) #guarda origem dos pacotes
        self.udp.bind(self.orig)
        self.hash_size=16 #tamanho da hash a ser utilizada
        self.tempo_max=tempo_max
        self.max_erro=max_erro
        self.erros=0

        self.errar=errar #probabilidade de gerar erro

    def receber(self):
        #chamda da função mais externa
        msg, cliente = self.__recebendo()
        checksum, mensagem=self.__decod(msg)
        if(self.__tratar_flag(not self.__validar(checksum, mensagem),cliente)):
            return cliente, mensagem
            self.erros=0
        else:
            if self.erros==self.max_erro:
                self.erros=0
                return False
            else:
                print(self.erros)
                self.erros+=1
                return self.receber()




    def __recebendo(self):
        #entra no estado recebendo
        if self.erros==0:
            self.udp.settimeout(None)

        msg,cliente=self.udp.recvfrom(1024)

        fmt="I I {}s".format(len(msg)-8)
        pac_anterior, tam, mensagem=struct.unpack(fmt,msg)
        x=1
        self.udp.settimeout(self.tempo_max)
        while(x<tam):
            try:
                msg,cliente=self.udp.recvfrom(1024)
            except :
                print("demorou")
                #manda qualquer coisa que resulte em erro
                return (("invalidoaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaainvalido".encode()),cliente)

            x+=1

            fmt="I {}s".format(len(msg)-4)


            pacote, m =struct.unpack(fmt, msg)
            print("recebendo mensagem {}...".format(pacote))
            mensagem+=m






        return mensagem,cliente





    def fechar(self):
        self.udp.close()
    def __decod(self,msg):
        #separa checksum da mensagem
        checksum=msg[-16:]

        mensagem=msg[:-16]
        return checksum, mensagem

    def __validar(self,checksum,mensagem):
        #valida se a mensagem esta de acordo com o checksum
        h = hashlib.new('md5')
        h.update(mensagem)


        return checksum==h.digest()

    def __tratar_flag(self,erro,cliente):
        #da o alerta caso haja erro
        if erro:
            self.udp.sendto ("irineu".encode(), cliente)
            print ("falha ao receber")

        else:
            self.udp.sendto ("UUUU".encode(), cliente)
            print ("sucesso ao receber")
        return not erro

if __name__=="__main__":
    serv= Servidor (5000)
    while True:
        if serv.receber():
            print ("recebeu")
        else:
            print("nao recebeu")



    serv.fechar()

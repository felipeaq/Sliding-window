import socket
import struct
import hashlib
import random
import time
import math


class ClienteUDP:
    def __init__(self,HOST,PORT,max_tentativas=5,tempo_max=5,frame_tam=1024,delay=True):

        #gera erro, caso tenha um tamanho inválido
        if frame_tam<20:
            raise ValueError('tamanho minimo do frame deve ser 20')
        if frame_tam>1000:
            raise ValueError('tamanho maximo do frame deve ser 1400')

        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.delay=delay #controla o erro no local host (placa de rede n aguenta o tempo do processador)
        self.dest = (HOST, PORT)
        self.erro=0
        self.udp.settimeout(tempo_max)
        self.max_tentativas=max_tentativas
        self.frame_tam=frame_tam
        self.pacote=0

    def __recorta(self,item):
        #faz os frames
        return [item[ind:ind+self.frame_tam] for ind in range(0, len(item), self.frame_tam)]

    def enviar(self,mensagem):
        #metodo mais alto nivel, para quem usar a classe
        self.pacote=0
        mensagens=self.__empacotar_inicio(mensagem)
        frames=self.__recorta(mensagens)

        for msg in frames:
            self.__envia_mensagem(msg)
            if self.delay:
                #garante que o erro seja controlado
                time.sleep(0.0002)
            self.pacote+=1

        try:
            msg, servidor = self.udp.recvfrom(1024)
        except socket.timeout:
            print("demorou")
            self.erro+=1
            if self.erro==self.max_tentativas:
                self.erro=0
                print("erro!")
                return False

            return self.enviar(mensagem)
        print (msg)
        if msg=="UUUU".encode():
            print ("sucesso ao enviar!")
            self.erro=0
            return True

        else:
            self.erro+=1

            if self.erro==self.max_tentativas:
                self.erro=0
                print("erro!")
                return False


            return self.enviar(mensagem)
    def __envia_mensagem(self,mensagem):
        #envia cada frame
        tam=len(mensagem)
        enviar=self.empacotar(mensagem)
        print("enviando pacote {}...".format(self.pacote))
        self.udp.sendto (enviar, self.dest)


    def encerrar():
        self.udp.close()

    def __empacotar_inicio(self,mensagem):
        #empacota o primeiro frame, pois o primeiro tem o total de frames
        info=mensagem.encode()
        h = hashlib.new('md5')
        h.update(info)
        mensagem_formato="I {}s {}s".format(len(mensagem),len(h.digest()))
        total_frames= math.ceil((4+len(mensagem)+16)/self.frame_tam)

        return struct.pack(mensagem_formato,total_frames,info,h.digest())

    def empacotar(self,mensagem):

        mensagem_tam="I {}s".format(len(mensagem))
        return struct.pack(mensagem_tam,self.pacote, mensagem)

# -- coding: utf-8 --
"""Openlab.ipynb
"""
#Instalando bibliotecas
#pip install paho-mqtt

#Lucas Feng/Patrick Marques 

import paho.mqtt.client as mqtt
import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
import os

#import sys
#sys.path.append("/scrapy")
#import scrapy as i
# Pegando dado da variavel do arquivo do Robô do site
#resposta = i.pegatexto
# Pegando dado do modo de jogo do arquivo do Robô do site
#modoJogo = i.mode_element
# Pegando valor do contador
#cont = i.cont


user = "grupo1-bancadaB4"
passwd = "L@Bdygy1B4"

Broker = "labdigi.wiseful.com.br"   # Endereco do broker
Port = 80                           # Porta utilizada (firewall da USP exige 80)
KeepAlive = 60                      # Intervalo de timeout (60s)

E = []
S = []

for i in range(7):
    E.append(user+"/E"+str(i))
    S.append(user+"/S"+str(i))

# Quando conectar na rede (Callback de conexao)
def on_connect(client, userdata, flags, rc):

    for topicE in E:
        client.subscribe(topicE, qos=0)
    
    for topicS in S:
        client.subscribe(topicS, qos=0)
    
# Quando receber uma mensagem (Callback de mensagem)
def on_message(client, userdata, msg):
    global dados_pollock_payload
    global occurrence_time
    
    client.newmsg = True    
    client.topic = msg.topic
    client.msg = msg.payload.decode("utf-8")
    
    #if client.msg == "1" and client.topic == user+"/S2":
               



client = mqtt.Client()                      # Criacao do cliente MQTT
client.on_connect = on_connect              # Vinculo do Callback de conexao
client.on_message = on_message              # Vinculo do Callback de mensagem recebida
client.username_pw_set(user, passwd)        # Apenas para coneccao com login/senha
client.connect(Broker, Port, KeepAlive)     # Conexao do cliente ao broker


"""client.loop_start()
time.sleep(1)
client.publish(user+"/led", "1")
time.sleep(1)
client.publish(user+"/led", "0")"""



driver = webdriver.Chrome("C:/chromedriver.exe")

driver.get('https://sorteia-quiz.vercel.app/')

mode = '#root > div > div.sc-bdvvtL.lkYwdo > div.sc-hKwDye.fNiswD > div > div.sc-eCImPb.kKCenc > div > span'
dificuldade = '#root > div > div.sc-bdvvtL.lkYwdo > div.sc-hKwDye.fNiswD > div > div.handleDifficulty > span'
sortear = '#root > div > div.sc-bdvvtL.lkYwdo > div.sc-gsDKAQ.giCzBE > div > div.sc-dkPtRN.coZBdQ > button:nth-child(1)'
limpar = '#root > div > div.sc-bdvvtL.lkYwdo > div.sc-gsDKAQ.giCzBE > div > div.sc-dkPtRN.coZBdQ > button:nth-child(2)'
responde = '#alt'
salvar = '#root > div > div.sc-bdvvtL.lkYwdo > div.sc-gsDKAQ.giCzBE > div > button'
textoo = '#root > div > div.sc-bdvvtL.lkYwdo > div.sc-gsDKAQ.giCzBE > div > div.pega > span'

#identifica e retorna os elementos
sortear_element = driver.find_element_by_css_selector(sortear)
responde_element = driver.find_element_by_css_selector(responde)
salvar_element = driver.find_element_by_css_selector(salvar)
limpar_element = driver.find_element_by_css_selector(limpar)

"""
Acionando botao
    sortear_element.click()
    salvar_element.click()
"""
#instrucoes_element.click()


"""
Inserindo resposta
    responde_element.send_keys('(C)')
"""

#Tempo para jogador responder a Pergunta
#time.sleep(15)

verificaMode = 0

#loop para aguardar o Jogador escolher o modo de jogo
while verificaMode == 0:
    mode_element = driver.find_element_by_css_selector(mode).text
    if mode_element == 'showDoMilhao' or mode_element == 'highScore':
        print(f"********O modo de jogo escolhido foi {mode_element}********")
        verificaMode = 1


verificaDificuldade = 0

#Loop para aguardar o Jogador escolher a dificuldade
while  verificaDificuldade == 0:
    #Pegando nivel de dificuldade
    dificuldade_element = driver.find_element_by_css_selector(dificuldade).text
    #Verificando a resposta
    if dificuldade_element == 'Easy' or dificuldade_element == 'Medium' or dificuldade_element == 'Hard':
        print(f"********Dificuldade inserida foi: {dificuldade_element}********")
        verificaDificuldade = 1


cont = 0
if mode_element == 'highScore':
    while cont < 16:
        print(f"Cont está em {cont}")
        if dificuldade_element == 'Easy':
            #Iniciando o circuito Inicar no MQTT
            client.loop_start()
            print("Iniciando...")
            client.publish(user+"/E2", "1")
            time.sleep(0.5)
            limpar_element.click()
            time.sleep(0.5)
            sortear_element.click()
            time.sleep(2)
            # Pegando resposta da Pergunta
            pegatexto = driver.find_element_by_css_selector(textoo).text
            print(f"********Resposta inserida foi: {pegatexto}********")
            
            #Interagindo com o MQTT
            client.loop_start()
            #Inserindo modo de jogo
            print("Inserindo Modo de jogo")
            client.publish(user+"/E7", "1")
            time.sleep(0.5)
            
            # Realizando Validacao da resposta
            if pegatexto == '2':
                print("Acertou")
                client.loop_start()
                time.sleep(0.5)
                client.publish(user+"/E6", "1")
                time.sleep(1)
                #client.publish(user+"/E2", "0")
                #Setando resposta
                client.publish(user+"/E0", "1")
                time.sleep(1)
                client.publish(user+"/E6", "0")
                client.publish(user+"/E0", "0")
            else:
                print("Errou")
                client.loop_start()
                time.sleep(0.5)
                client.publish(user+"/E4", "1")
                time.sleep(0.5)
                #Setando resposta
                client.publish(user+"/E0", "1")
                time.sleep(1)
                client.publish(user+"/E4", "0")
                client.publish(user+"/E0", "0")

            if cont == 15:
                print("Aguardando tempo para dar RESET")
                client.loop_start()
                time.sleep(10)
                #desligando modo de jogo
                print("Desligando Modo de Jogo...")
                client.publish(user+"/E7", "0")
                time.sleep(0.5)
                #desligando inicar
                print("Desligando Iniciar...")
                client.publish(user+"/E2", "0")
                time.sleep(0.5)
                #ativando reset
                client.publish(user+"/E1", "1")
                client.publish(user+"/E1", "0")

            cont += 1

        elif dificuldade_element == 'Medium':
             #Iniciando o circuito Inicar no MQTT
            client.loop_start()
            print("Iniciando...")
            client.publish(user+"/E2", "1")
            time.sleep(0.5)
            limpar_element.click()
            time.sleep(0.5)
            sortear_element.click()
            time.sleep(2)
            # Pegando resposta da Pergunta
            pegatexto = driver.find_element_by_css_selector(textoo).text
            print(f"********Resposta inserida foi: {pegatexto}********")
            
            #Interagindo com o MQTT
            client.loop_start()
            #Inserindo modo de jogo
            print("Inserindo Modo de jogo")
            client.publish(user+"/E7", "1")
            time.sleep(0.5)
            
            # Realizando Validacao da resposta
            if pegatexto == '2':
                print("Acertou")
                client.loop_start()
                time.sleep(0.5)
                client.publish(user+"/E6", "1")
                time.sleep(1)
                #client.publish(user+"/E2", "0")
                #Setando resposta
                client.publish(user+"/E0", "1")
                time.sleep(1)
                client.publish(user+"/E6", "0")
                client.publish(user+"/E0", "0")
            else:
                print("Errou")
                client.loop_start()
                time.sleep(0.5)
                client.publish(user+"/E4", "1")
                time.sleep(0.5)
                #Setando resposta
                client.publish(user+"/E0", "1")
                time.sleep(1)
                client.publish(user+"/E4", "0")
                client.publish(user+"/E0", "0")

            if cont == 15:
                print("Aguardando tempo para dar RESET")
                client.loop_start()
                time.sleep(10)
                #desligando modo de jogo
                print("Desligando Modo de Jogo...")
                client.publish(user+"/E7", "0")
                time.sleep(0.5)
                #desligando inicar
                print("Desligando Iniciar...")
                client.publish(user+"/E2", "0")
                time.sleep(0.5)
                #ativando reset
                client.publish(user+"/E1", "1")
                client.publish(user+"/E1", "0")

            cont += 1

        elif dificuldade_element == 'Hard':
             #Iniciando o circuito Inicar no MQTT
            client.loop_start()
            print("Iniciando...")
            client.publish(user+"/E2", "1")
            time.sleep(0.5)
            limpar_element.click()
            time.sleep(0.5)
            sortear_element.click()
            time.sleep(2)
            # Pegando resposta da Pergunta
            pegatexto = driver.find_element_by_css_selector(textoo).text
            print(f"********Resposta inserida foi: {pegatexto}********")
            
            #Interagindo com o MQTT
            client.loop_start()
            #Inserindo modo de jogo
            print("Inserindo Modo de jogo")
            client.publish(user+"/E7", "1")
            time.sleep(0.5)
            
            # Realizando Validacao da resposta
            if pegatexto == '2':
                print("Acertou")
                client.loop_start()
                time.sleep(0.5)
                client.publish(user+"/E6", "1")
                time.sleep(1)
                #client.publish(user+"/E2", "0")
                #Setando resposta
                client.publish(user+"/E0", "1")
                time.sleep(1)
                client.publish(user+"/E6", "0")
                client.publish(user+"/E0", "0")
            else:
                print("Errou")
                client.loop_start()
                time.sleep(0.5)
                client.publish(user+"/E4", "1")
                time.sleep(0.5)
                #Setando resposta
                client.publish(user+"/E0", "1")
                time.sleep(1)
                client.publish(user+"/E4", "0")
                client.publish(user+"/E0", "0")

            if cont == 15:
                print("Aguardando tempo para dar RESET")
                client.loop_start()
                time.sleep(10)
                #desligando modo de jogo
                print("Desligando Modo de Jogo...")
                client.publish(user+"/E7", "0")
                time.sleep(0.5)
                #desligando inicar
                print("Desligando Iniciar...")
                client.publish(user+"/E2", "0")
                time.sleep(0.5)
                #ativando reset
                client.publish(user+"/E1", "1")
                client.publish(user+"/E1", "0")

            cont += 1
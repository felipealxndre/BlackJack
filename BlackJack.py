# Import
import json
import random
from os import system, name
# Função para limpar a tela a cada execução
def limpa_tela():
    # Windows
    if name == 'nt':
        _ = system('cls')
    # Mac ou Linux
    else:
        _ = system('clear')

import time
# Função para imprimir com atraso
def imprimir_com_atraso(*arg):
    for texto in arg:
        for caractere in texto:
            print(caractere, end='', flush=True)
            time.sleep(0.05)  # Ajuste o tempo de espera conforme necessário
        print()  # Adiciona uma quebra de linha no final

imprimir_com_atraso("Bem-vindo ao jogo de Blackjack!")
imprimir_com_atraso("Embaralhando as cartas...")
time.sleep(0.5)

# criando um baralho; um baralho é uma lista de tuplas
def novo_baralho():
    numeros = (2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A')
    naipes = ('Copas', 'Paus', 'Ouros', 'Espadas')
    baralho = []
    for naipe in naipes:
        for num in numeros:
            baralho.append((num, naipe))
    return baralho

# tira uma ou mais cartas do baralho
def puxa_carta(baralho):
    carta = random.choice(baralho)
    baralho.remove(carta)
    return carta

# printa a mão de forma organizada
def print_hand(mao):
    print('Sua mão é: ')
    for tup in mao:
        print("  ", f"{tup[0]} de {tup[1]}")

# calcula a soma máxima da mão(sem estourar por A's)
def soma_hand(mao):
    soma = 0
    nA = 0
    # calculando a soma e deixando para somar os A's depois
    for carta in mao:
        valor = carta[0]
        if valor in ['J', 'Q', 'K']:
            soma += 10
        elif valor == 'A':
            nA += 1
        else: soma += valor
    # agora verificando a maior soma com os A's
    while nA > 0:
        if soma + 11 + (nA - 1) <= 21:
            soma += 11
        else:
            soma += 1
        nA -= 1
    return soma

# printa a mão de forma organizada
def print_hand(mao):

    for tup in mao:
        print("  ", f"{tup[0]} de {tup[1]}")
    print('Soma:', soma_hand(mao), "\n")

limpa_tela()
print("\nBem-vindo(a) ao BlackJack!\n")

def verificar_resultado(mao, mao_dealer):

    soma_player = soma_hand(mao)
    soma_dealer = soma_hand(mao_dealer)
    
    if soma_player > soma_dealer:
        result = 'V'
        if len(mao) == 2 and soma_player == 21:
            print('Você ganhou! Você tinha o BlackJack!')
        else: print('Você ganhou!')
    elif soma_player == soma_dealer:
        result = 'E'
        print('Empate! Não perde nada.')
    elif soma_player < soma_dealer:
        result = 'P'
        if len(mao_dealer) == 2 and soma_dealer == 21:
            print('Você perdeu! O Dealer tinha o BlackJack!\n')
        elif soma_dealer > 21:
            print("Você ganhou! O Dealer estourou!")
            result = 'V'
        else: print('Perdeu! O Dealer ganhou.')

    return result


def inicializar_resultados():
    # Verificar se o arquivo já existe
    try:
        with open('resultados.txt', 'r') as arq:
            # Se o arquivo existe, retornar os resultados existentes
            resultados = json.load(arq)

    except FileNotFoundError:
        # Se o arquivo não existe, inicializar com valores padrão
        resultados = {'Vitórias': 0, 'Derrotas': 0, 'Empates': 0, 'Saldo': 1000}
        with open('resultados.txt', 'w') as arq:
            json.dump(resultados, arq)

    imprimir_com_atraso("\nSeus resultados são: \n")
    print(', '.join([f"{chave}: {valor}" for chave, valor in resultados.items()]))
    return resultados
    

jogar = '1'
while jogar == '1':
    limpa_tela()
    placar = inicializar_resultados()
    imprimir_com_atraso("\n\nVamos começar!\n\n")
    aposta = int(input('Selecione o quanto você quer apostar: \n'))
    result = ''
    Parar = False
    baralho = novo_baralho()
    hand = []
    hand_dealer = []
    # sortear as suas 2 cartas e as 2 do dealer
    for qtde in range(0,2):
        hand.append(puxa_carta(baralho))
        hand_dealer.append(puxa_carta(baralho))
    
    # mostrando a mão e soma máxima
    imprimir_com_atraso('Sua mão é: ')
    print_hand(hand)
    imprimir_com_atraso('\nPrimeira carta do Dealer = ', f"{hand_dealer[0][0]} de {hand_dealer[0][1]}")
    
    resp = input('\nDigite a sua ação:\n 0 - Dobrar aposta\n 1 - Puxar mais uma carta\n 2 - Parar\nResp: ')
    if resp == '0':
        aposta = aposta*2
        hand.append(puxa_carta(baralho))
        imprimir_com_atraso('\nSua mão é: ')
        print_hand(hand)

        if soma_hand(hand) > 21:
            imprimir_com_atraso('Perdeu! Estourou!\n')
            result = 'P'

    elif resp == '1':
        hand.append(puxa_carta(baralho))
        imprimir_com_atraso('\nSua mão é: ')
        print_hand(hand)

        while soma_hand(hand) <= 21 and Parar == False:
                resp = input('Digite a sua ação:\n 1 - Puxar mais uma carta\n 2 - Parar\nResp: ')
                if resp == '1':
                    hand.append(puxa_carta(baralho))
                    imprimir_com_atraso('\nSua mão é: ')
                    print_hand(hand)
                else: Parar = True

        if soma_hand(hand) > 21:
            imprimir_com_atraso('Perdeu! Estourou!\n')
            result = 'P'
            Parar = True

    elif resp == '2':
        Parar = True

    soma_player = soma_hand(hand)

    # Agora vem a parte do Dealer, se o jogador já não tiver perdido:
    if result != 'P':
        time.sleep(0.5)
        imprimir_com_atraso('\nCarta oculta do dealer: ', f"{hand_dealer[1][0]} de {hand_dealer[1][1]}")

        while soma_hand(hand_dealer) < 17 and soma_hand(hand_dealer) < soma_player:
            imprimir_com_atraso('\nDealer puxa mais uma...\n')
            carta = puxa_carta(baralho)
            hand_dealer.append(carta)
            imprimir_com_atraso('Dealer puxou: ', f"{carta[0]} de {carta[1]}")

        imprimir_com_atraso('\nMão do Dealer:')
        print_hand(hand_dealer)
        
        # agora verificando resultado, com a mão do dealer:
        result = verificar_resultado(hand, hand_dealer)

    # agora acerto de contas né
        
    
    if result == 'P':
        placar['Derrotas'] += 1
        placar['Saldo'] -= aposta
    elif result == 'V':
        placar['Vitórias'] += 1
        placar['Saldo'] += aposta
    elif result == 'E':
        placar['Empates'] += 1

    imprimir_com_atraso("Seus resultados finais são: ")
    print(', '.join([f"{chave}: {valor}" for chave, valor in placar.items()]))
    #escrever no arquivo agora 
    with open('resultados.txt', 'w') as arq:
            json.dump(placar, arq)
    # Jogar de novo?
    jogar = input('\nJogar de novo?\n 0 = Não\n 1 = Sim\n')






import random
import subprocess
from bit import PrivateKey, network
import time
import os
import re
import hashlib
import base58
import argparse
import shutil

def selecionar_range():
    public_key = '03633cbe3ec02b9401c5effa144c5b4d22f87940259634858fc7e59b1c09937852'
    start = int('200000000000000000000000000000000', 16)
    end = int('3ffffffffffffffffffffffffffffffff', 16)
    partes = 5_000_0000
    parte = int(input(f'\nDica: Você pode usar "_" para melhor visualização. Por exemplo: 11_111_111.\nDigite uma parte a ser procurada entre 1 e {partes}, ou 0 para uma parte aleatória: '))
    if parte == 0:
        parte = random.randint(1,partes)
        print(f'----------------------------\nAnote a parte gerada aleatória: {parte}\n----------------------------')
    range_total = end - start + 1
    fracao_range = range_total // partes

    inicio_selecionado = start + (parte - 1 ) * fracao_range
    fim_selecionado = inicio_selecionado + fracao_range - 1

    if parte  == partes:
        fim_selecionado = end

    with open('130.txt', 'w') as file:
        file.write(f"{hex(inicio_selecionado)[2:]}\n")
        file.write(f"{hex(fim_selecionado)[2:]}\n")
        file.write(f"{public_key}")

def iniciar_busca():
    path = './kangaroo'
    argumentos = '-gpu -g 80,128 -t 4 -o KFound.txt 130.txt'
    comando = f"{path} {argumentos}"
    print(comando)
    try: 
        print("Iniciando busca")
        subprocess.Popen(comando, shell=True)
    except Exception as e:
        print(f'Erro: {e}')

def transferir(wif, destino):
    if destino == '':
        print('\nEndereço não informado.\nNão será feito transferência.')
        return None
    if len(destino) <= 25: 
        print (f'Carteira informada {destino} está inválida, interrompendo transação.\n------\n------\n------\nWIF: {wif}')
        return None
    try: 
        key = PrivateKey(wif)
        saldo = key.get_balance('satoshi')
        print(f'Seu saldo é: {saldo} satoshis')

        num_inputs = len(key.get_unspents())
        num_outputs = 1

        tamanho_estimado = (num_inputs*148) + (num_outputs*34) + 10

        fee_por_byte = network.get_fee(fast=True)
        fee = tamanho_estimado * fee_por_byte
        valor_a_enviar = int(saldo) - fee

        if valor_a_enviar <= 0:
            print ("Saldo Insuficiente para cobrir a taxa.")
        else:
            try:
                transacao = key.send([(destino, valor_a_enviar, 'satoshi')], absolute_fee=True, fee=fee)
                if transacao:
                    print (f'Enviado com sucesso: {transacao}\nValor: {valor_a_enviar}')
            except Exception as e:
                print (f'Ocorreu um erro: {e}')
    except:
        print (f'Ocorreu um erro: {e}')

def verifica_saldo():
    endereco = '1Fo65aKq8s8iquMt6weF1rku1moWVEd5Ua'
    print('Verificando saldo da carteira 130, aguarde...')
    try:
        saldo = network.NetworkAPI.get_balance(endereco) / 1e8

        if saldo > 0:
            print(f"\n------------------------------ \nCarteira: {endereco}: \nSaldo: {saldo:.8f} BTC\n------------------------------")
            return

        else:
            if input("Carteira está sem saldo, o que indica que já foi encontrada, deseja continuar? (s/n): ") in ['sim','s','y','yes']:
                return
            else:
                print('Encerrando Bot')
                quit()
    except Exception as e:
        print(f"Houve um erro ao verificar o saldo: {e}")

def work_restore():
    save_path = f'/content/drive/MyDrive/save{parte}.work'
    if os.path.exists(save_path): # Verifica se ja existe um save
        shutil.copy(save_path, 'save.work') #Copia pro Kangaroo
        print(f"Work Save {parte} Recuperado.")
    else:
        print(f"Work Save {parte} Não Localizado.")

def work_save():
    save_path = f'/content/drive/MyDrive/save{parte}.work'
    global contador
    contador +=1
    save_local = 'save.work'
    try: 
        if contador == 5:
        #Se existir work e existir o save_path, copia pro drive a cada x minutos
            if os.path.exists(save_local):
                if drive_is_mounted:
                    shutil.copy(save_local, save_path)
                    print(f"Work {parte} Salvo no Drive")
                else:
                    print("Não foi possível salvar o work no seu drive, verifique se está montado corretamente.")
                contador = 0
    except Exception as e:
        print(f"Não foi possível salvar o work no seu drive, verifique se está montado corretamente.\n {e}")

def aguarda_quebra(): #Apos chamar o quebrar chave, fica procurando a key no arquivo KFound.txt na raiz a cada minuto
    kfound = 'KFound.txt'
    print('---------------------------------------------')
    time.sleep(70)
    while True:
        if os.path.exists(kfound):
            with open(kfound, "r") as file:
                content = file.read()
                match = re.search(r'Priv: (\w+)', content)
                if match:
                    try:
                        privkey = match.group(1)
                        wif = converter_wif(privkey)
                        print (f"CHAVE WIF = {wif}")
                        if drive_is_mounted:
                            with open ('/content/drive/MyDrive/WIF.TXT', 'w') as file:
                                file.write(f'WIF ENCONTRADA: {wif}\nCHAVE PRIVADA: {privkey}')
                        return wif
                    except Exception as e:
                        print (f'Erro ao retornar a chave: {e}')
        work_save()
        time.sleep(60)

def converter_wif(private_key_hex: str) -> str:
    try: 
        private_key_hex.lower()
        # Remove o prefixo 0x se ele estiver presente
        if private_key_hex.startswith('0x'):
            private_key_hex = private_key_hex[2:]

        private_key_hex = private_key_hex.zfill(64)

        # Adiciona o prefixo 0x80 para a mainnet
        prefix = b'\x80'
        private_key_bytes = bytes.fromhex(private_key_hex)
        # Adiciona o sufixo 0x01 para indicar que é uma chave comprimida
        compressed_suffix = b'\x01'
        extended_key = prefix + private_key_bytes + compressed_suffix
        
        # Realiza o SHA-256 duplo do extended_key
        first_sha256 = hashlib.sha256(extended_key).digest()
        second_sha256 = hashlib.sha256(first_sha256).digest()
        
        # Adiciona os 4 primeiros bytes do segundo SHA-256 ao final do extended_key
        checksum = second_sha256[:4]
        final_key = extended_key + checksum
        
        # Converte para base58
        wif_compressed = base58.b58encode(final_key)
        
        return wif_compressed.decode('utf-8')
    except Exception as e:
        print('Ocorreu um erro ao converter a chave privada para WIF: {e}')

def busca_completa_com_save():
    work_restore()
    path = './kangaroo'
    if os.path.exists('save.work'):
        argumentos = '-gpu -g 80,128 -t 4 -ws -w save.work -wi 60 -o KFound.txt -i save.work'
    else:
        argumentos = f'-gpu -g 80,128 -t 4 -ws -w save.work -wi 60 -o KFound.txt ranges/130-{parte}.txt'

    comando = f"{path} {argumentos}"
    print(comando)
    try: 
        print(f"Iniciando busca na parte {parte}/16")
        subprocess.Popen(comando, shell=True)
    except Exception as e:
        print(f'Erro: {e}')

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Bot para pesquisar a chave do puzzle 130\n"
            "Criado por Ataide Freitas\n"
            "https://github.com/ataidefcjr/colabkangaroo\n"
            "Doações: bc1qych3lyjyg3cse6tjw7m997ne83fyye4des99a9\n"
            "Exemplo de uso: !python main.py -m 2 -d bc1qych3lyjyg3cse6tjw7m997ne83fyye4des99a9"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )   
    partes = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
    parser.add_argument('-d', '--destination', type=str, required=False, help="Informe sua Carteira para transferir automaticamente se encontrada a chave privada.")
    parser.add_argument('-m', '--mode', type=str, choices=['1', '2'], required=False, help="Informe o modo (1 ou 2)")
    parser.add_argument('-p', '--parte', type=str, choices=partes, required=False, help="Selecione uma parte entre 1 e 16. (Obrigatório ao usar o modo 2)")

    args = parser.parse_args()

    global parte
    parte = args.parte
    my_wallet = args.destination
    selecionar = args.mode
    verifica_saldo()

    if not my_wallet:
        my_wallet = input('Se encontrar a chave o bot tentara realizar a transfernecia para a sua carteira\nCole o endereço da sua carteira: ')
    if not selecionar:
        selecionar = input('\n-------\n1 - Selecionar um número entre 1 e 50 milhoes.\n2 - Fazer a busca em todo o range da carteira 130 com save automático.\n-------Selecione uma opção: ')
    if selecionar == '1':
        selecionar_range()
        iniciar_busca()
    elif selecionar == '2':
        if not parte:
            parte = input('Insira um numero de 1 a 16: ')
        if parte not in partes:
            print('Parte inválida, encerrando.')
            quit()
        print(f'Parte selecionada: {parte}')
        busca_completa_com_save()
    else:
        print('Modo Inválido, encerrando.')
        quit()
    wif = aguarda_quebra()
    transferir(wif, my_wallet)

if __name__ == '__main__':
    drive_path = '/content/drive/MyDrive/'
    drive_is_mounted = os.path.exists(drive_path)
    parte = None
    contador = 0
    main()
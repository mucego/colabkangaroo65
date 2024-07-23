import random
import subprocess
from bit import PrivateKey, network
import time
import sys
import os
import re
import hashlib
import base58

privkey_path = '/content/drive/My Drive/Private Key - Puzzle 130.txt'

def selecionar_range():
    public_key = '03633cbe3ec02b9401c5effa144c5b4d22f87940259634858fc7e59b1c09937852'
    start = int('200000000000000000000000000000000', 16)
    end = int('3ffffffffffffffffffffffffffffffff', 16)
    partes = 50000000
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

def iniciar_busca(teste:bool):
    path = './kangaroo'
    argumentos = '-gpu -g 80,128 -t 1 -o KFound.txt 130.txt'
    if teste == True:
        argumentos = '-gpu -g 80,128 -t 1 65.txt'
    comando = f"{path} {argumentos}"
    print(comando)
    try: 
        print("Iniciando busca")
        subprocess.Popen(comando, shell=True)
    except Exception as e:
        print(f'Erro: {e}')

def transferir(wif, destino):
    try: 
        my_key = PrivateKey(wif)
        print('---------------------------------------------------\nEndereço da Carteira Capturada: ', my_key.address, '\n---------------------------------------------------')
        saldo = my_key.balance_as('satoshi')
        print('---------------------------------------------------\nSaldo da Carteira Capturada: ', saldo, 'satoshis', '\n---------------------------------------------------')
        if destino == 'Não Informado':
            print('\nTransferencia não informada, endereço não informado.\n')
            return None
        taxa = network.get_fee('fast') 
    except Exception as e:
        print(f'Erro ao verificar a carteira: {e}')
    print(f'Taxa de Transação Sugerida (satoshis por byte): {taxa}')
    taxa *= 2
    taxa = int(taxa) * 250
    print(f'---------- >> --------- >> Taxa a ser utilizada: ', taxa)
    valor = int(saldo)-taxa
    valor = int(valor)
    if valor < 0:
        print(f'\n-----------------\nSaldo nao possibilita transação: {saldo} satoshis\n ------------------')
        return None
    print(f'Valor a ser transferido: {valor} satoshis')
    print ('Iniciando a transferencia...')
    try:
        tx_hash = my_key.send([(destino, valor, "satoshi")], fee=taxa)
        if tx_hash:
            print('\n\nTransação Enviada com Sucesso !!!! ---- \n--- Hash da transação: ',tx_hash, '\n---')
            return tx_hash
        else:
            print('\n---------------Falha ao transferir, tente manualmente.---------------')
            return None
    except Exception as e:
        print(f'\n---------------Falha ao transferir, tente manualmente.---------------\n {e}')
        return None

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

def aguarda_quebra(): #Apos chamar o quebrar chave, fica procurando a key no arquivo KFound.txt na raiz
    kfound = 'KFound.txt'
    print('---------------------------------------------')
    time.sleep(20)
    contador = 0
    while True:
        sys.stdout.write(f"\r\nChave não encontrada... {contador} segundos\n")
        sys.stdout.flush()
        if os.path.exists(kfound):
            with open(kfound, "r") as file:
                content = file.read()
                match = re.search(r'Priv: (\w+)', content)
                if match:
                    try:
                        privkey = match.group(1)
                        wif = converter_wif(privkey)
                        try: 
                            with open (privkey_path, 'w') as file:
                                file.write(f'{wif}'.lower())
                        except Exception as e:
                            print(f'------------\nNão foi possivel salvar o arquivo com a chave WIF. WIF: {wif}\n-------------')
                        print (f"Chave Privada Salva no seu Drive: {privkey}")
                        print (f"CHAVE WIF = {wif}")
                        return wif
                    except Exception as e:
                        print (f'Erro ao retornar a chave: {e}')
        time.sleep(10)
        contador += 10
    
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
    path = './kangaroo'
    if os.path.exists('save.work'):
        argumentos = '-gpu -g 80,128 -t 0 -ws -w save.work -wi 60 -o KFound.txt save.work'
    else:
        argumentos = '-gpu -g 80,128 -t 0 -ws -w save.work -wi 60 -o KFound.txt all.txt'

    comando = f"{path} {argumentos}"
    print(comando)
    try: 
        print("Iniciando busca")
        subprocess.Popen(comando, shell=True)
    except Exception as e:
        print(f'Erro: {e}')

def main():
    verifica_saldo()
    my_wallet = input('Se encontrar a chave o bot tentara realizar a transfernecia para a sua carteira\nCole o endereço da sua carteira: ')
    selecionar = input('\n-------\n1 - Selecionar um número entre 1 e 50 milhoes.\n2 - Fazer a busca em todo o range da carteira 130 com save automático.\n-------Selecione uma opção: ')
    if selecionar == '1':
        selecionar_range()
        iniciar_busca(teste=False)
    elif selecionar == '2':
        busca_completa_com_save()
    else:
        print('Opção Inválida, encerrando.')
    wif = aguarda_quebra()
    transferir(wif, my_wallet)

if __name__ == '__main__':
    if input('Fazer teste na carteira 65? (s/n): ') in ['sim', 's', 'yes', 'y']:
        iniciar_busca(teste=True)
        aguarda_quebra()
    else:
        main()
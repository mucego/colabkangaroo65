import random
import subprocess
from bit import PrivateKey, network
import time
import sys
import os
import re
import hashlib
import base58
from google.colab import drive

drive.mount('/content/drive')
privkey_path = '/content/drive/My Drive/Private Key - Puzzle 130.txt'

def selecionar_range():
    parte = int(input('Digite uma parte a ser procurada entre 1 e 5_000_000 (cinco milhoes), ou 0 para uma parte aleatória: '))
    if parte == 0:
        parte = random.randint(1,5000000)
        print(f'Anote a parte gerada aleatória: {parte}')
    public_key = '03633cbe3ec02b9401c5effa144c5b4d22f87940259634858fc7e59b1c09937852'
    start = int('200000000000000000000000000000000', 16)
    end = int('3ffffffffffffffffffffffffffffffff', 16)
    partes = 5000000
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
    argumentos = '-gpu -t 1 -o KFound.txt 130.txt'
    if teste == True:
        argumentos = '-gpu -t 1 -o KFound.txt 65.txt'
    comando = f"{path} {argumentos}"
    print(comando)
    try: 
        subprocess.run(comando, shell=True, check=True)
        print("Iniciado busca")
    except Exception as e:
        print(f'Erro: {e}')

def transferir(wif, destino):

    my_key = PrivateKey(wif)
    print('---------------------------------------------------\nEndereço da Carteira Capturada: ', my_key.address, '\n---------------------------------------------------')
    saldo = my_key.balance_as('satoshi')
    print('---------------------------------------------------\nSaldo da Carteira Capturada: ', saldo, 'satoshis', '\n---------------------------------------------------')
    if destino == 'Não Informado':
        print('\nTransferencia não informada, endereço não informado.\n')
        return None
    taxa = network.get_fee('fast') 
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

def aguarda_quebra(segundos: int): #Apos chamar o quebrar chave, fica procurando a key no arquivo KFound.txt na raiz
    kfound = 'KFound.txt'
    time.sleep(1)
    for x in range(segundos):
        sys.stdout.write(f"\rEsperando Quebra da Chave... {x + 1}... / {segundos}\n")
        sys.stdout.flush()
        if os.path.exists(kfound):
            with open(kfound, "r") as file:
                content = file.read()
                match = re.search(r'Priv: (\w+)', content)
                if match:
                    privkey = match.group(1)
                    with open (privkey_path, 'w') as file:
                        file.write(privkey)
                    return match.group(1)
        time.sleep(1)

    print('\nVerifique se houve erro, Arquivo não encontrado.')
    if input("Tentar novamente? (s/n): ").lower() in ['s', 'sim', 'y', 'yes']:
        x = int(input("Digite quantos segundos quer aguardar: "))
        aguarda_quebra(x)
    else:
        chave_privada = input("Insira a chave privada: ")
        return chave_privada
    
def converter_wif(private_key_hex: str) -> str:
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

def main():
    verifica_saldo()
    selecionar_range()
    my_wallet = input('Cole o endereço da sua carteira: ')
    iniciar_busca(teste=False)
    chave_privada = aguarda_quebra(20)
    wif = aguarda_quebra(chave_privada)
    transferir(wif, my_wallet)


if __name__ == '__main__':
    if input('Fazer teste na carteira 65? (s/n): ') in ['sim', 's', 'yes', 'y']:
        iniciar_busca(teste=True)
        aguarda_quebra(20)
    else:
        main()
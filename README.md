# BOT 130 

Bot criado para automatizar o processo do desafio da carteira 130 usando Colab. Com sua conta Google é possivel utilizar algumas horas por dia `sem nenhum custo.`

## Como Usar? 
* Crie uma conta do Google se não tiver ainda.
* Acesse o site do Colab: https://colab.research.google.com
* Crie um novo notebook
* Clique em Ambiente de Execução
* Alterar Ambiente de Execução
* Marque a opção `T4 GPU` e salve.

Copie e cole os comandos abaixo:

```
!git clone https://github.com/ataidefcjr/colabkangaroo
%cd colabkangaroo/
!pip install -r requirements.txt
!python main.py
```
Para uso do modo 2 e manter os dados, é necessário montar o drive da conta google. Acrescente as seguintes linhas antes de `python main.py`.

**Observação**: Se não montar o drive, não será possível salvar o progresso.
```
from google.colab import drive
drive.mount('/content/drive')
```


Ao iniciar o bot vai ser solicitado 2 informações, sua carteira e o modo.
* Informe sua carteira para transferir o saldo se encontrada a chave ou deixe em branco para transferir manualmente.

**Selecione o modo**
* **Modo 1**: O range total é dividido em 50 milhões, voce escolhe um numero entre 1 e 50 milhões, ou 0 para um número aleatório, e a busca será feita nesse range. `(Você pode usar _ para ficar mais fácil de visualizar, por exemplo 32_541_305.)`
* **Modo 2**: O range total é divido em `16` para obtermos um intervalo de 125 bits, pois é o maximo suportado, informado para o Kangaroo, e será gerado arquivos work com salvamento do progresso, esse modo é indicado se deseja fazer multiplas contas google e unir os works, para isso leia o readme do repositorio do Kangaroo.
* Ao selecionar o modo 2 é necessário selecionar a parte entre 1 e 16 do range. 


Voce tambem pode passar o modo e o endereço da sua carteira via argumento. 

Por exemplo `!python main.py -m 2 -p 6 -d bc1qych3lyjyg3cse6tjw7m997ne83fyye4des99a9`
```
-m [É o modo a ser utilizado, podendo ser 1 ou 2.]
-p [É a parte entre 1 e 16, obrigatória para ser utilizado o modo 2.]
-d [É o endereço da sua carteira, para tentativa de transferencia imediatamente se a chave privada for encontrada]
```
   

## Observações Importantes

O Kangaroo do JeanLucPons já está devidamente compilado para usar no Colab, fique a vontade para compilar novamente por conta própria caso deseje. https://github.com/JeanLucPons/Kangaroo

* Comandos usados para compilar:
```
makefile_path = 'Makefile'
with open(makefile_path, 'r') as file:
    makefile_content = file.read()
    makefile_content = makefile_content.replace('/usr/local/cuda-8.0', '/usr/local/cuda-12.2')
    makefile_content = makefile_content.replace('/usr/bin/g++-4.8', '/usr/bin/g++')
with open(makefile_path, 'w') as file:
    file.write(makefile_content)
!make gpu=1 ccap=75 all
```
## Doações 

Se voce conseguir encontrar usando esse bot, o papai aceita um café: `bc1qych3lyjyg3cse6tjw7m997ne83fyye4des99a9`
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

Uma vez criado a conta e o notebook, da proxima vez que for usar basta navegar até o diretório e iniciar o bot.
```
%cd colabkangaroo
!python main.py
```
Ao iniciar o bot vai ser solicitado 2 informações, sua carteira e o modo.
* Informe sua carteira para transferir o saldo se encontrada a chave ou deixe em branco para transferir manualmente.

**Selecione o modo**
* **Modo 1**: O range total é dividido em 50 milhões, voce escolhe um numero entre 1 e 50 milhões, ou 0 para um número aleatório, e a busca será feita nesse range. `(Você pode usar _ para ficar mais fácil de visualizar, por exemplo 32_541_305.)`
* **Modo 2**: O range total é informado para o Kangaroo, e será gerado arquivos work com salvamento do progresso, esse modo é indicado se deseja fazer multiplas contas google e unir os works, para isso leia o readme do repositorio do Kangaroo.


Voce tambem pode passar o modo e o endereço da sua carteira via argumento. Por exemplo `!python main.py -m 2 -d bc1qych3lyjyg3cse6tjw7m997ne83fyye4des99a9`
   

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

Agora se voce conseguir encontrar usando esse bot, o papai aceita um café: `bc1qych3lyjyg3cse6tjw7m997ne83fyye4des99a9`
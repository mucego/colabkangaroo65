# BOT 130 

Bot criado para automatizar o processo do desafio da carteira 130 usando Colab `GRATUITAMENTE`

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

* Se desejar salvar o arquivo com a chave privada no seu google drive quando for encontrada, insira o comando abaixo antes da linha `!python main.py`
```
from google.colab import drive
drive.mount('/content/drive')
```
Uma vez criado a conta e o notebook, da proxima vez que for usar basta navegar até o diretório e iniciar o bot.
```
%cd colabkangaroo
!python main.py
```
Se der tudo certo o bot vai iniciar e vai perguntar se deseja fazer o teste na 65.

Ao selecionar `não` para o teste, o bot vai perguntar qual parte quer procurar, insira um numero entre 1 e 50 milhoes.
***(Você pode usar _ para ficar mais fácil de visualizar, por exemplo 32_541_305.)***

   
Informe o endereço da sua carteira, se por acaso voce for o sortudo, o bot tentara transferir os fundos para sua carteira. 

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
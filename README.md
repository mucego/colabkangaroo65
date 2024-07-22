# BOT 130 

Bot criado para automatizar o processo do desafio da carteira 130 usando Colab (GRATUITO)

# Como Usar? 
* Crie uma conta do Google se não tiver ainda.
* Acesse o site do Colab: https://colab.research.google.com
* Crie um novo notebook
* Clique em Ambiente de Execução
* Marque a opção `T4 GPU` e salve.

Cole os comandos abaixo:

```
!git clone https://github.com/ataidefcjr/colabkangaroo
%cd colabkangaroo/
!pip install -r requirements.txt
!python main.py
```
Se der tudo certo o bot vai iniciar e vai solicitar se deseja fazer o teste na 65.

Ao selecionar não ele vai perguntar qual parte quer procurar, insira um numero entre 1 e 5 milhoes.
***(Você pode usar _ para ficar mais fácil de visualizar, por exemplo 3_541_305.)***

Informe o endereço da sua carteira, se por acaso voce for o sortudo, o bot tentara transferir os fundos para sua carteira.    
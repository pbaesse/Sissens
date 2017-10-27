# SISSENS - SISTEMA DE GERENCIAMENTO DE SENSORES 

**Descrição**
------------------
SisSens visa a automação de aparelhos
eletrônicos, conectando-os à internet,
permitindo que o usuário interaja de forma
mais prática com os equipamentos de sua
residência e/ou empresa.

**Requisitos de Instalação**
------------------
	#Para que o sistema rode sem problemas no seu computador você deve criar um ambiente virtual por meio do virtualenv 	    utilizando 		#o seguinte comando no seu terminal: 

        - $ virtualenv Nome_Do_Ambiente 

	#Dessa forma todos os arquivos irão ser executados de forma correta.
	#É aconselhável você criar uma pasta primeiro e dentro dela clonar o ambiente virtual.
	#No termial, execute:

        - $ mkdir nomePasta
        - $ cd nomePasta/
        - nomePasta$ virtualenv Nome_Do_Ambiente

	#Depois que o ambiente estiver criado dentro da sua pasta, você executará o comando que irá clonar este repositório 	     para seu 	#computador.
	#Então, no seu terminal execute:

        - nomePasta$ git clone https://github.com/pbaesse/Sissen 

	#Após esse processo, você deve incluir todas as bibliotecas que estão sendo utilizadas nesse projeto.
	#Novamente, no terminal, execute:

        - nomePasta$ cd Nome_Do_Ambiente/
        - nomePasta/Nome_Do_Ambiente$ pip install -r bibliosAtualizadas.txt
	
	#Pronto. O sistema deve estar rodando sem erros!

	#** OBS **
	#Utilizamos neste o projeto a biblioteca Migrate, que serve como um gerenciador de comandos do Flask.
	#Para executá-lo é nescessário utilizar o seguinte comando:
	
	-(Nome_Do_Ambiente):NomePasta$ python run.py runserver	
	#Caso você faça alguma modificação no Banco de dados é nescessário executar os seguintes comandos:

	-(Nome_Do_Ambiente):NomePasta$ python run.py upgrade
	-(Nome_Do_Ambiente):NomePasta$ python run.py migrate 


**Problemas conhecidos e possíveis melhorias**
----------------------------------------------

- Corrigir a comunicação entre...
- ajeitar o banco de dados.
- Another WebApp, capable of comparing at least 10 stocks.

## Equipe
![eu copy](https://user-images.githubusercontent.com/19451652/30993612-2d93c5f6-a486-11e7-93ad-282acad1fb00.jpg)
![20526039_10212897312323106_4317811075203347960_n](https://user-images.githubusercontent.com/19451652/30993628-3798af62-a486-11e7-9c8a-e7df340fd9a5.jpg)
![eai-grupo-pq-o-silencio](https://user-images.githubusercontent.com/19451652/30993629-3883d26c-a486-11e7-8d46-be9648a403ab.jpg)
![teste](https://user-images.githubusercontent.com/19451652/30993633-3b64298c-a486-11e7-9c57-3bb67943e92e.jpg)
<br />Henrique spencer, Pedro baesse, João Pedro, Jessica
 

<a href="https://github.com/pbaesse">Pedro Baesse</a>                                                       
<a href="https://github.com/JoaoPedroSantosAlves">Joao Pedro</a>                                                 
<a href="https://github.com/henriqueSpencer">Henrique Spencer</a>
## [LICENSE](https://github.com/henriqueSpencer/Sissens/blob/master/LICENSE)

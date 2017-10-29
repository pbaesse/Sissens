
 <img src="https://user-images.githubusercontent.com/19451652/32145284-6ef08954-bca4-11e7-8a40-477851132390.png" align="middle"> 


**Descrição**
------------------
SisSens é um cliete mqtt criado em python com o framework flask, visando a automação de aparelhos eletrônicos, conectando-os à internet, permitindo que o usuário interaja de forma mais prática com os equipamentos de sua residência e/ou empresa.

**Requisitos de Instalação**
------------------
Abra o terminal e digite nele :

	# criando e ativando abiente virtual
        - $ virtualenv Nome_Do_Ambiente 
        - $ mkdir nomePasta
        - $ cd nomePasta/
        - $ nomePasta virtualenv Nome_Do_Ambiente

        - $ nomePasta git clone https://github.com/pbaesse/Sissen 

        - $ nomePasta cd Nome_Do_Ambiente/
        - $ nomePasta/Nome_Do_Ambiente$ pip install -r bibliosAtualizadas.txt
	
<br/><br/><br/>	

** OBS **
Utilizamos neste o projeto a biblioteca Migrate, que serve como um gerenciador de comandos do Flask.
Para executá-lo é nescessário utilizar o seguinte comando:
	
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
![image](https://user-images.githubusercontent.com/19451652/32110732-a883b50c-bb0e-11e7-900b-a198478c4ca6.png)
![image](https://user-images.githubusercontent.com/19451652/32110626-59cf2432-bb0e-11e7-859a-1938fbe62ff8.png)
![teste](https://user-images.githubusercontent.com/19451652/30993633-3b64298c-a486-11e7-9c57-3bb67943e92e.jpg)
<br />
 
<a href="https://github.com/henriqueSpencer">Henrique Spencer</a>

<a href="https://github.com/pbaesse">Pedro Baesse</a>      

<a href="https://github.com/JoaoPedroSantosAlves">João Pedro</a>

<a href="https://github.com/jessicakaroline">Jéssica</a>

## [LICENSE](https://github.com/henriqueSpencer/Sissens/blob/master/LICENSE)

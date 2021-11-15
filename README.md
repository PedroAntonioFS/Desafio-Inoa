# Desafio-Inoa
Bem-vindo ao Desafio-Inoa, minha solução da desafio proposto pela Inoa Sistemas.

## Instruções para execução
A solução utilizou Python e Django para construir uma aplicação web. A seguir algumas instruções de instalação e execução.

### Instruções
> Instalação Python

* Windows

Você pode baixar o instalador em https://www.python.org/downloads/windows/ . Certifique-se que está utilizando uma versão compatível com seu Windows (32-bits ou 64-bits) e 
marcar a caixa "Add Python X.XX to PATH" durante a instalação.

* MacOs

Você pode baixar versão do MacOS em  https://www.python.org/downloads/release/python-361. Antes de instalar, certifique-se que suas configurações permitam instalação de módulos
que não estejam na App Store.

* Linux

Execute o seguinte comando no terminal

`$ sudo apt install python3`

> Instalação Django

Após este repositório estiver dentro de um diretório (vamos usar o exemplo /desafio-inoa), execute os seguintes passos.

1. Criei um ambiente virtual, por exemplo:

Windows: `python -m venv myvenv`

Linux/MacOS: `python3 - =m venv myvenv`

2. Ative o ambiente virtual, por exemplo:

Windows: `myvenv\scripts\activate`

Linux/MacOS: `myvenv\bin\activate`

3. Instale o Django

Windows: `pip install django`

Linux/MacOS: `pip3 install django`

> Execute

1. Dentro de desafio-inoa, abra o diretório Inoa:

Windows: `cd Inoa`

Linux/MacOS: `cd Inoa`

1.1. Execute a aplicação:

Windows: `python manage.py runserver`

Linux/MacOS: `python3 manage.py runserver`

1.2. Execute os testes:

Windows: `python manage.py test`

Linux/MacOS: `python3 manage.py test`

### Limites
ATENÇÂO: A aplicação utiliza a API REST [ALPHA VANTAGE](https://www.alphavantage.co/) em sua versão gratuita, por isso há um limite de requisições, 5 chamadas por minuto e 500 chamadas por dia. Execute a aplicação e os testes com moderação.

## Entenda o Problema
Verifique a Wiki do projeto para uma compreensão mais ampla do problema e da solução implementada.

[Wiki](https://github.com/PedroAntonioFS/Desafio-Inoa/wiki)

A seguir alguns tópicos abordados na Wiki:

### Requisitos de Software
A especificação dos requisitos de software contém informações estruturadas do problema proposto. Nela há a descrição do problema, requisitos expostos e casos de usos encontrados.
[Ver](https://drive.google.com/file/d/1Yn1OREJIaLayQKNKZGOm9vAsNNeAHZDh/view)

### Arquitetura do Software
Nesse tópico há a arquitetura da solução implementada. Possui o diagrama entidade-realcionamento e o diagrama de classes.
[Ver](https://github.com/PedroAntonioFS/Desafio-Inoa/wiki/Arquitetura-do-Software)

### Product Backlog
O product backlog possui a descrição das features implementas, suas prioridades e issues relacionadas.
[Ver](https://github.com/PedroAntonioFS/Desafio-Inoa/wiki/Product-Backlog)

### Documentação
A documentação possui uma descrição das classes implementas, atributos, parâmetros, métodos e funções.
[Ver](https://github.com/PedroAntonioFS/Desafio-Inoa/wiki/Documenta%C3%A7%C3%A3o)

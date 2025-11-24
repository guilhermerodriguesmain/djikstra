<h1 align="center"> Rotas com Dijkstra</h1>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange">
</p>

<p align="center">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="NetworkX" src="https://img.shields.io/badge/NetworkX-FFA500?style=for-the-badge">
  <img alt="Matplotlib" src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge">
  <img alt="HTML5" src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
  <img alt="CSS3" src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
  <img alt="JavaScript" src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
</p>

## Descrição do projeto

* Projeto desenvolvido durante as aulas de Estrutura de Dados Avançado da Universidade de Vassouras (Univassouras) - Campos Maricá.

## Estrutura 

```text
/dijkstra/
│
├── .gitignore             <-- (Ignora arquivos desnecessários, como 'venv')
├── README.md              <-- (Este arquivo que você está lendo)
│── /docs/                 <-- (documentação)
├── pyproject.toml         <-- Configurações e atalhos (Taskipy)
│
├── /backend/              <-- (Toda a lógica da API FastAPI)
│   │
│   ├── /app/
│   │   │
│   │   ├── /api/
│   │   │   └── routes.py    <-- (Define os endpoints: /calculate-path, /graph-data)
│   │   │
│   │   ├── /core/
│   │   │   ├── graph.py     <-- (Classes 'Graph' e a lógica Dijkstra)
│   │   │   └── schemas.py   <-- (Modelos Pydantic)
│   │   │
│   │   └── main.py          <-- (Ponto de entrada da aplicação FastAPI)
│   │
│   ├── venv/                <-- (Ambiente virtual do Python - ignorado pelo .gitignore)
│   └── requirements.txt     <-- (Lista de dependências, ex: 'fastapi', 'uvicorn')
│
└── /frontend/             <-- (Toda a parte visual e interativa)
    │
    ├── index.html           <-- (A estrutura da página web)
    ├── style.css            <-- (Estilos: cores dos nós, layout, etc.)
    └── script.js            <-- (Lógica do cliente: fetch para a API) 

```

## Como Rodar o Projeto

### Pré-requisitos 

* Python 3.10 ou superior instalado.

### 1- Clone o repositório:

```bash
  git clone https://github.com/guilhermerodriguesmain/djikstra
  cd djikstra
```

### 2- Crie e ative um ambiente virtual (Recomendado):

```bash
  # Windows
  python -m venv venv
  .\venv\Scripts\activate

  # Linux/Mac
  python3 -m venv venv
  source venv/bin/activate
```

### 3- Instale as depedências

```bash
  pip install -r backend/requirements.txt
```

### 4- Execute a aplicação:

```bash
  # com o comando do task
  task run

  # ou manualmente
  cd backend && uvicorn app.main:app --reload
```

### 5- Acesse
Abra o arquivo frontend/index.html no navegador ou use uma extensão como "Live Server". 

Você pode também utilizar os atalhos do task 
```bash
  # abrir o html no Windows
  task open

  # abrir o html no Linux
  task openl
```

## Tecnologias Utilizadas

### Backend
* FastAPI: Framework moderno e rápido para construção da API.

* Uvicorn: Servidor ASGI para produção.

* NetworkX: Biblioteca poderosa para manipulação e estudo de grafos.

* Matplotlib: Utilizado para gerar a representação visual (imagem PNG) do grafo.

* Pydantic: Validação de dados e Schemas.

### Frontend
* HTML5 / CSS3: Layout responsivo (Flexbox) e estilização.

* JavaScript: Consumo da API via Fetch e manipulação do DOM.

### Ferramentas
* Taskipy: Automação de comandos de terminal.

## Arquitetura
<ol>
  <li>O Frontend envia a matriz ou solicitação de rota.</li>
  <li>O Backend (FastAPI) recebe os dados.</li>
  <li>O Núcleo (Graph Class) usa NetworkX para calcular o caminho.</li>
  <li>O Matplotlib desenha o grafo em memória (Buffer).</li>
  <li>A imagem é convertida para Base64.</li>
  <li>O Backend retorna um JSON contendo a Imagem Base64 + Dados da Matriz.</li>
  <li>O Frontend apenas exibe a imagem.</li>
</ol>


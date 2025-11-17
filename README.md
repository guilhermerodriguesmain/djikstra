<h1 align="center"> Rotas com Dijkstra</h1>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange">
</p>

<p align="center">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
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
│
├── /backend/              <-- (Toda a lógica da API FastAPI)
│   │
│   ├── /app/
│   │   │
│   │   ├── /api/
│   │   │   └── routes.py    <-- (Define os endpoints: /calculate-path, /graph-data)
│   │   │
│   │   ├── /core/
│   │   │   ├── graph.py     <-- (Classes 'Graph', 'Node' e a lógica Dijkstra)
│   │   │   └── schemas.py   <-- (Modelos Pydantic: PathRequest, MatrixRequest)
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
    └── script.js            <-- (Lógica do cliente: desenhar SVG, fetch para a API) 

```

## Pré-requisitos 
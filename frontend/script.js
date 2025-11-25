const API_URL = "http://localhost:8000";
const imgElement = document.getElementById('graph-img');

// Inicializa buscando o grafo padrão
fetchGraph();

// --- Funções de API ---

// 1. Busca dados iniciais
async function fetchGraph() {
    try {
        const res = await fetch(`${API_URL}/graph`);
        const data = await res.json();
        render(data);
    } catch (error) {
        console.error("Erro ao buscar grafo:", error);
    }
}

// 2. Gera mapa aleatório
async function generateRandomGraph() {
    try {
        const res = await fetch(`${API_URL}/random-map`, { method: 'POST' });
        const data = await res.json();
        render(data.graph);
        
        // Limpa mensagens de resultado antigo
        document.getElementById('result-display').innerText = "";
    } catch (error) {
        alert("Erro ao gerar mapa aleatório");
    }
}

// 3. Atualiza via Texto Manual (Textarea)
async function updateGraph() {
    const text = document.getElementById('matrix-input').value;
    
    const validation = validateMatrixInput(text);
    if (!validation.valid) {
        alert("Erro: " + validation.message);
        return; // Para aqui e não envia nada ao servidor
    }

    try {
        const res = await fetch(`${API_URL}/update-map`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ matrix_text: text })
        });
        const data = await res.json();
        
        if(data.status === 'ok') {
            render(data.graph);
            document.getElementById('result-display').innerText = "";
        } else {
            alert("Erro no formato da matriz: " + data.message);
        }
    } catch (error) {
        console.error(error);
    }
}

// 4. Calcula Rota (Dijkstra)
async function calculateRoute() {
    const start = document.getElementById('start-node').value;
    const end = document.getElementById('end-node').value;

    try {
        const res = await fetch(`${API_URL}/calculate`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ start, end })
        });
        
        // A resposta agora contém: { result: {...}, graph: {...} }
        // 'graph' traz a imagem já pintada de vermelho pelo Python
        const data = await res.json();
        const result = data.result;

        const display = document.getElementById('result-display');

        if(result.distance === -1) {
            display.innerText = "Sem caminho possível!";
            display.style.color = "red";
        } else {
            display.innerText = `Distância Mínima: ${result.distance}`;
            display.style.color = "black";
        }

        // Renderiza o grafo que veio na resposta (com o destaque visual)
        render(data.graph);

    } catch (error) {
        console.error("Erro ao calcular rota:", error);
    }
}

// --- Funções de Renderização e UI ---

// Função Central: Recebe os dados do Python e atualiza a tela
function render(data) {
    // 1. Atualiza a Imagem (O Python manda string Base64)
    if (data.image) {
        imgElement.src = data.image;
    }

    // 2. Atualiza os Dropdowns de seleção
    populateDropdowns(data.nodes);

    // 3. Atualiza a Tabela Editável
    renderMatrixTable(data.nodes, data.matrix);

    // 4. Mantém o Textarea sincronizado
    updateTextareaFromData(data.matrix);
}

function renderMatrixTable(nodes, matrix) {
    const table = document.getElementById('matrix-table');
    table.innerHTML = '';

    // Cabeçalho (A, B, C...)
    const thead = table.insertRow();
    thead.insertCell(); // Célula vazia no canto
    nodes.forEach(n => {
        const th = document.createElement('th');
        th.textContent = n;
        thead.appendChild(th);
    });

    // Corpo da Tabela
    matrix.forEach((row, i) => {
        const tr = table.insertRow();
        
        // Rótulo da linha
        const thRow = document.createElement('th');
        thRow.textContent = nodes[i];
        tr.appendChild(thRow);

        row.forEach((val, j) => {
            const td = tr.insertCell();
            
            // Diagonal principal bloqueada
            if (i === j) {
                td.textContent = '-';
                td.style.backgroundColor = "#ddd";
                return;
            }

            const input = document.createElement('input');
            input.type = "number";
            input.value = val;
            input.min = 0;
            input.className = "matrix-input";
            
            // Salva automaticamente ao mudar o valor e sair do campo
            input.onchange = () => saveFromTable(nodes.length);
            
            td.appendChild(input);
        });
    });
}

// Pega os dados da tabela HTML e envia para o backend
async function saveFromTable(size) {
    const table = document.getElementById('matrix-table');
    const rows = table.querySelectorAll('tr');
    
    let matrixRows = [];

    // Começa de i=1 pois a linha 0 é o cabeçalho
    for (let i = 1; i <= size; i++) {
        let cols = [];
        const inputs = rows[i].querySelectorAll('input');
        
        let inputIndex = 0;
        for (let j = 0; j < size; j++) {
            if (i - 1 === j) { 
                cols.push(0); // Diagonal
            } else {
                const val = inputs[inputIndex].value;
                cols.push(val === "" ? 0 : parseInt(val));
                inputIndex++;
            }
        }
        matrixRows.push(cols.join(','));
    }

    const matrixText = matrixRows.join(';');

    // Envia para o backend atualizar
    try {
        const res = await fetch(`${API_URL}/update-map`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ matrix_text: matrixText })
        });
        
        const data = await res.json();
        if(data.status === 'ok') {
            // Atualiza a imagem e o textarea, mas mantém a tabela como está
            // para não perder o foco do usuário (opcionalmente poderia chamar render total)
            if (data.graph.image) {
                imgElement.src = data.graph.image;
            }
            updateTextareaFromData(data.graph.matrix);
            
            // Limpa resultado anterior pois o mapa mudou
            document.getElementById('result-display').innerText = "";
        }
    } catch (error) {
        console.error("Erro ao salvar tabela:", error);
    }
}

function updateTextareaFromData(matrix) {
    const text = matrix.map(row => row.join(',')).join(';');
    document.getElementById('matrix-input').value = text;
}

function populateDropdowns(nodes) {
    const startSel = document.getElementById('start-node');
    const endSel = document.getElementById('end-node');
    
    const oldStart = startSel.value;
    const oldEnd = endSel.value;

    startSel.innerHTML = '';
    endSel.innerHTML = '';
    
    nodes.forEach(n => {
        startSel.add(new Option(n, n));
        endSel.add(new Option(n, n));
    });

    // Tenta manter a seleção anterior se o nó ainda existir
    if(nodes.includes(oldStart)) startSel.value = oldStart;
    if(nodes.includes(oldEnd)) endSel.value = oldEnd;
}

//--------------------------------------------------- validação de dados de entrada
function validateMatrixInput(text) {
    // 1. Verificação de Segurança (Regex)
    // Permite APENAS: Números (0-9), vírgula (,), ponto e vírgula (;), espaços e quebra de linha
    const allowedPattern = /^[0-9,;\s]+$/;
    
    if (!allowedPattern.test(text)) {
        return { valid: false, message: "A matriz contém caracteres inválidos! Use apenas números, vírgulas e ponto-e-vírgula." };
    }

    // 2. Verificação Estrutural (É uma matriz quadrada?)
    const rows = text.split(';').filter(row => row.trim().length > 0);
    if (rows.length === 0) return { valid: false, message: "A matriz está vazia." };

    const numRows = rows.length;
    
    for (let i = 0; i < numRows; i++) {
        const cols = rows[i].split(',').filter(col => col.trim().length > 0);
        
        // Verifica se cada linha tem o mesmo número de colunas que o total de linhas (NxN)
        if (cols.length !== numRows) {
            return { 
                valid: false, 
                message: `Erro na linha ${i+1}: A matriz deve ser quadrada (${numRows}x${numRows}). Encontrado ${cols.length} colunas.` 
            };
        }
    }

    return { valid: true };
}
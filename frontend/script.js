const API_URL = "http://localhost:8000";
const svg = document.getElementById('graph-svg');

// Inicializa
fetchGraph();

// Busca dados iniciais
async function fetchGraph() {
    const res = await fetch(`${API_URL}/graph`);
    const data = await res.json();
    render(data);
}

// Gera mapa aleatório
async function generateRandomGraph() {
    const res = await fetch(`${API_URL}/random-map`, { method: 'POST' });
    const data = await res.json();
    render(data.graph);
}

// Atualiza via Texto Manual
async function updateGraph() {
    const text = document.getElementById('matrix-input').value;
    if(!text) return alert("Digite a matriz!");

    const res = await fetch(`${API_URL}/update-map`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ matrix_text: text })
    });
    const data = await res.json();
    if(data.status === 'ok') {
        render(data.graph);
    } else {
        alert("Erro no formato da matriz");
    }
}

// Calcula rota Dijkstra
async function calculateRoute() {
    const start = document.getElementById('start-node').value;
    const end = document.getElementById('end-node').value;

    const res = await fetch(`${API_URL}/calculate`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ start, end })
    });
    const result = await res.json();
    
    const display = document.getElementById('result-display');

    if(result.distance === -1) {
        display.innerText = "Sem caminho possível!";
        display.style.color = "red";
        clearHighlights();
        return;
    }

    display.innerText = `Distância Mínima: ${result.distance}`;
    display.style.color = "black";
    highlightPath(result.path);
}

// ============================================
// Lógica de Renderização e Tabelas
// ============================================

function render(data) {
    const nodes = data.nodes;
    const edges = data.edges;
    const matrix = data.matrix;

    // 1. Atualiza SVG
    renderSVG(nodes, edges);

    // 2. Atualiza Controles
    populateDropdowns(nodes);

    // 3. Atualiza Tabela Editável
    renderMatrixTable(nodes, matrix);

    // 4. Atualiza Textarea para manter sincronicidade
    updateTextareaFromData(matrix);
}

function renderSVG(nodes, edges) {
    svg.innerHTML = `
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
            refX="19" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="black" />
            </marker>
        </defs>
    `;
    
    const centerX = 300, centerY = 150, radius = 100;
    const positions = {};
    const angleStep = (2 * Math.PI) / nodes.length;

    // Calcula Posições
    nodes.forEach((node, i) => {
        const angle = i * angleStep - (Math.PI / 2); 
        positions[node] = {
            x: centerX + radius * Math.cos(angle),
            y: centerY + radius * Math.sin(angle)
        };
    });

    // Desenha Arestas
    nodes.forEach(source => {
        if(edges[source]) {
            Object.entries(edges[source]).forEach(([target, weight]) => {
                const p1 = positions[source];
                const p2 = positions[target];
                
                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute("x1", p1.x);
                line.setAttribute("y1", p1.y);
                line.setAttribute("x2", p2.x);
                line.setAttribute("y2", p2.y);
                line.setAttribute("class", "edge-line");
                line.id = `edge-${source}-${target}`;
                svg.appendChild(line);

                // Peso da aresta
                const midX = (p1.x + p2.x) / 2;
                const midY = (p1.y + p2.y) / 2;
                
                // Fundo branco para o texto
                const textBg = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                textBg.setAttribute("x", midX - 5);
                textBg.setAttribute("y", midY - 10);
                textBg.setAttribute("width", 10);
                textBg.setAttribute("height", 14);
                textBg.setAttribute("fill", "white");
                svg.appendChild(textBg);

                const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                text.setAttribute("x", midX);
                text.setAttribute("y", midY);
                text.setAttribute("class", "edge-text");
                text.setAttribute("text-anchor", "middle");
                text.setAttribute("dominant-baseline", "middle");
                text.textContent = weight;
                svg.appendChild(text);
            });
        }
    });

    // Desenha Nós (Grupo para facilitar destaque)
    nodes.forEach(node => {
        const pos = positions[node];
        
        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.id = `node-group-${node}`;

        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", pos.x);
        circle.setAttribute("cy", pos.y);
        circle.setAttribute("r", 16);
        circle.setAttribute("class", "node-circle");
        g.appendChild(circle);

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", pos.x);
        text.setAttribute("y", pos.y);
        text.setAttribute("class", "node-text");
        text.textContent = node;
        g.appendChild(text);

        svg.appendChild(g);
    });
}

function renderMatrixTable(nodes, matrix) {
    const table = document.getElementById('matrix-table');
    table.innerHTML = '';

    // Header
    const thead = table.insertRow();
    thead.insertCell(); 
    nodes.forEach(n => {
        const th = document.createElement('th');
        th.textContent = n;
        thead.appendChild(th);
    });

    // Body
    matrix.forEach((row, i) => {
        const tr = table.insertRow();
        
        // Label lateral
        const thRow = document.createElement('th');
        thRow.textContent = nodes[i];
        tr.appendChild(thRow);

        row.forEach((val, j) => {
            const td = tr.insertCell();
            
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
            
            // Salva automaticamente ao mudar
            input.onchange = () => saveFromTable(nodes.length);
            
            td.appendChild(input);
        });
    });
}

// Pega dados da tabela e atualiza o mapa
async function saveFromTable(size) {
    const table = document.getElementById('matrix-table');
    const rows = table.querySelectorAll('tr');
    
    let matrixRows = [];

    // Começa do índice 1 (pula header)
    for (let i = 1; i <= size; i++) {
        let cols = [];
        const inputs = rows[i].querySelectorAll('input');
        
        let inputIndex = 0;
        for (let j = 0; j < size; j++) {
            if (i - 1 === j) { 
                cols.push(0); // Diagonal é sempre 0
            } else {
                const val = inputs[inputIndex].value;
                cols.push(val === "" ? 0 : parseInt(val));
                inputIndex++;
            }
        }
        matrixRows.push(cols.join(','));
    }

    const matrixText = matrixRows.join(';');

    // Atualiza backend
    const res = await fetch(`${API_URL}/update-map`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ matrix_text: matrixText })
    });
    
    const data = await res.json();
    if(data.status === 'ok') {
        // Atualiza visual (Textarea e SVG) sem perder estado
        updateTextareaFromData(data.graph.matrix);
        renderSVG(data.graph.nodes, data.graph.edges);
        
        // Se já tinha uma rota calculada, limpa o destaque pois o mapa mudou
        clearHighlights(); 
        document.getElementById('result-display').innerText = "";
    }
}

function updateTextareaFromData(matrix) {
    const text = matrix.map(row => row.join(',')).join(';');
    document.getElementById('matrix-input').value = text;
}

function populateDropdowns(nodes) {
    const startSel = document.getElementById('start-node');
    const endSel = document.getElementById('end-node');
    
    // Salva seleção atual se possível
    const oldStart = startSel.value;
    const oldEnd = endSel.value;

    startSel.innerHTML = '';
    endSel.innerHTML = '';
    
    nodes.forEach(n => {
        startSel.add(new Option(n, n));
        endSel.add(new Option(n, n));
    });

    if(nodes.includes(oldStart)) startSel.value = oldStart;
    if(nodes.includes(oldEnd)) endSel.value = oldEnd;
}

function clearHighlights() {
    // 1. Remove a classe de grupos de nós (círculo + texto)
    document.querySelectorAll('.highlight-group').forEach(el => {
        el.classList.remove('highlight-group');
    });

    // 2. Remove a classe das arestas (linhas)
    document.querySelectorAll('.highlight-edge').forEach(el => {
        el.classList.remove('highlight-edge');
    });

    // 3. (Segurança extra) Remove de nós soltos caso existam
    document.querySelectorAll('.highlight-node').forEach(el => {
        el.classList.remove('highlight-node');
    });
}

function highlightPath(path) {
    clearHighlights();

    // Destaca nós (adiciona classe ao grupo)
    path.forEach(node => {
        const g = document.getElementById(`node-group-${node}`);
        if(g) g.classList.add('highlight-group');
    });

    // Destaca arestas
    for(let i = 0; i < path.length - 1; i++) {
        const u = path[i];
        const v = path[i+1];
        // Tenta encontrar aresta U->V ou V->U (se for bidirecional, mas nosso grafo é dirigido visualmente)
        let edge = document.getElementById(`edge-${u}-${v}`);
        if(!edge) edge = document.getElementById(`edge-${v}-${u}`);
        
        if(edge) edge.classList.add('highlight-edge');
    }
}
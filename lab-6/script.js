const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');

const n1 = 3, n2 = 3, n3 = 2, n4 = 3;
const verticesNum = 10 + n3;
const k = 1.0 - n3 * 0.01 - n4 * 0.005 - 0.05;
const circlesPs = Math.floor(verticesNum / 4);
const radius = 30;
const margin = (1000 / circlesPs - 2 * radius);

let directedMatrix = [];
let undirectedMatrix = [];
let verticesCoord = {};
let mstEdges = [];
let currentEdgeIndex = 0;

const verticesOnSameSide = {
    1: [3, 4, 10, 11],
    2: [4],
    3: [1],
    4: [1, 2, 6, 7],
    5: [7],
    6: [4],
    7: [5, 4, 9, 10],
    8: [10],
    9: [7],
    10: [7, 8, 12, 1],
    11: [1],
    12: [10]
};

function directedMatrixGen() {
    const seed = 3323;
    Math.seedrandom(seed);

    directedMatrix = [];
    for (let i = 0; i < verticesNum; i++) {
        let row = [];
        for (let j = 0; j < verticesNum; j++) {
            let randomNumber = Math.random() * 2.0;
            let element = randomNumber * k;
            row.push(element < 1.0 ? 0 : 1);
        }
        directedMatrix.push(row);
    }
}

function undirectedMatrixGen() {
    directedMatrixGen();
    undirectedMatrix = [];
    for (let i = 0; i < verticesNum; i++) {
        let row = [];
        for (let j = 0; j < verticesNum; j++) {
            if (directedMatrix[i][j] === 1 || directedMatrix[j][i] === 1) {
                row.push(1);
            } else {
                row.push(0);
            }
        }
        undirectedMatrix.push(row);
    }
}

function getDirectedVerticesCoordcenters(x, y, dict) {
    let graphNum = 1;
    for (let i = 1; i <= circlesPs; i++) {
        dict[graphNum] = { x, y };
        y -= margin;
        graphNum++;
    }

    for (let i = circlesPs + 1; i <= 2 * circlesPs; i++) {
        dict[graphNum] = { x, y };
        x -= margin;
        graphNum++;
    }

    for (let i = 2 * circlesPs + 1; i <= 3 * circlesPs; i++) {
        dict[graphNum] = { x, y };
        y += margin;
        graphNum++;
    }

    for (let i = 3 * circlesPs + 1; i <= 4 * circlesPs; i++) {
        dict[graphNum] = { x, y };
        x += margin;
        graphNum++;
    }
}

function drawArrowHeads(weightMatrix) {
    let n = 0;
    for (let i = 0; i < verticesNum; i++) {
        for (let j = n; j < verticesNum; j++) {
            if (undirectedMatrix[i][j] === 1 && verticesOnSameSide[j + 1].includes(i + 1)) {
                drawCurvedArrow(i, j, weightMatrix);
            } else if (undirectedMatrix[i][j] === 1 && i === j) {
                drawLoop(i);
            } else if (undirectedMatrix[i][j] === 1) {
                drawStraightArrow(i, j, weightMatrix);
            }
        }
        n++;
    }
}

function drawLine(startX, startY, endX, endY, weight, color = 'black', width = 1) {
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = color;
    ctx.stroke();

    ctx.font = '13px Arial';
    ctx.fillStyle = 'red';
    ctx.lineWidth = width;
    const textX = (startX * 5 + endX - 60) / 6;
    const textY = (startY * 5 + endY) / 6;
    ctx.fillText(weight, textX, textY);
}

function drawCurvedArrow(i, j, weightMatrix, color = 'black') {
    let startX = verticesCoord[i + 1].x;
    let startY = verticesCoord[i + 1].y;
    let endX = verticesCoord[j + 1].x;
    let endY = verticesCoord[j + 1].y;

    let dx = endX - startX;
    let dy = endY - startY;
    let distance = Math.sqrt(dx * dx + dy * dy);

    endX = endX - (radius * dx) / distance;
    endY = endY - (radius * dy) / distance;

    let middleX, middleY;
    if (i <= circlesPs && j <= circlesPs) {
        middleX = (startX + endX) / 2 + 2 * radius;
        middleY = (startY + endY) / 2;
    } else if (circlesPs < j && j <= circlesPs * 2) {
        middleX = (startX + endX) / 2;
        middleY = (startY + endY) / 2 - 2 * radius;
    } else if (circlesPs * 2 < j && j <= circlesPs * 3) {
        middleX = (startX + endX) / 2 - 2 * radius;
        middleY = (startY + endY) / 2;
    } else if ((circlesPs * 3 < j && j < circlesPs * 4)) {
        middleX = (startX + endX) / 2;
        middleY = (startY + endY) / 2 + 2 * radius;
    }

    drawLine(startX, startY, middleX, middleY, weightMatrix[i][j], color);
    drawLine(middleX, middleY, endX, endY, weightMatrix[i][j], color);
}

function drawStraightArrow(i, j, weightMatrix, color = 'black') {
    let startX = verticesCoord[i + 1].x;
    let startY = verticesCoord[i + 1].y;
    let endX = verticesCoord[j + 1].x;
    let endY = verticesCoord[j + 1].y;

    let dx = endX - startX;
    let dy = endY - startY;
    let distance = Math.sqrt(dx * dx + dy * dy);

    endX = endX - (radius * dx) / distance;
    endY = endY - (radius * dy) / distance;
    drawLine(startX, startY, endX, endY, weightMatrix[i][j], color);
}

function drawLoop(i) {
    const x = verticesCoord[i + 1].x - radius / 1.5;
    const y = verticesCoord[i + 1].y - radius / 1.5;
    const loopRadius = 20;
    ctx.beginPath();
    ctx.arc(x, y, loopRadius, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.closePath();
}

function drawVertices(dict) {
    for (let vertex in dict) {
        let x = dict[vertex].x;
        let y = dict[vertex].y;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = 'lightblue';
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = 'black';
        ctx.font = '16px Arial';
        ctx.fillText(vertex, x - 5, y + 5);
    }
}

function drawGraphWithMST() {
    undirectedMatrixGen();
    getDirectedVerticesCoordcenters(900, 900, verticesCoord);
    drawVertices(verticesCoord);

    let weightMatrix = weightMatrixGen();
    drawArrowHeads(weightMatrix);
    
    const result = primMST(undirectedMatrix, weightMatrix);
    mstEdges = result.mstEdges;
    currentEdgeIndex = 0;
    
    console.log("Graph matrix:", undirectedMatrix);
    console.log("Weight matrix:", weightMatrix);
    console.log("Total weight of MST:", result.totalWeight);
}

function weightMatrixGen() {
    const cMatrix = [];
    for (let i = 0; i < verticesNum; i++) {
        let row = [];
        for (let j = 0; j < verticesNum; j++) {
            let randomNumber = Math.random();
            let ceilElement = Math.ceil(randomNumber * 100 * undirectedMatrix[i][j]);
            row.push(ceilElement);
        }
        cMatrix.push(row);
    }

    const dMatrix = [];
    for (let i = 0; i < verticesNum; i++) {
        let row = [];
        for (let j = 0; j < verticesNum; j++) {
            row.push(cMatrix[i][j] === 0 ? 0 : 1);
        }
        dMatrix.push(row);
    }

    const hMatrix = [];
    for (let i = 0; i < verticesNum; i++) {
        hMatrix.push(Array(verticesNum).fill(0));
    }
    for (let i = 0; i < verticesNum; i++) {
        for (let j = 0; j < verticesNum; j++) {
            hMatrix[i][j] = (dMatrix[i][j] !== dMatrix[j][i] ? 1 : 0);
        }
    }

    let trMatrix = [];
    for (let i = 0; i < verticesNum; i++) {
        trMatrix.push(Array(verticesNum).fill(0));
    }

    for (let i = 0; i < verticesNum; i++) {
        for (let j = i + 1; j < verticesNum; j++) {
            trMatrix[i][j] = 1;
        }
    }

    const weightMatrix = [];
    for (let i = 0; i < verticesNum; i++) {
        weightMatrix.push(Array(verticesNum).fill(0));
    }

    for (let i = 0; i < verticesNum; i++) {
        for (let j = 0; j < verticesNum; j++) {
            weightMatrix[i][j] = (dMatrix[i][j] + hMatrix[i][j] * trMatrix[i][j]) * cMatrix[i][j];
            weightMatrix[j][i] = weightMatrix[i][j];
        }
    }
    return weightMatrix;
}

class Node {
    constructor(item) {
        this.value = item;
        this.next = null;
    }
}

class LinkedList {
    constructor() {
        this.head = null;
        this.length = 0;
    }

    add(value) {
        const node = new Node(value);
        let current;

        if (!this.head) {
            this.head = node;
        } else {
            current = this.head;

            while (current.next) {
                current = current.next;
            }

            current.next = node;
        }
        this.length++;
    }

    remove(index) {
        if (index < 0 || index >= this.length) {
            throw new Error('Out of index');
        } else {
            let curr, prev, it = 0;
            curr = this.head;
            prev = curr;
            if (index === 0) {
                this.head = curr.next;
            } else {
                while (it < index) {
                    it++;
                    prev = curr;
                    curr = curr.next;
                }
                prev.next = curr.next;
            }
            this.length--;
            return curr.value;
        }
    }

    get(index) {
        if (index < 0 || index >= this.length) {
            throw new Error('Out of index');
        } else {
            let curr = this.head;
            for (let i = 0; i < index; i++) {
                curr = curr.next;
            }
            return curr.value;
        }
    }
}

class PriorityQueue {
    constructor() {
        this.items = [];
    }

    enqueue(element, priority) {
        let qElement = { element, priority };
        let added = false;

        for (let i = 0; i < this.items.length; i++) {
            if (this.items[i].priority > qElement.priority) {
                this.items.splice(i, 0, qElement);
                added = true;
                break;
            }
        }

        if (!added) {
            this.items.push(qElement);
        }
    }

    dequeue() {
        if (this.isEmpty()) {
            return null;
        }
        return this.items.shift();
    }

    isEmpty() {
        return this.items.length === 0;
    }
}

function primMST(graph, weightMatrix) {
    const numVertices = graph.length;
    const pq = new PriorityQueue();
    const inMST = new Array(numVertices).fill(false);
    const parent = new Array(numVertices).fill(null);
    const key = new Array(numVertices).fill(Infinity);
    const mstEdges = [];
    let totalWeight = 0; // Для зберігання загальної ваги MST

    key[0] = 0;
    pq.enqueue(0, 0);

    while (!pq.isEmpty()) {
        const { element: u } = pq.dequeue();
        inMST[u] = true;

        if (parent[u] !== null) {
            mstEdges.push([parent[u], u]);
            totalWeight += weightMatrix[parent[u]][u];
        }

        for (let v = 0; v < numVertices; v++) {
            if (graph[u][v] && !inMST[v] && weightMatrix[u][v] < key[v]) {
                key[v] = weightMatrix[u][v];
                pq.enqueue(v, key[v]);
                parent[v] = u;
            }
        }
    }

    return { mstEdges, totalWeight };
}

function drawNextStep() {
    if (currentEdgeIndex < mstEdges.length) {
        const [u, v] = mstEdges[currentEdgeIndex];
        let color = 'red';
        drawLine(
            verticesCoord[u + 1].x,
            verticesCoord[u + 1].y,
            verticesCoord[v + 1].x,
            verticesCoord[v + 1].y,
            ' ',
            color,
            2
        );
        currentEdgeIndex++;
    }
}

drawGraphWithMST();

document.addEventListener('keydown', (event) => {
    if (event.key === ' ') {
        drawNextStep();
    }
});
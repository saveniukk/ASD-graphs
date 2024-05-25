const canvas = document.getElementById('graphCanvas');
const ctx = canvas.getContext('2d');

const n1 = 3, n2 = 3, n3 = 2, n4 = 3;
const verticesNum = 10 + n3;
const k = 1.0 - n3 * 0.01 - n4 * 0.005 - 0.15;
const circlesPs = Math.floor(verticesNum / 4);
const radius = 30;
const margin = (800 / circlesPs - 2 * radius);

let directedMatrix = [];
let directedVerticesCoord = {};

const directedVerticesCoordonSameSide = {
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

    for (let i = 0; i < verticesNum; i++) {
        let row = [];
        for (let j = 0; j < verticesNum; j++) {
            let randomNumber = Math.random() * 2.0;
            let element = randomNumber * k;
            row.push(element < 1.0 ? 0 : 1);
        }
        directedMatrix.push(row);
    }
    console.log(directedMatrix);
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

function drawArrowHeads() {
    let copiedMatrix = JSON.parse(JSON.stringify(directedMatrix));
    for (let i = 0; i < verticesNum; i++) {
        for (let j = 0; j < verticesNum; j++) {
            if (directedVerticesCoordonSameSide[j + 1]?.includes(i + 1)) {
                if (copiedMatrix[i][j] === 1 && copiedMatrix[j][i] === 1 && i !== j) {
                    drawCurvedArrow(i, j);
                } else if (copiedMatrix[i][j] === 1) {
                    drawCurvedArrow(i, j);
                }
            } else if (copiedMatrix[i][j] === 1 && copiedMatrix[j][i] === 1 && i !== j) {
                drawDoubleArrow(i, j);
                copiedMatrix[j][i] = 0;
            } else if (copiedMatrix[i][j] === 1 && i === j) {
                drawLoop(i);
            } else if (copiedMatrix[i][j] === 1 && i !== j && copiedMatrix[i][j] !== copiedMatrix[j][i] && !directedVerticesCoordonSameSide[j + 1]?.includes(i + 1)) {
                drawStraightArrow(i, j);
            }
        }
    }
}

function drawArrow(startX, startY, endX, endY, color = 'black') {
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = color;
    ctx.stroke();

    let angle = Math.atan2(endY - startY, endX - startX);
    let arrowLength = 15;

    ctx.beginPath();
    ctx.moveTo(endX, endY);
    ctx.lineTo(endX - arrowLength * Math.cos(angle - Math.PI / 6), endY - arrowLength * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(endX - arrowLength * Math.cos(angle + Math.PI / 6), endY - arrowLength * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
}

function drawCurvedArrow(i, j, color = 'black') {
    let startX = directedVerticesCoord[i + 1].x;
    let startY = directedVerticesCoord[i + 1].y;
    let endX = directedVerticesCoord[j + 1].x;
    let endY = directedVerticesCoord[j + 1].y;

    let dx = endX - startX;
    let dy = endY - startY;
    let distance = Math.sqrt(dx * dx + dy * dy);

    endX = endX - (radius * dx) / distance;
    endY = endY - (radius * dy) / distance;

    let middleX, middleY;
    if (i <= circlesPs && j <= circlesPs) {
        middleX = (startX + endX) / 2 + 2 * radius;
        middleY = (startY + endY) / 2;
    } else if (circlesPs < i && i <= circlesPs * 2) {
        middleX = (startX + endX) / 2;
        middleY = (startY + endY) / 2 - 2 * radius;
    } else if (circlesPs * 2 < i && i <= circlesPs * 3) {
        middleX = (startX + endX) / 2 - 2 * radius;
        middleY = (startY + endY) / 2;
    } else if ((circlesPs * 3 < i && i < circlesPs * 4) || (i == 0 && (circlesPs * 3 < j && j < circlesPs * 4))) {
        middleX = (startX + endX) / 2;
        middleY = (startY + endY) / 2 + 2 * radius;
    }

    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(middleX, middleY);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = color;
    ctx.stroke();

    drawArrow(middleX, middleY, endX, endY, color);
}

function drawDoubleArrow(i, j) {
    let startX = directedVerticesCoord[i + 1].x + 5;
    let startY = directedVerticesCoord[i + 1].y - 5;
    let endX = directedVerticesCoord[j + 1].x + 5;
    let endY = directedVerticesCoord[j + 1].y - 5;

    let dx = endX - startX;
    let dy = endY - startY;
    let distance = Math.sqrt(dx * dx + dy * dy);

    endX = endX - (radius * dx) / distance;
    endY = endY - (radius * dy) / distance;
    drawArrow(startX, startY, endX, endY);

    startX = directedVerticesCoord[j + 1].x - 5;
    startY = directedVerticesCoord[j + 1].y + 5;
    endX = directedVerticesCoord[i + 1].x - 5;
    endY = directedVerticesCoord[i + 1].y + 5;

    dx = endX - startX;
    dy = endY - startY;
    distance = Math.sqrt(dx * dx + dy * dy);

    endX = endX - (radius * dx) / distance;
    endY = endY - (radius * dy) / distance;

    drawArrow(startX, startY, endX, endY);
}

function drawStraightArrow(i, j, color = 'black') {
    let startX = directedVerticesCoord[i + 1].x;
    let startY = directedVerticesCoord[i + 1].y;
    let endX = directedVerticesCoord[j + 1].x;
    let endY = directedVerticesCoord[j + 1].y;

    let dx = endX - startX;
    let dy = endY - startY;
    let distance = Math.sqrt(dx * dx + dy * dy);

    endX = endX - (radius * dx) / distance;
    endY = endY - (radius * dy) / distance;
    drawArrow(startX, startY, endX, endY, color);
}

function drawLoop(i) {
    const x = directedVerticesCoord[i + 1].x;
    const y = directedVerticesCoord[i + 1].y;
    const loopRadius = 20;
    const arrowLength = 10;
    const arrowHeadWidth = 10;

    ctx.save();
    ctx.beginPath();

    ctx.translate(x, y);
    ctx.arc(-radius, -radius, loopRadius, 0, 2 * Math.PI, false);
    ctx.strokeStyle = 'black';
    ctx.stroke();

    ctx.beginPath();
    const arrowX = -radius + loopRadius * Math.cos(1.5 * Math.PI);
    const arrowY = -radius + loopRadius * Math.sin(1.5 * Math.PI);
    ctx.moveTo(arrowX, arrowY);
    ctx.lineTo(arrowX - arrowLength, arrowY - arrowHeadWidth / 2);
    ctx.lineTo(arrowX - arrowLength, arrowY + arrowHeadWidth / 2);
    ctx.closePath();
    ctx.fillStyle = 'black';
    ctx.fill();

    ctx.restore();
}


function drawVertices(dict) {
    for (let vertex in dict) {
        let x = dict[vertex].x;
        let y = dict[vertex].y;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = 'red';
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = 'black';
        ctx.font = '16px Arial';
        ctx.fillText(vertex, x - 5, y + 5);
    }
}

function drawGraph() {
    directedMatrixGen();
    getDirectedVerticesCoordcenters(700, 700, directedVerticesCoord);
    drawArrowHeads();
    drawVertices(directedVerticesCoord);
}

function markVertex(vertex, color) {
    let x = directedVerticesCoord[vertex].x;
    let y = directedVerticesCoord[vertex].y;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = 'black';
    ctx.font = '16px Arial';
    ctx.fillText(vertex, x - 5, y + 5);
}

const vertexStatus = Array(verticesNum).fill(0);

const treeMatrixGen = () => {
    const treeMatrix = Array.from({ length: verticesNum }, () => Array(verticesNum).fill(0));
    return treeMatrix;
}

function DFS(matrix, startVertex) {
    const stack = [];

    const edgeStack = []; 
    const treeMatrix = treeMatrixGen();
    let currentVertex = startVertex;
    let k = 1;

    vertexStatus[startVertex] = k;
    stack.push(startVertex);
    markVertex(startVertex + 1, 'green');

    function nextStep(event) {
        if (event.key === ' ') {
            if (edgeStack.length > 0) {
                const [u, v] = edgeStack.pop();
                if (!directedVerticesCoordonSameSide[u + 1].includes(v + 1)) {
                    drawStraightArrow(u, v, 'blue');
                } else {
                    drawCurvedArrow(u, v, 'blue');
                }
                markVertex(v + 1, 'green');
            } else if (stack.length > 0) {
                currentVertex = stack.pop();
                markVertex(currentVertex + 1, 'yellow');
                for (let adjVertex = 0; adjVertex < verticesNum; adjVertex++) {
                    if (matrix[currentVertex][adjVertex] == 1 && vertexStatus[adjVertex] === 0) {
                        k++;
                        vertexStatus[adjVertex] = k;
                        stack.push(adjVertex);
                        edgeStack.push([currentVertex, adjVertex]);
                        treeMatrix[currentVertex][adjVertex] = 1;
                        break;
                    }
                }
            } else {
                document.removeEventListener('keydown', nextStep);
                console.log(vertexStatus);
                console.log(treeMatrix);
            }
        }
    }
    document.addEventListener('keydown', nextStep);
}

drawGraph();
DFS(directedMatrix, 0);


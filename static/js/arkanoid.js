// document.addEventListener('DOMContentLoaded', () => {
//     const canvas = document.getElementById('arkanoidCanvas');
//     const context = canvas.getContext('2d');
//     const roomName = document.getElementById('room-name').dataset.roomName;
//     const gameSocket = new WebSocket('ws://' + window.location.host + '/ws/game/' + roomName + '/');

//     let isController = false;
//     let gameState = {};
//     let gameInterval = null;
//     let gameRunning = false;
//     let restartGameRequested = false;

//     // WebSocket message handling
//     gameSocket.onmessage = function(e) {
//         const data = JSON.parse(e.data);
//         if (data.controller !== undefined) {
//             isController = data.controller;
//         } else {
//             gameState = data.game_state;
//             drawArkanoidElements();
//         }
//     };

//     gameSocket.onclose = function(e) {
//         console.error('Game socket closed unexpectedly');
//     };

//     // Start and restart game button event listeners
//     document.getElementById('startGameBtn').addEventListener('click', () => {
//         if (!gameRunning && isController) {
//             gameRunning = true;
//             startGame();
//         }
//     });

//     document.getElementById('restartGameBtn').addEventListener('click', () => {
//         if (!gameRunning && restartGameRequested) {
//             window.location.reload();
//         }
//     });

//     // Fetch initial game state
//     fetchInitialGameState();

//     // Fetch initial game state from the server
//     function fetchInitialGameState() {
//         fetch('/initial_game_state/')
//             .then(response => response.json())
//             .then(data => {
//                 gameState = data;
//                 drawArkanoidElements();
//                 checkGameState();
//                 restartGameRequested = false;
//             });
//     }

//     // Start game interval
//     function startGame() {
//         gameInterval = setInterval(fetchGameState, 10); // Fetch game state every 10ms
//     }

//     // Fetch game state if the current user is the controller
//     function fetchGameState() {
//         if (gameRunning && isController) {
//             fetch('/game_state/')
//                 .then(response => response.json())
//                 .then(data => {
//                     gameState = data;
//                     drawArkanoidElements();
//                     checkGameState();
//                     sendGameState(gameState);  // Send game state to WebSocket
//                 });
//         }
//     }

//     // Send game state to WebSocket
//     function sendGameState(gameState) {
//         if (isController) {
//             gameSocket.send(JSON.stringify({
//                 'game_state': gameState
//             }));
//         }
//     }

//     // Check game state and show restart button if game is over
//     function checkGameState() {
//         if (gameState.game_over) {
//             gameRunning = false;
//             showRestartButton();
//             restartGameRequested = true; 
//             clearInterval(gameInterval); 
//         }
//     }

//     // Show restart button
//     function showRestartButton() {
//         const restartButton = document.getElementById('restartGameBtn');
//         restartButton.style.display = 'inline-block';
//     }

//     // Handle key press events
//     document.addEventListener('keydown', (event) => {
//         if (['ArrowLeft', 'ArrowRight'].includes(event.key)) {
//             sendKeyPress(event.key);
//         }
//     });

//     // Send key press to the server
//     function sendKeyPress(key) {
//         if (gameRunning && isController) {
//             fetch('/game_state/', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': getCookie('csrftoken')
//                 },
//                 body: JSON.stringify({ key: key })
//             })
//             .then(response => response.json())
//             .then(data => {
//                 gameState = data;
//                 drawArkanoidElements();
//             });
//         }
//     }

//     // Get CSRF token
//     function getCookie(name) {
//         let cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             const cookies = document.cookie.split(';');
//             for (let i = 0; i < cookies.length; i++) {
//                 const cookie = cookies[i].trim();
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }

//     // Draw Arkanoid elements on the canvas
//     function drawArkanoidElements() {
//         context.clearRect(0, 0, canvas.width, canvas.height);
//         drawBricks();
//         drawBall();
//         drawPaddle();
//         drawLives();
//     }

//     // Draw bricks
//     function drawBricks() {
//         const rectWidth = canvas.dataset.rectWidth;
//         const rectHeight = canvas.dataset.rectHeight;

//         gameState.bricks.forEach(brick => {
//             if (brick.status === 1) {
//                 context.fillStyle = 'blue';
//                 context.fillRect(brick.x, brick.y, rectWidth, rectHeight);
//             }
//         });
//     }

//     // Draw ball
//     function drawBall() {
//         const ball = gameState.ball;
//         const ballRadius = canvas.dataset.ballRadius;
//         context.beginPath();
//         context.arc(ball.x, ball.y, ballRadius, 0, Math.PI * 2);
//         context.fillStyle = 'red';
//         context.fill();
//         context.closePath();
//     }

//     // Draw paddle
//     function drawPaddle() {
//         const paddle = gameState.paddle;
//         const bottomRectWidth = canvas.dataset.bottomRectWidth;
//         const bottomRectHeight = canvas.dataset.bottomRectHeight;
//         const gap = canvas.dataset.gap;
//         context.fillStyle = 'green';
//         context.fillRect(paddle.x, canvas.height - bottomRectHeight - gap, bottomRectWidth, bottomRectHeight);
//     }

//     // Draw lives
//     function drawLives() {
//         context.font = '16px Arial';
//         context.fillStyle = 'red';
//         context.fillText('Lives: ' + gameState.lives, canvas.width - 60, 15);
//     }
    
//     document.getElementById('restartGameBtn').style.display = 'none';
// });
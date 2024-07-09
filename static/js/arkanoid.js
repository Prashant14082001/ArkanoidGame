document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('arkanoidCanvas');
    const context = canvas.getContext('2d');

    const ballRadius = Number(canvas.dataset.ballRadius);
    const rectWidth = Number(canvas.dataset.rectWidth);
    const rectHeight = Number(canvas.dataset.rectHeight);
    const gap = Number(canvas.dataset.gap);
    const bottomRectWidth = Number(canvas.dataset.bottomRectWidth);
    const bottomRectHeight = Number(canvas.dataset.bottomRectHeight);

    let gameState = {};
    let gameInterval = null;
    let gameRunning = false;

    // Fetch initial game state
    fetch('/game_state/')
        .then(response => response.json())
        .then(data => {
            gameState = data;
            drawArkanoidElements();
            if (gameState.lives === 0) {
                gameOver();
            }
        });

    // Event listener for Start Game button
    document.getElementById('startGameBtn').addEventListener('click', () => {
        if (!gameRunning) {
            gameRunning = true;
            startGame();
        }
    });

    // Start the game loop
    function startGame() {
        gameInterval = setInterval(fetchGameState, 10);
    }

    // Fetch game state from server
    function fetchGameState() {
        fetch('/game_state/')
            .then(response => response.json())
            .then(data => {
                gameState = data;
                drawArkanoidElements();
                if (gameState.lives === 0) {
                    gameOver();
                }
            });
    }

    // Handle game over condition
    function gameOver() {
        
        gameRunning = false;
        alert('Game Over');
        
        setTimeout(() => {
            window.location.reload(); 
        }, 100); 
    }

    // Send key press events to server
    document.addEventListener('keydown', (event) => {
        if (['ArrowLeft', 'ArrowRight'].includes(event.key)) {
            sendKeyPress(event.key);
        }
    });

    // Send key press data to server
    function sendKeyPress(key) {
        if (gameRunning) {
            fetch('/game_state/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ key: key })
            })
            .then(response => response.json())
            .then(data => {
                gameState = data;
                drawArkanoidElements();
            });
        }
    }

    // Utility function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Draw game elements on canvas
    function drawArkanoidElements() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        drawBricks();
        drawBall();
        drawPaddle();
        drawLives();
    }

    // Draw bricks on canvas
    function drawBricks() {
        gameState.bricks.forEach(brick => {
            if (brick.status === 1) {
                context.fillStyle = 'blue';
                context.fillRect(brick.x, brick.y, rectWidth, rectHeight);
            }
        });
    }

    // Draw ball on canvas
    function drawBall() {
        const ball = gameState.ball;
        context.beginPath();
        context.arc(ball.x, ball.y, ballRadius, 0, Math.PI * 2);
        context.fillStyle = 'red';
        context.fill();
        context.closePath();
    }

    // Draw paddle on canvas
    function drawPaddle() {
        const paddle = gameState.paddle;
        context.fillStyle = 'green';
        context.fillRect(paddle.x, canvas.height - bottomRectHeight - gap, bottomRectWidth, bottomRectHeight);
    }

    // Draw lives counter on canvas
    function drawLives() {
        context.font = '16px Arial';
        context.fillStyle = 'red';
        context.fillText('Lives: ' + gameState.lives, canvas.width - 60, 15);
    }
});

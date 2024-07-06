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

    function fetchGameState() {
        fetch('/game_state/')
            .then(response => response.json())
            .then(data => {
                gameState = data;
                drawArkanoidElements();
            });
    }

    function sendKeyPress(key) {
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

    function drawBricks() {
        gameState.bricks.forEach(brick => {
            if (brick.status === 1) {
                context.fillStyle = 'blue';
                context.fillRect(brick.x, brick.y, rectWidth, rectHeight);
            }
        });
    }

    function drawBall() {
        const ball = gameState.ball;
        context.beginPath();
        context.arc(ball.x, ball.y, ballRadius, 0, Math.PI * 2);
        context.fillStyle = 'red';
        context.fill();
        context.closePath();
    }

    function drawPaddle() {
        const paddle = gameState.paddle;
        context.fillStyle = 'green';
        context.fillRect(paddle.x, canvas.height - bottomRectHeight - gap, bottomRectWidth, bottomRectHeight);
    }

    function drawArkanoidElements() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        drawBricks();
        drawBall();
        drawPaddle();
    }

    document.addEventListener('keydown', (event) => {
        if (['ArrowLeft', 'ArrowRight'].includes(event.key)) {
            sendKeyPress(event.key);
        }
    });

    setInterval(fetchGameState, 10);
});

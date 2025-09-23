// Configuración del canvas
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');

// Ajustar el tamaño del canvas al tamaño de la ventana
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Clase para las partículas
class Particle {
    constructor(x, y, size, color, velocity) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.color = color;
        this.velocity = velocity;
    }

    // Dibujar la partícula
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }

    // Actualizar la posición de la partícula
    update() {
        this.x += this.velocity.x;
        this.y += this.velocity.y;

        // Rebotar en los bordes del canvas
        if (this.x + this.size > canvas.width || this.x - this.size < 0) {
            this.velocity.x = -this.velocity.x;
        }
        if (this.y + this.size > canvas.height || this.y - this.size < 0) {
            this.velocity.y = -this.velocity.y;
        }

        this.draw();
    }
}

// Crear un array de partículas
const particles = [];
function initParticles() {
    particles.length = 0; // Limpiar el array
    const particleCount = 100; // Número de partículas
    for (let i = 0; i < particleCount; i++) {
        const size = Math.random() * 3 + 1; // Tamaño aleatorio entre 1 y 4
        const x = Math.random() * (canvas.width - size * 2) + size;
        const y = Math.random() * (canvas.height - size * 2) + size;
        const color = '#ffffff'; // Color de las partículas (blanco)
        const velocity = {
            x: (Math.random() - 0.5) * 2, // Velocidad aleatoria en X
            y: (Math.random() - 0.5) * 2, // Velocidad aleatoria en Y
        };
        particles.push(new Particle(x, y, size, color, velocity));
    }
}

// Función para animar las partículas
function animateParticles() {
    requestAnimationFrame(animateParticles);
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Limpiar el canvas

    // Dibujar un fondo oscuro
    ctx.fillStyle = '#1a1a1a'; // Fondo oscuro
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Actualizar y dibujar cada partícula
    particles.forEach((particle) => {
        particle.update();
    });
}

// Inicializar y animar las partículas
initParticles();
animateParticles();
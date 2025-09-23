// Desplazamiento suave para los enlaces del menú
document.querySelectorAll('nav ul li a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Animación para el formulario de contacto
const contactForm = document.getElementById('contact-form');
contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Gracias por contactarnos. Te responderemos pronto.');
    contactForm.reset();
});

// Animación para el formulario de suscripción
const subscribeForm = document.getElementById('subscribe-form');
subscribeForm.addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Gracias por suscribirte.');
    subscribeForm.reset();
});
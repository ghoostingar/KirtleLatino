// Personaje de TV
let nombre = "Homero";
let anime = "Los Simpsons";
let edad = 68;

let personaje = {
    nombre: "Homero",
    anime: "Los Simpsons",
    edad: 68,
};
console.log(personaje);
console.log(personaje.nombre);
console.log(personaje['anime']);

personaje.edad = 13;
let llave = "edad";
personaje[llave] = 68;

delete personaje.anime;

console.log(personaje);
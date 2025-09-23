// short-circuit

// Falso
// false
// 0
// ''
// undefined
// null
// NaN
let nombre = 'Alan Wep';
let username = nombre || 'Anónimo';
console.log(username);

function fn1() {
    console.log('Sou función 1');
    return false;
}

function fn2() {
    console.log('Sou función 2');
    return true;
}
let x = fn1() && fn2();
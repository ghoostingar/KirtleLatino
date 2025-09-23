// Ejercicio 12
Algoritmo cSocios
	Definir nombre, nombre2, direccion, direccion2 Como Caracter;
	Definir edad, edad2 Como Entero;
	
	Escribir "Ingrese el nombre del primer socio: ";
	Leer nombre;
	Escribir "Ingrese el nombre del segundo socio: ";
	Leer nombre2;
	Escribir "Ingrese la direccion del primer socio: ";
	Leer direccion;
	Escribir "Ingrese la direccion del segundo socio: ";
	Leer direccion2;
	Escribir "Ingrese la edad del primero socio: ";
	Leer edad;
	Escribir "Ingrese la edad del segundo socio: ";
	Leer edad2;
	
	Si edad < edad2 Entonces
		Escribir "Estos son los datos del socio mas joven: ", nombre, direccion, edad;
	FinSi
	
FinAlgoritmo
	
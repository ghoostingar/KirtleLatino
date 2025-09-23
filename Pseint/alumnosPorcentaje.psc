Algoritmo alumnosPorcentaje
	definir aluPromocionados, aluRegularizados, aluDesaprobados, aluLibres Como Real;
	definir promPromocionados, promRegularizados, promDesaprobados, promLibres Como Real;
	Definir totalAlumnos Como Real;
	
	Escribir "Ingrese la cantidad de alumnos promocionado: ";
	Leer aluPromocionados;
	Escribir "Ingrese la cantidad de los alumnos regularizados: ";
	Leer aluRegularizados;
	Escribir "Ingrese la cantidad de los alumnos desaprobados: ";
	Leer aluDesaprobados;
	Escribir "Ingrese la cantidad de los alumnos lubres: ";
	Leer aluLibres;
	
	// Alumnos totales
	totalAlumnos <- aluPromocionados + aluRegularizados + aluDesaprobados + aluLibres;
	
	//Porcentaje
	promPromocionados <- (totalAlumnos / aluPromocionados) * 100;
	promRegularizados <- (totalAlumnos / aluRegularizados) * 100;
	promDesaprobados <- (totalAlumnos / aluDesaprobados) * 100;
	promLibres <- (totalAlumnos / aluLibres) * 100;
	
	Escribir "El porcentaje de alumnos es:";
	Escribir "Promocionados: ", promPromocionados, "%";
	Escribir "Regularizados: ", promRegularizados, "%";
	Escribir "Desaprobados: ", promDesaprobados, "%";
	Escribir "Libres: ", promLibres, "%";
	
	
	
FinAlgoritmo
	
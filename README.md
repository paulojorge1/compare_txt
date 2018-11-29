# compare_txt
Compare txt or csv files.

Steps:
- Menu -> Select "Cargar fichero antiguo" to select first file, then opens windows to upload second file
- Wait for log: "Fichero "comparacion.xlsx" creado en la carpeta: ….." and the status bar: "'Ejecución terminada em … segundos'"
- Writes an excel with a matrix comparing the different lines between the files. 
  Between "index" and "col" columns we have the similarity indexes. In the "posiciones" column I identify the differences.

Image description:
En este caso, la primera línea (con index 0)  tiene un índice de similitud con la segunda línea de 0.998 y con la quinta línea de 0.998. 
En la columna 3 las diferencias con la segunda línea son "1('replace', 0, 1, 0, 1)('equal', 1, 463, 1, 463)". 
Aparece la numeración de la línea: 1 (los índices empiezan en cero, por eso la segunda línea la identifico con 1) seguida de 
('replace', 0, 1, 0, 1): significa que hay un carácter distinto en la primera posición. ('equal', 1, 463, 1, 463): significa que todo 
el restante es igual. Las diferencias con la quita línea son 4('replace', 0, 1, 0, 1)('equal', 1, 463, 1, 463).
Cuando aparece en blanco es porque es una línea nueva que está en el primero fichero y no en el segundo (left_only en la comuna "_merge").

1('replace', 0, 1, 0, 1)('equal', 1, 463, 1, 463)4('replace', 0, 1, 0, 1)('equal', 1, 463, 1, 463)
- La columna "index" identifica las líneas distintas, comezando por 0. El programa compara el primero fichero con el segundo, 
por eso en la columna "_merge" pongo left_only para las líneas distintas en el primero fichero y right_only para líneas distintas
identificadas en el segundo fichero.
- A partir de la columna posiciones podemos identificar la posición de los caracteres.
                                                                                                

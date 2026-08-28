# Diferencias entre los verbos GET, POST, PATCH, DELETE
# Porque POST no es idempotente?

* GET: Solo se utiliza para leer informacion del servidor, sin modificar ningun dato.
* POST: Se utiliza para creear un nuevo elemento o tarea, al llamarlo el servidor genera un nuevo elemento.
* PATCH: Se utiliza para actualizar un recurso existente, pero solo modifica los campos especificos que le envies en el cuerpo JSON. 
* Delete: Se utiliza para eliminar un recurso del servidor(el recurso debe existir).


* Post no es idempotente porque cada vez que hacés una llamada a POST el servidor crea y guarda un recurso nuevo con un identificador único distinto. Si se ejecuta el mismo comando 5 veces, la base de datos terminara con 5 tareas diferentes.En cambio métodos como GET, sí es idempotente, consultar un elemento GET 5 veces devuelve siempre la misma información.
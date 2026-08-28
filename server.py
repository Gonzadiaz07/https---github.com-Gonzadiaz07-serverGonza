from asyncio import tasks
from wsgiref.simple_server import make_server
import json


#Datos en memoria
tasks = [
    {"id": 1, "titulo": "Hacer las compras", "done": False},
    {"id": 2, "titulo": "Estudiar ISI", "done": True}
]

#Def para WSGI
def app(environ, start_response):
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')
    headers = [('Content-Type' , 'application /json; charset=utf-8')]

#Get tasks
    if path == '/tasks' and method == 'GET':
        start_response('200 OK', headers)
        return [json.dumps(tasks).encode('utf-8')]

#Post tasks 
    elif path ==  '/tasks' and method == 'POST':
        #Leemos el Json
        lenght = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(lenght)
        data = json.loads(body.decode('utf-8'))

        new_task = {
            "id": len(tasks) + 1,
            "titulo": data.get('titulo', ""),
            "done": data.get("done", False)
        }
        tasks.append(new_task)
        start_response('201 Created', headers)
        return [json.dumps(new_task).encode('utf-8')]

    #Rutas tasks {id}
    elif path.startswith('/tasks/'):
        parts = path.split('/')
        if len(parts)== 3 and parts[2].isdigit():
            task_id = int(parts[2])

            #Buscar la tarea primero
            task = next((t for t in tasks if t['id'] == task_id), None)

            #Si no existe, responde 404
            if not task:
                start_response('404 Not Found', headers)
                return [json.dumps({"error": "Tarea no encontrada"}).encode('utf-8')]

            #Si existe, procesar los metodos
            if method == 'GET':
                start_response('200 OK', headers)
                return [json.dumps(task).encode('utf-8')]

            elif method == 'PATCH':
                length = int(environ.get('CONTENT_LENGTH', 0))
                if length > 0:
                    body = environ['wsgi.input'].read(length)
                    data = json.loads(body.decode('utf-8'))
                else:
                    data = {}

                for key, value in data.items():
                    if key in task:
                        task[key] = value

                start_response('200 OK', headers)
                return [json.dumps(task).encode('utf-8')]

            elif method == 'DELETE':
                tasks.remove(task)
                start_response('200 OK', headers)
                return [json.dumps({"message": "Tarea eliminada"}).encode('utf-8')]
        
    #Get tasks {id}
            if method == 'GET':
                start_response('200 OK', headers)
                return [json.dumps(task).encode('utf-8')]

    # PATCH tasks{id}
    elif method == 'PATCH':
        #Leamos el Json
        length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(length)
        data = json.loads(body.decode('utf-8'))

        for key, value in data.items():
            if key in task:
                task[key] = value

        start_response('200 OK', headers)
        return [json.dumps(task).encode('utf-8')]


    #DELETE tasks{id}
    elif method == 'DELETE':
        tasks.remove(task)
        start_response('200 OK', headers)
        return [json.dumps({"message": "Tarea eliminada"}).encode('utf-8')]

    start_response('404 Not Found', headers)
    return [json.dumps({"error": "Ruta no encontrada"}).encode('utf-8')]

#Para enceder el servidor
make_server('localhost', 9292, app).serve_forever()
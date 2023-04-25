from flask import Flask, jsonify, make_response
from io import BytesIO


def generate_txt(data):

    buffer = BytesIO()

    # Escribir el nombre de la receta
    buffer.write(data['name'].encode('utf-8') + b'\n\n')

    # Escribir la sección de ingredientes
    buffer.write('Ingredientes:\n'.encode('utf-8'))
    for item in data['ingredients']:
        buffer.write(item.encode('utf-8') + b'\n')
    buffer.write(b'\n')

    # Escribir la sección de procedimientos
    buffer.write('Preparación:\n'.encode('utf-8'))
    for i, item in enumerate(data['procedure']):
        buffer.write( item.encode('utf-8') + b'\n')

    # Obtener el contenido del buffer y devolverlo
    response = make_response(buffer.getvalue())
    buffer.close()

    file_name = data["name"].replace(' ', '_')

    # set the content disposition
    response.headers.set('Content-Disposition', 'attachment', filename='{}.txt'.format(file_name))
    response.headers.set('Content-Type', 'text/plain')
    return response


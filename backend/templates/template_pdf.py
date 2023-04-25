from flask import Flask, make_response
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_pdf(data):

    # Crear un objeto StyleSheet con los estilos de texto por defecto
    styles = getSampleStyleSheet()
    heading3_style = ParagraphStyle(
        name='HeaderStyle',
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor='black',
        leading=20
    )
    custom_style = ParagraphStyle(name='CustomStyle', fontName='Helvetica', fontSize=12, leading=16)

    # Crear un buffer de memoria para almacenar el PDF
    buffer = BytesIO()

    # Crear el objeto de lienzo para dibujar en el PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)


    # Crea el titulo 
    pdf.drawCentredString(300, 750, data['name'])

    # Define la posición inicial de los elementos
    max_y = 700
    y = max_y

    # Crear un objeto Paragraph con el texto y estilo
    p = Paragraph("Ingredientes", heading3_style)
    w, h = p.wrapOn(pdf, 500, 1000)
    p.drawOn(pdf, 50, y)
    y -= h

    
    for item in data['ingredients']:
        # Crea el objeto Paragraph
        p = Paragraph(item, custom_style)

        # Obtén el ancho y alto del Paragraph
        w, h = p.wrapOn(pdf, 500, 1000)

        # Si el Paragraph no cabe en la página actual, crea una nueva página y resetea la posición
        if y - h < 50:
            pdf.showPage()
            y = max_y

        # Dibuja el Paragraph en la posición actual
        p.drawOn(pdf, 50, y)

        # Actualiza la posición de Y
        y -= h


    # Actualiza la posición de Y antes de comenzar la sección de procedimientos
    p = Paragraph("Preparación", heading3_style)
    w, h = p.wrapOn(pdf, 500, 1000)
    p.drawOn(pdf, 50, y)
    y -= h

    for item in data['procedure']:
        # Crea el objeto Paragraph
        p = Paragraph(item, custom_style)

        # Obtén el ancho y alto del Paragraph
        w, h = p.wrapOn(pdf, 500, 1000)

        # Si el Paragraph no cabe en la página actual, crea una nueva página y resetea la posición
        if y - h < 50:
            pdf.showPage()
            y = max_y

        # Dibuja el Paragraph en la posición actual
        p.drawOn(pdf, 50, y)

        # Actualiza la posición de Y
        y -= h

        # Agrega un espacio en blanco
        #paragraphs.append(Spacer(1, 0.2 * inch))


    # Build the PDF
    pdf.save()

    # create a response object and set the content type
    response = make_response(buffer.getvalue())

    file_name = data["name"].replace(' ', '_')

    # set the content disposition
    response.headers['Content-Disposition'] = 'attachment; filename={}.pdf'.format(file_name)
    response.headers['Content-Type'] = 'application/pdf'

    return response

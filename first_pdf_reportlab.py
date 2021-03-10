from reportlab.pdfgen import canvas

def hello(c):
    """ Escreve "Hello World"  em um pdf """

    c.drawString(100, 100, "Hello World")

c = canvas.Canvas("hello.pdf")

hello(c)
c.showPage() # Para o desenho na página corrente
c.save() # gera o documento pdf
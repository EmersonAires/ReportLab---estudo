from reportlab.pdfgen import canvas

def hello(c, i):
    """ Escreve "Hello World"  em um pdf """

    c.drawString(100, 100, "Hello World {}".format(i))

c = canvas.Canvas("hello_4pages.pdf")

i = 1
while i < 5:
    hello(c, i)
    c.showPage() # Para o desenho na página corrente
    i += 1

c.save() # gera o documento pdf
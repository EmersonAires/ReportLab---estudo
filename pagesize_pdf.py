from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

#mayCanvas = Canvas('myfile.pdf', pagesize=letter)

# altura e largura em pontos. --> 1 ponto = (1/72 de uma pol)

L_width, L_height = letter
A_width, A_height = A4 

print('Letter -- > Largura: {} , Altura: {}'.format(L_width, L_height))
print('A4 -- > Largura: {} , Altura: {}'.format(A_width, A_height))
import PySimpleGUI as sg
import os
from PIL import Image, ImageTk
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


# ---------------------------------------------------------------------------------------------------------------------------------------------
#    Gerar PDF
# ---------------------------------------------------------------------------------------------------------------------------------------------

width, height = A4
w_img = 200 # points
h_img = 200
x_ref = (width/2) - (w_img/2) # coordenada horizontal das imagens

def gerar_pdf(folder, fnames):

    nome_relatorio = sg.popup_get_text('Digite o nome do relatório')
    nome_relatorio = nome_relatorio + ".pdf"


    c = canvas.Canvas(nome_relatorio, pageCompression=1)

    for img in fnames:

        path = os.path.join(folder, img)

        if fnames.index(img) % 2 != 0:
            img_down(c, path)
        else:
            img_top(c, path)
    
    c.save()

def img_top(c, path):

    c.drawImage(path, x_ref, (0.60*height), w_img, h_img )

def img_down(c, path):

    c.drawImage(path, x_ref, (0.15*height), w_img, h_img )
    c.showPage()


# ----------------------------------------------------------------------------------------------------------------------------------------------







#  selecionar pasta com fotos
folder = sg.popup_get_folder('Selecione a pasta com as imagens', default_path='')

# Se não for selecionado nenhuma pasta, fechar aplicação
if not folder:
    sg.popup_cancel("Cancelando")
    raise SystemExit()

# Imagens suportadas pela biblioteca PIL
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

# Lista de arquivos na pasta selecionada
flist0 = os.listdir(folder)

# Cria uma sublista com arquivos válidos (imagens)
fnames = [f for f in flist0 if os.path.isfile(
    os.path.join(folder, f)) and f.lower().endswith(img_types)]

# Se a lista de arquivos for vazia, fechar aplicação
num_files = len(fnames)
if num_files == 0:
    sg.popup('Nenhum arquivo na pasta')
    raise SystemExit

del flist0

#---------------------------------------------------------------------------------------------
# Usando a biblioteca PIL para obeter uma imagem
# --------------------------------------------------------------------------------------------

def get_img_data(f, maxsize=(640, 360), first=False):

    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

# --------------------------------------------------------------------------------------------

# cria um display de imagem e dois de texto
# exibe as informações do primeiro elemento da lista

filename = os.path.join(folder, fnames[0]) 
image_elem = sg.Image(data=get_img_data(filename, first=True))
filename_display_elem = sg.Text(filename, size=(80, 3))
file_num_display_elem = sg.Text('File 1 of {}'.format(num_files), size=(15, 1))

# define o layout, exibe e ler o formulário



col = [[filename_display_elem],
       [image_elem],
       [sg.Button('Gerar Relatório', size=(16, 2))]]

col_files = [[sg.Listbox(values=fnames, change_submits=True, size=(60, 30), key='listbox')],
             [sg.Button('Prev', size=(8, 2)), sg.Button('Next', size=(8, 2)), file_num_display_elem]]

layout = [[sg.Column(col), sg.Column(col_files)]]

window = sg.Window('Pesquisar Imagem', layout, return_keyboard_events=True,
                   location=(0, 0), use_default_focus=False)

# loop. Ler a entrada do usuário e exibe 
i = 0
while True:
    # ler o formulário
    event, values = window.read()
    print(event, values)

    # captura os eventos do formulário
    if event == sg.WIN_CLOSED:
        break
    elif event in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34', 'Right:39'):
        i += 1
        if i >= num_files:
            i -= num_files
        filename = os.path.join(folder, fnames[i])
    elif event in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33', 'Left:37'):
        i -= 1
        if i < 0:
            i = num_files + i
        filename = os.path.join(folder, fnames[i])
    elif event == 'listbox':            # se algo na lista for selecionado
        f = values["listbox"][0]            # seleciona o nome do arquivo
        filename = os.path.join(folder, f)  # obtém o caminho do arquivo
        i = fnames.index(f)                 # atulizar o índex da página
    
    elif event == 'Gerar Relatório':
        gerar_pdf(folder, fnames)
    
    else:
        filename = os.path.join(folder, fnames[i])

    # atualiza o display com uma nova imagem
    image_elem.update(data=get_img_data(filename, first=True))
    # atualiza o nome do arquivo
    filename_display_elem.update(filename)
    # atualiza o display de páginas
    file_num_display_elem.update('File {} of {}'.format(i+1, num_files))








window.close()
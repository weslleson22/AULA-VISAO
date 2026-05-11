import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# ==========================================================
# 1. LER UMA IMAGEM
# ==========================================================

# Carrega a imagem usando caminho absoluto
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "messi5.jpg")
img = cv.imread(image_path)

# Verifica se a imagem foi carregada corretamente
if img is None:
    print("❌ Erro: Arquivo 'imagem.jpg' não encontrado!")
    print("Por favor, coloque uma imagem chamada 'imagem.jpg' na pasta opencv2")
    print("Ou altere o nome do arquivo no código.")
    exit()

# OpenCV usa BGR, converter para RGB para matplotlib
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# ==========================================================
# 2. PEGAR VALOR DE UM PIXEL
# ==========================================================

# Coordenada do pixel
y, x = 100, 100

# Valor completo do pixel (BGR)
pixel = img[y, x]

print("Valor do pixel [B,G,R]:", pixel)

# Pegando apenas canal azul
blue = img[y, x, 0]

print("Canal Azul:", blue)

# ==========================================================
# 3. TAMANHO DA IMAGEM
# ==========================================================

altura, largura, canais = img.shape

print("\nDimensões da imagem:")
print("Altura :", altura)
print("Largura:", largura)
print("Canais :", canais)

# ==========================================================
# 4. ATRIBUIR VALOR A UM PIXEL
# ==========================================================

# Altera pixel para branco
img[y, x] = [255, 255, 255]

print("\nNovo valor do pixel:")
print(img[y, x])

# ==========================================================
# 5. DEFINIR UMA ROI (REGIÃO DE INTERESSE)
# ==========================================================

# Seleciona uma região da imagem
roi = img[200:350, 200:350]

# Copia ROI para outra região
img[50:200, 50:200] = cv.resize(roi, (150, 150))

# Desenha retângulo indicando ROI original
cv.rectangle(img, (200, 200), (350, 350), (0, 255, 0), 3)

# ==========================================================
# 6. GERENCIAR OS CANAIS DA IMAGEM
# ==========================================================

# Divide os canais
b, g, r = cv.split(img)

# Cria imagens mostrando canais individuais
zeros = np.zeros_like(b)

blue_img = cv.merge([b, zeros, zeros])
green_img = cv.merge([zeros, g, zeros])
red_img = cv.merge([zeros, zeros, r])

# Junta novamente
merged = cv.merge((b, g, r))

# ==========================================================
# EXIBIÇÃO DOS RESULTADOS
# ==========================================================

plt.figure(figsize=(16, 10))

# Imagem original
plt.subplot(2, 3, 1)
plt.imshow(img_rgb)
plt.title("Imagem Original")
plt.axis("off")

# Imagem modificada
plt.subplot(2, 3, 2)
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.title("Imagem Modificada")
plt.axis("off")

# Canal Azul
plt.subplot(2, 3, 3)
plt.imshow(cv.cvtColor(blue_img, cv.COLOR_BGR2RGB))
plt.title("Canal Azul")
plt.axis("off")

# Canal Verde
plt.subplot(2, 3, 4)
plt.imshow(cv.cvtColor(green_img, cv.COLOR_BGR2RGB))
plt.title("Canal Verde")
plt.axis("off")

# Canal Vermelho
plt.subplot(2, 3, 5)
plt.imshow(cv.cvtColor(red_img, cv.COLOR_BGR2RGB))
plt.title("Canal Vermelho")
plt.axis("off")

# Imagem reconstruída
plt.subplot(2, 3, 6)
plt.imshow(cv.cvtColor(merged, cv.COLOR_BGR2RGB))
plt.title("Imagem Reconstruída")
plt.axis("off")

plt.tight_layout()
plt.show()

# ==========================================================
# SALVAR RESULTADO
# ==========================================================

cv.imwrite("resultado_final.jpg", img)

print("\nImagem salva como resultado_final.jpg")
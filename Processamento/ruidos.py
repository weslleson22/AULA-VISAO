import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Tenta carregar a imagem, se não existir cria uma de exemplo
img = cv.imread('opencv-logo-white.png')

if img is None:
    print("Arquivo 'opencv-logo-white.png' não encontrado. Criando imagem de exemplo...")
    # Cria uma imagem de exemplo com logo simulado
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Fundo branco
    img[:] = (255, 255, 255)
    
    # Adiciona formas para simular um logo
    cv.rectangle(img, (150, 100), (450, 300), (0, 0, 255), -1)  # Retângulo vermelho
    cv.circle(img, (300, 200), 80, (255, 0, 0), -1)  # Círculo azul
    cv.ellipse(img, (300, 200), (120, 60), 0, 0, 360, (0, 255, 0), -1)  # Elipse verde
    
    # Adiciona texto "OPENCV"
    cv.putText(img, 'OPENCV', (200, 350), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
    
    # Adiciona ruído para demonstração
    noise = np.random.normal(0, 15, img.shape).astype(np.uint8)
    img = cv.add(img, noise)
    
    # Salva a imagem criada
    cv.imwrite('opencv-logo-white.png', img)
    print("Imagem de exemplo criada e salva como 'opencv-logo-white.png'")

blur = cv.blur(img,(5,5))

# Converte BGR para RGB para exibição correta no matplotlib
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
blur_rgb = cv.cvtColor(blur, cv.COLOR_BGR2RGB)

plt.subplot(121), plt.imshow(img_rgb), plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(122), plt.imshow(blur_rgb), plt.title('Blurred')
plt.xticks([]), plt.yticks([])

plt.show()
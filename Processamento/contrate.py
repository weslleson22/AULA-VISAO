import cv2 as cv
import numpy as np

# Tenta carregar a imagem, se não existir cria uma de exemplo
img = cv.imread('messi5.jpg', cv.IMREAD_GRAYSCALE)

if img is None:
    print("Arquivo 'messi5.jpg' não encontrado. Criando imagem de exemplo...")
    # Cria uma imagem de exemplo com baixo contraste
    img = np.zeros((400, 600), dtype=np.uint8)
    
    # Regiões com diferentes intensidades (baixo contraste)
    img[50:150, 50:200] = 80   # Região escura
    img[50:150, 200:350] = 100 # Região média-escura
    img[50:150, 350:500] = 120 # Região média-clara
    img[150:350, 50:500] = 90  # Região geral escura
    
    # Adiciona alguns detalhes
    cv.rectangle(img, (200, 180), (400, 280), 150, 2)
    cv.circle(img, (300, 230), 40, 140, -1)
    
    # Adiciona ruído sutil
    noise = np.random.normal(0, 5, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Salva a imagem criada
    cv.imwrite('messi5.jpg', img)
    print("Imagem de exemplo criada e salva como 'messi5.jpg'")

equ = cv.equalizeHist(img)

res = np.hstack((img,equ))

cv.imwrite('res.png',res)

print("Processamento concluído!")
print("- Imagem original: messi5.jpg")
print("- Imagem equalizada: res.png (comparação lado a lado)")
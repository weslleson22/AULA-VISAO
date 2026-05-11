"""
===============================================================================
PARTE 1 - CLASSIFICAÇÃO DE IMAGEM
===============================================================================
Este código implementa a classificação de imagens para identificar se a imagem
contém gato, cachorro ou outro animal.

Bibliotecas utilizadas:
- OpenCV: Processamento de imagens e manipulação de arrays
- NumPy: Operações matemáticas e arrays
- TensorFlow/Keras: Modelo de classificação pré-treinado
- Pillow: Manipulação de imagens para compatibilidade com modelos

Autor: Sistema de IA
Data: 11/05/2026
===============================================================================
"""

import cv2 as cv
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import os

def criar_imagem_exemplo():
    """
    Cria uma imagem de exemplo simulando um gato ou cachorro
    quando não há imagem disponível
    """
    print("Criando imagem de exemplo...")
    
    # Cria uma imagem base
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Fundo (ambiente)
    img[:] = (200, 180, 140)  # Cor bege/tierra
    
    # Simula um gato (forma simplificada)
    # Corpo oval
    cv.ellipse(img, (300, 250), (80, 60), 0, 0, 360, (120, 60, 20), -1)
    
    # Cabeça circular
    cv.circle(img, (300, 180), 50, (120, 60, 20), -1)
    
    # Orelhas triangulares (característica de gato)
    pts1 = np.array([[270, 160], [280, 130], [290, 160]], np.int32)
    pts2 = np.array([[310, 160], [320, 130], [330, 160]], np.int32)
    cv.fillPoly(img, [pts1], (120, 60, 20))
    cv.fillPoly(img, [pts2], (120, 60, 20))
    
    # Olhos
    cv.circle(img, (285, 175), 5, (0, 0, 0), -1)
    cv.circle(img, (315, 175), 5, (0, 0, 0), -1)
    
    # Focinho
    cv.ellipse(img, (300, 195), (8, 5), 0, 0, 360, (255, 192, 203), -1)
    
    # Bigodes
    for i in range(3):
        y_pos = 190 + i * 5
        cv.line(img, (270, y_pos), (250, y_pos), (80, 40, 10), 2)
        cv.line(img, (330, y_pos), (350, y_pos), (80, 40, 10), 2)
    
    # Cauda longa (característica de gato)
    pts_tail = np.array([[220, 250], [180, 280], [150, 320], [140, 350]], np.int32)
    cv.polylines(img, [pts_tail], False, (120, 60, 20), 8)
    
    # Salva a imagem
    cv.imwrite('gato_exemplo.jpg', img)
    print("Imagem de exemplo 'gato_exemplo.jpg' criada com sucesso!")
    
    return 'gato_exemplo.jpg'

def classificar_imagem(caminho_imagem):
    """
    Classifica uma imagem usando MobileNetV2 pré-treinado
    
    Args:
        caminho_imagem (str): Caminho para o arquivo de imagem
    
    Returns:
        tuple: (classe_detectada, confianca, imagem_processada)
    """
    
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_imagem):
        print(f"Arquivo '{caminho_imagem}' não encontrado.")
        caminho_imagem = criar_imagem_exemplo()
    
    try:
        # Carrega e processa a imagem para o modelo
        img_pil = image.load_img(caminho_imagem, target_size=(224, 224))
        img_array = image.img_to_array(img_pil)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Carrega o modelo MobileNetV2 pré-treinado
        print("Carregando modelo MobileNetV2...")
        model = MobileNetV2(weights='imagenet')
        
        # Realiza a predição
        print("Realizando classificação...")
        predictions = model.predict(img_array)
        decoded = decode_predictions(predictions, top=3)[0]
        
        # Processa os resultados
        resultados = []
        for i, (imagenet_id, label, score) in enumerate(decoded):
            resultados.append({
                'posicao': i + 1,
                'classe': label,
                'confianca': score * 100,
                'classe_original': label
            })
        
        # Determina a classe principal
        principal = resultados[0]
        
        # Classificação melhorada para gato/cachorro/outro
        classe_detectada = "outro_animal"
        classe_lower = principal['classe_original'].lower()
        
        # Lista de termos para gatos
        termos_gato = ['cat', 'tabby', 'siamese', 'persian', 'egyptian', 'tiger', 'lynx', 'leopard', 'panther']
        # Lista de termos para cachorros
        termos_cachorro = ['dog', 'hound', 'puppy', 'terrier', 'retriever', 'bulldog', 'poodle', 'beagle', 'husky']
        
        if any(term in classe_lower for term in termos_gato):
            classe_detectada = "gato"
        elif any(term in classe_lower for term in termos_cachorro):
            classe_detectada = "cachorro"
        
        # Carrega imagem para exibição com OpenCV
        img_cv = cv.imread(caminho_imagem)
        if img_cv is None:
            raise ValueError("Não foi possível carregar a imagem com OpenCV")
        
        return classe_detectada, principal['confianca'], resultados, img_cv
        
    except Exception as e:
        print(f"Erro na classificação: {e}")
        # Retorna valores padrão em caso de erro
        img_cv = cv.imread(caminho_imagem) or criar_imagem_exemplo()
        return "erro_classificacao", 0.0, [], img_cv

def exibir_resultado(imagem, classe, confianca, resultados):
    """
    Exibe o resultado da classificação com informações detalhadas
    """
    
    # Redimensiona imagem para exibição se necessário
    altura, largura = imagem.shape[:2]
    if largura > 800:
        escala = 800 / largura
        imagem = cv.resize(imagem, (800, int(altura * escala)))
    
    # Adiciona informações na imagem
    font = cv.FONT_HERSHEY_SIMPLEX
    
    # Título principal
    cv.putText(imagem, "CLASSIFICACAO DE IMAGEM", (10, 30), font, 1, (0, 255, 0), 2)
    
    # Resultado principal
    texto_classe = f"Classe: {classe.upper()}"
    texto_confianca = f"Confianca: {confianca:.1f}%"
    
    cv.putText(imagem, texto_classe, (10, 70), font, 0.8, (255, 255, 255), 2)
    cv.putText(imagem, texto_confianca, (10, 100), font, 0.8, (255, 255, 255), 2)
    
    # Top 3 previsões
    cv.putText(imagem, "TOP 3 PREVISOES:", (10, 140), font, 0.6, (0, 255, 255), 1)
    
    for i, resultado in enumerate(resultados[:3]):
        y_pos = 170 + i * 30
        texto = f"{i+1}. {resultado['classe'][:20]}: {resultado['confianca']:.1f}%"
        cv.putText(imagem, texto, (10, y_pos), font, 0.5, (200, 200, 200), 1)
    
    # Adiciona legenda
    cv.putText(imagem, "Pressione qualquer tecla para fechar", (10, imagem.shape[0] - 20), 
              font, 0.5, (100, 100, 100), 1)
    
    # Exibe a imagem
    cv.imshow("Resultado da Classificacao", imagem)
    
    # Salva o resultado
    cv.imwrite('resultado_classificacao.jpg', imagem)
    print("Resultado salvo como 'resultado_classificacao.jpg'")
    
    return imagem

def main():
    """
    Função principal que executa a classificação de imagem
    """
    print("=" * 60)
    print("CLASSIFICACAO DE IMAGEM - DETECCAO DE ANIMAIS")
    print("=" * 60)
    
    # Caminho da imagem (pode ser modificado)
    caminho_imagem = "gatinho1.jpg"
    
    # Se quiser usar outra imagem, descomente a linha abaixo
    # caminho_imagem = "sua_imagem.jpg"
    
    print(f"Processando imagem: {caminho_imagem}")
    
    # Realiza a classificação
    classe, confianca, resultados, imagem = classificar_imagem(caminho_imagem)
    
    # Exibe os resultados no console
    print("\n" + "=" * 40)
    print("RESULTADO DA CLASSIFICACAO:")
    print("=" * 40)
    print(f"Classe detectada: {classe}")
    print(f"Confianca: {confianca:.2f}%")
    print("\nTop 3 previsoes:")
    for resultado in resultados:
        print(f"  {resultado['posicao']}. {resultado['classe']}: {resultado['confianca']:.2f}%")
    
    # Exibe o resultado visualmente
    exibir_resultado(imagem, classe, confianca, resultados)
    
    # Aguarda tecla para fechar
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    print("\nClassificacao concluida!")

if __name__ == "__main__":
    main()

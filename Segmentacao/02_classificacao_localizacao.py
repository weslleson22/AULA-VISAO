"""
===============================================================================
PARTE 2 - CLASSIFICAÇÃO + LOCALIZAÇÃO
===============================================================================
Este código implementa a classificação com localização, detectando um único
objeto principal e desenhando uma bounding box ao redor dele.

Bibliotecas utilizadas:
- OpenCV: Processamento de imagens e desenho de bounding boxes
- NumPy: Operações matemáticas e arrays
- Ultralytics YOLO: Modelo de detecção de objetos pré-treinado
- Pillow: Manipulação de imagens

Funcionalidades:
- Detecção do objeto principal
- Desenho de bounding box vermelha
- Exibição de classe e confiança
- Coordenadas da caixa delimitadora

Autor: Sistema de IA
Data: 11/05/2026
===============================================================================
"""

import cv2 as cv
import numpy as np
from ultralytics import YOLO
import os

def criar_imagem_exemplo_localizacao():
    """
    Cria uma imagem de exemplo com um animal para demonstrar localização
    """
    print("Criando imagem de exemplo para localização...")
    
    # Cria uma imagem base
    img = np.zeros((500, 700, 3), dtype=np.uint8)
    
    # Fundo (ambiente interno)
    img[:] = (240, 230, 220)  # Cor de parede clara
    
    # Adiciona alguns elementos de cena
    # Piso
    cv.rectangle(img, (0, 400), (700, 500), (180, 160, 140), -1)
    
    # Simula um cachorro (forma mais robusta)
    # Corpo retangular (característica de cachorro)
    cv.rectangle(img, (250, 250), (450, 380), (139, 69, 19), -1)
    
    # Cabeça quadrada (característica de cachorro)
    cv.rectangle(img, (220, 180), (320, 260), (139, 69, 19), -1)
    
    # Orelhas caídas (característica de cachorro)
    cv.ellipse(img, (230, 180), (15, 25), -20, 0, 180, (139, 69, 19), -1)
    cv.ellipse(img, (310, 180), (15, 25), 20, 0, 180, (139, 69, 19), -1)
    
    # Focinho mais longo
    cv.rectangle(img, (320, 210), (360, 230), (160, 82, 45), -1)
    
    # Olhos
    cv.circle(img, (260, 210), 8, (0, 0, 0), -1)
    cv.circle(img, (290, 210), 8, (0, 0, 0), -1)
    
    # Nariz
    cv.circle(img, (345, 220), 5, (0, 0, 0), -1)
    
    # Pernas mais robustas
    cv.rectangle(img, (270, 380), (290, 450), (139, 69, 19), -1)
    cv.rectangle(img, (320, 380), (340, 450), (139, 69, 19), -1)
    cv.rectangle(img, (370, 380), (390, 450), (139, 69, 19), -1)
    cv.rectangle(img, (420, 380), (440, 450), (139, 69, 19), -1)
    
    # Cauda curta e enrolada
    cv.ellipse(img, (450, 280), (30, 40), 45, 0, 270, (139, 69, 19), 15)
    
    # Adiciona alguns detalhes na cena
    # Janela
    cv.rectangle(img, (50, 50), (150, 200), (200, 200, 255), 3)
    cv.line(img, (50, 125), (150, 125), (200, 200, 255), 2)
    cv.line(img, (100, 50), (100, 200), (200, 200, 255), 2)
    
    # Porta
    cv.rectangle(img, (550, 200), (680, 480), (150, 75, 0), -1)
    cv.circle(img, (640, 340), 5, (255, 255, 0), -1)
    
    # Salva a imagem
    cv.imwrite('cachorro_localizacao.jpg', img)
    print("Imagem de exemplo 'cachorro_localizacao.jpg' criada com sucesso!")
    
    return 'cachorro_localizacao.jpg'

def detectar_e_localizar(caminho_imagem):
    """
    Detecta e localiza o objeto principal usando YOLO
    
    Args:
        caminho_imagem (str): Caminho para o arquivo de imagem
    
    Returns:
        tuple: (imagem_com_bbox, informacoes_da_detecao)
    """
    
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_imagem):
        print(f"❌ ERRO: Arquivo '{caminho_imagem}' não encontrado!")
        print(f"Por favor, coloque a imagem '{caminho_imagem}' na pasta Segmentacao")
        print("O programa será encerrado.")
        return None, None
    
    try:
        # Carrega a imagem
        img = cv.imread(caminho_imagem)
        if img is None:
            raise ValueError("Não foi possível carregar a imagem")
        
        # Carrega o modelo YOLOv8 pré-treinado
        print("Carregando modelo YOLOv8...")
        model = YOLO('yolov8n.pt')  # Versão nano para melhor performance
        
        # Realiza a detecção
        print("Realizando detecção e localização...")
        results = model(img)
        
        # Processa os resultados
        deteccoes = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None and len(boxes) > 0:
                # Pega a detecção com maior confiança (objeto principal)
                max_conf_idx = 0
                max_conf = 0
                
                for i, box in enumerate(boxes):
                    conf = box.conf[0]
                    if conf > max_conf:
                        max_conf = conf
                        max_conf_idx = i
                
                # Processa a melhor detecção
                box = boxes[max_conf_idx]
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0]
                cls = int(box.cls[0])
                
                # Mapeamento de classes para animais
                nomes_classes = model.names
                nome_classe = nomes_classes[cls]
                
                # Classificação melhorada para gato/cachorro/outro
                classe_simplificada = "outro_animal"
                classe_lower = nome_classe.lower()
                
                # Lista de termos para gatos
                termos_gato = ['cat', 'tabby', 'siamese', 'persian', 'egyptian', 'tiger', 'lynx', 'leopard', 'panther']
                # Lista de termos para cachorros
                termos_cachorro = ['dog', 'hound', 'puppy', 'terrier', 'retriever', 'bulldog', 'poodle', 'beagle', 'husky']
                
                if any(term in classe_lower for term in termos_gato):
                    classe_simplificada = "gato"
                elif any(term in classe_lower for term in termos_cachorro):
                    classe_simplificada = "cachorro"
                
                deteccoes.append({
                    'classe': classe_simplificada,
                    'classe_original': nome_classe,
                    'confianca': float(conf * 100),
                    'coordenadas': {
                        'x1': int(x1),
                        'y1': int(y1),
                        'x2': int(x2),
                        'y2': int(y2),
                        'largura': int(x2 - x1),
                        'altura': int(y2 - y1),
                        'centro_x': int((x1 + x2) / 2),
                        'centro_y': int((y1 + y2) / 2)
                    }
                })
        
        # Se não detectou animais, informa ao usuário
        if not deteccoes:
            print("⚠️ Nenhum animal detectado na imagem.")
            print("Tente usar uma imagem com animais mais visíveis.")
        
        return img, deteccoes
        
    except Exception as e:
        print(f"❌ Erro na detecção: {e}")
        print("Verifique se a imagem é válida e tente novamente.")
        return None, None

def criar_localizacao_simulada(img):
    """
    Cria uma localização simulada quando YOLO não está disponível
    """
    altura, largura = img.shape[:2]
    
    # Define uma bounding box simulada no centro da imagem
    x1 = int(largura * 0.2)
    y1 = int(altura * 0.2)
    x2 = int(largura * 0.8)
    y2 = int(altura * 0.7)
    
    deteccoes = [{
        'classe': 'animal_detectado',
        'classe_original': 'animal',
        'confianca': 85.0,
        'coordenadas': {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'largura': x2 - x1,
            'altura': y2 - y1,
            'centro_x': int((x1 + x2) / 2),
            'centro_y': int((y1 + y2) / 2)
        }
    }]
    
    return deteccoes

def desenhar_bbox_e_informacoes(img, deteccoes):
    """
    Desenha bounding boxes e informações na imagem
    """
    img_resultado = img.copy()
    
    # Desenha a bounding box principal (vermelha)
    if deteccoes:
        deteccao = deteccoes[0]  # Pega a detecção principal
        coords = deteccao['coordenadas']
        
        # Desenha a bounding box vermelha
        cv.rectangle(img_resultado, 
                    (coords['x1'], coords['y1']), 
                    (coords['x2'], coords['y2']), 
                    (0, 0, 255), 3)  # Vermelho, espessura 3
        
        # Prepara o texto do label
        texto_label = f"{deteccao['classe'].upper()}: {deteccao['confianca']:.1f}%"
        
        # Calcula o tamanho do texto para o background
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        
        # Obtém o tamanho do texto
        (text_width, text_height), baseline = cv.getTextSize(texto_label, font, font_scale, thickness)
        
        # Desenha o background do label
        label_x = coords['x1']
        label_y = coords['y1'] - 10  # Um pouco acima da bbox
        
        # Garante que o label não saia da imagem
        if label_y - text_height - baseline < 0:
            label_y = coords['y1'] + text_height + baseline
        
        cv.rectangle(img_resultado,
                    (label_x, label_y - text_height - baseline),
                    (label_x + text_width, label_y + baseline),
                    (0, 0, 255), -1)  # Preenchido
        
        # Desenha o texto
        cv.putText(img_resultado, texto_label, 
                   (label_x, label_y), 
                   font, font_scale, 
                   (255, 255, 255), 
                   thickness)
        
        # Adiciona informações detalhadas
        info_y = coords['y2'] + 30
        
        cv.putText(img_resultado, "COORDENADAS:", 
                   (coords['x1'], info_y), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, 
                   (0, 255, 0), 1)
        
        cv.putText(img_resultado, f"X: {coords['x1']}-{coords['x2']}", 
                   (coords['x1'], info_y + 20), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.4, 
                   (200, 200, 200), 1)
        
        cv.putText(img_resultado, f"Y: {coords['y1']}-{coords['y2']}", 
                   (coords['x1'], info_y + 40), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.4, 
                   (200, 200, 200), 1)
        
        cv.putText(img_resultado, f"Centro: ({coords['centro_x']}, {coords['centro_y']})", 
                   (coords['x1'], info_y + 60), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.4, 
                   (200, 200, 200), 1)
        
        # Adiciona título
        cv.putText(img_resultado, "CLASSIFICACAO + LOCALIZACAO", 
                   (10, 30), 
                   cv.FONT_HERSHEY_SIMPLEX, 1, 
                   (0, 255, 0), 2)
        
        # Adiciona cruz no centro
        centro_x = coords['centro_x']
        centro_y = coords['centro_y']
        cv.drawMarker(img_resultado, (centro_x, centro_y), (0, 255, 255), 
                     cv.MARKER_CROSS, 20, 2)
    
    return img_resultado

def exibir_resultado_localizacao(img_original, img_com_bbox, deteccoes):
    """
    Exibe os resultados da localização
    """
    # Exibe informações no console
    print("\n" + "=" * 50)
    print("RESULTADO DA LOCALIZACAO:")
    print("=" * 50)
    
    if deteccoes:
        deteccao = deteccoes[0]
        coords = deteccao['coordenadas']
        
        print(f"Classe detectada: {deteccao['classe']}")
        print(f"Confianca: {deteccao['confianca']:.2f}%")
        print(f"Classe original: {deteccao['classe_original']}")
        print("\nCoordenadas da Bounding Box:")
        print(f"  X1: {coords['x1']}")
        print(f"  Y1: {coords['y1']}")
        print(f"  X2: {coords['x2']}")
        print(f"  Y2: {coords['y2']}")
        print(f"  Largura: {coords['largura']}")
        print(f"  Altura: {coords['altura']}")
        print(f"  Centro: ({coords['centro_x']}, {coords['centro_y']})")
    
    # Exibe a imagem
    cv.imshow("Classificacao + Localizacao", img_com_bbox)
    
    # Salva o resultado
    cv.imwrite('resultado_localizacao.jpg', img_com_bbox)
    print("\nResultado salvo como 'resultado_localizacao.jpg'")
    
    # Adiciona legenda
    cv.putText(img_com_bbox, "Pressione qualquer tecla para fechar", 
              (10, img_com_bbox.shape[0] - 20), 
              cv.FONT_HERSHEY_SIMPLEX, 0.5, 
              (100, 100, 100), 1)
    
    return img_com_bbox

def main():
    """
    Função principal que executa a classificação com localização
    """
    print("=" * 60)
    print("CLASSIFICACAO + LOCALIZACAO - DETECCAO DE OBJETOS")
    print("=" * 60)
    
    # Caminho da imagem
    caminho_imagem = "obs.jpg"
    
    print(f"Processando imagem: {caminho_imagem}")
    
    # Realiza a detecção e localização
    img_original, deteccoes = detectar_e_localizar(caminho_imagem)
    
    # Verifica se a imagem foi carregada com sucesso
    if img_original is None or deteccoes is None:
        print("\n❌ Falha ao processar a imagem. Verifique se o arquivo existe.")
        return
    
    # Desenha bounding boxes e informações
    img_com_bbox = desenhar_bbox_e_informacoes(img_original, deteccoes)
    
    # Exibe o resultado
    exibir_resultado_localizacao(img_original, img_com_bbox, deteccoes)
    
    # Aguarda tecla para fechar
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    print("\nLocalizacao concluida!")

if __name__ == "__main__":
    main()

"""
===============================================================================
PARTE 3 - DETECÇÃO DE OBJETOS
===============================================================================
Este código implementa a detecção de múltiplos objetos simultaneamente,
desenhando múltiplas bounding boxes e identificando gatos, cachorros e outros.

Bibliotecas utilizadas:
- OpenCV: Processamento de imagens e desenho de bounding boxes
- NumPy: Operações matemáticas e arrays
- Ultralytics YOLO: Modelo de detecção de objetos pré-treinado (YOLOv8)
- Random: Geração de cores aleatórias para diferentes objetos

Funcionalidades:
- Detecção de múltiplos objetos simultaneamente
- Bounding boxes coloridas para cada objeto
- Labels com classe e confiança
- Contagem de objetos detectados
- Diferentes cores para cada tipo de objeto

Autor: Sistema de IA
Data: 11/05/2026
===============================================================================
"""

import cv2 as cv
import numpy as np
from ultralytics import YOLO
import random
import os

def criar_imagem_exemplo_multiplas_deteccoes():
    """
    Cria uma imagem de exemplo com múltiplos animais para demonstrar detecção
    """
    print("Criando imagem de exemplo com múltiplos objetos...")
    
    # Cria uma imagem base maior
    img = np.zeros((600, 800, 3), dtype=np.uint8)
    
    # Fundo (parque/jardim)
    img[:] = (135, 206, 235)  # Céu azul
    cv.rectangle(img, (0, 300), (800, 600), (34, 139, 34), -1)  # Grama verde
    
    # Adiciona elementos de cena
    # Sol
    cv.circle(img, (700, 100), 40, (255, 255, 0), -1)
    
    # Árvore
    cv.rectangle(img, (100, 200), (120, 350), (139, 69, 19), -1)  # Tronco
    cv.circle(img, (110, 180), 50, (0, 128, 0), -1)  # Copa
    
    # Banco
    cv.rectangle(img, (500, 380), (650, 420), (139, 69, 19), -1)
    cv.rectangle(img, (500, 420), (650, 440), (160, 82, 45), -1)
    
    # GATO 1 (em cima do banco)
    # Corpo alongado
    cv.ellipse(img, (575, 360), (40, 20), 0, 0, 360, (255, 140, 0), -1)
    # Cabeça
    cv.circle(img, (540, 350), 20, (255, 140, 0), -1)
    # Orelhas pontudas
    pts1 = np.array([[525, 340], [530, 325], [535, 340]], np.int32)
    pts2 = np.array([[545, 340], [550, 325], [555, 340]], np.int32)
    cv.fillPoly(img, [pts1], (255, 140, 0))
    cv.fillPoly(img, [pts2], (255, 140, 0))
    # Cauda longa
    pts_tail = np.array([[615, 360], [640, 350], [660, 370]], np.int32)
    cv.polylines(img, [pts_tail], False, (255, 140, 0), 8)
    
    # GATO 2 (no chão)
    # Corpo
    cv.ellipse(img, (300, 450), (35, 18), 30, 0, 360, (128, 0, 128), -1)
    # Cabeça
    cv.circle(img, (270, 440), 18, (128, 0, 128), -1)
    # Orelhas
    pts3 = np.array([[255, 430], [260, 415], [265, 430]], np.int32)
    pts4 = np.array([[275, 430], [280, 415], [285, 430]], np.int32)
    cv.fillPoly(img, [pts3], (128, 0, 128))
    cv.fillPoly(img, [pts4], (128, 0, 128))
    
    # CACHORRO 1 (maior, no chão)
    # Corpo robusto
    cv.rectangle(img, (400, 480), (500, 540), (139, 69, 19), -1)
    # Cabeça
    cv.rectangle(img, (380, 450), (430, 490), (139, 69, 19), -1)
    # Orelhas caídas
    cv.ellipse(img, (385, 450), (12, 20), -30, 0, 180, (139, 69, 19), -1)
    cv.ellipse(img, (425, 450), (12, 20), 30, 0, 180, (139, 69, 19), -1)
    # Pernas
    cv.rectangle(img, (410, 540), (425, 570), (139, 69, 19), -1)
    cv.rectangle(img, (440, 540), (455, 570), (139, 69, 19), -1)
    cv.rectangle(img, (470, 540), (485, 570), (139, 69, 19), -1)
    # Cauda curta
    cv.ellipse(img, (500, 500), (20, 15), 45, 0, 180, (139, 69, 19), 12)
    
    # CACHORRO 2 (menor, brincando)
    # Corpo
    cv.ellipse(img, (200, 500), (25, 15), 0, 0, 360, (255, 192, 203), -1)
    # Cabeça
    cv.circle(img, (175, 490), 15, (255, 192, 203), -1)
    # Pernas
    for i, x in enumerate([185, 195, 205, 215]):
        cv.rectangle(img, (x-3, 515), (x+3, 535), (255, 192, 203), -1)
    
    # PÁSSARO (no galho da árvore)
    # Corpo pequeno
    cv.ellipse(img, (110, 160), (8, 6), 0, 0, 360, (0, 0, 0), -1)
    # Cabeça
    cv.circle(img, (118, 158), 4, (0, 0, 0), -1)
    # Asas
    cv.ellipse(img, (105, 160), (12, 3), -20, 0, 180, (0, 0, 0), 2)
    cv.ellipse(img, (115, 160), (12, 3), 20, 0, 180, (0, 0, 0), 2)
    
    # BORBOLETA (voando)
    # Corpo
    cv.line(img, (600, 200), (610, 210), (255, 0, 255), 2)
    # Asas
    cv.ellipse(img, (595, 195), (8, 12), -30, 0, 180, (255, 0, 255), -1)
    cv.ellipse(img, (615, 205), (8, 12), 30, 0, 180, (255, 0, 255), -1)
    cv.ellipse(img, (595, 205), (6, 10), 30, 0, 180, (255, 150, 255), -1)
    cv.ellipse(img, (615, 195), (6, 10), -30, 0, 180, (255, 150, 255), -1)
    
    # Salva a imagem
    cv.imwrite('multiplos_animais.jpg', img)
    print("Imagem de exemplo 'multiplos_animais.jpg' criada com sucesso!")
    
    return 'multiplos_animais.jpg'

def gerar_cor_aleatoria():
    """
    Gera uma cor aleatória vívida para bounding boxes
    """
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

def detectar_multiplos_objetos(caminho_imagem):
    """
    Detecta múltiplos objetos usando YOLOv8
    
    Args:
        caminho_imagem (str): Caminho para o arquivo de imagem
    
    Returns:
        tuple: (imagem_original, lista_de_deteccoes)
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
        
        # Carrega o modelo YOLOv8
        print("Carregando modelo YOLOv8 para detecção múltipla...")
        model = YOLO('yolov8n.pt')
        
        # Realiza a detecção
        print("Detectando múltiplos objetos...")
        results = model(img)
        
        # Processa os resultados
        deteccoes = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Extrai informações da detecção
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    
                    # Obtém o nome da classe
                    nome_classe = model.names[cls]
                    
                    # Filtra apenas animais relevantes
                    classe_filtrada = filtrar_classe_animal(nome_classe)
                    
                    if classe_filtrada and conf > 0.3:  # Confiança mínima
                        deteccoes.append({
                            'classe': classe_filtrada,
                            'classe_original': nome_classe,
                            'confianca': conf * 100,
                            'coordenadas': {
                                'x1': int(x1),
                                'y1': int(y1),
                                'x2': int(x2),
                                'y2': int(y2),
                                'largura': int(x2 - x1),
                                'altura': int(y2 - y1),
                                'centro_x': int((x1 + x2) / 2),
                                'centro_y': int((y1 + y2) / 2)
                            },
                            'cor': gerar_cor_aleatoria()
                        })
        
        # Se não detectou objetos, informa ao usuário
        if len(deteccoes) == 0:
            print("⚠️ Nenhum objeto detectado na imagem.")
            print("Tente usar uma imagem com objetos mais visíveis.")
        
        return img, deteccoes
        
    except Exception as e:
        print(f"❌ Erro na detecção: {e}")
        print("Verifique se a imagem é válida e tente novamente.")
        return None, None

def filtrar_classe_animal(nome_classe):
    """
    Filtra e classifica nomes de classes para animais relevantes
    """
    nome_lower = nome_classe.lower()
    
    # Lista de termos para gatos
    termos_gato = ['cat', 'tabby', 'siamese', 'persian', 'egyptian', 'tiger', 'lynx', 'leopard', 'panther']
    # Lista de termos para cachorros
    termos_cachorro = ['dog', 'hound', 'puppy', 'terrier', 'retriever', 'bulldog', 'poodle', 'beagle', 'husky']
    
    if any(term in nome_lower for term in termos_gato):
        return 'gato'
    elif any(term in nome_lower for term in termos_cachorro):
        return 'cachorro'
    elif 'bird' in nome_lower:
        return 'passaro'
    elif 'butterfly' in nome_lower:
        return 'borboleta'
    elif 'horse' in nome_lower:
        return 'cavalo'
    elif 'cow' in nome_lower:
        return 'vaca'
    elif 'sheep' in nome_lower:
        return 'ovelha'
    elif 'person' in nome_lower:
        return 'pessoa'
    else:
        return None  # Ignora outras classes

def criar_deteccoes_simuladas(img, num_existentes):
    """
    Cria detecções simuladas para demonstração quando YOLO não está disponível
    """
    deteccoes = []
    altura, largura = img.shape[:2]
    
    # Posições simuladas para diferentes animais
    posicoes_simuladas = [
        {'classe': 'gato', 'x': 540, 'y': 350, 'w': 80, 'h': 40},
        {'classe': 'cachorro', 'x': 400, 'y': 450, 'w': 120, 'h': 90},
        {'classe': 'gato', 'x': 270, 'y': 440, 'w': 70, 'h': 35},
        {'classe': 'cachorro', 'x': 175, 'y': 490, 'w': 60, 'h': 45},
        {'classe': 'passaro', 'x': 110, 'y': 160, 'w': 20, 'h': 15},
        {'classe': 'borboleta', 'x': 600, 'y': 200, 'w': 30, 'h': 25}
    ]
    
    # Adiciona apenas as detecções que ainda não existem
    for i, pos in enumerate(posicoes_simuladas[num_existentes:], num_existentes):
        if i >= 6:  # Limite de 6 objetos
            break
            
        deteccoes.append({
            'classe': pos['classe'],
            'classe_original': pos['classe'],
            'confianca': random.uniform(75.0, 95.0),
            'coordenadas': {
                'x1': pos['x'] - pos['w']//2,
                'y1': pos['y'] - pos['h']//2,
                'x2': pos['x'] + pos['w']//2,
                'y2': pos['y'] + pos['h']//2,
                'largura': pos['w'],
                'altura': pos['h'],
                'centro_x': pos['x'],
                'centro_y': pos['y']
            },
            'cor': gerar_cor_aleatoria()
        })
    
    return deteccoes

def desenhar_multiplos_bboxes(img, deteccoes):
    """
    Desenha múltiplas bounding boxes coloridas com informações
    """
    img_resultado = img.copy()
    
    # Contador de objetos por classe
    contagem_classes = {}
    
    for deteccao in deteccoes:
        coords = deteccao['coordenadas']
        cor = deteccao['cor']
        classe = deteccao['classe']
        
        # Atualiza contador
        if classe not in contagem_classes:
            contagem_classes[classe] = 0
        contagem_classes[classe] += 1
        
        # Desenha a bounding box
        cv.rectangle(img_resultado,
                   (coords['x1'], coords['y1']),
                   (coords['x2'], coords['y2']),
                   cor, 3)
        
        # Prepara o texto do label
        texto_label = f"{classe.upper()} #{contagem_classes[classe]}: {deteccao['confianca']:.1f}%"
        
        # Calcula posição do label
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        
        (text_width, text_height), baseline = cv.getTextSize(texto_label, font, font_scale, thickness)
        
        label_x = coords['x1']
        label_y = coords['y1'] - 5
        
        # Garante que o label não saia da imagem
        if label_y - text_height - baseline < 0:
            label_y = coords['y1'] + text_height + baseline + 5
        if label_x + text_width > img.shape[1]:
            label_x = img.shape[1] - text_width - 5
        
        # Desenha background do label
        cv.rectangle(img_resultado,
                   (label_x, label_y - text_height - baseline),
                   (label_x + text_width, label_y + baseline),
                   cor, -1)
        
        # Desenha o texto
        cv.putText(img_resultado, texto_label,
                  (label_x, label_y),
                  font, font_scale,
                  (255, 255, 255),
                  thickness)
        
        # Adiciona marcador no centro
        cv.drawMarker(img_resultado,
                     (coords['centro_x'], coords['centro_y']),
                     (255, 255, 0),
                     cv.MARKER_CROSS, 10, 2)
    
    # Adiciona título e estatísticas
    cv.putText(img_resultado, "DETETCAO DE MULTIPLOS OBJETOS",
              (10, 30),
              cv.FONT_HERSHEY_SIMPLEX, 1,
              (0, 255, 0), 2)
    
    # Adiciona estatísticas
    y_stats = 60
    cv.putText(img_resultado, f"Total de objetos: {len(deteccoes)}",
              (10, y_stats),
              cv.FONT_HERSHEY_SIMPLEX, 0.6,
              (255, 255, 255), 1)
    
    y_stats += 25
    for classe, count in sorted(contagem_classes.items()):
        cv.putText(img_resultado, f"{classe.capitalize()}: {count}",
                  (10, y_stats),
                  cv.FONT_HERSHEY_SIMPLEX, 0.5,
                  (200, 200, 200), 1)
        y_stats += 20
    
    return img_resultado

def exibir_resultado_multiplas_deteccoes(img_original, img_com_bboxes, deteccoes):
    """
    Exibe os resultados da detecção múltipla
    """
    # Exibe informações no console
    print("\n" + "=" * 60)
    print("RESULTADO DA DETECAO MULTIPLA:")
    print("=" * 60)
    
    # Contagem por classe
    contagem = {}
    for deteccao in deteccoes:
        classe = deteccao['classe']
        if classe not in contagem:
            contagem[classe] = 0
        contagem[classe] += 1
    
    print(f"Total de objetos detectados: {len(deteccoes)}")
    print("\nDetalhes das detecções:")
    
    for i, deteccao in enumerate(deteccoes, 1):
        coords = deteccao['coordenadas']
        print(f"\n{i}. {deteccao['classe'].upper()}:")
        print(f"   Confiança: {deteccao['confianca']:.2f}%")
        print(f"   Posição: ({coords['x1']}, {coords['y1']}) - ({coords['x2']}, {coords['y2']})")
        print(f"   Centro: ({coords['centro_x']}, {coords['centro_y']})")
        print(f"   Tamanho: {coords['largura']} x {coords['altura']}")
    
    print(f"\nResumo por classe:")
    for classe, count in sorted(contagem.items()):
        print(f"  {classe.capitalize()}: {count}")
    
    # Exibe a imagem
    cv.imshow("Detecao de Multiplos Objetos", img_com_bboxes)
    
    # Salva o resultado
    cv.imwrite('resultado_multiplas_deteccoes.jpg', img_com_bboxes)
    print("\nResultado salvo como 'resultado_multiplas_deteccoes.jpg'")
    
    # Adiciona legenda
    cv.putText(img_com_bboxes, "Pressione qualquer tecla para fechar",
              (10, img_com_bboxes.shape[0] - 20),
              cv.FONT_HERSHEY_SIMPLEX, 0.5,
              (100, 100, 100), 1)
    
    return img_com_bboxes

def main():
    """
    Função principal que executa a detecção de múltiplos objetos
    """
    print("=" * 60)
    print("DETECAO DE MULTIPLOS OBJETOS - YOLOv8")
    print("=" * 60)
    
    # Caminho da imagem
    caminho_imagem = "obs.jpg"
    
    print(f"Processando imagem: {caminho_imagem}")
    
    # Realiza a detecção múltipla
    img_original, deteccoes = detectar_multiplos_objetos(caminho_imagem)
    
    # Verifica se a imagem foi carregada com sucesso
    if img_original is None or deteccoes is None:
        print("\n❌ Falha ao processar a imagem. Verifique se o arquivo existe.")
        return
    
    # Desenha bounding boxes
    img_com_bboxes = desenhar_multiplos_bboxes(img_original, deteccoes)
    
    # Exibe o resultado
    exibir_resultado_multiplas_deteccoes(img_original, img_com_bboxes, deteccoes)
    
    # Aguarda tecla para fechar
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    print("\nDetecao multipla concluida!")

if __name__ == "__main__":
    main()

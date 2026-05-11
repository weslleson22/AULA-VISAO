"""
===============================================================================
PARTE 4 - SEGMENTAÇÃO DE INSTÂNCIAS
===============================================================================
Este código implementa a segmentação de instâncias, segmentando individualmente
cada objeto com máscaras coloridas e contornos destacados.

Bibliotecas utilizadas:
- OpenCV: Processamento de imagens e desenho de máscaras
- NumPy: Operações matemáticas e arrays
- Ultralytics YOLO: Modelo de segmentação pré-treinado (YOLOv8 Segmentation)
- Random: Geração de cores para diferentes instâncias

Funcionalidades:
- Segmentação individual de cada objeto
- Máscaras coloridas semitransparentes
- Contornos destacados
- Overlay da segmentação na imagem original
- Identificação de cada instância

Autor: Sistema de IA
Data: 11/05/2026
===============================================================================
"""

import cv2 as cv
import numpy as np
from ultralytics import YOLO
import random
import os

def criar_imagem_exemplo_segmentacao():
    """
    Cria uma imagem de exemplo complexa para demonstrar segmentação
    """
    print("Criando imagem de exemplo para segmentação...")
    
    # Cria uma imagem base
    img = np.zeros((700, 900, 3), dtype=np.uint8)
    
    # Fundo (cena diversificada)
    img[:] = (135, 206, 235)  # Céu
    cv.rectangle(img, (0, 400), (900, 700), (34, 139, 34), -1)  # Grama
    
    # Elementos de cena
    # Sol
    cv.circle(img, (800, 100), 50, (255, 255, 0), -1)
    
    # Montanhas ao fundo
    pts_montanha = np.array([[0, 400], [200, 200], [400, 350]], np.int32)
    cv.fillPoly(img, [pts_montanha], (139, 90, 43))
    pts_montanha2 = np.array([[300, 400], [500, 250], [700, 380]], np.int32)
    cv.fillPoly(img, [pts_montanha2], (160, 110, 60))
    
    # Árvores
    for x in [150, 750]:
        cv.rectangle(img, (x-10, 300), (x+10, 400), (101, 67, 33), -1)  # Tronco
        cv.circle(img, (x, 280), 40, (0, 100, 0), -1)  # Copa
    
    # GATO 1 (sentado, proeminente)
    # Corpo principal
    cv.ellipse(img, (300, 500), (45, 35), 0, 0, 360, (255, 140, 0), -1)
    # Cabeça
    cv.circle(img, (300, 450), 30, (255, 140, 0), -1)
    # Orelhas pontudas
    pts1 = np.array([[280, 430], [285, 410], [295, 430]], np.int32)
    pts2 = np.array([[305, 430], [315, 410], [320, 430]], np.int32)
    cv.fillPoly(img, [pts1], (255, 140, 0))
    cv.fillPoly(img, [pts2], (255, 140, 0))
    # Cauda longa e curvada
    pts_tail = np.array([[345, 500], [380, 480], [420, 490], [450, 470]], np.int32)
    cv.polylines(img, [pts_tail], False, (255, 140, 0), 12)
    
    # GATO 2 (deitado)
    cv.ellipse(img, (550, 520), (60, 25), 20, 0, 360, (128, 0, 128), -1)
    cv.circle(img, (510, 510), 22, (128, 0, 128), -1)
    # Orelhas
    pts3 = np.array([[495, 495], [500, 480], [505, 495]], np.int32)
    pts4 = np.array([[515, 495], [520, 480], [525, 495]], np.int32)
    cv.fillPoly(img, [pts3], (128, 0, 128))
    cv.fillPoly(img, [pts4], (128, 0, 128))
    
    # CACHORRO 1 (grande, em pé)
    cv.rectangle(img, (650, 450), (750, 580), (139, 69, 19), -1)  # Corpo
    cv.rectangle(img, (630, 400), (680, 460), (139, 69, 19), -1)  # Cabeça
    # Orelhas caídas
    cv.ellipse(img, (635, 400), (15, 25), -30, 0, 180, (139, 69, 19), -1)
    cv.ellipse(img, (675, 400), (15, 25), 30, 0, 180, (139, 69, 19), -1)
    # Pernas
    for x in [660, 680, 700, 720]:
        cv.rectangle(img, (x-5, 580), (x+5, 620), (139, 69, 19), -1)
    # Cauda
    cv.ellipse(img, (750, 500), (25, 18), 45, 0, 180, (139, 69, 19), 15)
    
    # CACHORRO 2 (pequeno, brincando)
    cv.ellipse(img, (450, 550), (30, 20), 0, 0, 360, (255, 192, 203), -1)
    cv.circle(img, (425, 540), 18, (255, 192, 203), -1)
    # Pernas curtas
    for i, x in enumerate([435, 445, 455, 465]):
        cv.rectangle(img, (x-3, 570), (x+3, 585), (255, 192, 203), -1)
    
    # PÁSSARO 1 (no galho)
    cv.ellipse(img, (150, 280), (10, 7), 0, 0, 360, (0, 0, 0), -1)
    cv.circle(img, (160, 278), 5, (0, 0, 0), -1)
    cv.ellipse(img, (145, 280), (15, 4), -20, 0, 180, (0, 0, 0), 2)
    cv.ellipse(img, (155, 280), (15, 4), 20, 0, 180, (0, 0, 0), 2)
    
    # PÁSSARO 2 (voando)
    cv.ellipse(img, (400, 200), (8, 6), 0, 0, 360, (0, 0, 139), -1)
    cv.circle(img, (408, 198), 4, (0, 0, 139), -1)
    # Asas em movimento
    cv.ellipse(img, (395, 195), (12, 3), -45, 0, 180, (0, 0, 139), 2)
    cv.ellipse(img, (405, 205), (12, 3), 45, 0, 180, (0, 0, 139), 2)
    
    # BORBOLETA 1
    cv.line(img, (250, 350), (260, 360), (255, 0, 255), 2)
    cv.ellipse(img, (240, 345), (10, 15), -30, 0, 180, (255, 0, 255), -1)
    cv.ellipse(img, (260, 355), (10, 15), 30, 0, 180, (255, 0, 255), -1)
    cv.ellipse(img, (240, 355), (7, 12), 30, 0, 180, (255, 150, 255), -1)
    cv.ellipse(img, (260, 345), (7, 12), -30, 0, 180, (255, 150, 255), -1)
    
    # BORBOLETA 2
    cv.line(img, (600, 300), (610, 310), (0, 255, 255), 2)
    cv.ellipse(img, (590, 295), (8, 12), -20, 0, 180, (0, 255, 255), -1)
    cv.ellipse(img, (610, 305), (8, 12), 20, 0, 180, (0, 255, 255), -1)
    
    # Salva a imagem
    cv.imwrite('cena_segmentacao.jpg', img)
    print("Imagem de exemplo 'cena_segmentacao.jpg' criada com sucesso!")
    
    return 'cena_segmentacao.jpg'

def gerar_cor_segmentacao():
    """
    Gera cores vibrantes para segmentação
    """
    cores_vibrantes = [
        (255, 0, 0),    # Vermelho
        (0, 255, 0),    # Verde
        (0, 0, 255),    # Azul
        (255, 255, 0),  # Amarelo
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Ciano
        (255, 128, 0),  # Laranja
        (128, 0, 255),  # Roxo
        (0, 128, 255),  # Azul claro
        (255, 0, 128),  # Rosa
        (128, 255, 0),  # Verde limão
        (0, 255, 128),  # Turquesa
    ]
    return random.choice(cores_vibrantes)

def segmentar_instancias(caminho_imagem):
    """
    Realiza a segmentação de instâncias usando YOLOv8 Segmentation
    
    Args:
        caminho_imagem (str): Caminho para o arquivo de imagem
    
    Returns:
        tuple: (imagem_original, lista_de_segmentacoes)
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
        
        # Carrega o modelo YOLOv8 para segmentação
        print("Carregando modelo YOLOv8 para segmentação...")
        model = YOLO('yolov8n-seg.pt')  # Modelo de segmentação
        
        # Realiza a segmentação
        print("Realizando segmentação de instâncias...")
        results = model(img)
        
        # Processa os resultados
        segmentacoes = []
        
        for result in results:
            if result.masks is not None:
                masks = result.masks.data
                boxes = result.boxes
                
                for i in range(len(masks)):
                    # Extrai máscara
                    mask = masks[i].cpu().numpy()
                    mask = (mask > 0.5).astype(np.uint8) * 255
                    
                    # Extrai informações da caixa
                    if boxes is not None and i < len(boxes):
                        box = boxes[i]
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        
                        # Obtém nome da classe
                        nome_classe = model.names[cls]
                        classe_filtrada = filtrar_classe_animal_segmentacao(nome_classe)
                        
                        if classe_filtrada and conf > 0.3:
                            # Encontra contornos da máscara
                            contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                            
                            segmentacoes.append({
                                'classe': classe_filtrada,
                                'classe_original': nome_classe,
                                'confianca': conf * 100,
                                'mascara': mask,
                                'contornos': contours,
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
                                'cor': gerar_cor_segmentacao()
                            })
        
        # Se não detectou objetos, informa ao usuário
        if len(segmentacoes) == 0:
            print("⚠️ Nenhum objeto detectado na imagem para segmentação.")
            print("Tente usar uma imagem com objetos mais visíveis.")
        
        return img, segmentacoes
        
    except Exception as e:
        print(f"❌ Erro na segmentação: {e}")
        print("Verifique se a imagem é válida e tente novamente.")
        return None, None

def filtrar_classe_animal_segmentacao(nome_classe):
    """
    Filtra classes relevantes para segmentação
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
    elif 'person' in nome_lower:
        return 'pessoa'
    else:
        return None

def criar_segmentacoes_simuladas(img, num_existentes):
    """
    Cria segmentações simuladas para demonstração
    """
    segmentacoes = []
    altura, largura = img.shape[:2]
    
    # Posições simuladas para diferentes animais
    posicoes_simuladas = [
        {'classe': 'gato', 'x': 300, 'y': 450, 'w': 90, 'h': 80, 'forma': 'elipse'},
        {'classe': 'cachorro', 'x': 700, 'y': 450, 'w': 120, 'h': 130, 'forma': 'retangulo'},
        {'classe': 'gato', 'x': 550, 'y': 520, 'w': 80, 'h': 50, 'forma': 'elipse'},
        {'classe': 'cachorro', 'x': 450, 'y': 550, 'w': 60, 'h': 40, 'forma': 'elipse'},
        {'classe': 'passaro', 'x': 150, 'y': 280, 'w': 25, 'h': 20, 'forma': 'elipse'},
        {'classe': 'passaro', 'x': 400, 'y': 200, 'w': 20, 'h': 15, 'forma': 'elipse'},
        {'classe': 'borboleta', 'x': 250, 'y': 350, 'w': 35, 'h': 30, 'forma': 'complexa'},
        {'classe': 'borboleta', 'x': 600, 'y': 300, 'w': 30, 'h': 25, 'forma': 'complexa'}
    ]
    
    # Adiciona apenas as segmentações que ainda não existem
    for i, pos in enumerate(posicoes_simuladas[num_existentes:], num_existentes):
        if i >= 8:  # Limite de 8 objetos
            break
        
        # Cria máscara simulada
        mask = np.zeros((altura, largura), dtype=np.uint8)
        
        if pos['forma'] == 'retangulo':
            cv.rectangle(mask, 
                        (pos['x'] - pos['w']//2, pos['y'] - pos['h']//2),
                        (pos['x'] + pos['w']//2, pos['y'] + pos['h']//2),
                        255, -1)
        elif pos['forma'] == 'elipse':
            cv.ellipse(mask,
                      (pos['x'], pos['y']),
                      (pos['w']//2, pos['h']//2),
                      0, 0, 360, 255, -1)
        else:  # forma complexa
            cv.ellipse(mask,
                      (pos['x'], pos['y']),
                      (pos['w']//2, pos['h']//2),
                      0, 0, 360, 255, -1)
            # Adiciona detalhes para formas complexas
            if 'borboleta' in pos['classe']:
                cv.ellipse(mask,
                          (pos['x'] - 10, pos['y']),
                          (8, 12), -30, 0, 180, 255, -1)
                cv.ellipse(mask,
                          (pos['x'] + 10, pos['y']),
                          (8, 12), 30, 0, 180, 255, -1)
        
        # Encontra contornos
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        segmentacoes.append({
            'classe': pos['classe'],
            'classe_original': pos['classe'],
            'confianca': random.uniform(75.0, 95.0),
            'mascara': mask,
            'contornos': contours,
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
            'cor': gerar_cor_segmentacao()
        })
    
    return segmentacoes

def aplicar_segmentacao_visual(img, segmentacoes):
    """
    Aplica a segmentação visual com máscaras coloridas e contornos
    """
    img_resultado = img.copy()
    
    # Cria overlay para máscaras semitransparentes
    overlay = img.copy()
    
    # Contador de instâncias por classe
    contagem_instancias = {}
    
    for i, segmentacao in enumerate(segmentacoes):
        classe = segmentacao['classe']
        cor = segmentacao['cor']
        mask = segmentacao['mascara']
        contornos = segmentacao['contornos']
        
        # Atualiza contador
        if classe not in contagem_instancias:
            contagem_instancias[classe] = 0
        contagem_instancias[classe] += 1
        
        # Aplica máscara colorida semitransparente
        mask_colored = np.zeros_like(img)
        
        # Garante que a máscara tenha as mesmas dimensões que a imagem
        if mask.shape[:2] != img.shape[:2]:
            # Redimensiona a máscara se necessário
            mask = cv.resize(mask, (img.shape[1], img.shape[0]))
        
        mask_indices = mask > 0
        mask_colored[mask_indices] = cor
        
        # Aplica máscara com transparência de forma segura
        alpha = 0.4  # Transparência da máscara
        
        # Aplica blending de forma mais simples
        # Usa máscara booleana diretamente
        blended_region = cv.addWeighted(overlay, 1 - alpha, mask_colored, alpha, 0)
        
        # Aplica blending apenas onde a máscara está ativa
        overlay[mask_indices] = blended_region[mask_indices]
        
        # Desenha contornos destacados
        for contour in contornos:
            cv.drawContours(img_resultado, [contour], -1, cor, 3)
            cv.drawContours(overlay, [contour], -1, cor, 2)
        
        # Adiciona número da instância
        coords = segmentacao['coordenadas']
        texto_instancia = f"{classe[0].upper()}{contagem_instancias[classe]}"
        
        cv.putText(img_resultado, texto_instancia,
                  (coords['centro_x'] - 15, coords['centro_y']),
                  cv.FONT_HERSHEY_SIMPLEX, 0.8,
                  (255, 255, 255), 2)
        
        cv.putText(img_resultado, texto_instancia,
                  (coords['centro_x'] - 15, coords['centro_y']),
                  cv.FONT_HERSHEY_SIMPLEX, 0.8,
                  cor, 1)
    
    # Combina imagem original com overlay
    img_final = cv.addWeighted(img_resultado, 0.6, overlay, 0.4, 0)
    
    # Adiciona título e informações
    cv.putText(img_final, "SEGMENTACAO DE INSTANCIAS",
              (10, 30),
              cv.FONT_HERSHEY_SIMPLEX, 1,
              (0, 255, 0), 2)
    
    # Adiciona estatísticas
    y_stats = 60
    cv.putText(img_final, f"Total de instâncias: {len(segmentacoes)}",
              (10, y_stats),
              cv.FONT_HERSHEY_SIMPLEX, 0.6,
              (255, 255, 255), 1)
    
    y_stats += 25
    for classe, count in sorted(contagem_instancias.items()):
        cv.putText(img_final, f"{classe.capitalize()}: {count} instância(s)",
                  (10, y_stats),
                  cv.FONT_HERSHEY_SIMPLEX, 0.5,
                  (200, 200, 200), 1)
        y_stats += 20
    
    # Adiciona legenda
    cv.putText(img_final, "Máscaras coloridas + Contornos destacados",
              (10, img_final.shape[0] - 40),
              cv.FONT_HERSHEY_SIMPLEX, 0.5,
              (150, 150, 150), 1)
    
    cv.putText(img_final, "Pressione qualquer tecla para fechar",
              (10, img_final.shape[0] - 20),
              cv.FONT_HERSHEY_SIMPLEX, 0.5,
              (100, 100, 100), 1)
    
    return img_final

def exibir_resultado_segmentacao(img_original, img_segmentada, segmentacoes):
    """
    Exibe os resultados da segmentação
    """
    # Exibe informações no console
    print("\n" + "=" * 60)
    print("RESULTADO DA SEGMENTACAO DE INSTANCIAS:")
    print("=" * 60)
    
    # Contagem por classe
    contagem = {}
    for segmentacao in segmentacoes:
        classe = segmentacao['classe']
        if classe not in contagem:
            contagem[classe] = 0
        contagem[classe] += 1
    
    print(f"Total de instâncias segmentadas: {len(segmentacoes)}")
    print("\nDetalhes das segmentações:")
    
    # Contador global de instâncias
    contador_global = {}
    for i, segmentacao in enumerate(segmentacoes, 1):
        classe = segmentacao['classe']
        coords = segmentacao['coordenadas']
        
        if classe not in contador_global:
            contador_global[classe] = 0
        contador_global[classe] += 1
        
        print(f"\n{i}. {classe.upper()} #{contador_global[classe]}:")
        print(f"   Confiança: {segmentacao['confianca']:.2f}%")
        print(f"   Posição: ({coords['x1']}, {coords['y1']}) - ({coords['x2']}, {coords['y2']})")
        print(f"   Centro: ({coords['centro_x']}, {coords['centro_y']})")
        print(f"   Tamanho: {coords['largura']} x {coords['altura']}")
        print(f"   Pixels segmentados: {np.sum(segmentacao['mascara'] > 0)}")
    
    print(f"\nResumo por classe:")
    for classe, count in sorted(contagem.items()):
        print(f"  {classe.capitalize()}: {count} instância(s)")
    
    # Exibe a imagem
    cv.imshow("Segmentacao de Instancias", img_segmentada)
    
    # Salva o resultado
    cv.imwrite('resultado_segmentacao.jpg', img_segmentada)
    print("\nResultado salvo como 'resultado_segmentacao.jpg'")
    
    return img_segmentada

def main():
    """
    Função principal que executa a segmentação de instâncias
    """
    print("=" * 60)
    print("SEGMENTACAO DE INSTANCIAS - YOLOv8 SEGMENTATION")
    print("=" * 60)
    
    # Caminho da imagem
    caminho_imagem = "obs.jpg"
    
    print(f"Processando imagem: {caminho_imagem}")
    
    # Realiza a segmentação
    img_original, segmentacoes = segmentar_instancias(caminho_imagem)
    
    # Verifica se a imagem foi carregada com sucesso
    if img_original is None or segmentacoes is None:
        print("\n❌ Falha ao processar a imagem. Verifique se o arquivo existe.")
        return
    
    # Aplica a segmentação visual
    img_segmentada = aplicar_segmentacao_visual(img_original, segmentacoes)
    
    # Exibe o resultado
    exibir_resultado_segmentacao(img_original, img_segmentada, segmentacoes)
    
    # Aguarda tecla para fechar
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    print("\nSegmentacao concluida!")

if __name__ == "__main__":
    main()

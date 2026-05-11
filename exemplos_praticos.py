"""
===============================================================================
EXEMPLOS PRÁTICOS - PRÉ-PROCESSAMENTO DE IMAGENS COM OPENCV
===============================================================================
Este arquivo contém exemplos executáveis das técnicas de pré-processamento
explicadas no material didático. Cada função pode ser executada independentemente.

Autor: Sistema de IA
Data: 11/05/2026
Tecnologias: OpenCV, NumPy, Matplotlib
===============================================================================
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time
import os

def criar_imagem_exemplo():
    """Cria uma imagem de exemplo se não houver imagens disponíveis"""
    # Cria uma imagem com diferentes regiões de intensidade
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Região esquerda: escura
    img[100:300, 50:200] = [30, 30, 30]
    
    # Região centro: média
    img[100:300, 200:400] = [128, 128, 128]
    
    # Região direita: clara
    img[100:300, 400:550] = [200, 200, 200]
    
    # Adiciona ruído gaussiano
    noise = np.random.normal(0, 25, img.shape).astype(np.uint8)
    img = cv.add(img, noise)
    
    # Adiciona alguns detalhes
    cv.rectangle(img, (250, 150), (350, 250), (255, 255, 255), 2)
    cv.circle(img, (300, 200), 30, (0, 255, 0), -1)
    
    return img

def exemplo_suavizacao_completo():
    """
    Demonstração completa de técnicas de suavização
    Compara diferentes filtros e seus efeitos
    """
    print("=" * 60)
    print("DEMONSTRAÇÃO: TÉCNICAS DE SUAVIZAÇÃO")
    print("=" * 60)
    
    # Criar ou carregar imagem
    img = criar_imagem_exemplo()
    
    # Aplicar diferentes filtros
    metodos = {
        'Original': img,
        'Média (5x5)': cv.blur(img, (5, 5)),
        'Gaussiano (5x5)': cv.GaussianBlur(img, (5, 5), 0),
        'Mediana (5)': cv.medianBlur(img, 5),
        'Bilateral': cv.bilateralFilter(img, 9, 75, 75)
    }
    
    # Configurar visualização
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('TÉCNICAS DE SUAVIZAÇÃO - COMPARAÇÃO COMPLETA', fontsize=16, fontweight='bold')
    
    # Converter BGR para RGB para matplotlib
    for i, (nome, imagem) in enumerate(metodos.items()):
        if i == 5:  # Pular o último subplot se não houver 6 métodos
            break
            
        row = i // 3
        col = i % 3
        
        if len(imagem.shape) == 3:
            imagem_rgb = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)
            axes[row, col].imshow(imagem_rgb)
        else:
            axes[row, col].imshow(imagem, cmap='gray')
        
        axes[row, col].set_title(f'{nome}\n{imagem.shape}', fontsize=10)
        axes[row, col].axis('off')
    
    # Adicionar análise de ruído
    if len(metodos) > 5:
        # Calcular desvio padrão como medida de ruído
        ruidos = {}
        for nome, imagem in metodos.items():
            if len(imagem.shape) == 3:
                ruidos[nome] = np.std(cv.cvtColor(imagem, cv.COLOR_BGR2GRAY))
            else:
                ruidos[nome] = np.std(imagem)
        
        # Gráfico de barras
        axes[1, 2].bar(ruidos.keys(), ruidos.values())
        axes[1, 2].set_title('Nível de Ruído\n(Desvio Padrão)')
        axes[1, 2].tick_params(axis='x', rotation=45)
        axes[1, 2].set_ylabel('Desvio Padrão')
    
    plt.tight_layout()
    plt.savefig('demo_suavizacao_completa.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Benchmark de performance
    print("\nBENCHMARK DE PERFORMANCE:")
    print("-" * 40)
    
    def benchmark(filtro_func, nome, n_iter=100):
        inicio = time.time()
        for _ in range(n_iter):
            resultado = filtro_func(img)
        fim = time.time()
        tempo_medio = (fim - inicio) / n_iter
        print(f"{nome:15}: {tempo_medio*1000:.2f} ms")
        return tempo_medio
    
    benchmark(lambda x: cv.blur(x, (5, 5)), "Filtro Média")
    benchmark(lambda x: cv.GaussianBlur(x, (5, 5), 0), "Filtro Gaussiano")
    benchmark(lambda x: cv.medianBlur(x, 5), "Filtro Mediana")
    benchmark(lambda x: cv.bilateralFilter(x, 9, 75, 75), "Filtro Bilateral")

def exemplo_contraste_completo():
    """
    Demonstração completa de técnicas de aumento de contraste
    Análise quantitativa e visual
    """
    print("=" * 60)
    print("DEMONSTRAÇÃO: TÉCNICAS DE AUMENTO DE CONTRASTE")
    print("=" * 60)
    
    # Criar imagem com baixo contraste
    img = criar_imagem_exemplo()
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Aplicar diferentes técnicas
    metodos = {
        'Original': img_gray,
        'Equalização': cv.equalizeHist(img_gray),
        'CLAHE': cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(img_gray),
        'Normalização': cv.normalize(img_gray, None, 0, 255, cv.NORM_MINMAX),
        'Linear': cv.convertScaleAbs(img_gray, alpha=1.5, beta=50),
        'Logarítmico': np.uint8(np.log1p(img_gray) * 255 / np.log1p(255))
    }
    
    # Visualização
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('TÉCNICAS DE AUMENTO DE CONTRASTE - COMPARAÇÃO', fontsize=16, fontweight='bold')
    
    for i, (nome, imagem) in enumerate(metodos.items()):
        row = i // 3
        col = i % 3
        
        axes[row, col].imshow(imagem, cmap='gray')
        axes[row, col].set_title(f'{nome}', fontsize=10)
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.savefig('demo_contraste_completo.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Análise quantitativa
    print("\nANÁLISE QUANTITATIVA:")
    print("-" * 40)
    print(f"{'Método':12} {'Contraste':8} {'Média':8} {'Mín':6} {'Máx':6}")
    print("-" * 50)
    
    for nome, imagem in metodos.items():
        contraste = np.std(imagem)
        media = np.mean(imagem)
        min_val = np.min(imagem)
        max_val = np.max(imagem)
        print(f"{nome:12} {contraste:8.2f} {media:8.2f} {min_val:6} {max_val:6}")

def exemplo_histograma_detalhado():
    """
    Análise detalhada de histogramas antes e depois do processamento
    """
    print("=" * 60)
    print("ANÁLISE DETALHADA DE HISTOGRAMAS")
    print("=" * 60)
    
    # Criar imagem com distribuição não uniforme
    img = np.zeros((300, 500), dtype=np.uint8)
    
    # Regiões com diferentes intensidades
    img[50:150, 50:200] = 50   # Região escura
    img[50:150, 200:350] = 100 # Região média-escura
    img[50:150, 350:450] = 150 # Região média-clara
    img[150:250, 50:450] = 200 # Região clara
    
    # Adicionar ruído
    noise = np.random.normal(0, 10, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Processar imagem
    img_equalizada = cv.equalizeHist(img)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img)
    
    # Configurar visualização
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    fig.suptitle('ANÁLISE DE HISTOGRAMAS - COMPARAÇÃO DETALHADA', fontsize=16, fontweight='bold')
    
    imagens = [img, img_equalizada, img_clahe]
    titulos = ['Original', 'Equalização', 'CLAHE']
    
    for i, (imagem, titulo) in enumerate(zip(imagens, titulos)):
        # Imagem
        axes[i, 0].imshow(imagem, cmap='gray')
        axes[i, 0].set_title(f'Imagem {titulo}')
        axes[i, 0].axis('off')
        
        # Histograma
        axes[i, 1].hist(imagem.ravel(), bins=256, alpha=0.7)
        axes[i, 1].set_title(f'Histograma {titulo}')
        axes[i, 1].set_xlabel('Intensidade')
        axes[i, 1].set_ylabel('Frequência')
        axes[i, 1].grid(True, alpha=0.3)
        
        # Histograma acumulado
        hist, bins = np.histogram(imagem.ravel(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * 255 / cdf[-1]
        
        axes[i, 2].plot(cdf_normalized, color='b')
        axes[i, 2].set_title(f'CDF {titulo}')
        axes[i, 2].set_xlabel('Intensidade')
        axes[i, 2].set_ylabel('Frequência Acumulada')
        axes[i, 2].grid(True, alpha=0.3)
        axes[i, 2].set_xlim([0, 255])
        axes[i, 2].set_ylim([0, 255])
    
    plt.tight_layout()
    plt.savefig('demo_histograma_detalhado.png', dpi=150, bbox_inches='tight')
    plt.show()

def exemplo_combinacao_tecnicas():
    """
    Demonstra como combinar múltiplas técnicas para melhor resultado
    """
    print("=" * 60)
    print("COMBINAÇÃO DE TÉCNICAS - PIPELINE COMPLETO")
    print("=" * 60)
    
    # Criar imagem de teste com múltiplos problemas
    img = criar_imagem_exemplo()
    
    # Pipeline de processamento
    print("\nPipeline de Processamento:")
    print("1. Imagem Original")
    print("2. Redução de Ruído (Gaussiano)")
    print("3. Melhoria de Contraste (CLAHE)")
    print("4. Realce de Bordas (Unsharp Mask)")
    
    # Etapa 1: Original
    etapa1 = img.copy()
    
    # Etapa 2: Redução de ruído
    etapa2 = cv.GaussianBlur(etapa1, (5, 5), 0)
    
    # Etapa 3: Melhoria de contraste (aplicar em cada canal)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    b, g, r = cv.split(etapa2)
    b_clahe = clahe.apply(b)
    g_clahe = clahe.apply(g)
    r_clahe = clahe.apply(r)
    etapa3 = cv.merge([b_clahe, g_clahe, r_clahe])
    
    # Etapa 4: Unsharp Mask (realce de bordas)
    gaussian = cv.GaussianBlur(etapa3, (0, 0), 2.0)
    etapa4 = cv.addWeighted(etapa3, 1.5, gaussian, -0.5, 0)
    
    # Visualização do pipeline
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('PIPELINE DE PRÉ-PROCESSAMENTO COMPLETO', fontsize=16, fontweight='bold')
    
    etapas = [etapa1, etapa2, etapa3, etapa4]
    nomes = ['Original', 'Redução de Ruído', 'Melhoria de Contraste', 'Realce Final']
    
    for i, (imagem, nome) in enumerate(zip(etapas, nomes)):
        row = i // 2
        col = i % 2
        
        imagem_rgb = cv.cvtColor(imagem, cv.COLOR_BGR2RGB)
        axes[row, col].imshow(imagem_rgb)
        axes[row, col].set_title(f'{nome}\n{imagem.shape}', fontsize=12)
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.savefig('demo_pipeline_completo.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Análise de melhoria
    print("\nAnálise de Melhoria:")
    print("-" * 40)
    
    def calcular_sharpness(img):
        """Calcula uma medida de nitidez usando variação de Laplaciano"""
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return cv.Laplacian(gray, cv.CV_64F).var()
    
    def calcular_contraste(img):
        """Calcula contraste como desvio padrão"""
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return np.std(gray)
    
    for i, (imagem, nome) in enumerate(zip(etapas, nomes)):
        sharpness = calcular_sharpness(imagem)
        contraste = calcular_contraste(imagem)
        print(f"{nome:20}: Nitidez={sharpness:8.2f} Contraste={contraste:8.2f}")

def benchmark_comparativo():
    """
    Comparação de performance entre diferentes métodos
    """
    print("=" * 60)
    print("BENCHMARK COMPARATIVO DE PERFORMANCE")
    print("=" * 60)
    
    # Criar imagem de teste
    img = criar_imagem_exemplo()
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Funções para benchmark
    funcoes = [
        (lambda x: cv.blur(x, (5, 5)), "Filtro Média"),
        (lambda x: cv.GaussianBlur(x, (5, 5), 0), "Filtro Gaussiano"),
        (lambda x: cv.medianBlur(x, 5), "Filtro Mediana"),
        (lambda x: cv.bilateralFilter(x, 9, 75, 75), "Filtro Bilateral"),
        (lambda x: cv.equalizeHist(x), "Equalização Hist."),
        (lambda x: cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(x), "CLAHE"),
        (lambda x: cv.normalize(x, None, 0, 255, cv.NORM_MINMAX), "Normalização"),
        (lambda x: cv.convertScaleAbs(x, alpha=1.5, beta=50), "Realce Linear")
    ]
    
    print(f"{'Método':20} {'Tempo (ms)':12} {'Memória (KB)':12}")
    print("-" * 50)
    
    for func, nome in funcoes:
        # Benchmark de tempo
        n_iter = 50
        inicio = time.time()
        
        for _ in range(n_iter):
            if nome in ["Equalização Hist.", "CLAHE", "Normalização", "Realce Linear"]:
                resultado = func(img_gray)
            else:
                resultado = func(img)
        
        fim = time.time()
        tempo_ms = (fim - inicio) / n_iter * 1000
        
        # Benchmark de memória
        if nome in ["Equalização Hist.", "CLAHE", "Normalização", "Realce Linear"]:
            memoria_kb = img_gray.nbytes / 1024
        else:
            memoria_kb = img.nbytes / 1024
        
        print(f"{nome:20} {tempo_ms:12.2f} {memoria_kb:12.2f}")

def menu_principal():
    """
    Menu interativo para escolher qual demonstração executar
    """
    while True:
        print("\n" + "=" * 60)
        print("MENU DE DEMONSTRAÇÕES - PRÉ-PROCESSAMENTO DE IMAGENS")
        print("=" * 60)
        print("1. Suavização Completa")
        print("2. Aumento de Contraste Completo")
        print("3. Análise Detalhada de Histogramas")
        print("4. Pipeline Combinado")
        print("5. Benchmark Comparativo")
        print("6. Executar Todas as Demonstrações")
        print("0. Sair")
        print("-" * 60)
        
        try:
            opcao = int(input("Escolha uma opção: "))
            
            if opcao == 0:
                print("Encerrando demonstrações...")
                break
            elif opcao == 1:
                exemplo_suavizacao_completo()
            elif opcao == 2:
                exemplo_contraste_completo()
            elif opcao == 3:
                exemplo_histograma_detalhado()
            elif opcao == 4:
                exemplo_combinacao_tecnicas()
            elif opcao == 5:
                benchmark_comparativo()
            elif opcao == 6:
                print("Executando todas as demonstrações...")
                exemplo_suavizacao_completo()
                exemplo_contraste_completo()
                exemplo_histograma_detalhado()
                exemplo_combinacao_tecnicas()
                benchmark_comparativo()
                print("Todas as demonstrações concluídas!")
            else:
                print("Opção inválida. Tente novamente.")
                
        except ValueError:
            print("Entrada inválida. Digite um número.")
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    print("SISTEMA DE DEMONSTRAÇÃO - PRÉ-PROCESSAMENTO DE IMAGENS")
    print("Este programa demonstra técnicas de pré-processamento com OpenCV")
    print("=" * 60)
    
    # Verificar se matplotlib está disponível
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib disponível para visualização")
    except ImportError:
        print("⚠️ Matplotlib não encontrado. Instale com: pip install matplotlib")
        exit(1)
    
    # Executar menu
    menu_principal()

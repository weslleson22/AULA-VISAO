"""
===============================================================================
VISÃO COMPUTACIONAL COM OPENCV
===============================================================================
Este código demonstra operações básicas de processamento de imagens utilizando
OpenCV (cv2) e NumPy. Cada bloco representa uma funcionalidade fundamental
de visão computacional aplicada à inteligência artificial.

Autor: Sistema de IA
Data: 11/05/2026
Tecnologias: OpenCV, NumPy, Python
===============================================================================
"""

# Importação das bibliotecas necessárias
import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt

# =============================================================================
# BLOCO 1: LER UMA IMAGEM
# =============================================================================
"""
Ler uma imagem do disco utilizando OpenCV.
A função cv.imread() carrega uma imagem de arquivo para uma matriz NumPy.
O formato padrão é BGR (Blue, Green, Red) no OpenCV.
"""

try:
    # Tenta carregar a imagem 'messi5.jpg' do diretório atual
    img = cv.imread('messi5.jpg')
    
    # Verificação de segurança para garantir que a imagem foi carregada
    assert img is not None, "Arquivo não pôde ser lido, verifique com os.path.exists()"
    
    print("✅ Imagem carregada com sucesso!")
    print(f"Dimensões da imagem: {img.shape}")
    
except FileNotFoundError:
    print("⚠️ Arquivo 'messi5.jpg' não encontrado. Criando uma imagem de exemplo...")
    # Cria uma imagem de exemplo caso o arquivo não exista
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    # Adiciona um gradiente simples para visualização
    for i in range(400):
        for j in range(600):
            img[i, j] = [j//3, i//2, (i+j)//4]
    cv.imwrite('messi5.jpg', img)
    print("📁 Imagem de exemplo criada e salva como 'messi5.jpg'")

# =============================================================================
# BLOCO 2: PEGAR VALOR DE UM PIXEL
# =============================================================================
"""
Acessar valores individuais de pixels em uma imagem.
Em OpenCV, os pixels são acessados através de coordenadas [y, x] e canais de cor.
Formato: [linha, coluna, canal] onde canal 0=Azul, 1=Verde, 2=Vermelho (BGR)
"""

print("\n" + "="*60)
print("BLOCO 2: PEGAR VALOR DE UM PIXEL")
print("="*60)

# Acessa o pixel na posição (100, 100) - linha 100, coluna 100
px = img[100, 100]
print(f"Valor completo do pixel [100,100]: {px}")
print(f"Interpretação: Azul={px[0]}, Verde={px[1]}, Vermelho={px[2]}")

# Acessa individualmente cada canal de cor
blue = img[100, 100, 0]  # Canal Azul (índice 0)
green = img[100, 100, 1]  # Canal Verde (índice 1)
red = img[100, 100, 2]    # Canal Vermelho (índice 2)

print(f"Valor do canal Azul: {blue}")
print(f"Valor do canal Verde: {green}")
print(f"Valor do canal Vermelho: {red}")

# =============================================================================
# BLOCO 3: TAMANHO DE UMA IMAGEM
# =============================================================================
"""
Obter informações sobre as dimensões da imagem.
O atributo .shape retorna uma tupla com (altura, largura, canais).
Essas informações são cruciais para processamento e manipulação de imagens.
"""

print("\n" + "="*60)
print("BLOCO 3: TAMANHO DE UMA IMAGEM")
print("="*60)

# Obtém as dimensões da imagem
altura, largura, canais = img.shape
print(f"Dimensões completas (shape): {img.shape}")
print(f"Altura (número de linhas): {altura} pixels")
print(f"Largura (número de colunas): {largura} pixels")
print(f"Número de canais de cor: {canais}")

# Calcula informações adicionais
total_pixels = altura * largura
print(f"Total de pixels: {total_pixels:,}")
print(f"Tamanho em memória: {img.nbytes:,} bytes ({img.nbytes/1024:.2f} KB)")

# =============================================================================
# BLOCO 4: ATRIBUIR VALOR A UM PIXEL
# =============================================================================
"""
Modificar o valor de um pixel específico.
Atribuímos novos valores RGB a um pixel para demonstrar como podemos
manipular individualmente os pontos da imagem.
"""

print("\n" + "="*60)
print("BLOCO 4: ATRIBUIR VALOR A UM PIXEL")
print("="*60)

# Armazena o valor original do pixel
valor_original = img[100, 100].copy()
print(f"Valor original do pixel [100,100]: {valor_original}")

# Atribui um novo valor ao pixel (Branco: [255, 255, 255])
img[100, 100] = [255, 255, 255]
valor_modificado = img[100, 100]
print(f"Valor modificado do pixel [100,100]: {valor_modificado}")

# Demonstra outras cores
img[101, 101] = [255, 0, 0]    # Azul puro
img[102, 102] = [0, 255, 0]    # Verde puro  
img[103, 103] = [0, 0, 255]    # Vermelho puro

print("Pixels modificados:")
print(f"[101,101] - Azul: {img[101, 101]}")
print(f"[102,102] - Verde: {img[102, 102]}")
print(f"[103,103] - Vermelho: {img[103, 103]}")

# =============================================================================
# BLOCO 5: DEFINIR UMA ROI (REGION OF INTEREST)
# =============================================================================
"""
ROI (Region of Interest) é uma região específica da imagem que queremos
processar ou analisar. Aqui demonstramos como extrair e copiar regiões.
"""

print("\n" + "="*60)
print("BLOCO 5: DEFINIR UMA ROI")
print("="*60)

# Define uma região retangular da imagem (slice da matriz)
# Formato: [linha_inicial:linha_final, coluna_inicial:coluna_final]
try:
    # Extrai uma região "bola" da imagem original
    ball = img[280:340, 330:390]
    print(f"Dimensões da ROI 'ball': {ball.shape}")
    
    # Copia a região extraída para outra posição da imagem
    # Isso cria um efeito de "copiar e colar" na imagem
    img[273:333, 100:160] = ball
    
    print("✅ ROI extraída e copiada com sucesso!")
    print("Região [280:340, 330:390] copiada para [273:333, 100:160]")
    
except IndexError:
    print("⚠️ Regiões especificadas estão fora dos limites da imagem")
    print("Usando regiões alternativas...")
    # Usa regiões menores que sempre existirão
    roi_small = img[50:100, 50:100]
    img[150:200, 150:200] = roi_small
    print("ROI alternativa copiada com sucesso!")

# =============================================================================
# BLOCO 6: GERENCIAR OS CANAIS DA IMAGEM
# =============================================================================
"""
Manipulação dos canais de cor BGR (Blue, Green, Red).
Podemos separar os canais para processamento individual e depois
recombiná-los usando as funções split() e merge().
"""

print("\n" + "="*60)
print("BLOCO 6: GERENCIAR OS CANAIS DA IMAGEM")
print("="*60)

# Separa a imagem em seus três canais de cores individuais
b, g, r = cv.split(img)

print(f"Dimensões de cada canal: Azul={b.shape}, Verde={g.shape}, Vermelho={r.shape}")
print(f"Tipo de dado dos canais: {b.dtype}")

# Exibe estatísticas de cada canal
print(f"\nEstatísticas do canal Azul:")
print(f"  Valor mínimo: {b.min()}")
print(f"  Valor máximo: {b.max()}")
print(f"  Valor médio: {b.mean():.2f}")

print(f"\nEstatísticas do canal Verde:")
print(f"  Valor mínimo: {g.min()}")
print(f"  Valor máximo: {g.max()}")
print(f"  Valor médio: {g.mean():.2f}")

print(f"\nEstatísticas do canal Vermelho:")
print(f"  Valor mínimo: {r.min()}")
print(f"  Valor máximo: {r.max()}")
print(f"  Valor médio: {r.mean():.2f}")

# Recombina os canais para reconstruir a imagem original
img_reconstruida = cv.merge((b, g, r))

# Verifica se a reconstrução foi bem-sucedida
if np.array_equal(img, img_reconstruida):
    print("✅ Imagem reconstruída com sucesso a partir dos canais separados!")
else:
    print("⚠️ Pequenas diferenças encontradas na reconstrução")

# =============================================================================
# BLOCO ADICIONAL: VISUALIZAÇÃO E SALVAMENTO
# =============================================================================
"""
Funções adicionais para visualizar e salvar os resultados.
Este bloco demonstra práticas comuns em visão computacional.
"""

print("\n" + "="*60)
print("BLOCO ADICIONAL: VISUALIZAÇÃO E SALVAMENTO")
print("="*60)

# Salva a imagem processada
output_filename = 'imagem_processada.jpg'
cv.imwrite(output_filename, img)
print(f"📁 Imagem processada salva como '{output_filename}'")

# Salva os canais individuais para análise
cv.imwrite('canal_azul.jpg', b)
cv.imwrite('canal_verde.jpg', g)
cv.imwrite('canal_vermelho.jpg', r)

print("📁 Canais individuais salvos:")
print("  - canal_azul.jpg")
print("  - canal_verde.jpg") 
print("  - canal_vermelho.jpg")

# Cria uma visualização combinada dos canais
# Redimensiona para visualização lado a lado
b_resized = cv.resize(b, (200, 150))
g_resized = cv.resize(g, (200, 150))
r_resized = cv.resize(r, (200, 150))

# Combina horizontalmente
combined_channels = np.hstack([b_resized, g_resized, r_resized])
cv.imwrite('canais_combinados.jpg', combined_channels)
print("📁 Visualização combinada dos canais salva como 'canais_combinados.jpg'")

# =============================================================================
# BLOCO FINAL: VISUALIZAÇÃO COM TÍTULOS INFORMATIVOS
# =============================================================================
"""
Visualização dos resultados com títulos explicativos usando matplotlib.
Cada subplot mostra uma etapa do processamento com descrição informativa.
"""

print("\n" + "="*60)
print("BLOCO FINAL: VISUALIZAÇÃO COM TÍTULOS INFORMATIVOS")
print("="*60)

# Converte imagens de BGR para RGB para visualização correta no matplotlib
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_reconstruida_rgb = cv.cvtColor(img_reconstruida, cv.COLOR_BGR2RGB)

# Cria uma figura com múltiplos subplots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('VISÃO COMPUTACIONAL - ANÁLISE COMPLETA DA IMAGEM', fontsize=16, fontweight='bold')

# Subplot 1: Imagem Original
axes[0, 0].imshow(img_rgb)
axes[0, 0].set_title('Imagem Original Processada\n(Com modificações de pixels e ROI)', fontsize=10)
axes[0, 0].axis('off')

# Subplot 2: Canal Azul
axes[0, 1].imshow(b, cmap='Blues_r')
axes[0, 1].set_title('Canal Azul (BGR)\nExtraído usando cv.split()', fontsize=10)
axes[0, 1].axis('off')

# Subplot 3: Canal Verde
axes[0, 2].imshow(g, cmap='Greens_r')
axes[0, 2].set_title('Canal Verde (BGR)\nComponente verde da imagem', fontsize=10)
axes[0, 2].axis('off')

# Subplot 4: Canal Vermelho
axes[1, 0].imshow(r, cmap='Reds_r')
axes[1, 0].set_title('Canal Vermelho (BGR)\nComponente vermelho da imagem', fontsize=10)
axes[1, 0].axis('off')

# Subplot 5: Imagem Reconstruída
axes[1, 1].imshow(img_reconstruida_rgb)
axes[1, 1].set_title('Imagem Reconstruída\n(Recombinada dos canais B,G,R)', fontsize=10)
axes[1, 1].axis('off')

# Subplot 6: Canais Combinados
axes[1, 2].imshow(combined_channels, cmap='gray')
axes[1, 2].set_title('Canais Combinados\n(Azul | Verde | Vermelho)', fontsize=10)
axes[1, 2].axis('off')

# Ajusta o layout
plt.tight_layout()
plt.subplots_adjust(top=0.93)

# Salva a visualização
plt.savefig('analise_completa_visao_computacional.png', dpi=150, bbox_inches='tight')
print("📁 Visualização completa salva como 'analise_completa_visao_computacional.png'")

# Mostra a visualização
plt.show()

print("\n" + "="*60)
print("🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
print("="*60)
print("Resumo das operações realizadas:")
print("✅ 1. Leitura de imagem")
print("✅ 2. Acesso a valores de pixels")
print("✅ 3. Análise de dimensões")
print("✅ 4. Modificação de pixels")
print("✅ 5. Manipulação de ROI")
print("✅ 6. Gerenciamento de canais")
print("✅ 7. Salvamento dos resultados")
print("✅ 8. Visualização com títulos informativos")
print("\nTodos os arquivos foram salvos no diretório atual.")

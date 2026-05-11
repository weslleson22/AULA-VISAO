# PRÉ-PROCESSAMENTO DE IMAGENS COM OPENCV
## Material Didático Completo para Visão Computacional

---

## SUMÁRIO

1. [Introdução ao Pré-Processamento](#introdução)
2. [Suavização de Imagens](#suavizacao)
3. [Aumento de Contraste](#contraste)
4. [Equalização de Histograma](#histograma)
5. [Exemplos Práticos](#exemplos)
6. [Boas Práticas](#boas-praticas)
7. [Exercícios Práticos](#exercicios)

---

<a name="introdução"></a>
## 1. INTRODUÇÃO AO PRÉ-PROCESSAMENTO

O pré-processamento de imagens é uma etapa fundamental em visão computacional que consiste em aplicar técnicas para melhorar a qualidade das imagens antes da análise principal. Essas técnicas ajudam a:

- **Reduzir ruído** indesejado
- **Melhorar o contraste** para facilitar a detecção de features
- **Normalizar** a iluminação
- **Realçar** características importantes

<a name="suavizacao"></a>
## 2. SUAVIZAÇÃO DE IMAGENS

### 2.1 Código Base Explicado Detalhadamente

```python
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Leitura da imagem
img = cv.imread('opencv-logo-white.png')

# Validação da imagem
assert img is not None, "file could not be read, check with os.path.exists()"

# Aplicação do filtro de suavização
blur = cv.blur(img,(5,5))

# Configuração da visualização
plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(122), plt.imshow(blur), plt.title('Blurred')
plt.xticks([]), plt.yticks([])

plt.show()
```

### 2.2 Explicação Linha por Linha

#### Importação das Bibliotecas
```python
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
```

- **`import cv2 as cv`**: Importa a biblioteca OpenCV com alias `cv`. OpenCV é a principal biblioteca para processamento de imagens em Python, oferecendo mais de 2500 algoritmos otimizados.
- **`import numpy as np`**: Importa NumPy para operações matemáticas e manipulação de arrays. Imagens no OpenCV são representadas como arrays NumPy.
- **`from matplotlib import pyplot as plt`**: Importa o módulo pyplot para visualização de imagens e gráficos.

#### Leitura da Imagem
```python
img = cv.imread('opencv-logo-white.png')
```

- **`cv.imread()`**: Função que lê uma imagem do disco.
- **Parâmetros**: 
  - Nome do arquivo
  - Flag de leitura (opcional): `cv.IMREAD_COLOR` (padrão), `cv.IMREAD_GRAYSCALE`, `cv.IMREAD_UNCHANGED`
- **Retorno**: Array NumPy representando a imagem no formato BGR (Blue, Green, Red).

#### Validação da Imagem
```python
assert img is not None, "file could not be read, check with os.path.exists()"
```

- **`assert`**: Declaração que verifica uma condição. Se falsa, levanta uma AssertionError.
- **`img is not None`**: Verifica se a imagem foi carregada com sucesso.
- **Mensagem de erro**: Fornece dica útil para debugging.

#### Funcionamento do cv.blur()
```python
blur = cv.blur(img,(5,5))
```

- **`cv.blur()`**: Aplica um filtro de média (box filter) para suavização.
- **Como funciona**: Cada pixel na imagem de saída é a média dos pixels na vizinhança.
- **Parâmetro `(5,5)`**: Tamanho do kernel (janela de convolução).

#### Significado do (5,5)
- **Kernel 5×5**: Matriz 5x5 que desliza sobre a imagem
- **Cálculo**: Para cada pixel, calcula a média de 25 pixels (5×5)
- **Efeito**: Remove ruído de alta frequência, mas pode borrificar bordas
- **Regra geral**: Kernel ímpar para simetria, maior kernel = mais suavização

#### Funcionamento do subplot
```python
plt.subplot(121), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(122), plt.imshow(blur), plt.title('Blurred')
plt.xticks([]), plt.yticks([])
```

- **`plt.subplot(121)`**: Cria grade 1×2, seleciona primeira posição
- **`plt.subplot(122)`**: Cria grade 1×2, seleciona segunda posição
- **`plt.imshow()`**: Exibe a imagem
- **`plt.title()`**: Adiciona título
- **`plt.xticks([]), plt.yticks([])`**: Remove marcações dos eixos

#### Exibição das Imagens
```python
plt.show()
```

- **`plt.show()`**: Exibe a janela com as imagens
- **Bloqueante**: Mantém o programa aberto até fechar a janela

### 2.3 Comparação: Original vs Borrada

| Característica | Imagem Original | Imagem Borrada |
|----------------|-----------------|----------------|
| **Detalhes** | Nítidos, bordas definidas | Suavizados, bordas atenuadas |
| **Ruído** | Preservado | Reduzido/eliminado |
| **Contraste Local** | Alto | Reduzido |
| **Aplicação** | Análise de features | Pré-processamento |

<a name="contraste"></a>
## 3. AUMENTO DE CONTRASTE

### 3.1 Equalização do Histograma

#### Conceito
A equalização de histograma distribui uniformemente os intensidades dos pixels em toda a faixa dinâmica (0-255), melhorando o contraste global da imagem.

#### Funcionamento Matemático
1. Calcular o histograma da imagem
2. Calcular a função de distribuição cumulativa (CDF)
3. Mapear os valores originais usando a CDF normalizada

#### Aplicações Práticas
- **Imagens médicas**: Melhorar visualização de tecidos
- **Fotografia**: Corrigir subexposição/superexposição
- **Processamento industrial**: Detecção de defeitos

#### Vantagens
- Automática, não requer parâmetros
- Melhora contraste global
- Implementação eficiente

#### Limitações
- Pode ampliar ruído
- Não preserva detalhes locais
- Pode criar aparência não natural

### 3.2 CLAHE (Contrast Limited Adaptive Histogram Equalization)

#### Conceito
CLAHE é uma versão aprimorada da equalização que opera em pequenas regiões (tiles) e limita o contraste para evitar amplificação excessiva de ruído.

#### Funcionamento
1. Divide imagem em tiles (ex: 8×8)
2. Equaliza histograma de cada tile
3. Limita o contraste (clip limit)
4. Interpola entre tiles para evitar bordas

#### Aplicações Práticas
- **Imagens de satélite**: Melhorar detalhes terrestres
- **Imagens de segurança**: Face detection em baixa iluminação
- **Microscopia**: Realce de estruturas celulares

#### Vantagens
- Preserva detalhes locais
- Controla amplificação de ruído
- Adaptativo a diferentes regiões

#### Parâmetros Importantes
- **Clip Limit**: Limite de contraste (típico: 2.0-4.0)
- **Tile Grid Size**: Tamanho dos tiles (típico: 8×8)

### 3.3 Normalização de Contraste

#### Conceito
Normalização mapeia os valores de pixels para uma faixa específica, geralmente [0, 255] ou [0, 1].

#### Fórmulas
- **Min-Max**: `new_pixel = (pixel - min) * 255 / (max - min)`
- **Z-Score**: `new_pixel = (pixel - mean) / std_dev`

#### Aplicações
- **Padronização**: Para algoritmos de ML
- **Visualização**: Para melhor percepção humana
- **Comparação**: Para imagens de diferentes fontes

### 3.4 Realce Linear

#### Conceito
Aplica uma transformação linear aos valores de pixels: `y = ax + b`

#### Parâmetros
- **a (slope)**: Controla o contraste
- **b (intercept)**: Controla o brilho

#### Aplicações
- **Ajuste fino**: Correções específicas
- **Calibração**: Para sistemas de imagem
- **Arte digital**: Efeitos criativos

### 3.5 Realce Quadrático

#### Conceito
Usa função quadrática: `y = ax² + bx + c`

#### Características
- **Não linear**: Realça diferentes faixas diferentemente
- **Flexível**: Permite curvas complexas
- **Seletivo**: Pode realçar apenas certas regiões

#### Aplicações
- **Fotografia HDR**: High Dynamic Range
- **Processamento científico**: Realce de faixas específicas
- **Arte**: Efeitos dramáticos

### 3.6 Realce Logarítmico

#### Conceito
Aplica transformação logarítmica: `y = a * log(1 + x)`

#### Características
- **Compressão dinâmica**: Reduz grandes variações
- **Realce de escuros**: Melhora detalhes em áreas escuras
- **Percepção humana**: Similar à visão humana

#### Aplicações
- **Imagens astronômicas**: Estrelas e nebulosas
- **Imagens médicas**: Raios-X, ressonância
- **Imagens de infravermelho**: Thermal imaging

<a name="histograma"></a>
## 4. EQUALIZAÇÃO DE HISTOGRAMA - CÓDIGO DETALHADO

### 4.1 Código Base
```python
img = cv.imread('wiki.jpg', cv.IMREAD_GRAYSCALE)

assert img is not None, "file could not be read, check with os.path.exists()"

equ = cv.equalizeHist(img)

res = np.hstack((img,equ))

cv.imwrite('res.png',res)
```

### 4.2 Explicação Linha por Linha

#### Leitura em Escala de Cinza
```python
img = cv.imread('wiki.jpg', cv.IMREAD_GRAYSCALE)
```

- **`cv.IMREAD_GRAYSCALE`**: Flag que força leitura em tons de cinza
- **Vantagens**: 
  - Reduz complexidade (1 canal vs 3)
  - Processamento mais rápido
  - Foco em intensidade luminosa
- **Formato**: Array 2D com valores 0-255

#### Validação
```python
assert img is not None, "file could not be read, check with os.path.exists()"
```
- **Segurança**: Evita erros em operações subsequentes
- **Debugging**: Mensagem clara do problema

#### O que é Histograma?
- **Definição**: Gráfico de frequência dos valores de pixels
- **Eixo X**: Valores de intensidade (0-255)
- **Eixo Y**: Frequência/quantidade de pixels
- **Informação**: Distribuição de luminosidade da imagem

#### Funcionamento da Equalização
```python
equ = cv.equalizeHist(img)
```

- **`cv.equalizeHist()`**: Implementação OpenCV da equalização
- **Processo Interno**:
  1. Calcula histograma acumulado
  2. Normaliza para [0, 255]
  3. Aplica mapeamento a cada pixel
- **Complexidade**: O(N) onde N = número de pixels

#### Como o Contraste é Melhorado
- **Distribuição uniforme**: Espalha valores por toda faixa
- **Expansão dinâmica**: Usa full range [0, 255]
- **Detalhes ocultos**: Revela informações em faixas pouco utilizadas

#### Funcionamento do np.hstack
```python
res = np.hstack((img,equ))
```

- **`np.hstack()`**: Concatena arrays horizontalmente
- **Parâmetro**: Tupla com arrays a serem concatenados
- **Resultado**: Array único com as imagens lado a lado
- **Dimensões**: (altura, largura_original + largura_equalizada)

#### Salvamento com cv.imwrite
```python
cv.imwrite('res.png',res)
```

- **`cv.imwrite()`**: Salva array NumPy como arquivo de imagem
- **Parâmetros**: 
  - Nome do arquivo
  - Array da imagem
- **Formato**: Determinado pela extensão (.png, .jpg, etc.)
- **Retorno**: True se sucesso, False se falha

<a name="exemplos"></a>
## 5. EXEMPLOS PRÁTICOS

### 5.1 Exemplo Completo de Suavização
```python
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def demonstrar_suavizacao():
    """Demonstra diferentes técnicas de suavização"""
    
    # Carregar imagem
    img = cv.imread('lena.jpg')
    assert img is not None, "Imagem não encontrada"
    
    # Converter para RGB (matplotlib usa RGB)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    # Aplicar diferentes filtros
    blur_avg = cv.blur(img_rgb, (5, 5))           # Filtro da média
    blur_gauss = cv.GaussianBlur(img_rgb, (5, 5), 0)  # Filtro gaussiano
    blur_median = cv.medianBlur(img_rgb, 5)       # Filtro mediana
    blur_bilateral = cv.bilateralFilter(img_rgb, 9, 75, 75)  # Filtro bilateral
    
    # Visualização
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('TÉCNICAS DE SUAVIZAÇÃO', fontsize=16, fontweight='bold')
    
    # Imagem original
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title('Original\n(Sem suavização)')
    axes[0, 0].axis('off')
    
    # Filtro da média
    axes[0, 1].imshow(blur_avg)
    axes[0, 1].set_title('Filtro da Média\n(5x5 kernel)')
    axes[0, 1].axis('off')
    
    # Filtro gaussiano
    axes[0, 2].imshow(blur_gauss)
    axes[0, 2].set_title('Filtro Gaussiano\n(σ=0, auto)')
    axes[0, 2].axis('off')
    
    # Filtro mediana
    axes[1, 0].imshow(blur_median)
    axes[1, 0].set_title('Filtro Mediana\n(Kernel 5)')
    axes[1, 0].axis('off')
    
    # Filtro bilateral
    axes[1, 1].imshow(blur_bilateral)
    axes[1, 1].set_title('Filtro Bilateral\n(Preserva bordas)')
    axes[1, 1].axis('off')
    
    # Comparação de histogramas
    axes[1, 2].hist(img_rgb.ravel(), bins=256, alpha=0.5, label='Original')
    axes[1, 2].hist(blur_avg.ravel(), bins=256, alpha=0.5, label='Suavizada')
    axes[1, 2].set_title('Comparação de Histogramas')
    axes[1, 2].legend()
    axes[1, 2].set_xlabel('Intensidade')
    axes[1, 2].set_ylabel('Frequência')
    
    plt.tight_layout()
    plt.savefig('comparacao_suavizacao.png', dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    demonstrar_suavizacao()
```

### 5.2 Exemplo Completo de Contraste
```python
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def demonstrar_contraste():
    """Demonstra diferentes técnicas de aumento de contraste"""
    
    # Carregar imagem em escala de cinza
    img = cv.imread('low_contrast.jpg', cv.IMREAD_GRAYSCALE)
    assert img is not None, "Imagem não encontrada"
    
    # Equalização de histograma tradicional
    equ = cv.equalizeHist(img)
    
    # CLAHE
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(img)
    
    # Normalização Min-Max
    norm = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX)
    
    # Realce linear
    alpha = 1.5  # Contraste
    beta = 50    # Brilho
    linear = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
    
    # Realce logarítmico
    log = np.uint8(np.log1p(img) * 255 / np.log1p(255))
    
    # Visualização
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('TÉCNICAS DE AUMENTO DE CONTRASTE', fontsize=16, fontweight='bold')
    
    # Imagem original
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title('Original\n(Baixo contraste)')
    axes[0, 0].axis('off')
    
    # Equalização tradicional
    axes[0, 1].imshow(equ, cmap='gray')
    axes[0, 1].set_title('Equalização\n(Histograma)')
    axes[0, 1].axis('off')
    
    # CLAHE
    axes[0, 2].imshow(clahe_img, cmap='gray')
    axes[0, 2].set_title('CLAHE\n(Adaptativo)')
    axes[0, 2].axis('off')
    
    # Normalização
    axes[1, 0].imshow(norm, cmap='gray')
    axes[1, 0].set_title('Normalização\n(Min-Max)')
    axes[1, 0].axis('off')
    
    # Realce linear
    axes[1, 1].imshow(linear, cmap='gray')
    axes[1, 1].set_title(f'Realce Linear\n(α={alpha}, β={beta})')
    axes[1, 1].axis('off')
    
    # Realce logarítmico
    axes[1, 2].imshow(log, cmap='gray')
    axes[1, 2].set_title('Realce\n(Logarítmico)')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('comparacao_contraste.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Análise quantitativa
    print("\nANÁLISE QUANTITATIVA DO CONTRASTE:")
    print("=" * 50)
    
    def calcular_contraste(imagem):
        """Calcula o desvio padrão como medida de contraste"""
        return np.std(imagem)
    
    metodos = ['Original', 'Equalização', 'CLAHE', 'Normalização', 'Linear', 'Log']
    contrastes = [
        calcular_contraste(img),
        calcular_contraste(equ),
        calcular_contraste(clahe_img),
        calcular_contraste(norm),
        calcular_contraste(linear),
        calcular_contraste(log)
    ]
    
    for metodo, contraste in zip(metodos, contrastes):
        print(f"{metodo:12}: {contraste:.2f}")

if __name__ == "__main__":
    demonstrar_contraste()
```

<a name="boas-praticas"></a>
## 6. BOAS PRÁTICAS

### 6.1 Organização do Código

#### Estrutura Recomendada
```python
"""
Módulo: pré_processamento.py
Descrição: Funções para pré-processamento de imagens
Autor: [Seu Nome]
Data: [Data Atual]
"""

import cv2 as cv
import numpy as np

def carregar_imagem(caminho, escala_cinza=False):
    """Carrega imagem com validação e tratamento de erros"""
    flag = cv.IMREAD_GRAYSCALE if escala_cinza else cv.IMREAD_COLOR
    img = cv.imread(caminho, flag)
    
    if img is None:
        raise FileNotFoundError(f"Imagem não encontrada: {caminho}")
    
    return img

def aplicar_suavizacao(img, metodo='gaussiano', kernel_size=5):
    """Aplica diferentes métodos de suavização"""
    if metodo == 'media':
        return cv.blur(img, (kernel_size, kernel_size))
    elif metodo == 'gaussiano':
        return cv.GaussianBlur(img, (kernel_size, kernel_size), 0)
    elif metodo == 'mediana':
        return cv.medianBlur(img, kernel_size)
    else:
        raise ValueError(f"Método desconhecido: {metodo}")
```

### 6.2 Tratamento de Erros

#### Validações Essenciais
```python
def processar_imagem_seguro(caminho_entrada, caminho_saida):
    """Processamento robusto com tratamento de erros"""
    try:
        # Validação de entrada
        img = carregar_imagem(caminho_entrada)
        
        # Validação de dimensões
        if img.size == 0:
            raise ValueError("Imagem vazia")
        
        # Processamento
        resultado = cv.GaussianBlur(img, (5, 5), 0)
        
        # Validação de saída
        if not cv.imwrite(caminho_saida, resultado):
            raise IOError(f"Falha ao salvar: {caminho_saida}")
            
        return True
        
    except Exception as e:
        print(f"Erro no processamento: {e}")
        return False
```

### 6.3 Escolha Correta de Filtros

#### Guia de Seleção
| Situação | Filtro Recomendado | Razão |
|----------|-------------------|-------|
| Ruído gaussiano | Filtro gaussiano | Modela ruído adequadamente |
| Ruído impulso | Filtro mediana | Remove outliers |
| Preservar bordas | Filtro bilateral | Suaviza mantendo bordas |
| Processamento rápido | Filtro da média | Menor custo computacional |

### 6.4 Impacto na Performance

#### Otimizações
```python
# Usar tipos de dados adequados
img_uint8 = img.astype(np.uint8)  # Mais eficiente que float64

# Evitar cópias desnecessárias
img_processada = img  # Referência, não cópia

# Processar em lote
def processar_lote(lista_imagens):
    """Processa múltiplas imagens eficientemente"""
    resultados = []
    for img in lista_imagens:
        # Operações vetorizadas quando possível
        resultado = cv.GaussianBlur(img, (5, 5), 0)
        resultados.append(resultado)
    return resultados
```

#### Medição de Performance
```python
import time

def benchmark_processamento(img, n_iteracoes=100):
    """Mede tempo de processamento"""
    inicio = time.time()
    
    for _ in range(n_iteracoes):
        resultado = cv.GaussianBlur(img, (5, 5), 0)
    
    fim = time.time()
    tempo_medio = (fim - inicio) / n_iteracoes
    
    print(f"Tempo médio por processamento: {tempo_medio*1000:.2f} ms")
    return tempo_medio
```

<a name="exercicios"></a>
## 7. EXERCÍCIOS PRÁTICOS

### 7.1 Exercícios Fundamentais

#### Exercício 1: Filtro da Média
**Objetivo**: Implementar filtro da média manualmente

```python
def filtro_media_manual(img, kernel_size=3):
    """
    Implemente manualmente o filtro da média
    Dicas:
    - Use loops aninhados para percorrer pixels
    - Calcule a média da vizinhança
    - Trate bordas adequadamente
    """
    # TODO: Implementar
    pass
```

#### Exercício 2: Filtro Gaussiano
**Objetivo**: Criar kernel gaussiano e aplicar convolução

```python
def criar_kernel_gaussiano(size, sigma=1.0):
    """
    Crie um kernel gaussiano 2D
    Fórmula: G(x,y) = (1/(2πσ²)) * exp(-(x²+y²)/(2σ²))
    """
    # TODO: Implementar
    pass

def aplicar_convolucao(img, kernel):
    """
    Aplique convolução manualmente
    """
    # TODO: Implementar
    pass
```

#### Exercício 3: Filtro Bilateral
**Objetivo**: Implementar filtro bilateral simplificado

```python
def filtro_bilateral_simplificado(img, d=5, sigma_color=75, sigma_space=75):
    """
    Implemente versão simplificada do filtro bilateral
    Considere apenas uma pequena janela para praticidade
    """
    # TODO: Implementar
    pass
```

#### Exercício 4: Equalização de Histograma
**Objetivo**: Implementar equalização manualmente

```python
def equalizar_histograma_manual(img):
    """
    Implemente equalização de histograma passo a passo:
    1. Calcular histograma
    2. Calcular CDF
    3. Normalizar e aplicar mapeamento
    """
    # TODO: Implementar
    pass
```

#### Exercício 5: CLAHE
**Objetivo**: Implementar CLAHE básico

```python
def clahe_simplificado(img, tile_size=8, clip_limit=2.0):
    """
    Implemente versão simplificada do CLAHE
    Divida a imagem em tiles e processe individualmente
    """
    # TODO: Implementar
    pass
```

### 7.2 Desafios Extras

#### Desafio 1: Comparação Automática
**Objetivo**: Criar sistema que compara automaticamente diferentes métodos

```python
def comparar_metodos_imagem(img_path):
    """
    Compare todos os métodos vistos e gere um relatório:
    - Métricas de qualidade (PSNR, SSIM)
    - Tempo de processamento
    - Visualização comparativa
    """
    # TODO: Implementar
    pass
```

#### Desafio 2: Otimização Adaptativa
**Objetivo**: Criar sistema que escolhe melhor método automaticamente

```python
def escolher_metodo_automatico(img):
    """
    Analise a imagem e escolha o melhor método:
    - Detecte tipo de ruído
    - Meça o contraste atual
    - Recomende o método adequado
    """
    # TODO: Implementar
    pass
```

#### Desafio 3: Processamento em Tempo Real
**Objetivo**: Implementar processamento para vídeo em tempo real

```python
def processar_video_realtime(video_path):
    """
    Aplique pré-processamento em vídeo:
    - Processamento frame a frame
    - Mantenha FPS adequado
    - Permita ajuste de parâmetros em tempo real
    """
    # TODO: Implementar
    pass
```

### 7.3 Critérios de Avaliação

#### Para Exercícios Fundamentais:
- **Funcionalidade**: Código funciona corretamente
- **Eficiência**: Uso adequado de operações vetorizadas
- **Robustez**: Tratamento de casos extremos
- **Documentação**: Comentários explicativos

#### Para Desafios Extras:
- **Inovação**: Abordagens criativas
- **Performance**: Otimizações implementadas
- **Usabilidade**: Interface amigável
- **Completude**: Funcionalidades extras

---

## CONCLUSÃO

Este material cobre os fundamentos essenciais do pré-processamento de imagens com OpenCV, desde conceitos teóricos até implementações práticas. Os alunos devem praticar os exercícios para desenvolver intuição sobre quando e como aplicar cada técnica.

**Próximos Passos Recomendados:**
1. Praticar com diferentes tipos de imagens
2. Experimentar combinações de técnicas
3. Desenvolver projetos aplicativos
4. Explorar técnicas avançadas de processamento

**Recursos Adicionais:**
- Documentação OpenCV: https://docs.opencv.org/
- Scikit-image: https://scikit-image.org/
- Livro: "Digital Image Processing" - Gonzalez & Woods

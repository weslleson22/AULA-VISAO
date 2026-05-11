# PROJETO DE SEGMENTAÇÃO DE IMAGENS E DETECÇÃO DE OBJETOS

## Descrição do Projeto

Este projeto implementa quatro técnicas fundamentais de Visão Computacional utilizando Python, OpenCV e modelos de deep learning:

1. **Classificação de Imagem** - Identifica o objeto principal (gato, cachorro, outro)
2. **Classificação + Localização** - Detecta objeto com bounding box
3. **Detecção de Objetos** - Detecta múltiplos objetos simultaneamente
4. **Segmentação de Instâncias** - Segmenta individualmente cada objeto com máscaras

## Estrutura do Projeto

```
Segmentacao/
├── 01_classificacao_imagem.py      # Classificação simples
├── 02_classificacao_localizacao.py  # Classificação + bounding box
├── 03_detecacao_objetos.py          # Detecção múltipla
├── 04_segmentacao_instancias.py     # Segmentação com máscaras
├── requirements.txt                 # Dependências
└── README.md                        # Este arquivo
```

## Instalação

### 1. Clonar/Download do Projeto
Copie todos os arquivos para uma pasta local.

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Instalação Manual (Opcional)
Se preferir instalar manualmente:
```bash
pip install opencv-python numpy tensorflow torch ultralytics Pillow matplotlib
```

## Como Usar

### Executar Individualmente Cada Parte

#### Parte 1: Classificação de Imagem
```bash
python 01_classificacao_imagem.py
```
- Classifica se a imagem contém gato, cachorro ou outro animal
- Exibe confiança e top 3 previsões
- Cria imagem automática se não encontrar arquivo

#### Parte 2: Classificação + Localização
```bash
python 02_classificacao_localizacao.py
```
- Detecta objeto principal com bounding box vermelha
- Mostra coordenadas e confiança
- Localização precisa do objeto

#### Parte 3: Detecção de Objetos
```bash
python 03_detecacao_objetos.py
```
- Detecta múltiplos objetos simultaneamente
- Bounding boxes coloridas para cada objeto
- Contagem e identificação de todos os animais

#### Parte 4: Segmentação de Instâncias
```bash
python 04_segmentacao_instancias.py
```
- Segmentação individual com máscaras coloridas
- Contornos destacados
- Overlay semitransparente
- Identificação de cada instância

## Usar Próprias Imagens

Para usar suas próprias imagens, modifique a variável `caminho_imagem` em cada arquivo:

```python
# Substitua esta linha
caminho_imagem = "gato_exemplo.jpg"

# Por esta (com seu arquivo)
caminho_imagem = "minha_imagem.jpg"
```

## Modelos Utilizados

### YOLOv8 (Ultralytics)
- **yolov8n.pt**: Modelo nano para detecção rápida
- **yolov8n-seg.pt**: Modelo para segmentação de instâncias
- Download automático na primeira execução

### MobileNetV2 (TensorFlow/Keras)
- Modelo pré-treinado no ImageNet
- Para classificação de imagem
- Download automático na primeira execução

## Funcionalidades Implementadas

### 1. Classificação de Imagem
✅ Carregamento automático de imagem de exemplo  
✅ Classificação com MobileNetV2  
✅ Identificação: gato, cachorro, outro animal  
✅ Exibição de confiança e top 3  
✅ Tratamento de erros  

### 2. Classificação + Localização
✅ Detecção com YOLOv8  
✅ Bounding box vermelha  
✅ Label com classe e confiança  
✅ Coordenadas detalhadas  
✅ Centro do objeto marcado  

### 3. Detecção de Objetos
✅ Detecção múltipla simultânea  
✅ Bounding boxes coloridas  
✅ Labels para cada objeto  
✅ Contagem por classe  
✅ Estatísticas detalhadas  

### 4. Segmentação de Instâncias
✅ Máscaras coloridas semitransparentes  
✅ Contornos destacados  
✅ Numeração de instâncias  
✅ Overlay visual  
✅ Pixels segmentados contados  

## Imagens de Exemplo

Cada script cria automaticamente imagens de exemplo quando não encontra arquivos:

- `gato_exemplo.jpg` - Gato simulado para classificação
- `cachorro_localizacao.jpg` - Cachorro para localização
- `multiplos_animais.jpg` - Cena com múltiplos animais
- `cena_segmentacao.jpg` - Cena complexa para segmentação

## Resultados Gerados

Cada execução salva resultados:

- `resultado_classificacao.jpg` - Imagem com classificação
- `resultado_localizacao.jpg` - Imagem com bounding box
- `resultado_multiplas_deteccoes.jpg` - Múltiplas detecções
- `resultado_segmentacao.jpg` - Segmentação completa

## Requisitos de Sistema

### Mínimo
- Python 3.8+
- 4GB RAM
- Processador moderno

### Recomendado
- Python 3.9+
- 8GB RAM
- GPU com CUDA (para melhor performance)
- 2GB de espaço em disco

## Solução de Problemas

### Erros Comuns

#### 1. "model not found"
- **Causa**: Primeira execução, modelo não baixado
- **Solução**: Aguarde download automático ou verifique conexão

#### 2. "cannot load image"
- **Causa**: Arquivo de imagem não encontrado
- **Solução**: Script cria imagem automática

#### 3. "CUDA out of memory"
- **Causa**: GPU sem memória suficiente
- **Solução**: Use CPU ou modelo menor

#### 4. "ultralytics not found"
- **Causa**: Biblioteca não instalada
- **Solução**: `pip install ultralytics`

### Performance

#### Para Melhorar Performance:
1. Use GPU com CUDA
2. Reduza tamanho da imagem
3. Use modelos menores (yolov8n)
4. Feche outros programas

#### Para Reduzir Uso de Memória:
1. Use modelos menores
2. Processe uma imagem por vez
3. Limpe cache regularmente

## Customização

### Adicionar Novas Classes

Modifique as funções de filtragem:

```python
def filtrar_classe_animal(nome_classe):
    nome_lower = nome_classe.lower()
    
    if 'cat' in nome_lower:
        return 'gato'
    elif 'dog' in nome_lower:
        return 'cachorro'
    # Adicione novas classes aqui
    elif 'horse' in nome_lower:
        return 'cavalo'
    else:
        return None
```

### Alterar Cores

Modifique as funções de geração de cores:

```python
def gerar_cor_aleatoria():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
```

### Ajustar Confiança Mínima

Altere o threshold em cada script:

```python
if confianca > 0.3:  # Aumente para mais precisão
```

## Conceitos Teóricos

### Classificação de Imagem
- **Input**: Imagem completa
- **Output**: Uma classe + confiança
- **Uso**: Identificar o conteúdo principal

### Classificação + Localização
- **Input**: Imagem completa
- **Output**: Classe + bounding box + confiança
- **Uso**: Saber o quê e onde está

### Detecção de Objetos
- **Input**: Imagem completa
- **Output**: Múltiplas classes + bounding boxes + confianças
- **Uso**: Encontrar todos os objetos

### Segmentação de Instâncias
- **Input**: Imagem completa
- **Output**: Máscaras pixel a pixel + classes
- **Uso**: Análise detalhada por objeto

## Extensões Possíveis

1. **Vídeo em Tempo Real**
2. **Webcam Integration**
3. **Batch Processing**
4. **API REST**
5. **Interface Gráfica**
6. **Mobile Deployment**

## Referências

- [OpenCV Documentation](https://docs.opencv.org/)
- [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [PyTorch Documentation](https://pytorch.org/)

## Licença

Este projeto é para fins educacionais. Sinta-se livre para modificar e distribuir.

## Suporte

Para dúvidas ou problemas:
1. Verifique a seção de solução de problemas
2. Confirme se todas as dependências estão instaladas
3. Teste com as imagens de exemplo fornecidas

---

**Autor**: Sistema de IA  
**Data**: 11/05/2026  
**Versão**: 1.0  
**Tecnologias**: Python, OpenCV, YOLOv8, TensorFlow

# COMO USAR OS ALGORITMOS DE SEGMENTAÇÃO

## 📋 INSTRUÇÕES IMPORTANTES

### ⚠️ AVISO: IMAGEM NECESSÁRIA

Para usar os algoritmos 2, 3 e 4, você **PRECISA** colocar o arquivo:

```
gatinhocachorroobjetos.jpg
```

Na pasta: `c:\Users\wesll\Documents\Dev\UNDB\IA\aula 11-05\Segmentacao\`

## 🎯 O QUE FOI MODIFICADO

### ✅ **Alterações Realizadas:**
1. **Removida criação automática de imagens de exemplo** dos algoritmos 2, 3 e 4
2. **Agora os algoritmos usam APENAS** a imagem `gatinhocachorroobjetos.jpg`
3. **Mensagem de erro clara** quando a imagem não é encontrada
4. **Validação rigorosa** do arquivo antes do processamento

## 🚀 COMO EXECUTAR

### **Algoritmo 1 - Classificação (usa gatinho1.jpg)**
```bash
python 01_classificacao_imagem.py
```

### **Algoritmo 2 - Localização (usa gatinhocachorroobjetos.jpg)**
```bash
python 02_classificacao_localizacao.py
```

### **Algoritmo 3 - Detecção Múltipla (usa gatinhocachorroobjetos.jpg)**
```bash
python 03_detecacao_objetos.py
```

### **Algoritmo 4 - Segmentação (usa gatinhocachorroobjetos.jpg)**
```bash
python 04_segmentacao_instancias.py
```

## 📁 ESTRUTURA DE ARQUIVOS

```
Segmentacao/
├── gatinho1.jpg                    ← Necessário para algoritmo 1
├── gatinhocachorroobjetos.jpg      ← Necessário para algoritmos 2, 3, 4
├── 01_classificacao_imagem.py
├── 02_classificacao_localizacao.py
├── 03_detecacao_objetos.py
├── 04_segmentacao_instancias.py
└── README_USUARIO.md
```

## ⚠️ MENSAGENS DE ERRO

Se a imagem `gatinhocachorroobjetos.jpg` não for encontrada, você verá:

```
❌ ERRO: Arquivo 'gatinhocachorroobjetos.jpg' não encontrado!
Por favor, coloque a imagem 'gatinhocachorroobjetos.jpg' na pasta Segmentacao
O programa será encerrado.
```

## 🎯 RESULTADOS ESPERADOS

Quando executados com a imagem correta, os algoritmos irão:

### **Algoritmo 2:** 
- Detectar o objeto principal
- Desenhar bounding box vermelha
- Mostrar coordenadas e confiança

### **Algoritmo 3:**
- Detectar múltiplos objetos
- Desenhar bounding boxes coloridas
- Contar gatos, cachorros, etc.

### **Algoritmo 4:**
- Segmentar cada objeto individualmente
- Aplicar máscaras coloridas
- Mostrar contornos destacados

## 🔧 SOLUÇÃO DE PROBLEMAS

### **Problema: "Arquivo não encontrado"**
**Solução:** Coloque `gatinhocachorroobjetos.jpg` na pasta Segmentacao

### **Problema: "Nenhum objeto detectado"**
**Solução:** Use uma imagem com animais bem visíveis e nítidos

### **Problema: "Erro na detecção"**
**Solução:** Verifique se a imagem não está corrompida e tente novamente

## 📊 RESUMO DAS MUDANÇAS

| Algoritmo | Imagem Usada | Cria Exemplo? |
|-----------|--------------|---------------|
| 01_classificacao_imagem.py | gatinho1.jpg | ✅ Sim |
| 02_classificacao_localizacao.py | gatinhocachorroobjetos.jpg | ❌ Não |
| 03_detecacao_objetos.py | gatinhocachorroobjetos.jpg | ❌ Não |
| 04_segmentacao_instancias.py | gatinhocachorroobjetos.jpg | ❌ Não |

---

**Agora os algoritmos 2, 3 e 4 analisam APENAS sua imagem real!**

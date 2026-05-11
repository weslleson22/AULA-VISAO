"""
===============================================================================
EXECUTAR TODOS OS ALGORITMOS DE SEGMENTAÇÃO
===============================================================================
Este script executa todos os quatro algoritmos de segmentação em sequência
para testar a refatoração e garantir que funcionem corretamente.

Algoritmos:
1. Classificação de Imagem (gatinho1.jpg)
2. Classificação + Localização (gatinhocachorroobjetos.jpg)
3. Detecção de Objetos (gatinhocachorroobjetos.jpg)
4. Segmentação de Instâncias (gatinhocachorroobjetos.jpg)

Autor: Sistema de IA
Data: 11/05/2026
===============================================================================
"""

import subprocess
import sys
import os

def executar_script(nome_script, descricao):
    """
    Executa um script específico e exibe o resultado
    """
    print(f"\n{'='*80}")
    print(f"EXECUTANDO: {descricao}")
    print(f"SCRIPT: {nome_script}")
    print(f"{'='*80}")
    
    try:
        # Executa o script
        resultado = subprocess.run([sys.executable, nome_script], 
                                capture_output=True, 
                                text=True, 
                                cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # Exibe a saída
        if resultado.stdout:
            print("SAÍDA:")
            print(resultado.stdout)
        
        if resultado.stderr:
            print("ERROS/AVISOS:")
            print(resultado.stderr)
        
        if resultado.returncode == 0:
            print(f"✅ {nome_script} executado com sucesso!")
        else:
            print(f"❌ {nome_script} falhou com código {resultado.returncode}")
        
        return resultado.returncode == 0
        
    except Exception as e:
        print(f"❌ Erro ao executar {nome_script}: {e}")
        return False

def verificar_imagens():
    """
    Verifica se as imagens necessárias existem
    """
    print("\n" + "="*60)
    print("VERIFICANDO IMAGENS NECESSÁRIAS")
    print("="*60)
    
    imagens_necessarias = [
        "gatinho1.jpg",
        "gatinhocachorroobjetos.jpg"
    ]
    
    todas_existem = True
    for imagem in imagens_necessarias:
        if os.path.exists(imagem):
            print(f"✅ {imagem} - encontrada")
        else:
            print(f"❌ {imagem} - não encontrada")
            todas_existem = False
    
    return todas_existem

def main():
    """
    Função principal que executa todos os algoritmos
    """
    print("="*80)
    print("EXECUÇÃO COMPLETA DOS ALGORITMOS DE SEGMENTAÇÃO")
    print("="*80)
    print("Este script executará todos os 4 algoritmos de segmentação:")
    print("1. Classificação de Imagem")
    print("2. Classificação + Localização")
    print("3. Detecção de Objetos")
    print("4. Segmentação de Instâncias")
    print("="*80)
    
    # Verifica se as imagens existem
    if not verificar_imagens():
        print("\n⚠️ AVISO: Algumas imagens não foram encontradas.")
        print("Os scripts criarão imagens de exemplo automaticamente se necessário.")
    
    # Lista de scripts para executar
    scripts = [
        ("01_classificacao_imagem.py", "Classificação de Imagem (gatinho1.jpg)"),
        ("02_classificacao_localizacao.py", "Classificação + Localização (gatinhocachorroobjetos.jpg)"),
        ("03_detecacao_objetos.py", "Detecção de Objetos (gatinhocachorroobjetos.jpg)"),
        ("04_segmentacao_instancias.py", "Segmentação de Instâncias (gatinhocachorroobjetos.jpg)")
    ]
    
    # Executa cada script
    resultados = {}
    for script, descricao in scripts:
        resultados[script] = executar_script(script, descricao)
        
        # Pausa entre execuções para permitir visualização
        input("\nPressione Enter para continuar para o próximo algoritmo...")
    
    # Resumo final
    print(f"\n{'='*80}")
    print("RESUMO DA EXECUÇÃO")
    print("="*80)
    
    sucesso = 0
    falha = 0
    
    for script, resultado in resultados.items():
        if resultado:
            print(f"✅ {script} - Sucesso")
            sucesso += 1
        else:
            print(f"❌ {script} - Falha")
            falha += 1
    
    print(f"\nTotal: {sucesso + falha} scripts")
    print(f"Sucesso: {sucesso}")
    print(f"Falha: {falha}")
    
    if falha == 0:
        print("\n🎉 Todos os algoritmos foram executados com sucesso!")
    else:
        print(f"\n⚠️ {falha} algoritmo(s) falharam. Verifique os erros acima.")
    
    # Verifica se os resultados foram gerados
    print(f"\n{'='*60}")
    print("VERIFICANDO ARQUIVOS DE RESULTADO")
    print("="*60)
    
    arquivos_resultado = [
        "resultado_classificacao.jpg",
        "resultado_localizacao.jpg", 
        "resultado_multiplas_deteccoes.jpg",
        "resultado_segmentacao.jpg"
    ]
    
    for arquivo in arquivos_resultado:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - gerado")
        else:
            print(f"❌ {arquivo} - não encontrado")

if __name__ == "__main__":
    main()

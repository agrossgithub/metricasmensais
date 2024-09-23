# atualizar_dados.py

import os
import pandas as pd

def preparar_ambiente():
    # Definir o caminho para o diretório de dados
    CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), 'dados')
    
    # Criar a pasta 'dados/' se ela não existir
    if not os.path.exists(CAMINHO_DADOS):
        os.makedirs(CAMINHO_DADOS)
        print(f"Diretório '{CAMINHO_DADOS}' criado.")
    else:
        print(f"Diretório '{CAMINHO_DADOS}' já existe.")
    
    # Definir os arquivos CSV e seus cabeçalhos
    arquivos_csv = {
        'desempenho_ads.csv': ['Metrica', 'Facebook_Ads', 'Google_Ads'],
        'comparacao_mensal.csv': ['Metrica', 'Plataforma_Mes', 'Valor'],
        'melhores_anuncios.csv': ['Anuncio', 'CTR'],
        'cliques_estado.csv': ['Estado', 'Cliques'],
        'produtos.csv': ['Produto', 'Valor_Investido_R$', 'Retorno_R$']
    }
    
    # Criar os arquivos CSV com cabeçalhos se eles não existirem
    for arquivo, cabecalhos in arquivos_csv.items():
        caminho_arquivo = os.path.join(CAMINHO_DADOS, arquivo)
        if not os.path.exists(caminho_arquivo):
            df = pd.DataFrame(columns=cabecalhos)
            df.to_csv(caminho_arquivo, index=False)
            print(f"Arquivo '{arquivo}' criado com cabeçalhos {cabecalhos}.")
        else:
            print(f"Arquivo '{arquivo}' já existe.")

def atualizar_produtos(novos_dados):
    CAMINHO_DADOS = os.path.join(os.path.dirname(__file__), 'dados')
    caminho_arquivo = os.path.join(CAMINHO_DADOS, 'produtos.csv')
    
    # Carregar dados existentes
    try:
        df_produtos = pd.read_csv(caminho_arquivo)
    except Exception as e:
        print(f"Erro ao carregar 'produtos.csv': {e}")
        return
    
    # Adicionar novos dados
    df_novos = pd.DataFrame(novos_dados)
    df_produtos = pd.concat([df_produtos, df_novos], ignore_index=True)
    
    # Salvar de volta no CSV
    try:
        df_produtos.to_csv(caminho_arquivo, index=False)
        print("Produtos atualizados com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar 'produtos.csv': {e}")

if __name__ == "__main__":
    preparar_ambiente()
    
    # Dados iniciais de produtos (exemplo)
    novos_dados_produtos = {
        'Produto': ['Kit Plantio', 'Turbo Mix', 'Vollverini', 'Best Mix', 'Nitro Mix'],
        'Valor_Investido_R$': [21000.00, 16000.00, 19000.00, 23000.00, 26000.00],
        'Retorno_R$': [52000.00, 47000.00, 49000.00, 57000.00, 62000.00]
    }
    atualizar_produtos(novos_dados_produtos)

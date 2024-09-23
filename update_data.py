# update_data.py
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from init_db import DesempenhoAds, ComparacaoMensal, Base

# Conectar ao banco de dados
engine = create_engine('sqlite:///dados_dashboard.db')
Session = sessionmaker(bind=engine)
session = Session()

# Função para atualizar desempenho_ads
def atualizar_desempenho_ads(dados):
    # Limpar tabela antes de inserir novos dados
    session.query(DesempenhoAds).delete()
    session.commit()
    
    # Inserir novos dados
    for index, row in dados.iterrows():
        registro = DesempenhoAds(
            metrica=row['Metrica'],
            facebook_ads=row['Facebook_Ads'],
            google_ads=row['Google_Ads']
        )
        session.add(registro)
    session.commit()

# Função para atualizar comparacao_mensal
def atualizar_comparacao_mensal(dados):
    # Limpar tabela antes de inserir novos dados
    session.query(ComparacaoMensal).delete()
    session.commit()
    
    # Inserir novos dados
    for index, row in dados.iterrows():
        registro = ComparacaoMensal(
            metrica=row['Metrica'],
            plataforma_mes=row['Plataforma_Mes'],
            valor=row['Valor']
        )
        session.add(registro)
    session.commit()

if __name__ == "__main__":
    # Exemplo de atualização para desempenho_ads
    dados_desempenho = pd.DataFrame({
        'Metrica': ['Impressoes', 'Cliques_no_link', 'Resultados', 'CTR', 'CPL_R$', 'Valor_usado_R$'],
        'Facebook_Ads': [3551018, 49775, 1371, 1.72, 41.56, 44717.89],
        'Google_Ads': [274854, 21898, 300, 6.92, 49.85, 9452.34]
    })
    atualizar_desempenho_ads(dados_desempenho)
    
    # Exemplo de atualização para comparacao_mensal
    dados_comparacao = pd.DataFrame({
        'Metrica': ['Impressoes', 'Cliques_no_link', 'Resultados', 'CTR', 'CPL_R$'],
        'Plataforma_Mes': [
            'Facebook_Ads_Janeiro', 'Facebook_Ads_Janeiro', 'Facebook_Ads_Janeiro', 'Facebook_Ads_Janeiro', 'Facebook_Ads_Janeiro',
            # Adicione os outros meses e plataformas conforme necessário
            'Google_Ads_Janeiro', 'Google_Ads_Janeiro', 'Google_Ads_Janeiro', 'Google_Ads_Janeiro', 'Google_Ads_Janeiro'
        ],
        'Valor': [1500000, 20000, 500, 1.33, 40.00, 200000, 25000, 350, 5.00, 45.00]
    })
    atualizar_comparacao_mensal(dados_comparacao)
    
    print("Dados atualizados com sucesso!")

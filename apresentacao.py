import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import pyrebase
from dash import dash_table
import logging

logging.basicConfig(level=logging.INFO)

def botoes_navegacao(prev_href, next_href):
    return html.Div([
        dbc.Button(
            [html.I(className='fas fa-arrow-left'), " Voltar"],
            href=prev_href,
            color="success",  # Verde fluorescente
            className="nav-button-left",
            style={
                'position': 'fixed',
                'bottom': '20px',  # Botão inferior esquerdo
                'left': '20px',
                'zIndex': '1000',
                'display': 'flex',
                'alignItems': 'center',
                'padding': '12px 24px',
                'font-size': '18px',
                'border-radius': '50px',  # Botões arredondados
                'box-shadow': '0 4px 6px rgba(0,0,0,0.1)',  # Sombra
                'color': '#FFFFFF'
            }
        ),
        dbc.Button(
            ["Avançar ", html.I(className='fas fa-arrow-right')],
            href=next_href,
            color="success",  # Verde fluorescente
            className="nav-button-right",
            style={
                'position': 'fixed',
                'bottom': '20px',  # Botão inferior direito
                'right': '20px',
                'zIndex': '1000',
                'display': 'flex',
                'alignItems': 'center',
                'padding': '12px 24px',
                'font-size': '18px',
                'border-radius': '50px',  # Botões arredondados
                'box-shadow': '0 4px 6px rgba(0,0,0,0.1)',  # Sombra
                'color': '#FFFFFF'
            }
        )
    ])

# Configuração do Firebase
firebase_config = {
    "apiKey": "AIzaSyCBkiK8O5E_9ff3GTfOFi3kDgpy_r0lLL4",
    "authDomain": "dados-metricas.firebaseapp.com",
    "databaseURL": "https://dados-metricas-default-rtdb.firebaseio.com",
    "projectId": "dados-metricas",
    "storageBucket": "dados-metricas.appspot.com",
    "messagingSenderId": "275483793742",
    "appId": "1:275483793742:web:10f1253fb969eccb3ee61f",
    "measurementId": "G-TCQK2KE5RN"
}

def carregar_dados_existentes(mes, plataforma):
    """
    Função para carregar os dados existentes do Firebase para um determinado mês e plataforma.
    """
    try:
        # Acessar a estrutura no Firebase usando o mês e a plataforma como chaves
        print(f"🔍 Carregando dados para {mes} - {plataforma}...")
        dados_mes = db.child("desempenho").child(mes).child(plataforma).get().val()

        if dados_mes:
            # Carregar cada métrica individualmente, garantindo que o nome das chaves esteja correto
            impressoes = dados_mes.get("Impressoes", 0)
            cliques_no_link = dados_mes.get("Cliques_no_link", 0)
            orcamento = dados_mes.get("Orcamento", 0.0)
            ctr = dados_mes.get("CTR", 0.0)
            cpl = dados_mes.get("CPL", 0.0)
            resultados = dados_mes.get("Resultados", 0)

            # Exibir os dados carregados para verificação
            print(f"📊 Métricas carregadas para {mes} - {plataforma}:")
            print(f"  📌 Impressões: {impressoes}")
            print(f"  📌 Cliques no link: {cliques_no_link}")
            print(f"  📌 Orçamento: {orcamento}")
            print(f"  📌 CTR: {ctr}")
            print(f"  📌 CPL: {cpl}")
            print(f"  📌 Resultados: {resultados}")

            # Retornar os dados ordenados nas colunas esperadas
            return (
                impressoes,
                cliques_no_link,
                orcamento,
                ctr,
                cpl,
                resultados
            )
        else:
            # Se não houver dados, retornar valores padrão e informar ao usuário
            print(f"⚠️ Nenhum dado encontrado para {mes} - {plataforma}.")
            return None, None, None, None, None, None
    except Exception as e:
        print(f"❌ Erro ao carregar dados do Firebase: {e}")
        return None, None, None, None, None, None

# Inicializar o Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# Lista de estilos externos incluindo Montserrat via Google Fonts e Font Awesome para ícones
external_stylesheets = [
    dbc.themes.BOOTSTRAP,  # Usando o tema Bootstrap
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap',  # Fonte Montserrat
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',  # Font Awesome para ícones
]
mapa_metricas_firebase = {
    'Impressões': 'Impressoes',
    'Cliques no link': 'Cliques_no_link',
    'Resultados': 'Resultados',
    'Orçamento (R$)': 'Orcamento',
    'CTR (%)': 'CTR',
    'CPL (R$)': 'CPL'
}

def ajustar_nomes_metricas(df):
    # Verificar se o DataFrame possui as colunas a serem renomeadas
    if not df.empty:
        df.rename(columns=mapa_metricas_firebase, inplace=True)
    return df

# Inicializar o aplicativo Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server  # Necessário para implantação e para o Gunicorn

# Definir esquema de cores da Agross do Brasil
primary_color = '#00FF7F'  # Verde fluorescente para títulos
secondary_color = '#f0f2f5'  # Fundo mais agradável
accent_color = '#343a40'  # Cor de texto escuro para contraste

# Lista completa de meses
meses_completos = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

# Dados de desempenho de Facebook Ads e Google Ads (Junho a Setembro)
dados_desempenho = {
    'Plataforma': [],
    'Mês': [],
    'Impressões': [],
    'Cliques no link': [],
    'Resultados': [],
    'Orçamento (R$)': [],
    'CTR (%)': [],
    'CPL (R$)': []
}

# Dados existentes para Facebook Ads
facebook_ads_data = {
    'Junho': {'Impressões': 1703129, 'Cliques no link': 16241, 'Resultados': 516, 'Orçamento (R$)': 21361.39, 'CTR (%)': 0.93, 'CPL (R$)': 43.54},
    'Julho': {'Impressões': 2676920, 'Cliques no link': 23930, 'Resultados': 1140, 'Orçamento (R$)': 28062.78, 'CTR (%)': 1.36, 'CPL (R$)': 42.28},
    'Agosto': {'Impressões': 3551018, 'Cliques no link': 49775, 'Resultados': 1371, 'Orçamento (R$)': 44717.89, 'CTR (%)': 2.88, 'CPL (R$)': 32.50},
    'Setembro': {'Impressões': 1453771, 'Cliques no link': 18896, 'Resultados': 719, 'Orçamento (R$)': 17278.33, 'CTR (%)': 1.74, 'CPL (R$)': 33.06}
}

# Dados existentes para Google Ads
google_ads_data = {
    'Junho': {'Impressões': 273086, 'Cliques no link': 10151, 'Resultados': 240, 'Orçamento (R$)': 8595.68, 'CTR (%)': 5.51, 'CPL (R$)': 30.58},
    'Julho': {'Impressões': 191434, 'Cliques no link': 7170, 'Resultados': 221, 'Orçamento (R$)': 7952.17, 'CTR (%)': 5.48, 'CPL (R$)': 63.13},
    'Agosto': {'Impressões': 274854, 'Cliques no link': 21898, 'Resultados': 300, 'Orçamento (R$)': 9452.34, 'CTR (%)': 1.78, 'CPL (R$)': 40.00},
    'Setembro': {'Impressões': 108475, 'Cliques no link': 9447, 'Resultados': 224, 'Orçamento (R$)': 7485.53, 'CTR (%)': 7.49, 'CPL (R$)': 30.70}
}

# Preencher dados_desempenho com todos os meses
for plataforma in ['Facebook Ads', 'Google Ads']:
    for mes in meses_completos:
        dados_desempenho['Plataforma'].append(plataforma)
        dados_desempenho['Mês'].append(mes)
        if plataforma == 'Facebook Ads':
            if mes in facebook_ads_data:
                dados_desempenho['Impressões'].append(facebook_ads_data[mes]['Impressões'])
                dados_desempenho['Cliques no link'].append(facebook_ads_data[mes]['Cliques no link'])
                dados_desempenho['Resultados'].append(facebook_ads_data[mes]['Resultados'])
                dados_desempenho['Orçamento (R$)'].append(facebook_ads_data[mes]['Orçamento (R$)'])
                dados_desempenho['CTR (%)'].append(facebook_ads_data[mes]['CTR (%)'])
                dados_desempenho['CPL (R$)'].append(facebook_ads_data[mes]['CPL (R$)'])
            else:
                # Placeholder para meses sem dados
                dados_desempenho['Impressões'].append(0)
                dados_desempenho['Cliques no link'].append(0)
                dados_desempenho['Resultados'].append(0)
                dados_desempenho['Orçamento (R$)'].append(0.0)
                dados_desempenho['CTR (%)'].append(0.0)
                dados_desempenho['CPL (R$)'].append(0.0)
        elif plataforma == 'Google Ads':
            if mes in google_ads_data:
                dados_desempenho['Impressões'].append(google_ads_data[mes]['Impressões'])
                dados_desempenho['Cliques no link'].append(google_ads_data[mes]['Cliques no link'])
                dados_desempenho['Resultados'].append(google_ads_data[mes]['Resultados'])
                dados_desempenho['Orçamento (R$)'].append(google_ads_data[mes]['Orçamento (R$)'])
                dados_desempenho['CTR (%)'].append(google_ads_data[mes]['CTR (%)'])
                dados_desempenho['CPL (R$)'].append(google_ads_data[mes]['CPL (R$)'])
            else:
                # Placeholder para meses sem dados
                dados_desempenho['Impressões'].append(0)
                dados_desempenho['Cliques no link'].append(0)
                dados_desempenho['Resultados'].append(0)
                dados_desempenho['Orçamento (R$)'].append(0.0)
                dados_desempenho['CTR (%)'].append(0.0)
                dados_desempenho['CPL (R$)'].append(0.0)

df_desempenho = pd.DataFrame(dados_desempenho)
@app.callback(
    [Output('tabela-melhores-anuncios', 'children'),
     Output('imagem-preview-public', 'src')],
    Input('mes-melhores-anuncios-dropdown', 'value')
)
def atualizar_tabela_e_imagem_melhores_anuncios(mes_selecionado):
    try:
        # Carregar os 5 melhores anúncios do Firebase
        anuncios_firebase = db.child("melhores_anuncios").child(mes_selecionado).get().val()
        imagem_firebase = db.child("imagens_melhores_anuncios").child(mes_selecionado).get().val()  # Pegar a imagem associada

        if anuncios_firebase:
            # Criar os dados para a tabela
            anuncios_data = [
                {"nome": anuncios_firebase[f"Anuncio_{i+1}"]['nome'], 
                 "CTR": anuncios_firebase[f"Anuncio_{i+1}"]['CTR']} 
                for i in range(5)
            ]
            
            # Criar a tabela com os dados
            tabela = dash_table.DataTable(
                columns=[
                    {"name": "Nome do Anúncio", "id": "nome"},
                    {"name": "CTR (%)", "id": "CTR"},
                ],
                data=anuncios_data,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '10px'},
                style_header={'backgroundColor': primary_color, 'fontWeight': 'bold', 'color': 'white'},
                style_data={'backgroundColor': '#f9f9f9'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#e9e9e9'}
                ]
            )

            # Retornar a tabela e o link da imagem
            return tabela, imagem_firebase if imagem_firebase else ""
        else:
            # Nenhum dado encontrado para o mês selecionado
            return dbc.Alert("Nenhum dado encontrado para o mês selecionado.", color="warning"), ""
    except Exception as e:
        return dbc.Alert(f"Erro ao carregar dados: {str(e)}", color="danger"), ""

# Dados de melhores anúncios (CTR) para todos os meses (Agosto e Setembro têm dados)
dados_melhores_anuncios = {
    'Mês': [],
    'Anúncio': [],
    'CTR (%)': [],
    'Imagem': []
}

# Lista de anúncios fixos
lista_anuncios = [
    'Aumente sua PRODUTIVIDADE!', 
    'Cadastre-se e fale conosco', 
    'Com o KIT PLANTIO TORNITEC', 
    'Para o grande e pequeno produtor!', 
    'Cadastre-se e fale conosco (Turbomix)', 
    'KIT PLANTIO NA AGROLEITE!'
]

# URLs das imagens para anúncios (placeholder para meses sem dados)
imagem_placeholder = "https://i.ibb.co/FByXKbq/anuncios.png"
imagem_setembro = "https://i.ibb.co/8rWv8vG/Captura-de-tela-2024-09-26-102148.png"

for mes in meses_completos:
    for anuncio in lista_anuncios:
        dados_melhores_anuncios['Mês'].append(mes)
        dados_melhores_anuncios['Anúncio'].append(anuncio)
        if mes == 'Agosto':
            # Dados reais para Agosto
            index = lista_anuncios.index(anuncio)
            dados_melhores_anuncios['CTR (%)'].append([2.88, 2.73, 2.57, 1.94, 1.84, 1.78][index])
            dados_melhores_anuncios['Imagem'].append(imagem_placeholder)
        elif mes == 'Setembro':
            # Dados reais para Setembro com 5 diferentes CTRs
            ctrs_setembro = {
                'Aumente sua PRODUTIVIDADE!': 0.0,  # Placeholder, ajuste conforme necessário
                'Cadastre-se e fale conosco': 3.86,
                'Com o KIT PLANTIO TORNITEC': 5.08,
                'Para o grande e pequeno produtor!': 2.71,
                'Cadastre-se e fale conosco (Turbomix)': 2.27,
                'KIT PLANTIO NA AGROLEITE!': 1.52
            }
            # Verificar se o anúncio tem um CTR específico
            ctr = ctrs_setembro.get(anuncio, 0.0)
            dados_melhores_anuncios['CTR (%)'].append(ctr)
            dados_melhores_anuncios['Imagem'].append(imagem_setembro)
        else:
            # Placeholder para meses sem dados
            dados_melhores_anuncios['CTR (%)'].append(0.0)
            dados_melhores_anuncios['Imagem'].append(imagem_placeholder)

df_melhores_anuncios = pd.DataFrame(dados_melhores_anuncios)

# Dados de valores individuais de cada produto
dados_produtos = {
    'Mês': meses_completos * 5,  # 5 produtos
    'Produto': ['Kit Plantio'] * 12 + ['Turbo Mix'] * 12 + ['Vollverini'] * 12 + ['Best Mix'] * 12 + ['Nitro Mix'] * 12,
    'Valor Investido (R$)': [
        0, 0, 0, 0, 0, 0, 0, 10845.15, 0, 0, 0, 0,  # Kit Plantio
        0, 0, 0, 0, 0, 0, 0, 5842.36, 0, 0, 0, 0,   # Turbo Mix
        0, 0, 0, 0, 0, 0, 0, 4621.99, 0, 0, 0, 0,   # Vollverini
        0, 0, 0, 0, 0, 0, 0, 1260.09, 0, 0, 0, 0,   # Best Mix
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0        # Nitro Mix
    ],
    'Retorno (R$)': [
        0, 0, 0, 0, 0, 0, 0, 1655659.44, 0, 0, 0, 0,  # Kit Plantio
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,           # Turbo Mix
        0, 0, 0, 0, 0, 0, 0, 816725.00, 0, 0, 0, 0,   # Vollverini
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,           # Best Mix
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0            # Nitro Mix
    ]
}

df_produtos = pd.DataFrame(dados_produtos)

# Calcular ROI por produto, com tratamento para valores investidos iguais a 0
df_produtos['ROI (%)'] = df_produtos.apply(
    lambda row: ((row['Retorno (R$)'] - row['Valor Investido (R$)']) / row['Valor Investido (R$)']) * 100 
    if row['Valor Investido (R$)'] > 0 else 0.0,
    axis=1
)

# Função para formatar valores monetários e porcentagens para as tabelas
def formatar_valores(df):
    # Formatar colunas de valores numéricos para moeda
    df_formatado = df.copy()
    for col in ['Valor Investido (R$)', 'Retorno (R$)']:
        if col in df_formatado.columns:
            df_formatado[col] = df_formatado[col].apply(
                lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") 
                if isinstance(x, (int, float)) else x
            )
    # Formatar ROI
    if 'ROI (%)' in df_formatado.columns:
        df_formatado['ROI (%)'] = df_formatado['ROI (%)'].apply(
            lambda x: f"{x:.2f}%"
        )
    return df_formatado

# Aplicando a formatação de valores monetários
df_produtos_formatado = formatar_valores(df_produtos)



# Função para formatar valores monetários conforme a métrica
def formatar_valor(metrica, valor):
    try:
        # Verificar se o valor é nulo ou vazio
        if pd.isna(valor) or valor == '':
            return ''
        
        # Formatação para métricas numéricas inteiras
        if metrica in ['Impressões', 'Cliques no link', 'Resultados']:
            return f"{int(valor):,}".replace(",", ".")  # Separador de milhar com ponto
        
        # Formatação para métricas de percentual
        elif metrica == 'CTR (%)':
            return f"{float(valor):.2f}%".replace(".", ",")  # Converter ponto para vírgula em porcentagem
        
        # Formatação para valores monetários (R$)
        elif metrica in ['CPL (R$)', 'Orçamento (R$)']:
            return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")  # Ajuste de separadores
        
        # Retorno padrão para valores que não precisam de formatação
        else:
            return str(valor)
    
    except (ValueError, TypeError):
        # Caso haja algum erro de conversão, retornar string vazia
        return ''


# Função para gerar a tabela com estilos aprimorados
def gerar_tabela(df):
    return dbc.Table.from_dataframe(
        df, striped=True, bordered=True, hover=True, 
        className="table",
        style={
            'font-size': '20px', 
            'text-align': 'center', 
            'background-color': '#FFFFFF',
            'color': '#343a40'
        }
    )

# Função para gerar a tabela de desempenho com totais e espaçamento refinado
def gerar_tabela_desempenho(df, total_facebook, total_google, total_spend, total_resultado):
    tabela = gerar_tabela(df)

    # Ajustar o tamanho e estilo dos cards de totais com mais espaçamento entre eles
    cards = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total gasto no Facebook Ads", className="card-title", style={'font-size': '12px'}),
                    html.P(f"R$ {total_facebook:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                           className="card-text", style={'font-size': '12px'})
                ])
            ], color="success", inverse=True, style={'width': '10rem', 'padding': '5px', 'margin': '10px'})  # Ajuste de margem e largura menor
        ], width='auto'),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total gasto no Google Ads", className="card-title", style={'font-size': '12px'}),
                    html.P(f"R$ {total_google:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                           className="card-text", style={'font-size': '12px'})
                ])
            ], color="danger", inverse=True, style={'width': '10rem', 'padding': '5px', 'margin': '10px'})  # Ajuste de margem e largura menor
        ], width='auto'),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Investido", className="card-title", style={'font-size': '12px'}),
                    html.P(f"R$ {total_spend:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                           className="card-text", style={'font-size': '12px'})
                ])
            ], color="info", inverse=True, style={'width': '10rem', 'padding': '5px', 'margin': '10px'})  # Ajuste de margem e largura menor
        ], width='auto'),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total de Resultados", className="card-title", style={'font-size': '12px'}),
                    html.P(f"{total_resultado}", className="card-text", style={'font-size': '12px'})  # Valor de total_resultado
                ])
            ], color="primary", inverse=True, style={'width': '10rem', 'padding': '5px', 'margin': '10px'})  # Ajuste de margem e largura menor
        ], width='auto')
    ], className="mb-4", justify='center')  # Centralizando os cards

    # Container fixo para centralizar os cards na parte inferior
    cards_fixed = html.Div([cards], style={
        'position': 'fixed',
        'bottom': '20px',  # Alinhar os cards ao canto inferior
        'left': '50%',  # Centralizar horizontalmente
        'transform': 'translateX(-50%)',  # Centralizar no meio da tela
        'zIndex': '1000',
        'display': 'flex',
        'justify-content': 'center',  # Espaçamento centralizado
        'align-items': 'center',
        'flex-wrap': 'nowrap',  # Manter todos os elementos em uma linha
        'gap': '20px'  # Espaçamento entre os elementos
    })

    # Container para a tabela e os cards
    return html.Div([tabela, cards_fixed], style={'position': 'relative', 'height': 'auto'})

def renomear_conversoes_para_vendas():
    try:
        funil_data = db.child("funil_vendas").get().val()
        if not funil_data:
            print("Nenhum dado encontrado para 'funil_vendas'.")
            return
        
        for mes, dados in funil_data.items():
            if 'Conversões' in dados:
                vendas = dados.pop('Conversões')
                dados['Vendas'] = vendas
                db.child("funil_vendas").child(mes).update({'Vendas': vendas})
                db.child("funil_vendas").child(mes).child('Conversões').remove()
                print(f"Renomeado 'Conversões' para 'Vendas' no mês {mes}.")
    except Exception as e:
        print(f"Erro ao renomear 'Conversões' para 'Vendas': {e}")

# Execute a função uma vez para renomear os dados existentes
renomear_conversoes_para_vendas()
# Função para criar o gráfico de média dos totais (incluindo Google Ads e Facebook Ads)
def criar_grafico_media_totais(metrica_selecionada):
    try:
        logging.info(f"Atualizando gráfico para a métrica: {metrica_selecionada}")
        
        # Buscar todos os meses disponíveis no Firebase
        dados_desempenho = db.child("desempenho").get().val()
        
        if not dados_desempenho:
            logging.warning("Nenhum dado encontrado em 'desempenho'.")
            return px.bar(title="Nenhum dado disponível.")
        
        # Lista para armazenar os dados para o gráfico
        dados_para_grafico = {
            'Mês': [],
            'Plataforma': [],
            'Valor': []
        }
        
        # Iterar sobre cada mês e plataforma para coletar os dados
        for mes, plataformas in dados_desempenho.items():
            for plataforma, metrics in plataformas.items():
                # Obter o valor da métrica selecionada, garantindo que a chave exista
                chave_firebase = mapa_metricas_firebase.get(metrica_selecionada, metrica_selecionada)
                valor = metrics.get(chave_firebase, 0)
                
                # Converter valor para float se possível
                try:
                    valor = float(valor)
                except (ValueError, TypeError):
                    valor = 0.0
                
                dados_para_grafico['Mês'].append(mes)
                dados_para_grafico['Plataforma'].append(plataforma)
                dados_para_grafico['Valor'].append(valor)
                logging.info(f"Mês: {mes}, Plataforma: {plataforma}, Valor: {valor}")
        
        # Criar DataFrame
        df_grafico = pd.DataFrame(dados_para_grafico)
        
        # Manter a ordem correta dos meses
        meses_ordenados = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        
        df_grafico['Mês'] = pd.Categorical(df_grafico['Mês'], categories=meses_ordenados, ordered=True)
        df_grafico.sort_values('Mês', inplace=True)
        
        # Formatar os valores conforme a métrica
        if "R$" in metrica_selecionada:
            df_grafico['Valor'] = df_grafico['Valor'].astype(float).round(2)
            valor_formatado = 'R$ {0:,.2f}'
        elif "%" in metrica_selecionada:
            df_grafico['Valor'] = df_grafico['Valor'].astype(float).round(2)
            valor_formatado = '{0:.2f}%'
        else:
            df_grafico['Valor'] = df_grafico['Valor'].astype(int)
            valor_formatado = '{0:,}'
        
        # Criar o gráfico de barras
        fig = px.bar(
            df_grafico,
            x='Mês',
            y='Valor',
            color='Plataforma',
            barmode='group',
            title=f"{metrica_selecionada} - Média dos Totais",
            labels={'Valor': metrica_selecionada, 'Mês': 'Mês'},
            text='Valor',
            height=500
        )
        
        # Atualizar layout do gráfico
        fig.update_layout(
            plot_bgcolor=secondary_color,
            paper_bgcolor=secondary_color,
            font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
            title_x=0.5
        )
        
        # Formatar o texto nos eixos com texttemplate adequado
        fig.update_traces(texttemplate=valor_formatado, textposition='outside')
        
        return fig
    
    except Exception as e:
        logging.error(f"Erro na função 'criar_grafico_media_totais': {e}")
        return px.bar(title="Erro ao carregar os dados.")



# Função para criar o gráfico de cliques por estado para vários meses
def criar_grafico_cliques_estado(mes_selecionado):
    try:
        # Buscar os dados de cliques por estado para o mês selecionado no Firebase
        cliques_data = db.child("cliques_por_estado").child(mes_selecionado).get().val()
        
        if not cliques_data:
            # Sem dados para o mês selecionado
            fig = px.pie(title=f"Cliques por Estado - {mes_selecionado} (Sem dados)")
            fig.update_layout(
                plot_bgcolor=secondary_color,
                paper_bgcolor=secondary_color,
                font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
                title_x=0.5
            )
            return fig
        
        # Converter os dados em um DataFrame
        df_mes = pd.DataFrame(list(cliques_data.items()), columns=['Estado', 'Cliques'])
        
        # Gerar o gráfico de pizza
        fig = px.pie(
            df_mes,
            names='Estado',
            values='Cliques',
            title=f'Distribuição de Cliques por Estado - {mes_selecionado}',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_layout(
            plot_bgcolor=secondary_color,
            paper_bgcolor=secondary_color,
            font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
            title_x=0.5
        )
        
        # Adicionar porcentagens no gráfico
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return fig

    except Exception as e:
        logging.error(f"Erro na função 'criar_grafico_cliques_estado': {e}")
        # Retornar um gráfico vazio com mensagem de erro
        fig = px.pie(title="Erro ao carregar os dados.")
        fig.update_layout(
            plot_bgcolor=secondary_color,
            paper_bgcolor=secondary_color,
            font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
            title_x=0.5
        )
        return fig

# Dados de Funil de Vendas (Junho a Setembro)
dados_funil = {
    'Mês': meses_completos,
    'Leads Frios': [0] * 12,
    'Atendidos': [0] * 12,
    'Conversões': [0] * 12
}

# Definir dados para Agosto e Setembro
dados_funil['Leads Frios'][meses_completos.index('Agosto')] = 1371
dados_funil['Atendidos'][meses_completos.index('Agosto')] = 635
dados_funil['Conversões'][meses_completos.index('Agosto')] = 61

dados_funil['Leads Frios'][meses_completos.index('Setembro')] = 943
dados_funil['Atendidos'][meses_completos.index('Setembro')] = 622
dados_funil['Conversões'][meses_completos.index('Setembro')] = 0

df_funil = pd.DataFrame(dados_funil)

# Página Inicial Pública (/)
# Página Inicial Pública (/)
public_home_layout = html.Div([
    html.Div([
        # Logo
        html.Div([
            html.Img(
                src="https://i.ibb.co/jf2b0g7/AGROSS-texto-versaofinal.png",  # Novo link da logo
                style={
                    'width': '600px',
                    'height': 'auto',
                    'display': 'block',
                    'margin-left': 'auto',
                    'margin-right': 'auto'
                }
            )
        ], style={'margin-top': '100px'}),
        
        # Título da Apresentação
        html.Div([
            html.H1("Relatório Mensal de Desempenho", className="text-center", 
                    style={'font-size': '48px', 'font-weight': '700', 'color': primary_color, 'margin-top': '50px'})
        ]),
        
        # Frase "Transformando o Agronegócio"
        html.Div([
            html.H2("Transformando o Agronegócio", className="text-center", 
                    style={'font-size': '36px', 'font-weight': '600', 'color': primary_color, 'margin-top': '20px'})
        ]),
        
        # Botão "Visualizar Métricas"
        html.Div([
            dbc.Button(
                "Visualizar Métricas", 
                href='/page-1',  # Link para a página 1
                color="success",
                style={
                    'font-size': '24px', 
                    'margin-top': '30px',
                    'display': 'block',
                    'margin-left': 'auto',
                    'margin-right': 'auto',
                    'padding': '10px 20px',
                    'border-radius': '50px',  # Botão arredondado
                    'width': '300px'  # Largura do botão
                }
            )
        ], style={'text-align': 'center'}),
        
        # Link para login administrativo
        html.Div([
            dcc.Link(
                "Administrador: Faça login para editar dados",
                href='/admin/login',
                style={'font-size': '24px', 'color': primary_color, 'text-decoration': 'underline'}
            )
        ], style={'text-align': 'center', 'margin-top': '30px'}),
    ]),
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 'height': '100vh', 'background-color': secondary_color})


# Página de Login Administrativo (/admin/login)
admin_login_layout = html.Div([
    html.H1("Login Administrativo", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Formulário de Login
    dbc.Form([
        dbc.Row([
            dbc.Label("Usuário:", html_for="input-usuario", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="text", id="input-usuario", placeholder="Digite seu usuário", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        dbc.Row([
            dbc.Label("Senha:", html_for="input-senha", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="password", id="input-senha", placeholder="Digite sua senha", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        dbc.Button("Login", id="botao-login", color="primary", 
                   style={'font-size': '18px', 'width': '100%'},
                   className="mt-3")
    ], style={'width': '300px', 'margin': 'auto', 'margin-top': '50px'}),
    
    # Feedback de Login
    html.Div(id='login-feedback', style={'text-align': 'center', 'margin-top': '10px'}),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/', next_href='/admin')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Dashboard Administrativo (/admin)
admin_dashboard_layout = html.Div([
    html.H1("Dashboard Administrativo", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
    
    # Links para páginas de edição
    html.Div([
        dbc.Button("Editar Desempenho", href='/admin/page-1', color="primary", style={'margin': '10px'}),
        # Adicione mais botões para outras páginas de edição conforme necessário
    ], className="text-center"),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/admin/login', next_href='/admin/page-2')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Página Administrativa de Edição de Desempenho (/admin/page-1)
# Layout do Painel de Edição de Desempenho (Administrador)
admin_page_1_layout = html.Div([
    html.H1("Admin: Editar Desempenho", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),

    # Formulário de edição
    dbc.Form([
        dbc.Row([
            dbc.Label("Mês:", html_for="edit-mes", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dcc.Dropdown(
                    id='edit-mes',
                    options=[{'label': mes, 'value': mes} for mes in meses_completos],
                    value='Agosto',
                    clearable=False,
                    style={'font-size': '18px'}
                ),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Plataforma:", html_for="edit-plataforma", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dcc.Dropdown(
                    id='edit-plataforma',
                    options=[{'label': p, 'value': p} for p in ['Facebook Ads', 'Google Ads']],
                    value='Facebook Ads',
                    clearable=False,
                    style={'font-size': '18px'}
                ),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Impressões:", html_for="edit-impressao", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="number", id="edit-impressao", placeholder="Digite o número de impressões", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Cliques no Link:", html_for="edit-clique", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="number", id="edit-clique", placeholder="Digite o número de cliques no link", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Orçamento (R$):", html_for="edit-orcamento", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="number", id="edit-orcamento", placeholder="Digite o orçamento", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("CTR (%):", html_for="edit-ctr", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="number", step="0.01", id="edit-ctr", placeholder="Digite o CTR (%)", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("CPL (R$):", html_for="edit-cpl", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="number", step="0.01", id="edit-cpl", placeholder="Digite o CPL (R$)", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        
        # Novo Campo: Resultados
        dbc.Row([
            dbc.Label("Resultados:", html_for="edit-resultados", width=2, style={'font-size': '20px'}),  # Adiciona o label
            dbc.Col(
                dbc.Input(type="number", id="edit-resultados", placeholder="Digite o número de resultados", style={'font-size': '18px'}),  # Adiciona o campo de input para Resultados
                width=10,
            ),
        ], className="mb-3"),
        
        # Botão de salvar
        dbc.Button("Salvar", id="salvar-desempenho", color="primary", style={'font-size': '18px', 'width': '100%'}, className="mt-3")
    ], style={'width': '600px', 'margin': 'auto', 'margin-top': '50px'}),
    
    # Feedback de Edição
    html.Div(id='editar-feedback', style={'text-align': 'center', 'margin-top': '10px'}),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/admin', next_href='/admin/page-2')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 'background-color': secondary_color, 'padding': '20px', 'min-height': '100vh'})
# Layout específico para a página administrativa 3: Gerenciar Melhores Anúncios
# Layout da Página 3 para Gerenciar Melhores Anúncios
admin_page_3_layout = html.Div([
    html.H1("Gerenciar Melhores Anúncios", className="text-center",
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),

    # Seletor de Mês
    html.Div([
        html.Label('Selecionar Mês:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='mes-anuncio-dropdown',
            options=[{'label': mes, 'value': mes} for mes in meses_completos],
            value='Agosto',
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px'}),

    # Tabela para exibir e editar os anúncios existentes
    html.Div([
        html.H3("Editar Nome e CTR dos 5 Anúncios", className="text-center", style={'font-size': '24px', 'font-weight': '700'}),
        dash_table.DataTable(
            id='tabela-edicao-anuncios',
            columns=[
                {'name': 'Nome do Anúncio', 'id': 'nome_anuncio', 'editable': True},
                {'name': 'CTR (%)', 'id': 'ctr', 'editable': True}
            ],
            data=[{"nome_anuncio": "", "ctr": 0.0} for _ in range(5)],
            style_table={'margin': 'auto', 'width': '80%'},
            style_cell={'textAlign': 'center', 'padding': '5px', 'font-family': 'Montserrat, sans-serif'},
            style_header={'backgroundColor': primary_color, 'fontWeight': 'bold', 'color': 'white'},
            style_data={'backgroundColor': '#f9f9f9'},
            style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#e9e9e9'}]
        )
    ], style={'margin-top': '20px'}),

    # Link da Imagem e Visualização
    html.Div([
        html.Label("Link da Imagem para o Mês Selecionado:", style={'font-weight': 'bold', 'font-size': '16px'}),
        dbc.Input(id='input-link-imagem', type='text', placeholder='Digite o link da imagem...',
                  style={'width': '70%', 'margin': 'auto', 'display': 'block', 'font-size': '16px'}),
        # Exibir a imagem do link fornecido
        html.Div([
            html.H3("Prévia da Imagem dos Anúncios", className="text-center", style={'font-size': '24px', 'font-weight': '700'}),
            html.Img(id='imagem-preview-anuncios', src="", style={'max-width': '100%', 'height': 'auto', 'margin': 'auto'})
        ], style={'text-align': 'center', 'margin-top': '20px'})
    ], style={'margin-top': '30px', 'margin-bottom': '30px'}),

    # Botão para salvar as alterações
    html.Button('Salvar Alterações', id='btn-salvar-anuncios', n_clicks=0,
                style={'background-color': '#28a745', 'color': 'white', 'font-weight': 'bold',
                       'padding': '10px 20px', 'margin-top': '30px', 'display': 'block', 'margin': 'auto'}),

    # Feedback de atualização
    html.Div(id='feedback-anuncios', style={'margin-top': '20px', 'font-size': '18px', 'color': '#28a745'}),

    # Navegação entre páginas administrativas
    botoes_navegacao(prev_href='/admin/page-2', next_href='/admin/page-4')
], style={'padding': '20px', 'background-color': secondary_color})
admin_page_4_layout = html.Div([
    html.H1("Admin: Editar Cliques por Estado", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
    
    # Formulário de edição
    dbc.Form([
        # Selecionar Mês
        dbc.Row([
            dbc.Label("Mês:", html_for="edit-mes-cliques", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dcc.Dropdown(
                    id='edit-mes-cliques',
                    options=[{'label': mes, 'value': mes} for mes in meses_completos],
                    value='Agosto',
                    clearable=False,
                    style={'font-size': '18px'}
                ),
                width=10,
            ),
        ], className="mb-3"),
        
        # Tabela para inserir estados e cliques
        html.Div([
            dash_table.DataTable(
                id='tabela-cliques-estado',
                columns=[
                    {'name': 'Estado', 'id': 'estado', 'type': 'text', 'editable': True},
                    {'name': 'Cliques', 'id': 'cliques', 'type': 'numeric', 'editable': True}
                ],
                data=[{'estado': '', 'cliques': 0} for _ in range(10)],  # Até 10 estados
                row_deletable=False,
                style_table={'overflowX': 'auto', 'width': '100%'},
                style_cell={'textAlign': 'center', 'padding': '5px', 'font-family': 'Montserrat, sans-serif'},
                style_header={'backgroundColor': primary_color, 'fontWeight': 'bold', 'color': 'white'},
                style_data={'backgroundColor': '#f9f9f9'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#e9e9e9'}
                ]
            )
        ], style={'margin-top': '20px'}),
        
        # Botão de salvar
        dbc.Button("Salvar", id="salvar-cliques-estado", color="primary", 
                   style={'font-size': '18px', 'width': '100%', 'margin-top': '20px'}),
    ], style={'width': '800px', 'margin': 'auto', 'margin-top': '50px'}),
    
    # Feedback de Edição
    html.Div(id='editar-cliques-feedback', style={'text-align': 'center', 'margin-top': '10px'}),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/admin/page-3', next_href='/admin/page-5')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})
admin_page_5_layout = html.Div([
    html.H1("Admin: Editar Valores Individuais de Cada Produto", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
    
    # Formulário de edição
    dbc.Form([
        dbc.Row([
            dbc.Label("Produto:", html_for="edit-produto", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dcc.Dropdown(
                    id='edit-produto',
                    options=[{'label': produto, 'value': produto} for produto in ['Kit Plantio', 'Turbo Mix', 'Vollverini', 'Best Mix', 'Nitro Mix']],
                    value='Kit Plantio',
                    clearable=False,
                    style={'font-size': '18px'}
                ),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Mês:", html_for="edit-mes-produto", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dcc.Dropdown(
                    id='edit-mes-produto',
                    options=[{'label': mes, 'value': mes} for mes in meses_completos],
                    value='Agosto',
                    clearable=False,
                    style={'font-size': '18px'}
                ),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Valor Investido (R$):", html_for="edit-valor-investido", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="number", id="edit-valor-investido", placeholder="Digite o valor investido", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Retorno (R$):", html_for="edit-retorno", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="number", id="edit-retorno", placeholder="Digite o retorno", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        
        # Botão de salvar
        dbc.Button("Salvar", id="salvar-produto", color="primary", style={'font-size': '18px', 'width': '100%'}, className="mt-3")
    ], style={'width': '600px', 'margin': 'auto', 'margin-top': '50px'}),
    
    # Feedback de Edição
    html.Div(id='editar-produto-feedback', style={'text-align': 'center', 'margin-top': '10px'}),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/admin/page-4', next_href='/admin/page-6')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 'background-color': secondary_color, 'padding': '20px', 'min-height': '100vh'})
# Admin page 6 layout: Editar Funil de Vendas
# Página Administrativa de Edição de Funil de Vendas (/admin/page-6)
admin_page_6_layout = html.Div([
    html.H1("Admin: Editar Funil de Vendas", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
    
    # Formulário de edição
    dbc.Form([
        dbc.Row([
            dbc.Label("Mês:", html_for="edit-mes-funil", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dcc.Dropdown(
                    id='edit-mes-funil',
                    options=[{'label': mes, 'value': mes} for mes in meses_completos],
                    value='Agosto',
                    clearable=False,
                    style={'font-size': '18px'}
                ),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Leads Frios:", html_for="edit-leads-frios", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="number", id="edit-leads-frios", placeholder="Digite o número de Leads Frios", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Atendidos:", html_for="edit-atendidos", width=2, style={'font-size': '20px'}),
            dbc.Col(
                dbc.Input(type="number", id="edit-atendidos", placeholder="Digite o número de Atendidos", style={'font-size': '18px'}),
                width=10,
            ),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Label("Vendas:", html_for="edit-vendas", width=2, style={'font-size': '20px'}),  # Alterado de Conversões para Vendas
            dbc.Col(
                dbc.Input(type="number", id="edit-vendas", placeholder="Digite o número de Vendas", style={'font-size': '18px'}),  # ID alterado
                width=10,
            ),
        ], className="mb-3"),
        
        # Botão de salvar
        dbc.Button("Salvar", id="salvar-funil", color="primary", style={'font-size': '18px', 'width': '100%'}, className="mt-3")
    ], style={'width': '600px', 'margin': 'auto', 'margin-top': '50px'}),
    
    # Feedback de Edição
    html.Div(id='editar-funil-feedback', style={'text-align': 'center', 'margin-top': '10px'}),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/admin/page-5', next_href='/admin/page-7')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Definir os layouts para todas as páginas administrativas (/admin/page-2 a /admin/page-9)
admin_page_layouts = {
    '/admin/page-1': admin_page_1_layout,
    '/admin/page-2': html.Div([
        html.H1("Admin Página 2 - Em Desenvolvimento", className="text-center",
                style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
        html.P("Conteúdo da página administrativa.", style={'font-size': '20px', 'text-align': 'center'}),
        botoes_navegacao(prev_href='/admin/page-1', next_href='/admin/page-3')
    ], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif',
              'background-color': secondary_color, 'padding': '20px',
              'min-height': '100vh'}),
    '/admin/page-3': admin_page_3_layout,
    '/admin/page-4': admin_page_4_layout,  # Novo Layout Adicionado Aqui
    '/admin/page-5': admin_page_5_layout,
    '/admin/page-6': admin_page_6_layout,
    '/admin/page-7': html.Div([
        html.H1("Admin Página 7 - Em Desenvolvimento", className="text-center",
                style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
        html.P("Conteúdo da página administrativa.", style={'font-size': '20px', 'text-align': 'center'}),
        botoes_navegacao(prev_href='/admin/page-6', next_href='/admin/page-8')
    ], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif',
              'background-color': secondary_color, 'padding': '20px',
              'min-height': '100vh'}),
    '/admin/page-8': html.Div([
        html.H1("Admin Página 8 - Em Desenvolvimento", className="text-center",
                style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
        html.P("Conteúdo da página administrativa.", style={'font-size': '20px', 'text-align': 'center'}),
        botoes_navegacao(prev_href='/admin/page-7', next_href='/admin/page-9')
    ], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif',
              'background-color': secondary_color, 'padding': '20px',
              'min-height': '100vh'}),
    '/admin/page-9': html.Div([
        html.H1("Admin Página 9 - Em Desenvolvimento", className="text-center",
                style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
        html.P("Conteúdo da página administrativa.", style={'font-size': '20px', 'text-align': 'center'}),
        botoes_navegacao(prev_href='/admin/page-8', next_href='/admin')
    ], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif',
              'background-color': secondary_color, 'padding': '20px',
              'min-height': '100vh'}),
}
    
public_page_1_layout = html.Div([
    # Título da Página
    html.H1("Desempenho de Facebook e Google Ads", className="text-center",
            style={'font-size': '36px', 'font-weight': '700', 'color': primary_color}),

    # Seletor de Mês
    html.Div([
        html.Label('Selecionar Mês:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='mes-desempenho-dropdown',
            options=[{'label': mes, 'value': mes} for mes in meses_completos],
            value='Agosto',  # Valor padrão
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px'}),

    # Mensagem de erro
    html.Div(id='erro-msg', style={'color': 'red', 'font-size': '18px', 'text-align': 'center', 'margin-top': '10px'}),

    # Tabela de Desempenho
    html.Div([
        dash_table.DataTable(
            id='tabela-desempenho',
            columns=[
                {'name': 'Plataforma', 'id': 'Plataforma'},
                {'name': 'Impressões', 'id': 'Impressões'},
                {'name': 'Cliques no link', 'id': 'Cliques no link'},
                {'name': 'Resultados', 'id': 'Resultados'},
                {'name': 'Orçamento (R$)', 'id': 'Orçamento (R$)'},
                {'name': 'CTR (%)', 'id': 'CTR (%)'},
                {'name': 'CPL (R$)', 'id': 'CPL (R$)'}
            ],
            data=[],  # Preenchido dinamicamente
            style_table={'margin': 'auto', 'width': '80%'},
            style_cell={
                'textAlign': 'center',
                'padding': '8px',
                'font-family': 'Montserrat, sans-serif',
                'fontSize': '16px',  # Aumentar tamanho da fonte para destaque
                'border': '1px solid #ddd',
                'fontWeight': 'bold'  # Deixar texto e números em negrito
            },
            style_header={
                'backgroundColor': '#28a745',  # Verde padrão da Agross do Brasil
                'fontWeight': 'bold',
                'color': 'white',
                'fontSize': '18px'  # Tamanho da fonte do cabeçalho
            },
            style_data={'backgroundColor': '#f9f9f9'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#e9e9e9'}
            ]
        )
    ], style={'position': 'relative', 'height': 'auto', 'margin-top': '30px'}),

    # Quadros de Totais na Parte Inferior
    html.Div([
        html.Div([
            html.Div("Total de Impressões:", style={
                'font-weight': 'bold', 'font-size': '16px', 'margin-bottom': '5px'}),
            html.Div(id='total-impressao', style={
                'font-size': '20px', 'font-weight': 'bold'})
        ], style={
            'background-color': '#28a745', 'color': 'white', 'padding': '10px',
            'border-radius': '10px', 'margin': '10px', 'width': '180px', 'text-align': 'center'}),

        html.Div([
            html.Div("Total de Cliques no link:", style={
                'font-weight': 'bold', 'font-size': '16px', 'margin-bottom': '5px'}),
            html.Div(id='total-cliques', style={
                'font-size': '20px', 'font-weight': 'bold'})
        ], style={
            'background-color': '#007bff', 'color': 'white', 'padding': '10px',
            'border-radius': '10px', 'margin': '10px', 'width': '180px', 'text-align': 'center'}),

        html.Div([
            html.Div("Total de Resultados:", style={
                'font-weight': 'bold', 'font-size': '16px', 'margin-bottom': '5px'}),
            html.Div(id='total-resultados', style={
                'font-size': '20px', 'font-weight': 'bold'})
        ], style={
            'background-color': '#ffc107', 'color': 'white', 'padding': '10px',
            'border-radius': '10px', 'margin': '10px', 'width': '180px', 'text-align': 'center'}),

        html.Div([
            html.Div("Orçamento Total (R$):", style={
                'font-weight': 'bold', 'font-size': '16px', 'margin-bottom': '5px'}),
            html.Div(id='total-orcamento', style={
                'font-size': '20px', 'font-weight': 'bold'})
        ], style={
            'background-color': '#dc3545', 'color': 'white', 'padding': '10px',
            'border-radius': '10px', 'margin': '10px', 'width': '180px', 'text-align': 'center'}),
    ], style={
        'display': 'flex', 'justify-content': 'center', 'align-items': 'center',
        'margin-top': '150px'}),  # Posição mais baixa na tela

    # Botões de navegação entre páginas
    botoes_navegacao(prev_href='/', next_href='/page-2')
], style={
    'color': '#343a40', 'font-family': 'Montserrat, sans-serif',
    'background-color': secondary_color, 'padding': '20px',
    'min-height': '100vh'})
@app.callback(
    [Output('tabela-desempenho', 'data'),
     Output('total-impressao', 'children'),
     Output('total-cliques', 'children'),
     Output('total-resultados', 'children'),
     Output('total-orcamento', 'children'),
     Output('erro-msg', 'children')],
    [Input('mes-desempenho-dropdown', 'value')]
)
def update_tabela_e_totais(mes_selecionado):
    if not mes_selecionado:
        return [], "0", "0", "0", "0", "⚠️ Por favor, selecione um mês."

    try:
        # Obter os dados do Firebase para o mês especificado
        dados_mes = db.child("desempenho").child(mes_selecionado).get().val()

        if not dados_mes:
            return [], "0", "0", "0", "0", f"⚠️ Dados não encontrados para o mês {mes_selecionado}."

        # Estrutura de dados para preencher a tabela
        data = {
            'Plataforma': [],
            'Impressões': [],
            'Cliques no link': [],
            'Resultados': [],
            'Orçamento (R$)': [],
            'CTR (%)': [],
            'CPL (R$)': []
        }

        # Preencher os valores para cada plataforma
        total_impressao = 0
        total_cliques = 0
        total_resultado = 0
        total_orcamento = 0

        for plataforma, metrics in dados_mes.items():
            data['Plataforma'].append(plataforma)
            impressoes = float(metrics.get('Impressoes', 0))
            cliques = float(metrics.get('Cliques_no_link', 0))
            resultados = float(metrics.get('Resultados', 0))
            orcamento = float(metrics.get('Orcamento', 0))
            ctr = float(metrics.get('CTR', 0))
            cpl = float(metrics.get('CPL', 0))

            data['Impressões'].append(formatar_valor(metrica='Impressões', valor=impressoes))
            data['Cliques no link'].append(formatar_valor(metrica='Cliques no link', valor=cliques))
            data['Resultados'].append(formatar_valor(metrica='Resultados', valor=resultados))
            data['Orçamento (R$)'].append(formatar_valor(metrica='Orçamento (R$)', valor=orcamento))
            data['CTR (%)'].append(formatar_valor(metrica='CTR (%)', valor=ctr))
            data['CPL (R$)'].append(formatar_valor(metrica='CPL (R$)', valor=cpl))

            # Somar os totais para exibir nos quadros
            total_impressao += impressoes
            total_cliques += cliques
            total_resultado += resultados
            total_orcamento += orcamento

        # Aqui, você pode converter `data` para o formato esperado pela tabela
        # Supondo que `tabela-desempenho` espera uma lista de dicionários
        tabela_dados = []
        for i in range(len(data['Plataforma'])):
            tabela_dados.append({
                'Plataforma': data['Plataforma'][i],
                'Impressões': data['Impressões'][i],
                'Cliques no link': data['Cliques no link'][i],
                'Resultados': data['Resultados'][i],
                'Orçamento (R$)': data['Orçamento (R$)'][i],
                'CTR (%)': data['CTR (%)'][i],
                'CPL (R$)': data['CPL (R$)'][i]
            })

        return (
            tabela_dados, 
            f"{total_impressao:,.0f}".replace(",", "."), 
            f"{total_cliques:,.0f}".replace(",", "."), 
            f"{total_resultado:,.0f}".replace(",", "."), 
            f"R$ {total_orcamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
            ""
        )
    except Exception as e:
        logging.error(f"Erro ao carregar dados do Firebase: {e}")
        return [], "0", "0", "0", "0", f"⚠️ Erro ao carregar os dados: {str(e)}"
        
@app.callback(
    [Output('editar-produto-feedback', 'children')],
    [Input('salvar-produto', 'n_clicks')],
    [State('edit-produto', 'value'),
     State('edit-mes-produto', 'value'),
     State('edit-valor-investido', 'value'),
     State('edit-retorno', 'value')]
)
def salvar_dados_produto(n_clicks, produto, mes, valor_investido, retorno):
    if n_clicks and n_clicks > 0:
        if not all([produto, mes, valor_investido, retorno]):
            return [dbc.Alert("Por favor, preencha todos os campos.", color="danger")]
        try:
            dados_corrigidos = validar_chaves_e_valores({
                'Valor Investido (R$)': valor_investido,
                'Retorno (R$)': retorno
            })
            db.child("produtos").child(produto).child(mes).update(dados_corrigidos)
            feedback = dbc.Alert("Dados salvos com sucesso!", color="success")
            return [feedback]
        except Exception as e:
            feedback = dbc.Alert(f"Erro ao salvar os dados: {str(e)}", color="danger")
            return [feedback]
    return [dash.no_update]
@app.callback(
    [Output('editar-funil-feedback', 'children'),
     Output('edit-leads-frios', 'value'),
     Output('edit-atendidos', 'value'),
     Output('edit-vendas', 'value')],  # Alterado de 'edit-conversoes' para 'edit-vendas'
    [Input('salvar-funil', 'n_clicks'),
     Input('edit-mes-funil', 'value')],
    [State('edit-leads-frios', 'value'),
     State('edit-atendidos', 'value'),
     State('edit-vendas', 'value')]  # Alterado de 'edit-conversoes' para 'edit-vendas'
)
def salvar_ou_carregar_funil(n_clicks, mes, leads_frios, atendidos, vendas):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'edit-mes-funil' and mes:
        try:
            dados_mes = db.child("funil_vendas").child(mes).get().val()
            if dados_mes:
                leads_frios = dados_mes.get('Leads Frios', 0)
                atendidos = dados_mes.get('Atendidos', 0)
                vendas = dados_mes.get('Vendas', 0)  # Alterado de 'Conversões' para 'Vendas'
                return [dbc.Alert(f"Dados carregados para {mes}.", color="info")], leads_frios, atendidos, vendas
            else:
                return [dbc.Alert(f"Nenhum dado encontrado para {mes}.", color="warning")], None, None, None
        except Exception as e:
            return [dbc.Alert(f"Erro ao carregar dados: {str(e)}", color="danger")], None, None, None

    elif trigger_id == 'salvar-funil' and n_clicks > 0:
        try:
            if leads_frios is None or atendidos is None or vendas is None:
                return [dbc.Alert("Por favor, preencha todos os campos.", color="danger")], leads_frios, atendidos, vendas

            db.child("funil_vendas").child(mes).update({
                'Leads Frios': int(leads_frios),
                'Atendidos': int(atendidos),
                'Vendas': int(vendas)  # Alterado de 'Conversões' para 'Vendas'
            })
            return [dbc.Alert("Dados salvos com sucesso!", color="success")], leads_frios, atendidos, vendas
        except Exception as e:
            return [dbc.Alert(f"Erro ao salvar os dados: {str(e)}", color="danger")], leads_frios, atendidos, vendas

    return dash.no_update, leads_frios, atendidos, vendas
    
def load_produtos_data():
    dados_produtos = {
        'Mês': [],
        'Produto': [],
        'Valor Investido (R$)': [],
        'Retorno (R$)': []
    }
    
    try:
        produtos_data = db.child("produtos").get().val()
        logging.info(f"Dados carregados de 'produtos': {produtos_data}")
        
        if produtos_data:
            for produto, meses_data in produtos_data.items():
                for mes in meses_completos:
                    dados_produtos['Mês'].append(mes)
                    dados_produtos['Produto'].append(produto)
                    mes_data = meses_data.get(mes, {})
                    valor_investido = mes_data.get('Valor_Investido_R', 0)  # Chaves corrigidas
                    retorno = mes_data.get('Retorno_R', 0)  # Chaves corrigidas
                    dados_produtos['Valor Investido (R$)'].append(valor_investido)
                    dados_produtos['Retorno (R$)'].append(retorno)
        else:
            logging.warning("Nenhum dado encontrado para 'produtos' no Firebase.")
    except Exception as e:
        logging.error(f"Erro ao carregar dados de produtos do Firebase: {e}")
    
    df_produtos = pd.DataFrame(dados_produtos)
    logging.info(f"DataFrame de produtos:\n{df_produtos}")
    return dados_produtos

# Carregar os dados dos produtos
dados_produtos = load_produtos_data()
df_produtos = pd.DataFrame(dados_produtos)
def load_funil_data():
    df_funil = pd.DataFrame(columns=['Mês', 'Leads Frios', 'Atendidos', 'Vendas'])  # Alterado de 'Conversões' para 'Vendas'
    try:
        funil_data = db.child("funil_vendas").get().val()
        if funil_data:
            for mes in meses_completos:
                mes_data = funil_data.get(mes, {})
                leads_frios = mes_data.get('Leads Frios', 0)
                atendidos = mes_data.get('Atendidos', 0)
                vendas = mes_data.get('Vendas', 0)  # Alterado de 'Conversões' para 'Vendas'
                df_funil = pd.concat([df_funil, pd.DataFrame([{
    'Mês': mes,
    'Leads Frios': leads_frios,
    'Atendidos': atendidos,
    'Vendas': vendas
}])], ignore_index=True)
        else:
            print("Nenhum dado encontrado para 'funil_vendas' no Firebase.")
    except Exception as e:
        print(f"Erro ao carregar dados de funil_vendas do Firebase: {e}")
    return df_funil

# Carregar os dados do funil de vendas
df_funil = load_funil_data()

# Página 3: Comparação de Todos os Meses (/page-2)
public_page_2_layout = html.Div([
    html.H1("Comparação de Todos os Meses", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),

    # Seletor de Meses
    html.Div([
        html.Label('Selecionar Meses:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Checklist(
            id='mes-comparacao-checklist',
            options=[{'label': mes, 'value': mes} for mes in meses_completos],
            value=['Junho', 'Julho', 'Agosto', 'Setembro'],  # Seleção inicial
            inline=True,
            labelStyle={'margin-right': '15px', 'font-size': '18px'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px', 'margin-bottom': '20px'}),

    # Caixa de comentários (aparece conforme seleção)
    html.Div([
        dbc.Alert(
            id='comentario-box',
            children="",
            is_open=False,
            color="info",
            dismissable=True,
            style={'font-size': '18px', 'margin-bottom': '20px', 'border': '1px solid #ced4da', 'padding': '15px'}
        )
    ]),

    # Gráficos
    html.Div(id='graficos-metricas', style={'margin-bottom': '20px'}),

    # Explicação das Métricas com Caixa ao Redor
    html.Div([
        html.Div([
            html.H4("Explicação das Métricas", className="text-center", 
                    style={'font-size': '24px', 'color': primary_color, 'margin-bottom': '10px'}),
            dbc.ListGroup([
                dbc.ListGroupItem([
                    html.B("Impressões: "),
                    "Quantidade de vezes que o anúncio foi exibido.",
                    html.Br(),
                    html.I("Fórmula: Impressões = Total de exibições do anúncio.")
                ], style={'font-size': '18px'}),
                dbc.ListGroupItem([
                    html.B("Cliques no link: "),
                    "Quantidade de cliques no anúncio.",
                    html.Br(),
                    html.I("Fórmula: Cliques no link = Total de cliques no anúncio.")
                ], style={'font-size': '18px'}),
                dbc.ListGroupItem([
                    html.B("Resultados: "),
                    "Total de ações realizadas pelos usuários (conversões).",
                    html.Br(),
                    html.I("Fórmula: Resultados = Total de conversões obtidas.")
                ], style={'font-size': '18px'}),
                dbc.ListGroupItem([
                    html.B("CTR (%): "),
                    "Taxa de cliques.",
                    html.Br(),
                    html.I("Fórmula: CTR (%) = (Cliques / Impressões) × 100")
                ], style={'font-size': '18px'}),
                dbc.ListGroupItem([
                    html.B("CPL (R$): "),
                    "Custo por Lead.",
                    html.Br(),
                    html.I("Fórmula: CPL (R$) = Orçamento / Resultados")
                ], style={'font-size': '18px'}),
            ], flush=True, style={'font-size': '18px'})
        ], style={
            'border': '1px solid #ced4da',
            'padding': '20px',
            'border-radius': '5px',
            'background-color': '#FFFFFF'
        })
    ], style={'margin-top': '20px'}),

    # Botões de navegação
    botoes_navegacao(prev_href='/page-1', next_href='/page-3')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})


# Página 3: Melhores Anúncios (CTR) (/page-3)
public_page_3_layout = html.Div([
    html.H1("Melhores Anúncios (CTR)", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),

    # Selecionar Mês
    html.Div([
        html.Label('Selecionar Mês:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='mes-melhores-anuncios-dropdown',
            options=[{'label': mes, 'value': mes} for mes in ['Junho', 'Julho', 'Agosto', 'Setembro']],
            value='Agosto',
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px'}),

    # Tabela de melhores anúncios
    html.Div(id='tabela-melhores-anuncios', style={'margin-top': '30px', 'overflowX': 'auto', 'font-size': '18px'}),

    # Área para exibir a imagem associada
    html.Div([
        html.H3("Imagem dos Anúncios", className="text-center", style={'font-size': '24px', 'font-weight': '700'}),
        html.Img(id='imagem-preview-public', src="", style={'max-width': '100%', 'height': 'auto', 'margin': 'auto'})
    ], style={'text-align': 'center', 'margin-top': '30px'}),

    # Botões de navegação
    botoes_navegacao(prev_href='/page-2', next_href='/page-4')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})


# Página 4: Cliques por Estado (/page-4)
public_page_4_layout = html.Div([
    html.H1("Cliques por Estado", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),

    # Seletor de Mês
    html.Div([
        html.Label('Selecionar Mês:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='mes-cliques-dropdown',
            options=[{'label': mes, 'value': mes} for mes in meses_completos],
            value='Agosto',
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px'}),

    # Gráfico de Pizza
    html.Div([
        dcc.Graph(
            id='grafico-pizza-cliques'
        )
    ], style={'height': '600px', 'margin-top': '30px'}),

    # Caixa de texto explicativo com borda
    html.Div([
        dbc.Alert(
            id='comentario-cliques-box',
            children="",
            is_open=False,
            color="info",
            dismissable=True,
            style={'font-size': '18px', 'margin-bottom': '20px', 'border': '1px solid #ced4da', 'padding': '15px'}
        )
    ], style={'text-align': 'center'}),

    # Botões de navegação
    botoes_navegacao(prev_href='/page-3', next_href='/page-5')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})


# Página 6: Valores Individuais de Cada Produto (/page-5)
public_page_5_layout = html.Div([
    html.H1("Valores Individuais de Cada Produto", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Selecionar Produto
    html.Div([
        html.Label('Selecionar Produto:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='produto-select-dropdown',
            options=[{'label': produto, 'value': produto} for produto in df_produtos['Produto'].unique()],
            value='Kit Plantio',  # Valor inicial
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px'}),
    
    # Tabela de valores investidos, retornos e ROI
    html.Div([
        html.Div(id='tabela-produtos')
    ], style={'margin-top': '30px', 'overflowX': 'auto', 'font-size': '18px'}),
    
    # Caixa de texto explicativo
    html.Div([
        html.Div([
            html.P(
                "Esta tabela mostra os investimentos realizados em cada produto e os respectivos retornos obtidos. Analisar esses dados permite avaliar a eficácia dos investimentos e tomar decisões estratégicas para futuros lançamentos e campanhas.",
                style={'font-size': '18px', 'text-align': 'center'}
            )
        ], style={
            'border': '1px solid #ced4da',
            'padding': '20px',
            'border-radius': '5px',
            'background-color': '#FFFFFF',
            'max-width': '800px',
            'margin': '20px auto'
        })
    ], style={'margin-top': '20px'}),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/page-4', next_href='/page-6')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Página 7: Funil de Vendas (/page-6)
public_page_6_layout = html.Div([
    html.H1("Funil de Vendas", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Seletor de Mês
    html.Div([
        html.Label('Selecionar Mês:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='seletor-mes-funil',
            options=[{'label': mes, 'value': mes} for mes in meses_completos],
            value='Agosto',  # Valor inicial selecionado
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px'}),
    
    # Gráfico de Funil de Vendas em Barras (Horizontal) que será atualizado pelo callback
    html.Div([
        dcc.Graph(id='grafico-funil')
    ], style={'height': '600px', 'margin-bottom': '20px'}),
    
    # Taxa de Conversão destacada para o mês selecionado (inicialmente agosto)
    html.Div(id='taxa-conversao', style={'text-align': 'center', 'font-size': '24px', 'margin-top': '10px'}),
    
    # Caixa de texto explicativo
    html.Div([
        html.Div([
            html.P(
                "Este funil de vendas ilustra a jornada dos leads desde o estágio inicial até a conversão final. É uma ferramenta essencial para identificar gargalos e otimizar nosso processo de vendas.",
                style={'font-size': '18px', 'text-align': 'center'}
            )
        ], style={
            'border': '1px solid #ced4da',
            'padding': '20px',
            'border-radius': '5px',
            'background-color': '#FFFFFF',
            'max-width': '800px',
            'margin': '20px auto'
        })
    ], style={'margin-top': '20px'}),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/page-5', next_href='/page-7')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Página 8: Explicação de ROI e ROAS (/page-7)
public_page_7_layout = html.Div([
    html.H1("Explicação do ROI e ROAS", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Duas Tabelas Separadas
    dbc.Row([
        dbc.Col([
            dbc.Table([
                html.Thead(html.Tr([html.Th("ROI Externo")])),
                html.Tbody([
                    html.Tr([html.Td("Marketing Digital")]),
                    html.Tr([html.Td("Investimento: R$ 54.170,23")]),
                    html.Tr([html.Td("Retorno gerado: R$ 7.515.208,52")]),
                    html.Tr([html.Td("ROI = 13.771,37%")]),
                    html.Tr([html.Td("ROAS: R$ 138,74")]),
                    html.Tr([html.Td(
                        "Isso significa que para cada R$ 1 investido, gerou R$ 138,74 em receita, e o retorno sobre o investimento total foi de 13.771,37%."
                    )]),
                ])
            ], bordered=True, hover=True, responsive=True, striped=True, style={
                'background-color': '#FFFFFF',
                'color': '#343a40',
                'font-size': '18px',
                'margin-bottom': '20px'
            })
        ], md=6),
        dbc.Col([
            dbc.Table([
                html.Thead(html.Tr([html.Th("ROI Interno")])),
                html.Tbody([
                    html.Tr([html.Td("Marketing Digital")]),
                    html.Tr([html.Td("Faturamento interno (receita): R$ 2.497.224,63 (Kit e Máquinas)")]),
                    html.Tr([html.Td("Investimento total (custo): R$ 54.170,23")]),
                    html.Tr([html.Td("ROI: 4.508,98%")]),
                    html.Tr([html.Td("ROAS: R$ 46,09")]),
                    html.Tr([html.Td(
                        "Isso significa que para cada R$ 1 investido, você gerou R$ 46,09 em receita internamente, com um retorno sobre o investimento de 4.508,98%."
                    )]),
                ])
            ], bordered=True, hover=True, responsive=True, striped=True, style={
                'background-color': '#FFFFFF',
                'color': '#343a40',
                'font-size': '18px',
                'margin-bottom': '20px'
            })
        ], md=6)
    ], justify='center'),
    
    # Caixa de texto adicional no centro
    html.Div([
        html.Div([
            html.P(
                "Comentários adicionais sobre ROI e ROAS podem ser adicionados aqui para fornecer uma análise mais detalhada.",
                style={'font-size': '18px', 'text-align': 'center'}
            )
        ], style={
            'border': '1px solid #ced4da',
            'padding': '20px',
            'border-radius': '5px',
            'background-color': '#FFFFFF',
            'max-width': '800px',
            'margin': '20px auto'
        })
    ]),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/page-6', next_href='/page-8')  # Próximo slide será page-8
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

public_page_8_layout = html.Div([
    html.H1("Média dos Totais de Desempenho de Facebook e Google Ads", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Seletor de Métrica
    html.Div([
        html.Label('Selecionar Métrica:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='seletor-metrica-media',
            options=[
                {'label': 'Impressões', 'value': 'Impressões'},
                {'label': 'Cliques no link', 'value': 'Cliques no link'},
                {'label': 'Resultados', 'value': 'Resultados'},
                {'label': 'Orçamento (R$)', 'value': 'Orçamento (R$)'},
                {'label': 'CTR (%)', 'value': 'CTR (%)'},
                {'label': 'CPL (R$)', 'value': 'CPL (R$)'}
            ],
            value='Impressões',
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px', 'margin-bottom': '20px'}),
    
    # Gráfico único com 12 barras verticais para cada plataforma
    html.Div([
        dcc.Graph(
            id='grafico-media-totais'
        )
    ], style={'overflowX': 'auto'}),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/page-7', next_href='/')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})
@app.callback(
    Output('editar-cliques-feedback', 'children'),
    [Input('salvar-cliques-estado', 'n_clicks')],
    [State('edit-mes-cliques', 'value'),
     State('tabela-cliques-estado', 'data')]
)
def salvar_cliques_estado(n_clicks, mes, dados_cliques):
    if n_clicks and n_clicks > 0:
        if not mes:
            return dbc.Alert("Por favor, selecione um mês.", color="danger")
        
        # Filtrar apenas linhas com estado preenchido
        dados_filtrados = [d for d in dados_cliques if d['estado'].strip() != '']
        
        if not dados_filtrados:
            return dbc.Alert("Por favor, preencha pelo menos um estado.", color="danger")
        
        try:
            # Estrutura para salvar no Firebase
            cliques_data = {d['estado']: int(d['cliques']) for d in dados_filtrados}
            
            # Limitar a 10 estados
            if len(cliques_data) > 10:
                return dbc.Alert("Limite de 10 estados atingido. Por favor, remova alguns.", color="danger")
            
            # Salvar os dados no Firebase sob "cliques_por_estado/{mes}"
            db.child("cliques_por_estado").child(mes).set(cliques_data)
            
            return dbc.Alert("Dados salvos com sucesso!", color="success")
        except Exception as e:
            return dbc.Alert(f"Erro ao salvar os dados: {str(e)}", color="danger")
    
    return ""
# Função para gerar os botões de navegação fixos
# Layout do Modo Visualizador para Exibir os Melhores Anúncios
visualizador_layout = html.Div([
    html.H1("Visualizar Melhores Anúncios", className="text-center",
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),

    # Seletor de Mês
    html.Div([
        html.Label('Selecionar Mês:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='mes-visualizador-dropdown',
            options=[{'label': mes, 'value': mes} for mes in meses_completos],
            value='Agosto',
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px'}),

    # Tabela para exibir anúncios
    html.Div([
        html.H3("Top 5 Anúncios do Mês", className="text-center", style={'font-size': '24px', 'font-weight': '700'}),
        dash_table.DataTable(
            id='tabela-visualizador-anuncios',
            columns=[
                {'name': 'Nome do Anúncio', 'id': 'nome_anuncio'},
                {'name': 'CTR (%)', 'id': 'ctr'}
            ],
            data=[{"nome_anuncio": "", "ctr": 0.0} for _ in range(5)],
            style_table={'margin': 'auto', 'width': '80%'},
            style_cell={'textAlign': 'center', 'padding': '10px', 'font-family': 'Montserrat, sans-serif'},
            style_header={'backgroundColor': primary_color, 'fontWeight': 'bold', 'color': 'white'},
            style_data={'backgroundColor': '#f9f9f9'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#e9e9e9'}
            ]
        )
    ], style={'margin-top': '20px'}),

    # Imagem de visualização
    html.Div([
        html.H3("Imagem dos Melhores Anúncios", className="text-center", style={'font-size': '24px', 'font-weight': '700'}),
        html.Img(id='imagem-preview-visualizador', src="", style={'width': '70%', 'display': 'block', 'margin': 'auto'}),
    ], style={'margin-top': '30px'}),

    # Feedback
    html.Div(id='feedback-visualizador', style={'margin-top': '20px', 'font-size': '18px', 'color': '#28a745'})
], style={'padding': '20px', 'background-color': secondary_color})

# Layout da aplicação
# Definição do layout base do aplicativo
app.layout = html.Div([
    dcc.Store(id='auth-state', data={'authenticated': False}),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className="container", style={'position': 'relative', 'padding': '20px'})
], style={'backgroundColor': secondary_color, 'font-family': 'Montserrat, sans-serif', 'color': '#343a40'})

# Callback para carregar e editar os melhores anúncios
@app.callback(
    [Output('tabela-edicao-anuncios', 'data'),
     Output('input-link-imagem', 'value'),
     Output('imagem-preview-anuncios', 'src'),
     Output('feedback-anuncios', 'children')],
    [Input('mes-anuncio-dropdown', 'value'),
     Input('btn-salvar-anuncios', 'n_clicks')],
    [State('tabela-edicao-anuncios', 'data'),
     State('input-link-imagem', 'value')]
)

def carregar_editar_anuncios(mes_selecionado, n_clicks, anuncios_atualizados, link_imagem):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Se um mês foi selecionado, buscar os dados no Firebase
    if trigger_id == 'mes-anuncio-dropdown':
        try:
            # Carregar os 5 melhores anúncios do Firebase para o mês selecionado
            anuncios_firebase = db.child("melhores_anuncios").child(mes_selecionado).get().val()
            imagem_firebase = db.child("imagens_melhores_anuncios").child(mes_selecionado).get().val()  # Pegar imagem associada

            if anuncios_firebase:
                # Atualizar a tabela e o link com os dados carregados
                anuncios = [{"nome_anuncio": anuncios_firebase[f"Anuncio_{i+1}"]['nome'],
                             "ctr": anuncios_firebase[f"Anuncio_{i+1}"]['CTR']} for i in range(5)]
                # Link da imagem do Firebase
                link_imagem = imagem_firebase if imagem_firebase else ""
                return anuncios, link_imagem, link_imagem, ""
            else:
                # Retornar uma tabela vazia e link em branco se não houver dados
                return [{"nome_anuncio": "", "ctr": 0.0} for _ in range(5)], "", "", "Nenhum dado encontrado para o mês selecionado."

        except Exception as e:
            return [{"nome_anuncio": "", "ctr": 0.0} for _ in range(5)], "", "", f"Erro ao carregar os dados: {str(e)}"

    # Se o botão de salvar foi clicado, atualizar os dados no Firebase
    elif trigger_id == 'btn-salvar-anuncios' and n_clicks > 0:
        try:
            # Salvar os dados no Firebase
            dados_salvar = {
                f"Anuncio_{i+1}": {"nome": anuncios_atualizados[i]["nome_anuncio"], "CTR": anuncios_atualizados[i]["ctr"]}
                for i in range(5)
            }
            
            # Atualizar a imagem associada ao mês
            db.child("melhores_anuncios").child(mes_selecionado).set(dados_salvar)
            db.child("imagens_melhores_anuncios").child(mes_selecionado).set(link_imagem)  # Salvar o link da imagem separadamente

            return anuncios_atualizados, link_imagem, link_imagem, "Dados atualizados com sucesso!"
        except Exception as e:
            return anuncios_atualizados, link_imagem, link_imagem, f"Erro ao salvar os dados: {str(e)}"

    # Estado padrão quando não há alteração
    return anuncios_atualizados, link_imagem, link_imagem, ""


# Callback para alterar a página de acordo com a URL e autenticação
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('auth-state', 'data')]
)
def display_page(pathname, auth_state):
    print(f"Current Pathname: {pathname}")  # Para verificar o caminho atual
    print(f"Authentication State: {auth_state}")  # Para verificar se está autenticado

    # Definição das páginas públicas
    public_pages = {
        '/': public_home_layout,
        '/page-1': public_page_1_layout,
        '/page-2': public_page_2_layout,
        '/page-3': public_page_3_layout,
        '/page-4': public_page_4_layout,
        '/page-5': public_page_5_layout,
        '/page-6': public_page_6_layout,
        '/page-7': public_page_7_layout,
        '/page-8': public_page_8_layout,
        '/visualizador': visualizador_layout  # Adicione o modo visualizador aqui
    }

    # Definição das páginas administrativas
    admin_pages = {
        '/admin/login': admin_login_layout,
        '/admin': admin_dashboard_layout,
        '/admin/page-1': admin_page_1_layout,
        '/admin/page-2': admin_page_layouts.get('/admin/page-2'),
        '/admin/page-3': admin_page_layouts.get('/admin/page-3'),
        '/admin/page-4': admin_page_layouts.get('/admin/page-4'),
        '/admin/page-5': admin_page_layouts.get('/admin/page-5'),
        '/admin/page-6': admin_page_layouts.get('/admin/page-6'),
        '/admin/page-7': admin_page_layouts.get('/admin/page-7'),
        '/admin/page-8': admin_page_layouts.get('/admin/page-8'),
        '/admin/page-9': admin_page_layouts.get('/admin/page-9'),
    }

    # Verificar se a página é administrativa e o usuário está autenticado
    if pathname.startswith('/admin'):
        if auth_state and auth_state.get('authenticated'):
            # Retornar a página administrativa correspondente, se autenticado
            return admin_pages.get(pathname, html.Div([
                html.H1("Página Não Encontrada", className="text-center",
                        style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
                botoes_navegacao(prev_href='/admin', next_href='/admin')
            ], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif',
                      'background-color': secondary_color, 'padding': '20px',
                      'min-height': '100vh'}))
        else:
            # Redirecionar para a tela de login administrativa se não estiver autenticado
            return admin_login_layout

    # Se a página for pública, retornar o layout correspondente
    return public_pages.get(pathname, html.Div([
        html.H1("Página Não Encontrada", className="text-center",
                style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
        botoes_navegacao(prev_href='/', next_href='/')
    ], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif',
              'background-color': secondary_color, 'padding': '20px',
              'min-height': '100vh'}))


# Callback para autenticação e redirecionamento para o dashboard administrativo após login
@app.callback(
    [Output('auth-state', 'data'),
     Output('login-feedback', 'children'),
     Output('url', 'pathname')],
    [Input('botao-login', 'n_clicks')],
    [State('input-usuario', 'value'),
     State('input-senha', 'value'),
     State('auth-state', 'data')]
)
# Função para autenticar sem a necessidade de email e senha
def autenticar_usuario(n_clicks, usuario, senha, auth_state):
    if n_clicks and n_clicks > 0:
        # Valida se o usuário e a senha foram preenchidos
        if not usuario or not senha:
            return auth_state, dbc.Alert("Por favor, preencha todos os campos.", color="danger"), dash.no_update

        try:
            # Buscar o usuário diretamente no Realtime Database
            usuario_data = db.child("usuarios").child(usuario).get().val()
            
            # Verifica se o usuário existe e se a senha é correspondente
            if usuario_data and usuario_data.get("senha") == senha:
                auth_state['authenticated'] = True
                return auth_state, dbc.Alert("Login bem-sucedido!", color="success"), '/admin'
            else:
                return auth_state, dbc.Alert("Usuário ou senha incorretos.", color="danger"), dash.no_update
        except Exception as e:
            return auth_state, dbc.Alert(f"Erro ao conectar ao banco de dados: {str(e)}", color="danger"), dash.no_update
    
    return dash.no_update, "", dash.no_update



import logging

# Configuração de logging para identificar erros e processos durante a execução
logging.basicConfig(level=logging.INFO)
def validar_chaves_e_valores(dados):
    dados_corrigidos = {}
    for chave, valor in dados.items():
        # Remover caracteres inválidos
        chave_corrigida = chave.replace(" ", "_").replace("(", "").replace(")", "").replace("$", "")
        
        # Validar tipos de valores
        if isinstance(valor, (float, int)) and pd.notna(valor):
            dados_corrigidos[chave_corrigida] = float(valor)
        elif isinstance(valor, str) and valor.strip() != "":
            dados_corrigidos[chave_corrigida] = valor.strip()
        else:
            # Definir um valor padrão ou omitir a chave
            dados_corrigidos[chave_corrigida] = 0.0

    return dados_corrigidos

# Callback para carregar ou salvar dados no painel de administração
@app.callback(
    [Output('editar-feedback', 'children'),
     Output('edit-impressao', 'value'),
     Output('edit-clique', 'value'),
     Output('edit-orcamento', 'value'),
     Output('edit-ctr', 'value'),
     Output('edit-cpl', 'value'),
     Output('edit-resultados', 'value')],
    [Input('salvar-desempenho', 'n_clicks'),
     Input('edit-mes', 'value'),
     Input('edit-plataforma', 'value')],
    [State('edit-impressao', 'value'),
     State('edit-clique', 'value'),
     State('edit-orcamento', 'value'),
     State('edit-ctr', 'value'),
     State('edit-cpl', 'value'),
     State('edit-resultados', 'value')]
)
def salvar_ou_carregar_dados(n_clicks, mes, plataforma, impressao, clique, orcamento, ctr, cpl, resultados):
    # Obter o contexto do callback
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Caso o usuário tenha selecionado um mês ou plataforma, carregar os dados existentes
    if trigger_id in ['edit-mes', 'edit-plataforma'] and mes and plataforma:
        try:
            # Chama a função para carregar dados do Firebase
            dados_carregados = carregar_dados_existentes(mes, plataforma)
            
            # Se os dados foram carregados com sucesso, retornar os valores para os campos
            if dados_carregados:
                return [dbc.Alert(f"Dados carregados para {mes} - {plataforma}.", color="info")] + list(dados_carregados)
            else:
                # Caso não haja dados, retornar alert e valores nulos
                return [dbc.Alert(f"Nenhum dado encontrado para {mes} - {plataforma}.", color="warning")] + [None] * 6

        except Exception as e:
            # Captura de exceção e retorno com mensagem de erro
            return [dbc.Alert(f"Erro ao carregar dados: {str(e)}", color="danger")] + [None] * 6

    # Caso o botão de salvar tenha sido pressionado
    elif trigger_id == 'salvar-desempenho' and n_clicks > 0:
        try:
            # Validar se todos os campos foram preenchidos corretamente
            if not all([impressao, clique, orcamento, ctr, cpl, resultados]):
                return [dbc.Alert("Todos os campos devem ser preenchidos.", color="danger")] + [impressao, clique, orcamento, ctr, cpl, resultados]

            # Preparar os dados a serem atualizados no Firebase
            dados_atualizados = {
                "Impressoes": int(impressao),
                "Cliques_no_link": int(clique),
                "Resultados": int(resultados),
                "Orcamento": float(orcamento),
                "CTR": float(ctr),
                "CPL": float(cpl)
            }

            # Atualizar os dados no Firebase
            db.child("desempenho").child(mes).child(plataforma).update(dados_atualizados)

            return [dbc.Alert("Dados atualizados com sucesso!", color="success")] + [impressao, clique, orcamento, ctr, cpl, resultados]

        except Exception as e:
            return [dbc.Alert(f"Erro ao salvar os dados: {str(e)}", color="danger")] + [impressao, clique, orcamento, ctr, cpl, resultados]

    # Se nenhuma condição foi atendida, retornar os valores atuais
    return dash.no_update, impressao, clique, orcamento, ctr, cpl, resultados

@app.callback(
    Output('tabela-desempenho', 'children'),
    [Input('mes-desempenho-dropdown', 'value')]  # Certifique-se de que o dropdown correto está como input
)
def atualizar_tabela_desempenho(mes_selecionado):
    # Verificar se o mês foi selecionado
    if not mes_selecionado:
        return html.Div("Selecione um mês para visualizar as métricas.", style={'color': 'red', 'font-size': '20px', 'text-align': 'center'})

    # Carregar dados do Firebase para o mês selecionado
    try:
        # Verificar se os dados do mês estão no Firebase
        dados_mes_firebase = db.child("desempenho").child(mes_selecionado).get().val()
        
        if not dados_mes_firebase:
            logging.warning(f"Não há dados para o mês {mes_selecionado} no Firebase.")
            return html.Div(f"Não há dados para o mês {mes_selecionado}.", style={'color': 'red', 'font-size': '20px', 'text-align': 'center'})

        # Criar um DataFrame a partir dos dados do Firebase
        df_mes = pd.DataFrame(dados_mes_firebase).T  # Transpor para organizar por plataforma
        df_mes.reset_index(inplace=True)
        
        # Ajustar os nomes das colunas conforme o mapeamento
        df_mes = ajustar_nomes_metricas(df_mes)
        
        # Adicionar a coluna "Mês" para identificação
        df_mes['Mês'] = mes_selecionado
        logging.info(f"Dados carregados para o mês {mes_selecionado}: {df_mes}")

    except Exception as e:
        logging.error(f"Erro ao carregar dados do Firebase: {e}")
        return html.Div(f"Erro ao carregar dados do mês {mes_selecionado}.", style={'color': 'red', 'font-size': '20px', 'text-align': 'center'})

    # Criar um dicionário para mapear métricas esperadas
    metricas = ['Impressões', 'Cliques no link', 'Resultados', 'Orçamento (R$)', 'CTR (%)', 'CPL (R$)']

    # Verificar se as métricas esperadas estão no DataFrame
    for metrica in metricas:
        if metrica not in df_mes.columns:
            logging.warning(f"Métrica {metrica} não encontrada no DataFrame.")
            return html.Div(f"Erro: Métrica '{metrica}' não encontrada no DataFrame.", style={'color': 'red', 'font-size': '20px', 'text-align': 'center'})

    # Preparar os dados para a tabela
    dados_tabela = {'Métrica': metricas}
    for plataforma in df_mes['index'].unique():
        valores = []
        for metrica in metricas:
            valor = df_mes[df_mes['index'] == plataforma][metrica].values
            if valor.size > 0 and not pd.isna(valor[0]):
                valores.append(formatar_valor(metrica=metrica, valor=valor[0]))
            else:
                valores.append('')  # Substituir valores ausentes por string vazia
        dados_tabela[f'{plataforma}'] = valores

    # Criar o DataFrame final para a tabela
    df_tabela = pd.DataFrame(dados_tabela)
    
    # Calcular os totais de gastos
    total_facebook = df_mes[df_mes['index'] == 'Facebook Ads']['Orçamento (R$)'].values
    total_facebook = total_facebook[0] if total_facebook.size > 0 and not pd.isna(total_facebook[0]) else 0.0
    
    total_google = df_mes[df_mes['index'] == 'Google Ads']['Orçamento (R$)'].values
    total_google = total_google[0] if total_google.size > 0 and not pd.isna(total_google[0]) else 0.0

    total_spend = total_facebook + total_google

    # Calcular o Total de Resultados (soma dos resultados de Facebook e Google)
    total_resultado_facebook = df_mes[df_mes['index'] == 'Facebook Ads']['Resultados'].values
    total_resultado_facebook = total_resultado_facebook[0] if total_resultado_facebook.size > 0 and not pd.isna(total_resultado_facebook[0]) else 0

    total_resultado_google = df_mes[df_mes['index'] == 'Google Ads']['Resultados'].values
    total_resultado_google = total_resultado_google[0] if total_resultado_google.size > 0 and not pd.isna(total_resultado_google[0]) else 0

    total_resultado = total_resultado_facebook + total_resultado_google

    # Gerar a tabela com os dados e totais
    tabela = gerar_tabela_desempenho(df_tabela, total_facebook, total_google, total_spend, total_resultado)
    
    return tabela


# Adicionar logs para cada nível dos dados do Firebase
@app.callback(
    [Output('graficos-metricas', 'children'),
     Output('comentario-box', 'children'),
     Output('comentario-box', 'is_open')],
    [Input('mes-comparacao-checklist', 'value')]
)

def update_graphs(meses_selecionados):
    if not meses_selecionados:
        return [], "", False

    # Definir as métricas esperadas para o gráfico
    metricas = ['Impressões', 'Cliques no link', 'Resultados', 'Orçamento (R$)', 'CTR (%)', 'CPL (R$)']

    # Dicionário para armazenar os dados completos coletados do Firebase
    dados_completos = {
        'Plataforma': [],
        'Mês': [],
        'Impressões': [],
        'Cliques no link': [],
        'Resultados': [],
        'Orçamento (R$)': [],
        'CTR (%)': [],
        'CPL (R$)': []
    }

    # Buscar os dados do Firebase para cada mês selecionado
    for mes in meses_selecionados:
        try:
            print(f"📅 Carregando dados para o mês: {mes}...")
            dados_mes_firebase = db.child("desempenho").child(mes).get().val()
            print(f"📊 Dados brutos para o mês {mes}: {dados_mes_firebase}")

            if not dados_mes_firebase:
                print(f"⚠️  Não há dados para o mês {mes} no Firebase.")
                continue  # Se não há dados, pular para o próximo mês

            # Verificar a estrutura completa dos dados
            print(f"🔍 Estrutura dos dados para {mes}: {dados_mes_firebase}")

            # Processar dados de cada plataforma (Facebook Ads e Google Ads)
            for plataforma, dados in dados_mes_firebase.items():
                print(f"➡️ Plataforma: {plataforma} encontrada.")
                print(f"🔹 Dados brutos para {plataforma} no mês {mes}: {dados}")
                # Adicionar mês e plataforma aos dados
                dados_completos['Plataforma'].append(plataforma)
                dados_completos['Mês'].append(mes)

                # Adicionar cada métrica específica, preenchendo com zero se estiver faltando
                for metrica in metricas:
                    chave_firebase = mapa_metricas_firebase.get(metrica, metrica)  # Usar o mapeamento atualizado
                    valor = dados.get(chave_firebase, None)

                    if valor is None:
                        print(f"❓ Métrica '{chave_firebase}' não encontrada para '{plataforma}' no mês {mes}.")
                        valor = 0  # Definir valor como 0 para métricas faltantes

                    valor_final = valor if pd.notna(valor) else 0
                    dados_completos[metrica].append(valor_final)
                    print(f"🔢 Mês: {mes}, Plataforma: {plataforma}, Métrica: {metrica}, Valor: {valor_final}")

        except Exception as e:
            print(f"⚠️  Erro ao buscar dados para o mês {mes}: {str(e)}")

    # Converter os dados completos para um DataFrame
    df_firebase = pd.DataFrame(dados_completos)

    if df_firebase.empty:
        print("⚠️ DataFrame vazio. Não há dados para exibir.")
        return [], html.Div("Sem dados para os meses selecionados."), False

    # Verificar se as colunas do DataFrame correspondem aos nomes esperados
    print(f"🔍 Colunas do DataFrame: {df_firebase.columns}")
    print(f"🔍 Dados do DataFrame:\n{df_firebase}")

    graficos = []
    for metrica in metricas:
        df_plot = df_firebase[['Plataforma', 'Mês', metrica]].dropna()

        if df_plot.empty:
            print(f"⚠️ Sem dados para a métrica: {metrica} nos meses selecionados.")
            continue

        plataformas = ['Facebook Ads', 'Google Ads']
        complete_data = pd.DataFrame([(plataforma, mes) for plataforma in plataformas for mes in meses_selecionados],
                                     columns=['Plataforma', 'Mês'])
        df_plot = complete_data.merge(df_plot, on=['Plataforma', 'Mês'], how='left').fillna(0)

        fig = px.bar(
            df_plot,
            x='Mês',
            y=metrica,
            color='Plataforma',
            barmode='group',
            title=f"{metrica} - Comparação de Todos os Meses",
            labels={metrica: metrica, 'Mês': 'Mês'},
            height=300
        )
        fig.update_layout(
    plot_bgcolor=secondary_color,  # Cor de fundo do gráfico
    paper_bgcolor=secondary_color,  # Cor de fundo geral
    font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),  # Fonte do gráfico
    title_x=0.5
        )
        fig.update_traces(texttemplate='%{y:,}', textposition='outside', textfont_size=16)

        graficos.append(html.Div([
            html.H4(metrica, className="text-center", style={'color': primary_color, 'font-size': '24px'}),
            dcc.Graph(figure=fig)
        ], style={'margin-bottom': '30px'}))

    return graficos, html.Div("No mês de Agosto tivemos uma alta em todas as métricas pelos eventos"), True



# Callback para atualizar o gráfico de cliques por estado com base no mês selecionado (/page-4)
@app.callback(
    [Output('grafico-pizza-cliques', 'figure'),
     Output('comentario-cliques-box', 'children'),
     Output('comentario-cliques-box', 'is_open')],
    [Input('mes-cliques-dropdown', 'value')]
)
def update_cliques_pais(mes_selecionado):
    # Criar o gráfico de cliques por estado
    fig = criar_grafico_cliques_estado(mes_selecionado)
    
    # Comentários personalizados para cada mês (opcional)
    # Você pode personalizar os comentários conforme os dados ou eventos específicos
    if mes_selecionado == 'Agosto':
        comentario_text = "Em agosto, a participação em feiras nos estados do PR e RS aumentaram significativamente os cliques provenientes dessas regiões."
    elif mes_selecionado == 'Setembro':
        comentario_text = "Em setembro, observamos uma queda nos cliques devido à menor presença em eventos físicos."
    elif mes_selecionado == 'Junho':
        comentario_text = "Em junho, tivemos um começo de campanha com um bom número de cliques provenientes de diferentes estados."
    elif mes_selecionado == 'Julho':
        comentario_text = "Em julho, mantivemos um fluxo estável de cliques, com destaque para as campanhas em Santa Catarina."
    else:
        comentario_text = f"Não há dados disponíveis para o mês de {mes_selecionado}."
    
    comentario = html.Div([html.P(comentario_text, style={'font-size': '18px', 'text-align': 'center'})])
    
    return fig, comentario, True

# Callback para atualizar a tabela de produtos com base no produto selecionado (/page-5)
@app.callback(
    Output('tabela-produtos', 'children'),
    [Input('produto-select-dropdown', 'value')]
)
def atualizar_tabela_produtos(produto_selecionado):
    logging.info(f"Produto selecionado: {produto_selecionado}")
    df_produto = df_produtos[df_produtos['Produto'] == produto_selecionado].copy()
    logging.info(f"Dados filtrados para {produto_selecionado}:\n{df_produto}")
    df_produto_formatado = formatar_valores(df_produto)
    tabela = gerar_tabela(df_produto_formatado)
    return tabela
@app.callback(
    Output('grafico-media-totais', 'figure'),
    [Input('seletor-metrica-media', 'value')]
)

def update_grafico_media(metrica_selecionada):
    try:
        # Buscar os dados de 'desempenho' no Firebase
        dados_desempenho = db.child("desempenho").get().val()
        
        if not dados_desempenho:
            logging.warning("Nenhum dado encontrado em 'desempenho'.")
            return px.bar(title="Nenhum dado disponível.")
        
        # Lista para armazenar os dados para o gráfico
        dados_para_grafico = {
            'Mês': [],
            'Plataforma': [],
            'Valor': []
        }
        
        # Definir a ordem dos meses
        ordem_meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        
        # Definir o mapeamento para 'desempenho'
        mapa_metricas_desempenho = {
            'Impressões': 'Impressoes',
            'Cliques no link': 'Cliques_no_link',
            'Resultados': 'Resultados',
            'Orçamento (R$)': 'Orcamento',
            'CTR (%)': 'CTR',
            'CPL (R$)': 'CPL'
        }
        
        # Verificar se a métrica selecionada está no mapeamento
        chave_firebase = mapa_metricas_desempenho.get(metrica_selecionada)
        if not chave_firebase:
            logging.warning(f"Métrica selecionada inválida: {metrica_selecionada}")
            return px.bar(title=f"Métrica inválida: {metrica_selecionada}")
        
        # Iterar sobre cada mês na ordem definida
        for mes in ordem_meses:
            if mes in dados_desempenho:
                plataformas = dados_desempenho[mes]
                for plataforma, metrics in plataformas.items():
                    valor = metrics.get(chave_firebase, 0)
                    
                    # Converter valor para float se possível
                    try:
                        valor = float(valor)
                    except (ValueError, TypeError):
                        valor = 0.0
                    
                    dados_para_grafico['Mês'].append(mes)
                    dados_para_grafico['Plataforma'].append(plataforma)
                    dados_para_grafico['Valor'].append(valor)
        
        # Criar DataFrame e ordenar os meses
        df_grafico = pd.DataFrame(dados_para_grafico)
        df_grafico['Mês'] = pd.Categorical(df_grafico['Mês'], categories=ordem_meses, ordered=True)
        df_grafico = df_grafico.sort_values('Mês')
        
        # Log dos dados para verificação
        logging.info(f"Dados para o gráfico ({metrica_selecionada}):\n{df_grafico}")
        
        # Definir o formato correto com base na métrica selecionada
        if "R$" in metrica_selecionada:
            fig_title = f"{metrica_selecionada} - Média dos Totais"
            text_template = 'R$ %{y:,.2f}'
        elif "%" in metrica_selecionada:
            fig_title = f"{metrica_selecionada} - Média dos Totais"
            text_template = '%{y:.2f}%'
        else:
            fig_title = f"{metrica_selecionada} - Média dos Totais"
            text_template = '%{y:,}'  # Formato para números inteiros (como Impressões)
            df_grafico['Valor'] = df_grafico['Valor'].astype(int)
        
        # Filtrar apenas a métrica selecionada
        df_filtrado = df_grafico.copy()
        
        if df_filtrado.empty:
            logging.warning(f"Nenhum dado encontrado para a métrica selecionada: {metrica_selecionada}")
            return px.bar(title=f"Nenhum dado disponível para a métrica: {metrica_selecionada}")
        
        # Criar o gráfico de barras
        fig = px.bar(
            df_filtrado,
            x='Mês',
            y='Valor',
            color='Plataforma',
            barmode='group',
            title=fig_title,
            labels={'Valor': metrica_selecionada, 'Mês': 'Mês'},
            text='Valor',
            height=500
        )
        
        # Atualizar layout do gráfico
        fig.update_layout(
            plot_bgcolor=secondary_color,
            paper_bgcolor=secondary_color,
            font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
            title_x=0.5
        )
        
        # Formatar o texto nos eixos usando 'texttemplate'
        fig.update_traces(texttemplate=text_template, textposition='outside')
        
        return fig
    
    except Exception as e:
        logging.error(f"Erro no callback de 'grafico-media-totais': {e}")
        return px.bar(title="Erro ao carregar os dados.")


  

# Callback para atualizar o gráfico e a taxa de conversão no Funil de Vendas (/page-6)
@app.callback(
    [Output('grafico-funil', 'figure'),
     Output('taxa-conversao', 'children')],
    [Input('seletor-mes-funil', 'value')]
)
def update_funil(mes_selecionado):
    # Filtrar os dados para o mês selecionado
    df_mes = df_funil[df_funil['Mês'] == mes_selecionado]
    
    if df_mes.empty or (df_mes[['Leads Frios', 'Atendidos', 'Vendas']].sum(axis=1).values[0] == 0):
        fig = px.bar(title=f"Funil de Vendas - {mes_selecionado} (Sem dados)")
        fig.update_layout(
            plot_bgcolor=secondary_color,
            paper_bgcolor=secondary_color,
            font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
            title_x=0.5
        )
        taxa_conversao_text = "Taxa de Conversão: N/A"
    else:
        # Criar o gráfico de funil (barra horizontal) ordenado do maior para o menor
        df_funil_plot = df_mes.melt(id_vars=['Mês'], var_name='Etapa', value_name='Quantidade')
        etapas_order = ['Leads Frios', 'Atendidos', 'Vendas']  # Alterado de 'Conversões' para 'Vendas'
        df_funil_plot['Etapa'] = pd.Categorical(df_funil_plot['Etapa'], categories=etapas_order, ordered=True)
        df_funil_plot = df_funil_plot.sort_values('Etapa')
        
        # Definir cores para cada etapa
        cores = {'Leads Frios': '#FFA07A', 'Atendidos': '#20B2AA', 'Vendas': '#3CB371'}  # Alterado
        
        fig = px.bar(
            df_funil_plot,
            y='Etapa',
            x='Quantidade',
            orientation='h',
            title=f"Funil de Vendas - {mes_selecionado}",
            labels={'Quantidade': 'Quantidade', 'Etapa': 'Etapa'},
            color='Etapa',
            color_discrete_map=cores,
            height=400,
            text='Quantidade'  # Adiciona as quantidades sobre as barras
        )
        fig.update_layout(
            plot_bgcolor=secondary_color,
            paper_bgcolor=secondary_color,
            font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
            title_x=0.5
        )
        
        fig.update_traces(textposition='auto')  # Ajusta a posição do texto
        
        # Calcular as Taxas de Cada Etapa
        leads_frios = df_mes['Leads Frios'].values[0]
        atendidos = df_mes['Atendidos'].values[0]
        vendas = df_mes['Vendas'].values[0]
        
        taxa_atendimento = (atendidos / leads_frios) * 100 if leads_frios > 0 else 0.0
        taxa_conversao = (vendas / atendidos) * 100 if atendidos > 0 else 0.0
        
        taxa_conversao_text = f"""
        Taxa de Atendimento: {taxa_atendimento:.2f}% dos Leads Frios foram Atendidos.<br>
        Taxa de Conversão: {taxa_conversao:.2f}% dos Atendidos foram Convertidos em Vendas.
        """
        
        # Estilizar as taxas usando HTML
        taxa_conversao_text = html.Div([
            html.P(f"Taxa de Atendimento: {taxa_atendimento:.2f}%", style={'font-size': '20px'}),
            html.P(f"Taxa de Conversão: {taxa_conversao:.2f}%", style={'font-size': '20px'})
        ], style={'font-weight': 'bold'})
    
    return fig, taxa_conversao_text

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False, host='0.0.0.0', port=8050)

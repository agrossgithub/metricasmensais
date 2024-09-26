import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import datetime

# Lista de estilos externos incluindo Montserrat via Google Fonts e Font Awesome para ícones
external_stylesheets = [
    dbc.themes.BOOTSTRAP,  # Usando o tema Bootstrap
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap',  # Fonte Montserrat
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',  # Font Awesome para ícones
]

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
    if row['Valor Investido (R$)'] != 0 else -100.0,
    axis=1
)

# Função para formatar valores monetários e porcentagens para as tabelas
def formatar_valores(df):
    # Formatar colunas de valores numéricos para moeda
    df_formatado = df.copy()
    for col in ['Valor Investido (R$)', 'Retorno (R$)', 'Orçamento (R$)']:
        if col in df_formatado.columns:
            df_formatado[col] = df_formatado[col].apply(
                lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") 
                if isinstance(x, (int, float)) else x
            )
    # Formatar CTR e CPL
    if 'CTR (%)' in df_formatado.columns:
        df_formatado['CTR (%)'] = df_formatado['CTR (%)'].apply(
            lambda x: f"{float(x):.2f}%".replace(".", ",") 
            if isinstance(x, (int, float)) else x
        )
    if 'CPL (R$)' in df_formatado.columns:
        df_formatado['CPL (R$)'] = df_formatado['CPL (R$)'].apply(
            lambda x: f"R$ {float(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") 
            if isinstance(x, (int, float)) else x
        )
    return df_formatado

# Aplicando a formatação de valores monetários
df_produtos_formatado = formatar_valores(df_produtos)

# Dados de cliques por estado (Agosto e Setembro)
dados_estados = {
    'Agosto': {
        'Estado': [
            'Rio Grande do Sul', 'Paraná', 'Santa Catarina', 'Minas Gerais', 'Goiás', 'São Paulo', 
            'Mato Grosso', 'Tocantins', 'Atlântico', 'Maranhão', 'Distrito Federal', 
            'Mato Grosso do Sul', 'Pará', 'Alto Paraná Department', 'Piauí',
            'Itapúa Department', 'Central Department'
        ],
        'Cliques': [28788, 21854, 7365, 3749, 3319, 2985, 2672, 2420, 
                    1796, 1775, 1192, 1104, 647, 584, 520, 485, 398]
    },
    'Setembro': {
        'Estado': [
            'Rio Grande do Sul', 'Minas Gerais', 'Paraná', 'São Paulo (state)', 'Santa Catarina', 
            'Goiás', 'Mato Grosso', 'Tocantins', 'Federal District', 'Mato Grosso do Sul', 'Bahia', 
            'Maranhão', 'Alto Paraná Department', 'Itapúa Department', 'Atlantico', 'Pará', 
            'Caaguazú Department', 'Nuevo León', 'Canindeyú Department'
        ],
        'Cliques': [
            8408, 2812, 2399, 2220, 2081, 1990, 1960, 1166, 1114, 1064, 824, 722, 
            422, 294, 288, 264, 190, 115, 112
        ]
    }
}

df_estados = pd.DataFrame()

for mes, dados in dados_estados.items():
    df_mes_estados = pd.DataFrame(dados)
    df_mes_estados['Mês'] = mes
    df_estados = pd.concat([df_estados, df_mes_estados], ignore_index=True)

# Função para formatar valores monetários conforme a métrica
def formatar_valor(metrica, valor):
    try:
        if pd.isna(valor) or valor == '':
            return ''
        if metrica in ['Impressões', 'Cliques no link', 'Resultados']:
            return f"{int(valor):,}".replace(",", ".")
        elif metrica == 'CTR (%)':
            return f"{float(valor):.2f}%".replace(".", ",")
        elif metrica == 'CPL (R$)':
            return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        elif metrica == 'Orçamento (R$)':
            return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return valor
    except (ValueError, TypeError):
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

# Função para gerar a tabela de desempenho com totais
def gerar_tabela_desempenho(df, total_facebook, total_google, total_spend):
    tabela = gerar_tabela(df)
    # Cards de totais utilizando Row e Col em vez de CardDeck
    cards = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total gasto no Facebook Ads", className="card-title"),
                    html.P(f"R$ {total_facebook:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                           className="card-text")
                ])
            ], color="success", inverse=True, style={'width': '18rem', 'margin-bottom': '10px'})
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total gasto no Google Ads", className="card-title"),
                    html.P(f"R$ {total_google:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                           className="card-text")
                ])
            ], color="danger", inverse=True, style={'width': '18rem', 'margin-bottom': '10px'})
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Investido", className="card-title"),
                    html.P(f"R$ {total_spend:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                           className="card-text")
                ])
            ], color="info", inverse=True, style={'width': '18rem'})
        ], md=4)
    ], className="mb-4", justify='start')  # Alinhado à esquerda

    # Container para posicionar os totais no canto inferior esquerdo
    # Usando fixed position e ajustando a posição para evitar sobreposição
    cards_fixed = html.Div([
        cards
    ], style={
        'position': 'fixed',
        'bottom': '80px',  # Aumentei a margem para subir as caixas
        'left': '20px',
        'zIndex': '1000'
    })

    # Container para a tabela e os cards
    return html.Div([
        tabela,
        cards_fixed
    ], style={'position': 'relative', 'height': 'auto'})

# Função para criar o gráfico de média dos totais (incluindo Google Ads e Facebook Ads)
def criar_grafico_media_totais(metrica_selecionada):
    meses = meses_completos

    # Agregar os valores por mês e plataforma
    df_plot = df_desempenho.groupby(['Mês', 'Plataforma'], as_index=False)[metrica_selecionada].sum()

    # Garantir que todos os meses e plataformas estejam presentes
    plataformas = ['Facebook Ads', 'Google Ads']
    complete_data = pd.DataFrame([(mes, plataforma) for mes in meses for plataforma in plataformas], columns=['Mês', 'Plataforma'])
    df_plot = complete_data.merge(df_plot, on=['Mês', 'Plataforma'], how='left').fillna(0)
    
    fig = px.bar(
        df_plot,
        x='Mês',
        y=metrica_selecionada,
        color='Plataforma',
        barmode='group',
        title=f"Média de {metrica_selecionada} por Mês e Plataforma",
        labels={metrica_selecionada: metrica_selecionada, 'Mês': 'Mês'},
        height=600
    )
    
    fig.update_layout(
        plot_bgcolor=secondary_color,
        paper_bgcolor=secondary_color,
        font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
        title_x=0.5
    )
    
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    
    return fig

# Função para criar o gráfico de cliques por estado para vários meses
def criar_grafico_cliques_estado(mes_selecionado):
    # Filtrar os dados para o mês selecionado
    df_mes = df_estados[df_estados['Mês'] == mes_selecionado]
    
    if df_mes.empty:
        # Sem dados para o mês selecionado
        fig = px.bar(title=f"Cliques por Estado - {mes_selecionado} (Sem dados)")
        fig.update_layout(
            plot_bgcolor=secondary_color,
            paper_bgcolor=secondary_color,
            font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
            title_x=0.5
        )
        return fig
    else:
        # Criar o gráfico de pizza
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
        
        return fig

# Função para gerar os botões de navegação fixos
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

# Layout da aplicação
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className="container", style={'position': 'relative', 'padding': '20px'})
], style={'backgroundColor': secondary_color, 'font-family': 'Montserrat, sans-serif', 'color': '#343a40'})

# Página 1: Capa com o Novo Logo da Agross
page_1_layout = html.Div([
    # Novo Logo da Agross
    html.Div([
        html.Img(
            src="https://i.ibb.co/jf2b0g7/AGROSS-texto-versaofinal.png",  # Novo link da logo
            style={
                'width': '600px',        # Tamanho aumentado
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
    
    botoes_navegacao(prev_href='#', next_href='/page-2')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 'height': '100vh', 'background-color': secondary_color})

# Página 2: Desempenho de Facebook e Google Ads
page_2_layout = html.Div([
    html.H1("Desempenho de Facebook e Google Ads", className="text-center", 
            style={'font-size': '36px', 'font-weight': '700', 'color': primary_color}),
    
    # Seletor de Mês
    html.Div([
        html.Label('Selecionar Mês:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='mes-desempenho-dropdown',
            options=[{'label': mes, 'value': mes} for mes in meses_completos],
            value='Agosto',
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px'}),
    
    # Tabela de desempenho e totais
    html.Div([
        html.Div(id='tabela-desempenho')
    ], style={'position': 'relative', 'height': 'auto', 'margin-top': '50px'}),  # Ajuste do margin-top para dar espaço aos cards
    
    # Botões de navegação
    botoes_navegacao(prev_href='/page-1', next_href='/page-3')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Página 3: Comparação de Todos os Meses
page_3_layout = html.Div([
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
                    html.B("CTR (%)"),
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
    botoes_navegacao(prev_href='/page-2', next_href='/page-4')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Página 4: Melhores Anúncios (CTR)
page_4_layout = html.Div([
    html.H1("Melhores Anúncios (CTR)", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
    
    # Selecionar Mês
    html.Div([
        html.Label('Selecionar Mês:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='mes-melhores-anuncios-dropdown',
            options=[{'label': mes, 'value': mes} for mes in meses_completos],
            value='Agosto',
            clearable=False,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-top': '20px'}),
    
    # Tabela de melhores anúncios
    html.Div([
        html.Div(id='tabela-melhores-anuncios')
    ], style={'margin-top': '30px', 'overflowX': 'auto', 'font-size': '18px'}),
    
    # Caixa de comentários e imagem (apenas para o mês selecionado)
    html.Div([
        dbc.Alert(
            id='comentario-melhores-anuncios-box',
            children="",
            is_open=False,
            color="info",
            dismissable=True,
            style={'font-size': '18px', 'margin-top': '20px', 'border': '1px solid #ced4da', 'padding': '15px'}
        )
    ], style={'text-align': 'center'}),
    
    # Botões de navegação
    botoes_navegacao(prev_href='/page-3', next_href='/page-5')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Página 5: Cliques por Estado
page_5_layout = html.Div([
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
    botoes_navegacao(prev_href='/page-4', next_href='/page-6')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Página 6: Valores Individuais de Cada Produto (sem destaque)
page_6_layout = html.Div([
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
    botoes_navegacao(prev_href='/page-5', next_href='/page-7')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

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

dados_funil['Leads Frios'][meses_completos.index('Setembro')] = 0
dados_funil['Atendidos'][meses_completos.index('Setembro')] = 0
dados_funil['Conversões'][meses_completos.index('Setembro')] = 0

df_funil = pd.DataFrame(dados_funil)

# Convertendo o DataFrame para um formato longo adequado para o gráfico de barras
df_funil_long = df_funil.melt(id_vars=['Mês'], var_name='Etapa', value_name='Quantidade')

# Página 7: Funil de Vendas
page_7_layout = html.Div([
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
    botoes_navegacao(prev_href='/page-6', next_href='/page-8')
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Página 8: Explicação de ROI e ROAS em Duas Tabelas Separadas com Caixa Central
page_8_layout = html.Div([
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
    botoes_navegacao(prev_href='/page-7', next_href='/page-9')  # Próximo slide será page-9
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Página 9: Média dos Totais de Desempenho de Facebook e Google Ads
page_9_layout = html.Div([
    html.H1("Média dos Totais de Desempenho de Facebook e Google Ads", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Seletor de Métrica
    html.Div([
        html.Label('Selecionar Métrica:', style={'font-weight': '700', 'font-size': '20px'}),
        dcc.Dropdown(
            id='seletor-metrica-media',
            options=[{'label': metrica, 'value': metrica} for metrica in ['Impressões', 'Cliques no link', 'Resultados', 'Orçamento (R$)', 'CTR (%)', 'CPL (R$)']],
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
    botoes_navegacao(prev_href='/page-8', next_href='/page-1')  # Volta para o Slide 1
], style={'color': '#343a40', 'font-family': 'Montserrat, sans-serif', 
          'background-color': secondary_color, 'padding': '20px', 
          'min-height': '100vh'})

# Callback para alterar a página de acordo com a URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    elif pathname == '/page-5':
        return page_5_layout
    elif pathname == '/page-6':
        return page_6_layout
    elif pathname == '/page-7':
        return page_7_layout
    elif pathname == '/page-8':
        return page_8_layout
    elif pathname == '/page-9':
        return page_9_layout
    else:
        return page_1_layout

# Callback para atualizar a tabela de desempenho com base no mês selecionado
@app.callback(
    Output('tabela-desempenho', 'children'),
    [Input('mes-desempenho-dropdown', 'value')]
)
def atualizar_tabela_desempenho(mes_selecionado):
    # Filtrar os dados para o mês selecionado
    df_mes = df_desempenho[df_desempenho['Mês'] == mes_selecionado]
    
    # Criar um dicionário para mapear métricas
    metricas = ['Impressões', 'Cliques no link', 'Resultados', 'Orçamento (R$)', 'CTR (%)', 'CPL (R$)']
    
    # Preparar os dados para a tabela
    dados_tabela = {'Métrica': metricas}
    for plataforma in ['Facebook Ads', 'Google Ads']:
        valores = []
        for metrica in metricas:
            valor = df_mes[df_mes['Plataforma'] == plataforma][metrica].values
            if valor.size > 0 and not pd.isna(valor[0]):
                valores.append(formatar_valor(metrica=metrica, valor=valor[0]))
            else:
                valores.append('')  # Substituir valores ausentes por string vazia
        dados_tabela[f'{plataforma}'] = valores
    
    df_tabela = pd.DataFrame(dados_tabela)
    
    # Calcular os totais de gastos
    total_facebook = df_desempenho[
        (df_desempenho['Mês'] == mes_selecionado) & 
        (df_desempenho['Plataforma'] == 'Facebook Ads')
    ]['Orçamento (R$)'].values
    total_facebook = total_facebook[0] if total_facebook.size > 0 and not pd.isna(total_facebook[0]) else 0.0
    
    total_google = df_desempenho[
        (df_desempenho['Mês'] == mes_selecionado) & 
        (df_desempenho['Plataforma'] == 'Google Ads')
    ]['Orçamento (R$)'].values
    total_google = total_google[0] if total_google.size > 0 and not pd.isna(total_google[0]) else 0.0
    
    total_spend = total_facebook + total_google
    
    # Gerar a tabela com os dados e totais
    tabela = gerar_tabela_desempenho(df_tabela, total_facebook, total_google, total_spend)
    
    return tabela

# Callback para atualizar os gráficos e comentários na página de comparação de meses
@app.callback(
    [Output('graficos-metricas', 'children'),
     Output('comentario-box', 'children'),
     Output('comentario-box', 'is_open')],
    [Input('mes-comparacao-checklist', 'value')]
)
def update_graphs(meses_selecionados):
    if not meses_selecionados:
        return [], "", False
    
    metricas = ['Impressões', 'Cliques no link', 'Resultados', 'Orçamento (R$)', 'CTR (%)', 'CPL (R$)']
    graficos = []
    for metrica in metricas:
        # Filtrar os dados para as plataformas e meses selecionados
        df_filtrado = df_desempenho[
            (df_desempenho['Mês'].isin(meses_selecionados)) & 
            (df_desempenho['Plataforma'].isin(['Facebook Ads', 'Google Ads']))
        ]
        df_plot = df_filtrado[['Plataforma', 'Mês', metrica]].dropna()
        
        # Adicionar meses sem dados com valor 0
        meses = meses_selecionados  # Apenas os selecionados
        plataformas = ['Facebook Ads', 'Google Ads']
        complete_data = pd.DataFrame([(plataforma, mes) for plataforma in plataformas for mes in meses], columns=['Plataforma', 'Mês'])
        df_plot = complete_data.merge(df_filtrado[['Plataforma', 'Mês', metrica]], on=['Plataforma', 'Mês'], how='left').fillna(0)
        
        # Agregar valores por mês e plataforma
        df_agg = df_plot.groupby(['Mês', 'Plataforma'], as_index=False).sum()
        
        fig = px.bar(
            df_agg,
            x='Mês',
            y=metrica,
            color='Plataforma',
            barmode='group',
            title=f"{metrica} - {', '.join(meses_selecionados)}",
            labels={metrica: metrica, 'Mês': 'Mês'},
            height=300  # Reduzido o height para tornar os gráficos mais finos
        )
        fig.update_layout(
            plot_bgcolor=secondary_color,
            paper_bgcolor=secondary_color,
            font=dict(family="Montserrat, sans-serif", size=14, color="#343a40"),
            title_x=0.5
        )
        fig.update_traces(texttemplate='%{y}', textposition='outside')
        
        graficos.append(html.Div([
            html.H4(metrica, className="text-center", 
                    style={'color': primary_color, 'font-size': '24px'}),
            dcc.Graph(figure=fig)
        ], style={'margin-bottom': '30px'}))
    
    # Gerar comentários com base nos meses selecionados
    comentarios = []
    for mes in meses_selecionados:
        if mes == 'Agosto':
            comentario_text = f"Comentário para {mes}: No mês de Agosto tivemos uma alta no CTR devido ao investimento alto e campanhas para feiras com objetivo de engajamento"
        elif mes == 'Setembro':
            comentario_text = f"Comentário para {mes}: Setembro apresentou uma baixa no CTR comparado com mês de Agosto devido a feira, mas se comparar com Julho ainda estamos em alta"
        elif mes == 'Junho':
            comentario_text = f"Comentário para {mes}: Tivemos um aumento constante no CTR mês a mês, resultado de anúncios mais claros e objetivos. As copys foram ajustadas para comunicar soluções diretas aos problemas do público"
        elif mes == 'Julho':
            comentario_text = f"Comentário para {mes}: "
        else:
            comentario_text = f"Comentário para {mes}: [Comentários específicos para {mes}]."
        comentarios.append(html.Li(comentario_text, style={'font-size': '18px'}))
    comentario_list = html.Ul(comentarios, style={'list-style-type': 'disc', 'margin-left': '20px'})
    
    return graficos, html.Div([
        html.H4("Comentários sobre os Meses Selecionados", style={'text-align': 'center'}),
        comentario_list
    ]), True

# Callback para atualizar a tabela de melhores anúncios com base no mês selecionado
@app.callback(
    [Output('tabela-melhores-anuncios', 'children'),
     Output('comentario-melhores-anuncios-box', 'children'),
     Output('comentario-melhores-anuncios-box', 'is_open')],
    [Input('mes-melhores-anuncios-dropdown', 'value')]
)
def atualizar_melhores_anuncios(mes_selecionado):
    # Filtrar os dados para o mês selecionado e CTR > 0
    df_filtrado = df_melhores_anuncios[
        (df_melhores_anuncios['Mês'] == mes_selecionado) & 
        (df_melhores_anuncios['CTR (%)'] > 0)
    ]
    
    if df_filtrado.empty:
        # Sem dados para o mês selecionado
        tabela = gerar_tabela(pd.DataFrame({
            'Anúncio': [],
            'CTR (%)': []
        }))
        comentario = f"Não há dados disponíveis para o mês de {mes_selecionado}."
        return tabela, comentario, True
    else:
        # Tabela de melhores anúncios para o mês selecionado com CTR formatado
        df_tabela = df_filtrado[['Anúncio', 'CTR (%)']].copy()
        df_tabela['CTR (%)'] = df_tabela['CTR (%)'].apply(lambda x: formatar_valor('CTR (%)', x))
        tabela = gerar_tabela(df_tabela)
        
        # Selecionar a imagem correspondente ao mês
        imagem_url = df_filtrado['Imagem'].iloc[0] if not df_filtrado.empty else imagem_placeholder
        
        # Comentário para o mês selecionado
        if mes_selecionado == 'Agosto':
            comentario_text = (
                f"Comentário para {mes_selecionado}: Tivemos um bom desempenho nos anúncios, "
                f"o CTR se destacou em várias campanhas."
            )
        elif mes_selecionado == 'Setembro':
            # Calcular a média de CTR para o comentário
            media_ctr = df_filtrado['CTR (%)'].mean()
            comentario_text = (
                f"Comentário para {mes_selecionado}: Setembro apresentou desafios com menor CTR "
                f"de {media_ctr}% devido a ajustes nas estratégias de anúncios."
            )
        else:
            comentario_text = f"Comentário para {mes_selecionado}: [Comentários específicos para {mes_selecionado}]."
        
        # Renderizar a imagem e o comentário
        imagem = html.Img(
            src=imagem_url,
            style={
                'width': '100%',
                'max-width': '800px',
                'height': 'auto',
                'display': 'block',
                'margin-left': 'auto',
                'margin-right': 'auto'
            }
        )
        
        comentario = html.Div([
            html.P(comentario_text, style={'font-size': '18px', 'text-align': 'center'}),
            imagem
        ])
        
        return tabela, comentario, True

# Callback para atualizar o gráfico de cliques por estado com base no mês selecionado
@app.callback(
    [Output('grafico-pizza-cliques', 'figure'),
     Output('comentario-cliques-box', 'children'),
     Output('comentario-cliques-box', 'is_open')],
    [Input('mes-cliques-dropdown', 'value')]
)
def update_cliques_pais(mes_selecionado):
    # Criar o gráfico de cliques por estado
    fig = criar_grafico_cliques_estado(mes_selecionado)
    
    # Comentários personalizados para cada mês
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

# Callback para atualizar a tabela de produtos com base no produto selecionado
@app.callback(
    Output('tabela-produtos', 'children'),
    [Input('produto-select-dropdown', 'value')]
)
def atualizar_tabela_produtos(produto_selecionado):
    df_produto = df_produtos[df_produtos['Produto'] == produto_selecionado].copy()
    df_produto_formatado = formatar_valores(df_produto)
    return gerar_tabela(df_produto_formatado)

# Callback para atualizar o gráfico de média dos totais (agora incluindo plataformas separadas)
@app.callback(
    Output('grafico-media-totais', 'figure'),
    [Input('seletor-metrica-media', 'value')]
)
def update_grafico_media(metrica_selecionada):
    fig = criar_grafico_media_totais(metrica_selecionada)
    return fig

# Callback para atualizar o gráfico e a taxa de conversão no Funil de Vendas
@app.callback(
    [Output('grafico-funil', 'figure'),
     Output('taxa-conversao', 'children')],
    [Input('seletor-mes-funil', 'value')]
)
def update_funil(mes_selecionado):
    # Filtrar os dados para o mês selecionado
    df_mes = df_funil[df_funil['Mês'] == mes_selecionado]
    
    if df_mes.empty or (df_mes[['Leads Frios', 'Atendidos', 'Conversões']].sum(axis=1).values[0] == 0):
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
        etapas_order = ['Leads Frios', 'Atendidos', 'Conversões']
        df_funil_plot['Etapa'] = pd.Categorical(df_funil_plot['Etapa'], categories=etapas_order, ordered=True)
        df_funil_plot = df_funil_plot.sort_values('Etapa')
        
        # Definir cores para cada etapa
        cores = {'Leads Frios': '#FFA07A', 'Atendidos': '#20B2AA', 'Conversões': '#3CB371'}
        
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
        
        # Calcular a Taxa de Conversão
        leads_frios = df_mes['Leads Frios'].values[0]
        atendidos = df_mes['Atendidos'].values[0]
        conversoes = df_mes['Conversões'].values[0]
        
        taxa_conversao = (conversoes / atendidos) * 100 if atendidos > 0 else 0.0
        taxa_conversao_text = f"Taxa de Conversão: {taxa_conversao:.2f}%"
    
    return fig, taxa_conversao_text

# Rodar o servidor com host='0.0.0.0' para permitir conexões externas
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)

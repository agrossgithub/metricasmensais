<<<<<<< HEAD
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

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
primary_color = '#12723D'  # Verde oficial
secondary_color = '#FFFFFF'  # Branco

# Função para salvar os dados atualizados em CSV
def salvar_dados(df):
    df.to_csv('dados_atualizados.csv', index=False)

# Carregar os dados de desempenho de Facebook Ads e Google Ads
dados_desempenho = {
    'Métrica': ['Impressões', 'Cliques no link', 'Resultados', 'CTR (%)', 'CPL (R$)', 'Valor usado (R$)'],
    'Facebook Ads': [3551018, 49775, 1371, 1.72, 41.56, 44717.89],
    'Google Ads': [274854, 21898, 300, 6.92, 49.85, 9452.34]
}
df_desempenho = pd.DataFrame(dados_desempenho)

# Calcular o total de gastos
total_facebook_spend = df_desempenho[df_desempenho['Métrica'] == 'Valor usado (R$)']['Facebook Ads'].values[0]
total_google_spend = df_desempenho[df_desempenho['Métrica'] == 'Valor usado (R$)']['Google Ads'].values[0]
total_spend = total_facebook_spend + total_google_spend

# Função para formatar os valores conforme a métrica
def formatar_valor(metrica, valor):
    if metrica in ['Impressões', 'Cliques no link', 'Resultados']:
        return f"{int(valor):,}".replace(",", ".")
    elif metrica == 'CTR (%)':
        return f"{float(valor):.2f}%".replace(".", ",")
    elif metrica in ['CPL (R$)', 'Valor usado (R$)']:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return valor

# Aplicar a formatação aos valores do DataFrame
def formatar_linha(row):
    metrica = row['Métrica']
    for col in ['Facebook Ads', 'Google Ads']:
        valor = row[col]
        row[col] = formatar_valor(metrica, valor)
    return row

df_desempenho = df_desempenho.apply(formatar_linha, axis=1)

# Dados de comparação entre todos os meses do ano (Janeiro a Dezembro)
dados_comparacao = {
    'Métrica': ['Impressões', 'Cliques no link', 'Resultados', 'CTR (%)', 'CPL (R$)'],
    'Facebook Ads - Janeiro': [1500000, 20000, 500, 1.33, 40.00],
    'Facebook Ads - Fevereiro': [1600000, 22000, 550, 1.38, 39.50],
    'Facebook Ads - Março': [1700000, 24000, 600, 1.41, 39.00],
    'Facebook Ads - Abril': [1800000, 26000, 650, 1.44, 38.50],
    'Facebook Ads - Maio': [1900000, 28000, 700, 1.47, 38.00],
    'Facebook Ads - Junho': [1703129, 16241, 516, 1.00, 43.54],
    'Facebook Ads - Julho': [2676920, 23930, 1140, 1.36, 42.28],
    'Facebook Ads - Agosto': [3551018, 49775, 1371, 1.72, 41.56],
    'Facebook Ads - Setembro': [0, 0, 0, 0, 0],
    'Facebook Ads - Outubro': [0, 0, 0, 0, 0],
    'Facebook Ads - Novembro': [0, 0, 0, 0, 0],
    'Facebook Ads - Dezembro': [0, 0, 0, 0, 0],
    'Google Ads - Janeiro': [200000, 25000, 350, 5.00, 45.00],
    'Google Ads - Fevereiro': [210000, 26000, 360, 5.50, 44.50],
    'Google Ads - Março': [220000, 27000, 370, 6.00, 44.00],
    'Google Ads - Abril': [230000, 28000, 380, 6.10, 43.90],
    'Google Ads - Maio': [240000, 29000, 390, 6.20, 43.80],
    'Google Ads - Junho': [273086, 10151, 240, 6.00, 30.58],
    'Google Ads - Julho': [191434, 7170, 221, 5.48, 63.13],
    'Google Ads - Agosto': [274854, 21898, 300, 6.92, 49.85],
    'Google Ads - Setembro': [0, 0, 0, 0, 0],
    'Google Ads - Outubro': [0, 0, 0, 0, 0],
    'Google Ads - Novembro': [0, 0, 0, 0, 0],
    'Google Ads - Dezembro': [0, 0, 0, 0, 0]
}

df_comparacao = pd.DataFrame(dados_comparacao)
# Dados dos melhores anúncios
melhores_anuncios = {
    'Anúncio': [
        'Aumente sua PRODUTIVIDADE!', 
        'Cadastre-se e fale conosco', 
        'Com o KIT PLANTIO TORNITEC', 
        'Para o grande e pequeno produtor!', 
        'Cadastre-se e fale conosco (Turbomix)', 
        'KIT PLANTIO NA AGROLEITE!'
    ],
    'CTR (%)': [2.88, 2.73, 2.57, 1.94, 1.84, 1.78]
}

df_melhores_anuncios = pd.DataFrame(melhores_anuncios)

# Dados de cliques por estado fornecidos
dados_estados = {
    'Estado': [
        'Rio Grande do Sul', 'Paraná', 'Santa Catarina', 'Minas Gerais', 'Goiás', 'São Paulo', 
        'Mato Grosso', 'Tocantins', 'Atlântico', 'Maranhão', 'Distrito Federal', 
        'Mato Grosso do Sul', 'Pará', 'Alto Paraná Department', 'Piauí',
        'Itapúa Department', 'Central Department', 'OUTROS'
    ],
    'Cliques': [28788, 21854, 7365, 3749, 3319, 2985, 2672, 2420,
                1796, 1775, 1192, 1104, 647, 584, 520, 485, 398, 0]
}

# Calcular cliques de OUTROS
total_cliques_provided = sum(dados_estados['Cliques'][:-1])
total_cliques = 100000  # Substitua pelo total real de cliques
cliques_outros = total_cliques - total_cliques_provided
dados_estados['Cliques'][-1] = cliques_outros

df_estados = pd.DataFrame(dados_estados)

# Dados para Slide 6: Valores Individuais de Cada Produto (incluindo novos produtos)
dados_produtos = {
    'Produto': ['Kit Plantio', 'Turbo Mix', 'Vollverini', 'Best Mix', 'Nitro Mix'],
    'Valor Investido (R$)': [20000.00, 15000.00, 18000.00, 22000.00, 25000.00],
    'Retorno (R$)': [50000.00, 45000.00, 47000.00, 55000.00, 60000.00]
}

df_produtos = pd.DataFrame(dados_produtos)

# Calcular ROI por produto
df_produtos['ROI (%)'] = ((df_produtos['Retorno (R$)'] - df_produtos['Valor Investido (R$)']) / df_produtos['Valor Investido (R$)']) * 100

# Função para gerar a tabela de desempenho com estilos aprimorados
def gerar_tabela(df):
    return dbc.Table.from_dataframe(
        df, striped=True, bordered=True, hover=True, 
        className="table",
        style={
            'font-size': '18px', 
            'text-align': 'center', 
            'background-color': secondary_color,
            'color': '#000000'
        }
    )

# Função auxiliar para criar gráficos com filtros e ajustes de cores e labels
def criar_grafico(metric_name, titulo, plataformas, meses):
    # Filtrar as colunas correspondentes às plataformas e meses selecionados
    colunas_selecionadas = [f"{plataforma} - {mes}" for plataforma in plataformas for mes in meses]
    colunas_selecionadas = [col for col in colunas_selecionadas if col in df_comparacao.columns]
    
    df_filtered = df_comparacao[df_comparacao['Métrica'] == metric_name][colunas_selecionadas]
    df_melted = df_filtered.melt(var_name='Campanha', value_name='Valor')
    
    # Remover campanhas com valor 0 ou NaN
    df_melted = df_melted[df_melted['Valor'] > 0]
    
    if df_melted.empty:
        return px.bar(title=f"{titulo} (Sem dados para os meses selecionados)")
    
    # Adicionar coluna de Plataforma para diferenciar as cores
    df_melted['Plataforma'] = df_melted['Campanha'].apply(lambda x: x.split(' - ')[0])
    
    # Definir cores específicas para cada plataforma
    color_discrete_map = {
        'Facebook Ads': '#3b5998',  # Azul do Facebook
        'Google Ads': '#DB4437'     # Vermelho do Google
    }
    
    fig = px.bar(
        df_melted, 
        x='Campanha', 
        y='Valor', 
        color='Plataforma', 
        color_discrete_map=color_discrete_map,
        barmode='group', 
        title=titulo,
        text='Valor'
    )
    
    # Ajustar o eixo Y para dar espaço aos rótulos no topo das barras
    max_valor = df_melted['Valor'].max()
    fig.update_yaxes(range=[0, max_valor * 1.2])
    
    # Atualizar o layout para melhorar a legibilidade dos rótulos
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='outside',
        cliponaxis=False
    )
    
    fig.update_layout(
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        xaxis_tickangle=-45,
        yaxis_title=None,
        xaxis_title=None,
        legend_title_text='Plataforma',
        margin=dict(t=80),
        plot_bgcolor=secondary_color,
        paper_bgcolor=secondary_color,
        font=dict(family="Montserrat, sans-serif", size=12, color="#000000")
    )
    
    return fig
# Função para criar o Funil de Vendas Horizontal
def criar_funil_horizontal(df):
    # Ordenar as etapas do funil
    df = df[::-1]  # Inverter para que Leads Frios fiquem na parte superior

    fig = px.bar(
        df,
        x='Quantidade',
        y='Etapa',
        orientation='h',
        text='Quantidade',
        color='Etapa',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Inverter a ordem do eixo Y para manter a lógica do funil
    fig.update_yaxes(autorange="reversed")

    # Remover as barras de fundo
    fig.update_layout(
        showlegend=False,
        plot_bgcolor=secondary_color,
        paper_bgcolor=secondary_color,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=100, r=100, t=50, b=50)
    )

    # Adicionar título
    fig.update_layout(title_text='Funil de Vendas Horizontal', title_x=0.5)

    # Ajustar o layout para melhor aparência
    fig.update_traces(
        textposition='inside',
        texttemplate='%{x}',
        marker=dict(line=dict(width=0))
    )

    return fig

# Função para criar o Gráfico de Investimento e Retorno por Produto
def criar_grafico_produtos(df):
    fig = px.bar(
        df,
        x='Produto',
        y=['Valor Investido (R$)', 'Retorno (R$)'],
        barmode='group',
        title='Investimento vs Retorno por Produto',
        labels={'value': 'Valor (R$)', 'variable': 'Tipo'},
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    # Atualizar layout
    fig.update_layout(
        xaxis_title='Produto',
        yaxis_title='Valor (R$)',
        plot_bgcolor=secondary_color,
        paper_bgcolor=secondary_color,
        legend_title_text='Tipo',
        title_x=0.5,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Montserrat, sans-serif", size=12, color="#000000")
    )

    # Adicionar valores nas barras
    fig.update_traces(
        texttemplate='%{y:.2f}',
        textposition='outside'
    )

    return fig

# Layout da aplicação com design aprimorado e espaço para botões de navegação
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className="container", style={'position': 'relative', 'padding': '20px'})
], style={'backgroundColor': secondary_color, 'padding': '50px', 'font-family': 'Montserrat, sans-serif'})

# Função para criar os botões de navegação fixos nas laterais com classe CSS
def botoes_navegacao(prev_href, next_href):
    return html.Div([
        dcc.Link(
            html.I(className='fas fa-arrow-left nav-button nav-button-left'),
            href=prev_href
        ),
        dcc.Link(
            html.I(className='fas fa-arrow-right nav-button nav-button-right'),
            href=next_href
        )
    ])

# Slide 1: Capa com o Logo da Agross
page_1_layout = html.Div([
    # Logo da Agross
    html.Div([
        html.Img(
            src="https://i.ibb.co/VYvnyGg/logo-agross.png",  # Substitua pelo link direto da imagem do logo
            style={
                'width': '300px',  # Ajuste o tamanho conforme necessário
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
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif', 'height': '100vh', 'background-color': secondary_color})

# Slide 2: Desempenho de Facebook e Google Ads com Total Investido
page_2_layout = html.Div([
    html.H1("Slide 2: Desempenho de Facebook e Google Ads", className="text-center", 
            style={'font-size': '36px', 'font-weight': '700', 'color': primary_color}),
    
    # Tabela de desempenho
    html.Div([
        gerar_tabela(df_desempenho)
    ], style={'margin-top': '30px'}),

    # Total gasto no Facebook Ads, Google Ads e o Total Investido
    html.Div([
        html.H3(f"Total gasto no Facebook Ads: {formatar_valor('Valor usado (R$)', total_facebook_spend)}", 
                className="text-center", style={'font-weight': '700', 'color': primary_color, 'margin-top': '20px'}),
        html.H3(f"Total gasto no Google Ads: {formatar_valor('Valor usado (R$)', total_google_spend)}", 
                className="text-center", style={'font-weight': '700', 'color': primary_color, 'margin-top': '10px'}),
        html.H3(f"Total Investido: {formatar_valor('Valor usado (R$)', total_spend)}", 
                className="text-center", style={'font-weight': '700', 'color': primary_color, 'margin-top': '10px'})
    ], style={'margin-top': '30px'}),

    # Botões de navegação
    botoes_navegacao(prev_href='/page-1', next_href='/page-3')

], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})


# Slide 3: Comparação de Todos os Meses (Jan-Dez)
page_3_layout = html.Div([
    html.H1("Slide 3: Comparação de Todos os Meses", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Filtros centralizados no início do slide
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Label('Selecionar Plataforma:', style={'font-weight': '700', 'margin-right': '10px', 'font-size': '20px'}),
                dcc.Checklist(
                    id='plataforma-checklist',
                    options=[{'label': 'Facebook Ads', 'value': 'Facebook Ads'},
                             {'label': 'Google Ads', 'value': 'Google Ads'}],
                    value=['Facebook Ads', 'Google Ads'],
                    inline=True,
                    labelStyle={'margin-right': '15px', 'font-size': '18px'}
                )
            ], width=6),
            dbc.Col([
                html.Label('Selecionar Mês:', style={'font-weight': '700', 'margin-right': '10px', 'font-size': '20px'}),
                dcc.Checklist(
                    id='mes-checklist',
                    options=[{'label': mes, 'value': mes} for mes in ['Janeiro', 'Fevereiro', 'Março', 'Abril', 
                                                                    'Maio', 'Junho', 'Julho', 'Agosto', 
                                                                    'Setembro', 'Outubro', 'Novembro', 'Dezembro']],
                    value=['Agosto'],  # Mês atual por padrão
                    inline=True,
                    labelStyle={'margin-right': '15px', 'font-size': '18px'}
                )
            ], width=6)
        ])
    ], style={'text-align': 'center', 'margin-top': '20px', 'margin-bottom': '20px'}),
    
    # Caixa de texto explicativo
    html.Div([
        html.P(
            "Esta seção compara as métricas de desempenho de Facebook e Google Ads ao longo de todos os meses do ano. Complete os dados de setembro em diante quando disponíveis para uma análise completa.",
            style={'font-size': '18px', 'text-align': 'center', 'font-style': 'italic'}
        )
    ], style={'margin-bottom': '20px'}),
    
    # Gráficos
    html.Div(id='graficos-metricas'),
    
    # Explicação das Métricas
    html.Hr(),
    html.H4("Explicação das Métricas", className="text-center", 
            style={'font-size': '24px', 'color': primary_color}),
    html.Ul([
        html.Li([
            html.B("Impressões: "),
            "Quantidade de vezes que o anúncio foi exibido.",
            html.Br(),
            html.I("Fórmula: Impressões = Total de exibições do anúncio.")
        ], style={'font-size': '18px'}),
        html.Li([
            html.B("Cliques no link: "),
            "Quantidade de cliques no anúncio.",
            html.Br(),
            html.I("Fórmula: Cliques no link = Total de cliques no anúncio.")
        ], style={'font-size': '18px'}),
        html.Li([
            html.B("Resultados: "),
            "Total de ações realizadas pelos usuários (conversões).",
            html.Br(),
            html.I("Fórmula: Resultados = Total de conversões obtidas.")
        ], style={'font-size': '18px'}),
        html.Li([
            html.B("CTR (%): "),
            "Taxa de cliques.",
            html.Br(),
            html.I("Fórmula: CTR (%) = (Cliques / Impressões) × 100")
        ], style={'font-size': '18px'}),
        html.Li([
            html.B("CPL (R$): "),
            "Custo por Lead.",
            html.Br(),
            html.I("Fórmula: CPL (R$) = Valor gasto / Resultados")
        ], style={'font-size': '18px'}),
    ], className="list-group", style={'color': '#000000'}),
    
    botoes_navegacao(prev_href='/page-2', next_href='/page-4')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})
# Slide 4: Melhores Anúncios (CTR)
page_4_layout = html.Div([
    html.H1("Slide 4: Melhores Anúncios (CTR)", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
    
    # Tabela de melhores anúncios atualizada
    html.Div([
        gerar_tabela(df_melhores_anuncios)
    ], style={'margin-top': '30px'}),
    
    # Caixa de texto explicativo atualizado
    html.Div([
        html.P(
            "Tivemos um aumento constante no CTR mês a mês, resultado de anúncios mais claros e objetivos. As copys foram ajustadas para comunicar soluções diretas aos problemas do público, como no caso do \"KIT PLANTIO TORNITEC\" e o foco em \"produtividade\", destacando os benefícios de forma rápida e eficiente. Essa clareza ajudou a captar a atenção dos usuários, aumentando o engajamento e a taxa de cliques.",
            style={'font-size': '18px', 'text-align': 'center'}
        )
    ], style={'margin-top': '20px'}),
    
    # Exibir a imagem completa logo abaixo da tabela com o novo link
    html.Div([
        html.Img(
            src="https://i.ibb.co/FByXKbq/anuncios.png",  # Link direto para a imagem
            style={
                'width': '100%',   # Ajuste para ocupar toda a largura disponível
                'max-width': '800px',  # Define uma largura máxima de 800px para boa qualidade
                'height': 'auto',  # Mantém a altura proporcional
                'display': 'block',  # Centraliza a imagem
                'margin-left': 'auto',
                'margin-right': 'auto'
            }
        ),
    ], className="d-flex justify-content-center mt-4"),
    
    botoes_navegacao(prev_href='/page-3', next_href='/page-5')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

# Slide 5: Cliques por Estado
page_5_layout = html.Div([
    html.H1("Slide 5: Cliques por Estado", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
    dcc.Graph(
        id='grafico-pizza',
        figure=px.pie(
            df_estados,
            names='Estado',
            values='Cliques',
            title='Distribuição de Cliques por Estado',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        ),
        style={'height': '600px'}  # Aumenta o tamanho do gráfico
    ),
    # Caixa de texto explicativo atualizado
    html.Div([
        html.P(
            "O Rio Grande do Sul e o Paraná lideram em número de cliques, resultado da nossa participação em feiras nesses estados. Essa presença aumentou significativamente a interação do público local com nossos anúncios, indicando mercados prioritários para futuras ações.",
            style={'font-size': '18px', 'text-align': 'center'}
        )
    ], style={'margin-top': '20px'}),
    
    botoes_navegacao(prev_href='/page-4', next_href='/page-6')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

# Slide 6: Valores Individuais de Cada Produto (incluindo ROI e novos produtos)
page_6_layout = html.Div([
    html.H1("Slide 6: Valores Individuais de Cada Produto", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Tabela de Valores Investidos, Retornos e ROI
    html.Div([
        gerar_tabela(df_produtos)
    ], style={'margin-top': '30px', 'margin-bottom': '30px'}),
    
    # Gráfico de Investimento vs Retorno por Produto
    html.Div([
        dcc.Graph(
            id='grafico-produtos',
            figure=criar_grafico_produtos(df_produtos)
        )
    ], style={'height': '500px'}),
    
    # Caixa de texto explicativo
    html.Div([
        html.P(
            "Esta tabela e gráfico mostram os investimentos realizados em cada produto e os respectivos retornos obtidos. Analisar esses dados permite avaliar a eficácia dos investimentos e tomar decisões estratégicas para futuros lançamentos e campanhas.",
            style={'font-size': '18px', 'text-align': 'center'}
        )
    ], style={'margin-top': '20px'}),
    
    botoes_navegacao(prev_href='/page-5', next_href='/page-7')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

# Slide 7: Funil de Vendas com as Etapas
page_7_layout = html.Div([
    html.H1("Slide 7: Funil de Vendas", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Tabela do Funil de Vendas
    html.Div([
        gerar_tabela(pd.DataFrame({
            'Etapa': ['Leads Frios', 'Atendidos', 'Oportunidades', 'Conversões'],
            'Quantidade': [1000, 600, 300, 150]
        }))
    ], style={'margin-top': '30px', 'margin-bottom': '30px'}),
    
    # Gráfico do Funil de Vendas Horizontal
    html.Div([
        dcc.Graph(
            id='grafico-funil',
            figure=criar_funil_horizontal(pd.DataFrame({
                'Etapa': ['Leads Frios', 'Atendidos', 'Oportunidades', 'Conversões'],
                'Quantidade': [1000, 600, 300, 150]
            }))
        )
    ], style={'height': '400px'}),
    
    # Caixa de texto explicativo
    html.Div([
        html.P(
            "Este funil de vendas ilustra a jornada dos leads desde o estágio inicial até a conversão final. É uma ferramenta essencial para identificar gargalos e otimizar nosso processo de vendas.",
            style={'font-size': '18px', 'text-align': 'center'}
        )
    ], style={'margin-top': '20px'}),
    
    botoes_navegacao(prev_href='/page-6', next_href='/page-8')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

# Slide 8: Explicação de ROI e ROAS (último slide)
page_8_layout = html.Div([
    html.H1("Slide 8: Explicação do ROI e ROAS", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Explicação do ROI Externo
    html.Div([
        html.H3("ROI Externo", className="text-center", 
                style={'font-size': '28px', 'color': primary_color}),
        html.P("Investimento: R$ 54.170,23", className="text-center", 
               style={'font-size': '24px'}),
        html.P("Retorno gerado: R$ 7.515.208,52", className="text-center", 
               style={'font-size': '24px'}),
        html.P("ROI = 13.771,37%", className="text-center", 
               style={'font-size': '24px'}),
        html.P("ROAS: R$ 138,74", className="text-center", 
               style={'font-size': '24px'}),
        html.P(
            "Isso significa que para cada R$ 1 investido, gerou R$ 138,74 em receita, e o retorno sobre o investimento total foi de 13.771,37%.",
            style={'font-size': '20px', 'text-align': 'center'}
        )
    ], className="mb-4"),
    
        # Explicação do ROI Interno
    html.Div([
        html.H3("ROI Interno", className="text-center", 
                style={'font-size': '28px', 'color': primary_color}),
        html.P("Faturamento interno (receita): R$ 2.497.224,63 (Kit e Máquinas)", className="text-center", 
               style={'font-size': '24px'}),
        html.P("Investimento total (custo): R$ 54.170,23", className="text-center", 
               style={'font-size': '24px'}),
        html.P("ROI: 4.508,98%", className="text-center", 
               style={'font-size': '24px'}),
        html.P("ROAS: R$ 46,09", className="text-center", 
               style={'font-size': '24px'}),
        html.P(
            "Isso significa que para cada R$ 1 investido, você gerou R$ 46,09 em receita internamente, com um retorno sobre o investimento de 4.508,98%.",
            style={'font-size': '20px', 'text-align': 'center'}
        )
    ]),
    
    botoes_navegacao(prev_href='/page-7', next_href='/page-1')  # Volta para o Slide 1
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

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
    else:
        return page_1_layout

# Callback para atualizar os gráficos de métricas com base nos filtros selecionados
@app.callback(
    Output('graficos-metricas', 'children'),
    [Input('plataforma-checklist', 'value'),
     Input('mes-checklist', 'value')]
)
def update_graphs(plataformas, meses):
    metricas = ['Impressões', 'Cliques no link', 'Resultados', 'CTR (%)', 'CPL (R$)']
    graficos = []
    for metrica in metricas:
        fig = criar_grafico(metrica, metrica, plataformas, meses)
        graficos.append(html.Div([
            html.H4(metrica, className="text-center", 
                    style={'color': primary_color, 'font-size': '24px'}),
            dcc.Graph(figure=fig)
        ]))
    return graficos

# Callback para atualizar o Funil de Vendas Horizontal
@app.callback(
    Output('grafico-funil', 'figure'),
    [Input('url', 'pathname')]
)
def atualizar_funil(pathname):
    if pathname == '/page-7':
        # Substitua os dados abaixo com dados dinâmicos conforme necessário
        dados_funil = pd.DataFrame({
            'Etapa': ['Leads Frios', 'Atendidos', 'Oportunidades', 'Conversões'],
            'Quantidade': [1000, 600, 300, 150]
        })
        return criar_funil_horizontal(dados_funil)
    else:
        # Retornar um gráfico vazio ou uma figura padrão
        return px.bar(title="Funil de Vendas Não Disponível")

# Rodar o servidor com host='0.0.0.0' para permitir conexões externas
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)

=======
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

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
primary_color = '#12723D'  # Verde oficial
secondary_color = '#FFFFFF'  # Branco

# Função para salvar os dados atualizados em CSV
def salvar_dados(df):
    df.to_csv('dados_atualizados.csv', index=False)

# Carregar os dados de desempenho de Facebook Ads e Google Ads
dados_desempenho = {
    'Métrica': ['Impressões', 'Cliques no link', 'Resultados', 'CTR (%)', 'CPL (R$)', 'Valor usado (R$)'],
    'Facebook Ads': [3551018, 49775, 1371, 1.72, 41.56, 44717.89],
    'Google Ads': [274854, 21898, 300, 6.92, 49.85, 9452.34]
}
df_desempenho = pd.DataFrame(dados_desempenho)

# Calcular o total de gastos
total_facebook_spend = df_desempenho[df_desempenho['Métrica'] == 'Valor usado (R$)']['Facebook Ads'].values[0]
total_google_spend = df_desempenho[df_desempenho['Métrica'] == 'Valor usado (R$)']['Google Ads'].values[0]
total_spend = total_facebook_spend + total_google_spend

# Função para formatar os valores conforme a métrica
def formatar_valor(metrica, valor):
    if metrica in ['Impressões', 'Cliques no link', 'Resultados']:
        return f"{int(valor):,}".replace(",", ".")
    elif metrica == 'CTR (%)':
        return f"{float(valor):.2f}%".replace(".", ",")
    elif metrica in ['CPL (R$)', 'Valor usado (R$)']:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        return valor

# Aplicar a formatação aos valores do DataFrame
def formatar_linha(row):
    metrica = row['Métrica']
    for col in ['Facebook Ads', 'Google Ads']:
        valor = row[col]
        row[col] = formatar_valor(metrica, valor)
    return row

df_desempenho = df_desempenho.apply(formatar_linha, axis=1)

# Dados de comparação entre todos os meses do ano (Janeiro a Dezembro)
dados_comparacao = {
    'Métrica': ['Impressões', 'Cliques no link', 'Resultados', 'CTR (%)', 'CPL (R$)'],
    'Facebook Ads - Janeiro': [1500000, 20000, 500, 1.33, 40.00],
    'Facebook Ads - Fevereiro': [1600000, 22000, 550, 1.38, 39.50],
    'Facebook Ads - Março': [1700000, 24000, 600, 1.41, 39.00],
    'Facebook Ads - Abril': [1800000, 26000, 650, 1.44, 38.50],
    'Facebook Ads - Maio': [1900000, 28000, 700, 1.47, 38.00],
    'Facebook Ads - Junho': [1703129, 16241, 516, 1.00, 43.54],
    'Facebook Ads - Julho': [2676920, 23930, 1140, 1.36, 42.28],
    'Facebook Ads - Agosto': [3551018, 49775, 1371, 1.72, 41.56],
    'Facebook Ads - Setembro': [0, 0, 0, 0, 0],
    'Facebook Ads - Outubro': [0, 0, 0, 0, 0],
    'Facebook Ads - Novembro': [0, 0, 0, 0, 0],
    'Facebook Ads - Dezembro': [0, 0, 0, 0, 0],
    'Google Ads - Janeiro': [200000, 25000, 350, 5.00, 45.00],
    'Google Ads - Fevereiro': [210000, 26000, 360, 5.50, 44.50],
    'Google Ads - Março': [220000, 27000, 370, 6.00, 44.00],
    'Google Ads - Abril': [230000, 28000, 380, 6.10, 43.90],
    'Google Ads - Maio': [240000, 29000, 390, 6.20, 43.80],
    'Google Ads - Junho': [273086, 10151, 240, 6.00, 30.58],
    'Google Ads - Julho': [191434, 7170, 221, 5.48, 63.13],
    'Google Ads - Agosto': [274854, 21898, 300, 6.92, 49.85],
    'Google Ads - Setembro': [0, 0, 0, 0, 0],
    'Google Ads - Outubro': [0, 0, 0, 0, 0],
    'Google Ads - Novembro': [0, 0, 0, 0, 0],
    'Google Ads - Dezembro': [0, 0, 0, 0, 0]
}

df_comparacao = pd.DataFrame(dados_comparacao)
# Dados dos melhores anúncios
melhores_anuncios = {
    'Anúncio': [
        'Aumente sua PRODUTIVIDADE!', 
        'Cadastre-se e fale conosco', 
        'Com o KIT PLANTIO TORNITEC', 
        'Para o grande e pequeno produtor!', 
        'Cadastre-se e fale conosco (Turbomix)', 
        'KIT PLANTIO NA AGROLEITE!'
    ],
    'CTR (%)': [2.88, 2.73, 2.57, 1.94, 1.84, 1.78]
}

df_melhores_anuncios = pd.DataFrame(melhores_anuncios)

# Dados de cliques por estado fornecidos
dados_estados = {
    'Estado': [
        'Rio Grande do Sul', 'Paraná', 'Santa Catarina', 'Minas Gerais', 'Goiás', 'São Paulo', 
        'Mato Grosso', 'Tocantins', 'Atlântico', 'Maranhão', 'Distrito Federal', 
        'Mato Grosso do Sul', 'Pará', 'Alto Paraná Department', 'Piauí',
        'Itapúa Department', 'Central Department', 'OUTROS'
    ],
    'Cliques': [28788, 21854, 7365, 3749, 3319, 2985, 2672, 2420,
                1796, 1775, 1192, 1104, 647, 584, 520, 485, 398, 0]
}

# Calcular cliques de OUTROS
total_cliques_provided = sum(dados_estados['Cliques'][:-1])
total_cliques = 100000  # Substitua pelo total real de cliques
cliques_outros = total_cliques - total_cliques_provided
dados_estados['Cliques'][-1] = cliques_outros

df_estados = pd.DataFrame(dados_estados)

# Dados para Slide 6: Valores Individuais de Cada Produto (incluindo novos produtos)
dados_produtos = {
    'Produto': ['Kit Plantio', 'Turbo Mix', 'Vollverini', 'Best Mix', 'Nitro Mix'],
    'Valor Investido (R$)': [20000.00, 15000.00, 18000.00, 22000.00, 25000.00],
    'Retorno (R$)': [50000.00, 45000.00, 47000.00, 55000.00, 60000.00]
}

df_produtos = pd.DataFrame(dados_produtos)

# Calcular ROI por produto
df_produtos['ROI (%)'] = ((df_produtos['Retorno (R$)'] - df_produtos['Valor Investido (R$)']) / df_produtos['Valor Investido (R$)']) * 100

# Função para gerar a tabela de desempenho com estilos aprimorados
def gerar_tabela(df):
    return dbc.Table.from_dataframe(
        df, striped=True, bordered=True, hover=True, 
        className="table",
        style={
            'font-size': '18px', 
            'text-align': 'center', 
            'background-color': secondary_color,
            'color': '#000000'
        }
    )

# Função auxiliar para criar gráficos com filtros e ajustes de cores e labels
def criar_grafico(metric_name, titulo, plataformas, meses):
    # Filtrar as colunas correspondentes às plataformas e meses selecionados
    colunas_selecionadas = [f"{plataforma} - {mes}" for plataforma in plataformas for mes in meses]
    colunas_selecionadas = [col for col in colunas_selecionadas if col in df_comparacao.columns]
    
    df_filtered = df_comparacao[df_comparacao['Métrica'] == metric_name][colunas_selecionadas]
    df_melted = df_filtered.melt(var_name='Campanha', value_name='Valor')
    
    # Remover campanhas com valor 0 ou NaN
    df_melted = df_melted[df_melted['Valor'] > 0]
    
    if df_melted.empty:
        return px.bar(title=f"{titulo} (Sem dados para os meses selecionados)")
    
    # Adicionar coluna de Plataforma para diferenciar as cores
    df_melted['Plataforma'] = df_melted['Campanha'].apply(lambda x: x.split(' - ')[0])
    
    # Definir cores específicas para cada plataforma
    color_discrete_map = {
        'Facebook Ads': '#3b5998',  # Azul do Facebook
        'Google Ads': '#DB4437'     # Vermelho do Google
    }
    
    fig = px.bar(
        df_melted, 
        x='Campanha', 
        y='Valor', 
        color='Plataforma', 
        color_discrete_map=color_discrete_map,
        barmode='group', 
        title=titulo,
        text='Valor'
    )
    
    # Ajustar o eixo Y para dar espaço aos rótulos no topo das barras
    max_valor = df_melted['Valor'].max()
    fig.update_yaxes(range=[0, max_valor * 1.2])
    
    # Atualizar o layout para melhorar a legibilidade dos rótulos
    fig.update_traces(
        texttemplate='%{text}', 
        textposition='outside',
        cliponaxis=False
    )
    
    fig.update_layout(
        uniformtext_minsize=8, 
        uniformtext_mode='hide',
        xaxis_tickangle=-45,
        yaxis_title=None,
        xaxis_title=None,
        legend_title_text='Plataforma',
        margin=dict(t=80),
        plot_bgcolor=secondary_color,
        paper_bgcolor=secondary_color,
        font=dict(family="Montserrat, sans-serif", size=12, color="#000000")
    )
    
    return fig
# Função para criar o Funil de Vendas Horizontal
def criar_funil_horizontal(df):
    # Ordenar as etapas do funil
    df = df[::-1]  # Inverter para que Leads Frios fiquem na parte superior

    fig = px.bar(
        df,
        x='Quantidade',
        y='Etapa',
        orientation='h',
        text='Quantidade',
        color='Etapa',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Inverter a ordem do eixo Y para manter a lógica do funil
    fig.update_yaxes(autorange="reversed")

    # Remover as barras de fundo
    fig.update_layout(
        showlegend=False,
        plot_bgcolor=secondary_color,
        paper_bgcolor=secondary_color,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=100, r=100, t=50, b=50)
    )

    # Adicionar título
    fig.update_layout(title_text='Funil de Vendas Horizontal', title_x=0.5)

    # Ajustar o layout para melhor aparência
    fig.update_traces(
        textposition='inside',
        texttemplate='%{x}',
        marker=dict(line=dict(width=0))
    )

    return fig

# Função para criar o Gráfico de Investimento e Retorno por Produto
def criar_grafico_produtos(df):
    fig = px.bar(
        df,
        x='Produto',
        y=['Valor Investido (R$)', 'Retorno (R$)'],
        barmode='group',
        title='Investimento vs Retorno por Produto',
        labels={'value': 'Valor (R$)', 'variable': 'Tipo'},
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    # Atualizar layout
    fig.update_layout(
        xaxis_title='Produto',
        yaxis_title='Valor (R$)',
        plot_bgcolor=secondary_color,
        paper_bgcolor=secondary_color,
        legend_title_text='Tipo',
        title_x=0.5,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Montserrat, sans-serif", size=12, color="#000000")
    )

    # Adicionar valores nas barras
    fig.update_traces(
        texttemplate='%{y:.2f}',
        textposition='outside'
    )

    return fig

# Layout da aplicação com design aprimorado e espaço para botões de navegação
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className="container", style={'position': 'relative', 'padding': '20px'})
], style={'backgroundColor': secondary_color, 'padding': '50px', 'font-family': 'Montserrat, sans-serif'})

# Função para criar os botões de navegação fixos nas laterais com classe CSS
def botoes_navegacao(prev_href, next_href):
    return html.Div([
        dcc.Link(
            html.I(className='fas fa-arrow-left nav-button nav-button-left'),
            href=prev_href
        ),
        dcc.Link(
            html.I(className='fas fa-arrow-right nav-button nav-button-right'),
            href=next_href
        )
    ])

# Slide 1: Capa com o Logo da Agross
page_1_layout = html.Div([
    # Logo da Agross
    html.Div([
        html.Img(
            src="https://i.ibb.co/VYvnyGg/logo-agross.png",  # Substitua pelo link direto da imagem do logo
            style={
                'width': '300px',  # Ajuste o tamanho conforme necessário
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
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif', 'height': '100vh', 'background-color': secondary_color})

# Slide 2: Desempenho de Facebook e Google Ads com Total Investido
page_2_layout = html.Div([
    html.H1("Slide 2: Desempenho de Facebook e Google Ads", className="text-center", 
            style={'font-size': '36px', 'font-weight': '700', 'color': primary_color}),
    
    # Tabela de desempenho
    html.Div([
        gerar_tabela(df_desempenho)
    ], style={'margin-top': '30px'}),

    # Total gasto no Facebook Ads, Google Ads e o Total Investido
    html.Div([
        html.H3(f"Total gasto no Facebook Ads: {formatar_valor('Valor usado (R$)', total_facebook_spend)}", 
                className="text-center", style={'font-weight': '700', 'color': primary_color, 'margin-top': '20px'}),
        html.H3(f"Total gasto no Google Ads: {formatar_valor('Valor usado (R$)', total_google_spend)}", 
                className="text-center", style={'font-weight': '700', 'color': primary_color, 'margin-top': '10px'}),
        html.H3(f"Total Investido: {formatar_valor('Valor usado (R$)', total_spend)}", 
                className="text-center", style={'font-weight': '700', 'color': primary_color, 'margin-top': '10px'})
    ], style={'margin-top': '30px'}),

    # Botões de navegação
    botoes_navegacao(prev_href='/page-1', next_href='/page-3')

], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})


# Slide 3: Comparação de Todos os Meses (Jan-Dez)
page_3_layout = html.Div([
    html.H1("Slide 3: Comparação de Todos os Meses", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Filtros centralizados no início do slide
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Label('Selecionar Plataforma:', style={'font-weight': '700', 'margin-right': '10px', 'font-size': '20px'}),
                dcc.Checklist(
                    id='plataforma-checklist',
                    options=[{'label': 'Facebook Ads', 'value': 'Facebook Ads'},
                             {'label': 'Google Ads', 'value': 'Google Ads'}],
                    value=['Facebook Ads', 'Google Ads'],
                    inline=True,
                    labelStyle={'margin-right': '15px', 'font-size': '18px'}
                )
            ], width=6),
            dbc.Col([
                html.Label('Selecionar Mês:', style={'font-weight': '700', 'margin-right': '10px', 'font-size': '20px'}),
                dcc.Checklist(
                    id='mes-checklist',
                    options=[{'label': mes, 'value': mes} for mes in ['Janeiro', 'Fevereiro', 'Março', 'Abril', 
                                                                    'Maio', 'Junho', 'Julho', 'Agosto', 
                                                                    'Setembro', 'Outubro', 'Novembro', 'Dezembro']],
                    value=['Agosto'],  # Mês atual por padrão
                    inline=True,
                    labelStyle={'margin-right': '15px', 'font-size': '18px'}
                )
            ], width=6)
        ])
    ], style={'text-align': 'center', 'margin-top': '20px', 'margin-bottom': '20px'}),
    
    # Caixa de texto explicativo
    html.Div([
        html.P(
            "Esta seção compara as métricas de desempenho de Facebook e Google Ads ao longo de todos os meses do ano. Complete os dados de setembro em diante quando disponíveis para uma análise completa.",
            style={'font-size': '18px', 'text-align': 'center', 'font-style': 'italic'}
        )
    ], style={'margin-bottom': '20px'}),
    
    # Gráficos
    html.Div(id='graficos-metricas'),
    
    # Explicação das Métricas
    html.Hr(),
    html.H4("Explicação das Métricas", className="text-center", 
            style={'font-size': '24px', 'color': primary_color}),
    html.Ul([
        html.Li([
            html.B("Impressões: "),
            "Quantidade de vezes que o anúncio foi exibido.",
            html.Br(),
            html.I("Fórmula: Impressões = Total de exibições do anúncio.")
        ], style={'font-size': '18px'}),
        html.Li([
            html.B("Cliques no link: "),
            "Quantidade de cliques no anúncio.",
            html.Br(),
            html.I("Fórmula: Cliques no link = Total de cliques no anúncio.")
        ], style={'font-size': '18px'}),
        html.Li([
            html.B("Resultados: "),
            "Total de ações realizadas pelos usuários (conversões).",
            html.Br(),
            html.I("Fórmula: Resultados = Total de conversões obtidas.")
        ], style={'font-size': '18px'}),
        html.Li([
            html.B("CTR (%): "),
            "Taxa de cliques.",
            html.Br(),
            html.I("Fórmula: CTR (%) = (Cliques / Impressões) × 100")
        ], style={'font-size': '18px'}),
        html.Li([
            html.B("CPL (R$): "),
            "Custo por Lead.",
            html.Br(),
            html.I("Fórmula: CPL (R$) = Valor gasto / Resultados")
        ], style={'font-size': '18px'}),
    ], className="list-group", style={'color': '#000000'}),
    
    botoes_navegacao(prev_href='/page-2', next_href='/page-4')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})
# Slide 4: Melhores Anúncios (CTR)
page_4_layout = html.Div([
    html.H1("Slide 4: Melhores Anúncios (CTR)", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
    
    # Tabela de melhores anúncios atualizada
    html.Div([
        gerar_tabela(df_melhores_anuncios)
    ], style={'margin-top': '30px'}),
    
    # Caixa de texto explicativo atualizado
    html.Div([
        html.P(
            "Tivemos um aumento constante no CTR mês a mês, resultado de anúncios mais claros e objetivos. As copys foram ajustadas para comunicar soluções diretas aos problemas do público, como no caso do \"KIT PLANTIO TORNITEC\" e o foco em \"produtividade\", destacando os benefícios de forma rápida e eficiente. Essa clareza ajudou a captar a atenção dos usuários, aumentando o engajamento e a taxa de cliques.",
            style={'font-size': '18px', 'text-align': 'center'}
        )
    ], style={'margin-top': '20px'}),
    
    # Exibir a imagem completa logo abaixo da tabela com o novo link
    html.Div([
        html.Img(
            src="https://i.ibb.co/FByXKbq/anuncios.png",  # Link direto para a imagem
            style={
                'width': '100%',   # Ajuste para ocupar toda a largura disponível
                'max-width': '800px',  # Define uma largura máxima de 800px para boa qualidade
                'height': 'auto',  # Mantém a altura proporcional
                'display': 'block',  # Centraliza a imagem
                'margin-left': 'auto',
                'margin-right': 'auto'
            }
        ),
    ], className="d-flex justify-content-center mt-4"),
    
    botoes_navegacao(prev_href='/page-3', next_href='/page-5')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

# Slide 5: Cliques por Estado
page_5_layout = html.Div([
    html.H1("Slide 5: Cliques por Estado", className="text-center", 
            style={'color': primary_color, 'font-size': '36px', 'font-weight': '700'}),
    dcc.Graph(
        id='grafico-pizza',
        figure=px.pie(
            df_estados,
            names='Estado',
            values='Cliques',
            title='Distribuição de Cliques por Estado',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        ),
        style={'height': '600px'}  # Aumenta o tamanho do gráfico
    ),
    # Caixa de texto explicativo atualizado
    html.Div([
        html.P(
            "O Rio Grande do Sul e o Paraná lideram em número de cliques, resultado da nossa participação em feiras nesses estados. Essa presença aumentou significativamente a interação do público local com nossos anúncios, indicando mercados prioritários para futuras ações.",
            style={'font-size': '18px', 'text-align': 'center'}
        )
    ], style={'margin-top': '20px'}),
    
    botoes_navegacao(prev_href='/page-4', next_href='/page-6')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

# Slide 6: Valores Individuais de Cada Produto (incluindo ROI e novos produtos)
page_6_layout = html.Div([
    html.H1("Slide 6: Valores Individuais de Cada Produto", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Tabela de Valores Investidos, Retornos e ROI
    html.Div([
        gerar_tabela(df_produtos)
    ], style={'margin-top': '30px', 'margin-bottom': '30px'}),
    
    # Gráfico de Investimento vs Retorno por Produto
    html.Div([
        dcc.Graph(
            id='grafico-produtos',
            figure=criar_grafico_produtos(df_produtos)
        )
    ], style={'height': '500px'}),
    
    # Caixa de texto explicativo
    html.Div([
        html.P(
            "Esta tabela e gráfico mostram os investimentos realizados em cada produto e os respectivos retornos obtidos. Analisar esses dados permite avaliar a eficácia dos investimentos e tomar decisões estratégicas para futuros lançamentos e campanhas.",
            style={'font-size': '18px', 'text-align': 'center'}
        )
    ], style={'margin-top': '20px'}),
    
    botoes_navegacao(prev_href='/page-5', next_href='/page-7')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

# Slide 7: Funil de Vendas com as Etapas
page_7_layout = html.Div([
    html.H1("Slide 7: Funil de Vendas", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Tabela do Funil de Vendas
    html.Div([
        gerar_tabela(pd.DataFrame({
            'Etapa': ['Leads Frios', 'Atendidos', 'Oportunidades', 'Conversões'],
            'Quantidade': [1000, 600, 300, 150]
        }))
    ], style={'margin-top': '30px', 'margin-bottom': '30px'}),
    
    # Gráfico do Funil de Vendas Horizontal
    html.Div([
        dcc.Graph(
            id='grafico-funil',
            figure=criar_funil_horizontal(pd.DataFrame({
                'Etapa': ['Leads Frios', 'Atendidos', 'Oportunidades', 'Conversões'],
                'Quantidade': [1000, 600, 300, 150]
            }))
        )
    ], style={'height': '400px'}),
    
    # Caixa de texto explicativo
    html.Div([
        html.P(
            "Este funil de vendas ilustra a jornada dos leads desde o estágio inicial até a conversão final. É uma ferramenta essencial para identificar gargalos e otimizar nosso processo de vendas.",
            style={'font-size': '18px', 'text-align': 'center'}
        )
    ], style={'margin-top': '20px'}),
    
    botoes_navegacao(prev_href='/page-6', next_href='/page-8')
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

# Slide 8: Explicação de ROI e ROAS (último slide)
page_8_layout = html.Div([
    html.H1("Slide 8: Explicação do ROI e ROAS", className="text-center", 
            style={'font-size': '36px', 'color': primary_color, 'font-weight': '700'}),
    
    # Explicação do ROI Externo
    html.Div([
        html.H3("ROI Externo", className="text-center", 
                style={'font-size': '28px', 'color': primary_color}),
        html.P("Investimento: R$ 54.170,23", className="text-center", 
               style={'font-size': '24px'}),
        html.P("Retorno gerado: R$ 7.515.208,52", className="text-center", 
               style={'font-size': '24px'}),
        html.P("ROI = 13.771,37%", className="text-center", 
               style={'font-size': '24px'}),
        html.P("ROAS: R$ 138,74", className="text-center", 
               style={'font-size': '24px'}),
        html.P(
            "Isso significa que para cada R$ 1 investido, gerou R$ 138,74 em receita, e o retorno sobre o investimento total foi de 13.771,37%.",
            style={'font-size': '20px', 'text-align': 'center'}
        )
    ], className="mb-4"),
    
        # Explicação do ROI Interno
    html.Div([
        html.H3("ROI Interno", className="text-center", 
                style={'font-size': '28px', 'color': primary_color}),
        html.P("Faturamento interno (receita): R$ 2.497.224,63 (Kit e Máquinas)", className="text-center", 
               style={'font-size': '24px'}),
        html.P("Investimento total (custo): R$ 54.170,23", className="text-center", 
               style={'font-size': '24px'}),
        html.P("ROI: 4.508,98%", className="text-center", 
               style={'font-size': '24px'}),
        html.P("ROAS: R$ 46,09", className="text-center", 
               style={'font-size': '24px'}),
        html.P(
            "Isso significa que para cada R$ 1 investido, você gerou R$ 46,09 em receita internamente, com um retorno sobre o investimento de 4.508,98%.",
            style={'font-size': '20px', 'text-align': 'center'}
        )
    ]),
    
    botoes_navegacao(prev_href='/page-7', next_href='/page-1')  # Volta para o Slide 1
], style={'color': '#000000', 'font-family': 'Montserrat, sans-serif'})

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
    else:
        return page_1_layout

# Callback para atualizar os gráficos de métricas com base nos filtros selecionados
@app.callback(
    Output('graficos-metricas', 'children'),
    [Input('plataforma-checklist', 'value'),
     Input('mes-checklist', 'value')]
)
def update_graphs(plataformas, meses):
    metricas = ['Impressões', 'Cliques no link', 'Resultados', 'CTR (%)', 'CPL (R$)']
    graficos = []
    for metrica in metricas:
        fig = criar_grafico(metrica, metrica, plataformas, meses)
        graficos.append(html.Div([
            html.H4(metrica, className="text-center", 
                    style={'color': primary_color, 'font-size': '24px'}),
            dcc.Graph(figure=fig)
        ]))
    return graficos

# Callback para atualizar o Funil de Vendas Horizontal
@app.callback(
    Output('grafico-funil', 'figure'),
    [Input('url', 'pathname')]
)
def atualizar_funil(pathname):
    if pathname == '/page-7':
        # Substitua os dados abaixo com dados dinâmicos conforme necessário
        dados_funil = pd.DataFrame({
            'Etapa': ['Leads Frios', 'Atendidos', 'Oportunidades', 'Conversões'],
            'Quantidade': [1000, 600, 300, 150]
        })
        return criar_funil_horizontal(dados_funil)
    else:
        # Retornar um gráfico vazio ou uma figura padrão
        return px.bar(title="Funil de Vendas Não Disponível")

# Rodar o servidor com host='0.0.0.0' para permitir conexões externas
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)

>>>>>>> dc4880f (Primeiro commit: adicionando meu Dash App)

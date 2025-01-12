CTE

"Qual é a receita líquida total por ano e categoria de produto, considerando apenas as vendas realizadas por vendedores contratados nos últimos 5 anos?"

WITH Vendedores_Recente AS (
    SELECT 
        ID_Vendedor,
        Nome_Vendedor,
        Data_Contratacao
    FROM 
        Dim_Vendedor
    WHERE 
        Data_Contratacao >= DATEADD(YEAR, -5, GETDATE())
),
Vendas_Filtradas AS (
    SELECT 
        FV.ID_Produto,
        FV.ID_Tempo,
        FV.Receita_Liquida,
        DP.Categoria_Produto,
        DT.Ano
    FROM 
        Fato_Vendas FV
    INNER JOIN 
        Dim_Produto DP ON FV.ID_Produto = DP.ID_Produto
    INNER JOIN 
        Dim_Tempo DT ON FV.ID_Tempo = DT.ID_Tempo
    INNER JOIN 
        Vendedores_Recente VR ON FV.ID_Vendedor = VR.ID_Vendedor
)
SELECT 
    Ano,
    Categoria_Produto,
    SUM(Receita_Liquida) AS Receita_Liquida_Total
FROM 
    Vendas_Filtradas
GROUP BY 
    Ano, 
    Categoria_Produto
ORDER BY 
    Ano, 
    Categoria_Produto;




ROLLUP

"Qual é a receita líquida total por ano, trimestre e categoria de produto, incluindo totais acumulados por ano e categoria?"

SELECT 
    DT.Ano,
    DT.Trimestre,
    DP.Categoria_Produto,
    SUM(FV.Receita_Liquida) AS Receita_Liquida_Total
FROM 
    Fato_Vendas FV
INNER JOIN 
    Dim_Produto DP ON FV.ID_Produto = DP.ID_Produto
INNER JOIN 
    Dim_Tempo DT ON FV.ID_Tempo = DT.ID_Tempo
GROUP BY 
    ROLLUP(DT.Ano, DT.Trimestre, DP.Categoria_Produto)
ORDER BY 
    DT.Ano, 
    DT.Trimestre, 
    DP.Categoria_Produto;




CUBE

"Qual é a receita líquida total por ano, categoria de produto e método de pagamento, incluindo todas as combinações possíveis de totais acumulados?"

SELECT 
    DT.Ano,
    DP.Categoria_Produto,
    FV.Metodo_Pagamento,
    SUM(FV.Receita_Liquida) AS Receita_Liquida_Total
FROM 
    Fato_Vendas FV
INNER JOIN 
    Dim_Produto DP ON FV.ID_Produto = DP.ID_Produto
INNER JOIN 
    Dim_Tempo DT ON FV.ID_Tempo = DT.ID_Tempo
GROUP BY 
    CUBE(DT.Ano, DP.Categoria_Produto, FV.Metodo_Pagamento)
ORDER BY 
    DT.Ano, 
    DP.Categoria_Produto, 
    FV.Metodo_Pagamento;



GROUPING SETS

"Qual é a receita líquida total por ano, trimestre e categoria de produto, mas também os totais separados por ano, por categoria e os totais gerais?"

SELECT 
    DT.Ano,
    DT.Trimestre,
    DP.Categoria_Produto,
    SUM(FV.Receita_Liquida) AS Receita_Liquida_Total
FROM 
    Fato_Vendas FV
INNER JOIN 
    Dim_Produto DP ON FV.ID_Produto = DP.ID_Produto
INNER JOIN 
    Dim_Tempo DT ON FV.ID_Tempo = DT.ID_Tempo
GROUP BY 
    GROUPING SETS (
        (DT.Ano, DT.Trimestre, DP.Categoria_Produto), -- Receita por Ano, Trimestre e Categoria
        (DT.Ano, DT.Trimestre),                      -- Receita por Ano e Trimestre
        (DT.Ano, DP.Categoria_Produto),              -- Receita por Ano e Categoria
        (DT.Ano),                                    -- Receita por Ano
        (DP.Categoria_Produto),                      -- Receita por Categoria
        ()                                           -- Total Geral
    )
ORDER BY 
    DT.Ano, 
    DT.Trimestre, 
    DP.Categoria_Produto;

-- Script para criação das tabelas no SQL Server

-- Dimensão Cliente
CREATE TABLE Dim_Cliente (
    ID_Cliente INT PRIMARY KEY IDENTITY(1,1),
    Nome_Cliente NVARCHAR(100) NOT NULL,
    Data_Nascimento DATE,
    Genero CHAR(1),
    Categoria_Cliente NVARCHAR(50),
    Cidade NVARCHAR(100),
    Pais NVARCHAR(50)
);

-- Dimensão Produto
CREATE TABLE Dim_Produto (
    ID_Produto INT PRIMARY KEY IDENTITY(1,1),
    Nome_Produto NVARCHAR(100) NOT NULL,
    Categoria_Produto NVARCHAR(50),
    Subcategoria_Produto NVARCHAR(50),
    Marca NVARCHAR(50),
    Preco_Unitario DECIMAL(10, 2),
    Data_Lancamento DATE
);

-- Dimensão Tempo
CREATE TABLE Dim_Tempo (
    ID_Tempo INT PRIMARY KEY IDENTITY(1,1),
    Data DATE NOT NULL,
    Dia INT NOT NULL,
    Mes INT NOT NULL,
    Ano INT NOT NULL,
    Trimestre INT NOT NULL,
    Semana INT NOT NULL
);

-- Dimensão Vendedor
CREATE TABLE Dim_Vendedor (
    ID_Vendedor INT PRIMARY KEY IDENTITY(1,1),
    Nome_Vendedor NVARCHAR(100) NOT NULL,
    Regiao NVARCHAR(50),
    Data_Contratacao DATE
);

-- Fato Vendas
CREATE TABLE Fato_Vendas (
    ID_Venda INT PRIMARY KEY IDENTITY(1,1),
    ID_Cliente INT NOT NULL,
    ID_Produto INT NOT NULL,
    ID_Tempo INT NOT NULL,
    ID_Vendedor INT NOT NULL,
    Quantidade INT NOT NULL,
    Valor_Unitario DECIMAL(10, 2) NOT NULL,
    Valor_Total AS (Quantidade * Valor_Unitario) PERSISTED,
    Desconto DECIMAL(10, 2) DEFAULT 0.0,
    Receita_Liquida AS ((Quantidade * Valor_Unitario) - Desconto) PERSISTED,
    Metodo_Pagamento NVARCHAR(50),
    Status_Venda NVARCHAR(50),

    CONSTRAINT FK_Cliente FOREIGN KEY (ID_Cliente) REFERENCES Dim_Cliente(ID_Cliente),
    CONSTRAINT FK_Produto FOREIGN KEY (ID_Produto) REFERENCES Dim_Produto(ID_Produto),
    CONSTRAINT FK_Tempo FOREIGN KEY (ID_Tempo) REFERENCES Dim_Tempo(ID_Tempo),
    CONSTRAINT FK_Vendedor FOREIGN KEY (ID_Vendedor) REFERENCES Dim_Vendedor(ID_Vendedor)
);

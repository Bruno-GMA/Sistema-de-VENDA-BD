import sqlite3

with sqlite3.connect("vendas.db") as connection:
    cursor = connection.cursor()

    # Criação das tabelas
    create_table_query = """
    DROP TABLE IF EXISTS pedidos;
    DROP TABLE IF EXISTS produtos;
    DROP TABLE IF EXISTS clientes;
    
    CREATE TABLE clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    CREATE TABLE produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL
    );
    CREATE TABLE pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    );
    """
    cursor.executescript(create_table_query)

    # Inserção de dados
    insert_data_query = """
    INSERT INTO clientes (nome, email) 
    VALUES ('Pedro Silva', 'pedro@email.com'),
           ('Luan Cardozo', 'luan@email.com');
    INSERT INTO produtos (nome, preco)
    VALUES ('Feijão 1kg', 10.00),
           ('Arroz 5kg', 25.50),
           ('Macarrão 500g', 5.00),
           ('Óleo 1L', 8.00),
           ('Açúcar 1kg', 4.50);
    INSERT INTO pedidos (cliente_id, produto_id, quantidade, data)
    VALUES (1, 1, 2, '2023-10-01'),
           (1, 2, 1, '2023-10-02'),
           (2, 3, 5, '2023-10-03'),
           (2, 4, 3, '2023-10-04'),
           (1, 5, 4, '2023-10-05');
    """
    cursor.executescript(insert_data_query)  
    connection.commit()

    # Consulta: quanto cada cliente gastou no total
    cursor.execute("""
                   SELECT c.nome, SUM(p.preco * pd.quantidade) AS total_gasto
                   FROM clientes c
                   JOIN pedidos pd ON c.id = pd.cliente_id
                   JOIN produtos p ON pd.produto_id = p.id
                   GROUP BY c.nome
                   """)
    print("\nTotal gasto por cliente:")
    for nome, total in cursor.fetchall():
        print(f"{nome}: R$ {total:.2f}")

    # Consulta produto mais vendido
    cursor.execute("""
                   SELECT p.nome, SUM(pd.quantidade) AS total_vendido
                   FROM produtos p
                   JOIN pedidos pd ON p.id = pd.produto_id
                   GROUP BY p.nome
                   ORDER BY total_vendido DESC
                   LIMIT 1
                   """)
    produto_mais_vendido = cursor.fetchone()
    if produto_mais_vendido:
        print(f"\nProduto mais vendido: {produto_mais_vendido[0]} com {produto_mais_vendido[1]} unidades vendidas")
    else:
        print("\nNenhum produto vendido.")

    


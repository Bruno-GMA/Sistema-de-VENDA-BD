import sqlite3

# Conecta no banco de dados
conn = sqlite3.connect("vendas.db")
cursor = conn.cursor()

# Consulta: quanto cada cliente gastou
print("Total gasto por cliente:")
cursor.execute("""
    SELECT c.nome, SUM(p.preco * ip.quantidade) AS total_gasto
    FROM Clientes c
    JOIN Pedidos pd ON c.id = pd.cliente_id
    JOIN ItensPedido ip ON pd.id = ip.pedido_id
    JOIN Produtos p ON ip.produto_id = p.id
    GROUP BY c.nome
""")
clientes = cursor.fetchall()
if clientes:
    for nome, total in clientes:
        print(f"  - {nome}: R$ {total:.2f}")
else:
    print("  Nenhum cliente realizou compras.")

# Consulta: produto mais vendido
print(" Produto mais vendido:")
cursor.execute("""
    SELECT p.nome, SUM(ip.quantidade) AS total_vendido
    FROM Produtos p
    JOIN ItensPedido ip ON p.id = ip.produto_id
    GROUP BY p.nome
    ORDER BY total_vendido DESC
    LIMIT 1
""")
produto = cursor.fetchone()
if produto:
    print(f"  - {produto[0]} (Total vendido: {produto[1]})")
else:
    print("  Nenhum produto vendido ainda.")

# Consulta: produtos nunca vendidos
print(" Produtos nunca vendidos:")
cursor.execute("""
    SELECT nome FROM Produtos
    WHERE id NOT IN (
        SELECT produto_id FROM ItensPedido
    )
""")
nao_vendidos = cursor.fetchall()
if nao_vendidos:
    for (nome,) in nao_vendidos:
        print(f"  - {nome}")
else:
    print("  Todos os produtos foram vendidos.")

# Fecha conexão
conn.close()

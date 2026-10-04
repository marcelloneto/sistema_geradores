import os
import json
import django

# 1. Configura o ambiente do Django (substitua 'sistema' pelo nome real da sua pasta de configurações, onde fica o settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django.setup()

from cadastros.models import Fornecedor, CategoriaMaterial, Material

def importar():
    caminho_json = 'dados_importacao.json'

    if not os.path.exists(caminho_json):
        print(f"Erro: O arquivo '{caminho_json}' não foi encontrado na raiz do projeto.")
        return

    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    contador = 0
    for item in dados:
        nome_fornecedor = item.get('fornecedor')
        nome_categoria = item.get('categoria')

        # Cria ou recupera o Fornecedor
        fornecedor_obj = None
        if nome_fornecedor:
            fornecedor_obj, _ = Fornecedor.objects.get_or_create(
                nome=nome_fornecedor,
                defaults={'razao_social': nome_fornecedor, 'ativo': True}
            )

        # Cria ou recupera a Categoria de Material
        categoria_obj = None
        if nome_categoria:
            identificador_cat = nome_categoria.lower().replace(' ', '_')
            categoria_obj, _ = CategoriaMaterial.objects.get_or_create(
                nome=nome_categoria,
                defaults={'identificador': identificador_cat}
            )

        # Cria ou atualiza o Material baseado no código
        codigo = item.get('codigo_material')
        Material.objects.update_or_create(
            codigo_material=codigo,
            defaults={
                'nome': item.get('nome'),
                'categoria': categoria_obj,
                'descricao': item.get('descricao'),
                'fornecedor': fornecedor_obj,
                'prioridade': item.get('prioridade'),
                'preco': item.get('preco'),
                'ativo': item.get('ativo', True)
            }
        )
        contador += 1

    print(f"Sucesso! {contador} materiais foram importados para o banco de dados.")

if __name__ == '__main__':
    importar()
import os
import django
from django.apps import apps
from django.core.serializers import serialize

# Altere para o nome do seu projeto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema.settings")

django.setup()

objetos = []

# Apps que não vale a pena migrar
APPS_EXCLUIDOS = {
    "contenttypes",
    "admin",
    "sessions",
}

print("Exportando dados...\n")

for model in apps.get_models():

    # Ignora apps desnecessários
    if model._meta.app_label in APPS_EXCLUIDOS:
        continue

    # Ignora apenas a tabela de permissões
    if (
        model._meta.app_label == "auth"
        and model.__name__ == "Permission"
    ):
        continue

    queryset = model.objects.all()

    quantidade = queryset.count()

    if quantidade > 0:
        print(
            f"{model._meta.app_label}.{model.__name__}: {quantidade} registros"
        )
        objetos.extend(queryset)

print(f"\nTotal de objetos exportados: {len(objetos)}")

with open("dados.json", "w", encoding="utf-8") as arquivo:
    arquivo.write(
        serialize(
            "json",
            objetos,
            indent=2,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True,
        )
    )

print("\nArquivo 'dados.json' criado com sucesso!")
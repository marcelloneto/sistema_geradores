import os
import re
from decimal import Decimal
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema.settings")
django.setup()

from django.db import transaction
from cadastros.models import Material as MaterialAntigo
from materiais.models import (
    Calco,
    Condutor,
    CordaoPavio,
    Cunha,
    Fita,
    Isolacao,
    MaterialAuxiliar,
    ResinaVerniz,
    SensorTemperatura,
)

# Códigos duplicados no banco antigo (mesmo produto e fornecedor cadastrados em várias etapas)
CODIGOS_DUPLICADOS_IGNORAR = {
    "CAL-AE-003",  # Araldite CY5538 (já existe em RES-HU-001 / MAS-HU-001)
    "CAL-AE-007",  # Araldite CY5538
    "BAR-HU-002",  # Araldite CY5538
    "PAV-HU-001",  # Araldite CY5538
    "CUN-HU-001",  # Araldite CY5538
    "ARO-HU-001",  # Araldite CY5538
    "CAL-AE-005",  # Feltro nomex (duplicado de CAL-AE-004)
    "CAL-AE-006",  # Camisa de fibra de vidro Ø10 mm (duplicado de CAL-AE-002)
    "CAL-AE-008",  # Calços isolantes (duplicado de CAL-AE-001)
    "CON-KR-001",  # Camisa de fibra de vidro Ø10 mm (duplicado de BAR-KR-002)
    "CON-PPE-005", # Registro TESTE
}


def extrair_parametros(material_antigo):
    params = {}
    for pv in material_antigo.parametros_tecnicos.select_related("parametro", "unidade"):
        chave = pv.parametro.nome.strip().lower()
        params[chave] = (
            pv.valor_numero if pv.valor_numero is not None else (pv.valor_texto or "").strip()
        )
    return params


def normalizar_rolo_metros(valor):
    if valor is None:
        return None
    dec = Decimal(str(valor))
    # No banco antigo rolos de 50 m e 30 m estavam salvos como 50000 e 30000
    if dec >= Decimal("1000"):
        return dec / Decimal("1000")
    return dec


def base_defaults(m):
    return {
        "nome": m.nome.strip(),
        "descricao": (m.descricao or "").strip(),
        "fornecedor": m.fornecedor,
        "prioridade": m.prioridade if m.prioridade and m.prioridade > 0 else 1,
        "preco": m.preco,
        "unidade_preco": m.unidade_preco,
        "ativo": m.ativo,
    }


def inferir_isolacao_condutor(nome):
    match = re.search(r"-\s*([A-Za-z0-9\s]+?)\s*-\s*\d", nome)
    return match.group(1).strip() if match else ""


@transaction.atomic
def executar_migracao():
    antigos = MaterialAntigo.objects.select_related("categoria", "fornecedor", "unidade_preco").all()
    migrados = 0
    ignorados = 0

    for m in antigos:
        codigo = (m.codigo_material or "").strip().upper()
        if not codigo or codigo in CODIGOS_DUPLICADOS_IGNORAR or m.nome.strip().upper() == "TESTE":
            ignorados += 1
            continue

        cat = m.categoria.nome.strip()
        p = extrair_parametros(m)
        comuns = base_defaults(m)

        # 1. CONDUTOR
        if cat == "Condutor":
            largura = p.get("largura")
            altura = p.get("altura")
            larg_iso = p.get("largura isolação")
            alt_iso = p.get("altura isolação")

            # Corrige inversão de largura/altura no COND-PPE-001
            if codigo == "COND-PPE-001":
                largura, altura = Decimal("5.600"), Decimal("2.500")

            # Preenche dimensões do COND-PPE-004 a partir do nome ("8,0 x 3,4")
            if largura is None and "8,0 x 3,4" in m.nome:
                largura, altura = Decimal("8.000"), Decimal("3.400")

            forma_raw = str(p.get("tipo de condutor", "retangular")).lower()
            forma = Condutor.Forma.RETANGULAR
            if "redond" in forma_raw:
                forma = Condutor.Forma.REDONDO
            elif "roebel" in forma_raw:
                forma = Condutor.Forma.ROEBEL

            Condutor.objects.update_or_create(
                codigo_material=codigo,
                defaults={
                    **comuns,
                    "forma": forma,
                    "largura_mm": largura,
                    "altura_mm": altura,
                    "largura_isolacao_mm": larg_iso,
                    "altura_isolacao_mm": alt_iso,
                    "densidade_kg_m3": p.get("densidade") or Decimal("8960.00"),
                    "tipo_isolacao": inferir_isolacao_condutor(m.nome),
                },
            )

        # 2. ISOLAÇÃO (inclui mica de barramento BAR-KR-001)
        elif cat == "Isolação" or codigo == "BAR-KR-001":
            nome_low = m.nome.lower()
            if "panqueca" in (m.descricao or "").lower() or codigo == "ISO-KR-002":
                aplicacao = Isolacao.Aplicacao.PANQUECA
            elif "principal" in (m.descricao or "").lower():
                aplicacao = Isolacao.Aplicacao.PRINCIPAL
            else:
                aplicacao = Isolacao.Aplicacao.GERAL

            if "thermopreg" in nome_low:
                substrato = Isolacao.Substrato.PREPREG_NOMEX
            elif "nomex" in nome_low:
                substrato = Isolacao.Substrato.ARAMIDA
            elif "vidro" in (m.descricao or "").lower() or codigo == "ISO-KR-003":
                substrato = Isolacao.Substrato.VIDRO
            elif "poliéster" in (m.descricao or "").lower() or "poliester" in (m.descricao or "").lower() or codigo == "ISO-KR-004":
                substrato = Isolacao.Substrato.POLIESTER
            else:
                substrato = Isolacao.Substrato.OUTRO

            espessura = p.get("espessura") or (Decimal("0.160") if codigo == "BAR-KR-001" else Decimal("0.120"))
            largura = p.get("largura") or Decimal("25.00")
            comp_m = normalizar_rolo_metros(p.get("comprimento do rolo")) or (Decimal("30.00") if codigo == "BAR-KR-001" else Decimal("50.00"))

            Isolacao.objects.update_or_create(
                codigo_material=codigo,
                defaults={
                    **comuns,
                    "aplicacao": aplicacao,
                    "substrato": substrato,
                    "espessura_mm": espessura,
                    "largura_mm": largura,
                    "comprimento_rolo_m": comp_m,
                },
            )

        # 3. FITA / CADARÇO
        elif cat in ("Fita", "Cadarço"):
            fin_raw = str(p.get("finalidade", "")).lower()
            if cat == "Cadarço":
                finalidade = Fita.Finalidade.CADARCO
            elif fin_raw == "condutiva":
                finalidade = Fita.Finalidade.CONDUTIVA
            elif fin_raw == "semicondutiva":
                finalidade = Fita.Finalidade.SEMICONDUTIVA
            elif fin_raw == "sacrificio":
                finalidade = Fita.Finalidade.SACRIFICIO
            else:
                finalidade = Fita.Finalidade.ACABAMENTO

            Fita.objects.update_or_create(
                codigo_material=codigo,
                defaults={
                    **comuns,
                    "finalidade": finalidade,
                    "espessura_mm": p.get("espessura"),
                    "largura_mm": p.get("largura"),
                    "comprimento_rolo_m": normalizar_rolo_metros(p.get("comprimento do rolo")),
                    "material_base": "Fibra de vidro" if cat == "Cadarço" else "",
                },
            )

        # 4. RESINA / VERNIZ / MASSA
        elif cat in ("Resina", "Verniz", "Massa"):
            if cat == "Resina":
                cat_quim = ResinaVerniz.CategoriaQuimica.RESINA
                fin = ResinaVerniz.Finalidade.CONSOLIDACAO
            elif cat == "Massa":
                cat_quim = ResinaVerniz.CategoriaQuimica.MASSA
                fin = (
                    ResinaVerniz.Finalidade.CONDUTIVO
                    if "conductive" in m.nome.lower()
                    else ResinaVerniz.Finalidade.ENCHIMENTO
                )
            else:
                cat_quim = ResinaVerniz.CategoriaQuimica.VERNIZ
                fin_raw = str(p.get("finalidade", "isolante")).lower()
                mapa_fin = {
                    "condutivo": ResinaVerniz.Finalidade.CONDUTIVO,
                    "semicondutivo": ResinaVerniz.Finalidade.SEMICONDUTIVO,
                    "isolante": ResinaVerniz.Finalidade.ISOLANTE,
                }
                fin = mapa_fin.get(fin_raw, ResinaVerniz.Finalidade.ISOLANTE)

            ResinaVerniz.objects.update_or_create(
                codigo_material=codigo,
                defaults={
                    **comuns,
                    "categoria_quimica": cat_quim,
                    "finalidade": fin,
                    "rendimento_kg_m": p.get("rendimento"),
                },
            )

        # 5. PAVIO / CAMISA / ARO
        elif cat in ("Pavio", "Aro") or "camisa de fibra" in m.nome.lower():
            nome_low = m.nome.lower()
            if "camisa" in nome_low:
                tipo_cordao = CordaoPavio.TipoCordao.CAMISA
            elif cat == "Aro":
                tipo_cordao = CordaoPavio.TipoCordao.ARO
            else:
                tipo_cordao = CordaoPavio.TipoCordao.PAVIO

            diam_match = re.search(r"Ø\s*(\d+(?:[.,]\d+)?)", m.nome)
            diametro = Decimal(diam_match.group(1).replace(",", ".")) if diam_match else None

            CordaoPavio.objects.update_or_create(
                codigo_material=codigo,
                defaults={
                    **comuns,
                    "tipo": tipo_cordao,
                    "material_base": "Fibra de vidro",
                    "diametro_mm": diametro,
                },
            )

        # 6. CALÇO
        elif cat == "Calço":
            is_feltro = "feltro" in m.nome.lower()
            Calco.objects.update_or_create(
                codigo_material=codigo,
                defaults={
                    **comuns,
                    "tipo_calco": Calco.TipoCalco.FELTRO if is_feltro else Calco.TipoCalco.RADIAL,
                    "material_base": "Nomex" if is_feltro else "Laminado isolante",
                    "espessura_mm": Decimal("2.00") if is_feltro else None,
                    "largura_mm": Decimal("1000.00") if is_feltro else None,
                },
            )

        # 7. CUNHA
        elif cat == "Cunha":
            Cunha.objects.update_or_create(
                codigo_material=codigo,
                defaults={
                    **comuns,
                    "tipo_cunha": Cunha.TipoCunha.ISOLANTE,
                    "espessura_mm": Decimal("2.00") if codigo == "CUN-KR-001" else None,
                    "largura_mm": Decimal("17.00") if codigo == "CUN-KR-001" else None,
                    "comprimento_mm": Decimal("2460.00") if codigo == "CUN-KR-001" else None,
                    "desenho_referencia": "DT.1445.013-R00 / DT.1445.014-R00" if codigo == "CUN-AE-001" else "",
                },
            )

        # 8. SENSOR DE TEMPERATURA
        elif cat == "Sensor":
            SensorTemperatura.objects.update_or_create(
                codigo_material=codigo,
                defaults={
                    **comuns,
                    "tipo_sensor": SensorTemperatura.TipoSensor.PT100,
                },
            )

        # 9. MATERIAIS AUXILIARES (Barramento, Conexão, etc.)
        else:
            nome_low = m.nome.lower()
            if "cobre" in nome_low:
                subtipo = MaterialAuxiliar.Subtipo.BARRAMENTO_COBRE
            elif "silfoscoper" in nome_low or "prata" in nome_low:
                subtipo = MaterialAuxiliar.Subtipo.SOLDA_BRASAGEM
            elif "caixa" in nome_low or "calço" in nome_low:
                subtipo = MaterialAuxiliar.Subtipo.COMPONENTE_ISOLANTE
            elif "batedor" in nome_low or "macaquinho" in nome_low or "leiteira" in nome_low:
                subtipo = MaterialAuxiliar.Subtipo.DISPOSITIVO_MONTAGEM
            else:
                subtipo = MaterialAuxiliar.Subtipo.CONSUMIVEL_QUIMICO

            MaterialAuxiliar.objects.update_or_create(
                codigo_material=codigo,
                defaults={
                    **comuns,
                    "subtipo": subtipo,
                },
            )

        migrados += 1

    print(f"Migração concluída: {migrados} materiais transferidos, {ignorados} duplicados/testes ignorados.")


if __name__ == "__main__":
    executar_migracao()
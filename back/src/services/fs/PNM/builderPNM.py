from typing import Dict, Any
from ....utils.fsFormat import formatarValor, tributacaoICMS 

def builderPNM(dados: Dict[str, Any]) -> str:
    cst_icms = str(dados.get("cst_icms") or "").zfill(3)
    csta = cst_icms[0] if len(cst_icms) == 3 else ''
    cstb = cst_icms[1:] if len(cst_icms) == 3 else ''
    csosn = cst_icms if csta in ['1', '2', '3', '4', '5', '9'] else ''
    tipo_calc_cofins = "2" if float(dados.get("aliq_cofins_reais", 0) or 0) > 0 else "1"
    tipo_calc_pis = "2" if float(dados.get("aliq_pis_reais", 0) or 0) > 0 else "1"

    base_pis_cofins = (
        (float(dados.get("vl_item", 0) or 0)) +
        (float(dados.get("frete_rateado", 0) or 0)) +
        (float(dados.get("seguro_rateado", 0) or 0)) +
        (float(dados.get("outras_desp_rateado", 0) or 0))
    )
    valor_total_item = base_pis_cofins - (float(dados.get("vl_desc", 0) or 0))

    campos = [
        "PNM",                                          # 1
        str(dados.get("cod_item", ''))[:9],              # 2
        str(dados.get("cfop", ''))[:4],                  # 3
        "",                                             # 4
        csta,                                           # 5
        cstb,                                           # 6
        str(dados.get("unid", ''))[:6],                  # 7
        formatarValor(dados.get("qtd"), 2),             # 8
        formatarValor(dados.get("vl_item")),            # 9
        "",                                             # 10
        "3",                                            # 11
        "",                                             # 12
        "",                                             # 13
        formatarValor(dados.get("vl_bc_icms_st")),      # 14
        formatarValor(dados.get("vl_icms_st")),         # 15
        "",                                             # 16
        "",                                             # 17
        "",                                             # 18
        "",                                             # 19
        "",                                             # 20
        formatarValor(dados.get("aliq_st")),            # 21
        "",                                             # 22
        "",                                             # 23
        "",                                             # 24
        "",                                             # 25
        "",                                             # 26
        "",                                             # 27
        "",                                             # 28
        "",                                             # 29
        "",                                             # 30
        "",                                             # 31
        "",                                             # 32
        formatarValor(dados.get("vl_bc_ipi")),          # 33
        formatarValor(dados.get("aliq_ipi")),           # 34
        formatarValor(dados.get("vl_ipi")),             # 35
        str(dados.get("cst_ipi", ''))[:2],               # 36
        str(dados.get("cst_cofins", ''))[:2],            # 37
        str(dados.get("cst_pis", ''))[:2],               # 38
        formatarValor(base_pis_cofins),                 # 39
        formatarValor(base_pis_cofins),                 # 40
        formatarValor(dados.get("frete_rateado")),      # 41
        formatarValor(dados.get("seguro_rateado")),     # 42
        formatarValor(dados.get("vl_desc")),            # 43
        formatarValor(valor_total_item),                # 44
        str(dados.get("cod_nat", ''))[:3],               # 45
        str(dados.get("cod_nat", ''))[:3],               # 46
        "",                                             # 47
        "",                                             # 48
        csta if csosn else "",                          # 49
        csosn,                                          # 50
        tipo_calc_cofins,                               # 51
        formatarValor(dados.get("aliq_cofins")),        # 52
        formatarValor(dados.get("aliq_cofins_reais"), 4),# 53
        formatarValor(dados.get("vl_cofins")),          # 54
        tipo_calc_pis,                                  # 55
        formatarValor(dados.get("aliq_pis")),           # 56
        formatarValor(dados.get("aliq_pis_reais"), 4),  # 57
        formatarValor(dados.get("vl_pis")),             # 58
        "",                                             # 59
        "",                                             # 60
        "",                                             # 61
        formatarValor(dados.get("outras_desp_rateado")),# 62
        str(dados.get("cod_cta", ''))[:15],              # 63
        "0",                                            # 64
        "",                                             # 65
        "",                                             # 66
        "",                                             # 67
        "",                                             # 68
        "",                                             # 69
        "",                                             # 70
        "",                                             # 71
        "",                                             # 72
        "",                                             # 73
        "",                                             # 74
        "",                                             # 75
        "",                                             # 76
        "",                                             # 77
        "",                                             # 78
        "",                                             # 79
        "",                                             # 80
        "",                                             # 81
        "N",                                            # 82
        "",                                             # 83
        "",                                             # 84
        "",                                             # 85
        "",                                             # 86
        "",                                             # 87
        "",                                             # 88
        "",                                             # 89
        "",                                             # 90
        "N",                                            # 91
        "",                                             # 92
        "",                                             # 93
        "",                                             # 94
        "",                                             # 95
        "",                                             # 96
        "",                                             # 97
        "",                                             # 98
        "",                                             # 99
        "",                                             # 100
        "",                                             # 101
        "",                                             # 102
        "",                                             # 103
        "",                                             # 104
        "",                                             # 105
        "",                                             # 106
        "",                                             # 107
        "",                                             # 108
        "",                                             # 109
        "",                                             # 110
        "",                                             # 111
        "",                                             # 112
        "",                                             # 113
        "",                                             # 114
        "",                                             # 115
        "",                                             # 116
        "",                                             # 117
        "",                                             # 118
        "",                                             # 119
        "",                                             # 120
        "N",                                            # 121
        "",                                             # 122
        "N",                                            # 123
        ""                                              # 124
    ]

    return "|".join(campos)

# Estratégia de Match para MSP — `siteops-echo` / `cruzeiro_do_sul/graduação_ead`

## Contexto

A feature `cruzeiro_do_sul/graduação_ead` recebe as planilhas da IES e gera a MSP final de Graduação EaD para o grupo Cruzeiro.

Entradas principais analisadas:

- `UPLOAD GRAD EAD 26_2 - CAPTADORAS - 08.05 (3).xlsx`
  - Planilha original de ofertas da IES.
  - Contém `Cód. Curso`, `Cód. IES`, `Cód. Campus`, `Código SIAA`, `Curso`, `Grau`, `Modalidade`, descontos e `Certificadora`.

- `CURSOS VS POLOS- 23.03 (1).xlsx`
  - Relação de polos × cursos.
  - Contém dados do polo e colunas pivotadas no formato `CURSO_<COD>`, marcadas com `X` quando o polo oferece aquele curso.
  - Contém também `COD_INST`, que identifica a instituição/certificadora na relação.

- `FEATURE_CONTEXT.md`
  - Documento de referência da feature.
  - Define que a relação de polos deve ser despivotada (`unpivot/melt`) e que o match atual usa `Cód. Curso` / `COD_CURS`.

---

## Diagnóstico

O ponto crítico é que `Cód. Curso` sozinho **não identifica uma oferta única**.

Na planilha de ofertas, existem várias linhas para o mesmo `Cód. Curso`, variando por certificadora/campus/SIAA.

Resumo encontrado nas planilhas analisadas:

| Métrica | Resultado |
|---|---:|
| Linhas na planilha de ofertas | 833 |
| `Cód. Curso` únicos | 146 |
| `Código SIAA` únicos | 833 |
| Combinações únicas `Cód. Curso + Certificadora` | 833 |
| Cursos com mais de uma oferta por `Cód. Curso` | 135 |
| Polos/linhas na relação de polos | 1.892 |
| Colunas `CURSO_<COD>` na relação | 145 |
| Relações ativas polo × curso com `X` | 179.262 |

Conclusão:

```text
Cód. Curso identifica o curso.
Cód. Curso NÃO identifica a oferta.
```

A oferta correta depende da instituição/certificadora.

---

# Decisão atualizada

A melhor chave principal de match deve ser:

```text
COD_INST + COD_CURS + "0"
```

Essa chave deve ser comparada com:

```text
Código SIAA
```

da planilha original de ofertas.

Exemplo:

```text
COD_INST = 18
COD_CURS = 370

SIAA_KEY = 18 + 370 + 0
SIAA_KEY = 183700
```

Essa chave bate com:

```text
Código SIAA = 183700
```

na planilha original de ofertas.

---

## Por que essa chave é melhor

Antes, a sugestão era usar:

```text
COD_CURS + IES_KEY
```

Isso já era melhor do que usar apenas `COD_CURS`, mas ainda dependia de normalização textual da certificadora.

A nova regra:

```text
COD_INST + COD_CURS + "0" = Código SIAA
```

é mais objetiva, porque usa códigos da própria IES.

Assim:

```text
COD_INST identifica a instituição/certificadora.
COD_CURS identifica o curso.
O sufixo "0" completa o padrão do Código SIAA.
Código SIAA identifica a oferta exata na planilha original.
```

Portanto, a chave principal recomendada passa a ser:

```text
SIAA_KEY
```

E a chave textual:

```text
COD_CURS + IES_KEY
```

fica como validação auxiliar, diagnóstico ou fallback.

---

## Avaliação das alternativas anteriores

### Alternativa 1 — Match por `Cód. Curso` retornando todos os polos

Não recomendado.

Como existe mais de uma oferta para o mesmo `Cód. Curso`, esse desenho tende a criar um cruzamento indevido entre:

```text
todas as ofertas daquele curso
×
todos os polos daquele curso
```

Isso pode gerar duplicidade e associar ofertas de uma certificadora a polos de outra certificadora.

Risco:

```text
Alto risco de duplicidade e de oferta incorreta por polo.
```

---

### Alternativa 2 — Match por `Código SIAA` e depois por `Cód. Curso`

Com a nova regra, essa alternativa fica mais próxima do ideal, mas com uma diferença importante:

Não é necessário usar apenas o `Código SIAA` isolado.

O ideal é gerar o `Código SIAA esperado` a partir da relação de polos:

```text
COD_INST + COD_CURS + "0"
```

e então bater esse valor contra o `Código SIAA` da planilha original.

Assim, a relação de polos continua dizendo onde o curso existe, mas a oferta é localizada diretamente pelo código SIAA esperado.

---

# Estratégia recomendada

Usar a seguinte chave principal:

```text
SIAA_KEY = COD_INST + COD_CURS + "0"
```

E fazer o match contra:

```text
Código SIAA
```

da planilha original de ofertas.

Depois do match:

```text
A relação de polos define onde o curso existe.
O SIAA_KEY define qual oferta exata deve ser aplicada.
O ID_POLO continua definindo o campus.
O EXP de Campus continua separando Grupo e 3719.
```

---

## Fluxo recomendado

```text
1. Carregar planilha de ofertas
2. Carregar relação de polos × cursos
3. Fazer unpivot/melt das colunas CURSO_<COD>
4. Manter apenas linhas marcadas com X
5. Extrair COD_CURS da coluna CURSO_<COD>
6. Normalizar COD_INST
7. Normalizar COD_CURS
8. Criar SIAA_KEY = COD_INST + COD_CURS + "0"
9. Normalizar Código SIAA da planilha de ofertas
10. Fazer match SIAA_KEY -> Código SIAA
11. Copiar os atributos da oferta encontrada
12. Fazer lookup do ID_POLO contra EXP Campus
13. Separar Grupo e 3719
14. Calcular descontos
15. Gerar MSP final
```

---

## Exemplo conceitual

### Relação de polos após unpivot

| ID_POLO | NOM_FILI | COD_INST | COD_CURS |
|---:|---|---:|---:|
| 55 | UNICID - GRADUAÇÃO EAD | 18 | 370 |

Criar chave:

```text
SIAA_KEY = "18" + "370" + "0"
SIAA_KEY = "183700"
```

### Planilha original de ofertas

| Cód. Curso | Certificadora | Código SIAA | Curso |
|---:|---|---:|---|
| 370 | Unicid - Graduação Ead | 183700 | Administração |

Match:

```text
relação.SIAA_KEY = ofertas.Código SIAA
183700 = 183700
```

Resultado:

```text
O polo 55 recebe a oferta Código SIAA 183700.
```

---

# Ajuste principal no código

## Problema atual

Hoje o fluxo possui uma etapa semelhante a:

```python
_consolidate_offers_by_course()
```

Essa etapa deduplica as ofertas por `Cód. Curso`.

Para este caso, isso é perigoso, porque remove ofertas válidas de outras certificadoras/instituições.

---

## Ajuste recomendado

Trocar a consolidação por curso para uma consolidação por `Código SIAA`.

Exemplo:

```python
_consolidate_offers_by_siaa()
```

A chave de deduplicação/conflito deve ser:

```python
["SIAA_KEY"]
```

ou diretamente:

```python
["Código SIAA"]
```

depois da normalização.

Como a relação de polos gera o SIAA esperado, a planilha de ofertas deve ser única por `Código SIAA`.

Nas planilhas analisadas:

```text
Código SIAA únicos na planilha de ofertas: 833
Linhas na planilha de ofertas: 833
```

Ou seja, não há duplicidade de `Código SIAA` na planilha original analisada.

---

# Sugestão de implementação

## 1. Normalizar códigos

Criar ou reaproveitar um utilitário de normalização:

```python
import pandas as pd
import re

def normalize_code(value):
    if pd.isna(value):
        return ""

    value = str(value).strip()
    value = re.sub(r"\.0$", "", value)

    return value
```

---

## 2. Normalizar `Código SIAA` na planilha de ofertas

```python
offers["SIAA_KEY"] = offers["Código SIAA"].apply(normalize_code)
```

Também é recomendado normalizar `Cód. Curso`, pois ele ainda será útil para metadata, validações e logs:

```python
offers["COD_CURS"] = offers["Cód. Curso"].apply(normalize_code)
```

---

## 3. Fazer o unpivot da relação de polos

A relação vem no formato pivotado:

```text
ID_POLO | NOM_FILI | COD_INST | CURSO_369 | CURSO_370 | ...
```

Após o melt/unpivot:

```text
ID_POLO | NOM_FILI | COD_INST | course_col | active
```

Exemplo:

```python
course_cols = [
    col for col in offers_to_campus.columns
    if str(col).startswith("CURSO_")
]

fixed_cols = [
    col for col in offers_to_campus.columns
    if col not in course_cols
]

offers_to_campus = offers_to_campus.melt(
    id_vars=fixed_cols,
    value_vars=course_cols,
    var_name="course_col",
    value_name="active"
)
```

Manter apenas linhas marcadas com `X`:

```python
offers_to_campus = offers_to_campus[
    offers_to_campus["active"]
    .astype(str)
    .str.strip()
    .str.upper()
    .eq("X")
].copy()
```

Extrair `COD_CURS`:

```python
offers_to_campus["COD_CURS"] = (
    offers_to_campus["course_col"]
    .astype(str)
    .str.replace("CURSO_", "", regex=False)
    .apply(normalize_code)
)
```

---

## 4. Criar `SIAA_KEY` na relação de polos

```python
offers_to_campus["COD_INST"] = (
    offers_to_campus["COD_INST"]
    .apply(normalize_code)
)

offers_to_campus["SIAA_KEY"] = (
    offers_to_campus["COD_INST"].astype(str)
    + offers_to_campus["COD_CURS"].astype(str)
    + "0"
)
```

Exemplo:

```text
COD_INST = 75
COD_CURS = 514

SIAA_KEY = 755140
```

---

## 5. Fazer o match contra a planilha original

Opção com `merge`:

```python
offers_to_campus = offers_to_campus.merge(
    offers,
    on="SIAA_KEY",
    how="left",
    suffixes=("", "_offer")
)
```

Opção mantendo o padrão de `xlookup`:

```python
xlookup(
    left_df=offers_to_campus,
    right_df=offers,
    left_key="SIAA_KEY",
    right_key="SIAA_KEY",
    columns_to_return=[
        "Código SIAA",
        "Cód. Curso",
        "Cód. IES",
        "Cód. Campus",
        "Curso",
        "Grau",
        "Modalidade",
        "Duração",
        "Preço SIAA",
        "Porcentagem com Desconto 1° ano",
        "Desconto Garantido Demais Semestres",
        "Certificadora",
    ],
)
```

---

# Papel do `COD_CURS + IES_KEY`

A chave anterior:

```text
COD_CURS + IES_KEY
```

não precisa ser a chave principal.

Mas ainda é útil como validação auxiliar.

Ela pode ajudar a detectar casos onde:

```text
COD_INST aponta para uma instituição
mas NOM_FILI ou Certificadora aponta para outra
```

Recomendação:

```text
Usar SIAA_KEY para o match principal.
Usar COD_CURS + IES_KEY como diagnóstico.
```

---

## Normalização auxiliar de IES

Mesmo que `IES_KEY` deixe de ser a chave principal, ainda é útil normalizar os nomes para relatórios e validações.

```python
import unicodedata
import re

def normalize_text(value):
    if value is None:
        return ""

    value = str(value).strip().upper()

    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        char for char in value
        if not unicodedata.combining(char)
    )

    value = re.sub(r"\s+", " ", value)

    return value


def normalize_ies_key(value):
    text = normalize_text(value)

    if "UNICID" in text:
        return "UNICID"

    if "CRUZEIRO" in text or "UNICSUL" in text:
        return "CRUZEIRO"

    if "UNIFRAN" in text:
        return "UNIFRAN"

    if "FSG" in text:
        return "FSG"

    if "UNIPE" in text:
        return "UNIPE"

    if "BRAZ" in text or "MOGI" in text:
        return "BRAZCUBAS"

    if "POSITIVO" in text:
        return "POSITIVO"

    return text
```

Aplicar nas ofertas:

```python
offers["IES_KEY"] = offers["Certificadora"].apply(normalize_ies_key)
```

Aplicar na relação:

```python
offers_to_campus["IES_KEY"] = offers_to_campus["NOM_FILI"].apply(normalize_ies_key)
```

Criar chave auxiliar:

```python
offers["COURSE_IES_KEY"] = (
    offers["COD_CURS"].astype(str)
    + "|"
    + offers["IES_KEY"].astype(str)
)

offers_to_campus["COURSE_IES_KEY"] = (
    offers_to_campus["COD_CURS"].astype(str)
    + "|"
    + offers_to_campus["IES_KEY"].astype(str)
)
```

---

# Validações recomendadas

## 1. Relação de polos sem oferta correspondente

Após criar `SIAA_KEY` na relação:

```python
relacao_sem_oferta = offers_to_campus[
    ~offers_to_campus["SIAA_KEY"].isin(offers["SIAA_KEY"])
].copy()
```

Sugestão de aba auxiliar:

```text
relacao_sem_oferta
```

Nas planilhas analisadas:

```text
Relações ativas sem oferta correspondente: 3.063 linhas polo × curso
Chaves SIAA únicas da relação sem oferta: 23
```

Exemplos de chaves da relação sem oferta:

| COD_INST | COD_CURS | SIAA_KEY | NOM_FILI |
|---:|---:|---:|---|
| 16 | 453 | 164530 | CRUZEIRO DO SUL - GRADUAÇÃO EAD |
| 18 | 453 | 184530 | UNICID - GRADUAÇÃO EAD |
| 22 | 453 | 224530 | UNIFRAN - GRADUAÇÃO EAD |
| 60 | 453 | 604530 | FSG - GRADUAÇÃO EAD |
| 71 | 453 | 714530 | UNIPÊ - GRADUAÇÃO EAD |
| 75 | 453 | 754530 | BRAZ CUBAS - GRAD EAD |
| 80 | 453 | 804530 | POSITIVO - GRAD. EAD |
| 16 | 455 | 164550 | CRUZEIRO DO SUL - GRADUAÇÃO EAD |
| 18 | 455 | 184550 | UNICID - GRADUAÇÃO EAD |
| 22 | 455 | 224550 | UNIFRAN - GRADUAÇÃO EAD |
| 60 | 455 | 604550 | FSG - GRADUAÇÃO EAD |
| 71 | 455 | 714550 | UNIPÊ - GRADUAÇÃO EAD |
| 75 | 455 | 754550 | BRAZ CUBAS - GRAD EAD |
| 80 | 455 | 804550 | POSITIVO - GRAD. EAD |
| 80 | 477 | 804770 | POSITIVO - GRAD. EAD |
| 75 | 506 | 755060 | BRAZ CUBAS - GRAD EAD |
| 75 | 507 | 755070 | BRAZ CUBAS - GRAD EAD |
| 75 | 508 | 755080 | BRAZ CUBAS - GRAD EAD |
| 75 | 509 | 755090 | BRAZ CUBAS - GRAD EAD |
| 75 | 510 | 755100 | BRAZ CUBAS - GRAD EAD |
| 75 | 511 | 755110 | BRAZ CUBAS - GRAD EAD |
| 75 | 512 | 755120 | BRAZ CUBAS - GRAD EAD |
| 75 | 513 | 755130 | BRAZ CUBAS - GRAD EAD |

---

## 2. Oferta sem relação de polos correspondente

```python
ofertas_sem_relacao = offers[
    ~offers["SIAA_KEY"].isin(offers_to_campus["SIAA_KEY"])
].copy()
```

Sugestão de aba auxiliar:

```text
ofertas_sem_relacao_de_polos
```

Nas planilhas analisadas:

```text
Ofertas sem relação de polos correspondente: 12
```

Exemplos:

| Cód. Curso | Código SIAA | Certificadora | Curso | Grau |
|---:|---:|---|---|---|
| 441 | 714410 | Unipê - Graduação Ead | Radiologia | Tecnólogo |
| 514 | 755140 | Grad Ead - Mogi | Formacao Pedagogica - Biologia | Licenciatura |
| 515 | 755150 | Grad Ead - Mogi | Formacao Pedagogica - Historia | Licenciatura |
| 516 | 185160 | Unicid - Graduação Ead | Formacao Pedagogica - Filosofia | Licenciatura |
| 517 | 185170 | Unicid - Graduação Ead | Formacao Pedagogica - Geografia | Licenciatura |
| 518 | 185180 | Unicid - Graduação Ead | Formacao Pedagogica - Letras Port. E Ing. | Licenciatura |
| 519 | 755190 | Grad Ead - Mogi | Ciencias Biologicas - Licenciados | Graduação 2.0 |
| 520 | 755200 | Grad Ead - Mogi | Historia - Licenciados | Graduação 2.0 |
| 521 | 165210 | Cruzeiro - Graduação Ead | Ciencias Sociais - Licenciados | Graduação 2.0 |
| 522 | 185220 | Unicid - Graduação Ead | Filosofia - Licenciados | Graduação 2.0 |
| 523 | 185230 | Unicid - Graduação Ead | Geografia - Licenciados | Graduação 2.0 |
| 524 | 185240 | Unicid - Graduação Ead | Letras Portugues E Ingles - Licenciados | Graduação 2.0 |

---

## 3. Duplicidade de `Código SIAA` na planilha de ofertas

```python
ofertas_siaa_duplicado = offers[
    offers.duplicated(subset=["SIAA_KEY"], keep=False)
].copy()
```

Sugestão de aba auxiliar:

```text
ofertas_siaa_duplicado
```

Regra:

```text
Se houver duplicidade de Código SIAA, não é seguro seguir automaticamente.
```

Na planilha analisada:

```text
Não foram encontradas duplicidades de Código SIAA.
```

---

## 4. Divergência entre SIAA esperado e dados da oferta

Após o match por `SIAA_KEY`, validar se o curso bate:

```python
divergencia_curso = offers_to_campus[
    offers_to_campus["COD_CURS"].astype(str)
    != offers_to_campus["Cód. Curso"].apply(normalize_code)
].copy()
```

Sugestão de aba auxiliar:

```text
divergencia_cod_curso_siaa
```

Também pode validar a IES/certificadora:

```python
divergencia_ies = offers_to_campus[
    offers_to_campus["IES_KEY"]
    != offers_to_campus["IES_KEY_offer"]
].copy()
```

Sugestão de aba auxiliar:

```text
divergencia_ies_siaa
```

Essas abas ajudam a detectar erro da planilha de origem.

---

# Tratamento de `Grau` não mapeado

## Valores encontrados

Na planilha de ofertas analisada, os valores de `Grau` foram:

| Grau | Linhas |
|---|---:|
| Tecnólogo | 396 |
| Bacharelado | 264 |
| Licenciatura | 96 |
| Graduação 2.0 | 71 |
| Abi | 6 |

O mapa atual da feature contempla principalmente:

```text
BACHARELADO
TECNÓLOGO
LICENCIATURA
BACH / LICENC
```

Sem tratamento adicional, os valores:

```text
Graduação 2.0
Abi
```

podem ficar sem mapeamento e cair no `_remove_nan_offers`.

---

## Regra definida

Conforme decisão de negócio:

```text
Graduação 2.0 -> Segunda graduação
```

Para `Abi`, recomendação:

```text
Abi -> Bacharelado + Licenciatura (graduação)
```

---

## Mapa recomendado

```python
kinds_map = {
    "BACHARELADO": "Bacharelado (graduação)",
    "TECNOLOGO": "Tecnólogo (graduação)",
    "LICENCIATURA": "Licenciatura (graduação)",
    "BACH / LICENC": "Bacharelado + Licenciatura (graduação)",

    # Novos tratamentos
    "GRADUACAO 2.0": "Segunda graduação",
    "ABI": "Bacharelado + Licenciatura (graduação)",
}
```

---

## Normalização recomendada para `Grau`

```python
import unicodedata
import re

def normalize_grade(value):
    if value is None:
        return ""

    value = str(value).strip().upper()

    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        char for char in value
        if not unicodedata.combining(char)
    )

    value = re.sub(r"\s+", " ", value)

    return value
```

Aplicação:

```python
df["GRAU_NORMALIZADO"] = df["Grau"].apply(normalize_grade)
df["level"] = df["GRAU_NORMALIZADO"].map(kinds_map)
```

Se em algum ponto a coluna já tiver sido renomeada para `GRAU`, usar:

```python
df["GRAU_NORMALIZADO"] = df["GRAU"].apply(normalize_grade)
df["level"] = df["GRAU_NORMALIZADO"].map(kinds_map)
```

---

## Validação de grau antes de remover nulos

Antes do `_remove_nan_offers`, criar uma validação:

```python
grau_nao_mapeado = df[df["level"].isna()].copy()
```

Sugestão de aba auxiliar:

```text
grau_nao_mapeado
```

Ou, para log simples:

```python
unmapped_grades = (
    df.loc[df["level"].isna(), "Grau"]
    .dropna()
    .drop_duplicates()
    .sort_values()
)

if not unmapped_grades.empty:
    print("Grau não mapeado:")
    print(unmapped_grades.to_list())
```

---

# Tratamento do `Código SIAA`

O `Código SIAA` deve ser a chave da oferta final.

Recomendado:

```text
Gerar SIAA_KEY na relação de polos.
Bater SIAA_KEY com Código SIAA da planilha original.
Usar os dados da oferta encontrada para preencher a MSP.
```

Na MSP final:

```text
COD SIAA = Código SIAA da oferta encontrada
```

---

# Separação Grupo × 3719

A separação Grupo × 3719 deve continuar do jeito atual.

O fluxo atual usa:

```text
ID_POLO -> metadata_code
```

contra o EXP de Campus para preencher:

```text
lookup_group
lookup_3719
```

Essa parte não precisa mudar.

O novo desenho mexe apenas no match entre:

```text
relação de polos × cursos
e
planilha de ofertas
```

Depois disso, a geração de ofertas para Grupo e 3719 segue a regra atual.

---

# Impacto no pipeline

## InitialTreatments.py

- [ ] Manter o unpivot/melt da relação de polos.
- [ ] Extrair `COD_CURS` de `CURSO_<COD>`.
- [ ] Normalizar `COD_INST`.
- [ ] Normalizar `COD_CURS`.
- [ ] Criar `SIAA_KEY = COD_INST + COD_CURS + "0"`.
- [ ] Normalizar `Código SIAA` na planilha de ofertas.
- [ ] Evitar deduplicar ofertas por `Cód. Curso`.
- [ ] Consolidar ofertas por `SIAA_KEY`.
- [ ] Criar abas auxiliares para:
  - `relacao_sem_oferta`
  - `ofertas_sem_relacao_de_polos`
  - `ofertas_siaa_duplicado`

---

## AdjustmentsOffersPattern.py

- [ ] Trocar o join simples por `COD_CURS` para join por `SIAA_KEY`.
- [ ] Garantir que `Código SIAA` venha da oferta encontrada.
- [ ] Manter preenchimento de metadados fixos.
- [ ] Adicionar tratamento de `Grau`:
  - `Graduação 2.0 -> Segunda graduação`
  - `Abi -> Bacharelado + Licenciatura (graduação)`
- [ ] Validar `Grau` antes de `_remove_nan_offers`.
- [ ] Gerar auxiliar `grau_nao_mapeado`, se possível.

---

## MspGenerate.py

- [ ] Manter lookup `ID_POLO -> metadata_code`.
- [ ] Manter separação Grupo × 3719.
- [ ] Manter cálculo de descontos.
- [ ] Manter separação de descontos negativos.
- [ ] Avaliar incluir `COD SIAA` na deduplicação final.

Sugestão para a deduplicação final:

Hoje a deduplicação por SKU usa algo próximo de:

```text
university_id
campus_id
name
level
kind
Turno
Semestre de Ingresso
max_payments
full_price
```

Avaliar adicionar:

```text
COD SIAA
```

ou garantir que a deduplicação ocorra apenas depois que a oferta correta já foi determinada via `SIAA_KEY`.

---

# Descontos negativos

A feature já possui regra para separar ofertas em que:

```text
desconto_balcao_final < 0
```

Isso ocorre quando:

```text
Desconto Garantido Demais Semestres < 0.05
```

Essas ofertas devem continuar indo para a aba:

```text
Ofertas com Desconto Negativo
```

---

# Fluxo final recomendado

```text
Ofertas da IES
    ├─ normalizar Código SIAA -> SIAA_KEY
    ├─ normalizar Cód. Curso -> COD_CURS
    ├─ normalizar Grau
    └─ consolidar por SIAA_KEY

Relação Cursos × Polos
    ├─ unpivot CURSO_<COD>
    ├─ filtrar X
    ├─ extrair COD_CURS
    ├─ normalizar COD_INST
    ├─ criar SIAA_KEY = COD_INST + COD_CURS + "0"
    └─ manter ID_POLO para lookup de campus

Join
    └─ relação.SIAA_KEY -> ofertas.SIAA_KEY

Depois do join
    ├─ copiar Código SIAA
    ├─ copiar curso, grau, modalidade, duração, preço e descontos
    ├─ mapear Grau para level
    ├─ lookup ID_POLO -> EXP Campus
    ├─ separar Grupo e 3719
    ├─ calcular descontos
    ├─ separar negativos
    └─ gerar MSP final
```

---

# Regra final recomendada

Usar a seguinte regra de match:

```text
SIAA_KEY = COD_INST + COD_CURS + "0"
```

comparando com:

```text
Código SIAA
```

da planilha original.

Resumo:

```text
COD_INST define a instituição.
COD_CURS define o curso.
COD_INST + COD_CURS + "0" define o Código SIAA esperado.
Código SIAA localiza a oferta exata.
ID_POLO define o campus.
EXP Campus separa Grupo e 3719.
Grau normalizado define o level da MSP.
```

Essa abordagem evita duplicidade por `Cód. Curso`, reduz dependência de nome textual de certificadora e garante que cada polo receba a oferta correta da instituição correspondente.

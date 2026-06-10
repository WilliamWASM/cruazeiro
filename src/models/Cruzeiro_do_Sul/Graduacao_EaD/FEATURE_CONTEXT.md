# Feature — Cruzeiro do Sul / Graduação EaD

Documento de referência completo para a feature de geração MSP do grupo Cruzeiro (Cogna) para o produto Graduação EaD. Consolida todo o contexto das refatorações realizadas, regras de negócio e funcionamento atual do código.

---

## 1. Visão geral

O objetivo da feature é receber três planilhas da IES (Ofertas, Relação de Cursos×Polos e EXP de Campus), processar os dados conforme as regras de negócio, e gerar um arquivo Excel de saída com as abas:

- **Ofertas Grupo** — ofertas que pertencem a campi do grupo (qualquer `university_id` ≠ 3719)
- **Ofertas 3719** — ofertas que pertencem ao campus virtual Cruzeiro (`university_id = 3719`)
- Abas auxiliares (somente se não vazias): `campi_not_found`, `apenas_no_virtual`, `criar_no_3719`, `ofertas_codigo_conflitos`, `relacao_sem_oferta`, `ofertas_sem_relacao`, `Ofertas com Desconto Negativo`

> **Chave de match (refatoração):** a oferta de cada polo é localizada pela `MATCH_KEY = COD_INST + "|" + COD_CURS` (relação de polos) batendo contra `Cód. Campus + "|" + Cód. Curso` (planilha de ofertas). Antes o match usava só `Cód. Curso`, o que fazia todos os polos de um curso receberem a oferta da primeira certificadora — independentemente da instituição do polo. A nova chave desambigua por instituição.

---

## 2. Entradas (inputs do usuário)

### 2.1 Arquivos (na ordem da UI)

| Posição | Label na UI | Papel |
|---|---|---|
| paths[0] | "Selecione Ofertas" | Planilha de ofertas da IES |
| paths[1] | "Selecione Rel. Cursos" | Planilha de relação Polos × Cursos |
| paths[2] | "Selecione EXP de Campus" | Planilha EXP de campus do sistema interno |

### 2.2 Campos de texto (na ordem da UI)

| Posição | Label na UI | Parâmetro no código |
|---|---|---|
| inputs[0] | "Semestre de Ingresso" | `enrollment_semester` (ex: `"2026.1"`) |
| inputs[1] | "Data End" | `end_date` (ex: `"31/12/2026"`) |
| inputs[2] | "OSC" | `special_condition` (ex: `"OSC_ABC"`) |

> O controller (`cruzeiro_controller.py`) chama `grad.set_values(inputs[0], inputs[1], inputs[2])` que mapeia diretamente para `set_values(self, enrollment_semester, end_date, special_condition)`.

---

## 3. Formato das planilhas de entrada

### 3.1 Planilha de Ofertas (`cruzeiro_offers`)

Detectada pelo `SheetManipulation` por um conjunto de headers obrigatórios. Colunas relevantes:

| Coluna da IES | Papel no sistema |
|---|---|
| `Cód. Curso` | Parte da chave de match (COD_CURS) |
| `Cód. IES` | Código da IES no sistema da IES |
| `Cód. Campus` | Código da **instituição/certificadora** — corresponde ao `COD_INST` da relação de polos. Junto com `Cód. Curso` forma a `MATCH_KEY` |
| `Código SIAA` | Código SIAA do curso |
| `Curso` | Nome do curso |
| `GRAU` (ou `Grau`) | Grau do curso (BACHARELADO, TECNÓLOGO, etc.) |
| `Modalidade` | Modalidade (100% EAD, SEMIPRESENCIAL, AO VIVO, DIGITAL) |
| `Duração` | Duração em semestres |
| `Preço SIAA` | Mensalidade sem desconto |
| `Porcentagem com Desconto 1° ano` | Desconto do 1º semestre (decimal, ex: 0.20) |
| `Desconto Garantido Demais Semestres` | Desconto regressivo garantido (decimal, ex: 0.10) |
| `Certificadora` | Nome da IES certificadora (mapeado para `university_name`) |

As colunas de percentual são normalizadas pelo `adjust_columns_offers_cruzeiro` no carregamento (vírgula → ponto, formatado como `"0.20"`).

### 3.2 Planilha de Relação Polos × Cursos (`cruzeiro_offers_to_campus`)

Formato **matricial (pivotado)**: colunas fixas de identificação do polo + colunas `CURSO_<COD>` com `"X"` indicando que o polo oferece aquele curso.

Colunas fixas relevantes:

| Coluna | Papel |
|---|---|
| `ID_POLO` | ID do polo no sistema da IES → usado como `metadata_code` no lookup contra o EXP de campus |
| `NOME_POL` | Nome do polo |
| `NOM_FILI` | Nome da filial/IES (mapeado para `university_name`) |
| `COD_INST` | Código da instituição |
| `CIDADE`, `ESTADO` | Opcionais |

Colunas de curso: `CURSO_369`, `CURSO_412`, etc.

O `InitialTreatments` faz **unpivot** (melt) dessas colunas → filtra apenas linhas com `"X"` → extrai `COD_CURS` da string `"CURSO_<COD>"`.

### 3.3 EXP de Campus (`exp_campus`)

Tabela interna do sistema com todos os campi. Colunas relevantes:

| Coluna | Papel |
|---|---|
| `id` | ID interno do campus (usado como `campus_id` na saída) |
| `metadata_code` | Código do campus no sistema da IES → chave do lookup por `ID_POLO` |
| `university_id` | ID da universidade (`"3719"` = campus virtual Cruzeiro) |
| `name` | Nome do campus |
| `university_name` | Nome da universidade |

---

## 4. Fluxo de processamento

```
CruzeiroController.process_grad()
 │
 ├─ ModifyHandler.__init__(offers, campus_relation, exp_campus)
 │   └─ InitialTreatments.load()
 │       ├─ _load_dataframes()               — SheetManipulation carrega os 3 arquivos
 │       ├─ _normalize_offer_headers()       — padroniza "Grau" → "GRAU"
 │       ├─ _normalize_loaded_keys()         — normaliza chaves (str, strip, remove .0)
 │       ├─ _build_offers_match_key()        — MATCH_KEY = Cód. Campus + "|" + Cód. Curso (ofertas)
 │       ├─ _detect_offer_conflicts()        — flag MATCH_KEY duplicada → offer_conflicts (NÃO descarta ofertas)
 │       ├─ _unpivot_campus_relation()       — matriz → long; extrai COD_CURS; MATCH_KEY = COD_INST + "|" + COD_CURS; dedup (ID_POLO, COD_CURS)
 │       ├─ _build_validation_frames()       — relacao_sem_oferta / ofertas_sem_relacao
 │       ├─ _separate_group()               — campus_virtual (university_id=3719) vs campus_group
 │       ├─ _normalize_ies_names()          — NOM_FILI → nome padronizado (name_ies_map)
 │       ├─ _verify_offers_to_campus_not_match() — xlookup ID_POLO→metadata_code para grupo e virtual
 │       └─ _verify_campus_totally_existence()   — separa not_totally_group / not_totally_virtual
 │
 ├─ ModifyHandler.set_values(enrollment_semester, end_date, special_condition)
 │   └─ AdjustmentsOffersPattern.load()     — para offers_to_campus (e aux se não vazios)
 │       ├─ _multiples_xlookup()            — join MATCH_KEY → MATCH_KEY; traz atributos da oferta
 │       ├─ _columns_treatment()            — mapeia GRAU, METODOLOGIA, limpa DURAÇÃO
 │       ├─ _adjusts_offers()              — preenche metadados fixos (Turno, Semestre, etc.)
 │       └─ _remove_nan_offers()           — remove linhas com GRAU nulo
 │
 └─ ModifyHandler.load(fullpath)
     └─ MspGenerate.load()
         ├─ _set_campus_ids()              — campus_id = lookup_group
         ├─ _process_discounts()           — calcula todos os descontos (×100, inteiros)
         ├─ _separate_negative_discounts() — filtra desconto_balcao_final < 0
         ├─ _compute_derived_values()      — metadata, COD SIAA, campos nulos
         ├─ _fill_in_remaining_values()    — lookup campus fields (grupo); ExtraWarningGenerate
         ├─ _generate_virtual_offers()     — split lookup_3719; lookup virtual; aviso certificação
         ├─ _deduplicate_by_sku()          — dedup por 9 campos (grupo e virtual separados)
         ├─ _finalize_dataframe()          — rename → FINAL_COLUMNS (grupo e virtual)
         └─ retorna (offers_group, offers_virtual, offers_negative_discount)
```

---

## 5. Regras de negócio — Descontos

### 5.1 Lógica de regressão por semestre de ingresso

O semestre de ingresso determina quando o desconto regride:

| Semestre | `period` | `second_disc` | `last_disc` |
|---|---|---|---|
| `XXXX.1` | 1 | `first_disc` (sem regressão no 2º sem) | `DESCONTO GARANTIDO` |
| `XXXX.2` | 2 | `DESCONTO GARANTIDO` (regride já no 2º) | `DESCONTO GARANTIDO` |

> O 2º semestre de um ingresso em `.1` ainda é um semestre `.2` (julho), portanto sem regressão. A regressão só ocorre em janeiro (semestre `.1` seguinte), que é o 3º semestre.

### 5.2 Cálculo dos campos de desconto (todos ×100 → inteiro)

| Campo na saída | Fórmula | Exemplo (20% e 10% regressivo) |
|---|---|---|
| `discount_percentage` | `first_disc × 100` | 20 |
| `commercial_discount` | `(first_disc − 0.05) × 100` | 15 |
| `real_discount` | `last_disc × 100` | 10 |
| `desconto_balcao_final` | `(last_disc − 0.05) × 100` | 5 |
| `regressive_commercial_discount` | `(first_disc − last_disc) × 100` | 10 |
| `regressive_discount` | `second_disc × 100` | 10 |
| `university_regressive_discount` | `(last_disc − 0.05) × 100` | 5 |
| `first_regressive_discount` | `first_disc × 100` | 20 |
| `second_regressive_discount` | `second_disc × 100` | 10 |
| `last_regressive_discount` | `last_disc × 100` | 10 |

> `offered_price` não é preenchido (fica `None` na saída).

### 5.3 Separação de ofertas com desconto negativo

Após `_process_discounts`, qualquer linha onde `desconto_balcao_final < 0` (ou seja, `last_disc < 0.05`) é extraída para `offers_negative_discount` e **não entra** nas abas principais. Essas linhas vão para a aba auxiliar **"Ofertas com Desconto Negativo"**.

---

## 6. Separação Grupo × 3719

A separação ocorre em dois momentos:

**1. `InitialTreatments._verify_offers_to_campus_not_match`:**
- Faz `xlookup(ID_POLO → metadata_code)` contra `campus_group` → popula `lookup_group`
- Faz `xlookup(ID_POLO → metadata_code)` contra `campus_virtual` → popula `lookup_3719`
- Linhas sem nenhum match → `campus_offers_undefined` (aba `campi_not_found`)
- Linhas apenas no virtual (`lookup_group` nulo) → `not_totally_group` (aba `apenas_no_virtual`)
- Linhas apenas no grupo (`lookup_3719` nulo) → `not_totally_virtual` (aba `criar_no_3719`)

**2. `MspGenerate._generate_virtual_offers`:**
- Linhas com `lookup_3719` preenchido → `offers_virtual`; `campus_id = lookup_3719`; lookup no `campus_virtual`; `university_id = '3719'`; aviso `"Certificado pela <IES>"`
- Linhas com `lookup_group` preenchido → permanecem em `campus_offers`; `campus_id = lookup_group`; lookup no `campus_group`

> Um polo que existe em **ambos** os grupos gera ofertas nas duas abas.

---

## 7. Mapas de normalização

### 7.1 Certificadora → university_name (`name_ies_map`)

| Valor no campo `NOM_FILI` / `Certificadora` | `university_name` no sistema |
|---|---|
| UNICID - GRADUAÇÃO EAD | UNICID |
| CRUZEIRO DO SUL - GRADUAÇÃO EAD | UNICSUL - Cruzeiro do Sul |
| UNIFRAN - GRADUAÇÃO EAD | UNIFRAN |
| FSG - GRADUAÇÃO EAD | FSG |
| UNIPÊ - GRADUAÇÃO EAD | UNIPÊ |
| BRAZ CUBAS - GRAD EAD | Brazcubas |
| POSITIVO - GRAD. EAD | Universidade Positivo |

### 7.2 GRAU → `level` (`kinds_map`)

| Valor da IES | Valor MSP |
|---|---|
| BACHARELADO | Bacharelado (graduação) |
| TECNÓLOGO | Tecnólogo (graduação) |
| LICENCIATURA | Licenciatura (graduação) |
| BACH / LICENC | Bacharelado + Licenciatura (graduação) |
| GRADUAÇÃO 2.0 | Segunda graduação |
| ABI | Bacharelado + Licenciatura (graduação) |

### 7.3 Modalidade → `kind` / `shift` (`shift_map`)

| Valor da IES | Valor MSP |
|---|---|
| 100% EAD | EaD |
| DIGITAL | EaD |
| SEMIPRESENCIAL | Semipresencial |
| AO VIVO | Ao vivo |

### 7.4 Avisos por modalidade (`ExtraWarningGenerate`)

| `kind` | Aviso gerado |
|---|---|
| EaD | "EaD 100% Virtual, sendo necessário que o aluno se matricule…" |
| Ao vivo | "EaD 100% Virtual com Aulas ao vivo, sendo necessário…" |
| Semipresencial | "O EAD Semipresencial une o melhor do ensino a distância…" |

Cursos com `"2.0"` no nome recebem um aviso especial (comprovação de 160h).

Ofertas do grupo virtual (3719) recebem `" | Certificado pela <IES>"` concatenado ao aviso.

---

## 8. Campos preenchidos automaticamente (não vêm da IES)

| Campo | Valor |
|---|---|
| `Turno` | `"Virtual"` |
| `Tipo de duração do curso` | `"semestre"` |
| `Qual valor usar?\n% ou R$` | `"porcentagem"` |
| `LIMITADA?` | `"FALSE"` |
| `Data de Início da Oferta` | Data atual (`dd/mm/yyyy`) |
| `Data de Fim da Oferta` | `end_date` (input do usuário) |
| `Benefício 1 (Chave OSC)` | `special_condition` (input do usuário) |
| `Semestre de Ingresso` | `enrollment_semester` (input do usuário) |
| `total_seats` | `None` |
| `max_payments` | `None` |
| `course_metadata` | `None` |
| `offer_extra_benefit` | `None` |
| `offered_price` | `None` (não calculado) |
| `metadata` | `code:<COD_CURS>;campus_code:<ID_POLO>;ies_code:<CÓD_IES>` |

---

## 9. Schema de saída (`FINAL_COLUMNS`)

```python
[
    'commercial_discount', 'university_regressive_discount', 'discount_percentage',
    'real_discount', 'desconto_balcao_final', 'regressive_discount', 'regressive_commercial_discount',
    'first_regressive_discount', 'second_regressive_discount', 'last_regressive_discount',
    'offered_price', 'name_from_university', 'university_name', 'university_id',
    'campus_name', 'campus_id', 'name', 'level', 'kind', 'shift', 'period_kind',
    'max_periods', 'COD SIAA', 'full_price', 'start', 'end', 'limited', 'total_seats',
    'offer_special_conditions', 'offer_extra_warning', 'enrollment_semester',
    'max_payments', 'metadata', 'course_metadata', 'offer_extra_benefit'
]
```

Renomeamentos aplicados em `_finalize_dataframe`:

| Nome interno | Nome final |
|---|---|
| `PORCENTAGEM DE DESCONTO` | `first_regressive_discount` |
| `_second_disc` | `second_regressive_discount` |
| `_last_disc` | `last_regressive_discount` |
| `Turno` | `shift` |
| `Tipo de duração do curso` | `period_kind` |
| `LIMITADA?` | `limited` |
| `Data de Início da Oferta` | `start` |
| `Data de Fim da Oferta` | `end` |
| `Benefício 1 (Chave OSC)` | `offer_special_conditions` |
| `Semestre de Ingresso` | `enrollment_semester` |
| `Avisos` | `offer_extra_warning` |

---

## 10. Deduplicação por SKU

Após o split grupo/virtual e antes da finalização, cada DataFrame é deduplicado pela combinação:

```
university_id + campus_id + name + level + kind + Turno + Semestre de Ingresso + max_payments + full_price
```

Colunas ausentes são ignoradas silenciosamente.

---

## 11. Arquivos do módulo

| Arquivo | Responsabilidade |
|---|---|
| `ModifyHandler.py` | Orquestrador: inicializa, chama tratamentos, gera saída Excel |
| `InitialTreatments.py` | Carregamento, unpivot, normalização de chaves, separação grupo/virtual |
| `AdjustmentsOffersPattern.py` | Join por `COD_CURS`, mapeamento de enums, preenchimento de metadados fixos |
| `MspGenerate.py` | Cálculo de descontos, geração das abas grupo e virtual, finalização |
| `ExtraWarningGenerate.py` | Geração do campo `Avisos` por modalidade do curso |
| `CONTEXT.md` | Contexto original da refatoração (formato de entrada e decisões de design) |
| `Refatoração_Pt2.md` | Detalhamento das regras de negócio e relação polo↔oferta |
| `Last_refactor.md` | Regras finais de cálculo de descontos e preenchimento da planilha |
| `FEATURE_CONTEXT.md` | Este arquivo — referência consolidada |

**Dependências externas:**
- `src/models/excel_file/SheetManipulation.py` — detecção de tipo e carregamento dos arquivos
- `src/models/excel_file/DataFrameUtils.py` — utilitários DataFrame (xlookup, normalize, dedup, save)
- `src/gui/controllers/sections/cruzeiro_controller.py` — ponto de entrada via GUI
- `src/config/configurations.py` — configuração dos labels e ordem dos inputs na UI

---

## 12. Pontos de atenção

- **Normalização de chaves numéricas**: códigos como `370.0` (float do pandas) são normalizados via `.astype(str).str.replace(r'\.0$','',regex=True).str.strip()` antes de qualquer `xlookup`.
- **DataFrame vazio antes de atribuição escalar**: `_generate_virtual_offers` guarda contra `empty` antes de atribuir `university_id = '3719'`.
- **Ofertas com GRAU nulo**: removidas por `_remove_nan_offers` em `AdjustmentsOffersPattern` após o join.
- **Conflitos de código de curso**: se o mesmo `Cód. Curso` aparece com dados diferentes na planilha de ofertas, a primeira ocorrência é mantida e as demais vão para `offer_conflicts` (aba `ofertas_codigo_conflitos`).
- **Descontos negativos**: `desconto_balcao_final = (last_disc − 0.05) × 100 < 0` significa que o desconto regressivo é menor que 5% (comissão mínima). Essas ofertas vão para a aba **"Ofertas com Desconto Negativo"**.

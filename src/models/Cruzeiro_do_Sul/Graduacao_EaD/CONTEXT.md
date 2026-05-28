# Contexto — Refatoração Cruzeiro do Sul / Graduação EaD

## Objetivo geral
Refatorar o fluxo de geração MSP do grupo Cruzeiro (Cogna) para o novo formato de planilhas enviado pela IES. Saída deve gerar **duas abas principais** (`Ofertas Grupo` e `Ofertas 3719`) e remover colunas não utilizadas.

## Mudanças de formato (entrada)

### Planilha de Polos × Cursos (campus_relation)
- Antes: formato longo (uma linha por par polo+curso).
- Agora: **matriz pivotada** — colunas fixas de identificação do polo + várias colunas `CURSO_<COD>` contendo `"X"` quando o polo oferece o curso.
- Colunas fixas: `ID_POLO`, `NOME_POL`, `NOM_FILI`, `COD_INST` (+ `CIDADE`, `ESTADO` quando presentes).
- Tratamento: `melt` (unpivot) → manter apenas linhas com `"X"` → extrair `COD_CURS` da string `CURSO_<COD>`.

### Planilha de Ofertas (offers)
- Novas colunas: `Cód. IES`, `Cód. Campus`, `Cód. Curso`, `Curso`, `GRAU`, `Modalidade`, `Duração`, `Preço SIAA`, `Porcentagem com Desconto 1° ano`, `Desconto Garantido Demais Semestres`, `Certificadora`, `Código SIAA`.
- Chave de junção polo↔oferta: **`COD_CURS` (código do curso)** — não mais o nome do curso.

## Decisões de design
1. **Join por código apenas** (`COD_CURS` ↔ `Cód. Curso`). Sem fallback por nome.
2. **Sem `ID_POLO_HUB`** — polo identificado só por `ID_POLO`.
3. **Nome da IES** vem do campo `Certificadora` da oferta (mapeado para o `university_name` esperado no exp-campus).
4. **Validação dupla de polo**: cruza `ID_POLO` contra `campus_group` e `campus_virtual` separadamente. Polo é mantido se existir em **pelo menos um** dos dois (ofertas geradas para o lado existente). Polos ausentes nos dois vão para `campi_not_found`.
5. **Saídas separadas**:
   - `Ofertas Grupo` — linhas com `lookup_group` resolvido.
   - `Ofertas 3719` — linhas com `lookup_3719` resolvido; recebem `Avisos += " | Certificado pela <IES>"`, `university_id = '3719'` e `name_from_university = 'Cruzeiro Virtual'`.
   - Abas auxiliares apenas se não vazias.
6. **Descontos regressivos**: continuam dependentes do semestre de ingresso (`.1` → regressão no 3º; `.2` → regressão no 2º). Comercial (IES) = aluno − 5%.

## Arquivos tocados
- `src/models/excel_file/SheetManipulation.py` — HEADERS, dtypes, ajuste de colunas (novo formato).
- `src/models/Cruzeiro_do_Sul/Graduacao_EaD/InitialTreatments.py` — unpivot da matriz, normalização de IES, validação dupla.
- `src/models/Cruzeiro_do_Sul/Graduacao_EaD/AdjustmentsOffersPattern.py` — xlookup por `COD_CURS`, mapas de `kinds`/`shift`.
- `src/models/Cruzeiro_do_Sul/Graduacao_EaD/MspGenerate.py` — geração das duas saídas, finalização de colunas (`FINAL_COLUMNS`).
- `src/models/Cruzeiro_do_Sul/Graduacao_EaD/ModifyHandler.py` — orquestração + escrita das abas.
- `src/models/Cruzeiro_do_Sul/Graduacao_EaD/ExtraWarningGenerate.py` — geração de avisos por modalidade (inalterado em sua essência).

## Fluxo (resumo)
```
ModifyHandler
 ├─ InitialTreatments.load()
 │   ├─ _load_dataframes
 │   ├─ _unpivot_campus_relation   (matriz → long; X → linhas)
 │   ├─ _separate_group            (campus_virtual=3719; campus_group=resto)
 │   ├─ _normalize_ies_names       (NOM_FILI ← name_ies_map)
 │   ├─ _verify_offers_to_campus_not_match  (lookup_group | lookup_3719)
 │   └─ _verify_campus_totally_existence    (apenas_no_virtual / criar_no_3719)
 ├─ AdjustmentsOffersPattern.set_values(...)  (xlookup por COD_CURS; metadados)
 └─ MspGenerate.load()
     ├─ _process_discounts         (regressivos por semestre)
     ├─ _compute_derived_values    (offered_price, real_discount, metadata)
     ├─ _fill_in_remaining_values  (xlookup university_id/name; avisos)
     ├─ _generate_virtual_offers   (split do 3719)
     └─ _finalize_dataframe        (rename final → FINAL_COLUMNS)
```

## Pontos de atenção / pendências conhecidas
- **`MspGenerate._verify_regression`**: usava `self.campus_offers.loc[3,'Semestre de Ingresso']` (índice fixo 3). Frágil quando o df tem <4 linhas ou após `reset_index`. Substituir por `.iloc[0]` — alinhado com `_get_enrollment_period` já corrigido.
- **"cannot set a frame with no defined index and a scalar"**: ocorre em `_generate_virtual_offers` / `_split_group_and_virtual` quando o filtro resulta em DataFrame vazio antes de atribuir scalars (`df['col'] = '3719'`). Guardar contra `empty` antes de atribuir, ou usar `df = df.assign(col='3719')` após cópia.
- **Float-to-string em chaves**: pandas carrega códigos numéricos como `float` (ex.: `370.0`). Normalizar com `.astype(str).str.replace(r'\.0$','',regex=True).str.strip()` em ambos os lados do `xlookup` por `COD_CURS`/`Cód. Curso`.
- **Benefícios (OSC)**: hoje `special_condition` é gravado em `Benefício 1 (Chave OSC)` sem split. Se o usuário passa `OSC_A|OSC_B`, **não** é dividido automaticamente em `Benefício 1` / `Benefício 2`. Decidir se implementar o split (`str.split('|')`) ou exigir input em colunas separadas.

## Mapa de IES (Certificadora → university_name)
```
UNICID - GRADUAÇÃO EAD          → UNICID
CRUZEIRO DO SUL - GRADUAÇÃO EAD → UNICSUL - Cruzeiro do Sul
UNIFRAN - GRADUAÇÃO EAD         → UNIFRAN
FSG - GRADUAÇÃO EAD             → FSG
UNIPÊ - GRADUAÇÃO EAD           → UNIPÊ
BRAZ CUBAS - GRAD EAD           → Brazcubas
POSITIVO - GRAD. EAD            → Universidade Positivo
```

## Mapas auxiliares
- `kinds_map`: BACHARELADO/TECNÓLOGO/LICENCIATURA/BACH+LICENC → labels MSP.
- `shift_map`: `100% EAD` → `EaD`; `SEMIPRESENCIAL` → `Semipresencial`; `AO VIVO` → `Ao vivo` (verificar se `Digital` precisa entrar como `EaD`).

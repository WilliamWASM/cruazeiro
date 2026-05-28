Estou refatorando o código de uma IES chamada cruzeiro, a ideia da refatoração está contida no arquivo REFACTOR_CONTEXT.md
Já foi feita grande parte das alterações necessárias e está quase funcional. Realizei alguns testes e ainda não está perfeito.
O maior problema dessa refatoração é o tratamento da planilha e a relação de polos e ofertas realizadas.
Preciso que essa relação seja precisa e que separe as ofertas em ofertas do grupo e ofertas 3719.
Além disso preciso garantir que as saídas finais estejam no formato esperado pela MSP, com as colunas corretas e as informações precisas, incluindo o cálculo dos descontos regressivos com base no semestre de ingresso.
A seguir, vou detalhar a relação de polos e ofertas, o que são ofertas do grupo

Qual é a relação de polos e ofertas e como funciona? :
    - Existe uma planilha que a IES envia para nós que contém as seguintes colunas :
ID_POLO : ID do polo no lado da IES. Ele é dado no nosso sistema como metadata_code
-CURSO_369 : Existem inúmeras colunas con o prefixo "CURSO_" e o número 369 é apenas um exemplo. Essas colunas indicam se o polo tem ou não o curso correspondente. O número após "CURSO_" é o ID do curso no sistema da IES.
- Todas as outras colunas no sistema vão ser inutilizadas e podem ser ignoradas.

O que são ofertas do grupo e 3719 :
- Existe uma planilha chamada exp de campus onde temos os campus existentes no nosso banco de dados cada campus tem um campo chamado "university_id". Se o valor desse campo for 3719, então o campus é considerado um campus 3719. As ofertas 3719 são aquelas que pertencem a esse campus virtual específico da IES Cruzeiro_do_Sul.
- Campi do grupo são aquelas que pertencem a um grupo específico, que pode ser identificado pelo campo "university_id" na tabela de exp de campus. Se o valor desse campo não for 3719, então o campus é considerado um campus do grupo.
Para encontrar as ofertas do 3719 e grupo é necessário cruzar o ID do polo (ID_POLO) com os campus existentes no exp de campus para verificar se o polo pertence ao campus virtual (3719) ou a um campus do grupo (qualquer outro university_id).

Como é entregue as ofertas da IES Cruzeiro_do_Sul :
- As ofertas da IES Cruzeiro_do_Sul são entregues em um formato específico, onde tem a coluna COD_CURS que é o código do curso e é a chave de junção entre a planilha de polos e a planilha de ofertas. A partir dessa chave, é possível identificar quais ofertas pertencem a cada polo e, consequentemente, separar as ofertas do grupo e 3719 com base na relação de polos e campus.
- Além disso, essa planilha de ofertas contém outras colunas importantes, como o nome do curso, grau, modalidade, duração, preço, descontos e certificadora. Essas informações são essenciais para a geração das saídas finais e para garantir que as ofertas estejam corretas e precisas.

Regras de negócio para a geração das saídas finais :
- O desconto é regressivo e regresa sempre no semestre de janeiro (semestre .1). Se o semestre de ingresso for 2026.1, o desconto do 1º semestre se aplica apenas no 1º semestre pago. O desconto menor ("demais semestres") começa no 3º semestre (pois o 2º semestre ainda é julho/.2, e a regressão só acontece em janeiro). Se o semestre de ingresso for 2026.2, o desconto menor começa já no 2º semestre (que é janeiro/.1 seguinte). Na planilha MSP, isso se traduz nos campos:
- Porcentagem de desconto da bolsa (Fixo/1 º Semestre) → desconto do 1º semestre (ex: 0.20)
- Porcentagem total de desconto da bolsa (2º Semestre) → pode manter igual ou já regredir, dependendo do semestre de ingresso
- Porcentagem total de desconto da bolsa (3º Semestre) → desconto fixo regressivo (ex: 0.10)
A lógica deve calcular automaticamente em qual semestre (2º ou 3º) o desconto regride, com base no semestre de ingresso informado.

Do lado da IES, as colunas importantes para a geração das saídas finais e para garantir que as ofertas estejam corretas e precisas são:
- COD_CURS: código do curso, chave de junção entre a planilha de polos e a planilha de ofertas.
- Curso: nome do curso, importante para identificar o curso oferecido.
- GRAU: grau do curso, importante para classificar o curso.
- Modalidade: modalidade do curso (presencial, EAD, etc.), importante para identificar
a modalidade de ensino.
- Duração: duração do curso, importante para informar os alunos sobre o tempo necessário para concluir o curso.
- Preço SIAA: preço do curso, importante para informar os alunos sobre o custo do curso.
- Porcentagem com Desconto 1° ano: porcentagem de desconto para o primeiro
ano, importante para informar os alunos sobre os descontos disponíveis.
- Desconto Garantido Demais Semestres: desconto garantido para os demais semestres, importante para informar os alunos sobre os descontos disponíveis ao longo do curso.
- Certificadora: nome da instituição certificadora, importante para identificar a instituição responsável pela certificação do curso.
- Código SIAA: código do curso no sistema SIAA, importante para identificar o curso no sistema SIAA e garantir a precisão das informações.

As saídas devem vir no formato da MSP, ou seja, com as colunas finais esperadas. que são :
- commercial_discount : desconto comercial aplicado ao curso, importante para informar os alunos sobre os descontos disponíveis. Ele é calculado como o discount_percentage do 1º ano menos 5% (desconto comercial = desconto do 1º ano - 5%).
- offered_price : preço oferecido do curso, importante para informar os alunos sobre o custo do curso após descontos. Ele é calculado como o preço do curso multiplicado por (1 - desconto do 1º ano).
- discount_percentage : porcentagem de desconto aplicada ao curso, importante para informar os alunos sobre os descontos disponíveis. Ele é calculado com base no semestre de ingresso e nas regras de desconto regressivo.
- university_id : ID da universidade no banco, importante para identificar a universidade responsável pelo curso. Ele é obtido a partir do id do campus (metadata_code) cruzado com a tabela de exp de campus, retornando o id da universidade.
- university_name : nome da universidade, importante para identificar a universidade responsável pelo curso. Ele é obtido a partir do id da universidade cruzado com a tabela de exp de campus, retornando o nome da universidade.
- name_from_university : nome do curso fornecido pela universidade, importante para garantir a precisão das informações. Ele é obtido a partir do nome do curso na planilha de ofertas, garantindo que o nome do curso seja consistente com o fornecido pela universidade.
- Avisos : campo de avisos, importante para informar os alunos sobre informações adicionais ou condições especiais relacionadas ao curso. Ele pode conter mensagens como "Certificado pela <IES>" para ofertas 3719, ou outros avisos relevantes para os alunos.
- semestre_ingresso : semestre de ingresso do aluno, importante para calcular os descontos regressivos e informar os alunos sobre o período de ingresso. Ele é obtido a partir do semestre de ingresso informado como um input para a geração das saídas finais, garantindo que os descontos sejam aplicados corretamente com base no período de ingresso.
- offer_special_condition : condição especial da oferta, importante para informar os alunos sobre condições específicas relacionadas à oferta, como benefícios adicionais, requisitos especiais, ou outras informações relevantes. Ele pode ser preenchido com base em informações adicionais fornecidas pela IES ou por regras de negócio específicas relacionadas às ofertas.
Ele é obtido a partir de um input adicional fornecido pelo usuário, garantindo que as condições especiais sejam consideradas na geração das saídas finais e informadas aos alunos de forma clara e precisa. Caso haja mais de 1 condição especial, elas podem ser concatenadas em uma única string separada por "|", ou preenchidas em colunas adicionais, dependendo da estrutura desejada para a saída final.
- regressive_discount : desconto regressivo aplicado ao curso, importante para informar os alunos sobre os descontos disponíveis ao longo do tempo. Ele é calculado com base no semestre de ingresso e nas regras de desconto regressivo, garantindo que os alunos sejam informados sobre os descontos disponíveis em cada semestre do curso.
Além de outras colunas presentes na msp, presente na MSPGenerate.FINAL_COLUMNS, que são importantes para garantir a precisão das informações e a consistência com o formato esperado pela MSP. Essas colunas podem incluir informações adicionais sobre o curso, a universidade, os descontos, ou outras informações relevantes para os alunos. É importante garantir que todas as colunas necessárias estejam presentes e preenchidas corretamente para garantir a qualidade das saídas finais geradas.


O que é necessário fazer para separar as ofertas do grupo e 3719 :
- Primeiro, é necessário fazer um unpivot na planilha de polos para transformar as colunas "CURSO_XXX" em linhas, onde cada linha representa um par polo+curso. Isso permitirá identificar quais cursos cada polo oferece.
- Em seguida, é necessário cruzar o ID do polo (ID_POLO) com os campus existentes no exp de campus para verificar se o polo pertence ao campus virtual (3719) ou a um campus do grupo (qualquer outro university_id). Isso pode ser feito usando uma junção (join) entre a tabela de polos e a tabela de campus. Ou um xlookup por ID_POLO com o metadata_code na tabela de campus.
- É necessário cruzar as informações das ofertas com a tabela de polos para identificar quais ofertas pertencem a cada polo, usando o campo COD_CURS como chave de junção entre a planilha de ofertas e a planilha de polos. Isso permitirá identificar quais ofertas pertencem a cada polo e, consequentemente, separar as ofertas do grupo e 3719 com base na relação de polos e campus.
- Depois de identificar a qual grupo cada polo pertence, é necessário separar as ofertas em duas categorias: ofertas do grupo e ofertas 3719. As ofertas do grupo são aquelas que pertencem a campi do grupo, enquanto as ofertas 3719 são aquelas que pertencem ao campus virtual específico da IES Cruzeiro_do_Sul.
- Por fim, é necessário gerar as saídas finais para cada categoria de ofertas, garantindo que as colunas estejam corretas e que as informações estejam precisas. As ofertas do grupo devem ser geradas em uma aba chamada "Ofertas Grupo", enquanto as ofertas 3719 devem ser geradas em uma aba chamada "Ofertas 3719".

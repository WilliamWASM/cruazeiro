Algumas regras de negócio :

commercial_discount = discount_percentage - 0.05
discount_percentage = desconto da bolsa 1º semestre
regressive_commercial_discount = desconto da bolsa 1º semestre - ultimo desconto da bolsa (ultima regressão)
real_discount =  ultimo desconto da bolsa (ultima regressão)
regressive_discount = desconto da bolsa 1º semestre - desconto da bolsa 2º semestre - desconto da bolsa 3º semestre
university_regressive_discount = "desconto da bolsa 1º semestre - 5" "desconto da bolsa 2º semestre - 5" "desconto da bolsa 3º semestre - 5"
desconto balcao_final = real_discount - 0.05 

Preenchimento da planilha :
não é necessário preencher o offered_price
os descontos devem ser preenchidos com os valores calculados de acordo com as regras de negócio acima
os campos de desconto devem ser preenchidos com os valores calculados, e não com as fórmulas, para garantir a precisão dos dados
os campos de descontos devem ser inteiros, portanto multiplicar por 100 para converter os valores decimais em inteiros antes de preencher a planilha por exemplo, se o desconto for 0.15, deve ser preenchido como 15 na planilha

Tratamento da planilha : 
Preciso que as ofertas com desconto balcao_final que esteja negativo sejam separadas em uma nova planilha chamada "Ofertas com Desconto Negativo". Essa nova planilha deve conter todas as colunas da planilha original, mas apenas as linhas onde o desconto balcao_final seja negativo.
Além disso, as ofertas com desconto balcao_final negativo devem ser removidas da planilha original para garantir que apenas as ofertas com descontos válidos permaneçam nela.

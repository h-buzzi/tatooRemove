### Produzido por Henrique Eissmann Buzzi ###

# Software para atenuação/remoção de tatuagem.

## Modo de usar:

Antes de executar, defina seu Limiar (define qual o threshold para o pixel preto), quanto menor o valor, pega apenas os pixels mais pretos. Defina em um valor de 0 a 255
Automaticamente o Limiar está em 150 (o melhor encontrado pelo projetista para a imagem de exemplo)
Pode-se alterar o sigma também, mas quanto maior o sigma, maior o esforço computacional, e nem sempre terá melhores resultados.

Ao abrir a imagem pela primeira vez, tem-se as seguintes opções:

* Pressionar Tecla C: Entra no modo de captura, se você apertar com o botão esquerdo do mouse, define o ponto superior esquerdo do retângulo da zona de interesse.
Mantenha pressionado, até arrastar para o cantor inferior direito do retângulo, delimitando a região de trabalho.
* 2 opções são possíveis depois de delimitar a região de trabalho: A tecla Enter confirma que a região de trabalho está correta e continua o código, já a tecla
Espaço faz com que a etapa de captura seja descartada, significando que ocorreu um erro na delimitação, e permite a recaptura.

* Pressionar Tecla Esc: Cancela o código e termina a execução, sinalizando que você não quer rodar o código.

Após isso o código é executado. Caso queira fechar a janela e pular para próxima etapa, pode-se pressionar qualquer tecla

Para melhor entendimento, recomenda-se ler os comentários do código

## Conceitos aplicados

Filtragem 2D, convolução de filtro linear, design de arquitetura de filtros, detecção de threshold, aplicação em região de interesse,
captação de região de trabalho, aplicação de máscara.

## Possíveis implementações futuras

* Poder selecionar qual espaço de cor aplicar o Limiar (tal como HSV/HSL, CMYK, L*a*b, que talvez melhorem a identificação do pixel escuro, mas testes preliminares
indicam que o espaço BGR possuiu melhores resultados).

* Implementação automática de número de iterações, ao invés de apenas repetir manualmente (mas creio que, ao invés de inserir na função convolve_interest_region, apenas criar
uma função nova, como "loop_filtering" seja melhor, uma vez que o usuário precisa experimentar antes, para saber a diferença entre a qualidade das iterações)

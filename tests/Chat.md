oi chat, sabendo q vc eh um especialista em pesquisa academica, python, estatistica e afins, tome aq:

### Ajustes e melhorias:

##### O objetivo do meu projeto

Fazer uma analise do perfil dos alunos do curso de Sistemas de Informacao, tentando comparar o desempenho academico dos alunos cotistas e nao cotistas, 
e tentando encontrar padroes que identifiquem a diferencas entre os alunos que evadiram e os que nao evadiram, a distancia entre a residencia do aluno 
e a universidade(Que se encontra na Urca), o CRA dos alunos, a idade dos alunos, o sexo dos alunos, a forma de ingresso dos alunos, etc.

Pensei em usar este projeto para provar que o desempenho academicos dos alunos cotistas nao e pior que o desempenho academico dos alunos nao cotistas, 
mas ver o quanto as outras variaveis afetam o desempenho academico dos alunos, principalmente a distancia entre a residencia do aluno e a universidade.
Basicamente essa eh minha hipotese.

Baseado na estrutura dos dados disponibilizados pela minha orientadora, todos seguindo a rigor a LGPD,criei um script de criptografia e um script de join, 
que foi executado pelos meus professores e me retornou a planilha de dados criptografada,que tem os dados que vamos trabalhar em cima.
A partir dessa planilha, eu comecei a fazer a limpeza dos dados e ver algumas informacoes sobre.

##### Informacoes Adicionais

"Foi no decreto 7824, de 11 de outubro de 2012 que a Lei 12.711, conhecida como Lei de Cotas, entrou em vigor. Essa lei obrigou todos as instituições de ensino superior público deveriam reservar uma porcentagem das suas vagas para alunos oriundos de escola publica, de baixa renda, pretos, pardos e indígenas."

Tipos de Cotas (Forma_Ingresso), segundo os dados disponiveis.

```text
SISU Escola Publica - Independente de Renda
SISU Escola Publica - até 1,5 Salario Minimo
SISU Escola Publica - até 1,5 Salario Minimo : Preto, Pardo, Indígena
SISU Escola Publica - Independente de Renda : Preto, Pardo, Indígena
Ao analisar os dados da planilha, foram identificados esses tipos:

SISU Escola Publica - Independente de Renda
SISU Escola Publica - até 1,5 Salario Minimo
SISU Escola Publica - até 1,5 Salario Minimo : Preto, Pardo, Indígena
SISU Escola Publica - Independente de Renda : Preto, Pardo, Indígena
SISU Escola Pública - até 1,5 Salario Minimo : Preto e Pardo
SISU Escola Pública - até 1,5 Salario Minimo : Índio
SISU Escola Pública - Independente de Renda : Preto e Pardo
SISU Escola Pública - Independente de Renda : Índio

OBS: Há uma quebra das categorias "até 1,5 SM: Preto, Pardo e Indígena" e "Independente da Renda: Preto, Pardo e Indígena" em "Pretos e Pardos" e "Indígenas", acredito que isso se deva ao fato de ter vagas separadas para autodeclaração de "Indígena" e "Pretos e Pardos", por fazerem partes de minorias sociais diferentes.
```

Tipos de Ingresso segundo a planilha:

```text
    'AE - Aluno Especial - Disciplina Isolada = Outros
    'AE - Mobilidade Acadêmica IAE/IESCE = Outros
    'AE - Mobilidade Adadêmica Externa - ANDIFES = Outros
    'DJ - Decisão Judicial = Outros
    'EN - ENEM' = Ampla Concorrência
    'EO - Transferência Ex-Ofício' = Outros
    'PD - Portador de Diploma de Nível Superior' = Outros
    'Pessoas com Deficiência' = Outros
    'PG - Programa de Estudantes - Convênio (PEC-G)' = Outros
    'SISU Ampla Concorrência' = Ampla Concorrência
    'SISU Escola Pública - Indep. de Renda' = Cotas
    'SISU Escola Pública até 1,5 S.M Índio' = Cotas
    'SISU Escola Pública até 1,5 S.M Preto e Pardo' = Cotas
    'SISU Escola Pública até 1,5 S.M.' = Cotas
    'SISU Escola Pública até 1,5 S.M. Preto, Pardo, Indígena' = Cotas
    'SISU Escola Pública, Indep. de Renda: Preto, Pardo, Indígena' = Cotas
    'SISU Escola Pública, Indep. de Renda: Índio' = Cotas
    'SISU Escola Pública, Indep. de Renda: Preto e Pardo' = Cotas
    'TE - Transferência Externa - oriunda de outra instituição' = Outros
    'TC - Transferência Interna-Curso não relacionado ao anterior' = Outros
    'VE - Vestibular' = Ampla Concorrência
 ```

Ja o campo tipo de evasao, foi separado em 3 tipos:

```text
- Evasao
- Concluido
- Cursando
```

#### A estrutura dos meus dados

Meus dados vêm da planilha chamada <span style="color:#F3E6C9 ;">_planilhaCriptografada.xlsx_</span> que contém os dados dos alunos.
A planilha tem 17 colunas e 1286 linhas.
A coluna FORMA_INGRESSO tem 17 valores diferentes, mas representam os alunos cotistas e nao cotistas.
Os alundos do tipo TE E TC vao ser considerados especiais e nao devem entrar na contagem final.

###### A planilha contém os seguintes campos:
- ID_PESSOA = _(Critografado)_ Define o ID do aluno
- NOME_PESSOA = _(Critografado)_ Define o nome do aluno
- SEXO = _(Boolean)_ Define o sexo do aluno, e pode ter os seguintes valores:
  - <span style="color:#F3E6C9 ;">'F'</span>
  - <span style="color:#F3E6C9 ;">'M'</span>
- DT_NASCIMENTO = _(String)_ Define a data de nascimento do aluno, e pode ter os seguintes valores:
  - <span style="color:#F3E6C9 ;">'22/09/1982'</span>
- FORMA_INGRESSO = _(String)_ Define como o aluno ingressou na universidade, e pode ter os seguintes valores:
  - <span style="color:#F3E6C9 ;">'AE - Aluno Especial - Disciplina Isolada'</span>
  - <span style="color:#F3E6C9 ;">'AE - Mobilidade Acadêmica IAE/IESCE'</span>
  - <span style="color:#F3E6C9 ;">'AE - Mobilidade Adadêmica Externa - ANDIFES'</span>
  - <span style="color:#F3E6C9 ;">'DJ - Decisão Judicial'</span>
  - <span style="color:#F3E6C9 ;">'EN - ENEM'</span>
  - <span style="color:#F3E6C9 ;">'EO - Transferência Ex-Ofício'</span>
  - <span style="color:#F3E6C9 ;">'PD - Portador de Diploma de Nível Superior'</span>
  - <span style="color:#F3E6C9 ;">'Pessoas com Deficiência'</span>
  - <span style="color:#F3E6C9 ;">'PG - Programa de Estudantes - Convênio (PEC-G)'</span>
  - <span style="color:#F3E6C9 ;">'SISU Ampla Concorrência'</span>
  - <span style="color:#F3E6C9 ;">'SISU Escola Pública - Indep. de Renda'</span>
  - <span style="color:#F3E6C9 ;">'SISU Escola Pública até 1,5 S.M Índio'</span>
  - <span style="color:#F3E6C9 ;">'SISU Escola Pública até 1,5 S.M Preto e Pardo'</span>
  - <span style="color:#F3E6C9 ;">'SISU Escola Pública até 1,5 S.M.'</span>
  - <span style="color:#F3E6C9 ;">'SISU Escola Pública até 1,5 S.M. Preto, Pardo, Indígena'</span>
  - <span style="color:#F3E6C9 ;">'SISU Escola Pública, Indep. de Renda: Preto, Pardo, Indígena'</span>
  - <span style="color:#F3E6C9 ;">'SISU Escola Pública, Indep. de Renda: Índio'</span>
  - <span style="color:#F3E6C9 ;">'SISU Escola Pública, Indep. de Renda: Preto e Pardo'</span>
  - <span style="color:#F3E6C9 ;">'TE - Transferência Externa - oriunda de outra instituição'</span>
  - <span style="color:#F3E6C9 ;">'TC - Transferência Interna-Curso não relacionado ao anterior'</span>
  - <span style="color:#F3E6C9 ;">'VE - Vestibular'</span>
- FORMA_EVASAO = Define se o aluno evadiu ou nao(e como evadiu), e pode ter os seguintes valores:
  - <span style="color:#F3E6C9 ;">'ABA - Abandono do curso'</span>
  - <span style="color:#F3E6C9 ;">'APO - Aluno Especial - Disciplina Isolada'</span>
  - <span style="color:#F3E6C9 ;">'APO -Conclusão a Mobilidade Acadêmica Externa - ANDIFES'</span>
  - <span style="color:#F3E6C9 ;">'APO -Conclusão da Mobilidade Acadêmica Externa - IAE/IESCE'</span>
  - <span style="color:#F3E6C9 ;">'CON - Curso concluído'</span>
  - <span style="color:#F3E6C9 ;">'CAN - Cancelamento Geral do curso'</span>
  - <span style="color:#F3E6C9 ;">'Desistência SiSU'</span>
  - <span style="color:#F3E6C9 ;">'JUB - Jubilamento'</span>
  - <span style="color:#F3E6C9 ;">'Não identificada (vide pasta do aluno)'</span>
  - <span style="color:#F3E6C9 ;">'Sem evasão'</span>
  - <span style="color:#F3E6C9 ;">'FAL - Falecimento do discente'</span>
  - <span style="color:#F3E6C9 ;">'TIC - Transferência Interna'</span>
- COD_CURSO = _(String)_ Define o codigo do curso do aluno.
<br>
**obs:** Como nosso escopo e o curso de Sistemas de Informacao, todos os alunos tem o mesmo codigo de curso, que e <span style="color:#F3E6C9 ;">210</span>
- NOME_UNIDADE = _(String)_ Define o nome da unidade do aluno.
<br>
**obs:** Como nosso escopo e o curso de Sistemas de Informacao da UNIRIO, o valor e igual parada todos os alunos, que e <span style="color:#F3E6C9 ;">'Sistemas de Informação - Bacharelado - Turno Integral (V/N)'</span>
- MATR_ALUNO = _(Critografado)_ Define o numero de matricula do aluno.
- NUM_VERSAO = _(Inteiro)_ Ano e periodo que o dado foi registrado. Tem dois tipos de valores, ano e periodo (separado por /)
    - <span style="color:#F3E6C9 ;">2000/2</span>
    - <span style="color:#F3E6C9 ;">2008/1</span>
- PERIODO_INGRESSO = _(String)_ Define o periodo de ingresso do aluno, com o seguinte formato: 
    - <span style="color:#F3E6C9 ;">2002/2°. semestre</span>
- DT_EVASAO = _(String)_ Define a data exata de evasao do aluno. (Pode ser vazio) Tem sempre o seguinte formato:
    - <span style="color:#F3E6C9 ;">14/09/2009</span>
- PERIODO_EVASAO = _(String)_ Define o periodo de evasao do aluno. (Pode ser vazio) Tem sempre o seguinte formato:
    - <span style="color:#F3E6C9 ;">2009/2°. semestre</span>
- CPF_MASCARA = _(Critografado)_ Define o CPF do aluno.
- CRA = _(Float)_ Define o CRA do aluno.
- BAIRRO = _(String)_ Define o bairro do aluno. (Pode ser vazio)
- CIDADE = _(String)_ Define a cidade do aluno. (Pode ser vazio)
- ESTADO = _(String)_ Define o estado do aluno. (Pode ser vazio)

Baseado em varias das formatacoes que eu fiz, a tabela se encontra assim hoje em dia:

```text
SEXO - M
DT_NASCIMENTO - 1982-02-09
FORMA_INGRESSO - VE - Vestibular
FORMA_EVASAO - CON - Curso concluído
NUM_VERSAO - 2005/2
PERIODO_INGRESSO - 2.0
DT_EVASAO - 2009-09-14
PERIODO_EVASAO - 1.0
CRA - "6,4654"
BAIRRO - Barra da Tijuca
CIDADE - RIO DE JANEIRO
ESTADO - Rio de Janeiro
PER_PERIODO_EVASAO_FORMAT - 2009.2 
ANO_PERIODO_EVASAO - 2009.0
PER_PERIODO_INGRESSO_FORMAT - 2002.1
ANO_PERIODO_INGRESSO - 2002.0
```

Como pode ver, exclui varias colunas que me preciam inuteis e formatei outras para que os dados ficassem mais acessiveis.
O valor seguido ao lado do campo e um valor real da tabela.

##### O que eu quero fazer:

Agora que terminei a limpeza dos dados, quero partir para analise real deles.
Eu pensei em algumas possibilidades, mas quero uma olhada de alguem de fora, alguem experiente como voce, para analisar estatiticamente meus dados e minha hipotes.

###### Ideia 1:

- Olhar os dados em 3 cargas, Antes das Cotas/Depois das Cotas/Pandemia

- Repetir Análise para cada um dos grupos


- É possível verificar se o rendimento médio dos alunos cotistas é abaixo dos alunos não-cotistas?
// Fazer análise de dados comparando o CR médio de todos os cotistas e não cotistas
// Fazer análise do CR médio por ano e por períod
/

É possível verificar se os alunos não-cotistas evadem mais que os alunos cotistas? 
//Fazer análise da evasão por cotista e não cotista
//Fazer a evasão por por ano e periodo

É possível dizer se entre os alunos que evadiram, qual a relacao da evasão com o CR baixo(dificuldade de acomoanhar a dificuldade do curso)
//Fazer media do CR entre cotistas e nao cotistas que evadiram


- Os alunos cotistas moram mais longe da faculdade?
// Fazer analise visual do mapa de calor dos cotistas e nao cotistas
//Tentar ver a distancia média de cada bairro para UNIRIO
// Relacao de alunos × zona do rj q mora

Existe relacao entre evasão dos alunos e distância?

// Fazer analise com c e nc olhando evasao e zona que mora

##### Ideia 2

- Implementar a Analise baseada nesse passo-a-passo:
    - Agrupar os dados em 4 grupos diferentes:
      - Antes das Cotas
      - Depois das Cotas
      - Período Pandemico
      - Todos (3 grupos juntos)
    - Agrupar os dados em 2 sub-grupos diferentes:
        - Cotistas
        - Não-Cotistas
    - Repetir as seguintes análises:
        - Fazer comparacao do CRA  
        - Fazer comparacao do CRA Médio por período 
        - Fazer comparacao do CRA Médio por ano 
        - Fazer comparacao da evasao entre C e NC
        - Fazer comparacao da evasao entee C e NC por período(ou/e ano)
        - Fazer comparacao entre CR médio dos C e NC que evadiram e concluiram
        - Fazer análise visual do mapa de calor dos C e NC
        - Fazer distancia média do centro de cada bairro até a UNIRIO
        - Fazer comparacao entre C e NC olhando evasão e zona que mora do RJ
      

As duas ideias foram criadas por mim e m momentos diferentes.
Creio que nos podemos unir as 2.

Voce tem tudo que precisa para entender? Caso falte algo, me diga que fornecerei.

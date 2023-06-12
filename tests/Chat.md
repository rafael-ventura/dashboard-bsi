### Ajustes e melhorias:

##### O objetivo do meu projeto

Fazer uma analise do perfil dos alunos do curso de Sistemas de Informacao, tentando comparar o desempenho academico dos alunos cotistas e nao cotistas, 
e tentando encontrar padroes que identifiquem a diferencas entre os alunos que evadiram e os que nao evadiram, a distancia entre a residencia do aluno 
e a universidade(Que se encontra na Urca), o CRA dos alunos, a idade dos alunos, o sexo dos alunos, a forma de ingresso dos alunos, etc.

Pensei em usar este projeto para provar que o desempenho academicos dos alunos cotistas nao e pior que o desempenho academico dos alunos nao cotistas, 
mas ver o quanto as outras variaveis afetam o desempenho academico dos alunos, principalmente a distancia entre a residencia do aluno e a universidade.


##### O que eu ja fiz

Baseado na estrutura dos dados extraidos pelos meus professores,
criei um script de criptografia e um script de join, que foi executado pelos meus professores e me retornou a planilha de dados criptografada,
que esta na pasta "join".
A partir dessa planilha, eu comecei a fazer a limpeza dos dados e ver algumas informacoes sobre.

- Aqui esta um pouco do que eu fiz no juptyer notebook para separar os tipos de forma de evasao em 3 tipos ( Evasao, Concluido e Cursando). 
A tabelaPrinc eh o arquivo 'planilhaCriptografada.xlsx' em forma de dataframe:

<br>

O campo FORMA_INGRESSO Tambem deve ser reduzido em 3 campos: 
Um para os alunos que ingressaram por cotas, um para os alunos que ingressaram por ampla concorrencia e outro para os outrostipos de ingresso, 
entao eu fiz a seguinte analise manualmente:

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
 
#### A estrutura dos meus dados

Meus dados vêm da planilha chamada <span style="color:#F3E6C9 ;">_planilhaCriptografada.xlsx_</span> que contém os dados dos alunos.
A planilha tem 17 colunas e 1286 linhas.
A coluna FORMA_INGRESSO tem 17 valores diferentes, mas representam os alunos cotistas e nao cotistas.


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
- NUM_VERSAO = _(Inteiro)_ Incerto se e o numero de versao da matricula do aluno. Tem dois valores que parecem ser referentes a data:
    - <span style="color:#F3E6C9 ;">2000/2</span>
    - <span style="color:#F3E6C9 ;">2008/1</span>
- PERIODO_INGRESSO = _(String)_ Define o periodo de ingresso do aluno, podendo ter o seguinte formato: 
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

##### O que eu quero fazer:

- Implementar em Python (Pandas) uma analise dos dados para analisar meu ponto principal (desempenho dos alunos cotistas e nao cotistas).
- Implementar a Analise baseada nesse passo-a-passo:
    - Agrupar os dados em 4 grupos diferentes:
    - Antes das Cotas
    - Depois das Cotas
    - Período Pandemico
    - Todos (3 grupos juntos)
    - Agrupar os dados em 2 grupos diferentes:
        - Cotistas
        - Não-Cotistas
        - Repetir as seguintes análises:
            - Fazer comparacao do CR Médio 
            - Fazer comparacao do CR Médio por período 
            - Fazer comparacao do CR Médio por ano
            - Fazer comparacao da evasao entre C e NC
            - Fazer comparacao da evasao entee C e NC por período(ou/e ano)
            - Fazer comparacao entre CR médio dos C e NC que evadiram e concluiram
            - Fazer análise visual do mapa de calor dos C e NC
            - Fazer distancia média do centro de cada bairro até a UNIRIO
            - Fazer comparacao entre C e NC olhando evasão e zona que mora do RJ


<br>
Futuro:
- Comprovar ou nao a hipotese de que os alunos cotistas tem um desempenho inferior aos nao cotistas.
- Implementar um dashboard (Dash + Potly) para visualizar os dados de forma mais intuitiva.
- Criar um botao no dashboard para inserir planilhas no mesmo formato da planilha original e fazer a analise automaticamente(usar como default a planilha original).

Estrutura de Pastas do Projeto:
```
dashboard/
  .vscode/ 
  analise/  
    notebook/
        - analiseJupiter.ipynb
        - FormataçaoDados.ipynb 
  dados/
    bruto/
      - planilhaJoinCriptografada.xlsx
    processado/
      - dfPrincipal.csv
  scripts/
    - cripto.py
    - join.py
  src/
    - app.py (Dash)
  venv/
  Procfile
  README.md
  requirements.txt
  runtime.txt
```




!!!MANDAR A PARTIR DAQUI!!!!


ok, sobre o ponto 3 eu tenho 2 colunas que podem corresponder, sao:
PERIODO_INGRESSO= tem o periodo/semestre e ano que o aluno ingressou em formato de float (deveria ter uma conversao para date.year no arquivo de formatacao, mas vc esqeuceu)
CRA = um valor float de 0 a 10

a terceira coluna a gente tinha criado o codigo mas perdeu-se no meio da conversa.
vamos la:
- implemente no arquivo formatacao_dados uma conversão do campo ANO_PERIODO_INGRESSO de float para date.year
- coloque o trecho abaixo no fluxo do algoritmo de maneira correta
- revise o arquivo analise_jupiter apos essas configuracoes e ajuste o necessario

trecho de codigo:

# Mapeamento de categorias
forma_ingresso_mapping = {
    'AE - Aluno Especial - Disciplina Isolada': 'Outros',
    'AE - Mobilidade Acadêmica IAE/IESCE': 'Outros',
    'AE - Mobilidade Adadêmica Externa - ANDIFES': 'Outros',
    'DJ - Decisão Judicial': 'Outros',
    'EN - ENEM': 'Ampla Concorrência',
    'EO - Transferência Ex-Ofício': 'Outros',
    'PD - Portador de Diploma de Nível Superior': 'Outros',
    'Pessoas com Deficiência': 'Outros',
    'PG - Programa de Estudantes - Convênio (PEC-G)': 'Outros',
    'SISU Ampla Concorrência': 'Ampla Concorrência',
    'SISU EscolaPública - Indep. de Renda': 'Cotas',
    'SISU Escola Pública até 1,5 S.M Índio': 'Cotas',
    'SISU Escola Pública até 1,5 S.M Preto e Pardo': 'Cotas',
    'SISU Escola Pública até 1,5 S.M.': 'Cotas',
    'SISU Escola Pública até 1,5 S.M. Preto, Pardo, Indígena': 'Cotas',
    'SISU Escola Pública, Indep. de Renda: Preto, Pardo, Indígena': 'Cotas',
    'SISU Escola Pública, Indep. de Renda: Índio': 'Cotas',
    'SISU Escola Pública, Indep. de Renda: Preto e Pardo': 'Cotas',
    'TE - Transferência Externa - oriunda de outra instituição': 'Outros',
    'TC - Transferência Interna-Curso não relacionado ao anterior': 'Outros',
    'VE - Vestibular': 'Ampla Concorrência'
}

# Substituir as categorias
df['FORMA_INGRESSO'] = df['FORMA_INGRESSO'].replace(forma_ingresso_mapping)
# dashboard-bsi

Aplicacao feita em Python com o intuito de mostrar os resultados da análise exploratória feita nos dados dos discentes do curso de Sistemas de Informacao da UNIRIO de maneira grafica e visual.

Os dados disponibilizados foram criptografados.

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
* Você instalou a versão mais recente de `<Python / Pip / Pandas / Dash / Jupyter>`.
* Você leu `<Documentacao Pandas / Documentacao Dash>`.

### Instalar depedencias
```bash
pip install pandas
pip install dash 
```
### Executar Jupyter Notebook com a Análise dos Dados

```bash
cd analise/notebook
jupyter notebook analiseFinal.ipynb

```
### Executar aplicacacao

```bash
python app.py
```

### Voce pode acessar a aplicacao funcionando online

<!--- [Heroku App](https://dashboard-bsi.herokuapp.com/) </>  ---> 

### Para voce, chat:
##### O objetivo do meu projeto
Analisar se os alunos cotistas tem realmente um desempenho pior que os alunos de ampla concorrencia. 
##### O que eu ja fiz
Baseado nos dados extraidos pelos meus professores, eles executaram o script de criptografia que esta na pasta "join" e me retornaram a planilha de dados criptografadas. Eu executei um join nas planilhas enderecos_CRA (que contem os CRs dos alunos) com a planilhaCriptografada e criou-se a planilhaJoinCriptografada.
A partir dessa planilha, comecei a extrair alguns dataframes para csv e formatar todos os dados para acertar os campos da maneira que eu queria. A partir disso eu queria analisar os dados. Eu tambem criei uma apliacao/dashboard com os dados, mas esta simples e as metricas nao refletem bem os dados e o objetivo do projeto. 
##### Me ajude
Meu foco eh entender como eu posso melhorar meu dados e a estrutura do meu codigo, para que ele seja reutilizavel. Ate pensei se seria possivel colocar algum botao no dashboard para a pessoa adicionar um arquivo e eu pegar os dados desse arquivo e adicionar nos meu dados.

Eu gostaria de entender melhor como estruturar o codigo do meu projeto, principalmente as paginas. Depois gostaria de revisar os codigos e melhora-los. Terceiro, gostaria que voce analisasse como sao meus dados e me ajudasse a entender como eu posso fazer mais analises e comparacoes entre os grupos.
Tambem gostaria que voce guardasse e absorvesse a informacao.

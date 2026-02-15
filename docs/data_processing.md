# Documentação do Processamento de Dados

Este documento detalha todas as etapas de tratamento, limpeza e preparação dos dados realizadas no notebook `1_data_processing.ipynb` para o desafio de previsão de defasagem escolar.

## 1. Configuração do Logger
- Utilização do `LoggerManager` (customizado) para registrar logs do processamento em arquivo, facilitando rastreabilidade e auditoria.
- Integração com a biblioteca padrão `logging` do Python para registrar eventos importantes ao longo do pipeline.

## 2. Carregamento dos Dados
- Leitura do arquivo `PEDE2024.csv` com pandas.
- Padronização dos nomes das colunas para minúsculo, garantindo consistência.
- Registro do shape do DataFrame e das colunas carregadas.

## 3. Exploração Inicial
- Log das colunas, tipos de dados, valores nulos por coluna e estatísticas descritivas.
- Exemplo de registro de aluno logado para inspeção manual.

## 4. Limpeza de Dados
- Remoção de colunas desnecessárias, como identificadores, datas, nomes, turmas e avaliadores, para evitar vazamento de informação e reduzir dimensionalidade.
- Análise e remoção das colunas de status ("ativo/inativo") caso todos estejam cursando.

## 5. Remoção de Colunas com Muitos Nulos
- Exclusão de colunas com mais de 30% de valores nulos, mantendo apenas variáveis relevantes e bem preenchidas.

## 6. Padronização e Encoding
- Padronização das colunas "fase" e "fase ideal" para valores numéricos, facilitando o uso em modelos.
- Remoção da coluna "escola" para garantir generalização do modelo para novas escolas.
- Encoding manual da coluna "gênero" em variáveis binárias (masculino/feminino).
- Normalização e one-hot/manual encoding da coluna "instituição de ensino", com mapeamento salvo em JSON para reprodutibilidade.

## 7. Remoção de Colunas Derivadas
- Remoção das colunas "pedra 2024" e "inde 2024" por serem derivadas de outros indicadores já presentes no dataset.

## 8. Tratamento de Valores Nulos Restantes
- Preenchimento de valores nulos em colunas numéricas (IAA, IPS, IPP, IDA, MAT, POR, IPV) com a média da respectiva coluna.
- Log detalhado das colunas tratadas e dos valores preenchidos.

## 9. Salvamento dos Dados Processados
- Exportação do DataFrame final para o arquivo `data/processed_data.csv` para uso posterior em modelagem.

---

**Resumo:**
O notebook realiza um pipeline robusto de limpeza, padronização e preparação dos dados, com registro detalhado de logs e decisões. O resultado é um dataset pronto para modelagem preditiva, sem vazamento de informações e com variáveis bem tratadas para uso em algoritmos de machine learning.
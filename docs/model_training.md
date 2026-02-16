# Documentação do Treinamento de Modelos

Este documento detalha o pipeline de modelagem implementado no notebook `2_model_train.ipynb`.

## 1. Preparação e Normalização dos Dados
- Carregamento dos dados processados.
- Separação entre variáveis preditoras (X) e alvo (`defasagem`).
- Normalização dos dados com MinMaxScaler e salvamento do scaler para uso futuro.
- Log de exemplos de alunos com defasagem extrema para validação qualitativa.

## 2. Separação em Treino e Teste
- Divisão dos dados em 80% para treino e 20% para teste, garantindo reprodutibilidade com `random_state`.

## 3. Modelos e Busca de Hiperparâmetros
- Teste de quatro modelos de regressão: Regressão Linear, Árvore de Decisão, Random Forest e HistGradientBoosting.
- Definição de grids de hiperparâmetros para cada modelo.
- Treinamento com GridSearchCV (validação cruzada 5-fold, métrica MAE).
- Seleção automática do melhor modelo pelo maior R² no conjunto de teste.

## 4. Avaliação e Resultados
- Cálculo de métricas: MAE, RMSE, R² e MAE médio da validação cruzada (CV_MAE).
- Ranking dos modelos por desempenho.
- Salvamento do melhor modelo em `ml_models/best_model.pkl`.
- Logs detalhados de todo o processo.

## 5. Rastreamento de Experimentos com MLflow
- Configuração do MLflow para rastreamento local dos experimentos.
- Log de parâmetros, métricas e modelos de cada execução.

## 6. Validação Final
- Validação das predições do melhor modelo para exemplos extremos de defasagem (-2 e 2).
- Garantia de coerência e robustez do pipeline.

---

*Para detalhes do processamento de dados, consulte o arquivo `docs/data_processing.md`.*
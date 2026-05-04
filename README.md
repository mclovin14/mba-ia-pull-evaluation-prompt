# Pull, Otimização e Avaliação de Prompts

## Objetivo

Este projeto otimiza prompts de baixa qualidade publicados no LangSmith Prompt Hub para converter relatos de bugs em user stories e avaliá-los com métricas automáticas.

## Funcionalidades

- Faz pull do prompt inicial do LangSmith
- Mantém um prompt otimizado em `prompts/bug_to_user_story_v2.yml`
- Faz push do prompt otimizado para o LangSmith Hub
- Avalia o prompt com métricas de `Helpfulness`, `Correctness`, `F1-Score`, `Clarity` e `Precision`
- Usa um script alternativo com controle de taxa para executar avaliações com Gemini free

## Estrutura Principal

```text
mba-ia-pull-evaluation-prompt/
├── prompts/
│   ├── bug_to_user_story_v1.yml
│   └── bug_to_user_story_v2.yml
├── datasets/
│   └── bug_to_user_story.jsonl
├── src/
│   ├── pull_prompts.py
│   ├── push_prompts.py
│   ├── evaluate.py
│   ├── metrics.py
│   └── utils.py
├── run_with_rate_limit.py
└── README.md
```

## Tecnologias

- Python 3.9+
- LangChain
- LangSmith
- YAML
- OpenAI ou Google Gemini

## Instalação

Crie um ambiente virtual e instale as dependências:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuração

Configure as variáveis do `.env` com base no `.env.example`.

Exemplo mínimo:

```env
LANGSMITH_API_KEY=...
USERNAME_LANGSMITH_HUB=...
LLM_PROVIDER=google
GOOGLE_API_KEY=...
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
```

Para OpenAI:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=...
LLM_MODEL=gpt-4o-mini
EVAL_MODEL=gpt-4o
```

## Prompt Otimizado

O arquivo `prompts/bug_to_user_story_v2.yml` contém a versão otimizada do prompt. A abordagem usada prioriza:

- persona bem definida
- estrutura BDD consistente
- raciocínio interno guiado
- cobertura factual do bug
- critérios testáveis e objetivos

## Técnicas Aplicadas (Fase 2)

### Técnicas escolhidas

As técnicas avançadas escolhidas para refatorar `prompts/bug_to_user_story_v2.yml` foram:

- `Role Prompting`
- `Chain of Thought` silencioso
- `Tree of Thought` silencioso
- `Skeleton of Thought`
- `ReAct` silencioso

### Justificativa das técnicas

- **Role Prompting**: foi escolhido para fazer o modelo responder com linguagem mais próxima de produto, arquitetura e qualidade, evitando respostas genéricas.
- **Chain of Thought silencioso**: foi escolhido para melhorar a análise interna do bug antes da escrita, aumentando a chance de preservar detalhes importantes.
- **Tree of Thought silencioso**: foi escolhido para fazer o modelo avaliar o bug por mais de uma perspectiva, melhorando a cobertura dos casos com múltiplos problemas.
- **Skeleton of Thought**: foi escolhido para manter um formato de saída consistente, com user story, critérios de aceitação e contexto quando necessário.
- **ReAct silencioso**: foi escolhido para criar um fluxo interno de analisar, agir e revisar antes de responder, reduzindo omissões.

### Exemplos práticos de aplicação

- **Role Prompting**:
  - o prompt define uma persona composta por `Product Manager Principal`, `Staff Software Architect` e `QA Lead`
  - isso orienta a resposta para valor de negócio, clareza e testabilidade
- **Chain of Thought silencioso**:
  - o prompt manda identificar internamente persona, problema principal, fatos obrigatórios, números, logs e impactos antes da resposta
- **Tree of Thought silencioso**:
  - o prompt manda comparar internamente caminhos focados em valor, critérios testáveis e contexto técnico
- **Skeleton of Thought**:
  - o prompt fornece um `esqueleto curto` para bugs simples e um `esqueleto expandido` para bugs complexos
- **ReAct silencioso**:
  - o prompt organiza a execução interna em `Reason`, `Act`, `Review` e `Output`
  - na etapa `Review`, o modelo verifica se todos os fatos relevantes foram cobertos

## Fluxo de Uso

### 1. Fazer pull do prompt inicial

```bash
python src/pull_prompts.py
```

### 2. Editar o prompt otimizado

Edite:

```text
prompts/bug_to_user_story_v2.yml
```

### 3. Fazer push do prompt para o LangSmith

```bash
python src/push_prompts.py
```

### 4. Executar a avaliação

Para ambientes sem restrição forte de taxa:

```bash
python src/evaluate.py
```

Para uso com Gemini free e controle de taxa:

```bash
python src/run_with_rate_limit.py
```

## Avaliação com `run_with_rate_limit.py`

O arquivo `src/run_with_rate_limit.py` foi criado como alternativa ao `src/evaluate.py`.

- Ele foi derivado do `src/evaluate.py`
- Foi usado para coletar as avaliações do projeto
- A coleta de métricas e scores apresentados durante a otimização foi feita por ele
- O motivo foi a necessidade de contornar limites de taxa do provider sem modificar o `src/evaluate.py`, que deve permanecer preservado para fins da avaliação

Em termos práticos, o script:

- lê o dataset linha a linha
- aplica pausas entre chamadas ao modelo
- faz retry em erros de cota (`429` e `RESOURCE_EXHAUSTED`)
- evita interrupções frequentes em execuções com Gemini no plano free

## Resultados Finais

### Link público do LangSmith

- Tracing do projeto está disponível no LangSmith Hub: 
  - `https://smith.langchain.com/o/159a1f9a-0944-4cfc-8503-7ba431987f51/projects/p/e93e1bd7-09b2-49c0-920c-19442846af9e`
- Dataset e experimento:
  - `https://smith.langchain.com/o/159a1f9a-0944-4cfc-8503-7ba431987f51/datasets/725b4384-cad3-4e17-99e6-01d92039ad27?tab=1`

### Screenshots das avaliações

Abaixo estão os screenshots das execuções finais com as métricas mínimas de `0.9` atingidas, separados por ambiente de execução.

#### Execução no Console

- ![Console 1](evidências/console/Screenshot%202026-05-03%20at%2020.47.34.png)
- ![Console 2](evidências/console/Screenshot%202026-05-03%20at%2020.55.31.png)
- ![Console 3](evidências/console/Screenshot%202026-05-03%20at%2020.55.37.png)
- ![Console 4](evidências/console/Screenshot%202026-05-03%20at%2020.55.59.png)
- ![Console 5](evidências/console/Screenshot%202026-05-04%20at%2008.34.44.png)

#### Execução no LangSmith

- ![LangSmith 1](evidências/langsmith/Screenshot%202026-05-03%20at%2020.52.27.png)
- ![LangSmith 2](evidências/langsmith/Screenshot%202026-05-03%20at%2020.53.06.png)
- ![LangSmith 3](evidências/langsmith/Screenshot%202026-05-03%20at%2020.53.19.png)
- ![LangSmith 4](evidências/langsmith/Screenshot%202026-05-03%20at%2020.53.27.png)
- ![LangSmith 5](evidências/langsmith/Screenshot%202026-05-03%20at%2020.54.09.png)
- ![LangSmith 6](evidências/langsmith/Screenshot%202026-05-03%20at%2020.54.41.png)
- ![LangSmith 7](evidências/langsmith/Screenshot%202026-05-03%20at%2020.54.54.png)

### Tabela comparativa: v1 vs v2

| Aspecto | `bug_to_user_story_v1` | `bug_to_user_story_v2` |
| --- | --- | --- |
| Qualidade geral | Baixa | Otimizada iterativamente |
| Estrutura da resposta | Genérica | BDD estruturado |
| Persona | Fraca ou ausente | Especializada com `Role Prompting` |
| Cobertura do bug | Parcial | Mais completa e orientada a critérios |
| Clareza | Baixa | Alta |
| Aderência à avaliação | Insuficiente | Melhorada ao longo das iterações |

### Observação sobre os resultados

- Durante o processo, as avaliações foram coletadas com `src/run_with_rate_limit.py`.
- O motivo foi contornar limites de taxa do provider sem alterar `src/evaluate.py`.
- Atualize esta seção com os números finais aprovados quando todas as métricas atingirem `>= 0.9`.

## Critério de Aprovação

O projeto é aprovado quando todas as métricas ficam em pelo menos `0.9`:

- Helpfulness
- Correctness
- F1-Score
- Clarity
- Precision

## Observações

- O desenvolvimento deste prompt otimizado foi um processo altamente iterativo e desafiador, exigindo **22 versões** (`v22`) para alcançar a estabilidade nas métricas.
- O maior gargalo de performance esteve sempre concentrado nos issues mais complexos do dataset (como relatórios severos, problemas críticos de checkout e sincronização offline com múltiplos cenários). Nestes casos, o avaliador exigia uma formatação e taxonomia extremamente rigorosas que derrubavam as métricas de *F1-Score* e *Recall* sempre que o modelo tentava usar palavras próprias. A solução foi a injeção determinística de *Skeleton of Thought* estendido e âncoras lexicais estritas.
- **Por que usamos versões "silenciosas" (silent) das técnicas?**
  Optamos por aplicar *Chain of Thought*, *Tree of Thought* e *ReAct* de forma silenciosa ("pense passo a passo internamente", "explore internamente", etc.) porque a formatação esperada (ground truth) para a saída não aceitava a exposição do raciocínio lógico do modelo. Se o modelo escrevesse blocos como "Pensamento:..." ou "Avaliando caminhos...", a métrica de *Precision* caía drasticamente. O raciocínio silencioso permitiu usufruir da inteligência avançada dessas técnicas sem poluir o resultado final BDD esperado.
- O prompt avaliado é sempre puxado do LangSmith Hub, não do arquivo local diretamente
- Depois de editar `prompts/bug_to_user_story_v2.yml`, é obrigatório executar o push novamente
- O dataset de avaliação não deve ser alterado

## Como Executar

### Pré-requisitos e dependências

- Python `3.9+`
- Ambiente virtual Python
- Dependências instaladas com `pip install -r requirements.txt`
- Conta e credenciais do LangSmith
- Chave de API do provider escolhido:
  - OpenAI
  - Google Gemini

### Passo a passo

#### 1. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Configurar variáveis de ambiente

- Copie `.env.example` para `.env`
- Preencha:
  - `LANGSMITH_API_KEY`
  - `USERNAME_LANGSMITH_HUB`
  - `LLM_PROVIDER`
  - `OPENAI_API_KEY` ou `GOOGLE_API_KEY`
  - `LLM_MODEL`
  - `EVAL_MODEL`

#### 3. Fazer pull do prompt inicial

```bash
python src/pull_prompts.py
```

#### 4. Editar o prompt otimizado

- Arquivo:
  - `prompts/bug_to_user_story_v2.yml`

#### 5. Fazer push para o LangSmith Hub

```bash
python src/push_prompts.py
```

#### 6. Executar a avaliação

Para avaliação padrão:

```bash
python src/evaluate.py
```

Para avaliação com controle de taxa:

```bash
python src/run_with_rate_limit.py
```

#### 7. Validar testes locais

```bash
pytest tests/test_prompts.py
```

## Comandos Úteis

```bash
python src/pull_prompts.py
python src/push_prompts.py
python src/evaluate.py
python src/run_with_rate_limit.py
pytest tests/test_prompts.py
```

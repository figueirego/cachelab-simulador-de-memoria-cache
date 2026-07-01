# CacheLab - Simulador de Memória Cache

**Data da entrega:** 30 de junho de 2026

Projeto acadêmico em Python 3 para simular políticas de substituição de cache a partir de traces em CSV. O trabalho compara FIFO, LRU e LFU, executa experimentos com diferentes capacidades e gera os resultados em tabela, gráfico e relatório PDF.

## Objetivo

O objetivo do projeto é avaliar como a capacidade do cache influencia a taxa de acertos. Para isso, o simulador lê uma sequência de acessos no formato CSV e contabiliza:

- número total de acessos;
- número de hits;
- número de misses;
- hit ratio em porcentagem.

## Estrutura do projeto

```text
cache_simulator.py
cache/
  policies.py
  simulator.py
scripts/
  generate_trace.py
  run_experiments.py
  generate_report.py
data/
  trace.csv
results/
  experiment_results.csv
  hit_ratio_by_policy.png
docs/
  relatorio-experimental.pdf
tests/
```

## Políticas implementadas

- **FIFO:** remove o item inserido há mais tempo.
- **LRU:** remove o item menos recentemente utilizado.
- **LFU:** remove o item menos frequente. Em caso de empate, remove o item mais antigo entre os empatados.

## Instalação

```bash
python3 -m pip install -r requirements.txt
```

Em ambientes onde `python` aponta para Python 3, os comandos também podem ser executados com `python`.

## Formato do CSV de entrada

O arquivo de entrada precisa ter uma coluna chamada `item_id`.

```csv
item_id
10
15
10
20
```

Cada linha representa uma requisição a um item.

## Gerar o trace principal

```bash
python3 scripts/generate_trace.py --output data/trace.csv --rows 10000
```

O arquivo `data/trace.csv` já está incluído no projeto e possui 10.000 linhas de acesso, conforme solicitado no enunciado.

## Executar o simulador

Exemplo no formato solicitado pelo enunciado:

```bash
python3 cache_simulator.py --input data/trace.csv --policy lru --capacity 100
```

Para executar uma política específica e ver somente o resultado dela, troque o valor de `--policy`:

```bash
python3 cache_simulator.py --input data/trace.csv --policy fifo --capacity 100
python3 cache_simulator.py --input data/trace.csv --policy lru --capacity 100
python3 cache_simulator.py --input data/trace.csv --policy lfu --capacity 100
```

Políticas aceitas:

- `fifo`
- `lru`
- `lfu`

Exemplo de saída:

```text
Policy: lru
Capacity: 100
Total accesses: 10000
Hits: 4659
Misses: 5341
Hit ratio: 46.59%
```

## Executar os experimentos principais

```bash
python3 scripts/run_experiments.py --input data/trace.csv
```

Por padrão, o script executa as três políticas nas capacidades 100, 500 e 1000. Os resultados principais ficam em:

- `results/experiment_results.csv`
- `results/hit_ratio_by_policy.png`

## Gerar o relatório PDF

```bash
python3 scripts/generate_report.py
```

O relatório experimental fica em:

```text
docs/relatorio-experimental.pdf
```

## Rodar os testes

```bash
python3 -m pytest -v
```

## Resultado observado

No trace sintético principal, a política LFU apresentou a melhor média de hit ratio. O aumento da capacidade elevou a taxa de acertos para todas as políticas, mostrando a relação direta entre tamanho do cache e desempenho.

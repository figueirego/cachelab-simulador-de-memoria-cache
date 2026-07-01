from __future__ import annotations

import argparse
import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def load_results(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def best_policy(rows: list[dict[str, str]]) -> str:
    averages: dict[str, list[float]] = {}
    for row in rows:
        averages.setdefault(row["policy"], []).append(float(row["hit_ratio"]))
    policy, values = max(averages.items(), key=lambda item: sum(item[1]) / len(item[1]))
    average = sum(values) / len(values)
    return f"{policy.upper()} apresentou a melhor média de hit ratio ({average:.2f}%)."


def capacity_summary(rows: list[dict[str, str]]) -> str:
    capacities = sorted({int(row["capacity"]) for row in rows})
    first_capacity = capacities[0]
    last_capacity = capacities[-1]
    first_average = sum(
        float(row["hit_ratio"]) for row in rows if int(row["capacity"]) == first_capacity
    ) / len([row for row in rows if int(row["capacity"]) == first_capacity])
    last_average = sum(
        float(row["hit_ratio"]) for row in rows if int(row["capacity"]) == last_capacity
    ) / len([row for row in rows if int(row["capacity"]) == last_capacity])
    return (
        f"A média de hit ratio aumentou de {first_average:.2f}% na capacidade {first_capacity} "
        f"para {last_average:.2f}% na capacidade {last_capacity}."
    )


def add_paragraph(story: list[object], text: str, style: object, space: float = 0.22) -> None:
    story.append(Paragraph(text, style))
    story.append(Spacer(1, space * cm))


def build_report(results_path: Path, chart_path: Path, output_path: Path) -> None:
    rows = load_results(results_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Relatório Experimental - Simulador de Memória Cache", styles["Title"]))
    story.append(Paragraph("Data da entrega: 30 de junho de 2026", styles["Normal"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Introdução", styles["Heading1"]))
    add_paragraph(
        story,
        "Este relatório apresenta a implementação e a avaliação experimental de um simulador de memória cache em Python. "
        "O estudo compara as políticas FIFO, LRU e LFU a partir de um trace sintético com 10.000 acessos, seguindo um procedimento reproduzível por linha de comando.",
        styles["BodyText"],
    )
    story.append(Paragraph("Descrição das políticas implementadas", styles["Heading1"]))
    add_paragraph(
        story,
        "<b>FIFO:</b> remove o item inserido há mais tempo, sem considerar recência ou frequência de uso.<br/>"
        "<b>LRU:</b> remove o item menos recentemente utilizado, priorizando itens acessados há menos tempo.<br/>"
        "<b>LFU:</b> remove o item com menor frequência de acesso e, em caso de empate, remove o item mais antigo entre os empatados.",
        styles["BodyText"],
    )
    story.append(Paragraph("Objetivo do experimento", styles["Heading1"]))
    add_paragraph(
        story,
        "O objetivo foi medir como a variação da capacidade do cache influencia o hit ratio e comparar o comportamento das três políticas sob o mesmo conjunto de acessos. "
        "A hipótese avaliada foi que capacidades maiores tendem a aumentar a taxa de acertos, mas que a intensidade desse ganho depende da política de substituição.",
        styles["BodyText"],
    )
    story.append(Paragraph("Metodologia experimental", styles["Heading1"]))
    add_paragraph(
        story,
        "O experimento foi conduzido com um trace em CSV contendo uma coluna <b>item_id</b>. Cada linha representa uma requisição a um item. "
        "O trace foi gerado artificialmente com distribuição não uniforme: itens quentes aparecem com maior probabilidade, itens mornos aparecem com frequência intermediária e itens frios aparecem ocasionalmente. "
        "Essa escolha cria um workload com repetição suficiente para evidenciar diferenças entre políticas de substituição.",
        styles["BodyText"],
    )
    add_paragraph(
        story,
        "<b>Variável independente:</b> capacidade máxima do cache.<br/>"
        "<b>Variável dependente:</b> hit ratio obtido ao final da simulação.<br/>"
        "<b>Variáveis controladas:</b> mesmo trace de entrada, mesma implementação do simulador, mesmas políticas avaliadas e mesma métrica de comparação.",
        styles["BodyText"],
    )
    add_paragraph(
        story,
        "<b>Procedimento reproduzível:</b><br/>"
        "1. Gerar ou reutilizar o arquivo <b>data/trace.csv</b> com 10.000 acessos.<br/>"
        "2. Executar o simulador para cada política: FIFO, LRU e LFU.<br/>"
        "3. Repetir cada política nas capacidades 100, 500 e 1000 itens.<br/>"
        "4. Registrar total de acessos, hits, misses e hit ratio.<br/>"
        "5. Consolidar os resultados em CSV e gerar o gráfico comparativo.",
        styles["BodyText"],
    )
    story.append(Paragraph("Configuração dos experimentos", styles["Heading1"]))
    add_paragraph(
        story,
        "As políticas FIFO, LRU e LFU foram executadas com capacidades de 100, 500 e 1000 itens. "
        "A métrica principal analisada foi o hit ratio, calculado como <b>hits / total de acessos * 100</b>. "
        "Todas as execuções utilizaram o mesmo arquivo de entrada, permitindo comparação direta entre as políticas.",
        styles["BodyText"],
    )
    add_paragraph(
        story,
        "Comandos utilizados: <br/>"
        "<b>python3 scripts/generate_trace.py --output data/trace.csv --rows 10000</b><br/>"
        "<b>python3 scripts/run_experiments.py --input data/trace.csv</b><br/>"
        "<b>python3 scripts/generate_report.py</b>",
        styles["BodyText"],
    )

    table_data = [["Política", "Capacidade", "Acessos", "Hits", "Misses", "Hit ratio (%)"]]
    for row in rows:
        table_data.append(
            [
                row["policy"].upper(),
                row["capacity"],
                row["total_accesses"],
                row["hits"],
                row["misses"],
                f"{float(row['hit_ratio']):.2f}",
            ]
        )
    table = Table(table_data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173f7a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
            ]
        )
    )
    story.append(Spacer(1, 0.25 * cm))
    story.append(table)

    story.append(PageBreak())
    story.append(Paragraph("Gráficos gerados", styles["Heading1"]))
    story.append(Image(str(chart_path), width=16 * cm, height=9.5 * cm))

    story.append(Paragraph("Discussão dos resultados", styles["Heading1"]))
    add_paragraph(
        story,
        "O aumento da capacidade elevou o hit ratio porque mais itens puderam permanecer no cache entre acessos repetidos. "
        + capacity_summary(rows)
        + " As diferenças entre as políticas aparecem porque FIFO considera apenas a ordem de entrada, LRU privilegia recência e LFU privilegia frequência. "
        + best_policy(rows),
        styles["BodyText"],
    )
    add_paragraph(
        story,
        "No workload utilizado, a presença de itens quentes favoreceu políticas capazes de preservar itens acessados repetidamente. "
        "Por isso, a LFU apresentou vantagem, principalmente na menor capacidade, pois acumulou frequência para itens recorrentes e evitou removê-los cedo.",
        styles["BodyText"],
    )
    story.append(Paragraph("Limitações", styles["Heading1"]))
    add_paragraph(
        story,
        "A simulação avalia apenas identificadores de itens. Ela não modela latência, tamanho variável de objetos, custo de escrita, concorrência, pré-busca, hierarquias reais de cache ou efeitos de hardware. "
        "Além disso, o trace é sintético; portanto, os resultados representam o comportamento desse workload específico e não devem ser generalizados sem novos traces.",
        styles["BodyText"],
    )

    story.append(Paragraph("Conclusão", styles["Heading1"]))
    add_paragraph(
        story,
        "O simulador permitiu comparar experimentalmente FIFO, LRU e LFU usando um processo reproduzível. "
        "Os resultados confirmam que a capacidade do cache influencia diretamente a taxa de acertos e que a escolha da política deve considerar o padrão de acesso do workload. "
        "Para o trace analisado, a LFU apresentou o melhor desempenho médio.",
        styles["BodyText"],
    )
    doc.build(story)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the experimental report PDF")
    parser.add_argument("--results", default="results/experiment_results.csv")
    parser.add_argument("--chart", default="results/hit_ratio_by_policy.png")
    parser.add_argument("--output", default="docs/relatorio-experimental.pdf")
    args = parser.parse_args()
    build_report(Path(args.results), Path(args.chart), Path(args.output))
    print(f"Report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

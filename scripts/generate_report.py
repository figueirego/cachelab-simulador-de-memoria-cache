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
    story.append(
        Paragraph(
            "Este relatório apresenta a implementação e a avaliação experimental de um simulador de memória cache em Python. "
            "Foram comparadas as políticas FIFO, LRU e LFU usando um trace sintético com 10.000 acessos.",
            styles["BodyText"],
        )
    )
    story.append(Paragraph("Descrição das políticas implementadas", styles["Heading1"]))
    story.append(
        Paragraph(
            "FIFO remove o item inserido há mais tempo. LRU remove o item menos recentemente utilizado. "
            "LFU remove o item com menor frequência de acesso e, em caso de empate, remove o item mais antigo entre os empatados.",
            styles["BodyText"],
        )
    )
    story.append(Paragraph("Metodologia experimental", styles["Heading1"]))
    story.append(
        Paragraph(
            "O trace possui uma distribuição não uniforme, com itens quentes, mornos e frios. "
            "Essa configuração simula um workload com repetição frequente em parte dos itens e acessos ocasionais a itens menos populares.",
            styles["BodyText"],
        )
    )
    story.append(Paragraph("Configuração dos experimentos", styles["Heading1"]))
    story.append(
        Paragraph(
            "As políticas FIFO, LRU e LFU foram executadas com capacidades de 100, 500 e 1000 itens. "
            "A métrica principal analisada foi o hit ratio, calculado como hits divididos pelo total de acessos.",
            styles["BodyText"],
        )
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
    story.append(
        Paragraph(
            "O aumento da capacidade tende a elevar o hit ratio porque mais itens permanecem disponíveis no cache entre acessos repetidos. "
            "As diferenças entre as políticas aparecem porque FIFO considera apenas a ordem de entrada, LRU privilegia recência e LFU privilegia frequência. "
            + best_policy(rows),
            styles["BodyText"],
        )
    )
    story.append(
        Paragraph(
            "O workload sintético favorece políticas capazes de preservar itens acessados repetidamente. "
            "Como limitação, a simulação avalia apenas identificadores de itens e não considera latência, tamanho variável de objetos, escrita em memória ou hierarquias reais de cache.",
            styles["BodyText"],
        )
    )

    story.append(Paragraph("Conclusão", styles["Heading1"]))
    story.append(
        Paragraph(
            "O simulador permitiu comparar experimentalmente FIFO, LRU e LFU. "
            "Os resultados mostram que a capacidade do cache influencia diretamente a taxa de acertos e que a escolha da política deve considerar o padrão de acesso do workload.",
            styles["BodyText"],
        )
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

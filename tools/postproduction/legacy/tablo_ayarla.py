# -*- coding: utf-8 -*-
"""
DOCX Tablo Genişliği Optimize Edici
-----------------------------------

Amaç:
- Pandoc/Word çıktısındaki tabloların gereksiz geniş görünen sütunlarını
  daha dengeli hâle getirmek.
- Özellikle "Ölçüt / Açıklama / Puan" veya "Kavram / Açıklama" gibi
  tablolarda kısa sütunları daraltıp açıklama sütunlarını genişletmek.

İki çalışma modu vardır:

1) proportional  [varsayılan]
   Sütun genişliklerini içerik uzunluğuna göre yaklaşık hesaplar.
   Daha kararlı DOCX/PDF çıktısı verir.

2) autofit
   Word'e "içeriğe göre otomatik sığdır" talimatı verir.
   Word dosya açıldığında tabloyu yeniden hesaplayabilir.
   Ancak LibreOffice/Pandoc sonrası PDF çıktısında her zaman aynı kararlılıkta olmayabilir.

Kullanım örnekleri:

    python docx_tablo_genislik_optimize.py KompaktBirlesik_duzeltilmis_v2.docx

    python docx_tablo_genislik_optimize.py KompaktBirlesik_duzeltilmis_v2.docx KompaktBirlesik_tablo_opt.docx

    python docx_tablo_genislik_optimize.py KompaktBirlesik_duzeltilmis_v2.docx --mode autofit

    python docx_tablo_genislik_optimize.py KompaktBirlesik_duzeltilmis_v2.docx --in-place

    python docx_tablo_genislik_optimize.py KompaktBirlesik_duzeltilmis_v2.docx --dry-run

Not:
- Bu betik tablo başlık renklerini değiştirmez.
- Dikkat/İpucu kutularına dokunmaz.
- Resim, H1 başlık, BÖLÜM SONU hizalarına dokunmaz.
"""

from __future__ import annotations

import argparse
import math
import re
import shutil
import sys
import zipfile
from pathlib import Path


# ------------------------------------------------------------
# XML yardımcıları
# ------------------------------------------------------------

def xml_text(xml: str) -> str:
    parts = re.findall(r"<w:t(?=[\s>])[^>]*>(.*?)</w:t>", xml, flags=re.DOTALL)
    text = "".join(parts)
    text = (
        text.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("&quot;", '"')
            .replace("&apos;", "'")
    )
    return re.sub(r"\s+", " ", text).strip()


def split_top_level(pattern: str, xml: str) -> list[re.Match]:
    return list(re.finditer(pattern, xml, flags=re.DOTALL))


def get_cells_from_row(tr_xml: str) -> list[str]:
    return [m.group(0) for m in re.finditer(r"<w:tc(?=[\s>])[^>]*>.*?</w:tc>", tr_xml, flags=re.DOTALL)]


def get_rows_from_table(tbl_xml: str) -> list[str]:
    return [m.group(0) for m in re.finditer(r"<w:tr(?=[\s>])[^>]*>.*?</w:tr>", tbl_xml, flags=re.DOTALL)]


def has_gridspan(tc_xml: str) -> bool:
    return "<w:gridSpan" in tc_xml


def get_gridspan(tc_xml: str) -> int:
    m = re.search(r'<w:gridSpan\s+w:val="(\d+)"', tc_xml)
    return int(m.group(1)) if m else 1


def get_col_count(tbl_xml: str) -> int:
    rows = get_rows_from_table(tbl_xml)
    max_cols = 0

    for row in rows[:12]:
        cells = get_cells_from_row(row)
        col_count = 0
        for cell in cells:
            col_count += get_gridspan(cell)
        max_cols = max(max_cols, col_count)

    return max_cols


def table_has_merged_cells(tbl_xml: str) -> bool:
    return "<w:gridSpan" in tbl_xml or "<w:vMerge" in tbl_xml


def set_tbl_width_pct(tbl_xml: str, pct: int = 100) -> str:
    """
    Tablo genel genişliğini yüzde olarak ayarlar.
    OOXML pct değeri 5000 = %100 anlamına gelir.
    """
    w_val = int(pct * 50)

    m = re.search(r"<w:tblPr\b[^>]*>.*?</w:tblPr>", tbl_xml, flags=re.DOTALL)
    if not m:
        m2 = re.match(r"(<w:tbl(?=[\s>])[^>]*>)", tbl_xml)
        if not m2:
            return tbl_xml
        tbl_pr = f'<w:tblPr><w:tblW w:w="{w_val}" w:type="pct"/></w:tblPr>'
        return m2.group(1) + tbl_pr + tbl_xml[m2.end():]

    tbl_pr = m.group(0)

    if re.search(r"<w:tblW\b", tbl_pr):
        tbl_pr = re.sub(
            r'<w:tblW\b[^>]*/>',
            f'<w:tblW w:w="{w_val}" w:type="pct"/>',
            tbl_pr,
            flags=re.DOTALL,
        )
    else:
        tbl_pr = tbl_pr.replace("</w:tblPr>", f'<w:tblW w:w="{w_val}" w:type="pct"/></w:tblPr>')

    return tbl_xml[:m.start()] + tbl_pr + tbl_xml[m.end():]


def set_tbl_layout(tbl_xml: str, layout: str) -> str:
    """
    layout: fixed veya autofit
    """
    m = re.search(r"<w:tblPr\b[^>]*>.*?</w:tblPr>", tbl_xml, flags=re.DOTALL)
    if not m:
        m2 = re.match(r"(<w:tbl(?=[\s>])[^>]*>)", tbl_xml)
        if not m2:
            return tbl_xml
        tbl_pr = f'<w:tblPr><w:tblLayout w:type="{layout}"/></w:tblPr>'
        return m2.group(1) + tbl_pr + tbl_xml[m2.end():]

    tbl_pr = m.group(0)

    if re.search(r"<w:tblLayout\b", tbl_pr):
        tbl_pr = re.sub(r'<w:tblLayout\b[^>]*/>', f'<w:tblLayout w:type="{layout}"/>', tbl_pr)
    else:
        tbl_pr = tbl_pr.replace("</w:tblPr>", f'<w:tblLayout w:type="{layout}"/></w:tblPr>')

    return tbl_xml[:m.start()] + tbl_pr + tbl_xml[m.end():]


def remove_tbl_grid(tbl_xml: str) -> str:
    return re.sub(r"<w:tblGrid\b[^>]*>.*?</w:tblGrid>", "", tbl_xml, flags=re.DOTALL)


def replace_tbl_grid(tbl_xml: str, pct_widths: list[float]) -> str:
    """
    tblGrid değerleri twips ister. Burada yaklaşık 9072 twips = 6.3 inch kullanılır.
    Bu yalnızca Word'e başlangıç ızgarası önerisi verir.
    """
    total_twips = 9072
    grid_cols = []
    for pct in pct_widths:
        w = max(300, int(total_twips * pct / 100.0))
        grid_cols.append(f'<w:gridCol w:w="{w}"/>')

    tbl_grid = "<w:tblGrid>" + "".join(grid_cols) + "</w:tblGrid>"

    if re.search(r"<w:tblGrid\b", tbl_xml):
        return re.sub(r"<w:tblGrid\b[^>]*>.*?</w:tblGrid>", tbl_grid, tbl_xml, flags=re.DOTALL)

    # tblPr'den sonra ekle
    m = re.search(r"</w:tblPr>", tbl_xml)
    if m:
        return tbl_xml[:m.end()] + tbl_grid + tbl_xml[m.end():]

    m2 = re.match(r"(<w:tbl(?=[\s>])[^>]*>)", tbl_xml)
    if m2:
        return m2.group(1) + tbl_grid + tbl_xml[m2.end():]

    return tbl_xml


def set_tc_width_pct(tc_xml: str, pct: float) -> str:
    """
    Hücre genişliğini yüzde olarak ayarlar.
    OOXML pct değeri 5000 = %100.
    """
    w_val = max(1, int(round(pct * 50)))

    m = re.search(r"<w:tcPr\b[^>]*>.*?</w:tcPr>", tc_xml, flags=re.DOTALL)
    if not m:
        m2 = re.match(r"(<w:tc(?=[\s>])[^>]*>)", tc_xml)
        if not m2:
            return tc_xml
        tc_pr = f'<w:tcPr><w:tcW w:w="{w_val}" w:type="pct"/></w:tcPr>'
        return m2.group(1) + tc_pr + tc_xml[m2.end():]

    tc_pr = m.group(0)
    if re.search(r"<w:tcW\b", tc_pr):
        tc_pr = re.sub(r'<w:tcW\b[^>]*/>', f'<w:tcW w:w="{w_val}" w:type="pct"/>', tc_pr)
    else:
        tc_pr = tc_pr.replace("</w:tcPr>", f'<w:tcW w:w="{w_val}" w:type="pct"/></w:tcPr>')

    return tc_xml[:m.start()] + tc_pr + tc_xml[m.end():]


def set_tc_width_auto(tc_xml: str) -> str:
    m = re.search(r"<w:tcPr\b[^>]*>.*?</w:tcPr>", tc_xml, flags=re.DOTALL)
    if not m:
        m2 = re.match(r"(<w:tc(?=[\s>])[^>]*>)", tc_xml)
        if not m2:
            return tc_xml
        tc_pr = '<w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr>'
        return m2.group(1) + tc_pr + tc_xml[m2.end():]

    tc_pr = m.group(0)
    if re.search(r"<w:tcW\b", tc_pr):
        tc_pr = re.sub(r'<w:tcW\b[^>]*/>', '<w:tcW w:w="0" w:type="auto"/>', tc_pr)
    else:
        tc_pr = tc_pr.replace("</w:tcPr>", '<w:tcW w:w="0" w:type="auto"/></w:tcPr>')

    return tc_xml[:m.start()] + tc_pr + tc_xml[m.end():]


# ------------------------------------------------------------
# İçeriğe göre sütun genişliği tahmini
# ------------------------------------------------------------

def text_score(text: str) -> float:
    """
    Hücre içeriğinden genişlik skoru üretir.
    Çok uzun metinler tüm tabloyu domine etmesin diye kırpılır.
    """
    t = text.strip()
    if not t:
        return 3.0

    # Kod/metot adları ve uzun tekil tokenlar biraz daha geniş alan ister.
    tokens = t.split()
    longest_token = max((len(tok) for tok in tokens), default=0)
    visible_len = len(t)

    score = min(80.0, visible_len * 0.65 + longest_token * 0.55)
    return max(4.0, score)


def compute_column_scores(tbl_xml: str, col_count: int, max_rows: int = 30) -> list[float]:
    scores = [4.0 for _ in range(col_count)]
    row_count = 0

    for row in get_rows_from_table(tbl_xml):
        cells = get_cells_from_row(row)
        if not cells:
            continue

        col = 0
        for cell in cells:
            span = get_gridspan(cell)
            text = xml_text(cell)
            score = text_score(text)

            # Başlık satırları genellikle kısa olur; yine de tamamen ezilmesin.
            if row_count == 0:
                score *= 1.2

            # Birleşik hücre varsa skoru ilgili sütunlara böl.
            for k in range(span):
                if col + k < col_count:
                    scores[col + k] = max(scores[col + k], score / max(span, 1))
            col += span

        row_count += 1
        if row_count >= max_rows:
            break

    return scores


def normalize_widths(
    scores: list[float],
    min_pct: float,
    max_pct: float,
) -> list[float]:
    n = len(scores)
    if n == 0:
        return []

    # Çok sütunlu tablolarda max daha düşük olmalı.
    if n >= 5:
        max_pct = min(max_pct, 38.0)
    elif n == 4:
        max_pct = min(max_pct, 45.0)
    elif n == 3:
        max_pct = min(max_pct, 62.0)
    elif n == 2:
        max_pct = min(max_pct, 72.0)

    total = sum(scores)
    if total <= 0:
        return [100.0 / n for _ in range(n)]

    widths = [s / total * 100.0 for s in scores]

    # Min/max sınırlarını yinelemeli uygula.
    for _ in range(8):
        changed = False
        for i, w in enumerate(widths):
            if w < min_pct:
                widths[i] = min_pct
                changed = True
            elif w > max_pct:
                widths[i] = max_pct
                changed = True

        rem = 100.0 - sum(widths)
        if abs(rem) < 0.01:
            break

        adjustable = [
            i for i, w in enumerate(widths)
            if (rem > 0 and w < max_pct) or (rem < 0 and w > min_pct)
        ]

        if not adjustable:
            break

        score_sum = sum(scores[i] for i in adjustable)
        if score_sum <= 0:
            delta = rem / len(adjustable)
            for i in adjustable:
                widths[i] += delta
        else:
            for i in adjustable:
                widths[i] += rem * (scores[i] / score_sum)

        if not changed and abs(rem) < 0.1:
            break

    # Son küçük farkı en geniş sütuna ekle/çıkar.
    diff = 100.0 - sum(widths)
    if widths:
        idx = max(range(len(widths)), key=lambda i: widths[i])
        widths[idx] += diff

    return widths


# ------------------------------------------------------------
# Tablo dönüştürme
# ------------------------------------------------------------

def apply_autofit(tbl_xml: str) -> str:
    tbl_xml = set_tbl_layout(tbl_xml, "autofit")
    tbl_xml = set_tbl_width_pct(tbl_xml, 100)
    tbl_xml = remove_tbl_grid(tbl_xml)

    def tc_repl(match: re.Match) -> str:
        return set_tc_width_auto(match.group(0))

    tbl_xml = re.sub(r"<w:tc(?=[\s>])[^>]*>.*?</w:tc>", tc_repl, tbl_xml, flags=re.DOTALL)
    return tbl_xml


def apply_proportional(tbl_xml: str, min_pct: float, max_pct: float, skip_merged: bool) -> tuple[str, bool, list[float]]:
    col_count = get_col_count(tbl_xml)

    if col_count <= 1:
        return tbl_xml, False, []

    if skip_merged and table_has_merged_cells(tbl_xml):
        return tbl_xml, False, []

    scores = compute_column_scores(tbl_xml, col_count)
    widths = normalize_widths(scores, min_pct=min_pct, max_pct=max_pct)

    tbl_xml = set_tbl_layout(tbl_xml, "fixed")
    tbl_xml = set_tbl_width_pct(tbl_xml, 100)
    tbl_xml = replace_tbl_grid(tbl_xml, widths)

    def row_repl(match: re.Match) -> str:
        row = match.group(0)
        cells = get_cells_from_row(row)

        if not cells:
            return row

        out = []
        last_end = 0
        col = 0

        for cm in re.finditer(r"<w:tc(?=[\s>])[^>]*>.*?</w:tc>", row, flags=re.DOTALL):
            out.append(row[last_end:cm.start()])
            cell = cm.group(0)
            span = get_gridspan(cell)

            pct = sum(widths[col:col + span]) if col < len(widths) else 100.0 / col_count
            cell = set_tc_width_pct(cell, pct)

            out.append(cell)
            last_end = cm.end()
            col += span

        out.append(row[last_end:])
        return "".join(out)

    tbl_xml = re.sub(r"<w:tr(?=[\s>])[^>]*>.*?</w:tr>", row_repl, tbl_xml, flags=re.DOTALL)

    return tbl_xml, True, widths


def patch_document_xml(
    document_xml: str,
    mode: str,
    min_pct: float,
    max_pct: float,
    skip_merged: bool,
    dry_run: bool,
) -> tuple[str, dict]:
    stats = {
        "tables_total": 0,
        "tables_changed": 0,
        "tables_skipped_one_col": 0,
        "tables_skipped_merged": 0,
        "mode": mode,
        "sample_widths": [],
    }

    def tbl_repl(match: re.Match) -> str:
        tbl = match.group(0)
        stats["tables_total"] += 1

        col_count = get_col_count(tbl)

        if col_count <= 1:
            stats["tables_skipped_one_col"] += 1
            return tbl

        if mode == "autofit":
            new_tbl = apply_autofit(tbl)
            stats["tables_changed"] += 1
            if len(stats["sample_widths"]) < 10:
                stats["sample_widths"].append({"table": stats["tables_total"], "col_count": col_count, "mode": "autofit"})
            return tbl if dry_run else new_tbl

        if mode == "proportional":
            new_tbl, changed, widths = apply_proportional(tbl, min_pct, max_pct, skip_merged)
            if not changed:
                if skip_merged and table_has_merged_cells(tbl):
                    stats["tables_skipped_merged"] += 1
                return tbl

            stats["tables_changed"] += 1
            if len(stats["sample_widths"]) < 10:
                stats["sample_widths"].append({
                    "table": stats["tables_total"],
                    "col_count": col_count,
                    "widths": [round(w, 1) for w in widths],
                })
            return tbl if dry_run else new_tbl

        return tbl

    patched = re.sub(r"<w:tbl(?=[\s>])[^>]*>.*?</w:tbl>", tbl_repl, document_xml, flags=re.DOTALL)
    return patched, stats


def optimize_docx(
    input_docx: Path,
    output_docx: Path,
    mode: str,
    min_pct: float,
    max_pct: float,
    skip_merged: bool,
    dry_run: bool,
) -> dict:
    stats_final = None

    if dry_run:
        with zipfile.ZipFile(input_docx, "r") as zin:
            xml = zin.read("word/document.xml").decode("utf-8", errors="ignore")
            _, stats = patch_document_xml(xml, mode, min_pct, max_pct, skip_merged, dry_run=True)
            return stats

    with zipfile.ZipFile(input_docx, "r") as zin:
        with zipfile.ZipFile(output_docx, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)

                if item.filename == "word/document.xml":
                    xml = data.decode("utf-8", errors="ignore")
                    xml, stats_final = patch_document_xml(
                        xml,
                        mode=mode,
                        min_pct=min_pct,
                        max_pct=max_pct,
                        skip_merged=skip_merged,
                        dry_run=False,
                    )
                    data = xml.encode("utf-8")

                zout.writestr(item, data)

    return stats_final or {}


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="DOCX tablolarında sütun genişliklerini içerik uzunluğuna göre optimize eder."
    )
    parser.add_argument("input_docx", help="Girdi DOCX dosyası")
    parser.add_argument("output_docx", nargs="?", help="Çıktı DOCX dosyası")
    parser.add_argument(
        "--mode",
        choices=["proportional", "autofit"],
        default="proportional",
        help="proportional: kararlı içerik-oranlı genişlik; autofit: Word AutoFit",
    )
    parser.add_argument("--min-col-pct", type=float, default=7.0, help="Bir sütun için minimum yüzde genişlik")
    parser.add_argument("--max-col-pct", type=float, default=72.0, help="Bir sütun için maksimum yüzde genişlik")
    parser.add_argument("--include-merged", action="store_true", help="Birleşik hücreli tabloları da işlemeye çalışır")
    parser.add_argument("--dry-run", action="store_true", help="Dosya yazmadan analiz yapar")
    parser.add_argument("--in-place", action="store_true", help="Aynı dosyanın üzerine yazar; önce .bak yedeği alır")
    args = parser.parse_args(argv)

    input_docx = Path(args.input_docx)

    if not input_docx.exists():
        print(f"Hata: Dosya bulunamadı: {input_docx}")
        return 1

    if args.dry_run:
        output_docx = input_docx
    elif args.in_place:
        backup = input_docx.with_suffix(input_docx.suffix + ".bak")
        shutil.copy2(input_docx, backup)
        print(f"Yedek oluşturuldu: {backup}")
        output_docx = input_docx.with_suffix(".tmp.docx")
    else:
        output_docx = Path(args.output_docx) if args.output_docx else input_docx.with_name(input_docx.stem + "_tablo_opt.docx")

    stats = optimize_docx(
        input_docx=input_docx if not args.in_place else backup,
        output_docx=output_docx,
        mode=args.mode,
        min_pct=args.min_col_pct,
        max_pct=args.max_col_pct,
        skip_merged=not args.include_merged,
        dry_run=args.dry_run,
    )

    if args.in_place and not args.dry_run:
        shutil.move(str(output_docx), str(input_docx))
        output_docx = input_docx

    print("DOCX tablo genişliği optimizasyonu tamamlandı.")
    print(f"Girdi : {input_docx}")
    if not args.dry_run:
        print(f"Çıktı : {output_docx}")
    print()
    print("İşlem özeti:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    print()
    if args.mode == "autofit":
        print("Not: AutoFit modu Word dosya açıldığında yeniden hesaplanabilir. Word'de belgeyi açıp kaydetmeniz gerekebilir.")
    else:
        print("Not: proportional modu PDF/DOCX çıktısı için daha kararlı sonuç verir.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

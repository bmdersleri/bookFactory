"""
React kitap bölümleri için hafif Markdown kalite kontrol aracı.

Kullanım:
python -m tools.quality.check_chapter_markdown ^
  --chapter .\workspace\react\chapters\chapter_01_modern_web_giris.md ^
  --chapter-id chapter_01 ^
  --chapter-no 1 ^
  --report .\workspace\react\build\test_reports\chapter_01_markdown_quality_report.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_yaml_front_matter(text: str) -> bool:
    return text.startswith("---\n") and "\n---\n" in text[4:]


def extract_headings(text: str) -> list[str]:
    return re.findall(r"^(#{1,6})\s+(.+?)\s*$", text, flags=re.MULTILINE)


def count_fenced_blocks(text: str) -> int:
    return len(re.findall(r"^```", text, flags=re.MULTILINE))


def extract_code_meta_blocks(text: str) -> list[str]:
    return re.findall(r"<!--\s*CODE_META\s*(.*?)\s*-->", text, flags=re.DOTALL)


def extract_screenshot_markers(text: str) -> list[str]:
    return re.findall(r"\[SCREENSHOT:([A-Za-z0-9_\-]+)\]", text)


def add_result(results: list[dict], category: str, status: str, detail: str) -> None:
    results.append(
        {
            "category": category,
            "status": status,
            "detail": detail,
        }
    )


def status_icon(status: str) -> str:
    return {
        "OK": "✅",
        "WARN": "⚠️",
        "FAIL": "❌",
    }.get(status, "ℹ️")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", required=True, help="Kontrol edilecek Markdown dosyası")
    parser.add_argument("--chapter-id", default="chapter_01")
    parser.add_argument("--chapter-no", type=int, default=1)
    parser.add_argument("--report", required=True, help="Üretilecek Markdown raporu")
    parser.add_argument("--strict", action="store_true", help="FAIL varsa çıkış kodunu 1 yapar")
    args = parser.parse_args()

    chapter_path = Path(args.chapter)
    report_path = Path(args.report)

    results: list[dict] = []

    if not chapter_path.exists():
        add_result(results, "Dosya", "FAIL", f"Dosya bulunamadı: `{chapter_path}`")
        text = ""
    else:
        text = read_text(chapter_path)
        add_result(results, "Dosya", "OK", f"Dosya okundu: `{chapter_path}`")

    if text:
        # 1. YAML front matter
        if has_yaml_front_matter(text):
            add_result(results, "YAML front matter", "OK", "Dosya YAML front matter ile başlıyor.")
        else:
            add_result(results, "YAML front matter", "FAIL", "YAML front matter bulunamadı veya dosya başında değil.")

        # 2. Başlık kontrolü
        headings = extract_headings(text)
        h1 = [h for h in headings if h[0] == "#"]

        if len(h1) == 1:
            add_result(results, "Ana başlık", "OK", f"Tek H1 başlığı var: `{h1[0][1]}`")
        elif len(h1) == 0:
            add_result(results, "Ana başlık", "FAIL", "H1 düzeyinde bölüm başlığı bulunamadı.")
        else:
            add_result(results, "Ana başlık", "FAIL", f"Birden fazla H1 başlığı bulundu: {len(h1)}")

        expected_h1_prefix = f"Bölüm {args.chapter_no}:"
        if h1 and h1[0][1].startswith(expected_h1_prefix):
            add_result(results, "Bölüm numarası", "OK", f"H1 başlığı `{expected_h1_prefix}` ile başlıyor.")
        else:
            add_result(results, "Bölüm numarası", "WARN", f"H1 başlığı `{expected_h1_prefix}` ile başlamıyor olabilir.")

        # 3. Standart ana başlıklar
        expected_sections = [
            f"{args.chapter_no}.1 Bölümün yol haritası",
            f"{args.chapter_no}.2 Bölümün konumu",
            f"{args.chapter_no}.3 Öğrenme çıktıları",
            f"{args.chapter_no}.4 Ön bilgi",
            f"{args.chapter_no}.9 KampüsHub",
            f"{args.chapter_no}.10 Sık yapılan hatalar",
            f"{args.chapter_no}.11 Hata ayıklama",
            f"{args.chapter_no}.12 Bölüm özeti",
            f"{args.chapter_no}.13 Kavramsal sorular",
            f"{args.chapter_no}.14 Programlama alıştırmaları",
            f"{args.chapter_no}.15 Haftalık laboratuvar",
            f"{args.chapter_no}.16 İleri okuma",
        ]

        missing_sections = []
        for section in expected_sections:
            if section.lower() not in text.lower():
                missing_sections.append(section)

        if not missing_sections:
            add_result(results, "Standart bölüm başlıkları", "OK", "Beklenen ana bölüm başlıkları görünüyor.")
        else:
            add_result(
                results,
                "Standart bölüm başlıkları",
                "WARN",
                "Eksik veya farklı adlandırılmış başlıklar: " + ", ".join(f"`{s}`" for s in missing_sections),
            )

        # 4. Kod blokları kapanış kontrolü
        fence_count = count_fenced_blocks(text)
        if fence_count % 2 == 0:
            add_result(results, "Kod bloğu kapanışı", "OK", f"Fence sayısı çift: {fence_count}")
        else:
            add_result(results, "Kod bloğu kapanışı", "FAIL", f"Fence sayısı tek: {fence_count}. Kapanmamış kod bloğu olabilir.")

        # 5. CODE_META kontrolü
        code_meta_blocks = extract_code_meta_blocks(text)
        if code_meta_blocks:
            add_result(results, "CODE_META", "OK", f"{len(code_meta_blocks)} CODE_META bloğu bulundu.")
        else:
            add_result(results, "CODE_META", "WARN", "CODE_META bloğu bulunamadı.")

        if "// CODE_META" in text:
            add_result(
                results,
                "CODE_META biçimi",
                "FAIL",
                "`// CODE_META` kullanımı bulundu. CODE_META kod bloğu öncesinde HTML yorum bloğu olarak yazılmalı.",
            )
        else:
            add_result(results, "CODE_META biçimi", "OK", "`// CODE_META` biçiminde hatalı kullanım bulunmadı.")

        required_meta_fields = [
            "id:",
            "chapter_id:",
            "language:",
            "file:",
            "extract:",
            "test:",
        ]

        meta_field_warnings = []
        for i, block in enumerate(code_meta_blocks, start=1):
            for field in required_meta_fields:
                if field not in block:
                    meta_field_warnings.append(f"CODE_META #{i}: `{field}` eksik")

        if not meta_field_warnings:
            add_result(results, "CODE_META alanları", "OK", "Temel CODE_META alanları mevcut görünüyor.")
        else:
            add_result(results, "CODE_META alanları", "WARN", "; ".join(meta_field_warnings))

        # 6. Screenshot marker kontrolü
        screenshots = extract_screenshot_markers(text)
        if screenshots:
            add_result(results, "Screenshot marker", "OK", f"{len(screenshots)} screenshot marker bulundu: {', '.join(screenshots)}")
        else:
            add_result(results, "Screenshot marker", "WARN", "Screenshot marker bulunamadı.")

        invalid_screenshots = [s for s in screenshots if not re.match(r"^b\d{2}_\d{2}_[a-z0-9_]+$", s)]
        if invalid_screenshots:
            add_result(
                results,
                "Screenshot ad standardı",
                "WARN",
                "Standart dışı marker adları: " + ", ".join(invalid_screenshots),
            )
        else:
            add_result(results, "Screenshot ad standardı", "OK", "Screenshot marker adları standartla uyumlu görünüyor.")

        # 7. Bölüm 1 zorunlu kavram kontrolü
        required_terms = [
            "modern web",
            "SPA",
            "React",
            "bileşen",
            "Node.js",
            "npm",
            "Vite",
            "npm create vite@latest",
            "npm install",
            "npm run dev",
            "HMR",
            "React DevTools",
            "package.json",
            "index.html",
            "main.jsx",
            "App.jsx",
            "KampüsHub",
        ]

        missing_terms = []
        lower_text = text.lower()
        for term in required_terms:
            if term.lower() not in lower_text:
                missing_terms.append(term)

        if not missing_terms:
            add_result(results, "Bölüm 1 zorunlu kavramları", "OK", "Temel Bölüm 1 kavramları metinde bulunuyor.")
        else:
            add_result(
                results,
                "Bölüm 1 zorunlu kavramları",
                "WARN",
                "Eksik görünebilecek kavramlar: " + ", ".join(f"`{t}`" for t in missing_terms),
            )

        # 8. Kapsam dışı konu kontrolü
        forbidden_terms = [
            "Next.js App Router",
            "Server Components",
            "Server Actions",
            "GraphQL",
            "React Native",
            "Docker",
            "Kubernetes",
            "class component",
        ]

        found_forbidden = []
        for term in forbidden_terms:
            if term.lower() in lower_text:
                found_forbidden.append(term)

        if found_forbidden:
            add_result(
                results,
                "Kapsam dışı konu",
                "WARN",
                "Metinde kapsam dışı konu ifadesi bulundu; yalnızca kısa not olduğundan emin olun: "
                + ", ".join(f"`{t}`" for t in found_forbidden),
            )
        else:
            add_result(results, "Kapsam dışı konu", "OK", "Ana akışı bozacak kapsam dışı konu bulunmadı.")

        # 9. Bölüm sonu kontrolü
        ending_terms = [
            "Bölüm özeti",
            "Terim sözlüğü",
            "Kavramsal sorular",
            "Programlama alıştırmaları",
            "Haftalık laboratuvar",
            "İleri okuma",
            "Bir sonraki bölüme geçiş",
        ]

        missing_ending = [term for term in ending_terms if term.lower() not in lower_text]
        if not missing_ending:
            add_result(results, "Bölüm sonu yapısı", "OK", "Bölüm sonu bileşenleri mevcut görünüyor.")
        else:
            add_result(
                results,
                "Bölüm sonu yapısı",
                "WARN",
                "Eksik bölüm sonu bileşenleri: " + ", ".join(f"`{t}`" for t in missing_ending),
            )

        # 10. Türkçe karakter / bozulma kontrolü
        mojibake_patterns = ["KampÃ", "Ã¼", "Ä", "Å", "�"]
        found_mojibake = [p for p in mojibake_patterns if p in text]
        if found_mojibake:
            add_result(results, "UTF-8 / Türkçe karakter", "FAIL", "Olası bozulmuş karakter örüntüsü bulundu.")
        else:
            add_result(results, "UTF-8 / Türkçe karakter", "OK", "Belirgin Türkçe karakter bozulması bulunmadı.")

    total_fail = sum(1 for r in results if r["status"] == "FAIL")
    total_warn = sum(1 for r in results if r["status"] == "WARN")
    total_ok = sum(1 for r in results if r["status"] == "OK")

    if total_fail:
        final_decision = "❌ KRİTİK SORUN VAR"
    elif total_warn:
        final_decision = "⚠️ KÜÇÜK DÜZELTME / İNCELEME GEREKİYOR"
    else:
        final_decision = "✅ MARKDOWN KALİTE KONTROLÜ BAŞARILI"

    report_lines = [
        "# Bölüm Markdown Kalite Kontrol Raporu",
        "",
        f"**Dosya:** `{chapter_path}`",
        f"**Bölüm ID:** `{args.chapter_id}`",
        f"**Bölüm No:** `{args.chapter_no}`",
        "",
        "## Özet",
        "",
        f"- ✅ Başarılı kontrol: {total_ok}",
        f"- ⚠️ Uyarı: {total_warn}",
        f"- ❌ Kritik hata: {total_fail}",
        f"- **Genel karar:** {final_decision}",
        "",
        "## Kontrol sonuçları",
        "",
        "| # | Kategori | Durum | Açıklama |",
        "|---:|---|---:|---|",
    ]

    for i, result in enumerate(results, start=1):
        report_lines.append(
            f"| {i} | {result['category']} | {status_icon(result['status'])} {result['status']} | {result['detail']} |"
        )

    report_lines.extend(
        [
            "",
            "## Yorum",
            "",
            "Bu rapor yalnızca Markdown yapısını ve metin içi standart işaretçileri kontrol eder. "
            "Kodların gerçekten çalışıp çalışmadığı için ayrıca `tools.code.run_code_tests` hattı kullanılmalıdır.",
            "",
        ]
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    print(f"OK: {total_ok} | WARN: {total_warn} | FAIL: {total_fail}")
    print(f"Markdown report: {report_path}")
    print(f"Decision: {final_decision}")

    if args.strict and total_fail:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
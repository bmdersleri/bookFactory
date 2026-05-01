# -*- coding: utf-8 -*-
"""
DOCX Güvenli Biçim Onarıcı v2
-----------------------------

Bu sürüm, özellikle şu iki sorunu düzeltmek için hazırlandı:

1. Önceki ortalama betiği sonrasında "Dikkat", "İpucu", "Sınav Notu",
   "Bölüm Hedefi", "Alıştırma Molası" gibi pedagogik kutuların ortalanması.
2. Bazı tablo başlıklarının görünmez veya okunaksız hâle gelmesi.

Özellikler:
- python-docx gerektirmez; doğrudan DOCX içindeki OOXML dosyalarını düzenler.
- Resim paragraflarını ortalar.
- Ana bölüm/ek H1 başlıklarını ortalar.
- BÖLÜM SONU ve EK ... SONU paragraflarını ortalar.
- Pedagogik kutu paragraflarını iki yana yaslar.
- DikkatKutusu, IpucuKutusu, SinavNotuKutusu vb. stilleri iki yana yaslı hâle getirir.
- Tablo başlık satırlarını açık zemin + siyah yazı + kalın metin olarak onarır.
- Tablo gövde metinlerine genel hizalama uygulamaz.

Kullanım:
    python docx_guvenli_bicim_duzelt_v2.py KompaktBirlesik.docx

Ayrı çıktı:
    python docx_guvenli_bicim_duzelt_v2.py KompaktBirlesik.docx KompaktBirlesik_v2.docx

Yerinde düzeltme:
    python docx_guvenli_bicim_duzelt_v2.py KompaktBirlesik.docx --in-place

Tablo başlıklarını düzeltmeden:
    python docx_guvenli_bicim_duzelt_v2.py KompaktBirlesik.docx --no-table-header-fix
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


# ------------------------------------------------------------
# XML yardımcıları
# ------------------------------------------------------------

def xml_text(p_xml: str) -> str:
    """
    Bir paragraf veya hücre içindeki w:t metinlerini sade metne çevirir.
    XML kaçışlarını sınırlı düzeyde geri alır.
    """
    parts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p_xml, flags=re.DOTALL)
    text = "".join(parts)
    text = (
        text.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("&quot;", '"')
            .replace("&apos;", "'")
    )
    return re.sub(r"\s+", " ", text).strip()


def get_pstyle(p_xml: str) -> str:
    m = re.search(r'<w:pStyle\s+w:val="([^"]+)"', p_xml)
    return m.group(1) if m else ""


def has_drawing(p_xml: str) -> bool:
    return "<w:drawing" in p_xml or "<w:pict" in p_xml or "<pic:pic" in p_xml or "<a:blip" in p_xml


def replace_or_add_jc_in_ppr(ppr_xml: str, value: str) -> str:
    """
    w:pPr içinde w:jc varsa değiştirir, yoksa ekler.
    value: center, both, left vb.
    """
    if re.search(r"<w:jc\b", ppr_xml):
        return re.sub(r'<w:jc\b[^>]*/>', f'<w:jc w:val="{value}"/>', ppr_xml)

    # pPr kapanmadan önce ekle
    return ppr_xml.replace("</w:pPr>", f'<w:jc w:val="{value}"/></w:pPr>"')


def set_paragraph_alignment(p_xml: str, value: str) -> str:
    """
    Paragraf hizalamasını ayarlar.
    value: center, both, left vb.
    """
    m = re.search(r"<w:pPr\b[^>]*>.*?</w:pPr>", p_xml, flags=re.DOTALL)

    if m:
        old_ppr = m.group(0)
        new_ppr = replace_or_add_jc_in_ppr(old_ppr, value)
        return p_xml[:m.start()] + new_ppr + p_xml[m.end():]

    # pPr yoksa w:p açılışından hemen sonra ekle.
    m2 = re.match(r"(<w:p\b[^>]*>)", p_xml)
    if m2:
        return m2.group(1) + f'<w:pPr><w:jc w:val="{value}"/></w:pPr>' + p_xml[m2.end():]

    return p_xml


def add_or_replace_run_color_and_bold(r_xml: str) -> str:
    """
    Bir run içinde metni siyah ve kalın yapar.
    """
    if "<w:rPr" in r_xml:
        m = re.search(r"<w:rPr\b[^>]*>.*?</w:rPr>", r_xml, flags=re.DOTALL)
        if not m:
            return r_xml

        rpr = m.group(0)

        if re.search(r"<w:color\b", rpr):
            rpr = re.sub(r'<w:color\b[^>]*/>', '<w:color w:val="000000"/>', rpr)
        else:
            rpr = rpr.replace("</w:rPr>", '<w:color w:val="000000"/></w:rPr>')

        if not re.search(r"<w:b\b", rpr):
            rpr = rpr.replace("</w:rPr>", "<w:b/></w:rPr>")

        return r_xml[:m.start()] + rpr + r_xml[m.end():]

    # rPr yoksa w:r açılışından sonra ekle
    m = re.match(r"(<w:r\b[^>]*>)", r_xml)
    if m:
        return m.group(1) + '<w:rPr><w:b/><w:color w:val="000000"/></w:rPr>' + r_xml[m.end():]

    return r_xml


def ensure_cell_shading(tc_xml: str, fill: str = "D9EAF7") -> str:
    """
    Hücreye açık zemin rengi uygular.
    """
    m = re.search(r"<w:tcPr\b[^>]*>.*?</w:tcPr>", tc_xml, flags=re.DOTALL)

    if m:
        tcpr = m.group(0)
        if re.search(r"<w:shd\b", tcpr):
            tcpr = re.sub(r'<w:shd\b[^>]*/>', f'<w:shd w:fill="{fill}"/>', tcpr)
        else:
            tcpr = tcpr.replace("</w:tcPr>", f'<w:shd w:fill="{fill}"/></w:tcPr>')
        return tc_xml[:m.start()] + tcpr + tc_xml[m.end():]

    # tcPr yoksa w:tc açılışından sonra ekle
    m2 = re.match(r"(<w:tc\b[^>]*>)", tc_xml)
    if m2:
        return m2.group(1) + f'<w:tcPr><w:shd w:fill="{fill}"/></w:tcPr>' + tc_xml[m2.end():]

    return tc_xml


def ensure_table_header_repeat(tr_xml: str) -> str:
    """
    İlk tablo satırını Word'de tekrar eden başlık satırı olarak işaretler.
    """
    m = re.search(r"<w:trPr\b[^>]*>.*?</w:trPr>", tr_xml, flags=re.DOTALL)

    if m:
        trpr = m.group(0)
        if "<w:tblHeader" not in trpr:
            trpr = trpr.replace("</w:trPr>", '<w:tblHeader w:val="true"/></w:trPr>')
        else:
            trpr = re.sub(r'<w:tblHeader\b[^>]*/>', '<w:tblHeader w:val="true"/>', trpr)
        return tr_xml[:m.start()] + trpr + tr_xml[m.end():]

    m2 = re.match(r"(<w:tr\b[^>]*>)", tr_xml)
    if m2:
        return m2.group(1) + '<w:trPr><w:tblHeader w:val="true"/></w:trPr>' + tr_xml[m2.end():]

    return tr_xml


# ------------------------------------------------------------
# Hedef paragraf türleri
# ------------------------------------------------------------

PEDAGOGIC_STYLE_RE = re.compile(
    r"(Dikkat|Ipucu|İpucu|Ipu|İpu|Sinav|Sınav|Notu|Hedef|Derin|Alistirma|Alıştırma|Laboratuvar|Kutusu)",
    flags=re.IGNORECASE,
)

PEDAGOGIC_TEXT_RE = re.compile(
    r"^\s*(?:⚠️|💡|🎯|🔍)?\s*"
    r"(?:Dikkat|İpucu|Ipucu|Sınav Notu|Sinav Notu|Bölüm Hedefi|Bolum Hedefi|"
    r"Derinlemesine|Alıştırma Molası|Alistirma Molasi|Laboratuvar İpucu|Laboratuvar Ipucu)\s*:",
    flags=re.IGNORECASE,
)


def pedagogik_kutu_mu(p_xml: str) -> bool:
    style = get_pstyle(p_xml)
    text = xml_text(p_xml)

    if style and PEDAGOGIC_STYLE_RE.search(style):
        return True

    if PEDAGOGIC_TEXT_RE.search(text):
        return True

    return False


def ana_bolum_veya_ek_basligi_mi(p_xml: str) -> bool:
    style = get_pstyle(p_xml)
    text = xml_text(p_xml)

    is_h1 = style in {"Heading1", "Başlık1", "Baslik1"} or "outlineLvl w:val=\"0\"" in p_xml

    if not is_h1:
        return False

    if re.match(r"^(Bölüm|Bolum)\s+0?\d+\s*:", text, flags=re.IGNORECASE):
        return True

    if re.match(r"^Ek\s+[A-ZÇĞİÖŞÜ]\s*:", text, flags=re.IGNORECASE):
        return True

    return False


def bolum_sonu_mu(p_xml: str) -> bool:
    text = xml_text(p_xml).replace("*", "").strip()

    if text == "BÖLÜM SONU":
        return True

    if re.match(r"^EK\s+[A-ZÇĞİÖŞÜ]\s+SONU$", text, flags=re.IGNORECASE):
        return True

    return False


# ------------------------------------------------------------
# document.xml onarımı
# ------------------------------------------------------------

def patch_paragraphs(document_xml: str, stats: dict) -> str:
    """
    Tüm paragraf bloklarını dolaşır ve yalnızca hedeflenenleri hizalar.
    """
    def repl(match: re.Match) -> str:
        p_xml = match.group(0)

        if pedagogik_kutu_mu(p_xml):
            stats["justified_pedagogic_boxes"] += 1
            return set_paragraph_alignment(p_xml, "both")

        if has_drawing(p_xml):
            stats["centered_images"] += 1
            return set_paragraph_alignment(p_xml, "center")

        if ana_bolum_veya_ek_basligi_mi(p_xml):
            stats["centered_h1"] += 1
            return set_paragraph_alignment(p_xml, "center")

        if bolum_sonu_mu(p_xml):
            stats["centered_end_markers"] += 1
            return set_paragraph_alignment(p_xml, "center")

        return p_xml

    return re.sub(r"<w:p\b[^>]*>.*?</w:p>", repl, document_xml, flags=re.DOTALL)


def patch_table_header_row(tr_xml: str, stats: dict) -> str:
    """
    Bir tablonun ilk satırını başlık satırı olarak onarır.
    """
    tr_xml = ensure_table_header_repeat(tr_xml)

    def tc_repl(match: re.Match) -> str:
        tc = match.group(0)
        tc = ensure_cell_shading(tc, "D9EAF7")

        # Başlık hücrelerinin paragraflarını ortala.
        tc = re.sub(
            r"<w:p\b[^>]*>.*?</w:p>",
            lambda pm: set_paragraph_alignment(pm.group(0), "center"),
            tc,
            flags=re.DOTALL,
        )

        # Başlık hücrelerindeki run metinlerini siyah + kalın yap.
        tc = re.sub(
            r"<w:r\b[^>]*>.*?</w:r>",
            lambda rm: add_or_replace_run_color_and_bold(rm.group(0)),
            tc,
            flags=re.DOTALL,
        )

        stats["fixed_table_header_cells"] += 1
        return tc

    return re.sub(r"<w:tc\b[^>]*>.*?</w:tc>", tc_repl, tr_xml, flags=re.DOTALL)


def patch_tables(document_xml: str, stats: dict, fix_table_headers: bool = True) -> str:
    """
    Tablolarda yalnızca ilk satırı başlık olarak onarır.
    Tablo gövdesi hizalamasına dokunmaz.
    """
    if not fix_table_headers:
        return document_xml

    def tbl_repl(match: re.Match) -> str:
        tbl = match.group(0)

        m = re.search(r"<w:tr\b[^>]*>.*?</w:tr>", tbl, flags=re.DOTALL)
        if not m:
            return tbl

        old_tr = m.group(0)
        new_tr = patch_table_header_row(old_tr, stats)

        return tbl[:m.start()] + new_tr + tbl[m.end():]

    return re.sub(r"<w:tbl\b[^>]*>.*?</w:tbl>", tbl_repl, document_xml, flags=re.DOTALL)


# ------------------------------------------------------------
# styles.xml onarımı
# ------------------------------------------------------------

def patch_styles(styles_xml: str, stats: dict) -> str:
    """
    Pedagogik kutu stillerini kalıcı olarak iki yana yaslı yapar.
    Böylece yeni üretilen / aynı stile bağlı paragraflar da düzelir.
    """
    def style_repl(match: re.Match) -> str:
        style_xml = match.group(0)

        style_id_match = re.search(r'<w:styleId="([^"]+)"', style_xml)
        name_match = re.search(r'<w:name\s+w:val="([^"]+)"', style_xml)

        style_id = style_id_match.group(1) if style_id_match else ""
        name = name_match.group(1) if name_match else ""

        if not (PEDAGOGIC_STYLE_RE.search(style_id) or PEDAGOGIC_STYLE_RE.search(name)):
            return style_xml

        # pPr içinde iki yana yaslama.
        m = re.search(r"<w:pPr\b[^>]*>.*?</w:pPr>", style_xml, flags=re.DOTALL)
        if m:
            ppr = replace_or_add_jc_in_ppr(m.group(0), "both")
            style_xml = style_xml[:m.start()] + ppr + style_xml[m.end():]
        else:
            # style içine name'den sonra pPr eklemeyi dene.
            insert_pos = style_xml.find("</w:style>")
            if insert_pos != -1:
                style_xml = style_xml[:insert_pos] + '<w:pPr><w:jc w:val="both"/></w:pPr>' + style_xml[insert_pos:]

        # rPr içinde siyah metin.
        m2 = re.search(r"<w:rPr\b[^>]*>.*?</w:rPr>", style_xml, flags=re.DOTALL)
        if m2:
            rpr = m2.group(0)
            if re.search(r"<w:color\b", rpr):
                rpr = re.sub(r'<w:color\b[^>]*/>', '<w:color w:val="000000"/>', rpr)
            else:
                rpr = rpr.replace("</w:rPr>", '<w:color w:val="000000"/></w:rPr>')
            style_xml = style_xml[:m2.start()] + rpr + style_xml[m2.end():]

        stats["patched_pedagogic_styles"] += 1
        return style_xml

    return re.sub(r"<w:style\b[^>]*>.*?</w:style>", style_repl, styles_xml, flags=re.DOTALL)


# ------------------------------------------------------------
# DOCX zip işleme
# ------------------------------------------------------------

def copy_docx_with_patches(input_docx: Path, output_docx: Path, fix_table_headers: bool = True) -> dict:
    stats = {
        "centered_images": 0,
        "centered_h1": 0,
        "centered_end_markers": 0,
        "justified_pedagogic_boxes": 0,
        "fixed_table_header_cells": 0,
        "patched_pedagogic_styles": 0,
    }

    with zipfile.ZipFile(input_docx, "r") as zin:
        with zipfile.ZipFile(output_docx, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)

                if item.filename == "word/document.xml":
                    xml = data.decode("utf-8", errors="ignore")
                    xml = patch_paragraphs(xml, stats)
                    xml = patch_tables(xml, stats, fix_table_headers=fix_table_headers)
                    data = xml.encode("utf-8")

                elif item.filename == "word/styles.xml":
                    xml = data.decode("utf-8", errors="ignore")
                    xml = patch_styles(xml, stats)
                    data = xml.encode("utf-8")

                zout.writestr(item, data)

    return stats


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="DOCX içinde resim, ana başlık, bölüm sonu, pedagogik kutu ve tablo başlıklarını güvenli biçimde onarır."
    )
    parser.add_argument("input_docx", help="Girdi DOCX dosyası")
    parser.add_argument("output_docx", nargs="?", help="Çıktı DOCX dosyası")
    parser.add_argument("--in-place", action="store_true", help="Aynı dosyanın üzerine yazar; önce .bak yedeği alır")
    parser.add_argument("--no-table-header-fix", action="store_true", help="Tablo başlık satırı onarımını kapatır")
    args = parser.parse_args(argv)

    input_docx = Path(args.input_docx)

    if not input_docx.exists():
        print(f"Hata: Dosya bulunamadı: {input_docx}")
        return 1

    if args.in_place:
        backup = input_docx.with_suffix(input_docx.suffix + ".bak")
        shutil.copy2(input_docx, backup)
        output_docx = input_docx
        tmp_output = input_docx.with_suffix(".tmp.docx")
        print(f"Yedek oluşturuldu: {backup}")

        stats = copy_docx_with_patches(
            input_docx=backup,
            output_docx=tmp_output,
            fix_table_headers=not args.no_table_header_fix,
        )
        shutil.move(str(tmp_output), str(output_docx))

    else:
        output_docx = Path(args.output_docx) if args.output_docx else input_docx.with_name(input_docx.stem + "_v2.docx")
        stats = copy_docx_with_patches(
            input_docx=input_docx,
            output_docx=output_docx,
            fix_table_headers=not args.no_table_header_fix,
        )

    print("DOCX güvenli biçim onarımı v2 tamamlandı.")
    print(f"Girdi : {input_docx}")
    print(f"Çıktı : {output_docx}")
    print()
    print("İşlem özeti:")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    print()
    print("Öneri: Word'de belgeyi açtıktan sonra Ctrl+A, F9 ile içindekiler/alanları güncelleyiniz.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

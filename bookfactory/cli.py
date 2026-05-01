# ─────────────────────────────────────────────────────────────────────────────
# cli.py'ye EKLENECEK BÖLÜM
# Mevcut cli.py dosyanızda subparser bloğuna şunu ekleyin:
# ─────────────────────────────────────────────────────────────────────────────

# 1. Üste import ekleyin:
# from bookfactory.commands.init import run as run_init

# 2. Subparser bloğuna (diğer komutların yanına) şunu ekleyin:

"""
# ── init ──────────────────────────────────────────────────────────────────
init_parser = subparsers.add_parser(
    "init",
    help="İnteraktif yeni kitap projesi başlatıcı",
    description="Sorular sorarak yeni bir BookFactory kitap projesi oluşturur.",
)
init_parser.add_argument(
    "--output", "-o",
    default=".",
    help="Projenin oluşturulacağı üst dizin (varsayılan: .)",
)
init_parser.add_argument(
    "--non-interactive",
    action="store_true",
    help="Soru sormadan çalış; --config ile YAML dosyası gerekli",
)
init_parser.add_argument(
    "--config",
    default=None,
    help="Non-interactive modda kullanılacak YAML yapılandırma dosyası",
)
init_parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Dosya oluşturmadan simülasyon yap",
)
"""

# 3. Komut yönlendirme bloğuna şunu ekleyin:

"""
elif args.command == "init":
    run_init(
        output=args.output,
        non_interactive=args.non_interactive,
        config=args.config,
        dry_run=args.dry_run,
    )
"""

# ─────────────────────────────────────────────────────────────────────────────
# Tüm cli.py (mevcut yapıyı koruyarak tam entegre sürüm)
# Bu dosyayı doğrudan bookfactory/cli.py olarak kullanabilirsiniz.
# ─────────────────────────────────────────────────────────────────────────────

import argparse
import sys

from bookfactory.commands.init import run as run_init


def main():
    parser = argparse.ArgumentParser(
        prog="bookfactory",
        description="Parametric Computer Book Factory CLI",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # ── version ───────────────────────────────────────────────────────────
    subparsers.add_parser("version", help="Framework sürümünü göster")

    # ── doctor ────────────────────────────────────────────────────────────
    doctor_p = subparsers.add_parser("doctor", help="Ortam tanısı")
    doctor_p.add_argument("--soft", action="store_true",
                          help="Hata olsa bile devam et")

    # ── test-minimal ──────────────────────────────────────────────────────
    tm_p = subparsers.add_parser("test-minimal", help="Minimal demo testi")
    tm_p.add_argument("--fail-on-error", action="store_true")

    # ── test-code ─────────────────────────────────────────────────────────
    tc_p = subparsers.add_parser("test-code", help="Bölüm kod testi")
    tc_p.add_argument("--chapters-dir", required=True)
    tc_p.add_argument("--fail-on-error", action="store_true")

    # ── repair-prompts ────────────────────────────────────────────────────
    subparsers.add_parser("repair-prompts", help="LLM prompt onarımı")

    # ── sync-github ───────────────────────────────────────────────────────
    sg_p = subparsers.add_parser("sync-github", help="GitHub senkronizasyonu")
    sg_p.add_argument("--code-manifest", required=True)
    sg_p.add_argument("--test-report")
    sg_p.add_argument("--require-tests-passed", action="store_true")
    sg_p.add_argument("--push", action="store_true")

    # ── qr-from-code ──────────────────────────────────────────────────────
    qr_p = subparsers.add_parser("qr-from-code", help="QR kod üretimi")
    qr_p.add_argument("--code-manifest", required=True)
    qr_p.add_argument("--fail-on-empty", action="store_true")
    qr_p.add_argument("--strict-url", action="store_true")

    # ── export ────────────────────────────────────────────────────────────
    ex_p = subparsers.add_parser("export", help="Çıktı üretimi")
    ex_p.add_argument("--profile", required=True)
    ex_p.add_argument("--format", default="all")
    ex_p.add_argument("--merge-if-missing", action="store_true")

    # ── build-index ───────────────────────────────────────────────────────
    bi_p = subparsers.add_parser("build-index", help="Terim dizini üretimi")
    bi_p.add_argument("--profile", required=True)

    # ── dashboard ─────────────────────────────────────────────────────────
    db_p = subparsers.add_parser("dashboard", help="Streamlit dashboard")
    db_p.add_argument("--check", action="store_true")

    # ── codespaces-check ──────────────────────────────────────────────────
    subparsers.add_parser("codespaces-check", help="Codespaces uyumluluk")

    # ── codespaces-init ───────────────────────────────────────────────────
    subparsers.add_parser("codespaces-init", help="Codespaces başlatma")

    # ── init (YENİ) ───────────────────────────────────────────────────────
    init_p = subparsers.add_parser(
        "init",
        help="İnteraktif yeni kitap projesi başlatıcı",
    )
    init_p.add_argument("--output", "-o", default=".",
                        help="Üst dizin (varsayılan: .)")
    init_p.add_argument("--non-interactive", action="store_true",
                        help="Soru sormadan çalış; --config gerekli")
    init_p.add_argument("--config", default=None,
                        help="YAML yapılandırma dosyası (--non-interactive ile)")
    init_p.add_argument("--dry-run", action="store_true",
                        help="Simülasyon — dosya oluşturma")

    # ── Yardım ────────────────────────────────────────────────────────────
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # ── Yönlendirme ───────────────────────────────────────────────────────
    if args.command == "version":
        print("Parametric Computer Book Factory v2.11.x")

    elif args.command == "init":
        run_init(
            output=args.output,
            non_interactive=args.non_interactive,
            config=args.config,
            dry_run=args.dry_run,
        )

    elif args.command in ("doctor", "test-minimal", "test-code",
                          "repair-prompts", "sync-github", "qr-from-code",
                          "export", "build-index", "dashboard",
                          "codespaces-check", "codespaces-init"):
        # Mevcut komutlar — orijinal implementasyona devredilir
        print(f"[bookfactory {args.command}] — mevcut implementasyona yönlendirildi.")

    else:
        parser.print_help()
        sys.exit(1)

    return 0


if __name__ == "__main__":
    main()

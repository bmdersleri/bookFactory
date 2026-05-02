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
import importlib.util
import sys
from pathlib import Path

def _dispatch_sync_github() -> None:
    """Called before argparse when sys.argv[1] == 'sync-github'."""
    _bf_root = Path(__file__).resolve().parent.parent
    if str(_bf_root) not in sys.path:
        sys.path.insert(0, str(_bf_root))
    _script = _bf_root / "tools/github/sync_code_repository.py"
    _spec = importlib.util.spec_from_file_location("sync_code_repository", _script)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    raise SystemExit(_mod.main(sys.argv[2:]))


def _dispatch_export() -> None:
    """Called before argparse when sys.argv[1] == 'export'."""
    _bf_root = Path(__file__).resolve().parent.parent
    if str(_bf_root) not in sys.path:
        sys.path.insert(0, str(_bf_root))
    _script = _bf_root / "tools/export/export_book.py"
    _spec = importlib.util.spec_from_file_location("export_book", _script)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    raise SystemExit(_mod.main(sys.argv[2:]))


def _dispatch_qr_from_code() -> None:
    """Called before argparse when sys.argv[1] == 'qr-from-code'."""
    _bf_root = Path(__file__).resolve().parent.parent
    if str(_bf_root) not in sys.path:
        sys.path.insert(0, str(_bf_root))
    _script = _bf_root / "tools/postproduction/build_qr_manifest_from_code_manifest.py"
    _spec = importlib.util.spec_from_file_location("build_qr_manifest_from_code_manifest", _script)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    _argv = list(sys.argv[2:])
    if "--output" not in _argv:
        _argv += ["--output", "build/qr_manifest.yaml"]
    raise SystemExit(_mod.main(_argv))


def main(argv: list[str] | None = None):
    command_args = sys.argv[1:] if argv is None else list(argv)
    if command_args and command_args[0] != "init":
        from bookfactory._cli import main as orchestrator_main

        return orchestrator_main(command_args)

    if len(sys.argv) >= 2 and sys.argv[1] == "sync-github":
        _dispatch_sync_github()
    if len(sys.argv) >= 2 and sys.argv[1] == "qr-from-code":
        _dispatch_qr_from_code()
    if len(sys.argv) >= 2 and sys.argv[1] == "export":
        _dispatch_export()
    if len(sys.argv) >= 2 and sys.argv[1] == "build-index":
        _bf_root = Path(__file__).resolve().parent.parent
        if str(_bf_root) not in sys.path:
            sys.path.insert(0, str(_bf_root))
        _spec = importlib.util.spec_from_file_location(
            "build_glossary_index",
            _bf_root / "tools/indexing/build_glossary_index.py"
        )
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        raise SystemExit(_mod.main(sys.argv[2:]))

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
    subparsers.add_parser("sync-github", help="GitHub senkronizasyonu")

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
    if not command_args:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args(command_args)

    # ── Yönlendirme ───────────────────────────────────────────────────────
    if args.command == "version":
        print("Parametric Computer Book Factory v2.11.x")

    elif args.command == "init":
        from bookfactory.commands.init import run as run_init

        run_init(
            output=args.output,
            non_interactive=args.non_interactive,
            config=args.config,
            dry_run=args.dry_run,
        )

    elif args.command in ("doctor", "test-minimal", "test-code",
                          "repair-prompts", "qr-from-code",
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

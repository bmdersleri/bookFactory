# Meta Block Examples

## CODE_META — compile_run_assert

```markdown
<!-- CODE_META
id: decision_structures_code01
chapter_id: decision_structures
language: java
kind: example
title_key: "basic_if_usage"
file: "BasicIfExample.java"
extract: true
test: compile_run_assert
main_class: BasicIfExample
expected_stdout_contains:
  - "Geçti"
timeout_sec: 5
github: true
qr: dual
-->
```

## CODE_META — input kullanan örnek

```markdown
<!-- CODE_META
id: scanner_code01
chapter_id: scanner_input
language: java
kind: example
title_key: "scanner_name_input"
file: "ScannerNameInput.java"
extract: true
test: compile_run_assert
main_class: ScannerNameInput
stdin: |
  Ayşe
expected_stdout_contains:
  - "Merhaba Ayşe"
timeout_sec: 5
github: true
qr: dual
-->
```

## DIAGRAM_META

```markdown
<!-- DIAGRAM_META
id: decision_structures_diagram01
chapter_id: decision_structures
type: mermaid
title_key: decision_flow
auto_path: assets/auto/diagrams/decision_structures_diagram01.png
manual_path: assets/manual/diagrams/decision_structures_diagram01.png
final_path: assets/final/diagrams/decision_structures_diagram01.png
manual_override: true
width_cm: 12.5
-->
```

# Output Format Standard — Genel Çıktı Format Standardı

## Temel ilke

- Çıktı Pandoc/DOCX uyumlu Markdown olmalıdır.
- Başlıklar manuel numaralandırılmamalıdır.
- Otomasyon meta blokları HTML yorumları biçiminde verilmelidir.
- Dosya yolları İngilizce ve slug uyumlu olmalıdır.

## YAML front matter

```yaml
---
title: "Decision Structures: if, else-if and switch"
chapter_id: "decision_structures"
content_language: "en"
numbering_policy: "build_time"
automation_profile: "parametric_computer_book_factory_v2_0"
---
```

## Başlıklar

Doğru:

```markdown
# Decision Structures: if, else-if and switch

## Chapter roadmap
```

Yanlış:

```markdown
# Chapter 8: Decision Structures

## 8.1 Chapter roadmap
```

## CODE_META

```markdown
<!-- CODE_META
id: decision_structures_code01
chapter_id: decision_structures
language: java
kind: example
title_key: basic_if_usage
file: BasicIfExample.java
extract: true
test: compile
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

## SCREENSHOT_META

```markdown
<!-- SCREENSHOT_META
id: react_components_screenshot01
chapter_id: react_components
title_key: component_preview
route: /__book__/react_components/demo01
waitFor: "#app"
actions: []
output: assets/auto/screenshots/react_components_screenshot01.png
manual_path: assets/manual/screenshots/react_components_screenshot01.png
final_path: assets/final/screenshots/react_components_screenshot01.png
manual_override: true
-->
```

## Bölüm sonu

Bölüm sonunda elle `END OF CHAPTER`, `BÖLÜM SONU` gibi ifadeler yazılmaz. Bu etiket build veya style filter aşamasında üretilebilir.

# Approval Gate Policy — Parametrik Onay Kapısı Politikası

Onay kapıları sabit değildir. Her kitap manifestte kendi onay akışını tanımlar.

## Örnek

```yaml
approval_gates:
  manifest_validation:
    required: true
    actor: "human_or_llm"
    stop_on_failure: true
  outline_review:
    required: true
    actor: "human_or_llm"
    allowed_decisions: ["PASS", "REVISION_REQUIRED", "BLOCKED"]
    stop_on_blocked: true
  full_text_generation:
    required: true
    actor: "human"
    requires_previous_gate: "outline_review:PASS"
```

## Actor değerleri

| Actor | Anlam |
|---|---|
| `llm` | LLM kendisi yürütebilir |
| `human` | Kullanıcı onayı zorunlu |
| `human_or_llm` | LLM kontrol eder; kullanıcı isterse onaylar |
| `automated_tool` | Pipeline aracı yürütür |

# Parametric Computer Book Factory — LLM Project Brief (Index)

**Framework sürümü:** v2.11.x  
**Belge dili:** Türkçe | Teknik dosya adları: İngilizce  
**Aktif kitap bağlamı:** React ile Web Uygulama Geliştirme  
**Aktif çalışma alanı:** `workspace/react/`  
**Ana kümülatif uygulama:** KampüsHub  
**Yazar:** Prof. Dr. İsmail KIRBAŞ

---

## Bu dosya ne işe yarar?

Bu dosya bir **router/index**'tir. İçeriği kendisi taşımaz; hangi modülün ne zaman yükleneceğini gösterir. Tüm brief içeriği aşağıdaki 7 modül dosyasına bölünmüştür.

---

## Modül haritası

| Dosya | İçerik | Ne zaman yükle |
|---|---|---|
| [`brief_core.md`](brief_core.md) | Projenin ne olduğu, temel ilkeler, hedefler | Her oturumda — ilk yükle |
| [`brief_llm_rules.md`](brief_llm_rules.md) | LLM rolleri, yapması/yapmaması gerekenler, hata davranışı | Her oturumda — ikinci yükle |
| [`brief_structure.md`](brief_structure.md) | Klasör yapısı, `core/`, `workspace/`, `docs/`, `tools/`, `assets/` | Dosya/klasör işlemi yapılacaksa |
| [`brief_standards.md`](brief_standards.md) | CODE_META, screenshot, Mermaid, QR/GitHub, başlık, temizlik politikaları | Bölüm üretimi veya kod işlemi yapılacaksa |
| [`brief_react_context.md`](brief_react_context.md) | React kitabı bağlamı, kapsam, bölüm akışı, Bölüm 2 geçiş kontrolleri | React kitabıyla çalışılacaksa |
| [`brief_environment.md`](brief_environment.md) | PowerShell 7, UTF-8, VS Code, Dev Container, Codespaces | Ortam kurulumu veya Windows sorunu varsa |
| [`brief_loading_order.md`](brief_loading_order.md) | Dosya yükleme sırası, iş akışı, onay kapıları, kalite kararları | Üretim aşaması planlanırken |

---

## Minimum başlangıç komutu

```
Aşağıdaki dosyalar Parametric Computer Book Factory v2.11.x çerçevesine aittir.

Önce `brief_core.md`, ardından `brief_llm_rules.md` dosyasını oku.
Aktif kitap bağlamı için `brief_react_context.md` dosyasını yükle.
Bölüm üretimi yapacaksan `brief_standards.md` ve `brief_loading_order.md` dosyalarını da oku.

Manifesti doğrula. Eksik veya çelişkili alan varsa üretime geçmeden raporla.
```

---

## Hızlı senaryo rehberi

**Yeni oturum başlıyorum, ne yükleyeyim?**
→ `brief_core.md` + `brief_llm_rules.md` + `brief_react_context.md`

**Bölüm üretimi yapacağım:**
→ Yukarıdakilere ek: `brief_standards.md` + `brief_loading_order.md`

**Ortam sorunu yaşıyorum (PowerShell, UTF-8, Codespaces):**
→ `brief_environment.md`

**Klasör/dosya yapısını anlamak istiyorum:**
→ `brief_structure.md`

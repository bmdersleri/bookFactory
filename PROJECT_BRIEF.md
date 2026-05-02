# 📑 BookFactory v4.1.0: LLM-to-LLM Master Brief
**Subject:** Parametric Technical Publishing Framework & Engineering Pipeline
**Core Philosophy:** "Books as Code" (Manifest-Driven Development)

## 1. Project Identity & Vision
BookFactory is not just a text generator; it is a **Technical Verticalization** pipeline designed to produce high-quality, academically rigorous, and industrially relevant technical books. 

- **Single Source of Truth:** Every decision (structure, style, datasets, code rules) is derived from `book_manifest.yaml`.
- **Modular SOA Architecture:** Business logic is decoupled into specialized services (Manifest, Path, Health, Prompt, Asset, Code, Cloud).
- **Engineering Quality:** Includes automated code extraction, multi-agent peer review (Writer vs. Editor), and semantic consistency audits.

## 2. Technical Stack
- **Backend:** Python 3.10+ with FastAPI (The Studio).
- **Frontend:** Pure JS/HTML5 (Single Page App) for real-time orchestrating.
- **Publishing Engine:** Pandoc (PDF/Docx), MkDocs (Digital Twin/Web), Just-the-Docs (GitHub Pages).
- **Intelligence:** Adaptive Fragment-based Prompt Assembly + RAG (ChromaDB).
- **Ecosystem:** GitHub Codespaces & GitHub Actions (Cloud-Native).

## 3. The Manifest Model (`book_manifest.yaml`)
LLMs must strictly follow this schema:
- **`book`**: Metadata (title, author, edition).
- **`authoring`**: **Adaptive Intelligence** settings (Complexity: Novice/Expert, Context: Academic/Enterprise, Coding: snake_case/Strict).
- **`structure`**: Ordered chapters with `id`, `title`, and `status`.
- **`resources`**: External datasets, documentation, or links.
- **`academic`**: Course codes and pedagogical mapping (Bloom’s Taxonomy).

## 4. Key Verticalization Features (v4.0+)
- **Digital Twin:** Automatic transformation of markdown chapters into a professional MkDocs site.
- **Interactive Sandbox:** Auto-generating Google Colab/Wokwi links from code metadata.
- **Comparison Mode:** Side-by-side code blocks for multi-language or version comparisons.
- **Smart Layout:** Intelligent QR code placement for code snippets > 15 lines.
- **Semantic Audit:** RAG-based check to ensure Chapter 10 doesn't contradict Chapter 2.

## 5. Directory Structure at a Glance
```text
/bookfactory_studio/services/   # Decoupled business logic (SOA)
/core/fragments/                # Reusable prompt blocks for Adaptive Engine
/tools/quality/                 # Alignment check & dual-agent review tools
/tools/github/                  # GitHub Pages & Sync automation
/templates/cloud/               # .devcontainer & GitHub Actions blueprints
/schemas/                       # JSON Schemas for Manifest & Code Metadata
/docs/                          # Deep technical documentation
```

## 6. How to Interact with BookFactory (For LLMs)
If you are asked to "Write a chapter" for this project:
1.  **Read the Manifest:** Understand the `authoring` constraints.
2.  **Use CODE_META Blocks:** Always wrap code in HTML comment metadata:
    ```markdown
    <!-- CODE_META
    id: example_01
    language: python
    file: main.py
    test: pytest
    sandbox_link: true
    -->
    ```
3.  **Follow Bloom's Taxonomy:** Structure prose as: Introduction -> Theory -> Application -> Analysis -> Synthesis.
4.  **Surgical Precision:** Do not rewrite human prose; only replace specific logic blocks using regex-friendly markers.

## 7. Current Milestone: v4.1.0 Cloud-Native
The project is now fully integrated with the GitHub ecosystem. It supports one-click provisioning for **Codespaces** development and automated **GitHub Pages** deployment via Actions.

---

### **Quick Command References for LLM Agents:**
- `bookfactory init`: Scaffold a new project.
- `bookfactory validate`: Audit manifest against JSON schema.
- `bookfactory-studio`: Launch the interactive Command Center.
- `tools/export/generate_web_site.py`: Build the Digital Twin.

**End of Brief.**

## 8. Testing & Validation Strategy
BookFactory employs a multi-layered testing approach to ensure both framework integrity and book content quality.

### 8.1 Framework Testing (Infrastructure)
- **CLI Smoke Tests:** `pytest tests/test_cli_smoke.py` validates core command execution.
- **Studio API Tests:** `pytest tests/test_studio_gui.py` ensures FastAPI endpoints and job orchestrators are functional.
- **Service Layer Tests:** Individual logic in `bookfactory_studio/services/` is unit-tested for manifest IO and path safety.

### 8.2 Content & Code Validation (The Book)
- **Manifest Validation:** `bookfactory validate --manifest manifests/book_manifest.yaml` checks for schema compliance and broken file references.
- **Code Block Extraction & Testing:** The framework automatically extracts code from Markdown `CODE_META` blocks and runs them against specified test runners (pytest, node, etc.):
  ```bash
  bookfactory-studio --step test_code --root .
  ```
- **Alignment Audit:** `tools/quality/alignment_check.py` uses LLM/RAG to detect technical contradictions between the prose and the code snippets.
- **Visual Validation:** Studio's "Control Panel" provides a heatmap and matrix for manual/semi-automated verification of screenshots and quality reports.

### 8.3 Continuous Integration (CI)
- **GitHub Actions (`validate_book.yml`):** Automatically triggered on every push to validate:
  1. Manifest integrity.
  2. Code block executability.
  3. Digital Twin build success.
- **Production Quality Gate:** The `full_production` pipeline step in Studio enforces all quality gates before allowing final PDF/Docx exports.

### 8.4 How to Run Tests
- **Run All Framework Tests:** `pytest`
- **Validate Current Book:** `bookfactory-studio --step validate_manifest`
- **Test All Snippets in Book:** `bookfactory-studio --step test_code`
- **Generate Quality Report:** `bookfactory-studio --step quality_check`

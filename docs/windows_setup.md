# Windows Setup Notes

## Python

Python 3.11+ önerilir.

```bat
python --version
pip install -r requirements.txt
```

## Pandoc

Pandoc kurulduktan sonra:

```bat
pandoc --version
```

## Mermaid CLI

Node.js kurulduktan sonra:

```bat
npm install -g @mermaid-js/mermaid-cli
mmdc --version
```

## Java

```bat
java -version
javac -version
```

## Ortam kontrolü

```bat
python tools\check_environment.py --soft
```

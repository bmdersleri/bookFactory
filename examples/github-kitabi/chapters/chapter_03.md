# 3. GitHub: Bulut Tabanlı İşbirliği

Yerel depomuzdaki çalışmaları dünyaya açma ve diğer geliştiricilerle paylaşma vaktimiz geldi. GitHub, Git depoları için en popüler barındırma servisidir.

## 3.1. Uzak Depo (Remote) Bağlantısı

GitHub üzerinde bir depo oluşturduktan sonra, yerel depomuzu bu uzak depoya bağlamamız gerekir.

<!-- CODE_META
id: git_remote_add
chapter_id: chapter_03
language: shell
file: remote_setup.sh
test: compile_run
-->

```shell
git remote add origin https://github.com/kullanici/proje.git
```

## 3.2. Veri Gönderme (Push)

Değişiklikleri GitHub'a göndermek için `push` komutu kullanılır.

<!-- CODE_META
id: git_push_main
chapter_id: chapter_03
language: shell
file: push_code.sh
test: compile_run
-->

```shell
git push -u origin main
```

## 3.3. GitHub Actions ile Otomasyon Testi

Kitabımız için özel bir test senaryosu hazırlayalım. Aşağıdaki Python kodu, projenin metadata yapısının doğruluğunu basitçe simüle eder.

<!-- CODE_META
id: project_meta_test
chapter_id: chapter_03
language: python
file: test_meta.py
test: pytest
-->

```python
import sys

def test_version_format():
    version = "1.0.0"
    parts = version.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)

if __name__ == "__main__":
    test_version_format()
    print("Meta doğrulama testi başarılı.")
```

## 3.4. Pull Request Kavramı

İşbirliğinin en güçlü yönü, başkalarının kodlarını inceleyip ana projeye dahil edilmesini sağlamaktır. GitHub arayüzü üzerinden yapılan bu sürece "Pull Request" denir.

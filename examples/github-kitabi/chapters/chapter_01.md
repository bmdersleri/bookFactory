# 1. Versiyon Kontrol Sistemlerine Giriş

Bu bölümde, modern yazılım geliştirme süreçlerinin kalbinde yer alan Versiyon Kontrol Sistemleri'nin (VCS) ne olduğunu, neden gerekli olduğunu ve tarihsel gelişimini inceleyeceğiz.

## 1.1. Versiyon Kontrolü Nedir?

Versiyon kontrolü, bir dosya veya dosya kümesi üzerinde zaman içinde yapılan değişiklikleri kaydeden ve belirli bir geçmiş sürüme geri dönebilmenizi sağlayan bir sistemdir.

### Temel Faydaları:
- **Geri Alabilme:** Hatalı bir değişiklik yapıldığında önceki çalışan sürüme dönmek.
- **Takip Edilebilirlik:** Kimin, ne zaman ve neden bir değişiklik yaptığını görmek.
- **İşbirliği:** Birden fazla geliştiricinin aynı proje üzerinde çakışmadan çalışabilmesi.

## 1.2. Merkezi vs. Dağıtık Sistemler

### Merkezi Versiyon Kontrol Sistemleri (CVCS)
Subversion (SVN) gibi sistemlerde tüm geçmiş tek bir sunucuda tutulur. Sunucu çökerse işbirliği durur.

### Dağıtık Versiyon Kontrol Sistemleri (DVCS)
Git gibi sistemlerde, her geliştiricinin bilgisayarında projenin tüm geçmişinin tam bir kopyası (clone) bulunur.

<!-- CODE_META
id: check_git_version
chapter_id: chapter_01
language: shell
file: check_git.sh
test: compile_run
-->

```shell
# Git'in yüklü olup olmadığını kontrol edelim
git --version
```

## 1.4. Teknik Doğrulama

<!-- CODE_META
id: python_smoke_test
chapter_id: chapter_01
language: python
file: smoke_test.py
test: compile_run
-->

```python
import os
print("Sistem çalışıyor.")
```

Versiyon kontrolü artık bir tercih değil, profesyonel yazılım mühendisliğinin temel bir gereksinimidir. Bir sonraki bölümde bu sistemlerin en güçlü temsilcisi olan Git'in temellerini öğreneceğiz.

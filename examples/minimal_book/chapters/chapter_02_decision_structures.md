---
chapter_id: "decision_structures"
title: "Karar Yapılarına Kısa Bakış"
---

# Karar Yapılarına Kısa Bakış

## Bölümün yol haritası

Bu demo bölüm, `if` ve `else` yapılarının temel kullanımını gösterir.

## Kod örneği

<!-- CODE_META
id: decision_structures_code01
chapter_id: decision_structures
language: java
kind: example
title_key: "basic_if_example"
file: "BasicIfExample.java"
extract: true
test: compile_run_assert
github: true
qr: dual
expected_stdout_contains:
  - "Geçti"
timeout_sec: 5
-->

```java
// File: BasicIfExample.java
public class BasicIfExample {
    public static void main(String[] args) {
        int score = 75;

        if (score >= 60) {
            System.out.println("Geçti");
        } else {
            System.out.println("Kaldı");
        }
    }
}
```

## Bölüm özeti

Karar yapıları programın farklı koşullara göre farklı yollar izlemesini sağlar.


## Terim sözlüğü

| Terim | Açıklama |
|---|---|
| if | Bir koşul doğru olduğunda belirli kod bloğunu çalıştıran karar yapısı. |
| else | if koşulu sağlanmadığında çalıştırılan alternatif kod bloğu. |
| koşul | Program akışını belirleyen doğru/yanlış değerli ifade. |

# 2. Git Temelleri ve Yerel Depo Yönetimi

Git dünyasına ilk adımımızı atıyoruz. Bu bölümde yerel bir depo oluşturmayı, dosyaları takip etmeyi ve ilk "commit" işlemini gerçekleştirmeyi öğreneceğiz.

## 2.1. Kimlik Ayarları

Git'i ilk kez kullanırken, yaptığınız değişikliklerin kime ait olduğunu belirtmeniz gerekir.

<!-- CODE_META
id: git_config
chapter_id: chapter_02
language: shell
file: setup_git.sh
test: compile_run
-->

```shell
git config --global user.name "İsmail KIRBAŞ"
git config --global user.email "ismail@example.com"
```

## 2.2. Proje Başlatma (git init)

Yeni bir proje klasörü oluşturup Git'e burayı takip etmesini söyleyelim.

<!-- CODE_META
id: git_init_example
chapter_id: chapter_02
language: shell
file: init_repo.sh
test: compile_run
-->

```shell
mkdir proje_klasoru
cd proje_klasoru
git init
```

## 2.3. Dosya Ekleme ve Commit

Dosyalarımızı "staging area" (sahne) kısmına alıp kalıcı olarak kaydetmek için `add` ve `commit` komutlarını kullanırız.

<!-- CODE_META
id: git_commit_flow
chapter_id: chapter_02
language: shell
file: first_commit.sh
test: compile_run
-->

```shell
echo "# Proje Notları" > README.md
git add README.md
git commit -m "İlk döküman eklendi"
```

## 2.4. Durum Sorgulama

Depomuzun o anki durumunu görmek için `git status` komutunu sıkça kullanacağız.

<!-- CODE_META
id: git_status_check
chapter_id: chapter_02
language: shell
file: status.sh
test: compile_run
-->

```shell
git status
```

Bu komut bize hangi dosyaların değiştiğini, hangilerinin takip edilmediğini söyler.

# 2. Git Temelleri ve Yerel Depo Yönetimi

Git, modern yazılım geliştirme dünyasının "zaman makinesi"dir. Bu bölümde, Git'in kalbine inecek, yerel bir deponun nasıl yönetileceğini, dosyaların hangi evrelerden geçtiğini ve geçmişin nasıl titizlikle kaydedileceğini öğreneceğiz. Hedefimiz sadece komutları ezberlemek değil, Git'in felsefesini kavramaktır.

## 2.1. Git Kurulumu ve Derinlemesine Yapılandırma

Git'i sisteminize kurmak ilk adımdır, ancak onu profesyonel bir iş akışına hazırlamak için doğru yapılandırma şarttır.

### 2.1.1. Kurulumun İnce Detayları
Git kurulumu sırasında karşınıza çıkan seçenekler, gelecekteki "dosya sonu karakteri" (Line Ending) krizlerini belirler:
- **Windows (CRLF):** Satır sonları `\r\n` şeklindedir.
- **Linux/macOS (LF):** Satır sonları `\n` şeklindedir.
Kurulumda "Checkout Windows-style, commit Unix-style line endings" seçeneği, farklı işletim sistemlerinde çalışan ekiplerin kodlarının bozulmasını önler.

### 2.1.2. Yapılandırma Katmanları (Hiyerarşi)
Git ayarlarını üç farklı seviyede yönetir. Her seviye bir üsttekini ezer:
1.  **System (`--system`):** Tüm kullanıcıları etkiler. Genellikle `/etc/gitconfig` dosyasındadır.
2.  **Global (`--global`):** Mevcut kullanıcı için geçerlidir. `~/.gitconfig` dosyasında saklanır.
3.  **Local (`--local`):** Sadece o anki proje (repo) için geçerlidir. `.git/config` dosyasındadır.

<!-- CODE_META
id: git_identity_config_pro
chapter_id: chapter_02
language: shell
file: config_identity.sh
test: compile_run
-->

```shell
# Temel kimlik bilgileri
git config --global user.name "Prof. Dr. İsmail KIRBAŞ"
git config --global user.email "ismail@example.com"

# Profesyonel araç entegrasyonu
git config --global core.editor "code --wait" # VS Code'u varsayılan editör yapar
git config --global merge.tool meld           # Görsel birleştirme aracı
git config --global color.ui true             # Terminal çıktılarını renklendirir

# Otomatik düzeltme (Hatalı komutları tahmin eder)
git config --global help.autocorrect 20       # 2 saniye bekleyip doğru komutu çalıştırır

# Alias (Kısayol) Tanımlama
git config --global alias.st status
git config --global alias.ci commit
git config --global alias.br branch
```

## 2.2. Yerel Depo Oluşturma: `git init` Anatomisi

Bir dizinde `git init` komutunu çalıştırdığınızda, Git orada gizli bir `.git` klasörü oluşturur. Bu klasör, projenizin tüm hafızasıdır.

### 2.2.1. Derinlemesine Bakış: .git Klasörünün İçinde Ne Var?
- **objects/:** Git'in "içerik adreslenebilir" veritabanıdır. Tüm dosyalarınızın içerikleri (blobs), ağaç yapıları (trees) ve commit'ler burada SHA-1 hash değerleriyle saklanır.
- **refs/:** Dalları (branches) ve etiketleri (tags) tutan referans dosyalarıdır.
- **HEAD:** O an hangi dalda veya commit'te olduğunuzu gösteren bir dosyadır. Genellikle `ref: refs/heads/main` içeriğine sahiptir.
- **index (Staging Area):** Bir sonraki commit'e girecek olan değişikliklerin listesini tutan ikili bir dosyadır.

## 2.3. Dosya Yaşam Döngüsü (The Git Lifecycle)

Git'te bir dosyanın dört temel durumu vardır. Bu döngüyü anlamak, "Kodum neden commit edilmedi?" sorusunun cevabıdır.

1.  **Untracked (Takip Edilmeyen):** Dosya dizinde var ama Git onu izlemiyor. `git add` yapılana kadar Git'in veritabanında yer almaz.
2.  **Unmodified (Değişmemiş):** Dosya commit edilmiş ve üzerinde yeni bir değişiklik yapılmamış.
3.  **Modified (Değiştirilmiş):** Dosya üzerinde değişiklik yapılmış ancak bu değişiklikler henüz Git'e "rezerve" edilmemiş.
4.  **Staged (Sahneye Alınmış):** Değişiklikler `git add` ile işaretlenmiş, commit edilmeye hazır bekliyor.

### 2.3.1. Staging Area (İndeks) Kavramı
Neden doğrudan commit yapmıyoruz? Staging Area, size **mikro-yönetim** şansı verir. Eğer 10 farklı dosya değiştirdiyseniz ve bunlardan 3'ü bir hata düzeltmesi, 7'si yeni bir özellik ise; önce hata düzeltmelerini `add` yapıp commit edebilir, ardından diğerlerini ayrı bir commit olarak gönderebilirsiniz. Bu, temiz bir proje geçmişi sağlar.

<!-- CODE_META
id: git_status_advanced
chapter_id: chapter_02
language: shell
file: status_check.sh
test: compile_run
-->

```shell
# Kısa ve öz durum özeti
git status -s

# Çıktı analizi:
# M  index.html  -> Staging'de değiştirilmiş (Yeşil)
#  M index.html  -> Çalışma dizininde değiştirilmiş (Kırmızı)
# ?? newfile.py  -> Takip edilmiyor
# A  test.js     -> Yeni eklendi ve Staging'de
```

## 2.4. Kusursuz Commit Sanatı

Bir commit, sadece kod değişikliği değil, bir **iletişim** aracıdır.

### 2.4.1. Atomik Commit Prensibi
Bir commit, mümkün olan en küçük, mantıksal ve test edilebilir değişikliği içermelidir. Büyük, her şeyi içeren ("Giriş ekranı bitti ve logo değişti ve SQL hatası giderildi") commit'lerden kaçının.

### 2.4.2. Conventional Commits Standartları
Profesyonel ekipler genellikle şu formatı kullanır: `<tip>(<kapsam>): <açıklama>`
- **feat:** Yeni bir özellik.
- **fix:** Bir hata düzeltmesi.
- **docs:** Sadece dökümantasyon değişikliği.
- **style:** Kodun çalışmasını etkilemeyen format değişiklikleri.

<!-- CODE_META
id: git_commit_examples
chapter_id: chapter_02
language: shell
file: commit_examples.sh
test: compile_run
-->

```shell
# Standart commit
git commit -m "feat(auth): login formuna doğrulama eklendi"

# Sahneye almayı (add) ve commit'i birleştirmek (Sadece takip edilen dosyalar için)
git commit -am "fix(ui): buton rengi düzeltildi"

# Son commit mesajını değiştirmek (Henüz push edilmemişse)
git commit --amend -m "feat(auth): login formuna gelişmiş doğrulama eklendi"
```

## 2.5. Geçmişin İzinde: `git log` ve `git show`

Proje geçmişi bir kitaba benzer. `git log` ile bu kitabın sayfalarını çevirebilirsiniz.

### 2.5.1. Log Filtreleme Teknikleri
- `git log -p -2`: Son 2 commit'teki gerçek kod farklarını (diff) gösterir.
- `git log --stat`: Hangi dosyalarda kaç satır değiştiğinin özetini verir.
- `git log --author="İsmail"`: Sadece belirli bir yazarın commit'lerini listeler.
- `git log --since="2 weeks ago"`: Son 2 haftadaki commit'leri gösterir.

<!-- CODE_META
id: git_log_magic
chapter_id: chapter_02
language: shell
file: log_magic.sh
test: compile_run
-->

```shell
# Grafiksel ve süper detaylı görünüm (Bu komutu bir alias yapmanız önerilir)
git log --graph --pretty=format:'%C(yellow)%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

## 2.6. Değişiklikleri Anlamak: `git diff` Derinlikleri

Neyi değiştirdiğinizi commit etmeden önce görmek, hataları minimize eder.
- `git diff`: Çalışma dizini ile Staging Area arasındaki fark. (Neyi değiştirdim ama henüz eklemedim?)
- `git diff --staged`: Staging Area ile son commit arasındaki fark. (Neyi ekledim ve commit etmeye hazırım?)
- `git diff HEAD`: Çalışma dizini ile son commit arasındaki tüm farklar.

## 2.7. Dosya Yönetimi: Silme ve Taşıma

Dosyaları işletim sistemi üzerinden silmek veya taşımak yerine Git komutlarını kullanmak, Git'in kafasının karışmasını önler.
- `git rm <dosya>`: Dosyayı hem diskten siler hem de silme işlemini sahneye ekler.
- `git rm --cached <dosya>`: Dosyayı diskte tutar ama Git takibinden çıkarır. (.gitignore'a eklemeyi unuttuğunuz dosyalar için idealdir).
- `git mv <eski_ad> <yeni_ad>`: Dosyayı taşır veya adını değiştirir.

## 2.8. Gerçek Dünya Senaryosu: "Yanlış Dosyayı Add Yapmak"

Senaryo: `secret.env` dosyasını yanlışlıkla `git add .` ile sahneye aldınız. Henüz commit etmediniz.
Çözüm: `git restore --staged secret.env`. Bu komut dosyayı "Staged" durumundan "Modified" veya "Untracked" durumuna geri çeker.

## 2.9. Mülakat Soruları ve Cevapları

1. **Soru:** Git'te "Snapshot" (Anlık Görüntü) mantığı nedir, fark tabanlı (delta) sistemlerden ne farkı vardır?
   **Cevap:** Git, her commit'te sadece değişen dosyaların farkını tutmak yerine, o anki tüm projenin bir resmini (pointer'lar aracılığıyla) çeker. Değişmeyen dosyalar için bir önceki versiyona link verir. Bu, dallanma ve birleştirme işlemlerini inanılmaz hızlı kılar.

2. **Soru:** `.gitignore` dosyası ne işe yarar ve hali hazırda takip edilen bir dosyayı görmezden gelebilir mi?
   **Cevap:** `.gitignore`, Git'in takip etmemesi gereken dosyaları (loglar, bağımlılıklar, şifreler) tanımlar. Ancak takip edilen bir dosya buraya eklenirse Git onu izlemeye devam eder. Onu izlemeyi bırakmak için `git rm --cached` kullanılmalıdır.

## 2.10. Bölüm Özeti ve Değerlendirme

Bu bölümde yerel bir depoda tam hakimiyet sağlamayı öğrendik.
- Yapılandırma seviyelerini ve önemini kavradık.
- `.git` klasörünün gizli dünyasına göz attık.
- Dosyaların yaşam döngüsünü (Untracked -> Staged -> Committed) içselleştirdik.
- Profesyonel commit mesajı yazma standartlarını gördük.

**Değerlendirme Soruları:**
- Bir dosyanın "Staged" olup olmadığını nasıl anlarsınız?
- `git commit --amend` hangi durumlarda kullanılmalıdır?
- Log çıktılarını tarihe ve yazara göre nasıl filtrelersiniz?

Bir sonraki bölümde, bu yerel tecrübeyi buluta taşıyacak ve GitHub ile dünyaya açılacağız!

---

### Profesyonel İpucu
Git kullanırken "küçük ve sık" commit yapın. Büyük commit'ler, hata ayıklamayı zorlaştırır ve ekip arkadaşlarınızın kodunuzu incelemesini imkansız hale getirir. Her commit bir hikaye anlatmalıdır.

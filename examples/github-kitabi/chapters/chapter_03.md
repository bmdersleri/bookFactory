# 3. GitHub: Bulut Tabanlı İşbirliği

GitHub, 2008 yılındaki kuruluşundan bu yana sadece bir kod barındırma servisi olmanın ötesine geçerek, yazılım dünyasının "sosyal ağ"ı ve standart işbirliği platformu haline gelmiştir. Bu bölümde, yerel çalışmalarımızı dünyaya nasıl açacağımızı, güvenli bağlantı yöntemlerini ve profesyonel işbirliği ekosistemini tüm detaylarıyla inceleyeceğiz.

## 3.1. GitHub Ekosistemi: Kodun Sosyal Hali

GitHub, Git versiyon kontrol sistemini temel alan ancak üzerine devasa bir işbirliği katmanı ekleyen bir platformdur.

### 3.1.1. Kurumsal ve Açık Kaynak Gücü
Bugün dünyanın en büyük açık kaynak projeleri (Linux, React, Python, TensorFlow) GitHub üzerinde geliştirilmektedir. Bir geliştirici için GitHub profili, statik bir özgeçmişten çok daha değerlidir; çünkü yazdığınız kodun kalitesini, diğer projelerle etkileşiminizi ve sorun çözme yeteneğinizi doğrudan kanıtlar.

## 3.2. Güvenli Bağlantı: Kimlik Doğrulama Mekanizmaları

GitHub ile bilgisayarınız arasındaki veri transferi şifrelenmiş olmalıdır. Modern dünyada üç ana yöntem vardır.

### 3.2.1. SSH (Secure Shell): Profesyonellerin Tercihi
SSH, bir "kamu anahtarı" (public key) ve bir "özel anahtar" (private key) çifti kullanarak çalışır. Özel anahtar bilgisayarınızda kalırken, kamu anahtarını GitHub'a verirsiniz.

<!-- CODE_META
id: ssh_key_management_advanced
chapter_id: chapter_03
language: shell
file: lab_ssh_advanced.sh
test: compile_run
-->

```shell
# 1. Yeni nesil Ed25519 anahtarı oluştur (Daha güvenli ve hızlı)
ssh-keygen -t ed25519 -C "ismail@example.com"

# 2. SSH Agent'ı başlat ve anahtarı ekle
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. Anahtarı GitHub'a eklemek için kopyala
# Windows:
cat ~/.ssh/id_ed25519.pub | clip
# macOS:
pbcopy < ~/.ssh/id_ed25519.pub

# 4. Bağlantıyı test et
ssh -T git@github.com
```

### 3.2.2. HTTPS ve Personal Access Tokens (PAT)
GitHub artık klasik şifre ile giriş yapılmasına (güvenlik nedeniyle) izin vermemektedir. HTTPS kullanıyorsanız, şifre yerine bir Token üretmeli ve onu kullanmalısınız. PAT, belirli izinlere (scopes) ve son kullanma tarihine sahip özel bir anahtardır.

## 3.3. Remote (Uzak) Sunucu Yönetimi

Uzak depolar, projenizin internet üzerindeki kopyalarıdır. Bir yerel repo, birden fazla uzak depoya sahip olabilir.

### 3.3.1. Origin vs. Upstream Kavramı
- **origin:** Kendi GitHub hesabınızdaki kopya (genellikle fork yaptıktan sonraki yeriniz).
- **upstream:** Orijinal projenin ana kaynağı.

<!-- CODE_META
id: remote_management_lab
chapter_id: chapter_03
language: shell
file: remote_ops.sh
test: compile_run
-->

```shell
# Mevcut uzak depoları gör
git remote -v

# Yeni bir uzak depo ekle
git remote add origin git@github.com:ismailkirbas/my-project.git

# Orijinal kaynağı (upstream) ekle
git remote add upstream git@github.com:original-owner/original-project.git

# Uzak depo URL'sini değiştir
git remote set-url origin git@github.com:ismailkirbas/new-url.git
```

## 3.4. Senkronizasyon: Git Veri Transferi

### 3.4.1. `git fetch` vs. `git pull` (Kritik Fark)
- **Fetch:** "Git bak bakalım bulutta ne değişmiş, onları indir ama benim koduma dokunma" demektir. Değişiklikler `origin/main` gibi dallarda tutulur.
- **Pull:** Önce `fetch` yapar, sonra gelen değişiklikleri o anki dalınızla `merge` (birleştirme) yapmaya çalışır. Riskli olabilir!

### 3.4.2. `git push` Stratejileri
Push yaparken `-u` (upstream) parametresini kullanmak, o dalı kalıcı olarak uzak dal ile eşleştirir (tracking branch).

## 3.5. İşbirliği Akışı: Fork ve Pull Request (PR) Yaşam Döngüsü

Bu, profesyonel dünyada "GitHub Flow"un temelidir.

1.  **Fork:** Başkasının projesini kendi alanınıza kopyalarsınız.
2.  **Clone:** Fork'ladığınız projeyi yerelinize indirirsiniz.
3.  **Branch:** Yeni bir özellik için dal açarsınız (`git checkout -b feature/cool-stuff`).
4.  **Commit & Push:** Değişiklikleri yapıp kendi origin'inize gönderirsiniz.
5.  **Pull Request:** Orijinal proje sahibine değişikliğinizi sunarsınız.

### 3.5.1. Pull Request'te Kod İncelemesi (Code Review)
PR açıldığında, ekip arkadaşlarınız kodunuzu satır satır inceler. Yorum yapabilir, değişiklik isteyebilir veya onaylayabilirler. Bu, yazılım kalitesini artıran en önemli aşamadır.

## 3.6. GitHub Issues ve Proje Yönetimi

### 3.6.1. Issues: Hata ve İstek Takibi
Her issue bir tartışma konusudur. Etiketler (bug, enhancement, help wanted) ve Milestones (Kilometre Taşları) ile yönetilir.
**İpucu:** Bir commit mesajında `closes #42` yazarsanız, o commit ana dal ile birleştiğinde 42 numaralı issue otomatik olarak kapatılır.

### 3.6.2. GitHub Projects (Kanban)
Trello benzeri bir kart sistemi ile işlerin (To Do, In Progress, Done) takibi sağlanır.

## 3.7. Derinlemesine Bakış: GitHub Gists ve GitHub Pages

- **Gist:** Tek bir dosyayı veya küçük kod parçacıklarını paylaşmak için kullanılır. Her Gist aslında küçük bir Git reposudur.
- **Pages:** Projenizin dökümantasyonunu veya kişisel web sitenizi ücretsiz barındırmanızı sağlar. `index.html` dosyanızı `gh-pages` dalına push etmeniz yeterlidir.

## 3.8. Gerçek Dünya Senaryosu: "Fork'ladığım Proje Güncellendi!"

Senaryo: Bir projeyi fork'ladınız, 1 hafta geçti ve orijinal proje (upstream) ilerledi. Kendi fork'unuzu nasıl güncel tutarsınız?
Çözüm:
```shell
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

## 3.9. Mülakat Soruları ve Cevapları

1. **Soru:** `git pull` ve `git fetch` arasındaki fark nedir? Hangisi daha güvenlidir?
   **Cevap:** `fetch` sadece verileri indirir, yerel dosyaları değiştirmez. `pull` ise indirir ve birleştirir. `fetch` daha güvenlidir çünkü birleştirme öncesi kodları kontrol etme şansı verir.

2. **Soru:** Bir Pull Request (PR) sürecinde "Merge Conflict" oluşursa ne yapmalısınız?
   **Cevap:** Yerelde ana dalı güncellemeli, kendi dalıma birleştirmeli, çakışmaları çözmeli ve ardından tekrar push etmeliyim. PR otomatik olarak güncellenecektir.

## 3.10. Bölüm Özeti ve Değerlendirme

Bu bölümde GitHub'ın devasa dünyasına giriş yaptık.
- SSH ile güvenli bağlantı kurmayı öğrendik.
- Uzak depoları (remote) yönetme becerisi kazandık.
- Fork ve Pull Request ile dünya çapındaki projelere nasıl katkı verebileceğimizi gördük.
- Issues ve Projects ile ekip çalışmasının temellerini attık.

**Değerlendirme Soruları:**
- SSH Key oluştururken neden Ed25519 algoritması tercih edilir?
- `origin` ve `upstream` arasındaki fark nedir?
- Bir Pull Request'i kim onaylamalıdır?

Bir sonraki bölümde, ekiplerin birbirinin ayağına basmadan nasıl çalıştığını göreceğiz: Branching ve Merging Stratejileri!

---

### Kurumsal İpucu
GitHub üzerinde çalışırken **README.md** ve **CONTRIBUTING.md** dosyalarına özen gösterin. İyi bir README projenin yüzüdür; CONTRIBUTING ise diğer geliştiricilere nasıl yardım edebileceklerini gösteren bir yol haritasıdır.

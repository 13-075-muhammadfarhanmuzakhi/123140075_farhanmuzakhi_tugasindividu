# 📤 Panduan Push ke GitHub

## Prasyarat

- Git sudah terinstall di komputer
- Sudah punya akun GitHub
- Sudah punya repository di GitHub

---

## Step-by-Step Commands

### 1. Navigate ke project folder

```bash
cd D:\.vscode\html_css_js\Pengweb\tugas3\product-review-analyzer
```

### 2. Initialize Git Repository (hanya sekali di awal)

```bash
git init
```

### 3. Add remote repository (ganti URL dengan repo Anda)

```bash
git remote add origin https://github.com/USERNAME/product-review-analyzer.git
```

**Contoh:**

```bash
git remote add origin https://github.com/myusername/product-review-analyzer.git
```

**Atau jika pakai SSH:**

```bash
git remote add origin git@github.com:USERNAME/product-review-analyzer.git
```

### 4. Verify remote sudah benar

```bash
git remote -v
```

Output seharusnya:

```
origin  https://github.com/USERNAME/product-review-analyzer.git (fetch)
origin  https://github.com/USERNAME/product-review-analyzer.git (push)
```

### 5. Check status files

```bash
git status
```

### 6. Add all files (kecuali yang di .gitignore)

```bash
git add .
```

### 7. Check status lagi untuk confirm

```bash
git status
```

Seharusnya file yang sensitive (.env, node_modules, venv) tidak ada di list.

### 8. Commit dengan message yang deskriptif

```bash
git commit -m "Initial commit: Product Review Analyzer with sentiment analysis and Gemini API integration"
```

### 9. Create/Switch to main branch

```bash
git branch -M main
```

### 10. Push ke GitHub

```bash
git push -u origin main
```

**Jika sudah pernah push, untuk push update selanjutnya:**

```bash
git push origin main
```

---

## Workflow untuk Update Selanjutnya

Setiap kali ada perubahan:

```bash
# 1. Check status
git status

# 2. Add changes
git add .

# 3. Commit
git commit -m "Deskripsi perubahan yang dibuat"

# 4. Push
git push origin main
```

---

## Troubleshooting

### Jika error "fatal: not a git repository"

```bash
# Initialize git di folder yang benar
git init
```

### Jika error saat push (rejected)

```bash
# Pull latest version dari remote terlebih dahulu
git pull origin main --rebase

# Lalu push lagi
git push origin main
```

### Jika lupa setup username/email

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Check remote URL

```bash
git remote -v
```

### Hapus remote yang salah dan tambah yang benar

```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/repo.git
```

---

## Tips

- Selalu commit dengan message yang meaningful
- Commit frequently untuk track progress
- Jangan push file sensitive (.env, node_modules, venv)
- Pastikan .gitignore sudah ada sebelum push

---

## Contoh Full Workflow

```bash
# Navigate ke project
cd D:\.vscode\html_css_js\Pengweb\tugas3\product-review-analyzer

# Setup git (first time only)
git init
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git remote add origin https://github.com/yourname/product-review-analyzer.git

# Add dan push
git add .
git commit -m "Initial commit: Product Review Analyzer"
git branch -M main
git push -u origin main

# Update selanjutnya
git add .
git commit -m "Fix: sentiment analyzer multilingual support"
git push origin main
```

---

## Verifikasi

Setelah push, cek di browser:

```
https://github.com/yourname/product-review-analyzer
```

Seharusnya semua file sudah ter-upload (kecuali yang di .gitignore)! ✅

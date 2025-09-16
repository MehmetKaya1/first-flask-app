# --- Flask + Git güvenli push scripti (UTF-8 uyumlu) ---

# 1️⃣ Flask uygulamasını kapatmayı unutma
Write-Host "Flask uygulamasini kapat! CTRL+C ile kapat."

# 2️⃣ SQLite DB dosyasını gitignore'a ekle (ilk seferde)
if (-Not (Select-String -Path ".gitignore" -Pattern "instance/items.db" -Quiet)) {
    Add-Content -Path ".gitignore" -Value "instance/items.db"
    git add .gitignore
    git commit -m "Ignore SQLite DB file"
    Write-Host "SQLite DB git takibinden cikartildi."
}

# 3️⃣ Local değişiklikleri commit et
git add .
git commit -m "Local changes" 2>$null
Write-Host "Local degisiklikler commit edildi."

# 4️⃣ Remote branch’i al ve rebase yap
git pull origin main --rebase
if ($LASTEXITCODE -ne 0) {
    Write-Host "Conflict olustu! Cakismlari coz ve 'git rebase --continue' kullan."
    exit
}

# 5️⃣ Local değişiklikleri push et
git push -u origin main
Write-Host "Push tamamlandi! Local ve remote branch eslesti."

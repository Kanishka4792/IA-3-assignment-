# Creates one public GitHub repo per folder and pushes the code (Windows PowerShell).
# Needs: git and GitHub CLI (gh), and you must be logged in (run: gh auth login)
gh auth status 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host "Run 'gh auth login' first."; exit 1 }
Get-ChildItem -Directory | ForEach-Object {
  $name = $_.Name
  Write-Host "== $name"
  Push-Location $name
  if (Test-Path .git) { Remove-Item -Recurse -Force .git }
  git init -q -b main
  git add .
  git commit -q -m "Initial commit"
  gh repo create $name --public --source=. --remote=origin --push
  Pop-Location
}
Write-Host "Done."

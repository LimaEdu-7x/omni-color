<#
Instalação em um comando: copia as skills para ~/.claude/skills. O Python 3 só é necessário para rodar o script de paleta.
Uso: .\install.ps1
#>
$ErrorActionPreference = "Stop"
$dest = Join-Path $HOME ".claude\skills"
New-Item -ItemType Directory -Force $dest | Out-Null
foreach ($s in Get-ChildItem (Join-Path $PSScriptRoot "skills") -Directory) {
  $target = Join-Path $dest $s.Name
  if ($s.Name -eq "grill-me" -and (Test-Path $target)) { Write-Host "grill-me já instalada, pulando"; continue }
  Copy-Item -Recurse -Force $s.FullName $dest
  Write-Host "skill instalada: $($s.Name)"
}
if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command python3 -ErrorAction SilentlyContinue)) {
  Write-Host "Python 3 não encontrado. A IA vai oferecer instalá-lo (winget install Python.Python.3.12) quando precisar."
}

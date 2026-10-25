@echo off
setlocal
set "IDS_ROOT=%~dp0.."
if not exist "%IDS_ROOT%\.tools\uv\uv.exe" (
    powershell -NoProfile -Command "$ErrorActionPreference = 'Stop'; $target = Join-Path $env:IDS_ROOT '.tools'; New-Item -ItemType Directory -Force -Path $target | Out-Null; $archive = Join-Path $target 'uv.zip'; Invoke-WebRequest -Uri 'https://github.com/astral-sh/uv/releases/download/0.13.5/uv-x86_64-pc-windows-msvc.zip' -OutFile $archive; Expand-Archive -LiteralPath $archive -DestinationPath (Join-Path $target 'uv') -Force"
    if errorlevel 1 exit /b 1
)
call "%~dp0uv.cmd" sync --locked
if errorlevel 1 exit /b 1
call "%~dp0uv.cmd" run --locked playwright install chromium
exit /b %ERRORLEVEL%

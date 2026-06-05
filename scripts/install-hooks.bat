@echo off
for /f %%i in ('git rev-parse --show-toplevel') do set ROOT=%%i
git config core.hooksPath .githooks
echo Hooks installed via core.hooksPath=.githooks. Active hooks:
dir /b "%ROOT%\.githooks\"

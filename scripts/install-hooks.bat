@echo off
git config core.hooksPath .githooks
echo Hooks installed (core.hooksPath=.githooks).
dir /b .githooks

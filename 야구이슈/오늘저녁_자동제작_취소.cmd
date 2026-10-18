@echo off
chcp 65001 >nul
rem 10/17 user request: cancel tonight scheduled auto build (yagu_auto_tonight)
schtasks /delete /tn "yagu_auto_tonight" /f > "%~dp0_cancel_result.txt" 2>&1
schtasks /query /tn "yagu_auto_tonight" >> "%~dp0_cancel_result.txt" 2>&1

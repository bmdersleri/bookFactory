@echo off
setlocal EnableExtensions DisableDelayedExpansion
chcp 65001 >nul

REM DOCX conversion pipeline - v2.4.1 Windows fix
REM Single Mermaid render flow:
REM   1) tools\postproduction\prepare_mermaid_images.py extracts only .mmd files
REM   2) tools\postproduction\render_mermaid_png.py creates PNG files once
REM
REM This batch file can stay under tools\postproduction\windows.
REM It resolves reference DOCX, Lua filter and Python tools from the project root.
REM
REM Usage:
REM   donustur.bat "Source.md"
REM   donustur.bat "Source.md" "Output.docx"
REM   donustur.bat "Source.md" "Output.docx" 4.90in

if "%~1"=="" goto :usage

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..\..\..") do set "PROJECT_ROOT=%%~fI"
set "MD_FILE=%~f1"

if not exist "%MD_FILE%" (
    echo [ERROR] Source Markdown file was not found:
    echo         %MD_FILE%
    exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found in PATH.
    exit /b 1
)

where pandoc >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Pandoc was not found in PATH.
    exit /b 1
)

set "MD_DIR=%~dp1"
set "MD_NAME=%~nx1"
set "MD_BASE=%~n1"
set "MERMAID_DIR=%MD_DIR%mermaid_images"

if "%~2"=="" (
    set "OUT_DOCX=%MD_DIR%%MD_BASE%.docx"
) else (
    set "OUT_DOCX=%~f2"
)

if "%~3"=="" (
    set "MERMAID_IMAGE_WIDTH=4.90in"
) else (
    set "MERMAID_IMAGE_WIDTH=%~3"
)

set "REFERENCE_DOC=%PROJECT_ROOT%\templates\reference_docs\referenceV17_java_temelleri.docx"
set "LUA_FILTER=%PROJECT_ROOT%\templates\lua_filters\styles_revised_v17.lua"
set "PREPARE_PY=%PROJECT_ROOT%\tools\postproduction\prepare_mermaid_images.py"
set "RENDER_PY=%PROJECT_ROOT%\tools\postproduction\render_mermaid_png.py"

if not exist "%REFERENCE_DOC%" (
    echo [ERROR] Reference DOCX was not found:
    echo         %REFERENCE_DOC%
    exit /b 1
)

if not exist "%LUA_FILTER%" (
    echo [ERROR] Lua filter was not found:
    echo         %LUA_FILTER%
    exit /b 1
)

if not exist "%PREPARE_PY%" (
    echo [ERROR] Mermaid prepare script was not found:
    echo         %PREPARE_PY%
    exit /b 1
)

if not exist "%RENDER_PY%" (
    echo [ERROR] Mermaid render script was not found:
    echo         %RENDER_PY%
    exit /b 1
)

echo.
echo ============================================================
echo DOCX Conversion v2.4.1 - single Mermaid PNG render
echo ============================================================
echo Source MD        : %MD_FILE%
echo Output DOCX      : %OUT_DOCX%
echo Mermaid folder   : %MERMAID_DIR%
echo Mermaid width    : %MERMAID_IMAGE_WIDTH%
echo ============================================================
echo.

if not exist "%MERMAID_DIR%" mkdir "%MERMAID_DIR%"

echo [1/3] Extracting Mermaid blocks as MMD files only...
python "%PREPARE_PY%" "%MD_FILE%" --out-dir "%MERMAID_DIR%" --clean --force
if errorlevel 1 (
    echo [ERROR] Mermaid extraction failed.
    exit /b 1
)

echo.
echo [2/3] Rendering Mermaid MMD files as PNG files once...
python "%RENDER_PY%" "%MERMAID_DIR%" --recursive --pdf-fit --force --background white
if errorlevel 1 (
    echo [ERROR] Mermaid PNG rendering failed.
    exit /b 1
)

echo.
echo [3/3] Creating DOCX with Pandoc...
pushd "%MD_DIR%"
set "MERMAID_IMAGE_WIDTH=%MERMAID_IMAGE_WIDTH%"
set "MERMAID_IMAGE_DIR=%MERMAID_DIR%"
pandoc -f markdown+tex_math_single_backslash "%MD_NAME%" -o "%OUT_DOCX%" --reference-doc="%REFERENCE_DOC%" --lua-filter="%LUA_FILTER%" --toc --toc-depth=2 --metadata=toc-title:Icindekiler
set "PANDOC_EXIT=%ERRORLEVEL%"
popd

if not "%PANDOC_EXIT%"=="0" (
    echo [ERROR] Pandoc conversion failed.
    exit /b %PANDOC_EXIT%
)

echo.
echo [OK] DOCX file created:
echo      %OUT_DOCX%
exit /b 0

:usage
echo.
echo Usage:
echo   %~nx0 "Source.md"
echo   %~nx0 "Source.md" "Output.docx"
echo   %~nx0 "Source.md" "Output.docx" 4.90in
echo.
echo Example:
echo   %~nx0 "2Java_Temelleri_Kompakt_Birlesik_github_linkleri_kontrol_edilmis_qr_gomulu.md" "ciktiQR2.docx"
echo.
exit /b 1

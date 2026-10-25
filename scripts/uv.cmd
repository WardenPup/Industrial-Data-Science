@echo off
setlocal
set "IDS_ROOT=%~dp0.."
set "UV_PYTHON_INSTALL_DIR=%IDS_ROOT%\.uv-python"
set "PLAYWRIGHT_BROWSERS_PATH=%IDS_ROOT%\.tools\playwright"
set "JUPYTER_CONFIG_DIR=%IDS_ROOT%\.jupyter"
set "JUPYTER_DATA_DIR=%IDS_ROOT%\.local\share\jupyter"
set "JUPYTER_RUNTIME_DIR=%IDS_ROOT%\.local\share\jupyter\runtime"
set "IPYTHONDIR=%IDS_ROOT%\.local\ipython"
pushd "%IDS_ROOT%"
if exist "%IDS_ROOT%\.tools\uv\uv.exe" (
    "%IDS_ROOT%\.tools\uv\uv.exe" %*
) else (
    uv %*
)
set "IDS_EXIT=%ERRORLEVEL%"
popd
exit /b %IDS_EXIT%

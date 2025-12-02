@echo off
REM NanoBanana MCP Server 快速启动脚本

echo ========================================
echo   NanoBanana MCP Server
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
pip show mcp >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo [完成] 依赖已安装
)

echo.
echo [2/3] 启动 MCP 服务器...
echo.
echo 提示: 此服务器通过 stdio 与客户端通信
echo 请在 Claude Desktop 或其他 MCP 客户端中配置使用
echo.
echo 配置路径示例:
echo   Windows: %%APPDATA%%\Claude\claude_desktop_config.json
echo   macOS:   ~/Library/Application Support/Claude/claude_desktop_config.json
echo.
echo 按 Ctrl+C 停止服务器
echo.
echo ========================================
echo.

python mcp_server.py

if errorlevel 1 (
    echo.
    echo [错误] 服务器启动失败
    pause
    exit /b 1
)

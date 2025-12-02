# NanoBanana MCP Server - 快速测试脚本
# 使用前请先设置 OPENROUTER_API_KEY 环境变量

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NanoBanana MCP Server 测试工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 API Key
if (-not $env:OPENROUTER_API_KEY) {
    Write-Host "❌ 错误: OPENROUTER_API_KEY 环境变量未设置！" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先设置 API Key:" -ForegroundColor Yellow
    Write-Host '  $env:OPENROUTER_API_KEY="sk-or-v1-your-key-here"' -ForegroundColor Yellow
    Write-Host ""
    Write-Host "或输入您的 API Key (输入后按回车):" -ForegroundColor Yellow
    $apiKey = Read-Host "API Key"
    
    if ($apiKey) {
        $env:OPENROUTER_API_KEY = $apiKey
        Write-Host "✅ API Key 已设置" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "❌ 未输入 API Key，退出测试" -ForegroundColor Red
        exit 1
    }
} else {
    $maskedKey = $env:OPENROUTER_API_KEY.Substring(0, [Math]::Min(15, $env:OPENROUTER_API_KEY.Length)) + "..."
    Write-Host "✅ API Key 已设置: $maskedKey" -ForegroundColor Green
    Write-Host ""
}

# 检查依赖
Write-Host "检查 Python 依赖..." -ForegroundColor Cyan
$mcpInstalled = python -c "import mcp" 2>$null; $?
$httpxInstalled = python -c "import httpx" 2>$null; $?

if (-not $mcpInstalled -or -not $httpxInstalled) {
    Write-Host "⚠️  缺少依赖，正在安装..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host ""
}

# 测试菜单
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "请选择测试类型:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. 基础功能测试 (test_mcp.py)"
Write-Host "2. Gemini 图像生成测试 (test_gemini_image.py)"
Write-Host "3. 全部测试"
Write-Host "0. 退出"
Write-Host ""

$choice = Read-Host "请输入选项 (0-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "运行基础功能测试..." -ForegroundColor Green
        python test_mcp.py
    }
    "2" {
        Write-Host ""
        Write-Host "运行 Gemini 图像生成测试..." -ForegroundColor Green
        python test_gemini_image.py
    }
    "3" {
        Write-Host ""
        Write-Host "运行全部测试..." -ForegroundColor Green
        Write-Host ""
        Write-Host ">>> 测试 1/2: 基础功能" -ForegroundColor Yellow
        python test_mcp.py
        Write-Host ""
        Write-Host ">>> 测试 2/2: Gemini 图像生成" -ForegroundColor Yellow
        python test_gemini_image.py
    }
    "0" {
        Write-Host "退出测试" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "无效选项" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "测试完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

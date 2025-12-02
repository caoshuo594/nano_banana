# NanoBanana MCP Server

一个封装 OpenRouter API 的 MCP (Model Context Protocol) 服务器，可供 Claude Desktop、Gemini CLI 等 MCP 客户端使用。

## 功能特性

- 🚀 通过 MCP 协议访问 OpenRouter API
- 🤖 默认使用 Google Gemini 3 Pro Image Preview 模型
- 💬 支持聊天补全（Chat Completion）
- 📋 支持列出所有可用模型
- 🖼️ 支持文本和图像输入

## 安装

### 1. 获取 OpenRouter API Key

⚠️ **必需步骤**: 在使用此服务前，您必须先获取 OpenRouter API Key。

1. 访问 [OpenRouter](https://openrouter.ai/)
2. 注册/登录账号
3. 在 [API Keys 页面](https://openrouter.ai/keys) 创建新的 API Key
4. 复制您的 API Key（格式：`sk-or-v1-...`）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

**必须设置环境变量** `OPENROUTER_API_KEY`：

#### Windows PowerShell
```powershell
# 临时设置（当前会话）
$env:OPENROUTER_API_KEY="sk-or-v1-your-actual-key-here"

# 永久设置
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'sk-or-v1-your-key-here', 'User')
```

#### Linux/Mac
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-actual-key-here"

# 永久设置，添加到 ~/.bashrc 或 ~/.zshrc
echo 'export OPENROUTER_API_KEY="sk-or-v1-your-key-here"' >> ~/.bashrc
```

**配置说明**：
- **API URL**: https://openrouter.ai/api/v1
- **默认模型**: google/gemini-3-pro-image-preview

## 使用方法

### 在 Claude Desktop 中使用

1. 找到 Claude Desktop 的配置文件：
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. 将以下配置添加到 `mcpServers` 部分：

```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "python",
      "args": [
        "d:\\ai_coding\\Antigravity\\nano_banana\\mcp_server.py"
      ],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-v1-your-actual-key-here"
      }
    }
  }
}
```

⚠️ **重要**: 请将 `sk-or-v1-your-actual-key-here` 替换为您的实际 OpenRouter API Key！

3. 重启 Claude Desktop

### 在 Gemini CLI 中使用

如果 Gemini CLI 支持 MCP 协议，可以使用类似的配置方式。具体配置方法请参考 Gemini CLI 的文档。

### 直接测试

可以使用 MCP Inspector 进行测试：

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

## 可用工具

### 1. chat_completion

发送聊天补全请求到 OpenRouter API。

**参数**:
- `messages` (必需): 消息数组，每个消息包含 `role` 和 `content`
  - `role`: "user", "assistant", 或 "system"
  - `content`: 消息内容（文本或图像 URL）
- `model` (可选): 使用的模型，默认为 `google/gemini-3-pro-image-preview`
- `temperature` (可选): 采样温度 (0-2)，默认为 1
- `max_tokens` (可选): 生成的最大 token 数
- `stream` (可选): 是否流式返回，默认为 false

**示例**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "你好，请介绍一下自己"
    }
  ],
  "temperature": 0.7
}
```

### 2. list_models

列出 OpenRouter API 上所有可用的模型。

**参数**: 无

## 可用资源

### nano-banana://config

返回 NanoBanana MCP Server 的配置信息，包括 API URL 和默认模型。

## 架构说明

```
┌─────────────────┐
│  MCP 客户端     │
│ (Claude/Gemini) │
└────────┬────────┘
         │ MCP Protocol
         │ (stdio)
┌────────▼────────┐
│  MCP Server     │
│  (mcp_server.py)│
└────────┬────────┘
         │ HTTPS
         │
┌────────▼────────┐
│  OpenRouter API │
│  (Gemini 3 Pro) │
└─────────────────┘
```

## 开发说明

### 项目结构

```
nano_banana/
├── mcp_server.py              # MCP 服务器主程序
├── requirements.txt           # Python 依赖
├── claude_desktop_config.json # Claude Desktop 配置示例
├── README.md                  # 本文档
├── nano_banana.md            # API 配置信息
└── prompt.md                 # 项目需求说明
```

### 修改配置

如需修改 API Key 或默认模型，请编辑 `mcp_server.py` 中的以下常量：

```python
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
OPENROUTER_API_KEY = "your-api-key-here"
DEFAULT_MODEL = "google/gemini-3-pro-image-preview"
```

### 添加新工具

在 `mcp_server.py` 中：

1. 在 `list_tools()` 函数中添加新工具的定义
2. 在 `call_tool()` 函数中添加工具调用逻辑
3. 实现具体的工具函数

## 故障排除

### 问题：Claude Desktop 无法连接到 MCP 服务器

**解决方案**:
1. 检查 Python 是否在系统 PATH 中
2. 确认 `mcp_server.py` 的路径正确
3. 查看 Claude Desktop 的日志文件
4. 尝试手动运行 `python mcp_server.py` 检查是否有错误

### 问题：API 请求失败

**解决方案**:
1. 检查 API Key 是否有效
2. 确认网络连接正常
3. 查看 OpenRouter API 状态页面
4. 检查是否超出 API 配额

### 问题：依赖安装失败

**解决方案**:
```bash
# 升级 pip
python -m pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关链接

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [OpenRouter API](https://openrouter.ai/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

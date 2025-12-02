# NanoBanana MCP Server 测试指南

## ⚠️ 重要：需要 OpenRouter API Key

在使用此 MCP 服务之前，**必须**先设置 OpenRouter API Key。

### 获取 API Key

1. 访问 [OpenRouter](https://openrouter.ai/)
2. 注册/登录账号
3. 在 [API Keys 页面](https://openrouter.ai/keys) 创建新的 API Key
4. 复制您的 API Key（格式类似：`sk-or-v1-...`）

### 设置环境变量

#### Windows PowerShell
```powershell
# 临时设置（仅当前会话有效）
$env:OPENROUTER_API_KEY="your_api_key_here"

# 永久设置（需要管理员权限）
[System.Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'your_api_key_here', 'User')
```

#### Windows CMD
```cmd
set OPENROUTER_API_KEY=your_api_key_here
```

#### Linux/Mac
```bash
export OPENROUTER_API_KEY="your_api_key_here"

# 永久设置，添加到 ~/.bashrc 或 ~/.zshrc
echo 'export OPENROUTER_API_KEY="your_api_key_here"' >> ~/.bashrc
```

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

所需依赖：
- `mcp>=0.9.0` - Model Context Protocol SDK
- `httpx>=0.27.0` - 异步 HTTP 客户端

## 🧪 测试步骤

### 1. 设置 API Key

**必须先设置！**
```powershell
$env:OPENROUTER_API_KEY="sk-or-v1-your-actual-key-here"
```

### 2. 基础功能测试

测试 MCP 服务器的基本功能：
```bash
python test_mcp.py
```

这将测试：
- ✅ 服务器初始化
- ✅ 资源列表
- ✅ 工具列表
- ✅ 聊天完成（Chat Completion）

### 3. Gemini 图像生成测试

**Gemini 3 Pro Image Preview 支持直接生成图像！**

```bash
python test_gemini_image.py
```

这将测试：
- 🎨 可爱动物图像生成
- 🎨 赛博朋克城市场景
- 🎨 自然风景图像
- 🎨 科幻场景图像
- 🎨 抽象艺术生成

### 4. 其他图像生成模型

如需使用其他模型，可在调用时指定 `model` 参数：

可用的图像生成模型（通过 OpenRouter）：
- `google/gemini-3-pro-image-preview` - Gemini 3 (默认)
- `openai/dall-e-3` - DALL-E 3
- `openai/dall-e-2` - DALL-E 2
- `stability-ai/stable-diffusion-xl` - Stable Diffusion XL
- `google/imagen-3.0-generate-001` - Google Imagen 3

使用 `list_models` 工具查看所有可用模型。

创建测试脚本 `test_real_image.py`：
```python
# 使用 DALL-E 3 生成图像
result = await session.call_tool(
    "chat_completion",
    {
        "messages": [
            {
                "role": "user",
                "content": "生成一只穿太空服的可爱小猫在月球上的图像"
            }
        ],
        "model": "openai/dall-e-3",  # 指定图像生成模型
        "temperature": 0.7
    }
)
```

## 🔍 验证测试

### 成功标志

如果看到以下输出，说明服务正常：
```
✅ MCP Server 初始化成功
可用工具数量: 2
  - chat_completion: ...
  - list_models: ...
```

### 失败情况

1. **API Key 未设置**
   ```
   ❌ 错误: OPENROUTER_API_KEY 环境变量未设置！
   ```
   **解决**: 设置环境变量后重试

2. **API Key 无效**
   ```
   HTTP error: 401
   ```
   **解决**: 检查 API Key 是否正确

3. **网络问题**
   ```
   Connection timeout
   ```
   **解决**: 检查网络连接，可能需要代理

## 🎯 关于图像生成

**重要说明**:

1. **当前默认模型** (`google/gemini-3-pro-image-preview`) ✨ **支持图像生成！**
   - 这是 Google 最新发布的 Gemini 3 模型
   - 原生支持文本转图像生成
   - 推荐使用此模型进行图像生成测试

2. **其他图像生成模型** - 也可以使用：
   - `openai/dall-e-3` - DALL-E 3
   - `openai/dall-e-2` - DALL-E 2
   - `stability-ai/stable-diffusion-xl` - Stable Diffusion XL
   - `google/imagen-3.0-generate-001` - Google Imagen 3

3. **OpenRouter 支持**: OpenRouter 支持多种图像生成模型，返回的可能是图像 URL 或 base64 编码的图像数据。

4. **推荐做法**: 
   - 优先使用默认的 Gemini 3 Pro Image Preview 模型
   - 用 `test_gemini_image.py` 测试图像生成
   - 查看 `list_models` 工具了解其他可用模型
   - 解析返回的图像 URL 或 base64 数据

## 📝 示例输出

成功的测试输出应该类似：
```
🚀 启动 NanoBanana MCP Server...
✅ MCP Server 初始化成功

📋 测试：列出资源
可用资源数量: 1
  - NanoBanana Configuration (nano-banana://config)

💬 测试：Chat Completion
模型: google/gemini-3-pro-image-preview
内容: 你好！我是一个 AI 助手...
Token 使用: 45 (输入: 12, 输出: 33)

✅ 所有测试完成！
```

## 🔗 在 Claude Desktop 中使用

配置文件位置：
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

添加配置：
```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "python",
      "args": ["d:\\ai_coding\\Antigravity\\nano_banana\\mcp_server.py"],
      "env": {
        "OPENROUTER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**注意**: 将 `your_api_key_here` 替换为您的实际 API Key。

重启 Claude Desktop 后即可使用！

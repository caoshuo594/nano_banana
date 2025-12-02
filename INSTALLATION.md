# 🚀 NanoBanana MCP Server - 快速安装指南

## 📋 前置要求

- ✅ Python 3.10 或更高版本
- ✅ pip (Python 包管理器)
- ✅ Claude Desktop 或其他 MCP 客户端

## 🔧 安装步骤

### 步骤 1: 安装 Python 依赖

打开命令提示符，进入项目目录：

```bash
cd d:\ai_coding\Antigravity\nano_banana
pip install -r requirements.txt
```

### 步骤 2: 验证安装

运行测试脚本：

```bash
python test_mcp.py
```

如果看到 "✅ 所有测试完成！"，说明安装成功。

### 步骤 3: 配置 Claude Desktop

#### Windows 用户

1. 打开文件资源管理器，在地址栏输入：
   ```
   %APPDATA%\Claude
   ```

2. 找到或创建文件 `claude_desktop_config.json`

3. 编辑文件，添加以下内容：
   ```json
   {
     "mcpServers": {
       "nano-banana": {
         "command": "python",
         "args": [
           "d:\\ai_coding\\Antigravity\\nano_banana\\mcp_server.py"
         ],
         "env": {}
       }
     }
   }
   ```

4. 保存文件

#### macOS 用户

1. 打开终端，编辑配置文件：
   ```bash
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. 添加配置（注意修改路径）：
   ```json
   {
     "mcpServers": {
       "nano-banana": {
         "command": "python3",
         "args": [
           "/path/to/nano_banana/mcp_server.py"
         ],
         "env": {}
       }
     }
   }
   ```

3. 保存并退出 (Ctrl+X, Y, Enter)

#### Linux 用户

1. 编辑配置文件：
   ```bash
   nano ~/.config/Claude/claude_desktop_config.json
   ```

2. 添加配置（注意修改路径）

3. 保存并退出

### 步骤 4: 重启 Claude Desktop

完全退出 Claude Desktop，然后重新启动。

### 步骤 5: 验证集成

在 Claude Desktop 中，你应该能看到 NanoBanana 工具可用。尝试发送：

```
请使用 nano-banana 工具，介绍一下你自己
```

如果 Claude 成功调用了工具并返回响应，说明配置成功！

## 🎯 使用 Gemini CLI

如果你使用的是 Gemini CLI 且支持 MCP：

1. 查看 Gemini CLI 的 MCP 配置文档
2. 添加类似的服务器配置
3. 确保 Python 路径和脚本路径正确

## ⚠️ 常见问题

### 问题 1: Claude Desktop 找不到 Python

**解决方案**: 使用 Python 的完整路径

Windows 示例：
```json
{
  "mcpServers": {
    "nano-banana": {
      "command": "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
      "args": ["d:\\ai_coding\\Antigravity\\nano_banana\\mcp_server.py"]
    }
  }
}
```

查找 Python 路径：
```bash
where python
```

### 问题 2: 依赖安装失败

**解决方案**: 升级 pip 并重试

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### 问题 3: Claude Desktop 无法连接

**解决方案**: 检查日志

Windows 日志位置：
```
%APPDATA%\Claude\logs
```

查看最新的日志文件，寻找错误信息。

### 问题 4: API 调用失败

**解决方案**: 检查网络和 API Key

1. 确认网络可以访问 https://openrouter.ai
2. 验证 API Key 是否有效
3. 检查 API 配额是否用完

## 🔍 调试技巧

### 手动测试 MCP 服务器

```bash
python mcp_server.py
```

服务器应该启动并等待输入（通过 stdio）。

### 使用 MCP Inspector

安装并运行 MCP Inspector：

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

这会打开一个 Web 界面，让你可以交互式地测试 MCP 服务器。

### 查看详细日志

修改 `mcp_server.py`，添加日志输出：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 下一步

- 📖 阅读 [README.md](README.md) 了解详细功能
- 💡 查看 [EXAMPLES.md](EXAMPLES.md) 学习使用示例
- 🏗️ 阅读 [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) 了解架构

## 🆘 获取帮助

如果遇到问题：

1. 查看本文档的常见问题部分
2. 运行 `python test_mcp.py` 进行诊断
3. 检查 Claude Desktop 日志
4. 提交 Issue 到项目仓库

---

**祝你使用愉快！** 🎉

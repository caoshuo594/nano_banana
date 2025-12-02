#!/usr/bin/env python3
"""
NanoBanana MCP Server
封装 OpenRouter API 为 MCP 服务，供 Claude Code 和 Gemini CLI 使用
"""

import asyncio
import json
import os
from typing import Any, Optional
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# OpenRouter API 配置
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
# 不要在模块级别抛出异常，以免影响 MCP Server 启动
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
DEFAULT_MODEL = "google/gemini-3-pro-image-preview"

# 创建 MCP 服务器实例
app = Server("nano-banana")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """列出可用的资源"""
    return [
        Resource(
            uri="nano-banana://config",
            name="NanoBanana Configuration",
            mimeType="application/json",
            description="OpenRouter API configuration for NanoBanana",
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """读取资源内容"""
    if uri == "nano-banana://config":
        config = {
            "api_url": OPENROUTER_API_URL,
            "model": DEFAULT_MODEL,
            "description": "NanoBanana MCP Server - OpenRouter API Wrapper",
        }
        return json.dumps(config, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的工具"""
    return [
        Tool(
            name="chat_completion",
            description="Send a chat completion request to OpenRouter API using Gemini 3 Pro Image Preview model. Supports text and image inputs.",
            inputSchema={
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "array",
                        "description": "Array of message objects with role and content",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {
                                    "type": "string",
                                    "enum": ["user", "assistant", "system"],
                                    "description": "Role of the message sender",
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Message content (text or image URL)",
                                },
                            },
                            "required": ["role", "content"],
                        },
                    },
                    "model": {
                        "type": "string",
                        "description": f"Model to use (default: {DEFAULT_MODEL})",
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Sampling temperature (0-2, default: 1)",
                        "minimum": 0,
                        "maximum": 2,
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum tokens to generate",
                    },
                    "stream": {
                        "type": "boolean",
                        "description": "Whether to stream the response (default: false)",
                    },
                },
                "required": ["messages"],
            },
        ),
        Tool(
            name="list_models",
            description="List all available models from OpenRouter API",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """调用工具"""
    if name == "chat_completion":
        return await chat_completion(arguments)
    elif name == "list_models":
        return await list_models()
    else:
        raise ValueError(f"Unknown tool: {name}")


async def chat_completion(arguments: dict) -> list[TextContent]:
    """调用 OpenRouter Chat Completion API"""
    messages = arguments.get("messages", [])
    model = arguments.get("model", DEFAULT_MODEL)
    temperature = arguments.get("temperature", 1.0)
    max_tokens = arguments.get("max_tokens")
    stream = arguments.get("stream", False)

    # 构建请求体
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "modalities": ["image", "text"],  # 支持图像生成
    }

    if max_tokens:
        payload["max_tokens"] = max_tokens

    if stream:
        payload["stream"] = True

    # 发送请求
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/nano-banana/mcp-server",
        "X-Title": "NanoBanana MCP Server",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{OPENROUTER_API_URL}/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            result = response.json()

            # 提取响应内容
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0]["message"]
                content = message.get("content", "")
                images = message.get("images", [])
                usage = result.get("usage", {})

                response_data = {
                    "content": content,
                    "model": result.get("model", model),
                    "usage": usage,
                }
                
                # 如果有图像，添加到响应中
                if images:
                    response_data["images"] = [
                        {
                            "url": img.get("image_url", {}).get("url", ""),
                            "detail": img.get("image_url", {}).get("detail", "auto")
                        }
                        for img in images
                    ]

                return [
                    TextContent(
                        type="text",
                        text=json.dumps(
                            response_data,
                            indent=2,
                            ensure_ascii=False,
                        ),
                    )
                ]
            else:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(
                            {"error": "No response from API", "raw_response": result},
                            indent=2,
                        ),
                    )
                ]

        except httpx.HTTPStatusError as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "error": f"HTTP error: {e.response.status_code}",
                            "details": e.response.text,
                        },
                        indent=2,
                    ),
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2),
                )
            ]


async def list_models() -> list[TextContent]:
    """列出所有可用的模型"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                f"{OPENROUTER_API_URL}/models",
                headers=headers,
            )
            response.raise_for_status()
            result = response.json()

            return [
                TextContent(
                    type="text",
                    text=json.dumps(result, indent=2, ensure_ascii=False),
                )
            ]

        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2),
                )
            ]


async def main():
    """启动 MCP 服务器"""
    if not OPENROUTER_API_KEY:
        import sys
        print("⚠️ 警告: OPENROUTER_API_KEY 环境变量未设置！MCP Server 将启动，但调用 API 会失败。", file=sys.stderr)
        print("请在 MCP 客户端配置中设置环境变量: OPENROUTER_API_KEY", file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())

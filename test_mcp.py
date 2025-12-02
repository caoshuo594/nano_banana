#!/usr/bin/env python3
"""
测试 NanoBanana MCP Server
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """测试 MCP 服务器的基本功能"""
    
    # 服务器参数
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None,
    )
    
    print("🚀 启动 NanoBanana MCP Server...")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化
            await session.initialize()
            print("✅ MCP Server 初始化成功\n")
            
            # 1. 列出资源
            print("📋 测试：列出资源")
            resources = await session.list_resources()
            print(f"可用资源数量: {len(resources.resources)}")
            for resource in resources.resources:
                print(f"  - {resource.name} ({resource.uri})")
            print()
            
            # 2. 读取配置资源
            print("📖 测试：读取配置资源")
            config_resource = await session.read_resource("nano-banana://config")
            for content in config_resource.contents:
                if hasattr(content, 'text'):
                    config = json.loads(content.text)
                    print(f"API URL: {config['api_url']}")
                    print(f"默认模型: {config['model']}")
            print()
            
            # 3. 列出工具
            print("🔧 测试：列出工具")
            tools = await session.list_tools()
            print(f"可用工具数量: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # 4. 测试 chat_completion 工具
            print("💬 测试：Chat Completion")
            print("发送消息: '你好，请用一句话介绍自己'")
            
            result = await session.call_tool(
                "chat_completion",
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "你好，请用一句话介绍自己"
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 100
                }
            )
            
            print("\n响应:")
            for content in result.content:
                if hasattr(content, 'text'):
                    response_data = json.loads(content.text)
                    print(f"模型: {response_data.get('model', 'N/A')}")
                    print(f"内容: {response_data.get('content', 'N/A')}")
                    if 'usage' in response_data:
                        usage = response_data['usage']
                        print(f"Token 使用: {usage.get('total_tokens', 'N/A')} (输入: {usage.get('prompt_tokens', 'N/A')}, 输出: {usage.get('completion_tokens', 'N/A')})")
            print()
            
            print("✅ 所有测试完成！")


if __name__ == "__main__":
    try:
        asyncio.run(test_mcp_server())
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

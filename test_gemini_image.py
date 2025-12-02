#!/usr/bin/env python3
"""
测试 Gemini 3 Pro Image Preview 的图像生成能力
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_gemini_image_generation():
    """测试 Gemini 3 Pro Image Preview 的图像生成功能"""
    
    # 服务器参数
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
        env=None,
    )
    
    print("🚀 测试 Gemini 3 Pro Image Preview 图像生成功能")
    print("=" * 70)
    print("📦 模型: google/gemini-3-pro-image-preview")
    print("🎨 这是 Google 最新发布的支持图像生成的 Gemini 模型")
    print("=" * 70)
    print()
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化
            await session.initialize()
            print("✅ MCP Server 初始化成功\n")
            
            # 测试案例列表
            test_cases = [
                {
                    "name": "可爱动物",
                    "prompt": "生成一张图片：一只穿着宇航服的橙色小猫站在月球表面，地球在背景中，卡通风格，高清细节"
                },
                {
                    "name": "赛博朋克城市",
                    "prompt": "生成一张图片：未来赛博朋克城市夜景，霓虹灯闪烁，飞行汽车穿梭，雨后湿润的街道反射着彩色灯光，电影级画质，8K超高清"
                },
                {
                    "name": "自然风景",
                    "prompt": "生成一张图片：日落时分的富士山，前景是樱花盛开的树林，湖面倒映着粉色的天空，油画风格"
                },
                {
                    "name": "科幻场景",
                    "prompt": "生成一张图片：外星球表面的科研基地，巨大的透明穹顶，两个太阳挂在紫色的天空，科幻电影风格"
                },
                {
                    "name": "抽象艺术",
                    "prompt": "生成一张图片：抽象派艺术作品，流动的色彩，金色、蓝色和紫色的交织，像星云一样的质感，现代艺术风格"
                }
            ]
            
            results = []
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"🎨 测试 {i}/{len(test_cases)}: {test_case['name']}")
                print("-" * 70)
                print(f"提示词: {test_case['prompt']}")
                print()
                
                try:
                    result = await session.call_tool(
                        "chat_completion",
                        {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": test_case['prompt']
                                }
                            ],
                            "temperature": 0.8,
                            "max_tokens": 2000
                        }
                    )
                    
                    print("✅ 响应:")
                    success = False
                    for content in result.content:
                        if hasattr(content, 'text'):
                            response_data = json.loads(content.text)
                            
                            if 'error' in response_data:
                                print(f"❌ 错误: {response_data['error']}")
                                if 'details' in response_data:
                                    print(f"详情: {response_data['details'][:300]}")
                                results.append({
                                    "test": test_case['name'],
                                    "status": "failed",
                                    "error": response_data['error']
                                })
                            else:
                                model = response_data.get('model', 'N/A')
                                content_text = response_data.get('content', '')
                                
                                print(f"模型: {model}")
                                
                                # 检查是否包含图像 URL 或 base64 数据
                                has_image = False
                                if any(keyword in content_text.lower() for keyword in [
                                    'http://', 'https://', 'data:image', 'base64',
                                    '.png', '.jpg', '.jpeg', '.webp'
                                ]):
                                    print("🖼️  检测到图像数据!")
                                    has_image = True
                                    
                                    # 尝试提取 URL
                                    lines = content_text.split('\n')
                                    for line in lines:
                                        if 'http' in line.lower() or 'data:image' in line.lower():
                                            print(f"📎 图像链接: {line[:100]}...")
                                
                                # 显示内容预览
                                print(f"内容预览: {content_text[:200]}...")
                                if len(content_text) > 200:
                                    print(f"(内容总长度: {len(content_text)} 字符)")
                                
                                if 'usage' in response_data:
                                    usage = response_data['usage']
                                    print(f"Token 使用: {usage.get('total_tokens', 'N/A')} " +
                                          f"(输入: {usage.get('prompt_tokens', 'N/A')}, " +
                                          f"输出: {usage.get('completion_tokens', 'N/A')})")
                                
                                success = True
                                results.append({
                                    "test": test_case['name'],
                                    "status": "success",
                                    "has_image": has_image,
                                    "content_length": len(content_text),
                                    "tokens": usage.get('total_tokens', 0) if 'usage' in response_data else 0
                                })
                    
                    if not success:
                        results.append({
                            "test": test_case['name'],
                            "status": "no_response"
                        })
                    
                except Exception as e:
                    print(f"❌ 调用失败: {e}")
                    results.append({
                        "test": test_case['name'],
                        "status": "exception",
                        "error": str(e)
                    })
                
                print()
                
                # 避免速率限制
                if i < len(test_cases):
                    await asyncio.sleep(2)
            
            # 输出测试总结
            print("=" * 70)
            print("📊 测试总结")
            print("=" * 70)
            print()
            
            success_count = sum(1 for r in results if r['status'] == 'success')
            image_count = sum(1 for r in results if r.get('has_image', False))
            
            print(f"总测试数: {len(results)}")
            print(f"成功: {success_count}")
            print(f"失败: {len(results) - success_count}")
            print(f"包含图像: {image_count}")
            print()
            
            print("详细结果:")
            for r in results:
                status_icon = "✅" if r['status'] == 'success' else "❌"
                image_icon = "🖼️ " if r.get('has_image', False) else ""
                print(f"{status_icon} {image_icon}{r['test']}: {r['status']}")
                if r.get('tokens'):
                    print(f"   Token 使用: {r['tokens']}")
                if r.get('error'):
                    print(f"   错误: {r['error'][:100]}")
            
            print()
            print("=" * 70)
            
            if image_count > 0:
                print("✅ Gemini 3 Pro Image Preview 成功生成图像！")
            elif success_count > 0:
                print("⚠️  模型响应成功，但未检测到图像数据")
                print("   可能需要更明确的图像生成指令")
            else:
                print("❌ 测试失败，请检查 API Key 和网络连接")
            
            print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(test_gemini_image_generation())
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except ValueError as e:
        print(f"\n\n❌ 配置错误: {e}")
        print("\n💡 提示: 请先设置 OPENROUTER_API_KEY 环境变量")
        print("   PowerShell: $env:OPENROUTER_API_KEY='your_key_here'")
    except Exception as e:
        print(f"\n\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

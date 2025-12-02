#!/usr/bin/env python3
"""
生成熊猫武士图片并保存到文件
"""

import asyncio
import json
import os
import base64
import httpx
from datetime import datetime


async def generate_and_save_panda():
    """生成熊猫武士图片并保存"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ 请先设置 OPENROUTER_API_KEY 环境变量")
        return
    
    print("🎨 正在生成熊猫武士图片...")
    print("=" * 70)
    
    prompt = "生成一张图片：一只威武的熊猫武士，穿着传统的日本武士盔甲，手持武士刀，站在竹林中，月光洒下，电影级画质，细节丰富，史诗般的氛围"
    
    print(f"📝 提示词: {prompt}\n")
    
    payload = {
        "model": "google/gemini-3-pro-image-preview",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "modalities": ["image", "text"],
        "temperature": 0.8,
        "max_tokens": 2000,
        "n": 1  # 只生成1张图像，而不是默认的2张
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/nano-banana/mcp-server",
        "X-Title": "NanoBanana MCP Server",
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            print("⏳ 正在生成，请稍候...")
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            result = response.json()
            
            print("\n✅ API 响应成功！\n")
            
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0]["message"]
                content = message.get("content", "")
                images = message.get("images", [])
                
                # 显示文本内容
                if content:
                    print("📝 文本描述:")
                    print(content[:200] + "..." if len(content) > 200 else content)
                    print()
                
                # 保存图像
                if images:
                    print(f"✨ 成功生成 {len(images)} 张图像！\n")
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    for i, img in enumerate(images, 1):
                        url = img.get("image_url", {}).get("url", "")
                        if url and url.startswith("data:image"):
                            # 解析 base64 数据
                            header, encoded = url.split(",", 1)
                            image_data = base64.b64decode(encoded)
                            
                            # 确定文件格式
                            if "jpeg" in header or "jpg" in header:
                                ext = "jpg"
                            elif "png" in header:
                                ext = "png"
                            elif "webp" in header:
                                ext = "webp"
                            else:
                                ext = "jpg"
                            
                            # 保存文件
                            filename = f"panda_warrior_{timestamp}_{i}.{ext}"
                            with open(filename, "wb") as f:
                                f.write(image_data)
                            
                            file_size = len(image_data) / 1024  # KB
                            print(f"🖼️  图像 {i} 已保存:")
                            print(f"   文件名: {filename}")
                            print(f"   格式: {ext.upper()}")
                            print(f"   大小: {file_size:.2f} KB")
                            print()
                    
                    print(f"✅ 所有图像已保存到当前目录！")
                else:
                    print("⚠️  未检测到图像数据")
                
                # Token 使用统计
                if "usage" in result:
                    usage = result["usage"]
                    print(f"\n📊 Token 使用: {usage.get('total_tokens', 'N/A')}")
                
        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP 错误: {e.response.status_code}")
            print(f"响应: {e.response.text}")
        except Exception as e:
            print(f"❌ 失败: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(generate_and_save_panda())

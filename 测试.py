import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ================= 配置区域 =================
# 请替换为你的 DeepSeek API Key
API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-你的KEY在这里")
# DeepSeek 官方地址，如果你用中转请填写中转地址
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
# 测试使用的模型，通常用 deepseek-chat
MODEL_NAME = "deepseek-v4-flash"
# ===========================================

def get_client():
    return OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )

def test_with_system_role():
    """
    测试 1: 发送包含独立 system 角色的标准请求
    这是 Claude Code 默认可能发送的格式
    """
    print("--- 测试 1: 发送包含 'system' 角色的请求 ---")
    client = get_client()
    
    messages = [
        {"role": "system", "content": "你是一个测试助手，只回答'OK'。"},
        {"role": "user", "content": "你好"}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.5
        )
        print(f"✅ 成功! API 返回: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ 失败! 错误信息: {str(e)}")
        # 检查是否是我们遇到的那个特定错误
        if "unknown variant `system`" in str(e) or "400" in str(e):
            print("   -> 确认：当前 API 端点不支持独立的 'system' 角色。")
        return False

def test_with_merged_role():
    """
    测试 2: 将 system 内容合并到第一条 user 消息中
    这是兼容性最好的写法
    """
    print("\n--- 测试 2: 将 System 提示合并到 User 消息中 ---")
    client = get_client()
    
    # 模拟合并逻辑
    system_prompt = "你是一个测试助手，只回答'OK'。"
    user_input = "你好"
    
    messages = [
        {"role": "user", "content": f"{system_prompt}\n\n{user_input}"}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.5
        )
        print(f"✅ 成功! API 返回: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ 失败! 错误信息: {str(e)}")
        return False

if __name__ == "__main__":
    if API_KEY == "sk-你的KEY在这里":
        print("⚠️ 警告: 请先在代码中或环境变量中设置 DEEPSEEK_API_KEY")
        exit(1)

    print(f"正在测试 API: {BASE_URL}")
    print(f"使用模型: {MODEL_NAME}\n")

    # 执行测试
    support_system = test_with_system_role()
    
    if not support_system:
        print("\n👇 因为测试 1 失败，正在尝试兼容性方案...")
        test_with_merged_role()
    else:
        print("\n🎉 你的 API 配置完全正常，支持 System 角色。")
        print("   如果 Claude Code 依然报错，可能是 Claude Code 本地的缓存或配置问题。")
# sk-9a44244e7deb4bacb553a1aad6bac780

import os
from langchain_openai import ChatOpenAI
from langchain import agents
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

os.environ["DEEPSEEK_API_KEY"] = "sk-9a44244e7deb4bacb553a1aad6bac780"

# --- 1. 配置 DeepSeek API Key ---
if not os.environ.get("DEEPSEEK_API_KEY"):
    print("错误: 未设置 DEEPSEEK_API_KEY 环境变量")
    exit(1)

# --- 2. 定义工具 (Tools) ---
@tool
def calculator(expression: str) -> str:
    """用于计算数学表达式。输入应为简单的数学表达式字符串，如 '2 + 2'。"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"

@tool
def get_weather(city: str) -> str:
    """查询指定城市的天气。"""
    return f"{city} 今天晴朗，气温 25 度。"

tools = [calculator, get_weather]

# --- 3. 初始化 LLM ---
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com",
    temperature=0
)

# --- 4. 创建 Agent ---
agent_executor = agents.create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个有用的智能助手。如果遇到无法回答的问题，请尝试使用工具。",
    debug=True
)

# --- 5. 交互测试函数 ---
def chat_loop():
    print("开始与 DeepSeek Agent 对话。输入 'q' 退出。\n")
    messages = []
    
    while True:
        user_input = input("你: ").strip()
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("再见！")
            break
        
        if not user_input:
            continue
            
        try:
            # 将用户消息添加到消息列表
            messages.append(HumanMessage(content=user_input))
            initial_length = len(messages)
            
            # 调用 Agent (使用 stream 以获取实时输出)
            for event in agent_executor.stream(
                {"messages": messages},
                stream_mode="updates"
            ):
                if "agent" in event:
                    agent_output = event["agent"]
                    if "messages" in agent_output and agent_output["messages"]:
                        # 更新消息列表
                        messages = agent_output["messages"]
            
            # 获取最后一条 AIMessage (Agent 的回复)
            if messages and len(messages) > initial_length:
                # 获取最后添加的消息，应该是 AIMessage
                last_agent_message = messages[-1]
                if hasattr(last_agent_message, 'content'):
                    print(f"Agent: {last_agent_message.content}\n")
                else:
                    print(f"Agent: {last_agent_message}\n")
                
        except Exception as e:
            print(f"发生错误: {e}\n")

if __name__ == "__main__":
    chat_loop()
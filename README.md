# DeepSeek Agent - 智能助手

一个基于 LangChain 和 DeepSeek API 的多功能智能助手，支持工具调用和多轮对话。

## ✨ 功能特性

- 🤖 **AI 对话**: 基于 DeepSeek 大模型的智能对话
- 🧮 **计算器工具**: 支持数学表达式计算
- 🌤️ **天气工具**: 查询城市天气信息
- 💬 **多轮对话**: 保存对话历史，实现连贯的多轮交互
- 🔧 **工具自动调用**: Agent 智能判断何时使用工具

## 📋 前置要求

- Python 3.8+
- DeepSeek API Key (获取地址: https://api.deepseek.com)

## 🛠️ 安装依赖

```bash
pip install langchain langchain-openai langchain-community
```

## 🚀 使用方法

### 1. 配置 API Key

编辑文件中第 11 行，设置你的 DeepSeek API Key:

```python
os.environ["DEEPSEEK_API_KEY"] = "your-api-key-here"
```

或者设置环境变量：
```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="your-api-key-here"

# Linux/Mac
export DEEPSEEK_API_KEY="your-api-key-here"
```

### 2. 运行程序

```bash
python q1.py
```

### 3. 与 Agent 交互

```
你: 2+2等于多少？
Agent: 2+2等于4

你: 北京的天气怎么样？
Agent: 北京 今天晴朗，气温 25 度。

你: q  # 输入 'q' 退出程序
再见！
```

## 🔧 代码结构

| 组件 | 说明 |
|------|------|
| `calculator` | 数学计算工具 |
| `get_weather` | 天气查询工具 |
| `chat_loop()` | 主交互循环 |
| `agent_executor` | LangChain Agent 执行器 |

## 📝 工具说明

### Calculator 工具
- **功能**: 计算数学表达式
- **使用场景**: "2+2是多少？"、"计算 3.14 * 2"
- **底层实现**: Python eval()

### Get Weather 工具
- **功能**: 查询城市天气
- **使用场景**: "上海的天气"、"杭州今天天气如何"
- **注意**: 当前为模拟返回，实际应接入真实天气 API

## 💡 示例对话

```
🤖 DeepSeek Agent 已启动
你: 帮我计算 sqrt(16)
Agent: [调用计算器工具] 结果是 4.0

你: 明天北京天气预报
Agent: [调用天气工具] 北京 今天晴朗，气温 25 度。

你: 你能做什么？
Agent: [直接回答] 我是一个智能助手，可以帮你：
       - 进行数学计算
       - 查询天气信息
       - 回答各种问题
```

## 🔐 安全建议

⚠️ **重要**: 不要在代码中硬编码 API Key，应该：
- 使用环境变量存储敏感信息
- 不要将含有 API Key 的代码推送到公开仓库
- 定期更换 API Key

## 🐛 常见问题

**Q: 报错 "无法解析导入"**
- A: 确保已安装所有依赖: `pip install langchain langchain-openai`

**Q: 报错 "DEEPSEEK_API_KEY 环境变量未设置"**
- A: 检查是否正确设置了 API Key 环境变量或代码中的 key 赋值

**Q: Agent 没有调用工具**
- A: 确保输入包含相关关键词（如 "计算"、"天气"），并检查模型是否支持工具调用

## 📚 相关资源

- [LangChain 文档](https://docs.langchain.com)
- [DeepSeek API 文档](https://api.deepseek.com/docs)
- [OpenAI 兼容 API](https://docs.langchain.com/integrations/llms/openai)

## 📄 许可证

MIT License

## 👨‍💻 作者

Created with LangChain & DeepSeek API

---

**最后更新**: 2025-12-28

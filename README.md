# FastMCP 智能内容生成工具

## 项目概述
本项目基于 FastMCP 框架，支持多模态输入（文本、图片、聊天记录），通过智能策略匹配提示词，调用外部 LLM 生成高质量 HTML，并用 Playwright 渲染截图。

## 目录结构
```
project_root/
├── src/
│   ├── main.py
│   ├── input_processor.py
│   ├── prompt_manager.py
│   ├── fastmcp_policy.py
│   ├── html_generator.py
│   ├── file_saver.py
│   └── browser_renderer.py
├── prompts/
├── config/
│   └── settings.py
├── output/
├── .env
├── requirements.txt
└── README.md
```

## 安装指南
1. Python 3.9+，建议使用 venv：
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install
   ```
2. 配置 .env 文件，填写 API 密钥等敏感信息。

## 配置说明
- `config/settings.py`：管理所有路径、API KEY、超时、重试等参数。
- `.env`：存放敏感信息。

## 使用示例
```bash
python src/main.py --input "你的描述文本或图片路径"
```

## 故障排除
- Playwright 报错：请确保已运行 `playwright install`
- API 调用失败：检查 .env 配置和网络

## 贡献与测试
- 欢迎提交 PR，建议先写单元测试。

## License
MIT

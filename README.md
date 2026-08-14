# 网安 AI 助手

基于 Qwen2.5-7B 的网络安全学习辅助工具，支持代码审计、渗透报告生成、Payload 生成、知识库问答等功能。

## 功能列表

1. **netsec_ai.py** - 综合版（v4.0）
   - 10 个功能：自由对话、Payload 生成、漏洞原理、工具命令、代码审计、CTF 引导、错误排查、知识库问答、AI Agent、报告生成

2. **code_audit.py** - 代码审计
   - 输入：代码片段或文件路径
   - 输出：漏洞分析 + 修复建议

3. **generate_report.py** - 报告生成
   - 输入：漏洞类型 + 目标
   - 输出：完整渗透测试报告

4. **generate_payload.py** - Payload 生成
   - 输入：漏洞类型
   - 输出：可用 payload + 原理解释

5. **knowledge_base_qa.py** - 知识库问答
   - 输入：问题 + 笔记文件
   - 输出：基于笔记的回答

## 运行环境

- Windows / Linux
- Python 3.8+
- Ollama（本地运行模型）
- GPU: 推荐 8GB+ 显存（RTX 3060 / RTX 4060 / RTX 5060 等）

## 快速开始

### 1. 安装 Ollama
```bash
# Windows: 下载 https://ollama.com/download
# Linux: curl -fsSL https://ollama.com/install.sh | sh
```

### 2. 下载模型
```bash
ollama pull qwen2.5:7b
```

### 3. 运行助手
```bash
cd E:\网安\AI助手代码
ai.bat
# 或直接运行
python netsec_ai.py
```

## 项目截图

（待补充）

## 项目心得

做这个项目的起因是在学习网络安全时，经常需要：
- 查各种漏洞的 payload
- 分析代码有没有漏洞
- CTF 解题时不知道下一步

所以用本地大模型把这些功能整合在一起，用自然语言就能交互。

## 模型信息

- 主模型：Qwen/Qwen2.5-7B-Instruct
- 向量化模型：nomic-embed-text（知识库用）
- 大小：约 5GB（GGUF 量化版）
- 显存需求：约 6-8GB

## 部署记录

- 2026-08-13: AMD Radeon Cloud 部署成功，4 个功能全部验证通过
- 2026-08-14: 本地 RTX 5060 部署完成，v4.0 版本上线
- 下一步：添加更多漏洞类型支持、优化 CTF 引导功能

## 技术栈

- **模型推理**: Ollama + Qwen2.5-7B
- **Python**: 3.8+
- **前端**: 命令行交互
- **知识库**: ChromaDB（可选）
- **部署**: Windows 本地运行

## License

MIT License

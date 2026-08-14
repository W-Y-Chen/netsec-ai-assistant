# 网安 AI 助手

基于本地大模型的网络安全 AI 助手，无需联网、无需 API Key、完全免费。

## 功能

- 自由对话 - 直接问任何网安问题
- Payload 生成 - SQL 注入、XSS、命令注入等
- 漏洞原理讲解 - 用大白话讲清楚漏洞原理
- 工具命令速查 - sqlmap、nmap 等常用命令
- 代码审计 - 分析源码中的安全漏洞
- CTF 互动引导 - 一步步带你解题
- 错误排查 - payload 不生效时帮你分析
- 知识库问答 - 基于本地笔记回答
- AI Agent - 自动执行命令（实验性）
- 报告生成 - 生成渗透测试报告

## 快速开始

### 1. 安装 Ollama

**Windows**: 下载 https://ollama.com/download

**Linux/Mac**:
```bash
curl -fsSL https://ollama.com/install.sh | sh
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

## 项目博客

https://w-y-chen.github.io

## 部署记录

- 2026-08-13: AMD Radeon Cloud 部署成功，4 功能验证通过
- 2026-08-14: 本地 RTX 5060 部署完成，10 功能全部跑通

## 项目心得

做这个项目的起因是在学习网络安全时，经常需要：
- 查各种漏洞的 payload
- 分析代码有没有漏洞
- CTF 解题时不知道下一步

所以用本地大模型把这些功能整合在一起，用自然语言就能交互。

## 技术栈

- 大模型: Qwen2.5-7B-Instruct
- 推理框架: Ollama
- 编程语言: Python 3
- 用户界面: 命令行交互

## 使用要求

- 系统: Windows / Linux / Mac
- Python: 3.8+
- GPU: 8GB+ 显存（推荐）
- 内存: 16GB+ RAM
- 存储: 10GB+ 可用空间

## 许可证

MIT License

"""
网安 AI 助手 v4.0
功能：自由对话 / Payload生成 / 漏洞原理 / 工具速查 / 代码审计 / CTF引导 / 错误排查 / 知识库 / Agent / 报告
"""

import requests
import os
import time

# Ollama 配置
OLLAMA_URL = "http://localhost:11434/api"
MODEL = "qwen2.5:7b"

# 知识库路径
NOTES_PATH = r"E:\网安\笔记"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"


def call_ai(messages, max_tokens=1024):
    """调用 Ollama API"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/chat",
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "options": {"num_predict": max_tokens}
            },
            timeout=120
        )
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            return f"API 错误: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return f"[错误] 无法连接 Ollama，请先运行: ollama serve"
    except Exception as e:
        return f"[错误] 错误: {e}"


def load_notes():
    """加载笔记（前 3000 字符）"""
    if not os.path.exists(NOTES_PATH):
        return ""
    content = ""
    try:
        for root, dirs, files in os.walk(NOTES_PATH):
            for file in files:
                if file.endswith(".md"):
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        content += f"\n\n=== {file} ===\n" + f.read()
                        if len(content) > 3000:
                            return content[:3000]
    except Exception as e:
        print(f"[警告] 读取笔记失败: {e}")
    return content[:3000]


def ctf_interactive_guide():
    """CTF 互动式引导 - 新增功能"""
    print(f"\n{'='*60}")
    print(f"   CTF 互动式引导")
    print(f"{'='*60}")
    print(f"我会一步步帮你分析，请耐心回答问题\n")

    # 第 1 步：题目类型
    print(f"[1/6] 这是什么类型的题？")
    print(f"  1. SQL 注入")
    print(f"  2. XSS（跨站脚本）")
    print(f"  3. SSRF（服务器端请求伪造）")
    print(f"  4. 文件上传")
    print(f"  5. 文件包含")
    print(f"  6. 反序列化")
    print(f"  7. 其他")
    choice = input(f"\n选择 (1-7): ").strip()

    vuln_types = {
        "1": "SQL 注入", "2": "XSS", "3": "SSRF",
        "4": "文件上传", "5": "文件包含", "6": "反序列化", "7": "其他"
    }
    vuln_type = vuln_types.get(choice, "未知")

    # 第 2 步：注入点
    print(f"\n[2/6] 注入点在哪？")
    print(f"提示：看 URL 参数、表单输入、Cookie、HTTP 头")
    inject_point = input(f"描述（如: URL 参数 id）: ").strip()

    # 第 3 步：具体 URL
    print(f"\n[3/6] 具体的 URL 或参数名？")
    print(f"示例: http://xxx.com/?id=1")
    url_info = input(f"粘贴: ").strip()

    # 第 4 步：你试了什么
    print(f"\n[4/6] 你已经试了什么？")
    print(f"提示：直接粘贴你用的 payload")
    tried_payload = input(f"payload: ").strip()

    # 第 5 步：结果怎样
    print(f"\n[5/6] 结果怎样？")
    print(f"  1. 有回显（页面显示了数据）")
    print(f"  2. 没回显，但页面状态变了（正常/报错）")
    print(f"  3. 没回显，页面没变化")
    print(f"  4. 响应时间变了（快/慢）")
    print(f"  5. 报错了，显示错误信息")
    print(f"  6. 被拦截了（WAF/防火墙）")
    result_choice = input(f"\n选择 (1-6): ").strip()

    results = {
        "1": "有回显", "2": "页面状态变化", "3": "无变化",
        "4": "响应时间变化", "5": "报错", "6": "被拦截"
    }
    result = results.get(result_choice, "未知")

    # 第 6 步：卡在哪
    print(f"\n[6/6] 你卡在哪一步？")
    print(f"  1. 不知道怎么开始")
    print(f"  2. 找不到注入点")
    print(f"  3. payload 不生效")
    print(f"  4. 猜不出表名/字段名")
    print(f"  5. 绕不过 WAF")
    print(f"  6. 拿不到数据")
    print(f"  7. 其他")
    stuck_choice = input(f"\n选择 (1-7): ").strip()

    stuck_points = {
        "1": "不知道怎么开始", "2": "找不到注入点", "3": "payload 不生效",
        "4": "猜不出表名/字段名", "5": "绕不过 WAF", "6": "拿不到数据", "7": "其他"
    }
    stuck = stuck_points.get(stuck_choice, "未知")

    # 构建上下文
    context = f"""
题目类型: {vuln_type}
注入点: {inject_point}
URL: {url_info}
已试 payload: {tried_payload}
结果: {result}
卡在: {stuck}
"""

    print(f"\n正在分析你的情况...")

    # 调用 AI
    messages = [
        {
            "role": "system",
            "content": """你是 CTF 竞赛教练，擅长引导学生解决 Web 安全题目。

你的回答风格：
1. 直接给下一步 payload（不要讲原理）
2. 如果学生 payload 不对，告诉怎么改
3. 如果卡在某个环节，给具体的解决方案
4. 不要讲教科书理论，直接实战

示例回答格式：
下一步试这个：[具体 payload]
如果不生效，可能是因为：[原因]
试试这个：[另一个 payload]"""
        },
        {
            "role": "user",
            "content": f"我正在做 CTF 题，情况如下：\n{context}\n\n给我下一步的具体 payload，不要讲原理。"
        }
    ]

    result = call_ai(messages, max_tokens=1500)
    print(f"\n{result}")


def error_troubleshooting():
    """错误排查流程 - 新增功能"""
    print(f"\n{'='*60}")
    print(f"   错误排查流程")
    print(f"{'='*60}")
    print(f"告诉我你的问题，我帮你排查\n")

    # 第 1 步：问题类型
    print(f"[1/5] 你的问题是什么？")
    print(f"  1. payload 不生效（没反应）")
    print(f"  2. 报错了（显示错误信息）")
    print(f"  3. 绕不过 WAF")
    print(f"  4. 猜不出数据")
    print(f"  5. 其他")
    problem_choice = input(f"\n选择 (1-5): ").strip()

    problems = {
        "1": "payload 不生效", "2": "报错", "3": "绕不过 WAF",
        "4": "猜不出数据", "5": "其他"
    }
    problem = problems.get(problem_choice, "其他")

    # 第 2 步：题目类型
    print(f"\n[2/5] 题目类型？")
    print(f"  1. SQL 注入")
    print(f"  2. XSS")
    print(f"  3. SSRF")
    print(f"  4. 文件上传")
    print(f"  5. 其他")
    type_choice = input(f"\n选择 (1-5): ").strip()

    types = {"1": "SQL 注入", "2": "XSS", "3": "SSRF", "4": "文件上传", "5": "其他"}
    vuln_type = types.get(type_choice, "其他")

    # 第 3 步：你的 payload
    print(f"\n[3/5] 你用的 payload 是什么？")
    print(f"直接粘贴，多行也可以")
    payload_lines = []
    print(f"输入空行结束:")
    while True:
        line = input()
        if not line:
            break
        payload_lines.append(line)
    payload = "\n".join(payload_lines)

    # 第 4 步：错误信息
    print(f"\n[4/5] 有错误信息吗？")
    print(f"直接粘贴，没有就回车跳过")
    error_msg = input(f"错误信息: ").strip()

    # 第 5 步：预期结果
    print(f"\n[5/5] 你期望的结果是什么？")
    print(f"如: 拿到 flag、绕过 WAF、显示数据")
    expected = input(f"期望: ").strip()

    # 构建上下文
    context = f"""
问题: {problem}
题目类型: {vuln_type}
我的 payload: {payload}
错误信息: {error_msg or '无'}
期望结果: {expected}
"""

    print(f"\n正在排查...")

    # 调用 AI
    messages = [
        {
            "role": "system",
            "content": """你是 Web 安全专家，擅长排查漏洞利用中的问题。

你的回答风格：
1. 先分析可能的原因（列举 2-3 个）
2. 给具体的解决方案（不要讲原理）
3. 给修改后的 payload（直接能用）

常见问题排查思路：
- payload 不生效 → 闭合方式、编码、过滤
- 报错 → 语法错误、权限问题、函数禁用
- 绕不过 WAF → 编码、大小写、注释、替代函数
- 猜不出数据 → 字典、自动化脚本、手工验证"""
        },
        {
            "role": "user",
            "content": f"帮我排查这个问题：\n{context}"
        }
    ]

    result = call_ai(messages, max_tokens=1500)
    print(f"\n{result}")


def code_audit():
    """代码审计 - 支持多行粘贴 + 文件读取"""
    print("\n" + "="*50 + "\n    [ 代码审计 ]\n" + "="*50)
    print(f"选择输入方式:")
    print(f"  1. 手动粘贴（适合短代码）")
    print(f"  2. 从文件读取（推荐，多行/长代码）")
    choice = input(f"\n选择 (1-2): ").strip()

    if choice == "2":
        # 文件读取模式
        file_path = input(f"代码文件路径 (如 E:\\test\\vuln.php): ").strip()
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            print(f"[OK] 已读取文件: {len(code)} 字符")
        except Exception as e:
            print(f"[错误] 读取失败: {e}")
            return
    else:
        # 多行粘贴模式
        print(f"可直接粘贴多行代码，结束方式:")
        print(f"  - 输入 EOF 按回车")
        print(f"  - 输入空行两次（连按两次回车）\n")

        lines = []
        empty_count = 0

        while True:
            try:
                line = input()
            except EOFError:
                break

            # EOF 结束
            if line.strip().upper() == 'EOF':
                break

            # 空行计数
            if not line.strip():
                empty_count += 1
                if empty_count >= 2:
                    if lines and not lines[-1]:
                        lines.pop()
                    break
            else:
                empty_count = 0
                lines.append(line)

        code = "\n".join(lines)

        if not code.strip():
            print(f"[错误] 没收到任何代码")
            return

    print(f"\n审计中...")
    messages = [
        {"role": "system", "content": "你是网络安全专家，专门做代码审计。找出漏洞并给出修复建议。"},
        {"role": "user", "content": f"审计这段代码：\n\n{code}"}
    ]
    result = call_ai(messages, max_tokens=1500)
    print(f"\n{result}")


def generate_report():
    """报告生成"""
    print("\n" + "="*50 + "\n    [ 报告生成 ]\n" + "="*50)
    vuln = input(f"漏洞类型 (如: SQL注入): ").strip()
    target = input(f"测试目标 (可空): ").strip()

    if not vuln:
        return

    print(f"\n生成中...")
    messages = [
        {"role": "system", "content": "你是渗透测试专家。生成专业的渗透测试报告。"},
        {"role": "user", "content": f"生成 {vuln} 漏洞的渗透测试报告。目标：{target or '未指定'}\n\n包含：项目概述、测试方法、漏洞详情、风险等级、修复建议"}
    ]
    result = call_ai(messages, max_tokens=2000)
    print(f"\n{result}")


def generate_payload():
    """Payload 生成"""
    print("\n" + "="*50 + "\n    [ Payload 生成 ]\n" + "="*50)
    vuln_type = input(f"漏洞类型 (如: SQL注入, XSS): ").strip()
    bypass = input(f"需要绕过 WAF? (y/n): ").strip().lower() == "y"

    if not vuln_type:
        return

    print(f"\n生成中...")
    waf_text = "，包含绕过 WAF 的高级版本" if bypass else ""
    messages = [
        {"role": "system", "content": "你是渗透测试专家。生成实际可用的 Payload，并解释原理。"},
        {"role": "user", "content": f"生成 {vuln_type} 的常用 Payload{waf_text}。每个 Payload 都要解释原理和适用场景。"}
    ]
    result = call_ai(messages, max_tokens=2000)
    print(f"\n{result}")


def knowledge_qa():
    """知识库问答"""
    print("\n" + "="*50 + "\n    [ 知识库问答 ]\n" + "="*50)
    print(f"读取笔记中: {NOTES_PATH}")
    notes = load_notes()

    if not notes:
        print(f"[错误] 没找到笔记，请确认路径: {NOTES_PATH}")
        return

    print(f"[OK] 已加载 {len(notes)} 字符的笔记")
    question = input(f"\n你的问题: ").strip()

    if not question:
        return

    print(f"\n思考中...")
    messages = [
        {"role": "system", "content": f"你是网络安全助手。基于以下笔记回答问题：\n\n{notes}"},
        {"role": "user", "content": question}
    ]
    result = call_ai(messages, max_tokens=1500)
    print(f"\n{result}")


def free_chat():
    """自由对话"""
    print("\n" + "="*50 + "\n    [ 自由对话 ]\n" + "="*50)
    print(f"直接问问题，输入 'back' 返回菜单:")

    messages = [
        {"role": "system", "content": "你是网络安全专家，可以回答任何网安问题。"}
    ]

    while True:
        user_input = input(f"\n你: ").strip()
        if user_input.lower() in ['back', 'b', '退出']:
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        print(f"\nAI: ", end="", flush=True)
        result = call_ai(messages, max_tokens=1500)
        print(result)
        messages.append({"role": "assistant", "content": result})


def ai_agent_mode():
    """AI Agent 模式 - 让 AI 自主执行命令"""
    import subprocess
    import json

    print(f"\n{'='*60}")
    print(f"   AI Agent 自动执行模式")
    print(f"{'='*60}")
    print(f"AI 会自己思考并执行命令，每步需要你确认")
    print(f"支持: sqlmap, curl, Python 脚本, PowerShell 命令")
    print(f"安全限制: 不执行 rm/del/format 等危险命令\n")

    # 收集目标信息
    print(f"[Step 1] 告诉我你的目标")
    goal = input(f"目标 (如: 用 sqlmap 跑 URL 拿 flag): ").strip()
    if not goal:
        return

    url = input(f"URL (可空): ").strip()
    extra_info = input(f"其他信息 (可空): ").strip()

    # 构建上下文
    context = f"""
目标: {goal}
URL: {url or '未提供'}
其他信息: {extra_info or '无'}
"""

    # Agent 对话历史
    messages = [
        {
            "role": "system",
            "content": """你是渗透测试 AI Agent，可以自主执行命令完成任务。

你的工作方式：
1. 分析目标，生成第一条命令（JSON 格式）
2. 看命令输出，决定下一步
3. 循环直到目标完成

命令格式（必须是 JSON）：
```json
{
  "thinking": "我的分析...",
  "command": "具体命令",
  "reason": "为什么要执行"
}
```

安全规则：
- 只执行渗透测试命令（sqlmap, curl, python, nmap 等）
- 不执行危险命令（rm -rf, del, format, shutdown 等）
- 每次只执行一条命令
- 如果不确定，先询问用户

如果任务完成，输出：
```json
{
  "thinking": "任务已完成",
  "command": "DONE",
  "result": "最终结果"
}
```
"""
        },
        {
            "role": "user",
            "content": f"我的目标：{context}\n\n请生成第一条命令（JSON 格式）"
        }
    ]

    # Agent 循环
    max_steps = 10  # 最多 10 步
    step = 0

    while step < max_steps:
        step += 1
        print(f"\n{'─'*60}")
        print(f"  Step {step}/{max_steps}")
        print(f"{'─'*60}")

        # 调用 AI 思考
        print(f"🤖 AI 思考中...")
        ai_response = call_ai(messages, max_tokens=800)

        if "❌" in ai_response or "错误" in ai_response:
            print(f"{ai_response}")
            break

        # 解析 JSON
        try:
            # 提取 JSON 块
            if "```json" in ai_response:
                json_str = ai_response.split("```json")[1].split("```")[0].strip()
            elif "```" in ai_response:
                json_str = ai_response.split("```")[1].split("```")[0].strip()
            else:
                json_str = ai_response.strip()

            cmd_obj = json.loads(json_str)
        except json.JSONDecodeError:
            print(f"[错误] AI 返回格式错误，无法解析 JSON")
            print(f"AI 原始回答:\n{ai_response}")
            break

        # 显示 AI 思考
        thinking = cmd_obj.get("thinking", "")
        command = cmd_obj.get("command", "")
        reason = cmd_obj.get("reason", "")
        result = cmd_obj.get("result", "")

        print(f"\nAI 分析:")
        print(f"{thinking}")
        if reason:
            print(f"\n📋 原因: {reason}")

        # 检查是否完成
        if command == "DONE":
            print(f"\n{'='*60}")
            print(f"  [OK] 任务完成！")
            print(f"{'='*60}")
            if result:
                print(f"\n{result}")
            break

        # 安全检查
        dangerous_keywords = ["rm -rf", "del /", "format", "shutdown", "rmdir /s", "rd /s", ">"]
        if any(kw in command.lower() for kw in dangerous_keywords):
            print(f"[错误] 危险命令，拒绝执行: {command}")
            break

        # 显示命令，请确认
        print(f"\n[命令] 要执行的命令:")
        print(f"{command}")

        confirm = input(f"\n执行吗？(y=执行 / n=跳过 / stop=停止): ").strip().lower()

        if confirm == "stop":
            print(f"[错误] 已停止")
            break
        elif confirm != "y":
            print(f"[警告] 跳过此命令")
            messages.append({"role": "assistant", "content": ai_response})
            messages.append({"role": "user", "content": "用户跳过了这个命令，请生成其他方案"})
            continue

        # 执行命令
        print(f"\n执行中...")
        try:
            # Windows 下用 PowerShell
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,  # 2 分钟超时
                encoding="utf-8",
                errors="ignore"
            )
            output = result.stdout + result.stderr
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            output = "命令执行超时（120秒）"
            exit_code = -1
        except Exception as e:
            output = f"执行失败: {e}"
            exit_code = -1

        # 显示输出（截断）
        if len(output) > 2000:
            display_output = output[:2000] + "\n...[输出太长，已截断]..."
        else:
            display_output = output

        print(f"\n[输出] 命令输出:")
        print(f"{display_output}")
        print(f"退出码: {exit_code}")

        # 把结果喂回 AI
        messages.append({"role": "assistant", "content": ai_response})
        messages.append({
            "role": "user",
            "content": f"""命令已执行，结果如下：
退出码: {exit_code}
输出:
{output}

请根据结果决定下一步（如果已完成，返回 command=DONE）"""
        })

    if step >= max_steps:
        print(f"\n[警告] 达到最大步数（{max_steps}），任务未完成")


def vuln_explain():
    """漏洞原理讲解 - 新功能"""
    print(f"\n{'='*50}")
    print(f"漏洞原理讲解")
    print(f"{'='*50}")
    print(f"支持的漏洞类型:")
    print(f"  SQL注入  XSS  CSRF  SSRF  文件上传")
    print(f"  文件包含  反序列化  命令注入  逻辑漏洞")
    print(f"  XXE  SSTI  LFI  RFI  条件竞争")
    print()

    vuln_type = input(f"漏洞类型（或直接描述，如'SQL注入原理'）: ").strip()
    if not vuln_type:
        return

    # 可选：输入靶场名称
    target = input(f"结合哪个靶场/题目？（可空）: ").strip()

    print(f"\n[AI 分析中...]")
    messages = [
        {
            "role": "system",
            "content": """你是网络安全讲师，擅长用通俗易懂的方式讲解漏洞原理。

回答风格：
- 先用一句话说清楚是什么
- 画一个简单的流程图（用文字箭头）
- 举一个生活中的类比
- 说清楚危害等级
- 最后给一个最简单的 payload 示例
- 控制在 500 字以内，言简意赅

不要讲太多废话，不要罗列一堆防护措施。"""
        },
        {
            "role": "user",
            "content": f"讲解 {vuln_type} 的原理{'，结合 ' + target if target else ''}"
        }
    ]
    result = call_ai(messages, max_tokens=800)
    print(f"\n{result}")


def tool_cheatsheet():
    """工具命令速查 - 新功能"""
    print(f"\n{'='*50}")
    print(f"工具命令速查")
    print(f"{'='*50}")
    print(f"支持的工具:")
    print(f"  sqlmap  nmap  dirb  gobuster  hydra")
    print(f"  burp  wfuzz  xsstrike  commix  john")
    print(f"  hashcat  gobuster  ffuf  nuclei")
    print()

    tool = input(f"工具名称: ").strip()
    if not tool:
        return

    task = input(f"要做什么？（如：扫目录、爆破密码、扫注入）: ").strip()
    target = input(f"目标URL或IP（可空）: ").strip()

    print(f"\n[AI 生成命令...]")
    messages = [
        {
            "role": "system",
            "content": """你是渗透测试专家，擅长给出实用的一行命令。

回答风格：
- 直接给 1-3 个最常用的命令
- 每个命令后面加一行注释说明参数
- 如果有多个选项，简要说明区别
- 控制在 300 字以内
- 如果是 Windows 命令，用 PowerShell 语法"""
        },
        {
            "role": "user",
            "content": f"给出 {tool} 的常用命令，任务: {task or '通用'}{'，目标: ' + target if target else ''}"
        }
    ]
    result = call_ai(messages, max_tokens=600)
    print(f"\n{result}")


def show_banner():
    banner = r"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║    ▓█████  ██▓     ██▓  ██████ ▓█████  ▄▄▄       ██▀███      ║
    ║    ▓█   ▀ ▓██▒    ▓██▒▒██    ▒ ▓█   ▀ ▒████▄    ▓██ ▒ ██▒    ║
    ║    ▒███   ▒██░    ▒██▒░ ▓██▄   ▒███   ▒██  ▀█▄  ▓██ ░▄█ ▒    ║
    ║    ▒▓█  ▄ ▒██░    ░██░  ▒   ██▒▒▓█  ▄ ░██▄▄▄▄██ ▒██▀▀█▄      ║
    ║    ░▒████▒░██████▒░██░▒██████▒▒░▒████▒ ▓█   ▓██▒░██▓ ▒██▒    ║
    ║    ░░ ▒░ ░░ ▒░▓  ░░▓  ▒ ▒▓▒ ▒ ░░░ ▒░ ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░    ║
    ║     ░ ░  ░░ ░ ▒  ░ ▒ ░░ ░▒  ░ ░ ░ ░  ░  ▒   ▒▒ ░  ░▒ ░ ▒░    ║
    ║       ░     ░ ░    ▒ ░░  ░  ░     ░     ░   ▒     ░░   ░     ║
    ║       ░  ░    ░  ░ ░        ░     ░  ░      ░  ░   ░         ║
    ║                                                               ║
    ║              [  CYBERSECURITY AI ASSISTANT  ]                 ║
    ║                         v4.0                                  ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)



def main():
    """主菜单 - 实战频率排序"""
    show_banner()
    # 检查 Ollama
    print(f"正在检查 Ollama...")
    try:
        r = requests.get(f"{OLLAMA_URL}/tags", timeout=5)
        if r.status_code != 200:
            raise Exception()
    except:
        print("[错误] Ollama 没运行！请先执行: ollama serve")
        input("    [ 按回车退出 ]")
        return

    print(f"[OK] Ollama 已连接，模型: {MODEL}")

    while True:
        print(r"""
    ┌──────────────────────────────────────────────────────────────┐
    │  [ 功能模块 ]                                                 │
    ├──────────────────────────────────────────────────────────────┤
    │  [1] 自由对话          >> 直接问任何问题                     │
    │  [2] Payload 生成      >> 查常见漏洞的 payload               │
    │  [3] 漏洞原理讲解      >> 搞懂漏洞是什么                     │
    │  [4] 工具命令速查      >> 查工具怎么用                       │
    │  [5] 代码审计          >> 分析源码漏洞                       │
    │  [6] CTF 互动引导      >> 一步步带你做 CTF                   │
    │  [7] 错误排查          >> payload 不生效？帮你排查           │
    │  [8] 知识库问答        >> 读你的笔记回答                     │
    │  [9] AI Agent          >> AI 自动跑命令                      │
    │  [10] 报告生成         >> 生成渗透报告                       │
    ├──────────────────────────────────────────────────────────────┤
    │  [0] 退出系统                                                │
    └──────────────────────────────────────────────────────────────┘
        """)
        choice = input("    >> 选择 [0-10]: ").strip()

        if choice == "1":
            free_chat()
        elif choice == "2":
            generate_payload()
        elif choice == "3":
            vuln_explain()
        elif choice == "4":
            tool_cheatsheet()
        elif choice == "5":
            code_audit()
        elif choice == "6":
            ctf_interactive_guide()
        elif choice == "7":
            error_troubleshooting()
        elif choice == "8":
            knowledge_qa()
        elif choice == "9":
            ai_agent_mode()
        elif choice == "10":
            generate_report()
        elif choice == "0":
            print(f"\n再见！")
            break
        else:
            print(f"无效选择")

        input(f"\n按回车继续...")


if __name__ == "__main__":
    main()

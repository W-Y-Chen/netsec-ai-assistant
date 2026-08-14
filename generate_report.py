# 报告生成功能
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "Qwen/Qwen2.5-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

def generate_report(vulnerability, target=""):
    messages = [
        {"role": "system", "content": "You are a penetration testing expert. Generate a professional penetration testing report."},
        {"role": "user", "content": f"生成一份 {vulnerability} 漏洞的渗透测试报告，目标：{target}"}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=1024, do_sample=True, temperature=0.7)
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return response.split("assistant")[-1].strip() if "assistant" in response else response

# 使用示例
print(generate_report("SQL注入", "电商网站用户登录页面"))

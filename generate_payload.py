# Payload 生成功能
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

def generate_payload(vuln_type, bypass_waf=False):
    waf_text = "，包括绕过 WAF 的高级版本" if bypass_waf else ""
    messages = [
        {"role": "system", "content": "You are a penetration testing expert. Generate practical payloads with explanations."},
        {"role": "user", "content": f"生成 {vuln_type} 的常用 payload{waf_text}。包括基础版和高级版本，并解释每个 payload 的原理。"}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=1024, do_sample=True, temperature=0.7)
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return response.split("assistant")[-1].strip() if "assistant" in response else response

# 使用示例
print(generate_payload("SQL注入", bypass_waf=True))

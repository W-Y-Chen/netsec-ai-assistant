# 代码审计功能
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

def code_audit(code):
    messages = [
        {"role": "system", "content": "You are a cybersecurity expert specializing in code audit and vulnerability analysis."},
        {"role": "user", "content": f"审计这段代码，找出漏洞：{code}"}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.7)
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return response.split("assistant")[-1].strip() if "assistant" in response else response

# 使用示例
code = "<?php echo \$_GET['id']; ?>"
print(code_audit(code))

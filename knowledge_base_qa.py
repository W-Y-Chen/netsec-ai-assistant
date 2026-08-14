# 知识库问答功能
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

def load_notes(notes_path):
    with open(notes_path, 'r', encoding='utf-8') as f:
        return f.read()

def kb_qa(question, notes_path="all_notes.txt"):
    notes = load_notes(notes_path)[:3000]  # 取前3000字符
    messages = [
        {"role": "system", "content": f"You are a cybersecurity assistant. Use the following notes to answer questions:\n\n{notes}"},
        {"role": "user", "content": question}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer([text], return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.7)
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return response.split("assistant")[-1].strip() if "assistant" in response else response

# 使用示例
print(kb_qa("根据我的笔记，反射型 XSS 和存储型 XSS 有什么区别？"))

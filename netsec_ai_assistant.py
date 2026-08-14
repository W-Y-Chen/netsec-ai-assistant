# 网安 AI 助手 - 4合1 综合版
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class NetSecAI:
    def __init__(self):
        print("Loading Qwen2.5-7B model...")
        self.model_name = "Qwen/Qwen2.5-7B-Instruct"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        print("Model loaded!")
    
    def _generate(self, messages, max_tokens=512):
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens, do_sample=True, temperature=0.7)
        response = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        return response.split("assistant")[-1].strip() if "assistant" in response else response
    
    def code_audit(self, code):
        """代码审计"""
        messages = [
            {"role": "system", "content": "You are a cybersecurity expert specializing in code audit."},
            {"role": "user", "content": f"审计这段代码，找出漏洞并给出修复建议：\n\n{code}"}
        ]
        return self._generate(messages, max_tokens=1024)
    
    def generate_report(self, vulnerability, target=""):
        """报告生成"""
        messages = [
            {"role": "system", "content": "You are a penetration testing expert."},
            {"role": "user", "content": f"生成一份 {vulnerability} 漏洞的渗透测试报告。目标：{target}"}
        ]
        return self._generate(messages, max_tokens=1024)
    
    def generate_payload(self, vuln_type, bypass_waf=False):
        """Payload 生成"""
        waf_text = "，包括绕过 WAF 的高级版本" if bypass_waf else ""
        messages = [
            {"role": "system", "content": "You are a penetration testing expert. Generate payloads with explanations."},
            {"role": "user", "content": f"生成 {vuln_type} 的常用 payload{waf_text}，并解释原理。"}
        ]
        return self._generate(messages, max_tokens=1024)
    
    def kb_qa(self, question, notes=""):
        """知识库问答"""
        context = f"\n\n参考笔记：\n{notes[:2000]}" if notes else ""
        messages = [
            {"role": "system", "content": f"You are a cybersecurity assistant.{context}"},
            {"role": "user", "content": question}
        ]
        return self._generate(messages, max_tokens=512)

# 使用示例
if __name__ == "__main__":
    ai = NetSecAI()
    
    # 测试代码审计
    print("\n=== 代码审计 ===")
    print(ai.code_audit("<?php echo \$_GET['id']; ?>"))
    
    # 测试报告生成
    print("\n=== 报告生成 ===")
    print(ai.generate_report("SQL注入", "电商网站"))
    
    # 测试 Payload 生成
    print("\n=== Payload 生成 ===")
    print(ai.generate_payload("SQL注入", bypass_waf=True))

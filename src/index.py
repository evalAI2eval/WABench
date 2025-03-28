import ollama
import os 
import json 
import time
# MODELS = ['llama3.2', 'deepseek-r1']
MODELS = ['llama3.2', 'llama3.1']

input_file = '../dataset/first_task_tests.json'

if not os.path.exists(input_file):
    print(f"Input file '{input_file}' not found")
    exit(1)
else:
    print(f"Input file '{input_file}' found")
    
with open(input_file, 'r') as f:
    api_requests = json.load(f)


def make_prompt(log):
    return f"""
Given the following HTTP request log: 
{log}
Can this request be used in web attack?
Options for attack_type: [sqli, xss, lfi, rfi, file_upload, none]

Respond in *valid* JSON format:
{{ "is_attackable": true/false, "attack_type": "..." }}
"""

# === Initialize result containers ===
model_results = {model: [] for model in MODELS}

# === Main loop ===
for i, entry in enumerate(api_requests):
    log = entry["log"]
    # prompt = make_prompt(log)
    prompt = make_prompt(entry)

    print(f"\n Analyzing request {i+1}/{len(api_requests)}")

    for model in MODELS:
        try:
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response["message"]["content"]
            print(f"[{model}] Response:\n{content}")

            parsed = json.loads(content)
        except Exception as e:
            print(f"[!] Error with model {model} on entry {i}: {e}")
            parsed = {"is_attackable": None, "attack_type": "error"}

        model_results[model].append({
            "log": log,
            "model": model,
            **parsed
        })
        time.sleep(0.3)  # prevent overload (optional)

# === Save results ===
for model in MODELS:
    output_file = f"results_{model.replace(':', '_')}.json"
    with open(output_file, "w") as f:
        json.dump(model_results[model], f, indent=2)

print("\n✅ Done! Results saved for:")
for model in MODELS:
    print(f"→ {model}: results_{model.replace(':', '_')}.json")

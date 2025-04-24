import ollama
import os 
import json 
import time
import utils
import evaluation

# MODELS = ['llama3.2', 'deepseek-r1']
MODELS = ['llama3.2']
input_file = '../dataset/dataset.json'

if not os.path.exists(input_file):
    print(f"Input file '{input_file}' not found")
    exit(1)
else:
    print(f"Input file '{input_file}' found")
    
with open(input_file, 'r') as f:
    api_requests = json.load(f)




def make_prompt(log):
    return f"""
You are a cybersecurity expert analyzing HTTP requests to determine what is the security attack from malicious log.

Given the following HTTP request, give me answer if the attack is "sqli", "xss", "lfi", "rfi", "xxe", "rce","Command Injection","Header Smuggling","Parameter Tampering" I only need single word answer I don't need any explanations.

HTTP Request:
{log}

Your response should be one word only.

"""

# === Initialize result containers ===
model_results = {model: [] for model in MODELS}

ground_truth = []
model_output = []
# === Main loop ===
for i, entry in enumerate(api_requests):
    if entry.get("label") == "benign":
        continue;
    log = utils.build_http_request(entry.get("log", {}))
    ground_truth.append(entry.get("attack"))
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
            if not content or content == "error":
                content = None
            model_output.append(content)
            print(f"[{model}] Response:\n{content}")


            parsed = json.loads(content)
        except Exception as e:
            # print(f"[!] Error with model {model} on entry {i}: {e}")
            # parsed = {"is_attackable": None, "attack_type": "error"}
            parsed = {"label": "None"}

        model_results[model].append({
            "log": log,
            "model": model,
            **parsed
        })
        time.sleep(0.3)  # prevent overload (optional)

# === Save results ===
print('GROUND TRUTH___')
print(ground_truth)
print('MODEL RESPONSE__')
print(model_output)
eval = evaluation.Evaluation()
evl_result = eval.evaluate_from_lists(ground_truth=ground_truth, model_output=model_output, choice="acc")
print("Accuracy ==> {} ".format(evl_result))
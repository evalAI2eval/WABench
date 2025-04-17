import ollama
import os 
import json 
import time
import utils
import evaluation

# MODELS = ['llama3.2', 'deepseek-r1']
MODELS = ['llama3.2']
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
You are a cybersecurity expert analyzing HTTP requests to determine whether they are part of a cyber attack or normal web traffic.

Given the following HTTP request, give me answer if it's "benign" or "malicious". I only need single word answer I don't need any explanations.

HTTP Request:
{log}

Your response should be one word only: "benign" or "malicious".

"""

# === Initialize result containers ===
model_results = {model: [] for model in MODELS}

ground_truth = []
model_output = []
# === Main loop ===
for i, entry in enumerate(api_requests):
    log = utils.build_http_request(entry.get("log", {}))
    ground_truth.append(entry.get("label"))
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
for model in MODELS:
    output_file = f"results_{model.replace(':', '_')}.json"
    with open(output_file, "w") as f:
        json.dump(model_results[model], f, indent=2)
print('GROUND TRUTH___')
print(ground_truth)
print('MODEL RESPONSE__')
print(model_output)
print("\n✅ Done! Results saved for:")
eval = evaluation.Evaluation()
evl_result = eval.evaluate_from_lists(ground_truth=ground_truth, model_output=model_output)
print(eval)
eval.plot_metrics_figure(evl_result)
for model in MODELS:
    print(f"→ {model}: results_{model.replace(':', '_')}.json")

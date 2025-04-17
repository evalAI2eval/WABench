import ollama
import os 
import json 
import time
import utils
import evaluation
from explaination import Explanation
# MODELS = ['llama3.2', 'deepseek-r1']
MODELS = ['llama3.2']
input_file = '../dataset/for_perturbations.json'

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

Given the following HTTP request, give me answer if the attack is "sqli", "xss", "lfi", "rfi", "xxe", "rce". I only need single word answer I don't need any explanations.

HTTP Request:
{log}

Your response should be one word only.

"""

# === Initialize result containers ===
model_results = {model: [] for model in MODELS}
import pdb;pdb.set_trace()

# Assuming `api_requests[0]` is the XSS example

xss_log_dict = api_requests[0]['log']
# Run token perturbation on that log
per_list = Explanation.generate_perturbations(xss_log_dict)
    
model_output = []
ground_truth = (api_requests[0].get("label"))
print("Ground Truth Label ==> " + ground_truth)
for i, entry in enumerate(per_list):
    log = utils.build_http_request(entry)
    # prompt = make_prompt(log)
    prompt = make_prompt(entry)
    #print(log)
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

        time.sleep(0.3)  # prevent overload (optional)       


eval = evaluation.Evaluation()
flip_results, weight_results = eval.evaluate_perturbation_effects(
    model_outputs=model_output,
    perturbations=per_list,
    ground_truth="sqli"
)
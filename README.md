# WABench: Web Application Attack Benchmark for LLMs

## Overview
WABench is a benchmarking suite designed to evaluate the ability of Large Language Models (LLMs) to detect and classify web application attacks from HTTP requests. 

The current focus is on analyzing attacks such as:
- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Local File Inclusion (LFI)
- Command Injection
- header smuggling attack

WABench utilizes controlled perturbation techniques to test model robustness against token-level changes in the input, providing a fine-grained evaluation of LLM interpretability and stability in a cybersecurity context.

---

## Project Structure
```bash
WABench/
├── dataset/                    
|   ├── dataset.json           # Datasets used for evaluation
│   └── for_perturbations.json # For token perturbation explanation
├── src/
|   ├── first_task.py          # Run the first task
|   ├── second_task.py         # Run the second task
|   ├── explaination_task.py   # Run the explaination task
│   ├── explanation.py         # Perturbation generation module
│   ├── evaluation.py          # Evaluation metrics and analysis
│   ├── utils.py               # Utilities for building HTTP requests and prompts
├── results/                   # Output results and reports
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/evalexplainAI/WABench.git
cd WABench
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

Run the benchmark script:
```bash
python src/first_task.py
python src/second_task.py
python src/explanation_task.py
```

You can adjust configurations such as:
- Selected LLM models (e.g., LLaMA 3, DeepSeek)
- Perturbation strategies
- Dataset path

Example inside `first_task.py`:
```python
MODELS = ['llama3.2']
input_file = '../dataset/dataset.json'
```

---

## Tasks Details
### Classify an HTTP traffic (GET/POST)  as benign or malicious 
first we take each json object from the list, the following is example of the object before processing
```
{
        "log": {
            "Method": "GET",
            "User-Agent": "Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.8 (like Gecko)",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept": "text/xml,application/xml,application/xhtml\uc669\ufffd,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
            "Accept-encoding": "x-gzip, x-deflate, gzip, deflate",
            "Accept-charset": "utf-8, utf-8;q=0.5, *;q=0.5",
            "language": "en",
            "host": "localhost:8080",
            "cookie": "JSESSIONID=1F767F17239C9B670A39E9B10C3825F4",
            "content-type": "",
            "connection": "close",
            "lenght": "",
            "content": "",
            "URL": "http://localhost:8080/tienda1/index.jsp HTTP/1.1"
        },
        "label": "Benign",
        "attack": "None"
    }
```
Then we parse only the value of the log using as the following output
```
GET /tienda1/index.jsp HTTP/1.1
Host: localhost:8080
User-Agent: Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.8 (like Gecko)
Pragma: no-cache
Cache-Control: no-cache
Accept: text/xml,application/xml,application/xhtml\uc669\ufffd,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
Accept-Encoding: x-gzip, x-deflate, gzip, deflate
Accept-Charset: utf-8, utf-8;q=0.5, *;q=0.5
Language: en
Cookie: JSESSIONID=1F767F17239C9B670A39E9B10C3825F4
Connection: close
```
And we combine it with our prompt which is 
```
You are a cybersecurity expert analyzing HTTP requests to determine whether they are part of a cyber attack or normal web traffic.

Given the following HTTP request, give me answer if it's "benign" or "malicious". I only need single word answer I don't need any explanations.

HTTP Request:
{log}

Your response should be one word only: "benign" or "malicious".
```
So the final prompt we send to the model is 

```
You are a cybersecurity expert analyzing HTTP requests to determine whether they are part of a cyber attack or normal web traffic.

Given the following HTTP request, give me answer if it's "benign" or "malicious". I only need single word answer I don't need any explanations.

HTTP Request:
GET /tienda1/index.jsp HTTP/1.1
Host: localhost:8080
User-Agent: Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.8 (like Gecko)
Pragma: no-cache
Cache-Control: no-cache
Accept: text/xml,application/xml,application/xhtml\uc669\ufffd,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
Accept-Encoding: x-gzip, x-deflate, gzip, deflate
Accept-Charset: utf-8, utf-8;q=0.5, *;q=0.5
Language: en
Cookie: JSESSIONID=1F767F17239C9B670A39E9B10C3825F4
Connection: close

Your response should be one word only: "benign" or "malicious".
```

When we get the output we store it for evaluation functions.

### Classify the malicious logs based on the attack type
We do the same as the previous details but with different prompt like this
```
You are a cybersecurity expert analyzing HTTP requests to determine what is the security attack from malicious log.

Given the following HTTP request, give me answer if the attack is "sqli", "xss", "lfi", "rfi", "xxe", "rce". I only need single word answer I don't need any explanations.

HTTP Request:
{log}

Your response should be one word only.
```

## Perturbation Technique Details

Perturbations are created by progressively removing important parts of a malicious payload to analyze the model's resilience. For example:

Original Payload (SQLi):
```text
' OR '1'='1' --
```

Generated Variations:
- `' OR 1=1--`
- `' OR 1=1`
- `' OR 1`
- `' OR`
- `' `
- `'`

Each perturbed variant is tested separately, and its effect on model classification is recorded.

---

## Evaluation Metrics

- Accuracy =>  Measures the overall correctness of the model.
- Recall =>  Tells you how many of the actual Malicious samples were correctly detected by the model.
- Precision =>  Tells you how many of the samples labeled as Malicious by the model were actually Malicious.
- F1 =>  Provides a balance between Precision and Recall, especially useful when they are in trade-off.

---
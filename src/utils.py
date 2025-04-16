import json

def build_http_request(log):
    # Extract Method, URL, and HTTP version
    method = log.get("Method", "GET")
    full_url = log.get("URL", "")

    # Split the URL and HTTP version
    if " HTTP/" in full_url:
        url_path, http_version = full_url.split(" HTTP/")
        http_version = "HTTP/" + http_version
    else:
        url_path = full_url
        http_version = "HTTP/1.1"

    # Start building request
    request_lines = [f"{method} {url_path} {http_version}"]

    # Headers to exclude from body content
    excluded_headers = {"Method", "URL", "content", "lenght"}  # 'lenght' is assumed to be a typo for 'length'

    for key, value in log.items():
        if key not in excluded_headers and value:
            # Format keys properly for headers
            header_name = key.replace("_", "-").title()
            request_lines.append(f"{header_name}: {value}")

    # Add an empty line before the body
    request_lines.append("")

    # If there's body content
    body = log.get("content", "")
    if body:
        request_lines.append(body)

    return "\n".join(request_lines)

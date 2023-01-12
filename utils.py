from detoxify import Detoxify

def get_ip_address(request) -> str:
    req_headers = request.META
    x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for_value:
        ip_addr = x_forwarded_for_value.split(',')[-1].strip()
    else:
        ip_addr = req_headers.get('REMOTE_ADDR')
    return ip_addr


predictor = Detoxify('original')
def check_toxicity(message: str) -> bool:
    return True if predictor.predict(message)["toxicity"] > 0.89 else False
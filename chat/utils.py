def get_ip_address(request):
    req_headers = request.META
    try:
        x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(',')[-1].strip()
        else:
            ip_addr = req_headers.get('REMOTE_ADDR')
    except e:
        print("Error getting the ip address from request")
        ip_addr = None
    return ip_addr
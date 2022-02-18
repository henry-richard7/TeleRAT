import subprocess


def get_wifi_password():
    wifi_passwords = []
    data = (
        subprocess.check_output(["netsh", "wlan", "show", "profiles"])
        .decode("utf-8")
        .split("\n")
    )
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in profiles:
        results = (
            subprocess.check_output(
                ["netsh", "wlan", "show", "profile", i, "key=clear"]
            )
            .decode("utf-8")
            .split("\n")
        )
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            wifi_passwords.append("{:<30}:  {:<}".format(i, results[0]))
        except IndexError:
            wifi_passwords.append("{:<30}:  {:<}".format(i, ""))

    return wifi_passwords

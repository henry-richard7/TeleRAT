from easygui import enterbox


def chat(msg):
    client_Message = enterbox(msg, title="Message From Hacker")
    return client_Message

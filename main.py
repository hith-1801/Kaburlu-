import socket

def Auth(nickname, channel):
    IRC.send(f"NICK {nickname}\r\n".encode("utf-8"))
    IRC.send(f"USER {nickname} 0 * :Naaradha\r\n".encode("utf-8"))
    IRC.send(f"JOIN {channel}\r\n".encode("utf-8"))

def thekickback():
    while True:
        feedback=IRC.recv(2048).decode("utf-8")
        if feedback.startswith("PING"):
            IRC.send(f"PONG{feedback.split()[1]}\r\n".encode("utf-8"))
        else:
            print(feedback)

if __name__=='__main__':
    host=input("Enter the link for server: ")
    nickname=input("Enter your nickname: ")
    channel=input("Enter the channel name which u want to enter: ")
    port=6667
    try:
        IRC=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IRC.connect((host,port))
        print("Successfully Ocnnected to Liberachat")
    except:
        print("Connection to Freenode Failed!")

    Auth(nickname, channel)
    thekickback()

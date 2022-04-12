import socket

assert url.startswith("http://") # 브라우저가 HTTP로 시작하는지 확인한 뒤
url = url[len("http://"):] # HTTP를 제거

host, path = url.split("/", 1) # 경로에서 호스트를 분리
path = "/" + path

# 소켓 옵션을 선택해서 만들기
s = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM,
    proto=socket.IPPROTO_TCP,
)

# 다른 컴퓨터에 연결하도록 알리기 위해 호스트와 포트를 준비
# example.org 연결을 설정하고, 두 컴퓨터가 데이터를 교환할 수 있게 준비함
s.connect(("example.org", 80))


# 연결완료
s.send(b"GET /index.html HTTP/1.0\r\n" + 
       b"Host: example.org\r\n\r\n") # 다른 서버에 요청

# response 를 조각으로 나누기
statusline = response.readline()
version, status, explanation = statusline.split(" ", 2)
assert status == "200", "{}: {}".format(status, explanation)

headers = {}
while True:
    line = response.readline()
    if line == "\r\n": break
    header, value = line.split(":", 1)
    headers[header.lower()] = value.strip()

body = response.read()
s.close()

# 연결, 요청, 응답 코드를 모두 모아 request 함수로 만들기
def request(url):
    
    return headers, body

    
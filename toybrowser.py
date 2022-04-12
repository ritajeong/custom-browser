import socket
import sys

# 연결, 요청, 응답 코드를 모두 모아 request 함수로 만들기
def request(url):
	assert url.startswith("http://") # 브라우저가 HTTP로 시작하는지 확인한 뒤
	url = url[len("http://"):] # HTTP를 제거

	host, path = url.split("/", 1) # 경로에서 호스트를 분리
	path = "/" + path
	port = 80

	# 소켓 옵션을 선택해서 만들기
	s = socket.socket(
		family=socket.AF_INET,
		type=socket.SOCK_STREAM,
		proto=socket.IPPROTO_TCP,
	)

	# argument로 url을 받기 위해
	request_line = f"GET {path} HTTP/1.0\r\n".encode("utf-8")
	request_headers = [
		f"Host: {host}"
	]
	header_lines = ("\r\n".join(request_headers) + "\r\n\r\n").encode("utf-8")

	# 다른 컴퓨터에 연결하도록 알리기 위해 호스트와 포트를 준비
	# example.org 연결을 설정하고, 두 컴퓨터가 데이터를 교환할 수 있게 준비함
	s.connect((host, port))

	# 연결완료
	s.send(request_line + header_lines) # 다른 서버에 요청

	# response 를 조각으로 나누기
	response = s.makefile("r", encoding="utf8", newline="\r\n")
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

	return headers, body

def load(url):
    headers, body = request(url)
    print(body)

# 메인 함수
if __name__ == "__main__":
    load(sys.argv[1])
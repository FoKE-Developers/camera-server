# Camera Server for FourCutTogether

## 설치

```sh
sudo apt install gphoto2
pip install -r requirements.txt
```

## 실행

```
./server.py
# or
python /path/to/repo/server.py
```

시스템 시작과 동시에 실행을 원하는 경우 `/etc/rc.local`에 다음과 같이 넣어놓는 것을 권장.

<img width="563" alt="image" src="https://github.com/user-attachments/assets/2eed9bc6-eb9f-4bed-bef3-ac28ac55ddb0">

(`&> /path/to/repo/log.txt` 는 log.txt 파일에 실행 로그를 저장하는 역할)

## API

### GET `/preview`

> 카메라에서 960 x 640 해상도의 MJPEG 영상을 받아와 HTTP 스트림으로 제공.
> HTML의 경우 `<img src="/preview" width="640" height="480">` 등으로 렌더링할 수 있음.

MIME Type: `multipat/x-mixed-replace`

Parameter: 요청 시 선택적으로 `?timeout=N`을 제공하면 N초 만큼 촬영 후 종료.

Response Example:
```
HTTP/1.1 200 OK
Content-Type: multipart/x-mixed-replace; boundary=frame

--frame
Content-Type: image/jpeg

<jpeg data here>
--frame
Content-Type: image/jpeg

<jpeg data here>
```
<br>

### GET `/photo`

> 카메라에서 2592 x 1728 해상도의 JPEG 사진을 즉시 촬영하여 전송.
> 초점을 맞추고 셔터 소리가 날 때까지 약 2초의 딜레이가 있음.

MIME Type: image/jpeg

Response Example:
```
HTTP/1.1 200 OK
Content-Type: image/jpeg

<jpeg data here>
```
<br>

### GET `/reset`

> 카메라 상태를 초기화. 카메라 상태로 인한 촬영 오류 시에 유용할 수 있음.

MIME Type: text/html

Response Example:
```
HTTP/1.1 200 OK
Content-Type: text/html

Camera has been reset.
```
<br>

### GET `/cmd`

> `gphoto2` 명령행 인자를 `arg` 쿼리파람으로 전송하고, 텍스트로 응답.

MIME Type: text/plain

Parameter: 요청 시 `?arg=` 뒤에 `gphoto2` 커맨드와 호환되는 1개의 인자

Response Example: `/cmd?arg=--auto-detect`
```
HTTP/1.1 200 OK
Content-Type: text/plain

Model                          Port
----------------------------------------------------------
Canon EOS 700D                 usb:001,007
```

## Reference
- https://blog.miguelgrinberg.com/post/video-streaming-with-flask
- http://www.gphoto.org/doc/manual/ref-gphoto2-cli.html
- https://mlagerberg.gitbooks.io/raspberry-pi/content/4.6-gphoto2.html
- https://medium.com/@supersjgk/building-a-live-streaming-app-using-flask-opencv-and-webrtc-8cc8b521fa44
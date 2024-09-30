# Camera Server for FourCutTogether

## install

```sh
pip install -r requirements.txt
```

## API

### GET `/preview`

> 카메라에서 960 x 640 해상도의 MJPEG 영상을 받아와 HTTP 스트림으로 제공.
> 선택적인 쿼리 파람으로 `timeout=N`을 제공하면 N초 만큼 촬영 후 종료.
> HTML의 경우 `<img src="/preview" width="640" height="480">` 등으로 렌더링할 수 있음.

MIME Type: `multipat/x-mixed-replace `

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
<br>

### GET `/cmd`

> `gphoto2` 명령행 인자를 쿼리파람으로 전송하고, 텍스트로 응답.

import subprocess

# Each preview frame is about 180 KB
READ_SIZE = 100 * 1024
SOI = b'\xff\xd8'
EOI = b'\xff\xd9'

# Kill existing gphoto2 processes to properly detect camera
def reset():
    command = ['pkill', 'gphoto2']
    subprocess.run(command)

def command(arg):
    command = ['gphoto2', arg]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    if result.returncode == 0:
        return result.stdout.decode('utf-8');

def capture_image():
    reset()
    command = ['gphoto2', '--capture-image-and-download', '--stdout']
    result = subprocess.run(command, stdout=subprocess.PIPE)
    if result.returncode == 0:
        return result.stdout;

class MjpegStream:
    def __init__(self, timeout=None):
        reset()
        # Start capturing video from gphoto2 and send it over pipe
        command = ['gphoto2', '--capture-movie', '--stdout']
        if timeout:
            command[1] += f'={timeout}s'
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10**8)
        self.buf = b''

    def get_frame(self):
        while True:
            # Read in larger chunks to avoid too many reads, but ensure full frames
            chunk = self.process.stdout.read(READ_SIZE)
            if not chunk:
                break
            self.buf += chunk

            # Look for a complete JPEG frame (starting with FFD8 and ending with FFD9)
            start = self.buf.find(SOI)  # Start of JPEG frame
            end = self.buf.find(EOI)    # End of JPEG frame

            if start != -1 and end != -1:
                end += len(EOI)
                frame = self.buf[start:end]
                self.buf = self.buf[end:]  # Remove the processed frame from the
                return frame

    def __del__(self):
        self.process.terminate()
        self.process.wait()


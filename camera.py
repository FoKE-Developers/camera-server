import subprocess

# Each preview frame is about 180 KB
READ_SIZE = 100 * 1024
SOI = b'\xff\xd8'
EOI = b'\xff\xd9'

# Kill existing gphoto2 processes to properly detect camera
def reset():
    command = ['pkill', '-9', 'gphoto2']
    subprocess.run(command)

def command(arg):
    command = ['gphoto2', arg]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    if result.returncode == 0:
        return result.stdout.decode('utf-8');

def capture_image():
    reset() # NOTE: this may interrupt movie capture
    command = ['gphoto2', '--capture-image-and-download', '--stdout']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return result.stdout;
    else:
        raise IOError(result.stderr.decode('utf-8'))

class MjpegVideo:
    process = None
    def __init__(self, timeout=None):
        # Start capturing video from gphoto2 and send it over pipe
        command = ['gphoto2', '--capture-movie', '--stdout']
        if timeout:
            command[1] += f'={timeout}s'
        if MjpegVideo.process:
            MjpegVideo.process.terminate()
            MjpegVideo.process.wait()
        MjpegVideo.process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE, bufsize=10**8)
        try:
            # collect errors occurred within 1 second
            out, err = MjpegVideo.process.communicate(timeout=1)
            if err:
                raise IOError(err.decode('utf-8'))
            if out:
                raise Warning(out.decode('utf-8'))
        except subprocess.TimeoutExpired:
            # this implies video capture has started
            pass
        self.buf = b''

    def get_frame(self):
        while True:
            # Read in larger chunks to avoid too many reads, but ensure full frames
            chunk = MjpegVideo.process.stdout.read(READ_SIZE)
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
        MjpegVideo.process.terminate()
        MjpegVideo.process.wait()


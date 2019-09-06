
# import the necessary packages
from threading import Thread
import sys
import cv2
import time

if sys,version_info >= (3, 0):
    from queue import Queue
else:
    from Queue import Queue

class WebcamVideoStream:
	def __init__(self, path, transform=None, queue_size=128):

		self.stream = cv2.VideoCapture(path)
        	self.stopped = False
        	self.transform = transform

        	self.Q = Queue(maxsize=queue_size)
		self.thread = Thread(target=self.update, args=(), daemon=True)
		self.thread.daemon = True

##		(self.grabbed, self.frame) = self.stream.read()
##                self.stopped = False

	def start(self):

##                Thread(target=self.update, args=()).start()
		self.thread.start()
		return self

	def update(self):
		while True:
			if self.stopped:
				break
                        if not self.Q.full():
                                (grabbed, frame) = self.stream.read()
                                if not grabbed:
                                        break
                        if self.transform:
                                frame = self.transform(frame)
                        self.Q.put(frame)
                else:
                        time.sleep(0.1)
                        time.sleep(0.1)
        self.stream.release
##			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		return self.Q.get()

    	def running(self):
        	return self.more() or not self.stopped

    	def more(self):
        	tries = 0
        	while self.Q.qsize() == 0 and not self.stopped and tries < 5:
                time.sleep(0.1)
                tries += 1

        return self.Q.qsize() > 0

	def stop(self):
		self.stopped = True
		self.thread.join()



'''
# import the necessary packages
from threading import Thread
import cv2

class WebcamVideoStream:
	def __init__(self, src=0):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
        	self.thread.join()
'''










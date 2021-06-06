import proto.filestream_pb2_grpc as f_pb2_grpc
import proto.filestream_pb2 as f_pb2
from concurrent import futures
import numpy as np
import grpc


CHUNK = None


class FileStream(f_pb2_grpc.FileStreamServiceServicer):
	def __init__(self):
		pass

	def FileStreamResponse(self, request_iterator, context):
		global CHUNK

		# TODO: realise here real server side streaming
		"""
		while True:
			b64e = CHUNK

			yield f_pb2.FileData(chunk = b64e)
		"""

		b64e = CHUNK

		yield f_pb2.FileData(chunk = b64e)

	def FileStreamRequest(self, request_iterator, context):
		global CHUNK

		for req in request_iterator:
			CHUNK = req.chunk

			reply = "your file is received to server successfully"
			yield f_pb2.FileResponse(msg = reply)

	
def serve():

	server = grpc.server(futures.ThreadPoolExecutor(max_workers = 500),  options=[
		('grpc.max_send_message_length', 50 * 1024 * 1024),
		('grpc.max_receive_message_length', 50 * 1024 * 1024)
      	])
	f_pb2_grpc.add_FileStreamServiceServicer_to_server(FileStream(), server)

	server.add_insecure_port('[::]:50000')

	server.start()

	print('Server started successfully')

	server.wait_for_termination()


if __name__ == '__main__':
	serve()

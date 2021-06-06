import proto.filestream_pb2_grpc as f_pb2_grpc
import proto.filestream_pb2 as f_pb2
import numpy as np
import grpc
import uuid


GUID = str(uuid.uuid4())


def stream():
	global GUID
	
	filename = r"/home/kevin/Downloads/image00001.jpg"
	chunksize = 8192

	with open(filename, "rb") as f:
		while True:
			chunk = f.read(chunksize)
			if chunk:
				
				print(f"chunk: {chunk}")
				
				# for b in chunk:
					# yield b

				message_filemetadata = []
				filemeta_object = f_pb2.FileData.FileMetadata(type = '.FILE', size = 1280, chunkid = 30)
				message_filemetadata.append(filemeta_object)

				data = f_pb2.FileData(chunk = chunk, id = GUID, meta = iter(message_filemetadata))
				
				yield data
			else:
				break


def run():
	channel = grpc.insecure_channel('127.0.0.1:50000')

	stub = f_pb2_grpc.FileStreamServiceStub(channel)
	print('Sender started successfully')

	try:
		responses = stub.FileStreamRequest(stream())
		
		for res in responses:
			if res is None:
				run()
				
			continue
	except grpc.RpcError as e:
		print("ERROR: ")
		print(e.details())
		
		run()


if __name__ == '__main__':
	run()

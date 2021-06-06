import proto.filestream_pb2_grpc as f_pb2_grpc
import proto.filestream_pb2 as f_pb2
import numpy as np
import grpc


def run():
	channel = grpc.insecure_channel('127.0.0.1:50000')

	stub = f_pb2_grpc.FileStreamServiceStub(channel)
	print('Receiver started successfully')

	while True:
		try:
			responses = stub.FileStreamResponse(f_pb2.FileRequest(msg = 'requesting file'))

			for res in responses:
				# chunk_b = np.frombuffer(res.chunk, dtype = np.uint8)

				print(res)

		except grpc.RpcError as e:
			print(e.details())
			break


if __name__ == '__main__':
	run()

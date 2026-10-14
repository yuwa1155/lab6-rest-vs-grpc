from concurrent import futures
import argparse
import base64
import io

import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


def image_size(data):
    with Image.open(io.BytesIO(data)) as img:
        return lab6_pb2.imageReply(
            width=img.width,
            height=img.height
        )


class Lab6Service(lab6_pb2_grpc.Lab6Servicer):
    def add(self, request, context):
        return lab6_pb2.addReply(sum=request.a + request.b)

    def rawimage(self, request, context):
        return image_size(request.img)

    def dotproduct(self, request, context):
        if len(request.a) != len(request.b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have the same length"
            )

        result = sum(x * y for x, y in zip(request.a, request.b))
        return lab6_pb2.dotProductReply(dotproduct=result)

    def jsonimage(self, request, context):
        data = base64.b64decode(request.img)
        return image_size(data)


def main():
    parser = argparse.ArgumentParser(description="gRPC server")
    parser.add_argument("-p", "--port", type=int, default=50051)
    args = parser.parse_args()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6Servicer_to_server(Lab6Service(), server)

    if server.add_insecure_port(f"0.0.0.0:{args.port}") == 0:
        raise RuntimeError("Could not bind server port")

    server.start()
    print(f"gRPC server running on port {args.port}", flush=True)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    main()

import argparse
import base64
import math
import random
import time

import grpc
import lab6_pb2
import lab6_pb2_grpc


def do_operation(stub, cmd, debug=False):
    if cmd == "add":
        reply = stub.add(lab6_pb2.addMsg(a=5, b=10), timeout=30)
        assert reply.sum == 15

    elif cmd == "dotProduct":
        data = lab6_pb2.dotProductMsg(
            a=[random.random() for _ in range(100)],
            b=[random.random() for _ in range(100)]
        )
        reply = stub.dotproduct(data, timeout=30)
        expected = sum(x * y for x, y in zip(data.a, data.b))
        assert math.isclose(
            reply.dotproduct, expected, rel_tol=1e-6, abs_tol=1e-5
        )

    elif cmd == "rawImage":
        with open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb") as f:
            img = f.read()
        reply = stub.rawimage(
            lab6_pb2.rawImageMsg(img=img), timeout=30
        )
        assert (reply.width, reply.height) == (3004, 1002)

    elif cmd == "jsonImage":
        with open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb") as f:
            img = f.read()
        encoded = base64.b64encode(img).decode("ascii")
        reply = stub.jsonimage(
            lab6_pb2.jsonImageMsg(img=encoded), timeout=30
        )
        assert (reply.width, reply.height) == (3004, 1002)

    if debug:
        print(reply)


def main():
    parser = argparse.ArgumentParser(description="gRPC client")
    parser.add_argument("host")
    parser.add_argument(
        "cmd", choices=["add", "rawImage", "dotProduct", "jsonImage"]
    )
    parser.add_argument("reps", type=int)
    parser.add_argument("-p", "--port", type=int, default=50051)
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    if args.reps < 1:
        parser.error("reps must be at least 1")

    addr = f"{args.host}:{args.port}"
    print(f"Running {args.reps} reps against {addr}")

    with grpc.insecure_channel(addr) as channel:
        stub = lab6_pb2_grpc.Lab6Stub(channel)

        start = time.perf_counter()
        for _ in range(args.reps):
            do_operation(stub, args.cmd, args.debug)

        elapsed = time.perf_counter() - start
        print("Took", elapsed / args.reps * 1000, "ms per operation")


if __name__ == "__main__":
    main()

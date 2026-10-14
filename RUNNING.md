# Running Lab 6

Tested with Python 3.10 on Ubuntu 22.04. Run commands from the repository directory.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The generated protobuf files are included. To regenerate them:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. lab6.proto
```

## Localhost demo

Activate the virtual environment in each terminal.

Terminal 1:
```bash
python rest-server.py
```

Terminal 2:
```bash
python grpc-server.py
```

Terminal 3:
```bash
for cmd in add rawImage dotProduct jsonImage
do
  python rest-client.py localhost "$cmd" 1 --debug
  python grpc-client.py localhost "$cmd" 1 --debug
done
```

REST uses port 5000. gRPC uses port 50051.
Replace localhost with the server's internal IP for remote tests.
Replace 1 with the desired repetition count for timing.
Stop foreground servers with Ctrl+C.

Results are in SOLUTION.md. Original timing output is in measurements/.

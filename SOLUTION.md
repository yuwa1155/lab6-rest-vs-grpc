# Lab 6: REST vs gRPC

## Test setup

I used three GCP VMs with e2-standard-2 and Ubuntu 22.04:
- Client: us-west1-a
- Same-zone server: us-west1-a
- Different-region server: europe-west3-a

All remote tests used internal IP addresses. I ran each operation 1,000 times for localhost and same-zone tests, and 100 times for different-region tests. The numbers below are average milliseconds per operation.

Dot product used two vectors of 100 random values. Both image methods used the provided JPEG image, with dimensions 3004 x 1002.

## Results

| Operation | Localhost (ms) | Same zone (ms) | Different region (ms) |
|---|---:|---:|---:|
| REST add | 3.786 | 4.453 | 339.441 |
| gRPC add | 0.954 | 1.254 | 164.921 |
| REST rawimage | 6.609 | 9.976 | 1361.111 |
| gRPC rawimage | 10.180 | 15.958 | 223.710 |
| REST dotproduct | 4.273 | 5.699 | 345.837 |
| gRPC dotproduct | 1.043 | 1.503 | 185.095 |
| REST jsonimage | 42.323 | 47.478 | 1493.769 |
| gRPC jsonimage | 37.041 | 40.040 | 216.587 |
| PING average RTT | 0.041 | 0.671 | 160.970 |

## Observations

Localhost and same-zone results were fairly close. The different-region tests were much slower because the client and server were farther apart. For example, gRPC add took about 165 ms across regions, close to the 161 ms ping RTT.

My gRPC client reused one channel for all repetitions, while the REST client used requests.post separately for each request. Reusing the connection likely helped gRPC, especially across regions, where opening new connections costs more time.

The JSON image method uses base64, which makes the image payload larger and adds encoding and decoding work. It was much slower than raw images for REST. gRPC was faster for most tests, but raw images were faster with REST on localhost and within the same zone. These results show that gRPC is not always faster for every operation.

The timing also includes client-side work such as reading images, encoding data, and checking results, so these numbers measure the complete client operation rather than only network time.

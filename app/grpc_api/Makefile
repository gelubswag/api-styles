generate-grpc:
    python -m grpc_tools.protoc -I app/grpc_api/ \
        --python_out=app/grpc_api \
        --grpc_python_out=app/grpc_api \
        app/grpc_api/book.proto
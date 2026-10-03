FROM ubuntu:latest
LABEL authors="ce-pc"

ENTRYPOINT ["top", "-b"]
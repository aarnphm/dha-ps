# Build images
FROM golang:alpine AS builder

ENV GO111MODULE=on \
	CGO_ENABLED=0 \
	GOOS=linux \ 
	GOARCH=amd64

COPY . /app/src
WORKDIR /app/src

RUN apk add git ca-certificates

RUN go build -o /go/bin/app

# Run images
FROM alpine:latest

# copy from build images to container
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /go/bin/app /go/bin/app
COPY --from=builder /app/src/configs configs/
# expose PORT
EXPOSE 8080

CMD ["./go/bin/app"]

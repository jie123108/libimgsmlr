

export CGO_CFLAGS="-I$(brew --prefix gd)/include"
export CGO_LDFLAGS="-L$(brew --prefix gd)/lib"
GOOS=darwin CGO_ENABLED=1 go run test.go -filename $1
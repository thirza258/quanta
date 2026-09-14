CC ?= cc
CFLAGS ?= -O2 -g
WARN = -std=c17 -Wall -Wextra -Werror -pedantic
CORE = engine.c parallel.c
.PHONY: all test sanitize clean
all: quanta-bot
quanta-bot: main.c $(CORE) quanta.h
	$(CC) $(WARN) $(CFLAGS) -pthread main.c $(CORE) -o $@
quanta-test: test.c $(CORE) quanta.h
	$(CC) $(WARN) $(CFLAGS) -pthread test.c $(CORE) -o $@
test: quanta-test
	./quanta-test
sanitize: test.c $(CORE) quanta.h
	$(CC) $(WARN) -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize-recover=all -pthread test.c $(CORE) -o quanta-sanitize
	./quanta-sanitize
clean:
	rm -f quanta-bot quanta-test quanta-sanitize

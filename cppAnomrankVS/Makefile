CXX ?= g++
CXXFLAGS += -std=c++14 -Wall -Wextra -ggdb

# Enable optimizations
CXXFLAGS += -O3

HEADERS := $(wildcard *.hpp)
SOURCES := $(wildcard *.cpp)
OBJECTS := $(SOURCES:%.cpp=%.o)

TEST_PARAMS := "./darpa.txt"  " " 60 256 0 50 70

# Name/path of valgrind executable
VALGRIND ?= valgrind

.PHONY: all build run clean valgrind

all: build run

build: anomrank

run: anomrank
	./anomrank $(TEST_PARAMS)

clean:
	rm -f *.o

anomrank: $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $^ -o $@

valgrind: anomrank
	$(VALGRIND) --leak-check=full ./anomrank $(TEST_PARAMS)

%.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

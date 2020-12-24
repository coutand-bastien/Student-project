# options de compilation
CC = gcc
CCFLAGS = -Wall
LIBS = 		-lm -lstdc++		# par exemple, -lm rajoute le libm standard
LIBSDIR =

# fichiers du projet
SRC = src/main.cpp src/Source/Part1/Consign.cpp src/Source/Part1/Locker.cpp src/Source/Part1/Luggage.cpp src/Source/Ticket.cpp src/Source/Part2/VConsign.cpp src/Source/Part2/VLocker.cpp src/Source/Part2/VLuggage.cpp src/Test/Test.cpp src/Source/Part2/VLuggageRectangular.cpp src/Source/Part2/VLuggageCircle.cpp
OBJ = $(SRC:.c=.o)
EXEC = ./build/run.out

# règle initiale
all: $(EXEC)

# règles de compilation
%.o: %.c
	$(CC) $(CCFLAGS) -o $@ -c $<

# règles d'édition de liens
$(EXEC): $(OBJ)
	$(CC) -o $@ $^ $(LIBS) $(LIBSDIR)

# règles supplémentaires
.PHONY: clean mrproper

clean:
	rm -f *.o
mproper:
	rm -f $(EXEC) *.o
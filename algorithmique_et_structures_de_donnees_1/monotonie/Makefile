# options de compilation
CC = gcc
CCFLAGS = -Wall
LIBS = 		-lm -lstdc++		
LIBSDIR =

# fichiers du projet
SRC = ./src/monotonie.cpp
OBJ = $(SRC:.c=.o)
EXEC = ./build/run.out

.PHONY: all clean mrproper

# règle initiale
all: $(EXEC)

# règles de compilation
%.o: %.c
	$(CC) $(CCFLAGS) -o $@ -c $<

# règles d'édition de liens
$(EXEC): $(OBJ)
	$(CC) -o $@ $^ $(LIBS) $(LIBSDIR)

clean:
	rm -f *.o
	
mproper:
	rm -f $(EXEC) *.o
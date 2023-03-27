#include <stdio.h>

int main(int argc, char** argv){
  char c;

  // États internes des automates
  int L1=0;
  
  while((c = fgetc(stdin)) != EOF) {

    // Automate reconnaissant L1
    if (c == '\n' && L1!=0 && L1!=3)	printf("non ");
    if (c == '\n')		{printf("reconnu par L1\n"); L1 = 0;}
    else if(L1==0 && c=='a')	L1 = 1;
    else if(L1==1 && c=='a')	L1 = 0;
    else if(L1==2 && c=='a')	L1 = 3;
    else if(L1==3 && c=='a')	L1 = 2;
    else if(L1==0 && c=='b')	L1 = 2;
    else if(L1==1 && c=='b')	L1 = 3;
    else if(L1==2 && c=='b')	L1 = 0;
    else if(L1==3 && c=='b')	L1 = 1;
    else if(c!=' ' && c!='\t')	L1 = -1;

  }
  return 0;
}

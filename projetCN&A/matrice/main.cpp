/*
 * @nameProject :\n matrix library.
 *
 * @project :\n The aim of this project is to create a matrix library, in order to be able to reuse
 *            it in other projects later.
 *
 * @partOfTheProject :\n project as part of courses at the University of Nantes.
 *
 * @lastUpdate :\n 20 february by Bastien COUTAND and Cyprien GARNIER.
 *
 * @Creator :\n COUTAND Bastien (bastien.coutand@etu.univ-nantes.fr),
 *            GARNIER Cyprien (cyprien.garnier@etu.univ-nantes.fr).
 */
#include <iostream>
#include "matrix.h"

using namespace std;

int main(int argc, char** argv) {

    const uint64_t M1Size = 5, M2Size = 3, MatrixEx3SizeA = 4, MatrixEx3SizeB = 4, M4Size = 1, M5Size = 4, M6Size = 3,  M7Size = 3, matrixExercieTD4Size = 4, matrixTestProjetASize = 4, matrixTestProjetBSize = 4;

    double M1[] = {
        1,  2,  3,  4,  5,
        6,  7,  8,  9,  10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 24, 25
    };

    double M2[] = {
        1.66, 2,    3,
        4,    5.0,  6,
        7,    8,    9.45
    };

    double MatrixEx3A[] = {
        2,  1,  1, -3,
        6,  2,  5, -8,
        4,  3,  3, -9,
        -2, -2, -5,  10
    };


    double MatrixEx3B[] = {
        2, 3,  1,  5,
        6, 13, 5,  19,
        2, 19, 10, 23,
        4, 10, 11, 31
    };

    double M4[] = {3};

    double M5[] = {
        10, 3, 8, 7,
        0,  5, 3, 5,
        0,  0, 2, 3,
        0,  0, 0, 6
    };

    double M6[] = {
        1,  1,  2,
        0, -3, -2,
        0,  0, -2
    };

    double M7[] = {
        2, 4,  2, 
        6, 13, 5,  
        2, 10, 3, 
    };

    double matrixExercieTD4[] = {
        2, 3, 1, 5,
        6, 13, 5, 19,
        2, 19, 10, 23,
        4, 10, 11, 31
    };

    double matrixTestProjetA[] = {
        10, 7, 8, 7,
        7, 5, 6, 5,
        8, 6, 10, 9,
        7, 5, 9, 10
    };

    double matrixTestProjetB[] = {
        1, 7, 2, 1,
        7, 5, 1, 5,
        8, 6, 10, 9,
        7, 5, 9, 1
    };

    double b1[] = {
        3,
        2,
        3,
        3
    };

    double b2[] = {
        -1,
        -2,
        4
    };

    double b3[] = {
        -1,
        -4,
        -2
    };

    double bExercice3A[] = {
        7,
        29,
        17,
        -23
    };

    double bExercice3B[] = {
        1,
        3,
        3,
        4
    };

    double bProjetB1[] = {
            32,
            23,
            33,
            31
    };

    double bProjetB2[] = {
            32.1,
            22.9,
            33.1,
            30.9
    };

    double bProjetD1[] = {
            11,
            18,
            33,
            22
    };

    double bProjetD2[] = {
            11.1,
            17.9,
            33.1,
            21.9
    };


    double *S = allocateMatrix(0, 0);
    double *T = allocateMatrix(0, 0);
//--------------------- Test matrixMultiplyStrassen and NaiveMultiply-------------------//*/
    //--------------- Matrix of size 5 x 5 -------------//

    printf("\nStrassen multiplication gives for M1 (5 x 5) :\n");
    T = matrixMultiplyStrassen(S, M1, M1, M1Size);
    matrixAff(T,5, 5);

    printf("\nNaive multiplication gives for M1 (5 x 5) :\n");
    matrixMultiplyNaive(S, M1, M1, M1Size, M1Size, M1Size);
    matrixAff(S,5, 5);

    cout << "If the results are equals (1/0) : " << equals(S, T, 5, 5) << endl;


    //--------------- Matrix of size 4 x 4 MATRICE DE COURS -------------//

    printf("\nStrassen multiplication gives for MatrixEx3A (4 x 4) :\n");
    T = matrixMultiplyStrassen(S, MatrixEx3A, MatrixEx3A, MatrixEx3SizeA);
    matrixAff(T,4, 4);

    printf("\nNaive multiplication gives for MatrixEx3A (4 x 4) :\n");
    matrixMultiplyNaive(S, MatrixEx3A, MatrixEx3A, MatrixEx3SizeA, MatrixEx3SizeA, MatrixEx3SizeA);
    matrixAff(S,4, 4);

    cout << "If the results are equals (1/0) : " << equals(S, T, 4, 4) << endl;



    printf("\nStrassen multiplication gives for MatrixEx3B (4 x 4) :\n");
    T = matrixMultiplyStrassen(S, MatrixEx3B, MatrixEx3B, MatrixEx3SizeB);
    matrixAff(T,4, 4);

    printf("\nNaive multiplication gives for MatrixEx3B (4 x 4) :\n");
    matrixMultiplyNaive(S, MatrixEx3B, MatrixEx3B, MatrixEx3SizeB, MatrixEx3SizeB, MatrixEx3SizeB);
    matrixAff(S,4, 4);

    cout << "If the results are equals (1/0) : " << equals(S, T, 4, 4) << endl;


    //--------------- Matrix of size 3 x 3 -------------//

    printf("\nStrassen multiplication gives for M2 (3 x 3) :\n");
    T = matrixMultiplyStrassen(S, M2, M2, M2Size);
    matrixAff(T,3, 3);

    printf("\nNaive multiplication gives for M2 (3 x 3) :\n");
    matrixMultiplyNaive(S, M2, M2, M2Size, M2Size, M2Size);
    matrixAff(S,3, 3);

    cout << "If the results are equals (1/0) : " << equals(S, T, 3, 3) << endl;


    //--------------- Matrix of size 1 x 1 -------------//

    printf("\nStrassen multiplication gives for M4 (1 x 1) :\n");
    T = matrixMultiplyStrassen(S, M4, M4, M4Size);
    matrixAff(T,1, 1);


//--------------------- Test SolveTriangularSystemUP -------------------//
    //--------------- Matrix of size 4 x 4 -------------//

    printf("\nSolveTriangularSystemUP, for M5 * x = b1, give :\n");
    SolveTriangularSystemUP(S, M5, b1, M5Size);
    matrixAff(S, 4, 1); // result :-0.485 -0.55  0.75  0.5


    //--------------- Matrix of size 3 x 3 -------------//

    printf("\nSolveTriangularSystemUP, for M6 * x = b2, give :\n");
    SolveTriangularSystemUP(S, M6, b2, M6Size);
    matrixAff(S, 3, 1); // result : 1 2 -2

    
//--------------------- Test Triangularize -------------------//
    //--------------- Matrix of size 3 x 3 -------------//

    printf("\nTriangularize, for M7 * x = b3, give :\n");
    matrixAff(M7, M7Size, M7Size);
    Triangularize(M7, b3, M7Size);                    
    matrixAff(M7, M7Size, M7Size);


    //--------------- Matrix of size 4 x 4  and MATRICE DE COURS -------------//

    printf("\nTriangularize, for MatrixEx3A * x = bExercice3A, give :\n");
    matrixAff(MatrixEx3A, MatrixEx3SizeA, MatrixEx3SizeA);
    Triangularize(MatrixEx3A, bExercice3A, MatrixEx3SizeA);
    matrixAff(MatrixEx3A, MatrixEx3SizeA, MatrixEx3SizeA);
    

    printf("\nTriangularize, for MatrixEx3B * x = bExercice3B, give :\n");
    matrixAff(MatrixEx3B, MatrixEx3SizeB, MatrixEx3SizeB);
    Triangularize(MatrixEx3B, bExercice3B, MatrixEx3SizeB);
    matrixAff(MatrixEx3B, MatrixEx3SizeB, MatrixEx3SizeB);


//--------------------- Test SolveSystemGauss -------------------//

    printf("\nSolveSystemGauss, for MatrixEx3A, give :\n");
    SolveSystemGauss(S, MatrixEx3A, bExercice3A, MatrixEx3SizeA);
    matrixAff(S, 4, 1); // result : 2  -3  3  -1

    printf("\nSolveSystemGauss, for MatrixEx3B, give :\n");
    SolveSystemGauss(S, MatrixEx3B, bExercice3B, MatrixEx3SizeB);
    matrixAff(S, 4, 1); // result : 7  -1  10  -4

//--------------------- Test decompLU -------------------//
    //--------------------- matrixExercieTD4 -------------------//
    printf("\ndecompLU, for matrixExercieTD4, give :\n");
    matrixAff(matrixExercieTD4, matrixExercieTD4Size, matrixExercieTD4Size);
    
    decompLU(matrixExercieTD4, matrixExercieTD4Size);
    matrixAff(matrixExercieTD4, matrixExercieTD4Size, matrixExercieTD4Size);

//--------------------- Test det -------------------//
    printf("\ndeterminant of the matrixExercieTD4 :\n");
    printf("\n%f\n", det(matrixExercieTD4, matrixExercieTD4Size));


//--------------------- Test SolveSystemLU -------------------//
    double *x = allocateMatrix(0, 0);

    double *U = allocateMatrix(matrixTestProjetASize, matrixTestProjetASize);
    copyMatrix(matrixTestProjetA, U, matrixTestProjetASize, matrixTestProjetASize, matrixTestProjetASize, matrixTestProjetASize);

    double *V = allocateMatrix(matrixTestProjetBSize, matrixTestProjetBSize);
    copyMatrix(matrixTestProjetB, V, matrixTestProjetBSize, matrixTestProjetBSize, matrixTestProjetBSize, matrixTestProjetBSize);


    //--------------- matrix A -------------//
    printf("\nSolveSystemLU for the matrix A and the vector b1 :\n");
    SolveSystemLU(x, matrixTestProjetA, bProjetB1, matrixTestProjetASize);
    matrixAff(x,4,1);

    printf("\nSolveSystemLU for of the matrix A and the vector b2 :\n");
    SolveSystemLU(x, U, bProjetB2, matrixTestProjetASize);
    matrixAff(x,4,1);


    //--------------- matrix B -------------//
    printf("\nSolveSystemLU for the matrix B and the vector d1 :\n");
    SolveSystemLU(x, matrixTestProjetB, bProjetD1, matrixTestProjetBSize);
    matrixAff(x,4,1);

    printf("\nSolveSystemLU for the matrix B and the vector d2 :\n");
    SolveSystemLU(x, V, bProjetD2,matrixTestProjetBSize);
    matrixAff(x,4,1);

    return 0;
}
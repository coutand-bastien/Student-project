#include <cstdint>
#include <iostream>
#include <cstdlib>
#include "matrix.h"

using namespace std;

/**
 * @role memory allocation for a matrix of size n x m and initialization to 0.
 * @param n : the length of the matrix.
 * @param m : the width of the matrix.
 * @return matrix (n x m).
 */
double *allocateMatrix(uint64_t n,uint64_t m) {
    double *A;
    A = (double *) calloc (n * m, sizeof(double));
    return A;
}

/**
 * @role frees the memory allocated to matrix A.
 * @param A : the matrix.
 */
void freeMatrix(double *A) {
    free(A);
}

/**
 * @role allocates a n sized vector and initializes all entries to 0.
 * @param n : the length of the matrix.
 * @return vector of size n x n.
 */
double *allocateVector(uint64_t n) {
    double *v;
    v = (double *) calloc(n, sizeof(double));
    return v;
}

/**
 * @role : trees the memory allocated to a vector.
 * @param v : the vector.
 */
void freeVector(double *v) {
    free(v);
}

/**
 * @role sets a n * m matrix A to all zeros.
 * @param A : the matrix that we want to set to 0.
 * @param n : the length of the matrix.
 * @param m : the width of the matrix.
 */
void setMatrixZero(double *A, uint64_t n, uint64_t m) {
    uint64_t i, j;

    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) {
        /* Note that for a n x m matrix flattened to a 1D array, 
        element A_ij has index i * m + j
        */
        A[i * m + j] = 0.0;
        }
    }
}

/**
 * @role sets a n * n matrix A to identity.
 * @param A : the identity matrix.
 * @param n : the lenght of the matrix.
 */
void setMatrixIdentity (double *A, uint64_t n) {
    uint64_t i, j;

    for (i = 0; i < n; i++) {
        for (j = 0;j < n; j++) {
            A[i * n + j] = 0.0;
        }
        A[i * n + i] = 1.0;
    }
}

/**
 * @role copies a matrix.
 * @param A : the matrix copied of size n x m.
 * @param B : the matrix of size k x p.
 * @param n : the length of the matrix.
 * @param m : the width of the matrix.
 */
void copyMatrix(double *A, double *B, uint64_t n, uint64_t m, uint64_t k, uint64_t p) {
    // if the matrix A is the same or smaller than the matrix where it will be copied.
    if ((k * p) >= (n * m)) {
        for (uint64_t i = 0; i < n; i++) {
            for (uint64_t j = 0; j < m; j++) {
                B[i * p + j] = A[i * m + j];
            }
        }
    }
}

/**
 * @role Writes a matrix to a stream. For example, writing a matrix to standard output is
         writeMatrix(stdout, A, n, m);
         A sream can also be a file.
 * @param stream : the place where we want to write.
 * @param A : the matrix to write, of size n x m.
 * @param n : the length of the matrix.
 * @param m : the width of the matrix.
 */
void writeMatrix (FILE *stream, double *A, uint64_t n, uint64_t m) {
	fprintf(stream, "%d %d \n", (int)n, (int)m);
	int i, j;

	for (i = 0; i < n; ++i) {
	      for (j = 0; j < m; ++j) {
		      fprintf(stream, "%f \t", A[i * m + j]);
	      }
	      fprintf(stream, "\n");
	}
}

/**
 * @role the function computes the element-by-element abs of matrix A.
 * @param A : the matrix of size n x m.
 * @param n : the length of the matrix.
 * @param m : the width of the matrix.
 */
void absMatrix (double *A, uint64_t n, uint64_t m) {
	uint64_t i,j;

	for (i = 0; i < n; ++i) {
		for (j = 0; j < m; ++j) {
            A[i*m + j] = fabs(A[i*m + j]);
		}
	}
}

/**
 * @role Performs addition of two matrix A (size n x m) and B (size n x m).
         The result S = A + B is a n x m matrix.
         We consider that S is allocated outside the function.
 * @param S : the final matrix, S = A + B.
 * @param A : the matrix of size n x n.
 * @param B : the matrix of size m x m.
 * @param n : the length of the A matrix.
 * @param m : the length of the B matrix.
 */
void matrixAdd(double *S, const double *A, const double *B, uint64_t n, uint64_t m){
    uint64_t i,j;
	for(i = 0; i < n; ++i)
	{
		for(j = 0; j < m; ++j)
		{
            S[i*m + j] = A[i*m + j] + B[i*m + j];
		}
	}
}

/**
 * @role Performs subtraction of two matrix A (size n x m) and B (size n x m).
         The result S = A - B is a n x m matrix.
         We consider that S is allocated outside the function.
 * @param S : the final matrix, S = A - B.
 * @param A : the matrix of size n x n.
 * @param B : the matrix of size m x m.
 * @param n : the length of the A matrix.
 * @param m : the length of the B matrix.
 */
void matrixSub(double *S, double *A, double *B, uint64_t n, uint64_t m){
    uint64_t i,j;
	for (i = 0; i < n; ++i) {
		for (j = 0; j < m; ++j) {
            S[i*m + j] = A[i*m + j] - B[i*m + j];
		}
	}
}

/**
 * @role For a double m x n matrix A the function returns its maximum in absolute value
         element.
 * @param max : the maximum values in the matrix.
 * @param A : the matrix of size n x m.
 * @param n : the length of the matrix.
 * @param m : the width of the matrix.
 * @return the maximum values in the A matrix.
 */
double getMaxInMatrix(double max, double *A, uint64_t n, uint64_t m) {
	double maxA = fabs(A[0]);
	double current = fabs(A[0]);
	int i,j;

	for(i = 0; i < n; ++i) {
		for(j = 0; j < m; ++j) {
			current = fabs(A[i * m + j]);
			if(current > maxA) maxA = current;
		}
	}
    return maxA;
}

/**
 * @role : displays a matrix in the form of an array n x n.
 * @param M : the matrix (table).
 * @param n : the length of the matrix (n x n).
 * @param name : the name of the matrix.
 */
void matrixAff(double *M, uint64_t n, uint64_t m) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cout << M[i * m + j] << "\t";
        }
        printf("\n");
    }
    printf("\n");
}

/**
 * @role create a matrix with random values ranging from -127 to +127, of size size x size.
 * @param size : the lenght of the matrix.
 * @return matrix (size x size).
 */
double * matrixGenerate(uint64_t size) {
    double *A = allocateMatrix(size, size);

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            A[i * size + j] = rand() % (127 - (-127) + 1) - 127;
        }
    }
    return A;
}

bool equals(double *A, double *B, int n, int m) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < m-1; j++) {
            if (A[i * n + j] != B[i * n + j]) return false;
        }
    }

    return true;
}

/**
 * @role : create a matrix which will be size will be a square of 2. It consists of the
 *         initial matrix A and it is composed of as many rows and columns of 0 as possible
 *         to access the nearest square of 2.
 *         Example: A of size 5 will at the output of size 8 and the added columns and rows (6, 7, 8) will be 0.
 * @param A : the matrix initial, of size (size x size).
 * @param size : the size of the matrix.
 * @return a matrix which will be size will be the nearest square of 2.
 */
double * preTreatment(double *A, uint64_t size) {
    double *S; // the new matrix with zero if the length it's not a square of 2.
    uint64_t newSize = size;

    while (log2(newSize) != floor(log2(newSize))) { newSize++; }

    // creation of the matrix matrix with only zero.
    S = allocateMatrix(newSize, newSize);
    setMatrixZero(S, newSize, newSize);
    // we copy the matrix A in S;
    copyMatrix(A, S, size, size, newSize, newSize);

    return S;
}

/**
 * @role : remove the lines of 0 added during Strassen.
 * @param A : the matrix initial, of size (sizeUp x sizeUp).
 * @param S : the final matrix, of size (size x size).
 * @param size : the length of the S matrix.
 * @param sizeUp :  the length of the A matrix.
 */
double * postTreatment(const double *A, uint64_t size, uint64_t sizeUp) {
    double *S = allocateMatrix(size, size);

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            S[i * size + j] = A[i * sizeUp + j];
        }
    }

    return S;
}

/**
 * @role Performs naive multiplication of matrix A (size p x k) by a matrix B (size k x r).
         The result matrix S = A*B  is of size (k x r).
         We assume that S has already been allocated outside the function.
 * @param S : the final matrix, S = A * B.
 * @param A : the matrix of size p x k.
 * @param B : the matrix of size k x r.
 * @param p : the length of the A matrix.
 * @param k : the width of the A matrix and the length of the B matrix.
 * @param r : the width of the B matrix.
 */
void matrixMultiplyNaive (double *S, double *A, double *B, uint64_t p, uint64_t k, uint64_t r){
    if (p == k == r == 1) { S[0] = A[0] * B[0]; return; }

    for(int i=0; i<k;i++){
        for(int j=0; j<r; j++){
            S[i*p+j]=0;
            for(int m=0; m<k; m++){
                S[i*p+j] += A[i*k+m] * B[m*r+j];
            }
        }
    }
}

/**
 * @role multiply Strassen and remove the 0 if there are rows / columns added.
 * @param S : the final matrix, S = A * B.
 * @param A : the matrix of size n x n.
 * @param B : the matrix of size n x n.
 * @param size : the length of the matrix.
 */
double * matrixMultiplyStrassen (double *S, double *A, double *B, uint64_t size) {
    uint64_t sizeUp = size;

    matrixMultiplyStrassen_rec(S, A, B, size, sizeUp);
    return postTreatment(S, size, sizeUp);
}

/**
 * @role Performs a multiplication of two square matrices A and B (size n x n) by Strassen algorithm.
         We assume that S has already been allocated outside the function.
 * @param S : the final matrix, S = A * B.
 * @param A : the matrix of size n x n.
 * @param B : the matrix of size n x n.
 * @param size : the length of the matrix.
 * @param sizeUp : the newSze of the matrix after preTreatment.
 */
void matrixMultiplyStrassen_rec (double *S, double *A, double *B, uint64_t size, uint64_t &sizeUp) {

    if (size == 1) { matrixMultiplyNaive(S, A, B, size, size, size); return; }

    //addition of row(s) and column(s) of 0 and change the size, to access the nearest square of 2.
    if (log2(size) != floor(log2(size))) {
        A = preTreatment(A, size);
        B = preTreatment(B, size);

        while (log2(sizeUp) != floor(log2(sizeUp))) { sizeUp++; }
    }

    // if the initial matrix are of size 2, or when the sub-matrix (block) are of size 2.
    if (size == 2) {
        double M1, M2, M3, M4, M5, M6, M7;

        M1 = (A[0] + A[3]) * (B[0] + B[3]);
        M2 = (A[2] + A[3]) * B[0];
        M3 = A[0] * (B[1] - B[3]);
        M4 = A[3] * (B[2] - B[0]);
        M5 = (A[0] + A[1]) * B[3];
        M6 = (A[2] - A[0]) * (B[0] + B[1]);
        M7 = (A[1] - A[3]) * (B[2] + B[3]);

        S[0] = M1 + M4 - M5 + M7;
        S[1] = M3 + M5;
        S[2] = M2 + M4;
        S[3] = M1 - M2 + M3 + M6;

        return;
    }
    else {
        uint64_t newSize = sizeUp / 2;

        double *A11     = allocateMatrix(newSize, newSize), *A12 = allocateMatrix(newSize, newSize), *A21 = allocateMatrix(newSize, newSize), *A22     = allocateMatrix(newSize, newSize),
               *B11     = allocateMatrix(newSize, newSize), *B12 = allocateMatrix(newSize, newSize), *B21 = allocateMatrix(newSize, newSize), *B22     = allocateMatrix(newSize, newSize),
               *M1      = allocateMatrix(newSize, newSize),  *M2 = allocateMatrix(newSize, newSize),  *M3 = allocateMatrix(newSize, newSize),  *M4     = allocateMatrix(newSize, newSize),
               *M5      = allocateMatrix(newSize, newSize),  *M6 = allocateMatrix(newSize, newSize),  *M7 = allocateMatrix(newSize, newSize),  *C11    = allocateMatrix(newSize, newSize),
               *C12     = allocateMatrix(newSize, newSize), *C21 = allocateMatrix(newSize, newSize), *C22 = allocateMatrix(newSize, newSize), *result1 = allocateMatrix(newSize, newSize),
               *result2 = allocateMatrix(newSize, newSize);

        //---------------------- Partition into 4 sub-matrix ------------------------//

        for (int i = 0; i < newSize ; i++) {
            for (int j = 0; j < newSize; j++) {
                A11[i * newSize + j] = A[i * sizeUp + j];
                A12[i * newSize + j] = A[i * sizeUp + newSize + j];
                A21[i * newSize + j] = A[i * sizeUp + newSize * sizeUp + j];
                A22[i * newSize + j] = A[i * sizeUp + newSize * sizeUp + newSize + j];

                B11[i * newSize + j] = B[i * sizeUp + j];
                B12[i * newSize + j] = B[i * sizeUp + newSize + j];
                B21[i * newSize + j] = B[i * sizeUp + newSize * sizeUp + j];
                B22[i * newSize + j] = B[i * sizeUp + newSize * sizeUp + newSize + j];
            }
        }

        //---------------------- Creation of the sub-matrix of A and B with Strassen operation ------------------------//

        // M1 = (A[0] + A[3]) * (B[0] + B[3]);
        matrixAdd(result1, A11, A22, newSize, newSize);
        matrixAdd(result2, B11, B22, newSize, newSize);
        matrixMultiplyStrassen(M1, result1, result2, newSize);

        // M2 = (A[2] + A[3]) * B[0];
        matrixAdd(result1, A21, A22, newSize, newSize);
        matrixMultiplyStrassen(M2, result1, B11, newSize);

        // M3 = A[0] * (B[1] - B[3]);
        matrixSub(result1, B12, B22, newSize, newSize);
        matrixMultiplyStrassen(M3, A11, result1, newSize);

        // M4 = A[3] * (B[2] - B[0]);
        matrixSub(result1, B21, B11, newSize, newSize);
        matrixMultiplyStrassen(M4, A22, result1, newSize);

        // M5 = (A[0] + A[1]) * B[3];
        matrixAdd(result1, A11, A12, newSize, newSize);
        matrixMultiplyStrassen(M5, result1, B22, newSize);

        // M6 = (A[2] - A[0]) * (B[0] + B[1]);
        matrixSub(result1, A21, A11, newSize, newSize);
        matrixAdd(result2, B11, B12, newSize, newSize);
        matrixMultiplyStrassen(M6, result1, result2, newSize);

        // M7 = (A[1] - A[3]) * (B[2] + B[3]);
        matrixSub(result1, A12, A22, newSize, newSize);
        matrixAdd(result2, B21, B22, newSize, newSize);
        matrixMultiplyStrassen(M7, result1, result2, newSize);


        //---------------------- Addition of its operations in a matrix C ------------------------//

        // C11 = M1 + M4 - M5 + M7
        matrixAdd(result1, M1, M4, newSize, newSize);
        matrixAdd(result2, result1, M7, newSize, newSize);
        matrixSub(C11, result2, M5, newSize, newSize);

        // C12 = M3 + M5;
        matrixAdd(C12, M3, M5, newSize, newSize);

        // C21 = M2 + M4;
        matrixAdd(C21, M2, M4, newSize, newSize);

        // C22 = M1 - M2 + M3 + M6;
        matrixAdd(result1, M1, M3, newSize, newSize);
        matrixAdd(result2, result1, M6, newSize, newSize);
        matrixSub(C22, result2, M2, newSize, newSize);

        //---------------------- Addition of the result in the final matrix ------------------------//

        for (int i = 0; i < newSize; i++) {
            for (int j = 0; j < newSize; j++) {
                S[i * sizeUp + j]                               = C11[i * newSize + j]; // S11
                S[i * sizeUp + newSize + j]                     = C12[i * newSize + j]; // S12
                S[i * sizeUp + newSize * sizeUp + j]            = C21[i * newSize + j]; // S21
                S[i * sizeUp + newSize * sizeUp + newSize + j]  = C22[i * newSize + j]; // S22
            }
        }
    }
}

/**
 * @role Solves a system of linear equations Ax=b for a double-precision matrix A (size n x n) calculating
         the bj terms as a function of the values above (A [j * n + i]) of the pivots (A [i * n + i]).
         **Warning**, in this method the terms of the matrix A, are not modified, because useless for the function.
 * @param x : the solution Ax=b.
 * @param A : the matrix of size n x n.
 * @param b : the double value.
 * @param n : the length of the matrix.
**/
void SolveTriangularSystemUP (double *x, double *A, double *b, uint64_t n) {
    double value;
    // we start with the last pivot (A[(n-1) * n + (n-1)]) and go up...
    for(int i = n - 1 ; i >= 0 ; i--) {
        x[i] = b[i] / A[i * n + i]; // Look for the result of the only variable in the last row of A, such that t = ...

        for (int j = i - 1; j >= 0; j--) {
            value = x[i] * A[j * n + i]; // ... then we replace (here t) by its value found previously, on the column ...
            b[j] -= value; // ... and we move this value on the side of b to leave only the variables in the A matrix.
        }
    }
}

/**
 * @role: Solves a system of linear equations Ay=b for a double-precision matrix A (size n x n).
        Uses iterative ascension algorithm.
        After the procedure, y contains the solution of Ay=b.
        We assume that y has been allocated outside the function.
 * @param y : the solution Axy=b.
 * @param A : the matrix of size n x n.
 * @param b : the double value.
 * @param n : the length of the matrix.
 */
void SolveTriangularSystemDown (double *y, double *A, double *b, uint64_t n) {
    double value;
    y[0] = b[0];

    for(int i = 1 ; i <= n ; i++) {
        value = b[i];
        for (int j = 0; j <= i; j++) {
            value -= A[i*n+j]*y[j];
        }
        y[i] = value;
   }
}

/**
 *   Performs Gauss elimination for given a matrix A (size n x n) and a vector b (size n).
    Modifies directly matrix A and vector b.
    In the end of the procedure, A is upper triangular and b is modified accordingly.
    Returns a boolean variable:
        *  true in case of success and
        *  false in case of failure, for example matrix is impossible to triangularize.
 * @param A : the matrix A.
 * @param b : the vector b.
 * @param n : the length of the matrix A.
**/
bool Triangularize (double *A, double *b, uint64_t n) {
    diagZero(A,n);

    for (int cl = 0; cl < n - 1; cl++) {
        for (int lgn = cl + 1; lgn < n; lgn++) {
            // if the coef is not null
            if (A[cl * n + cl] != 0) {
                // determine the coef x (exp L2 = L2 - xL1)
                int x = A[lgn * n + cl] / A[cl * n + cl];
                // performs the calculation (L2 = L2-xL1) by applying x to each cell of the line
                for (int w = cl; w < n; w++) {

                    A[lgn * n + w] = A[lgn * n + w] - x * A[cl * n + w];
                }
                b[lgn] -= x * b[cl];
            }
        }
    }

    return diagZero(A,n);
}

/**
 * @role : Allows the decomposition of LU inside the starting matrix A. L and U are stored in it.
 * @param A : the started matrix of size (n x n).
 * @param n : the length of the A matrix.
 * @return true if the decomposition of LU is good, and false if not.
 */
bool decompLU (double *A, uint64_t n) {
    diagZero(A, n);
    double x;

    for (int cl = 0; cl < n - 1; cl++) {
        for (int lgn = cl + 1; lgn < n; lgn++) {
            // if the coef is not null
            if (A[cl * n + cl] != 0) {
                // determine the coef x (exp L2 = L2 - xL1)
                 x = A[lgn * n + cl] / A[cl * n + cl];
                // performs the calculation (L2 = L2-xL1) by applying x to each cell of the line

                for (int w = cl; w < n; w++) {
                    A[lgn * n + w ] = A[lgn * n + w] - x * A[cl * n + w];
                }

                A[lgn * n + cl] = x;
            }
        }
    }

    return diagZero(A, n);
}

/**
 * Look that there is no 0 on the diagonal.
 * @param A : the matrix A.
 * @param n : the length of matrix A.
**/
bool diagZero(double *A, uint64_t n){
    
    for (int i = 0; i < n; ++i) {
        if (A[i*n + i] == 0) {
            return false;
        }
	}
    return true;
}

/**
 * @role : compute the determinant of a matrix in LU form. Calculation of diagonal coefficients.
 * @param A : the started matrix of size (n x n).
 * @param n : the length of the A matrix.
 * @return the value of the determinant.
 */
double det(double *A, uint64_t n) {
    double resultat = 1;

    for (int i = 0; i < n; i++) {
        resultat = resultat * A[i*n + i];
    }

    return resultat;
}
/*
    Solves a system of linear equations Ax=b, given a matrix A (size n x n) and vector b(size n).
    Uses Gauss elimination algorithm based on triangularization and the ascension solving.
    After the procedure, vector x contains the solution to Ax=b.
    We assume that x has been allocated outside the function.
        Returns a boolean variable:
        *  true in case of success and
        *  false in case of failure, for example matrix is of rank <n .
*/

bool SolveSystemGauss (double *x, double *A, double *b, uint64_t n) {

   if (Triangularize(A, b, n)) {
       SolveTriangularSystemUP(x, A, b, n); 
       return true;
   }

   return false;
}

/*
    Solves a system of linear equations Ax=b, given a matrix A (size n x n) = L*U and vector b(size n).
    Uses descent algorithm.
    After the procedure, vector x contains the solution to Ax=b.
    We assume that x has been allocated outside the function.
*/
bool SolveSystemLU (double *x, double *A, double *b, uint64_t n){
    double *y = allocateMatrix(4, 1);

    decompLU(A, n);
    SolveTriangularSystemDown(y, A, b, n);
    SolveTriangularSystemUP(x, A, y, n);

    return true;
}

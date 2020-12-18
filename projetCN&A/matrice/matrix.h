#ifndef TP3_MATRIX_H
#define TP3_MATRIX_H

#include <cmath>
#include <climits>
#include <cstdlib>
#include <cstdio>
#include <cstdint>

double*     allocateMatrix      (uint64_t n,uint64_t m) ;
double*     allocateVector      (uint64_t n) ;
void        freeMatrix          (double *A);
void        freeVector          (double *v);
void        setMatrixZero       (double *A, uint64_t n, uint64_t m);
void        setMatrixIdentity   (double *A, uint64_t n);
void        copyMatrix          (double *B, double *A, uint64_t n, uint64_t m, uint64_t k, uint64_t p);
void        writeMatrix         (FILE *stream, double *A, uint64_t n, uint64_t m);
void        absMatrix           (double *Aabs,double *A, uint64_t n, uint64_t m);
double      getMaxInMatrix      (double max, double *A, uint64_t n, uint64_t m);
void        matrixSub           (double *S, const double *A, const double *B, uint64_t n, uint64_t m);
void        matrixAdd           (double *S, const double *A, const double *B, uint64_t n, uint64_t m);
bool        diagZero            (double *A, uint64_t n);

/**
 * @role: displays a matrix in the form of an array n x n.
 * @param M : the matrix (table).
 * @param n : the length of the matrix (n x n).
 */
void matrixAff(double *M, uint64_t n, uint64_t m);

/**
 * @role: create a matrix with random values ranging from -127 to +127, of size size x size.
 * @param size : the lenght of the matrix.
 * @return matrix (size x size).
 */
double * matrixGenerate(uint64_t size);

/**
 * @role: look if the two matrix are equals or not.
 * @param A : the 1st matrix, of size (n x m).
 * @param B : the 2st matrix, of size (n x m).
 * @param n : the length of the matrix.
 * @param m : the width of the matrix.
 * @return
 */
bool equals(double *A, double *B, int n, int m);

/**
 * @role: create a matrix which will be size will be a square of 2. It consists of the
 *         initial matrix A and it is composed of as many rows and columns of 0 as possible
 *         to access the nearest square of 2.
 *         Example: A of size 5 will at the output of size 8 and the added columns and rows (6, 7, 8) will be 0.
 * @param A : the matrix initial, of size (size x size).
 * @param size : the size of the matrix.
 * @return a matrix which will be size will be the nearest square of 2.
 */
double * preTreatment(double *A, uint64_t size);

/**
 * @role: remove the lines of 0 added during Strassen.
 * @param A : the matrix initial, of size (sizeUp x sizeUp).
 * @param S : the final matrix, of size (size x size).
 * @param size : the length of the S matrix.
 * @param sizeUp :  the length of the A matrix.
 */
double * postTreatment(double *S, const double *A, uint64_t size, uint64_t sizeUp);

/**
 * @role: Performs naive multiplication of matrix A (size p x k) by a matrix B (size k x r).
         The result matrix S = A*B  is of size (k x r).
         We assume that S has already been allocated outside the function.
 * @param S : the final matrix, S = A * B.
 * @param A : the matrix of size p x k.
 * @param B : the matrix of size k x r.
 * @param p : the length of the A matrix.
 * @param k : the width of the A matrix and the length of the B matrix.
 * @param r : the width of the B matrix.
 */
void matrixMultiplyNaive (double *S, double *A, double *B, uint64_t p, uint64_t k, uint64_t r);


/**
 * @role: multiply Strassen and remove the 0 if there are rows / columns added.
 * @param S : the final matrix, S = A * B.
 * @param A : the matrix of size n x n.
 * @param B : the matrix of size n x n.
 * @param size : the length of the matrix.
 */
double * matrixMultiplyStrassen (double *S, double *A, double *B, uint64_t size);

/**
 * @role: Performs a multiplication of two square matrices A and B (size n x n) by Strassen algorithm.
        We assume that S has already been allocated outside the function.
 * @param S : the final matrix, S = A * B.
 * @param A : the matrix of size n x n.
 * @param B : the matrix of size n x n.
 * @param size : the length of the matrix.
 * @param sizeUp : the newSze of the matrix after preTreatment.
 */
void matrixMultiplyStrassen_rec (double *S, double *A, double *B, uint64_t size, uint64_t &sizeUp);

/**
 * @role: Solves a system of linear equations Ax=b for a double-precision matrix A (size n x n).
        Uses iterative ascension algorithm.
        After the procedure, x contains the solution of Ax=b.
        We assume that x has been allocated outside the function.
 * @param x : the solution Ax=b.
 * @param A : the matrix of size n x n.
 * @param b : the double value.
 * @param n : the length of the matrix.
 */
void SolveTriangularSystemUP (double *x, double *A, double *b, uint64_t n);

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
void SolveTriangularSystemDown (double *y, double *A, double *b, uint64_t n);

/*
    Performs Gauss elimination for given a matrix A (size n x n) and a vector b (size n).
    Modifies directly matrix A and vector b.
    In the end of the procedure, A is upper truangular and b is modified accordingly.
    Returns a boolean variable:
        *  true in case of success and
        *  false in case of failure, for example matrix is impossible to triangularize.
*/
bool Triangularize (double *A,  double *b,  uint64_t n);

/**
 * @role : Allows the decomposition of LU inside the starting matrix A. L and U are stored in it.
 * @param A : the started matrix of size (n x n).
 * @param n : the length of the A matrix.
 * @return true if the decomposition of LU is good, and false if not.
 */
bool decompLU(double *A, uint64_t n);

/**
 * @role : compute the determinant of a matrix in LU form. Calculation of diagonal coefficients.
 * @param A : the started matrix of size (n x n).
 * @param n : the length of the A matrix.
 * @return the value of the determinant.
 */
double det(double *A, uint64_t n);

/*
    Solves a system of linear equations Ax=b, given a matrix A (size n x n) and vector b(size n).
    Uses Gauss elimination algorithm based on truangularization and the ascension solving.
    After the procedure, vector x contains the solution to Ax=b.
    We assume that x has been allocated outside the function.
        Returns a boolean variable:
        *  true in case of success and
        *  false in case of failure, for example matrix is of rank <n .
*/
bool SolveSystemGauss (double *x, double *A, double *b, uint64_t n);

/*
    Solves a system of linear equations Ax=b, given a matrix A (size n x n) = L*U and vector b(size n).
    Uses descent algorithm.
    After the procedure, vector x contains the solution to Ax=b.
    We assume that x has been allocated outside the function.
*/
bool SolveSystemLU (double *x, double *A, double *b, uint64_t n);

#endif //TP3_MATRIX_H

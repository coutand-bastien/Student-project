import * as isPossible from '../src/move-validation';
import * as pieces from '../src/piece';
import { Chessboard, createEmptyChessboard, putPiece, historique } from '../src/chessboard';
import { Position, position } from '../src/position';
import { Move, move } from '../src/movements';

let chessboard : Chessboard;

const positionA1 : Position = position(0, 0); // A1
const positionA4 : Position = position(0, 3); // A4
const positionA5 : Position = position(0, 4); // A5
const positionA6 : Position = position(0, 5); // A6
const positionA7 : Position = position(0, 6); // A7
const positionA8 : Position = position(0, 7); // A8

const positionB1 : Position = position(1, 0); // B1
const positionB2 : Position = position(1, 1); // B2
const positionB3 : Position = position(1, 2);// B3
const positionB4 : Position = position(1, 3); // B4
const positionB5 : Position = position(1, 4); // B5
const positionB6 : Position = position(1, 5); // B6
const positionB7 : Position = position(1, 6); // B7

const positionC1 : Position = position(2, 0); // C1
const positionC3 : Position = position(2, 2); // C3
const positionC4 : Position = position(2, 3); // C4
const positionC5 : Position = position(2, 4); // C5
const positionC6 : Position = position(2, 5); // C6
const positionC7 : Position = position(2, 6); // C7
const positionC8 : Position = position(2, 7); // C8

const positionD2 : Position = position(3, 1); // D2
const positionD3 : Position = position(3, 2); // D3
const positionD4 : Position = position(3, 3); // D4
const positionD5 : Position = position(3, 4); // D5
const positionD6 : Position = position(3, 5); // D6

const positionE1 : Position = position(4, 0); // E1
const positionE2 : Position = position(4, 1); // E2
const positionE3 : Position = position(4, 2); // E3
const positionE4 : Position = position(4, 3); // E4
const positionE5 : Position = position(4, 4); // E5
const positionE7 : Position = position(4, 6); // E7
const positionE8 : Position = position(4, 7); // E8

const positionF2 : Position = position(5, 1); // F2
const positionF3 : Position = position(5, 2); // F3
const positionF4 : Position = position(5, 3); // F4
const positionF5 : Position = position(5, 4); // F5
const positionF6 : Position = position(5, 5); // F6

const positionG1 : Position = position(6, 0); // G1
const positionG3 : Position = position(6, 2); // G3
const positionG5 : Position = position(6, 4); // G5
const positionG8 : Position = position(6, 7); // G8

const positionH1 : Position = position(7, 0); // H1
const positionH4 : Position = position(7, 3); // H4
const positionH7 : Position = position(7, 6); // H7
const positionH8 : Position = position(7, 7); // H8

// Horizontal moves
const moveE4_H4 : Move = move(positionE4, positionH4);
const moveE4_A4 : Move = move(positionE4, positionA4);
const moveE1_C1 : Move = move(positionE1, positionC1);
const moveE1_G1 : Move = move(positionE1, positionG1);
const moveE8_C8 : Move = move(positionE8, positionC8);
const moveE8_G8 : Move = move(positionE8, positionG8);

// Vertical moves
const moveE4_E1 : Move = move(positionE4, positionE1);
const moveE4_E8 : Move = move(positionE4, positionE8);
const moveB4_B5 : Move = move(positionB4, positionB5);
const moveB7_B5 : Move = move(positionB7, positionB5); 
const moveB5_B4 : Move = move(positionB5, positionB4);
const moveB2_B4 : Move = move(positionB2, positionB4);
const moveE8_E7 : Move = move(positionE8, positionE7);
const moveE1_E2 : Move = move(positionE1, positionE2);

// Diagonal moves
const moveE4_A8 : Move = move(positionE4, positionA8);

// Knight moves
const moveE4_F6 : Move = move(positionE4, positionF6);
const moveE4_G5 : Move = move(positionE4, positionG5);
const moveE4_F2 : Move = move(positionE4, positionF2);
const moveE4_G3 : Move = move(positionE4, positionG3);
const moveE4_D2 : Move = move(positionE4, positionD2);
const moveE4_C3 : Move = move(positionE4, positionC3);
const moveE4_C5 : Move = move(positionE4, positionC5);
const moveE4_D6 : Move = move(positionE4, positionD6);

// Impossible moves
const moveE4_C7 : Move = move(positionE4, positionC7);
const moveE4_B2 : Move = move(positionE4, positionB2);

describe("Test blackPawnMove()", () => {
    beforeEach( () => {
        chessboard = createEmptyChessboard();
    });

    it("Pawns can move forward", () => {
        putPiece(chessboard, positionA7, pieces.blackPawn);
        
        let singleForward: Move = {from: positionA7, to: positionA6, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, singleForward)).toBeTruthy();
    });

    it("Pawns cannot move backward", () => {
        putPiece(chessboard, positionA7, pieces.blackPawn);

        let singleForward: Move = {from: positionA7, to: positionA8, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, singleForward)).toBeFalsy();
    });

    it("When in the initial position, paws can move 2 squares forward", () => {
        putPiece(chessboard, positionA7, pieces.blackPawn);

        let doubleForward: Move = {from: positionA7, to: positionA5, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, doubleForward)).toBeTruthy();
    });

    it("When a paws has already moved, it cannot move 2 squares forward", () => {
        putPiece(chessboard, positionC6, pieces.blackPawn);

        let doubleForward: Move = {from: positionC6, to: positionC4, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, doubleForward)).toBeFalsy();
    });

    it("When in the initial position, pawns cannot move 3 squares forward", () => {
        putPiece(chessboard, positionC6, pieces.blackPawn);

        let tripleForward: Move = {from: positionA7, to: positionA4, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, tripleForward)).toBeFalsy();
    });

    it("When in face of another piece, pawns cannot move forward", () => {
        putPiece(chessboard, positionA6, pieces.whitePawn);
        putPiece(chessboard, positionA7, pieces.blackPawn);

        let singleForward: Move = {from: positionA7, to: positionA6, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, singleForward)).toBeFalsy();
    });

    it("Pawns cannot capture an empty square ", () => {
        putPiece(chessboard, positionA7, pieces.blackPawn);

        let diagonalCapture: Move = {from: positionA7, to: positionB6, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, diagonalCapture)).toBeFalsy();
    });

    it("Pawns cannot capture pieces of the same color", () => {
        putPiece(chessboard, positionA7, pieces.blackPawn);
        putPiece(chessboard, positionB6, pieces.blackKing);

        let diagonalCapture: Move = {from: positionA7, to: positionB6, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, diagonalCapture)).toBeFalsy();
    });

    it("Pawns can capture pieces of a different color", () => {
        putPiece(chessboard, positionA7, pieces.blackPawn);
        putPiece(chessboard, positionB6, pieces.whiteQueen);

        let diagonalCapture: Move = {from: positionA7, to: positionB6, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, diagonalCapture)).toBeTruthy();
    });

    it("Pawns can use the movement 'en passant' ", () => {
        putPiece(chessboard, positionA4, pieces.blackPawn);
        putPiece(chessboard, positionB2, pieces.whitePawn);

        isPossible.whitePawnMove(chessboard, moveB2_B4);
        historique(chessboard, moveB2_B4);
        chessboard.nbCoup++;

        let diagonalCapture: Move = {from: positionA4, to: positionB3, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, diagonalCapture)).toBeTruthy();
    });

    it("Pawns cannot use the movement 'en passant'", () => {
        putPiece(chessboard, positionA5, pieces.blackPawn);
        putPiece(chessboard, positionB2, pieces.whitePawn);

        isPossible.whitePawnMove(chessboard, moveB2_B4);
        historique(chessboard, moveB2_B4);
        chessboard.nbCoup++;

        isPossible.whitePawnMove(chessboard, moveB4_B5);
        historique(chessboard, moveB4_B5);
        chessboard.nbCoup++;

        let diagonalCapture: Move = {from: positionA5, to: positionB4, isValid: true};
        expect(isPossible.blackPawnMove(chessboard, diagonalCapture)).toBeFalsy();
    });
});

describe("Test whitePawnMove()", () => {
    beforeEach( () => {
        chessboard = createEmptyChessboard();
    });

    it("When there is a piece in front it, pawns cannot move forward", () => {
        putPiece(chessboard, positionD4, pieces.whitePawn); // White Pawn at D4
        putPiece(chessboard, positionD5, pieces.blackPawn); // Black Pawn at D5

        let simpleFowardMove: Move = {from: positionD4, to: positionD5, isValid: true};
        expect(isPossible.whitePawnMove(chessboard, simpleFowardMove)).toBeFalsy();
    });

    it("Pawns can move forward", () => {
        putPiece(chessboard, positionD4, pieces.whitePawn); // White Pawn at D4

        let simpleFowardMove: Move = {from: positionD4, to: positionD5, isValid: true};
        expect(isPossible.whitePawnMove(chessboard, simpleFowardMove)).toBeTruthy();
    });

    it("When in the initial position, pawns can move two squares forward", () => {
        putPiece(chessboard, positionD2, pieces.whitePawn); // White Pawn at D2

        let doubleFowardMove: Move = {from: positionD2, to: positionD4, isValid: true};
        expect(isPossible.whitePawnMove(chessboard, doubleFowardMove)).toBeTruthy();
    });

    it("When they have already moved, pawns cannot move two squares forward", () => {
        putPiece(chessboard, positionD3, pieces.whitePawn); // White Pawn at D3

        let doubleFowardMove: Move = {from: positionD3, to: positionD5, isValid: true};
        expect(isPossible.whitePawnMove(chessboard, doubleFowardMove)).toBeFalsy();
    });

    it("Pawns cannot capture an empty square", () => {
        putPiece(chessboard, positionD3, pieces.whitePawn); // White Pawn at D3

        let diagonalCapture: Move = {from: positionD3, to: positionC4, isValid: true};
        expect(isPossible.whitePawnMove(chessboard, diagonalCapture)).toBeFalsy();
    });

    it("Pawns cannot capture a piece of the same color", () => {
        putPiece(chessboard, positionD3, pieces.whitePawn); // White Pawn at D3
        putPiece(chessboard, positionC4, pieces.whitePawn); // White Pawn at C4

        let diagonalCapture: Move = {from: positionD3, to: positionC4, isValid: true};
        expect(isPossible.whitePawnMove(chessboard, diagonalCapture)).toBeFalsy();
    });

    it("Pawns can capture pieces of a different color", () => {
        putPiece(chessboard, positionD3, pieces.whitePawn); // White Pawn at D3
        putPiece(chessboard, positionC4, pieces.blackKing); // Black King at C4

        let diagonalCapture: Move = {from: positionD3, to: positionC4, isValid: true};
        expect(isPossible.whitePawnMove(chessboard, diagonalCapture)).toBeTruthy();
    });

    it("Pawns can use the movement 'en passant' ", () => {
        putPiece(chessboard, positionA5, pieces.whitePawn);
        putPiece(chessboard, positionB7, pieces.blackPawn);

        isPossible.blackPawnMove(chessboard, moveB7_B5);
        historique(chessboard, moveB7_B5);
        chessboard.nbCoup++;

        let diagonalCapture: Move = {from: positionA5, to: positionB6, isValid: true};
        expect(isPossible.whitePawnMove(chessboard, diagonalCapture)).toBeTruthy();
    });

    it("Pawns cannot use the movement 'en passant'", () => {
        putPiece(chessboard, positionA4, pieces.whitePawn);
        putPiece(chessboard, positionB7, pieces.blackPawn);

        isPossible.blackPawnMove(chessboard, moveB7_B5);
        historique(chessboard, moveB7_B5);
        chessboard.nbCoup++;

        isPossible.blackPawnMove(chessboard, moveB5_B4);
        historique(chessboard, moveB5_B4);
        chessboard.nbCoup++;

        let diagonalCapture: Move = {from: positionA4, to: positionB5, isValid: true};
        expect(isPossible.whitePawnMove(chessboard, diagonalCapture)).toBeFalsy();
    });
});

describe("Test kingMove and blackKingMove()", () => {
    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.blackKing);
    });

    it("A King can move 1 square in all directions", () => {
        let simpleFowardMove: Move = {from: positionE4, to: positionD3, isValid: true};
        expect(isPossible.KingMove(chessboard, simpleFowardMove)).toBeTruthy();

        let simpleFowardMove1: Move = {from: positionE4, to: positionD4, isValid: true};
        expect(isPossible.KingMove(chessboard, simpleFowardMove1)).toBeTruthy();

        let simpleFowardMove2: Move = {from: positionE4, to: positionD5, isValid: true};
        expect(isPossible.KingMove(chessboard, simpleFowardMove2)).toBeTruthy();

        let simpleFowardMove3: Move = {from: positionE4, to: positionE3, isValid: true};
        expect(isPossible.KingMove(chessboard, simpleFowardMove3)).toBeTruthy();

        let simpleFowardMove4: Move = {from: positionE4, to: positionE5, isValid: true};
        expect(isPossible.KingMove(chessboard, simpleFowardMove4)).toBeTruthy();

        let simpleFowardMove5: Move = {from: positionE4, to: positionF3, isValid: true};
        expect(isPossible.KingMove(chessboard, simpleFowardMove5)).toBeTruthy();

        let simpleFowardMove6: Move = {from: positionE4, to: positionF4, isValid: true};
        expect(isPossible.KingMove(chessboard, simpleFowardMove6)).toBeTruthy();

        let simpleFowardMove7: Move = {from: positionE4, to: positionF5, isValid: true};
        expect(isPossible.KingMove(chessboard, simpleFowardMove7)).toBeTruthy();
    });

    it("A King cannot move more than 1 square", () => {
        let singleForward: Move = {from: positionE4, to: positionA4, isValid: true};
        expect(isPossible.KingMove(chessboard, singleForward)).toBeFalsy();

        let singleForward1: Move = {from: positionE4, to: positionH4, isValid: true};
        expect(isPossible.KingMove(chessboard, singleForward1)).toBeFalsy();

        let singleForward2: Move = {from: positionE4, to: positionE7, isValid: true};
        expect(isPossible.KingMove(chessboard, singleForward2)).toBeFalsy();

        let singleForward3: Move = {from: positionE4, to: positionE1, isValid: true};
        expect(isPossible.KingMove(chessboard, singleForward3)).toBeFalsy();

        let singleForward4: Move = {from: positionE4, to: positionB1, isValid: true};
        expect(isPossible.KingMove(chessboard, singleForward4)).toBeFalsy();

        let singleForward5: Move = {from: positionE4, to: positionB7, isValid: true};
        expect(isPossible.KingMove(chessboard, singleForward5)).toBeFalsy();

        let singleForward6: Move = {from: positionE4, to: positionH7, isValid: true};
        expect(isPossible.KingMove(chessboard, singleForward6)).toBeFalsy();

        let singleForward7: Move = {from: positionE4, to: positionH1, isValid: true};
        expect(isPossible.KingMove(chessboard, singleForward7)).toBeFalsy();
    });

    it("A blackKing cannot capure pieces from the same color", () => {
        putPiece(chessboard, positionE4, pieces.blackKing);
        putPiece(chessboard, positionE5, pieces.blackPawn);

        let forwardCapture: Move = {from: positionE4, to: positionE5, isValid: true};
        expect(isPossible.KingMove(chessboard, forwardCapture)).toBeFalsy();
    });

    it("A blackKing can capure pieces from a different color", () => {
        putPiece(chessboard, positionE4, pieces.blackKing);
        putPiece(chessboard, positionE5, pieces.whitePawn);

        let forwardCapture: Move = {from: positionE4, to: positionE5, isValid: true};
        expect(isPossible.KingMove(chessboard, forwardCapture)).toBeTruthy();
    });

    it("A blackking can use the roque", () => {
        putPiece(chessboard, positionE8, pieces.blackKing);

        putPiece(chessboard, positionA8, pieces.blackRook);
        expect(isPossible.KingMove(chessboard, moveE8_C8)).toBeTruthy();

        putPiece(chessboard, positionH8, pieces.blackRook);
        expect(isPossible.KingMove(chessboard, moveE8_G8)).toBeTruthy();
    });

    it("A blackKing cannot move on a square which is controlled by on opponent's", () => {
        putPiece(chessboard, positionE8, pieces.blackKing);
        putPiece(chessboard, positionC5, pieces.whiteBishop);

        expect(isPossible.KingMove(chessboard, moveE8_E7)).toBeFalsy();
    });
});

describe("Test whiteKingMove()", () => {
   
    /** The tests of movements :
     * - A King cannot move more than 1 square
     * - A King can move 1 square in all directions
     * has already been done above
     */

    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.whiteKing);
    });

    it("A whiteKing cannot capure pieces from the same color", () => {
        putPiece(chessboard, positionE4, pieces.whiteKing);
        putPiece(chessboard, positionE5, pieces.whitePawn);

        let forwardCapture: Move = {from: positionE4, to: positionE5, isValid: true};
        expect(isPossible.KingMove(chessboard, forwardCapture)).toBeFalsy();
    });

    it("A whiteKing can capure pieces from a different color", () => {
        putPiece(chessboard, positionE4, pieces.whiteKing);
        putPiece(chessboard, positionE5, pieces.blackPawn);

        let forwardCapture: Move = {from: positionE4, to: positionE5, isValid: true};
        expect(isPossible.KingMove(chessboard, forwardCapture)).toBeTruthy();
    });
    
    it("A whiteKing can use the roque", () => {
        putPiece(chessboard, positionE1, pieces.whiteKing);

        putPiece(chessboard, positionA1, pieces.whiteRook);
        expect(isPossible.KingMove(chessboard, moveE1_C1)).toBeTruthy();

        putPiece(chessboard, positionH1, pieces.whiteRook);
        expect(isPossible.KingMove(chessboard, moveE1_G1)).toBeTruthy();
    });

    it("A whiteKing cannot move on a square which is controlled by on opponent's", () => {
        putPiece(chessboard, positionE1, pieces.whiteKing);
        putPiece(chessboard, positionC4, pieces.blackBishop);

        expect(isPossible.KingMove(chessboard, moveE1_E2)).toBeFalsy();
    });
});

describe("Test QueenMove and blackQueenMove()", () => {
    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.blackQueen);
    });

    it("A Queen can move diagonally", () => {
        let diagonalMove1: Move = {from: positionE4, to: positionA8, isValid: true};
        expect(isPossible.QueenMove(chessboard, diagonalMove1)).toBeTruthy();
        
        let diagonalMove2: Move = {from: positionE4, to: positionB1, isValid: true};
        expect(isPossible.QueenMove(chessboard, diagonalMove2)).toBeTruthy();

        let diagonalMove3: Move = {from: positionE4, to: positionH7, isValid: true};
        expect(isPossible.QueenMove(chessboard, diagonalMove3)).toBeTruthy();

        let diagonalMove4: Move = {from: positionE4, to: positionH1, isValid: true};
        expect(isPossible.QueenMove(chessboard, diagonalMove4)).toBeTruthy();  
    });

    it("A Queen can move horizontally", () => {
        expect(isPossible.QueenMove(chessboard, moveE4_H4)).toBeTruthy();
        expect(isPossible.QueenMove(chessboard, moveE4_A4)).toBeTruthy();
    });

    it("A Queen can move vertically", () => {
        expect(isPossible.QueenMove(chessboard, moveE4_E8)).toBeTruthy();
        expect(isPossible.QueenMove(chessboard, moveE4_E1)).toBeTruthy();
    });

    it("A Queen can only move horizontally, vertically, and diagonally", () => {
        expect(isPossible.QueenMove(chessboard, moveE4_C7)).toBeFalsy();
        expect(isPossible.QueenMove(chessboard, moveE4_B2)).toBeFalsy();
    });

    it("A Queen cannot leap other pieces", () => {
        putPiece(chessboard, positionC6, pieces.whitePawn);
        putPiece(chessboard, positionF4, pieces.blackPawn);

        expect(isPossible.QueenMove(chessboard, moveE4_A8)).toBeFalsy();
        expect(isPossible.QueenMove(chessboard, moveE4_H4)).toBeFalsy();
    });

    it("A blackQueen cannot capure pieces from the same color", () => {
        putPiece(chessboard, positionH4, pieces.blackPawn);
        expect(isPossible.QueenMove(chessboard, moveE4_H4)).toBeFalsy();  
    });

    it("A blackQueen can capure pieces from a different color", () => {
        putPiece(chessboard, positionH4, pieces.whitePawn);
        expect(isPossible.QueenMove(chessboard, moveE4_H4)).toBeTruthy();
    });
});

describe("Test whiteQueenMove()", () => {

    /** The tests of movements :
     * - A Queen can move diagonally
     * - A Queen can move horizontally
     * - A Queen can move vertically
     * - A Queen can only move horizontally, vertically, and diagonally
     * - A Queen cannot leap other pieces
     * has already been done above
     */

    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.whiteQueen);
    });

    it("A whiteQueen cannot capure pieces from the same color", () => {
        putPiece(chessboard, positionH4, pieces.whitePawn);
        expect(isPossible.QueenMove(chessboard, moveE4_H4)).toBeFalsy();  
    });

    it("A whiteQueen can capure pieces from a different color", () => {
        putPiece(chessboard, positionH4, pieces.blackPawn);
        expect(isPossible.QueenMove(chessboard, moveE4_H4)).toBeTruthy();
    });
});

describe("Test BishopMove and blackBishopMove()", () => {
    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.blackBishop);
    });

    it("A Bishop can move diagonally", () => {
        let diagonalMove1: Move = {from: positionE4, to: positionA8, isValid: true};
        expect(isPossible.BishopMove(chessboard, diagonalMove1)).toBeTruthy();
        
        let diagonalMove2: Move = {from: positionE4, to: positionB1, isValid: true};
        expect(isPossible.BishopMove(chessboard, diagonalMove2)).toBeTruthy();

        let diagonalMove3: Move = {from: positionE4, to: positionH7, isValid: true};
        expect(isPossible.BishopMove(chessboard, diagonalMove3)).toBeTruthy();

        let diagonalMove4: Move = {from: positionE4, to: positionH1, isValid: true};
        expect(isPossible.BishopMove(chessboard, diagonalMove4)).toBeTruthy();  
    });

    it("A Bishop cannot move horizontally", () => {
        expect(isPossible.BishopMove(chessboard, moveE4_H4)).toBeFalsy(); 
        expect(isPossible.BishopMove(chessboard, moveE4_A4)).toBeFalsy(); 
    });

    it("A Bishop cannot move vertically", () => {
        expect(isPossible.BishopMove(chessboard, moveE4_E1)).toBeFalsy(); 
        expect(isPossible.BishopMove(chessboard, moveE4_E8)).toBeFalsy(); 
    });

    it("A blackBishop can capture a piece from another color", () => {
        putPiece(chessboard, positionA8, pieces.whiteKing);
        expect(isPossible.BishopMove(chessboard, moveE4_A8)).toBeTruthy(); 
    });

    it("A blackBishop cannot capture a piece from the same color", () => {
        putPiece(chessboard, positionA8, pieces.blackKing);
        expect(isPossible.BishopMove(chessboard, moveE4_A8)).toBeFalsy(); 
    });

    it("A Bishop cannot leap other pieces", () => {
        putPiece(chessboard, positionC6, pieces.whiteKing);
        expect(isPossible.BishopMove(chessboard, moveE4_A8)).toBeFalsy(); 
    });
});

describe("Test whiteBishopMove()", () => {
    
    /** The tests of movements :
     * - A Bishop can move diagonally
     * - A Bishop cannot move horizontally
     * - A Bishop cannot move vertically
     * - A Bishop cannot leap other pieces
     * has already been done above
     */

    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.whiteBishop);
    });

    it("A whiteBishop can capture a piece from another color", () => {
        putPiece(chessboard, positionA8, pieces.blackKing);
        expect(isPossible.BishopMove(chessboard, moveE4_A8)).toBeTruthy(); 
    });

    it("A whiteBishop cannot capture a piece from the same color", () => {
        putPiece(chessboard, positionA8, pieces.whiteKing);
        expect(isPossible.BishopMove(chessboard, moveE4_A8)).toBeFalsy(); 
    });
});

describe("Test knightMove and whiteKnightMove()", () => {
    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.whiteKnight);
    });

    it("A Knight can move two squares horizontally and one square vertically", () => {
        expect(isPossible.knightMove(chessboard, moveE4_G3)).toBeTruthy();
        expect(isPossible.knightMove(chessboard, moveE4_C3)).toBeTruthy();
        expect(isPossible.knightMove(chessboard, moveE4_G5)).toBeTruthy();
        expect(isPossible.knightMove(chessboard, moveE4_C5)).toBeTruthy();
    });

    it("A Knight can move two squares vertically and one square horizontally", () => {
        expect(isPossible.knightMove(chessboard, moveE4_F2)).toBeTruthy();
        expect(isPossible.knightMove(chessboard, moveE4_D2)).toBeTruthy();
        expect(isPossible.knightMove(chessboard, moveE4_D6)).toBeTruthy();
        expect(isPossible.knightMove(chessboard, moveE4_F6)).toBeTruthy();
    });

    it("A Knight can 'jump' obstacles" , () => {
        putPiece(chessboard, positionF4, pieces.whitePawn);
        putPiece(chessboard, positionF3, pieces.blackPawn);
        expect(isPossible.knightMove(chessboard, moveE4_F2)).toBeTruthy(); 
    });

    it("A Knight cannot move diagonally", () => {
        let diagonalMove1: Move = {from: positionE4, to: positionA8, isValid: true};
        expect(isPossible.knightMove(chessboard, diagonalMove1)).toBeFalsy();
        
        let diagonalMove2: Move = {from: positionE4, to: positionB1, isValid: true};
        expect(isPossible.knightMove(chessboard, diagonalMove2)).toBeFalsy();

        let diagonalMove3: Move = {from: positionE4, to: positionH7, isValid: true};
        expect(isPossible.knightMove(chessboard, diagonalMove3)).toBeFalsy();

        let diagonalMove4: Move = {from: positionE4, to: positionH1, isValid: true};
        expect(isPossible.knightMove(chessboard, diagonalMove4)).toBeFalsy();  
    });

    it("A Knight cannot move horizontally", () => {
        expect(isPossible.knightMove(chessboard, moveE4_H4)).toBeFalsy(); 
        expect(isPossible.knightMove(chessboard, moveE4_A4)).toBeFalsy(); 
    });

    it("A Knight cannot move vertically", () => {
        expect(isPossible.knightMove(chessboard, moveE4_E1)).toBeFalsy(); 
        expect(isPossible.knightMove(chessboard, moveE4_E8)).toBeFalsy(); 
    });

    it("A whiteKnight can capture a piece from another color", () => {
        putPiece(chessboard, positionF2, pieces.blackPawn);
        expect(isPossible.knightMove(chessboard, moveE4_F2)).toBeTruthy(); 
    });

    it("A whiteKnight cannot capture a piece from the same color", () => {
        putPiece(chessboard, positionF2, pieces.whitePawn);
        expect(isPossible.knightMove(chessboard, moveE4_F2)).toBeFalsy(); 
    });
});

describe("Test blackKnightMove()", () => {

    /** The tests of movements :
     * - A Knight can move two squares horizontally and one square vertically
     * - A Knight can move two squares vertically and one square horizontally
     * - A Knight can 'jump' obstacles
     * - A Knight cannot move diagonally
     * - A Knight cannot move horizontally
     * - A Knight cannot move vertically
     * has already been done above
     */

    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.blackKnight);
    });

    it("A blackKnight can capture a piece from another color", () => {
        putPiece(chessboard, positionF2, pieces.whitePawn);
        expect(isPossible.knightMove(chessboard, moveE4_F2)).toBeTruthy(); 
    });

    it("A blackKnight cannot capture a piece from the same color", () => {
        putPiece(chessboard, positionF2, pieces.blackPawn);
        expect(isPossible.knightMove(chessboard, moveE4_F2)).toBeFalsy(); 
    });
});

describe("Test RookMove and whiteRookMove()", () => {
    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.whiteRook);
    });

    it("A rook can move horizontally", () => {
        expect(isPossible.RookMove(chessboard, moveE4_H4)).toBeTruthy();
        expect(isPossible.RookMove(chessboard, moveE4_A4)).toBeTruthy();
    });

    it("A rook can move vertically", () => {
        expect(isPossible.RookMove(chessboard, moveE4_E8)).toBeTruthy();
        expect(isPossible.RookMove(chessboard, moveE4_E1)).toBeTruthy();
    });

    it("A rook cannot move diagonally", () => {
        let diagonalMove1: Move = {from: positionE4, to: positionA8, isValid: true};
        expect(isPossible.RookMove(chessboard, diagonalMove1)).toBeFalsy();

        let diagonalMove2: Move = {from: positionE4, to: positionB1, isValid: true};
        expect(isPossible.RookMove(chessboard, diagonalMove2)).toBeFalsy();

        let diagonalMove3: Move = {from: positionE4, to: positionH7, isValid: true};
        expect(isPossible.RookMove(chessboard, diagonalMove3)).toBeFalsy();

        let diagonalMove4: Move = {from: positionE4, to: positionH1, isValid: true};
        expect(isPossible.RookMove(chessboard, diagonalMove4)).toBeFalsy();  
    });

    it("A whiteRook can capture a piece from another color", () => {
        putPiece(chessboard, positionH4, pieces.blackKing);
        expect(isPossible.RookMove(chessboard, moveE4_H4)).toBeTruthy();       
    });

    it("A whiteRook cannot capture a piece from the same color", () => {
        putPiece(chessboard, positionH4, pieces.whiteKing);
        expect(isPossible.RookMove(chessboard, moveE4_H4)).toBeFalsy();       
    });

    it("A Rook cannot leap other pieces", () => {
        putPiece(chessboard, positionF4, pieces.whiteKing);
        expect(isPossible.RookMove(chessboard, moveE4_H4)).toBeFalsy();    
   });
}); 

describe("Test blackRookMove()", () => {

    /** The tests of movements :
     * - A Rook can move horizontally
     * - A Rook can move vertically
     * - A Rook cannot move diagonally
     * - A Rook cannot leap other pieces
     * has already been done above
     */
    
    beforeEach( () => {
        chessboard = createEmptyChessboard();
        putPiece(chessboard, positionE4, pieces.blackRook);
    });

    it("A blackRook can capture a piece from another color", () => {
        putPiece(chessboard, positionH4, pieces.whiteKing);
        expect(isPossible.RookMove(chessboard, moveE4_H4)).toBeTruthy();       
    });

    it("A blackRook cannot capture a piece from the same color", () => {
        putPiece(chessboard, positionH4, pieces.blackKing);
        expect(isPossible.RookMove(chessboard, moveE4_H4)).toBeFalsy();       
    });
}); 
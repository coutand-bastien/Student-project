import * as CD from './chessboard';
import { Move, enPassant, castling } from './movements';
import { equals, left, right, bottom, top } from "./position";
import { Piece, whitePawn, blackPawn } from "./piece";
import { kingdidMove, rookdidMove } from './historique-gestion';

/**
 * Checks whether a Black Pawn can perform a given move.
 * A pawn can move forward to the unoccupied square immediately in front of 
 * it on the same file, or on its first move it can advance two squares along 
 * the same file, provided both squares are unoccupied (black dots in the 
 * diagram); or the pawn can capture an opponent's piece on a square diagonally 
 * in front of it on an adjacent file, by moving to that square (black "x"s). 
 * 
 * A pawn has two special moves: the en passant capture and promotion.
 * 
 * @param chessboard : The chessboard of the current game.
 * @param move       : the movement of the piece.
 */
export function blackPawnMove(chessboard : CD.Chessboard, move : Move) : boolean {

    if (equals(move.to!, top(move.from!))) {
        //console.log("Single forward");
        return CD.isEmpty(chessboard, move.to!);
    }

    if (move.from!.rank === 6 && equals(move.to!, top(top(move.from!)))) {
        //console.log("Double forward");
        return CD.isEmpty(chessboard, top(move.from!)) && CD.isEmpty(chessboard, move.to!);
    }

    if (equals(move.to!, left(top(move.from!))) || equals(move.to!, right(top(move.from!)))) {
        let destination: CD.Square = CD.squareAtPosition(chessboard, move.to!);
        return ((!(destination.isEmpty || !destination.piece!.isWhite)) || (enPassant(chessboard, move)));
    }

    return false;
}

/**
 * A pawn can move forward to the unoccupied square immediately in front of 
 * it on the same file, or on its first move it can advance two squares along 
 * the same file, provided both squares are unoccupied (black dots in 
 * the diagram); or the pawn can capture an opponent's piece on a square diagonally 
 * in front of it on an adjacent file, by moving to that square (black "x"s). 
 * 
 * A pawn has two special moves: the en passant capture and promotion.
 * 
 * @param chessboard : The chessboard of the current game.
 * @param move       : the movement of the piece.
 */
export function whitePawnMove(chessboard : CD.Chessboard, move : Move) : boolean {

    if (equals(move.to!, bottom(move.from!))) {
        return CD.isEmpty(chessboard, move.to!);
    }

    if (move.from!.rank === 1 && equals(move.to!, bottom(bottom(move.from!)))) {
        return CD.isEmpty(chessboard, bottom(move.from!)) && CD.isEmpty(chessboard, move.to!);
    }

    if (equals(move.to!, left(bottom(move.from!))) || equals(move.to!, right(bottom(move.from!)))) {
        let destination: CD.Square = CD.squareAtPosition(chessboard, move.to!);
        return ((!(destination.isEmpty || destination.piece!.isWhite)) || (enPassant(chessboard, move)));
    }

    return false;
}

/**
 * Checks whether a King can perform a given move.
 * The king moves one square in any direction. 
 * 
 * @param chessboard : The chessboard of the current game.
 * @param move       : the movement of the piece.
 */
export function KingMove(chessboard : CD.Chessboard, move : Move) : boolean {

    if ((!CD.squareIsControl(chessboard, move)) && ((Math.abs(move.from!.file - move.to!.file) === 1) || (Math.abs(move.from!.rank - move.to!.rank) === 1))) {
        return CD.validEndOfPieceMouvement(chessboard, move);
    } 

    // Casteling
    if (Math.abs(move.from!.file - move.to!.file) === 2 && kingdidMove(chessboard) && rookdidMove(chessboard, move) && !CD.squareIsControl(chessboard, move)) {
        if(CD.isEmptySquareBetweenPieceMovement(chessboard, move)) {
            castling(chessboard, move);
            return true;
        }
    }

    return false;
}

/**
 * Checks whether a Queen can perform a given move.
 * The queen combines the power of a rook and bishop and can move any 
 * number of squares along a rank, file, or diagonal, but cannot leap over other pieces.
 * 
 * @param chessboard : The chessboard of the current game.
 * @param move       : the movement of the piece.
 */
export function QueenMove(chessboard : CD.Chessboard, move : Move) : boolean {

    if ((Math.abs(move.from!.file - move.to!.file) === Math.abs(move.from!.rank - move.to!.rank)) || 
        (move.from!.rank === move.to!.rank) ||  (move.from!.file === move.to!.file)) {

        return CD.isEmptySquareBetweenPieceMovement(chessboard, move);
    } 

    return false;
}

/**
 * Checks whether a Rook can perform a given move.
 * A rook can move any number of squares along a rank or file, 
 * but cannot leap over other pieces. 
 * 
 * @param chessboard : The chessboard of the current game.
 * @param move       : the movement of the piece.
 */
export function RookMove(chessboard : CD.Chessboard, move : Move) : boolean {

    if (move.from!.rank === move.to!.rank || move.from!.file === move.to!.file) {
        return CD.isEmptySquareBetweenPieceMovement(chessboard, move);
    }

    return false;
}

/**
 * Checks whether a Bishop can perform a given move.
 * A bishop can move any number of squares diagonally, 
 * but cannot leap over other pieces.
 * 
 * @param chessboard : The chessboard of the current game.
 * @param move       : the movement of the piece.
 */
export function BishopMove(chessboard : CD.Chessboard, move : Move) : boolean {
    
    // checking that the movements of "files" and "ranks" are equal
    if (Math.abs(move.from!.file - move.to!.file) === Math.abs(move.from!.rank - move.to!.rank)) {    
        return CD.isEmptySquareBetweenPieceMovement(chessboard, move);
    }

    return false;
}

/**
 * Checks whether a Knight can perform a given move.
 * A knight moves to any of the closest squares that are not on the 
 * same rank, file, or diagonal. (Thus the move forms an "L"-shape: 
 * two squares vertically and one square horizontally, or two 
 * squares horizontally and one square vertically.) 
 * 
 * The knight is the only piece that can leap over other pieces.
 * 
 * @param chessboard : The chessboard of the current game.
 * @param move       : the movement of the piece.
 */
export function knightMove(chessboard : CD.Chessboard, move : Move) : boolean {

    // two horizontal movements and one vertical or two vertical movements and one horizontal
    if ((Math.abs(move.from!.file - move.to!.file) == 2 && Math.abs(move.from!.rank - move.to!.rank) == 1) || 
        (Math.abs(move.from!.file - move.to!.file) == 1 && Math.abs(move.from!.rank - move.to!.rank) == 2)) {

        return CD.validEndOfPieceMouvement(chessboard, move);
    }

    return false;
} 

/**
 * Function that return true when one pawns are in the back of the adversaire in the chessboard.
 * 
 * @param chessboard : The chessboard of the current game.
 * @param historique : The historique for the game.
 */
export function isValidPromotion(chessboard : CD.Chessboard, move : Move) : boolean {

    if (chessboard.nbCoup != 0 && move.isValid) {
        let pawn : Piece = CD.pieceAtPosition(chessboard, move.to!);
        return ((move.to!.rank == 7 && pawn == whitePawn) || (move.to!.rank == 0 && pawn == blackPawn));
    }
    return false;
}
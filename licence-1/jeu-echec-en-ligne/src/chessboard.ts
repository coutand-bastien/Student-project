import * as pieces  from './piece';
import { Move, isMovePossible, move } from './movements';
import { Position, position } from './position';

export interface Square {
    position : Position;
    isEmpty  : boolean;
    piece?   : pieces.Piece;
}

export interface Chessboard {
    board      : Array<Array<Square>> ; //plateau de jeu
    nbCoup     : number;
    historique : Array<Move>; //historique des coups (optionnel)
}

export function isEmpty(chessboard : Chessboard, position : Position) : boolean {
    let square : Square = squareAtPosition(chessboard, position);
    return square.isEmpty;
}

export function squareAtPosition(chessboard : Chessboard, position : Position) : Square {
    let square : Square = chessboard.board[position.file][position.rank];
    return square;
}

export function pieceAtPosition(chessboard : Chessboard, position : Position) : pieces.Piece {
    let square : Square = squareAtPosition(chessboard, position);
    return square.piece!;
}

/**
 * Function that validate the final destination of a black and white piece.
 * 
 * @param chessboard : The chessboard of the current game.
 * @param move       : The movement of the piece.
 */
export function validEndOfPieceMouvement(chessboard : Chessboard, move : Move) : boolean {
    let destination : Square        = squareAtPosition(chessboard, move.to!);
    let source      : pieces.Piece  = pieceAtPosition(chessboard, move.from!);

    if (source.isWhite) {
        return destination.isEmpty || !destination.isEmpty && !destination.piece!.isWhite;
    } 
    
    return destination.isEmpty || !destination.isEmpty && destination.piece!.isWhite;     
}

/**
 * Function that returns true if there is no piece between the start move and the end move of 
 * a one piece.
 * 
 * @param chessboard : The chessboard of the current game.
 * @param move       : the movement of the piece.
 */
export function isEmptySquareBetweenPieceMovement(chessboard : Chessboard, move : Move) : boolean {
    let rank : number = move.from!.rank;
    let file : number = move.from!.file;

    while (rank != move.to!.rank || file != move.to!.file) {

        if (move.from!.file > move.to!.file) {file--;}
        if (move.from!.file < move.to!.file) {file++;}
        if (move.from!.rank > move.to!.rank) {rank--;}
        if (move.from!.rank < move.to!.rank) {rank++;}

        let position : Position = {rank : rank, file : file};

        if (!(squareAtPosition(chessboard, position).isEmpty)) {
            if (validEndOfPieceMouvement(chessboard, move) && rank == move.to!.rank && file == move.to!.file) {
                return true;
            }
            return false;
        }
    }

    return true;
}

/**
 * Function which return true if a square is attackable by an opponent's piece 
 * otherwise it returns false (useful for the check).
 * 
 * @param chessboard : The chessboard of the current game.
 * @param kingMove   : The move of the king. 
 */
export function squareIsControl(chessboard : Chessboard, kingMove : Move) : boolean {    
    for (let rank : number = 0; rank <= 7; rank++) {
        for (let file : number = 0; file <= 7; file++) {

            // allows to test only the parts present and not all the chessboard.
            if(!isEmpty(chessboard, position(file, rank)) && pieceAtPosition(chessboard, position(file, rank)).name != "King") {

                let possibleMovementOfOpenent : Move    = move(position(file, rank), kingMove.to!);
                let whiteKing                 : boolean = pieceAtPosition(chessboard, kingMove.from!).isWhite ? true : false;
                let otherWhitePiece           : boolean = pieceAtPosition(chessboard, possibleMovementOfOpenent.from!).isWhite ? true : false;

                if ((whiteKing && !otherWhitePiece) || (!whiteKing && otherWhitePiece)) {
                    if (isMovePossible(chessboard, possibleMovementOfOpenent)) {
                        return true;
                    }
                }
            }
        }
    }

    return false;
}

/**
 * function that returns a king square according to the turn of games. 
 * If it's black to play then we will get the black king and not the white 
 * because when we go into the function processMove, the move is played before 
 * the call of the function check.
 * 
 * @param chessboard : The chessboard of the current game. 
 */
export function shearchKing(chessboard : Chessboard) : Square {

    let nullSquare : Square = {position : {rank : 0, file : 0}, isEmpty : true};

    for (let rank : number = 0; rank <= 7; rank++) {
        for (let file : number = 0; file <= 7; file++) {

            let square : Square = squareAtPosition(chessboard, position(file, rank));

            // allows to test only the parts present and not all the chessboard.
            if(!isEmpty(chessboard, position(file, rank))) {
                if ((chessboard.nbCoup % 2 == 0 && square.piece! == pieces.whiteKing) || (chessboard.nbCoup % 2 == 1 && square.piece! == pieces.blackKing)) {
                    return square;
                } 
            }
        }
    }

    return nullSquare;
}

/**
 * Function that return an initialized chessboard.
 */
export function createInitialChessboard() : Chessboard {
    let chessboard : Chessboard = createChessboard();

    // ranks 2 - 6 are empty
    for(let rank : number = 2; rank < 6; rank++) {
        for(let col : number = 0; col < 8; col++) {
            let position : Position = {rank : rank, file : col};
            let square   : Square   = {position : position, isEmpty : true};
            chessboard.board[col][rank] = square;
        }
    }

    // Pawns in ranks 2 and 6
    for(let col : number = 0; col < 8; col++) {
        putPieceAtCoordinate(chessboard, col, 1, pieces.whitePawn);
        putPieceAtCoordinate(chessboard, col, 6, pieces.blackPawn);
    }

    // Kings and Queens
    putPieceAtCoordinate(chessboard, 4, 0, pieces.whiteKing);
    putPieceAtCoordinate(chessboard, 4, 7, pieces.blackKing);
    putPieceAtCoordinate(chessboard, 3, 0, pieces.whiteQueen);
    putPieceAtCoordinate(chessboard, 3, 7, pieces.blackQueen);

    // Bishops
    putPieceAtCoordinate(chessboard, 2, 0, pieces.whiteBishop);
    putPieceAtCoordinate(chessboard, 2, 7, pieces.blackBishop);
    putPieceAtCoordinate(chessboard, 5, 0, pieces.whiteBishop);
    putPieceAtCoordinate(chessboard, 5, 7, pieces.blackBishop);

    // Knights
    putPieceAtCoordinate(chessboard, 1, 0, pieces.whiteKnight);
    putPieceAtCoordinate(chessboard, 1, 7, pieces.blackKnight);
    putPieceAtCoordinate(chessboard, 6, 0, pieces.whiteKnight);
    putPieceAtCoordinate(chessboard, 6, 7, pieces.blackKnight);

    // Rooks
    putPieceAtCoordinate(chessboard, 0, 0, pieces.whiteRook);
    putPieceAtCoordinate(chessboard, 0, 7, pieces.blackRook);
    putPieceAtCoordinate(chessboard, 7, 0, pieces.whiteRook);
    putPieceAtCoordinate(chessboard, 7, 7, pieces.blackRook);

    return chessboard;
}

export function createEmptyChessboard() : Chessboard {
    let newChessboard : Chessboard = createChessboard();

    for(let rank : number = 0; rank < 8; rank++) {
        for(let col : number = 0; col < 8; col++) {
            let position : Position = {rank : rank, file : col};
            let square   : Square   = {position : position, isEmpty : true};
            newChessboard.board[col][rank] = square;
        }
    }

    return newChessboard;
}

function createChessboard() : Chessboard {
    let board : Square[][] = []
    for (let i = 0; i < 8; i++) {
        board[i] = [];
    }

    let newChessboard : Chessboard = {
        board      : board,
        nbCoup     : 0,
        historique : []
    };
    return newChessboard;
}

/**
 * Function that increments an array of Move for each valid move play to make it a history.
 * 
 * @param chessboard : The chessboard for the current game.
 * @param move       : the move to play at the moment.
 */
export function historique(chessboard : Chessboard, move : Move) : void {
    chessboard.historique.push(move);
    //console.log(chessboard.historique);
}

function putPieceAtCoordinate(chessboard : Chessboard, file : number, rank : number, piece : pieces.Piece) : void {
    let position : Position = {rank : rank, file : file};
    return putPiece(chessboard, position, piece);
}

export function putPiece(chessboard : Chessboard, position : Position, piece : pieces.Piece) : void {
    let board  : Array<Array<Square>>   = chessboard.board;
    let square : Square                 = {position : position, isEmpty : false, piece : piece};
    board[position.file][position.rank] = square;
}
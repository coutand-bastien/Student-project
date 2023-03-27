import { Position, position } from './position';
import * as pieces       from './piece';
import * as MV           from './move-validation'
import * as CD           from './chessboard';
import { isWhiteToPlay } from './historique-gestion';

const VALID_MOVE_STRING: RegExp = new RegExp('([a-z]|[A-Z])([1-8])-([A-H]|[a-z])([1-8])');

export interface Move {
    isValid : boolean;
    from?   : Position;
    to?     : Position;
}

/**
 * Creates a new Move from two Positions, representing
 * the Move's initial and final position.
 * 
 * @param from : The initial position
 * @param to   : The final position
 */
export function move(from : Position, to : Position) : Move {
    let move: Move = {from: from, to: to, isValid: true};
    return move;
}

/**
 * Processes a move received from a client browser or an historique (during the backReturn, that why the variable move is build like that).
 * If the move is valid and possible, the move is performed and this function
 * returns true. Furthemore, an historique is implements. Otherwise, it returns false.
 * 
 * @param chessboard     : The chessboard for the current game.
 * @param moveString     : The string received from the client containing a move.
 * @param historiqueMove : The move in the historique.
 */
export function processMove(chessboard : CD.Chessboard, moveString : string, historiqueMove : Move) : boolean {
    
    let move : Move = moveString === "" ? historiqueMove : parseMoveString(moveString);

    if (move.isValid && isWhiteToPlay(chessboard, move) && isMovePossible(chessboard, move)) {
        
        if (!check(chessboard) || (check(chessboard) && MV.KingMove(chessboard, move))) {
            performMove(chessboard, move); 
            CD.historique(chessboard, move);
        } 
        
        if (check(chessboard)) {
            console.log("ECHEC");
        }
    } 
    else {
        console.log("Invalid movement !");
        return false;

    }

    return true;
}

/**
 * Parses a string in the format "A1-F8" and returns a Move.
 * If the format is not valid, returns a Move with isValid === false.
 * 
 * @param movementString : A 5 characters string containing a move.
 */
export function parseMoveString(movementString : string) : Move {
    let newMove : Move;

    if (movementString.length != 5 || !movementString.match(VALID_MOVE_STRING)) {
        let invalidMove : Move = {isValid : false};
        newMove = invalidMove;
    } 
    else {
        let fromFile : number = movementString.charCodeAt(0);
        let fromRank : number = parseInt(movementString[1]);
        let toFile   : number = movementString.charCodeAt(3);
        let toRank   : number = parseInt(movementString[4]);

        // In Unicode, charCode('A') == 65, charCode('a') == 97.
        // Remember that Arrays start from [0][0] == position 'A1'.
        let from : Position = {rank : fromRank -1, file : fromFile > 90 ? fromFile - 97 : fromFile - 65};
        let to   : Position = {rank : toRank -1,   file : toFile > 90   ? toFile - 97   : toFile - 65 };

        newMove = {isValid: true, from: from, to: to};
    }

    return newMove;
}

/**
 * Checks whether a move is possible in the given chessboard.
 * 
 * @param chessboard : The chessboard for the current game.
 * @param move       : The movement to be treated.
 */
export function isMovePossible(chessboard : CD.Chessboard, move : Move) : boolean {
    let square : CD.Square = CD.squareAtPosition(chessboard, move.from!);
    if (square.isEmpty) { return false; }

    let piece : pieces.Piece = square.piece!;

    switch(piece) {
        case pieces.whitePawn   : return  MV.whitePawnMove(chessboard, move);
        case pieces.whiteKing   : return  MV.KingMove(chessboard, move);
        case pieces.whiteQueen  : return  MV.QueenMove(chessboard, move);
        case pieces.whiteBishop : return  MV.BishopMove(chessboard, move);
        case pieces.whiteKnight : return  MV.knightMove(chessboard, move);
        case pieces.whiteRook   : return  MV.RookMove(chessboard, move);
        case pieces.blackPawn   : return  MV.blackPawnMove(chessboard, move);
        case pieces.blackKing   : return  MV.KingMove(chessboard, move);
        case pieces.blackQueen  : return  MV.QueenMove(chessboard, move);
        case pieces.blackBishop : return  MV.BishopMove(chessboard, move);
        case pieces.blackKnight : return  MV.knightMove(chessboard, move);
        case pieces.blackRook   : return  MV.RookMove(chessboard, move);
    }

    return false;
}

/**
 * performMove allows to apply the movement on the chessboard.
 * 
 * @param chessboard : The chessboard for the current game.
 * @param move       : The movement to be treated.
 */
export function performMove(chessboard : CD.Chessboard, move : Move) : void {
    let source      : CD.Square = CD.squareAtPosition(chessboard, move.from!);
    let destination : CD.Square = CD.squareAtPosition(chessboard, move.to!);

    destination.piece   = source.piece;
    destination.isEmpty = false;
    source.isEmpty      = true;
    chessboard.nbCoup   = chessboard.nbCoup + 1;
}

/**
 * function that returns true if a pawn makes a takeover "en passant".
 * 
 * In chess, taking by the way is a special possibility to capture a pawn. When a 
 * pawn is on the fifth row1 and the opponent advances a pawn of a neighboring column 
 * by two spaces (the two pawns are then side-by-side on the same row), the first pawn 
 * may take the second. To make the take by the way, the player advances his pawn 
 * diagonally on the sixth row and the column of the opponent's pawn, and removes 
 * him from the chessboard.
 * @link https://fr.wikipedia.org/wiki/En_passant_(%C3%A9checs).
 * 
 * @param chessboard : The chessboard for the current game.
 * @param move       : The move of the pawns.
 */
export function enPassant(chessboard : CD.Chessboard, move : Move) : boolean {   

    if (chessboard.nbCoup != 0) {
        let lastMove            : Move         = chessboard.historique[chessboard.historique.length - 1];
        let destinationLastMove : pieces.Piece = CD.pieceAtPosition(chessboard, lastMove.to!);
        let sourcePiece         : pieces.Piece = CD.pieceAtPosition(chessboard, move.from!).isWhite ? pieces.whitePawn : pieces.blackPawn;

        // if the two pawns are in the same rank but in a one file difference.
        if (Math.abs(move.from!.file - lastMove.to!.file) == 1 && Math.abs(move.from!.rank - lastMove.to!.rank) == 0) {
            if (Math.abs(lastMove.from!.rank - lastMove.to!.rank) == 2 && destinationLastMove != sourcePiece) {
                
                // create an empty square in the place of the piece which are eating
                    let lastSquare : CD.Square = CD.squareAtPosition(chessboard, lastMove.to!);  
                    lastSquare.isEmpty = true;

                    return true;
            }
        }
    }

    return false;
}

/**
 * Function that change the piece after the validation of the promotion.
 * 
 * @param chessboard      : The chessboard for the current game.
 * @param move            : The move of the pawns.
 * @param piecePromotion  : The piece who want the user.
 */
export function promotion(chessboard : CD.Chessboard, move : Move, piecePromotion : string) : void {
    
    if (chessboard.nbCoup != 0) {
        let square : CD.Square = CD.squareAtPosition(chessboard, move.to!);
        
        switch(piecePromotion) {
            case "rook"   : square.piece!.isWhite ? square.piece = pieces.whiteRook   : square.piece = pieces.blackRook;   break;
            case "queen"  : square.piece!.isWhite ? square.piece = pieces.whiteQueen  : square.piece = pieces.blackQueen;  break;
            case "knight" : square.piece!.isWhite ? square.piece = pieces.whiteKnight : square.piece = pieces.blackKnight; break;
            case "bishop" : square.piece!.isWhite ? square.piece = pieces.whiteBishop : square.piece = pieces.blackBishop; break;
        }
    }
}

/**
 * Function that allows the change of place between the tower and the king during a castling.
 * All the verifications have already been made.
 * 
 * @param chessboard : The chessboard for the current game.
 * @param kingMove   : The move of the king during the Castling.
 */
export function castling(chessboard : CD.Chessboard, kingMove : Move) : void {

    let pieceIsWhite : boolean = CD.pieceAtPosition(chessboard, kingMove.from!).isWhite ? true : false; 

    if (kingMove.from!.file > kingMove.to!.file) {
        if (pieceIsWhite) {
            // delete the old rook...
            let oldRookPlace : CD.Square = CD.squareAtPosition(chessboard, {rank : 0, file : 0});
            oldRookPlace.isEmpty = true;

            // ... and place a new rook in the position of the casteling
            let newRookPlace : Position = {rank : 0, file : 3};
            CD.putPiece(chessboard, newRookPlace, pieces.whiteRook);
        }
        else {
            let oldRookPlace : CD.Square = CD.squareAtPosition(chessboard, {rank : 7, file : 0});
            oldRookPlace.isEmpty = true;

            let newRookPlace : Position = {rank : 7, file : 3};
            CD.putPiece(chessboard, newRookPlace, pieces.blackRook);
        }
    } 
 
    if (kingMove.from!.file < kingMove.to!.file) {
        if (pieceIsWhite) {
            let oldRookPlace : CD.Square = CD.squareAtPosition(chessboard, {rank : 0, file : 7});
            oldRookPlace.isEmpty = true;

            let newRookPlace : Position = {rank : 0, file : 5};
            CD.putPiece(chessboard, newRookPlace, pieces.whiteRook);
        }     
        else {
            let oldRookPlace : CD.Square = CD.squareAtPosition(chessboard, {rank : 7, file : 7});
            oldRookPlace.isEmpty = true;

            let newRookPlace : Position = {rank : 7, file : 5};
            CD.putPiece(chessboard, newRookPlace, pieces.blackRook);
        } 
    }
}

/**
 * Function which return true if a king is attackable by an opponent's piece 
 * otherwise it returns false (useful for the check).
 * 
 * @param chessboard : The chessboard of the current game.
 */
export function check(chessboard : CD.Chessboard) : boolean {   
    
    let placeOfKingPiece : CD.Square = CD.shearchKing(chessboard);

    for (let rank : number = 0; rank <= 7; rank++) {
        for (let file : number = 0; file <= 7; file++) {
                
            // allows to test only the parts present, except the king and not all the chessboard.
            if(!CD.isEmpty(chessboard, position(file, rank)) && CD.pieceAtPosition(chessboard, position(file, rank)).name != "King") {

                let possibleMovementOfOpenent : Move    = move(position(file, rank), placeOfKingPiece.position);
                let isWhitePiece              : boolean = CD.pieceAtPosition(chessboard, possibleMovementOfOpenent.from!).isWhite ? true : false;                       

                if ((placeOfKingPiece.piece! == pieces.whiteKing && !isWhitePiece) || (placeOfKingPiece.piece! == pieces.blackKing && isWhitePiece)) {
                    if (isMovePossible(chessboard, possibleMovementOfOpenent)) {
                        return true;
                    }
                }
            }
        }      
    } 

    return false;
}

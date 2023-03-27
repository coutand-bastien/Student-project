import { Move, processMove, promotion } from './movements';
import * as pieces from "./piece";
import { Chessboard, createInitialChessboard, pieceAtPosition } from './chessboard';
import { isValidPromotion } from './move-validation';

/**
 * Function that returns true if the number of move is even and the piece is white else returns false 
 * if it's odd and the piece is black.
 * 
 * @param chessboard : The chessboard for the current game.
 * @param move       : The move of one piece in the chessboard.
 */
export function isWhiteToPlay(chessboard : Chessboard, move : Move) : boolean {
    let startOfMovement : pieces.Piece = pieceAtPosition(chessboard, move.from!);
    return (chessboard.nbCoup % 2 == 0 && startOfMovement.isWhite) || (chessboard.nbCoup % 2 == 1 && !startOfMovement.isWhite);
}

/**
 * Function that allow a back return in the chessboard thanks to the 
 * replay of the historique less one move.
 * 
 * @param chessboard          : The chessboard for the current game.
 * @param historiquePromotion : The historique of all the promotion during the game.
 */
export function backReturn(chessboard : Chessboard, historiquePromotion : Array<string>) : Chessboard {
    let historique : Array<Move> = chessboard.historique;
    let j          : number      = 0;
    
    chessboard = createInitialChessboard();

    for (let i = 0; i < historique.length - 1; i++) {
        processMove(chessboard, "", historique[i]);

        if(isValidPromotion(chessboard, historique[i])) {
            promotion(chessboard, historique[i], historiquePromotion[j]);
            j++;
        }
    }

    return chessboard;
}

/**
 * Function that looks in the history if the starting position of the king appears there, 
 * if yes returns false.
 * 
 * @param chessboard : The chessboard of the current game.
 */
export function kingdidMove(chessboard : Chessboard) : boolean {
    let historique  : Array<Move> = chessboard.historique
   
    historique.forEach(element => {
        let sourcePiece : pieces.Piece = pieceAtPosition(chessboard, element.from!).isWhite ? pieces.whiteKing : pieces.blackKing; 
       
        if (element.from! == {rank : 0, file : 4} && sourcePiece == pieces.whiteKing) {return false;}  
        if (element.from! == {rank : 7, file : 4} && sourcePiece == pieces.blackKing) {return false;}    
    });

    return true;
}

/**
 * Function that looks in the history if the starting position of the tower according 
 * to the movement of the king appears there, if so returns false.
 * 
 * @param chessboard : The chessboard of the current game.
 * @param kingMove   : The move of the king during the Castling.
 */
export function rookdidMove(chessboard : Chessboard, kingMove : Move) : boolean {
    let historique : Array<Move> = chessboard.historique
   
    historique.forEach(element => {
        let sourcePiece : pieces.Piece = pieceAtPosition(chessboard, element.from!).isWhite ? pieces.whiteRook : pieces.blackRook; 
       
        if (element.from! == {rank : 0, file : 0} && sourcePiece == pieces.whiteRook && kingMove.from!.file > kingMove.to!.file) {return false;}  
        if (element.from! == {rank : 0, file : 7} && sourcePiece == pieces.whiteRook && kingMove.from!.file < kingMove.to!.file) {return false;}  
        if (element.from! == {rank : 7, file : 0} && sourcePiece == pieces.blackRook && kingMove.from!.file > kingMove.to!.file) {return false;}  
        if (element.from! == {rank : 7, file : 7} && sourcePiece == pieces.blackRook && kingMove.from!.file < kingMove.to!.file) {return false;}
    });

    return true;
}
export interface Piece {
    symbol  : string;
    isWhite : boolean;
    name    : string;
}

export const whitePawn   : Piece = {symbol : "♙", name: "Pawn", isWhite : true};
export const whiteKing   : Piece = {symbol : "♔", name: "King", isWhite : true};
export const whiteQueen  : Piece = {symbol : "♕", name: "Queen", isWhite : true};
export const whiteRook   : Piece = {symbol : "♖", name: "Rook", isWhite : true};
export const whiteKnight : Piece = {symbol : "♘", name: "Knight", isWhite : true};
export const whiteBishop : Piece = {symbol : "♗", name: "Bishop", isWhite : true};

export const blackPawn   : Piece = {symbol : "♟", name: "Pawn", isWhite : false};
export const blackKing   : Piece = {symbol : "♚", name: "King", isWhite : false};
export const blackQueen  : Piece = {symbol : "♛", name: "Queen", isWhite : false};
export const blackRook   : Piece = {symbol : "♜", name: "Rook", isWhite : false};
export const blackKnight : Piece = {symbol : "♞", name: "Knight", isWhite : false};
export const blackBishop : Piece = {symbol : "♝", name: "Bishop", isWhite : false};
import express    = require('express');
import bodyParser = require('body-parser');

import { Chessboard, createInitialChessboard } from './chessboard';
import { processMove, promotion, parseMoveString, Move, check} from './movements';
import { backReturn }  from "./historique-gestion";
import { isValidPromotion } from "./move-validation";

const PORT : number = 8080;
const PUBLIC_DIR    = 'client';

class HttpServer {
  port : number;

  constructor(port: number) {
    this.port = port;
  }

  public onStart() : void {
    let chessboard          : Chessboard          = createInitialChessboard();
    let app                 : express.Application = express();
    let nullMove            : Move                = {isValid : false};
    let historiquePromotion : Array<string>       = [];
    let unparsedMove        : string;

    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({ extended: true }));
    app.use(express.static(PUBLIC_DIR));
    app.set('view engine', 'ejs');

    app.listen(this.port, () => {
      console.log("Application lancée à l'adresse http://localhost:" + this.port);
    });

    app.get('/',  (req: express.Request, res: express.Response) => {
      res.render('index', {error: null, promotion : false});
    });

    // promotion dans le res.render permet d'afficher où non les inputs pour la promotion dans index.ejs.
    app.post("/", (req: express.Request, res: express.Response) => {
      unparsedMove  = req.body.move;
      let didPerfom : boolean = processMove(chessboard, unparsedMove, nullMove);
      let message   : string  = didPerfom ? (check(chessboard) ? "ECHEC" : "") : "Veuillez saisir un mouvement valide!";
      res.render('index', {error: message, promotion : isValidPromotion(chessboard, parseMoveString(unparsedMove))});
    });

    // récupération de la requète POST pour faire la promotion d'un pion de l'échiquier
    app.post("/promotion", (req: express.Request, res: express.Response) => {
      let piecePromotion : string = (req.body.piecePromotion).toLowerCase();
      let parsedMove     : Move   = parseMoveString(unparsedMove);

      while (piecePromotion != "rook" && piecePromotion != "queen" && piecePromotion != "bishop" && piecePromotion != "knight" ) {
        res.render('index', {error : "Veuillez saisir une piece valide !", promotion : true});
      }

      // insertion de la piece promue (string) dans un tableau qui contient toutes les promotions.
      historiquePromotion.push(piecePromotion);

      promotion(chessboard, parsedMove, piecePromotion);
      res.redirect('/');
     });

    // récupération de la requète POST pour reset tout l'échiquier
    app.post("/reset", (req: express.Request, res: express.Response) => {
      chessboard = createInitialChessboard();
      historiquePromotion = [];
      res.redirect('/');
    });

    // récupération de la requète POST pour faire un coup en arriere l'échiquier
    app.post("/coupArriere", (req: express.Request, res: express.Response) => {
     chessboard = backReturn(chessboard, historiquePromotion);
     res.redirect('/');
    });

    app.get("/status.js", (req: express.Request, res: express.Response) => {
      res.end("var boardJSON= " + JSON.stringify(chessboard));
    });
  }
}

let server : HttpServer = new HttpServer(PORT);
server.onStart();
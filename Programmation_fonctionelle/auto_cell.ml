(*
    @goal:
        Cellular automaton modeling the diffusion of particles in a medium. 
        Some of the particles are fixed while others move. The two rules governing 
        the behavior of particles are:

        - Aggregation : if a mobile cell encounters (= is close to) a fixed particle, 
                        it aggregates to this particle and attaches itself;

        - Diffusion   : if a mobile particle is close to an empty location, 
                        it moves to that location leaving the one it leaves empty.

    @authors: 
        - COUTAND Bastien (bastien.coutand@etu.univ-nantes.fr)
        - GARNIER Cyprien (cyprien.garnier@etu.univ-nantes.fr)

    @date: 25/03/2021 by COUTAND Bastien
    @version: 4.08.1 - Unbuntu
*)

(* ------------------------- modules ------------------------- *) 


open Graphics;;
open List;;


(* ------------------------- types ------------------------- *)


type position = {
    x: int ; 
    y: int;
};;

type state = Empty | Movable | Fixed;;

type cell  = {
    pos:position; 
    state:state
};;


(* ------------------------- variables ------------------------- *)


let width_size              = 1500;;
let height_size             = 1000;;
let rect_size               = 20;;
let nb_rect_by_width        = width_size / rect_size;;
let nb_rect_by_height       = height_size / rect_size;;
let nb_movable_cell_by_time = nb_rect_by_width;;

exception End;;


(* ------------------------- terminal display ------------------------- *)


(**
    @role: 
        Displays a cell with its coordinates and state.
*)
let print_cell cell =
    print_string " x: "; print_int cell.pos.x; print_string "; y: "; print_int cell.pos.y;

    match cell.state with
    | Empty   -> print_string "; state: Empty";   print_newline ()
    | Movable -> print_string "; state: Movable"; print_newline ()
    | Fixed   -> print_string "; state: fixed";   print_newline ()   
;;

(**
    @role: 
        Displays a list of cells with their coordinates and states.
*)
let print_cell_list cell_list = 
    print_string "List:"; print_newline ();

    let rec aux list =
        match list with
        | []      -> print_string "End List"; print_newline () 
        | el :: l -> print_cell el; aux l
    in aux cell_list
;;


(* ------------------------- functions ------------------------- *)


(** 
    @role :
        Draw a grid line by line, starting from the lower left corner.

    @return :
        List containing all the positions of the cells (their lower left corner).
*)
let grid () =
    let list_cel = [] in
    set_color black;

    let rec grid_rec i j cell_list =
        let new_list = cell_list@[{pos = {x = j*rect_size; y = i*rect_size}; state = Empty}] in

        match (i, j) with 
        | (a, b) when a = (nb_rect_by_height-1) && b = (nb_rect_by_width-1) -> 
            begin
                draw_rect (rect_size * j) (rect_size * i) rect_size rect_size; 
                new_list
            end
        | (_, b) when b = (nb_rect_by_width-1) -> 
            begin
                draw_rect (rect_size * j) (rect_size * i) rect_size rect_size;
                grid_rec (i+1) 0 new_list
            end
        | (_, _) -> 
            begin
                draw_rect (rect_size * j) (rect_size * i) rect_size rect_size;
                grid_rec i (j+1) new_list
            end
    in grid_rec 0 0 list_cel
;;

(**
    @role:
        Count the number of occurrences in a movable cell list.

    @tests :
        let p = [
            {pos={x=rect_size*4;y=rect_size*4};state=Movable};
            {pos={x=rect_size*5;y=rect_size*4};state=Movable};
            {pos={x=rect_size*5;y=rect_size*4};state=Empty};
            {pos={x=rect_size*5;y=rect_size*4};state=Fixed}
        ];; 
        count_occu_movable p;; --> 2
*)
let count_occu_movable cell_list =
    let rec aux list acc =
        match list with
        | []                              -> acc
        | el :: l when el.state = Movable -> aux l (acc+1)
        | el :: l                         -> aux l acc
    in aux cell_list 0
;;


(* ------- Color management ------- *)


(**
    @role: 
        choose the color according to the state of the cell in parameter.

    @choice: 
        returns false for the Empty state because it is useful to 
        be able to keep the gridlines. (see the fill_one_cell function).
 *)
let color_choice cell =
    match cell.state with
    | Empty   -> set_color white; false
    | Movable -> set_color red;   true
    | Fixed   -> set_color green; true
;;

(** 
    @role: 
        Color the cell as a parameter according to its state. 

    @choice:
        If Empty then applies the color white and redraws a black square to keep
        the gridlines. Indeed, if we put set_color white only, then the borders of 
        the cell will be erased when filling it.

    @test :
        fill_one_cell {pos = {x = rect_size; y = 0}; state = Movable};; ---> red;;
        fill_one_cell {pos = {x = rect_size; y = 0}; state = Fixed};;   ---> green;;
*)
let fill_one_cell cell =
    if color_choice cell then
        fill_rect (cell.pos.x) (cell.pos.y) rect_size rect_size
    else
        fill_rect (cell.pos.x) (cell.pos.y) rect_size rect_size;

        set_color black;
        draw_rect (cell.pos.x) (cell.pos.y) rect_size rect_size
;;

(**
    @role:
        colors all cells in a list according to their state.
 *)
let rec fill_all_cells cell_list =
    match cell_list with
    | []      -> cell_list
    | el :: l -> fill_one_cell el; fill_all_cells l
;;


(* ------- Local rule application ------- *)


(**
    @role: 
        Determine the neighbors (cells next to the target cells).

    @return:
        Returns a list of cells neighboring the target cells.

    @tests :
        let p = [{pos = {x = rect_size*4; y = rect_size*4}; state = Movable}];;
        let t = {pos = {x = rect_size*5; y = rect_size*4}; state = Fixed};;
        neighborhood p t Movable = p;; ---> true 

        let p = [{pos = {x = rect_size*4; y = rect_size*4}; state = Movable}];;
        let i = {pos = {x = rect_size*7; y = rect_size*4}; state = Fixed};;
        neighborhood p i Movable = p;; ---> false 
*)
let rec neighborhood cell_list cell state =   
    let possible_position_list = [   
        {pos={x = cell.pos.x + rect_size; y = cell.pos.y + rect_size}; state = state };    
        {pos={x = cell.pos.x + rect_size; y = cell.pos.y};             state = state };    
        {pos={x = cell.pos.x + rect_size; y = cell.pos.y - rect_size}; state = state };    
        {pos={x = cell.pos.x;             y = cell.pos.y - rect_size}; state = state };   
        {pos={x = cell.pos.x - rect_size; y = cell.pos.y - rect_size}; state = state };    
        {pos={x = cell.pos.x - rect_size; y = cell.pos.y};             state = state };   
        {pos={x = cell.pos.x - rect_size; y = cell.pos.y + rect_size}; state = state }; 
        {pos={x = cell.pos.x;             y = cell.pos.y + rect_size}; state = state } 
    ] in
    filter (fun a -> exists (fun b -> b = {pos = a.pos; state = a.state}) cell_list) possible_position_list 
;;


(**
    @role:
        Changes a movable cell to a fixed cell if it is in its neighborhood.

    @choice:
         choice to take element fixed in the list and not movable 
         because there are less to choose most of the time, therefore 
         performance gain.

    @test:
        let p = [
            {pos = {x = rect_size;   y = rect_size}; state = Movable};
            {pos = {x = rect_size*2; y = rect_size}; state = Fixed}
        ];; 
        aggregation p;; ---> [
            {pos = {x = rect_size;   y = rect_size}; state = Fixed};
            {pos = {x = rect_size*2; y = rect_size}; state = Fixed}
        ];; 
*)
let aggregation cell_list =
    let rec aux start_list end_list =
        match start_list with
        | [] -> end_list
        | fixed_el :: l when fixed_el.state = Fixed ->                                                        (* for all Fixed cells ... *)
            begin
                let pos_neighborhood_list = neighborhood end_list fixed_el Movable in                         (* list of all Movable cells around the Fixed cell *)
                
                let rec aux2 pos_neigh_list start_l end_l =                                                   (* for all Movable cells around the Fixed cell *)
                    match pos_neigh_list with 
                    | [] -> aux start_l end_l                                                                 (* if the list is empty, we go to the next Fixed cell *)
                    | neighborhood_el :: l2  ->                                                               (* otherwise we pass it to Fixed *)     
                        begin
                            let new_cel      = {pos = neighborhood_el.pos; state = Fixed} in                  (* new cell with coord of the neighborhood and state become Fixed *)
                            let new_end_list = [new_cel]@(filter (fun x -> x <> neighborhood_el) end_list) in  (* remove the old cell and add the new one in front of *)      
                                            
                            fill_one_cell new_cel;                                                             (* color the Fixed cell *)    
                            aux2 l2 start_l new_end_list                                                      (* we relaunch on the same fixed cell in case there are still Movable neighborhoods cells *)
                        end
                in aux2 pos_neighborhood_list l end_list
            end
        | _ :: l -> aux l end_list
    in aux cell_list cell_list
;;

(**
                      Numbering of neighboring cells of the main cell (x)
                            +-----------+-----------+-----------+
                            |           |           |           |
                            |     6     |     7     |     0     |
                            |           |           |           |
                            |           |           |           |
                            +-----------+-----------+-----------+
                            |           |           |           |
                            |     5     |     x     |     1     |
                            |           |           |           |
                            |           |           |           |
                            +-----------+-----------+-----------+
                            |           |           |           |
                            |     4     |     3     |     2     |
                            |           |           |           |
                            |           |           |           |
                            +-----------+-----------+-----------+

    @role:
        if a mobile particle is close to an empty location, 
        it moves to that location leaving the one it leaves empty.

    @test:
        let p = [
            {pos = {x = rect_size*5; y = rect_size*4}; state = Movable};
            {pos = {x = rect_size*6; y = rect_size*5}; state = Fixed};
            {pos = {x = rect_size*6; y = rect_size*4}; state = Empty};
            {pos = {x = rect_size*6; y = rect_size*3}; state = Empty};
            {pos = {x = rect_size*5; y = rect_size*3}; state = Empty};
            {pos = {x = rect_size*4; y = rect_size*3}; state = Empty};
            {pos = {x = rect_size*4; y = rect_size*4}; state = Empty};    
            {pos = {x = rect_size*5; y = rect_size*5}; state = Empty};    
            {pos = {x = rect_size*4; y = rect_size*5}; state = Empty}
        ];;
        
        diffusion p;; ---> modification of a cell in Movable and the old Movable in Empty
*)
let diffusion cell_list =
    let rec aux start_list end_list =
        match start_list with
        | [] -> end_list
        | movable_el :: l when movable_el.state = Movable ->                                                                                                 (* for all Movable cells ... *)
            begin    
                let pos_neighborhood_list = neighborhood end_list movable_el Empty in

                match pos_neighborhood_list with
                | [] -> end_list                                                           
                | _  -> 
                    begin
                        let neighborhood_empty_cel = nth pos_neighborhood_list (Random.int (length pos_neighborhood_list)) in                                (* choose a position at random in the list of possible cell *)
                        let new_movable_cel        = {pos = neighborhood_empty_cel.pos; state = Movable}                   in                                (* new cell with coord of the neighborhood and state become Movable *)                                                   
                        let old_movable_cel        = {pos = movable_el.pos;             state = Empty}                     in                                (* old cell with Movable cell coord and state become Empty *) 

                        fill_one_cell new_movable_cel;                                                                                                       (* color in the new Movable cell *)
                        fill_one_cell old_movable_cel;                                                                                                       (* color the old cell Movable *)
                        
                        let new_end_list = [old_movable_cel; new_movable_cel]@(filter (fun x -> x <> movable_el && x <> neighborhood_empty_cel) end_list) in (* remove the old cells and add the new ones in front*) 
                        aux l new_end_list
                    end
            end 
        | _ :: l-> aux l end_list
    in aux cell_list cell_list
;;

(** 
    @role: 
        advances the model by +1 over time.
    
    @choice:
        if ... else ... for more speed at the exec level for small cell values.
*)
let time_plus_one cell_list =
    if rect_size <= 20 then
        diffusion (aggregation (diffusion (aggregation (diffusion (aggregation (diffusion (aggregation (diffusion (aggregation (diffusion (aggregation (diffusion (aggregation (diffusion (aggregation cell_list)))))))))))))))
    else
        diffusion (aggregation cell_list);
;;

(**
    @role:
        returns a list of Empty cells on one side of the window
 *)
let empty_cells_positions_on_windows_side cell_list =
    filter (fun a -> 
        (
            a.pos.y = 0 && a.pos.x >= 0 && a.pos.x <= width_size  ||
            a.pos.x = 0 && a.pos.y >= 0 && a.pos.y <= height_size ||
            a.pos.y = height_size - rect_size && a.pos.x >= 0 && a.pos.x <= width_size ||
            a.pos.x = width_size  - rect_size && a.pos.y >= 0 && a.pos.y <= height_size
        ) && a.state = Empty   
    ) cell_list
;;

(**
    @role:
        Generates a defined number (nb_movable_cell_by_time) of Movable 
        cells on one side of the window, chosen at random.

        Numbering of the possible choices for one side of the window
                         
                                         0
                                    +---------+
                                    |         |
                                  3 |         | 1
                                    |         |
                                    +---------+
                                         2
 *)
let generation_movable_cell cell_list =  
    let new_empty_side_cell_list = empty_cells_positions_on_windows_side cell_list in
    
    let rec applies cell_l n i empty_cell_list =
        match (empty_cell_list, i) with 
        | (_, a) when a = n -> cell_l
        | ([], _) ->                                  (* if the list of possible cells to generate Movable cells is empty then ... *)
            begin
                if count_occu_movable cell_l > 0 then (* if there are still Movable cells then we can still apply the aggregation rule *)
                    time_plus_one cell_l 
                else
                    raise End    
            end
        | (l, _)  ->
            begin   
                let random_pos_empty_cel = nth l (Random.int (length l)) in                                         (* choose a position at random in the possible cell list *)
                let new_movable_cel      = {pos = random_pos_empty_cel.pos; state = Movable} in                     (* new cell with coord of the neighborhood and state become Movable *)

                fill_one_cell new_movable_cel;                                                                      (* color in the new Movable cell *)

                let new_cell_list       = [new_movable_cel]@(filter (fun x -> x <> random_pos_empty_cel) cell_l) in (* remove the old cell (Empty) and replace it with another (Movable) *)          
                let new_empty_cell_list = filter (fun x -> x <> random_pos_empty_cel) empty_cell_list in            (* remove the old cell (Empty) from the list of potential cells for the new movable cell *)
                applies new_cell_list n (i+1) new_empty_cell_list
            end       
    in applies cell_list nb_movable_cell_by_time 0 new_empty_side_cell_list
;;


(* ------------------------- main ------------------------- *)


(** 
    @role:
       Initialization of the model with Movable cells and one Fixed cell.
 *)
let init cell_list =
    let middle_cell = {pos = {x = ((width_size / rect_size) / 2) * rect_size; y = ((height_size / rect_size) / 2) * rect_size}; state = Fixed} in (* the 1st cell fixed is in the middle *)
    generation_movable_cell ([middle_cell]@(filter (fun x -> x.pos <> middle_cell.pos) cell_list)) (* suppresion de la cell du milieu (Empty) et ajout dans la liste, de la nouvelle cell Fixed *)
;;

(**
    @role:
        finish the model.
 *)
let f_end () = 
   close_graph();
   print_string "Aucune regle ne peut encore être appliqué : FIN du modele de calcul"; print_newline ();
   print_string "Good bye..."; print_newline()
;; 

(**
    @role:
        processes the action to be done according to the type key on the keyboard.
 *)
let check_key key cell_list =
    match key with
    | 'a' -> time_plus_one cell_list
    | _   -> raise End
;;


let main () =
    open_graph (Printf.sprintf " %ix%i" width_size height_size); (* required space before% i *)
   
    Random.self_init ();                                         (* allows to change the "random" part of the model each time it is launched *)
    
    let cell_list_empty = grid ()              in                (* creation of the grid and the list of cells *)
    let start_modele    = init cell_list_empty in                (* initialization of the states at t = 0 of the model (initial state of the model) *)
     
    fill_all_cells start_modele;                                 (* color the cells at time t = 0 (initial state of the model) *)
    
    let rec aux cell_list =
        if ((count_occu_movable cell_list) < nb_movable_cell_by_time) then (* we always add a finite number of Movable cells (nb_movable_cell_by_time), if the model does not include enough *)
            begin
                try
                    aux (generation_movable_cell cell_list)   
                with
                    End -> raise End      
            end
        else
            begin         
                let event = wait_next_event [Key_pressed] in

                try
                    while true do
                        try 
                            if event.Graphics.keypressed then                                                         
                                let new_list = check_key event.Graphics.key cell_list in
                                aux new_list
                        with 
                            End -> raise End 
                    done
                with
                    End -> f_end () 
            end 

    in aux start_modele
;;


(* ------------------------- execution ------------------------- *)


main ();;
f_end ();;


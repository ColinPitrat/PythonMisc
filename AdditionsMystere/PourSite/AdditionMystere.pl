#!/usr/bin/gprolog --consult-file
/* 
   Pour lancer le programme on peut l'utiliser directement en tant qu'executable grace au shebang.
   On peut aussi, ce qui revient au même, appeler explicitement gprolog: 
   gprolog --consult-file AdditionMystere.pl

   Une autre façon de lancer le programme, qui permet d'avoir une sortie moins polluée, est:
   gprolog --init-goal "consult('AdditionMystere.pl')"
   Cependant, les informations de compilation sont toujours présentes.

   Pour n'obtenir vraiment que la sortie du programme lui même, la seule solution est de le compiler:
   gplc AdditionMystere.pl
   Et de lancer l'executable AdditionMystere qui en resulte.

*/
:- initialization(main).

main:-
    findall(_, smm, _),
    halt.

smm:-
    X = [S,E,N,D,M,O,R,Y],
    Digits = [0,1,2,3,4,5,6,7,8,9],
    assign_digits(X, Digits),
    M > 0, 
    S > 0,
    1000*S + 100*E + 10*N + D +
    1000*M + 100*O + 10*R + E =:=
    10000*M + 1000*O + 100*N + 10*E + Y,
    write('[S,E,N,D,M,O,R,Y] = '),
    write(X), 
    nl.

    selectDigit(X, [X|R], R).
    selectDigit(X, [Y|Xs], [Y|Ys]):- selectDigit(X, Xs, Ys).

    assign_digits([], _List).
    assign_digits([D|Ds], List):-
        selectDigit(D, List, NewList),
        assign_digits(Ds, NewList).

:- dynamic known/3.

telldisease(malaria).

telldisease(malaria,sweating,sweating,sweating,sweating).

telldisease(fever,X,sweating,sweating,sweating).

telldisease(fever,X,sweating,sweating,sweating).

%RULES

telldisease(malaria,'I am currently experiencing COVID symptoms, I want to know what to do',res,turk).


%rules for I HAVE SYMPTOMS

answer('You need to test at City Test SF','I am currently experiencing COVID symptoms, I want to know what to do',res,turk).


% Enter your KB below this line:

# % rule 1
problem(battery) :- engine(turning_over), battery(bad).

% rule 2.
battery(bad) :- lights(weak).

% rule 3
battery(bad) :- radio(weak).

% rule 4
problem(engine_flooded) :- smell(gas), engine(turning_over). % rule 4

% rule 5
problem(out_of_gas):- engine(turning_over), gas_gauge(empty).

lights(X):- ask(lights,X).
engine(X) :- ask(engine, X).
smell(X) :- ask(smell, X).
radio(X) :- ask(radio, X).
gas_gauge(X) :- ask(gas_gauge, X).

% Asking clauses
multivalued(none). % We don't have any multivalued attributes

ask(A, V):-
known(yes, A, V), % succeed if true

!.	% stop looking

ask(A, V):-
known(_, A, V), % fail if false
!, fail.

% If not multivalued, and already known, don't ask again for a different value.
ask(A, V):-
\+multivalued(A),
known(yes, A, V2),
V \== V2,
!.

ask(A, V):-
read_py(A,V,Y), % get the answer
asserta(known(Y, A, V)), % remember it
write_py(known(Y, A, V)),
Y == yes.	% succeed or fail
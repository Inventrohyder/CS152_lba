KB = """
%  Tell prolog that known/3 will be added later by asserta
:- dynamic known/3.

% Enter your KB below this line:

problem(battery) :- \+engine(turning_over), battery(bad).
problem(notbattery) :- \+engine(turning_over), battery(bad).
battery(bad) :- lights(weak).
battery(bad) :- radio(weak).
problem(out_of_gas) :- engine(turning_over), gas_gauge(empty).
problem(engine_flooded) :- engine(turning_over), smell(gas).

% The code below implements the prompting to ask the user:

gas_gauge(X) :- ask(gas_gauge, X).
engine(X) :- ask(engine, X).
lights(X) :- ask(lights, X).
radio(X) :- ask(radio, X).
smell(X) :- ask(smell, X).


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
Y == yes.	% succeed or fail

ask(A, V)

"""
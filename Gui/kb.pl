%%KB

              
%RULES


%rules for I HAVE SYMPTOMS

answer('You need to contact Geo Blue') :- intention('I am currently experiencing COVID symptoms, I want to know what to do'), \+reside(res), insured('GeoBlue').
answer('You need to contact your local provider') :- intention('I am currently experiencing COVID symptoms, I want to know what to do'), \+reside(res), \+insured('GeoBlue').


answer('You need to test at City Test SF') :- intention('I am currently experiencing COVID symptoms, I want to know what to do'), reside(res), res_hall(turk).
answer('You need to test at chinatown') :- intention('I am currently experiencing COVID symptoms, I want to know what to do'), reside(res), res_hall('851').



%rules for I HAVE TRAVELLED/ WILL BE TRAVELLING

answer('Visit the City Test SF test centera') :-
    intention('I want to travel around'), result(urgent), res_hall(turk).
answer('Visit the glide test center') :-
    intention('I want to travel around'), result(urgent), res_hall(turk).
answer('Visit the chinatown test center') :- 
    intention('I want to travel around'), result(urgent), res_hall('851').
answer('Test privately') :-
    intention('I want to travel around'), \+result(urgent), testing(at_home).
answer('Visit the glide test center') :- 
    intention('I want to travel around'), \+result(urgent), testing(at_testing_center), reside(res), res_hall(turk).
answer('Visit the carbon health market test center') :- 
    intention('I want to travel around'), \+result(urgent), testing(at_testing_center), reside(res), res_hall(turk).
answer('Visit the carbon health market test center') :- 
    intention('I want to travel around'), \+result(urgent), testing(at_testing_center), reside(res), res_hall('851').
answer('Visit the carbon health market test center'):- 
    intention('I want to travel around'), \+result(urgent), testing(at_testing_center), reside(res), res_hall('851').



%rules for HAVE A CLOSE CONTACT WITH COVID

answer('You should start quarantine immediately'):- 
    intention('I had a close contact with a COVID patient. What next?'), exposure(known), \+quarantine_status(qurantine).
answer('You should continue your quarantine'):- 
    intention('I had a close contact with a COVID patient. What next?'), exposure(known), quarantine_status(quarantine).

answer('Visit City Test SF'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), \+symptoms(felt).
answer('Visit the local provider'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), symptoms(felt),  \+reside(res), \+insured('GeoBlue').
answer('Visit Geo Blue'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), symptoms(felt), \+reside(res),\+insured('GeoBlue'). 
answer('Visit City Test SF'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), symptoms(felt), reside(res), res_hall(turk).
answer('Visit chinatown center'):- 
    intention('I had a close contact with a COVID patient. What next?'), \+exposure(known), symptoms(felt), reside(res), res_hall('851').


% rules for A CASUAL CHECK
%The 4 lines below I am not sure, as there are two options glide and carbon for given askables
answer('Visit the glide test center') :-
    intention('I just wanted to know about some casual stuff'), testing(at_testing_center), res_hall(turk).
answer('Visit the carbon health market test center') :-
    intention('I just wanted to know about some casual stuff'), testing(at_testing_center), res_hall(turk).
answer('Visit the Concentera Downtown Center') :- 
    intention('I just wanted to know about some casual stuff'), testing(at_testing_center), res_hall('851').
answer('Visit the carbon health fin test center') :- 
    intention('I just wanted to know about some casual stuff'), testing(at_testing_center), res_hall('851').
answer('Test privately') :- 
    intention('I just wanted to know about some casual stuff'), testing(at_home).



%FACTS 
reside(X) :- 
    ask('Do you live in the', X).

res_hall(X) :- 
    menuask('Which res hall do you reside in?', X, [turk, '851']).

testing(X) :-
    menuask('Where do you want to test?', X, [at_home, at_testing_center]).



exposure(X) :- 
    ask('Is your source of exposure', X).

result(X) :- ask('Is your need for testing', X).

insured(X) :- ask('Are you insured by', X).


intention(X) :- 
    menuask('What is your intention for taking the COVID test?', X, ['I am currently experiencing COVID symptoms, I want to know what to do', 'I want to travel around', 'I had a close contact with a COVID patient. What next?', 'I just wanted to know about some casual stuff']).


quarantine_status(X) :-
    ask('Are you currently in', X).


symptoms(X) :-
    ask('Are your symptoms', X).


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
user_response(Y),
Y == yes.	% succeed or fail


menuask(A, V, _):-
known(yes, A, V), % succeed if true
!.	% stop looking

menuask(A, V, _):-
known(yes, A, V2), % If already known, don't ask again for a different value.
V \== V2,
!,
fail.

menuask(A, V, MenuList) :-
 read_py_menu(A, X, MenuList),
 check_val(X, A, V, MenuList),
 asserta( known(yes, A, X) ),
 X == V.
check_val(X, _, _, MenuList) :-
 member(X, MenuList),
 !.
check_val(X, A, V, MenuList) :-
 system_response(X), system_response(' is not a legal value, try again.\n'),
 menuask(A, V, MenuList). 
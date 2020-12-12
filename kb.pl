telldisease(malaria).

telldisease(malaria,sweating,sweating,sweating,sweating).

telldisease(fever,X,sweating,sweating,sweating).

telldisease(fever,X,sweating,sweating,sweating).

%RULES


telldisease(malaria,'I am currently experiencing COVID symptoms, I want to know what to do',res,turk).


%rules for I HAVE SYMPTOMS

answer('You need to test at City Test SF','I am currently experiencing COVID symptoms, I want to know what to do',res,turk).



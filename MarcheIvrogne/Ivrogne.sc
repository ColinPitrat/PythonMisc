S=input("nombre de simulations: ");
B=0;
for i=1:S
  D=0;
  for j=1:20
    P=floor(2*rand());
    if (P==0) then D=D+1;
    end;
  end;
  if (D==10) then B=B+1;
  end;
end;
disp('fr�quence: ')
disp(B/S)


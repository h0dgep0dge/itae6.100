PROGRAM program0
  VAR
    Traffic_A : BOOL;
    Traffic_B : BOOL;
    AtoB_Amber : BOOL;
    BtoA_Amber : BOOL;
    A_Crossing_A_Amber : BOOL;
    A_Crossing_B_Amber : BOOL;
    B_Crossing_A_Amber : BOOL;
    B_Crossing_B_Amber : BOOL;
    A_Crossing_A : BOOL;
    A_Crossing_B : BOOL;
    B_Crossing_A : BOOL;
    B_Crossing_B : BOOL;
  END_VAR
  VAR
    Change AT %IX0.2 : BOOL;
    Cross_A AT %IX0.1 : BOOL;
    Cross_B AT %IX0.0 : BOOL;
  END_VAR
  VAR
    Amber_Dwell : TIME := T#2s;
    Crossing_Dwell : TIME := T#3s;
    Traffic_B_Wait : TIME := T#5s;
    TON0 : TON;
    TON1 : TON;
    TON2 : TON;
    TON3 : TON;
    TON4 : TON;
    TON5 : TON;
    TON6 : TON;
    TON7 : TON;
    TON8 : TON;
  END_VAR
  VAR
    Red_B AT %QX0.0 : BOOL;
    Amber_B AT %QX0.1 : BOOL;
    Green_B AT %QX0.2 : BOOL;
    Stop_B AT %QX0.3 : BOOL;
    Red_A AT %QX0.4 : BOOL;
    Amber_A AT %QX0.5 : BOOL;
    Green_A AT %QX0.6 : BOOL;
    Stop_A AT %QX0.7 : BOOL;
  END_VAR
  VAR
    R_TRIG1 : R_TRIG;
    R_TRIG2 : R_TRIG;
    R_TRIG3 : R_TRIG;
    R_TRIG4 : R_TRIG;
    R_TRIG5 : R_TRIG;
  END_VAR

  TON1(IN := BtoA_Amber, PT := Amber_Dwell);
  TON0(IN := A_Crossing_A OR A_Crossing_B, PT := Crossing_Dwell);
  Traffic_A := TON0.Q OR TON1.Q OR NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND (NOT(Traffic_A) OR Traffic_A);
  TON2(IN := B_Crossing_A OR B_Crossing_B, PT := Crossing_Dwell);
  TON3(IN := AtoB_Amber, PT := Amber_Dwell);
  Traffic_B := TON2.Q OR TON3.Q OR NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND Traffic_B AND NOT(Traffic_A);
  R_TRIG1(CLK := Change);
  AtoB_Amber := NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND AtoB_Amber AND NOT(Traffic_B) AND NOT(Traffic_A) OR R_TRIG1.Q AND Traffic_A;
  TON4(IN := Traffic_B, PT := Traffic_B_Wait);
  BtoA_Amber := TON4.Q OR NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND BtoA_Amber AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND NOT(Traffic_A);
  R_TRIG2(CLK := Cross_A);
  A_Crossing_A_Amber := NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND A_Crossing_A_Amber AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND NOT(Traffic_A) OR R_TRIG2.Q AND Traffic_A;
  R_TRIG3(CLK := Cross_B);
  A_Crossing_B_Amber := NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND A_Crossing_B_Amber AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND NOT(Traffic_A) OR R_TRIG3.Q AND Traffic_A;
  R_TRIG4(CLK := Cross_A);
  B_Crossing_A_Amber := NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND B_Crossing_A_Amber AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND NOT(Traffic_A) OR R_TRIG4.Q AND Traffic_B;
  R_TRIG5(CLK := Cross_B);
  B_Crossing_B_Amber := NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND B_Crossing_B_Amber AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND NOT(Traffic_A) OR R_TRIG5.Q AND Traffic_B;
  TON5(IN := A_Crossing_A_Amber, PT := Amber_Dwell);
  A_Crossing_A := TON5.Q OR NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND A_Crossing_A AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND NOT(Traffic_A);
  TON7(IN := A_Crossing_B_Amber, PT := Amber_Dwell);
  A_Crossing_B := TON7.Q OR NOT(B_Crossing_B) AND NOT(B_Crossing_A) AND A_Crossing_B AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND NOT(Traffic_A);
  TON8(IN := B_Crossing_A_Amber, PT := Amber_Dwell);
  B_Crossing_A := TON8.Q OR NOT(B_Crossing_B) AND B_Crossing_A AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND NOT(Traffic_A);
  TON6(IN := B_Crossing_B_Amber, PT := Amber_Dwell);
  B_Crossing_B := TON6.Q OR B_Crossing_B AND NOT(B_Crossing_A) AND NOT(A_Crossing_B) AND NOT(A_Crossing_A) AND NOT(B_Crossing_B_Amber) AND NOT(B_Crossing_A_Amber) AND NOT(A_Crossing_B_Amber) AND NOT(A_Crossing_A_Amber) AND NOT(BtoA_Amber) AND NOT(AtoB_Amber) AND NOT(Traffic_B) AND NOT(Traffic_A);
  Green_A := Traffic_A;
  Amber_A := A_Crossing_A_Amber OR A_Crossing_B_Amber OR AtoB_Amber;
  Red_A := NOT(Amber_A) AND NOT(Green_A);
  Green_B := Traffic_B;
  Amber_B := B_Crossing_A_Amber OR B_Crossing_B_Amber OR BtoA_Amber;
  Red_B := NOT(Amber_B) AND NOT(Green_B);
  Stop_A := NOT(A_Crossing_A OR B_Crossing_A);
  Stop_B := NOT(A_Crossing_B OR B_Crossing_B);
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#50ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION

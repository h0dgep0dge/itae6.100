void LOGGER_init__(LOGGER *data__, BOOL retain) {
  __INIT_VAR(data__->EN,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->ENO,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->TRIG,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->MSG,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->LEVEL,LOGLEVEL__INFO,retain)
  __INIT_VAR(data__->TRIG0,__BOOL_LITERAL(FALSE),retain)
}

// Code part
void LOGGER_body__(LOGGER *data__) {
  // Control execution
  if (!__GET_VAR(data__->EN)) {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(FALSE));
    return;
  }
  else {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(TRUE));
  }
  // Initialise TEMP variables

  if ((__GET_VAR(data__->TRIG,) && !(__GET_VAR(data__->TRIG0,)))) {
    #define GetFbVar(var,...) __GET_VAR(data__->var,__VA_ARGS__)
    #define SetFbVar(var,val,...) __SET_VAR(data__->,var,__VA_ARGS__,val)

   LogMessage(GetFbVar(LEVEL),(char*)GetFbVar(MSG, .body),GetFbVar(MSG, .len));
  
    #undef GetFbVar
    #undef SetFbVar
;
  };
  __SET_VAR(data__->,TRIG0,,__GET_VAR(data__->TRIG,));

  goto __end;

__end:
  return;
} // LOGGER_body__() 





void PROGRAM0_init__(PROGRAM0 *data__, BOOL retain) {
  __INIT_VAR(data__->TRAFFIC_A,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->TRAFFIC_B,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->ATOB_AMBER,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->BTOA_AMBER,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->A_CROSSING_A_AMBER,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->A_CROSSING_B_AMBER,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->B_CROSSING_A_AMBER,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->B_CROSSING_B_AMBER,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->A_CROSSING_A,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->A_CROSSING_B,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->B_CROSSING_A,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->B_CROSSING_B,__BOOL_LITERAL(FALSE),retain)
  __INIT_LOCATED(BOOL,__IX0_2,data__->CHANGE,retain)
  __INIT_LOCATED_VALUE(data__->CHANGE,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__IX0_1,data__->CROSS_A,retain)
  __INIT_LOCATED_VALUE(data__->CROSS_A,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__IX0_0,data__->CROSS_B,retain)
  __INIT_LOCATED_VALUE(data__->CROSS_B,__BOOL_LITERAL(FALSE))
  __INIT_VAR(data__->AMBER_DWELL,__time_to_timespec(1, 0, 2, 0, 0, 0),retain)
  __INIT_VAR(data__->CROSSING_DWELL,__time_to_timespec(1, 0, 3, 0, 0, 0),retain)
  __INIT_VAR(data__->TRAFFIC_B_WAIT,__time_to_timespec(1, 0, 5, 0, 0, 0),retain)
  TON_init__(&data__->TON0,retain);
  TON_init__(&data__->TON1,retain);
  TON_init__(&data__->TON2,retain);
  TON_init__(&data__->TON3,retain);
  TON_init__(&data__->TON4,retain);
  TON_init__(&data__->TON5,retain);
  TON_init__(&data__->TON6,retain);
  TON_init__(&data__->TON7,retain);
  TON_init__(&data__->TON8,retain);
  __INIT_LOCATED(BOOL,__QX0_0,data__->RED_B,retain)
  __INIT_LOCATED_VALUE(data__->RED_B,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_1,data__->AMBER_B,retain)
  __INIT_LOCATED_VALUE(data__->AMBER_B,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_2,data__->GREEN_B,retain)
  __INIT_LOCATED_VALUE(data__->GREEN_B,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_3,data__->STOP_B,retain)
  __INIT_LOCATED_VALUE(data__->STOP_B,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_4,data__->RED_A,retain)
  __INIT_LOCATED_VALUE(data__->RED_A,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_5,data__->AMBER_A,retain)
  __INIT_LOCATED_VALUE(data__->AMBER_A,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_6,data__->GREEN_A,retain)
  __INIT_LOCATED_VALUE(data__->GREEN_A,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_7,data__->STOP_A,retain)
  __INIT_LOCATED_VALUE(data__->STOP_A,__BOOL_LITERAL(FALSE))
  R_TRIG_init__(&data__->R_TRIG1,retain);
  R_TRIG_init__(&data__->R_TRIG2,retain);
  R_TRIG_init__(&data__->R_TRIG3,retain);
  R_TRIG_init__(&data__->R_TRIG4,retain);
  R_TRIG_init__(&data__->R_TRIG5,retain);
}

// Code part
void PROGRAM0_body__(PROGRAM0 *data__) {
  // Initialise TEMP variables

  __SET_VAR(data__->TON1.,IN,,__GET_VAR(data__->BTOA_AMBER,));
  __SET_VAR(data__->TON1.,PT,,__GET_VAR(data__->AMBER_DWELL,));
  TON_body__(&data__->TON1);
  __SET_VAR(data__->TON0.,IN,,(__GET_VAR(data__->A_CROSSING_A,) || __GET_VAR(data__->A_CROSSING_B,)));
  __SET_VAR(data__->TON0.,PT,,__GET_VAR(data__->CROSSING_DWELL,));
  TON_body__(&data__->TON0);
  __SET_VAR(data__->,TRAFFIC_A,,((__GET_VAR(data__->TON0.Q,) || __GET_VAR(data__->TON1.Q,)) || (((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && (!(__GET_VAR(data__->TRAFFIC_A,)) || __GET_VAR(data__->TRAFFIC_A,)))));
  __SET_VAR(data__->TON2.,IN,,(__GET_VAR(data__->B_CROSSING_A,) || __GET_VAR(data__->B_CROSSING_B,)));
  __SET_VAR(data__->TON2.,PT,,__GET_VAR(data__->CROSSING_DWELL,));
  TON_body__(&data__->TON2);
  __SET_VAR(data__->TON3.,IN,,__GET_VAR(data__->ATOB_AMBER,));
  __SET_VAR(data__->TON3.,PT,,__GET_VAR(data__->AMBER_DWELL,));
  TON_body__(&data__->TON3);
  __SET_VAR(data__->,TRAFFIC_B,,((__GET_VAR(data__->TON2.Q,) || __GET_VAR(data__->TON3.Q,)) || (((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && __GET_VAR(data__->TRAFFIC_B,)) && !(__GET_VAR(data__->TRAFFIC_A,)))));
  __SET_VAR(data__->R_TRIG1.,CLK,,__GET_LOCATED(data__->CHANGE,));
  R_TRIG_body__(&data__->R_TRIG1);
  __SET_VAR(data__->,ATOB_AMBER,,((((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && __GET_VAR(data__->ATOB_AMBER,)) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,))) || (__GET_VAR(data__->R_TRIG1.Q,) && __GET_VAR(data__->TRAFFIC_A,))));
  __SET_VAR(data__->TON4.,IN,,__GET_VAR(data__->TRAFFIC_B,));
  __SET_VAR(data__->TON4.,PT,,__GET_VAR(data__->TRAFFIC_B_WAIT,));
  TON_body__(&data__->TON4);
  __SET_VAR(data__->,BTOA_AMBER,,(__GET_VAR(data__->TON4.Q,) || (((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && __GET_VAR(data__->BTOA_AMBER,)) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,)))));
  __SET_VAR(data__->R_TRIG2.,CLK,,__GET_LOCATED(data__->CROSS_A,));
  R_TRIG_body__(&data__->R_TRIG2);
  __SET_VAR(data__->,A_CROSSING_A_AMBER,,((((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && __GET_VAR(data__->A_CROSSING_A_AMBER,)) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,))) || (__GET_VAR(data__->R_TRIG2.Q,) && __GET_VAR(data__->TRAFFIC_A,))));
  __SET_VAR(data__->R_TRIG3.,CLK,,__GET_LOCATED(data__->CROSS_B,));
  R_TRIG_body__(&data__->R_TRIG3);
  __SET_VAR(data__->,A_CROSSING_B_AMBER,,((((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && __GET_VAR(data__->A_CROSSING_B_AMBER,)) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,))) || (__GET_VAR(data__->R_TRIG3.Q,) && __GET_VAR(data__->TRAFFIC_A,))));
  __SET_VAR(data__->R_TRIG4.,CLK,,__GET_LOCATED(data__->CROSS_A,));
  R_TRIG_body__(&data__->R_TRIG4);
  __SET_VAR(data__->,B_CROSSING_A_AMBER,,((((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && __GET_VAR(data__->B_CROSSING_A_AMBER,)) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,))) || (__GET_VAR(data__->R_TRIG4.Q,) && __GET_VAR(data__->TRAFFIC_B,))));
  __SET_VAR(data__->R_TRIG5.,CLK,,__GET_LOCATED(data__->CROSS_B,));
  R_TRIG_body__(&data__->R_TRIG5);
  __SET_VAR(data__->,B_CROSSING_B_AMBER,,((((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && __GET_VAR(data__->B_CROSSING_B_AMBER,)) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,))) || (__GET_VAR(data__->R_TRIG5.Q,) && __GET_VAR(data__->TRAFFIC_B,))));
  __SET_VAR(data__->TON5.,IN,,__GET_VAR(data__->A_CROSSING_A_AMBER,));
  __SET_VAR(data__->TON5.,PT,,__GET_VAR(data__->AMBER_DWELL,));
  TON_body__(&data__->TON5);
  __SET_VAR(data__->,A_CROSSING_A,,(__GET_VAR(data__->TON5.Q,) || (((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && __GET_VAR(data__->A_CROSSING_A,)) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,)))));
  __SET_VAR(data__->TON7.,IN,,__GET_VAR(data__->A_CROSSING_B_AMBER,));
  __SET_VAR(data__->TON7.,PT,,__GET_VAR(data__->AMBER_DWELL,));
  TON_body__(&data__->TON7);
  __SET_VAR(data__->,A_CROSSING_B,,(__GET_VAR(data__->TON7.Q,) || (((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && !(__GET_VAR(data__->B_CROSSING_A,))) && __GET_VAR(data__->A_CROSSING_B,)) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,)))));
  __SET_VAR(data__->TON8.,IN,,__GET_VAR(data__->B_CROSSING_A_AMBER,));
  __SET_VAR(data__->TON8.,PT,,__GET_VAR(data__->AMBER_DWELL,));
  TON_body__(&data__->TON8);
  __SET_VAR(data__->,B_CROSSING_A,,(__GET_VAR(data__->TON8.Q,) || (((((((((((!(__GET_VAR(data__->B_CROSSING_B,)) && __GET_VAR(data__->B_CROSSING_A,)) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,)))));
  __SET_VAR(data__->TON6.,IN,,__GET_VAR(data__->B_CROSSING_B_AMBER,));
  __SET_VAR(data__->TON6.,PT,,__GET_VAR(data__->AMBER_DWELL,));
  TON_body__(&data__->TON6);
  __SET_VAR(data__->,B_CROSSING_B,,(__GET_VAR(data__->TON6.Q,) || (((((((((((__GET_VAR(data__->B_CROSSING_B,) && !(__GET_VAR(data__->B_CROSSING_A,))) && !(__GET_VAR(data__->A_CROSSING_B,))) && !(__GET_VAR(data__->A_CROSSING_A,))) && !(__GET_VAR(data__->B_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->B_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_B_AMBER,))) && !(__GET_VAR(data__->A_CROSSING_A_AMBER,))) && !(__GET_VAR(data__->BTOA_AMBER,))) && !(__GET_VAR(data__->ATOB_AMBER,))) && !(__GET_VAR(data__->TRAFFIC_B,))) && !(__GET_VAR(data__->TRAFFIC_A,)))));
  __SET_LOCATED(data__->,GREEN_A,,__GET_VAR(data__->TRAFFIC_A,));
  __SET_LOCATED(data__->,AMBER_A,,((__GET_VAR(data__->A_CROSSING_A_AMBER,) || __GET_VAR(data__->A_CROSSING_B_AMBER,)) || __GET_VAR(data__->ATOB_AMBER,)));
  __SET_LOCATED(data__->,RED_A,,(!(__GET_LOCATED(data__->AMBER_A,)) && !(__GET_LOCATED(data__->GREEN_A,))));
  __SET_LOCATED(data__->,GREEN_B,,__GET_VAR(data__->TRAFFIC_B,));
  __SET_LOCATED(data__->,AMBER_B,,((__GET_VAR(data__->B_CROSSING_A_AMBER,) || __GET_VAR(data__->B_CROSSING_B_AMBER,)) || __GET_VAR(data__->BTOA_AMBER,)));
  __SET_LOCATED(data__->,RED_B,,(!(__GET_LOCATED(data__->AMBER_B,)) && !(__GET_LOCATED(data__->GREEN_B,))));
  __SET_LOCATED(data__->,STOP_A,,!((__GET_VAR(data__->A_CROSSING_A,) || __GET_VAR(data__->B_CROSSING_A,))));
  __SET_LOCATED(data__->,STOP_B,,!((__GET_VAR(data__->A_CROSSING_B,) || __GET_VAR(data__->B_CROSSING_B,))));

  goto __end;

__end:
  return;
} // PROGRAM0_body__() 






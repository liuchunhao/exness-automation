



// socket=SocketCreate();



//+------------------------------------------------------------------+

//| Expert initialization function                                   |

//+------------------------------------------------------------------+



int socket = SocketCreate();

int OnInit(){

   

   if(socket!=INVALID_HANDLE) {

      if(SocketConnect(socket,"127.0.0.1",9999,1000)) {

         Print("Connected to "," localhost",":",9999);

      } else {

         Print("Connection ","localhost",":",9999," error ", GetLastError());

      }

   }

   return(INIT_SUCCEEDED);

}

//+------------------------------------------------------------------+

//| Expert deinitialization function                                 |

//+------------------------------------------------------------------+

void OnDeinit(const int reason)

  {

   // 

   // socket.Disconnect();

  }

//+------------------------------------------------------------------+

//| Expert tick function                                             |

//+------------------------------------------------------------------+

void OnTick() {

   MqlTick last_tick;

   string request;

   string symbol = "BTCUSD";

   string newline = "\n" ;

   

 /*  

   if(SymbolInfoTick(symbol, last_tick)) {

      Print(last_tick.time,": Bid = ",last_tick.bid, " Ask = ",last_tick.ask," Volume = ",last_tick.volume);

      // request = TimeToString(last_tick.time) + ": Bid = " + DoubleToString(last_tick.bid) + " Ask = " + DoubleToString(last_tick.ask) + " Volume = " + IntegerToString(last_tick.volume);

   }

 */

   

   // Not running in Strategy Tester



   // int socket = SocketCreate();

   if(socket!=INVALID_HANDLE) {

      // if(SocketConnect(socket,"127.0.0.1", 9999,1000)) {   // error 4104

         // Print("Connected to "," localhost",":",9999);

         

         // MqlTick last_tick;

         if(SymbolInfoTick(symbol, last_tick)) {

            Print(last_tick.time,": Bid = ",last_tick.bid, " Ask = ",last_tick.ask," Volume = ",last_tick.volume);

            string request = TimeToString(last_tick.time) + ": Bid = " + DoubleToString(last_tick.bid) + " Ask = " + DoubleToString(last_tick.ask) + " Volume = " + IntegerToString(last_tick.volume) + newline;

            char req [];

            int  len = StringToCharArray(request, req)-1;

            SocketSend(socket, req, len);

         } else {

            Print("SymbolInfoTick () failed, error = ", GetLastError());

         }

         

      // } else { 

         // Print("Connection ","localhost",":", 9999," error ", GetLastError());

         

      // } 

      // SocketClose(socket);

   }

   

 

}


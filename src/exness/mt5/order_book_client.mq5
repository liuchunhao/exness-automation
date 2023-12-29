


socket=SocketCreate();

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit(){
   

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
 socket=SocketCreate();
 if(socket!=INVALID_HANDLE) {
  if(SocketConnect(socket,"localhost",9999,1000)) {
   Print("Connected to "," localhost",":",9999);
         

         
   string tosend;
   for(int i=0;i<ArraySize(clpr);i++) tosend+=(string)clpr[i]+" ";       
   string received = socksend(socket, tosend) ? socketreceive(socket, 10) : ""; 
   drawlr(recieved); 
   
  } else { 
    Print("Connection ","localhost",":",9090," error ",GetLastError());
    SocketClose(socket); 
  } else {
      Print("Socket creation error ",GetLastError()); 
  }

// Connect to the server
if (SocketConnect(hSocket,IP_ADDRESS,PORT_NUMBER,1000))
   Print("Connected to the server");
else
   Print("Connection error ",GetLastError());

// Send data to the server
if (SocketSend(hSocket,"Hello server!",13,1000))
   Print("Data has been sent");
else
   Print("Sending error ",GetLastError());

// Receive data from the server
char buffer[256];
uint received;
if (SocketReceive(hSocket,buffer,256,received,1000))
   Print("Data has been received: ",buffer);
else
   Print("Receiving error ",GetLastError());

// Disconnect from the server
if (SocketClose(hSocket))
   Print("Socket has been closed");
else
   Print("Closing error ",GetLastError());

//+------------------------------------------------------------------+

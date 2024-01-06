//+------------------------------------------------------------------+
//|                                                      onTrade.mq5 |
//|                                  Copyright 2023, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2023, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"


//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+



string SOCKET_ADDRESS = "127.0.0.1";
int SOCKET_PORT = 19999;

string SYMBOL = "BTCUSD";
string URL = "http://127.0.0.1:5000/notification/trade";

int socket = SocketCreate();

int OnInit()
{

      if(socket != INVALID_HANDLE) {
         if(SocketConnect(socket, SOCKET_ADDRESS, SOCKET_PORT, 1000)) {
            PrintFormat("Connected to [%s:%d]", SOCKET_ADDRESS, SOCKET_PORT);
            return(INIT_SUCCEEDED);
         } else {
            Print("Connection ", SOCKET_ADDRESS,":", SOCKET_PORT," error ", GetLastError());
         }
      }
      Print("Failed to create a socket, error ", GetLastError());
      return(INIT_FAILED);

}


//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   SocketClose(socket);
}


//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
string NEW_LINE = "\r\n";
void OnTick()
{

   MqlTick last_tick;
   string request;
  
   if(socket!=INVALID_HANDLE) {

       if(SymbolInfoTick(SYMBOL, last_tick)) {
            // string time = TimeToString(last_tick.time); 
            MqlDateTime dt_struct;
            datetime current_time = TimeCurrent(dt_struct); 
            string time = StringFormat("%04d-%02d-%02d %02d:%02d:%02d", dt_struct.year, dt_struct.mon, dt_struct.day, dt_struct.hour, dt_struct.min, dt_struct.sec);
                    
            double bid = last_tick.bid;
            double ask = last_tick.ask;
            ulong volume = last_tick.volume;
            
            string data = StringFormat("{ \"time\": \"%s\", \"symbol\": \"%s\", \"bid\": %.2f, \"ask\": %.2f, \"volume\": %d }", time, SYMBOL, bid, ask, volume);
            PrintFormat("onTick(): %s, %s", SYMBOL, data);
            
            request = StringFormat("%s%s", data, NEW_LINE);
            char req [];
            int len = StringToCharArray(request, req)-1;

            if(SocketSend(socket, req, len) == len) {
               PrintFormat("Success sending: [%s]", data);
            } else {
               PrintFormat("Failed sending: [%s]", data);
               OnInit();                                       // reconnect !!
            };

       } else {
            Print("SymbolInfoTick () failed, error = ", GetLastError());
       }
   }
}


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool SendPost(string jsonStr)
{

   /*
      https://www.mql5.com/en/docs/network/webrequest

      To enable access to the server, you should add URL "https://finance.yahoo.com"
      to the list of allowed URLs (Main Menu->Tools->Options, tab "Expert Advisors"):
      Resetting the last error code
      
   */
   
   // string url = "http://127.0.0.1:5000/notification/trade";
   string method = "POST";
   string headers = "Content-Type: application/json";
   int timeout = 5000;
   char data[];
   StringToCharArray(jsonStr, data, 0, StringLen(jsonStr));  // when converting the data string to POST data object the length was not WHOLE_ARRAY, but StringLen.
   char result [];
   string result_headers;

   ResetLastError();

   PrintFormat("SendPost: request: %s", jsonStr);
   int res = WebRequest(
                method,
                URL,
                headers,
                timeout,
                data,
                result,
                result_headers
             );

   if(res == -1) {
      Print("SendPost: WebRequest failed with error ", GetLastError());
   } else {
      if(res == 200) {
         PrintFormat("SendPost: The request has been successfully sent, result: [%s] ", CharArrayToString(result));
      } else {
         PrintFormat("SendPost: [Failed] Server response: [%s]", CharArrayToString(result));
      }
   }
   return res == -1? false: true;
}


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string GetTimeStamp()
{
   /* https://www.mql5.com/en/docs/convert/timetostring
   */
   datetime current_time = TimeCurrent();
   string timestamp = TimeToString(current_time, TIME_DATE | TIME_SECONDS);
   return timestamp;
}


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string GetOrderList()
{

   /* List all active orders */
   
   string orders = ""; 
   int totalOrders = OrdersTotal();                // Get the total number of active orders
   for(int i = 0; i < totalOrders; i++)
   {
      ulong ticket = OrderGetTicket(i);            // Get the ticket number of the order at the specified index
      if(OrderSelect(ticket))                      // Select the order with the specified ticket number
      {
         /*
            order properties:
            https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties
         */
         
         string symbol = OrderGetString(ORDER_SYMBOL);                        // Get the symbol of the selected order
         double price  = OrderGetDouble(ORDER_PRICE_OPEN);                    // Get the open price of the selected order
         double volumeCurrent = OrderGetDouble(ORDER_VOLUME_CURRENT);         // Get the open price of the selected order
         double volumeInitial = OrderGetDouble(ORDER_VOLUME_INITIAL);         // Get the initial volume of the selected order
         double stopLossValue = OrderGetDouble(ORDER_SL);                     // Stop Loss value
         double takeProfitValue = OrderGetDouble(ORDER_TP);                   // Take Profit value
         // int ticket = OrderGetInteger(ORDER_TICKET);

         string order = StringFormat("{ \"ticket\": %d, \"symbol\": \"%s\", \"price\": %.2f, \"volumeCurrent\": %.2f, \"volumeInitial\": %.2f, \"stopLossValue\": %.2f, \"takeProfitValue\": %.2f }",
                                      ticket,
                                      symbol,
                                      price,
                                      volumeCurrent,
                                      volumeInitial,
                                      stopLossValue,
                                      takeProfitValue
                                    );

         Print("OnTrade: Order with ticket ", ticket, " on symbol ", symbol, " has initial volume ", volumeCurrent, " and open price ", price);
         
         if (i == totalOrders - 1) {
             orders = StringFormat("%s %s", orders, order);
         } else {
             orders = StringFormat("%s %s,", orders, order);
         }
      }
   }
   orders = StringFormat("{ \"timestamp\": \"%s\", \"data\": [ %s ] }", GetTimeStamp(), orders);
   return orders;
}


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string GetPositionList()
{
    /* List all positions */
    
    string positions = "";
    int totalPositions = PositionsTotal();           // Get the total number of open positions
    
    for(int i = 0; i < totalPositions; i++)
    {
         ulong ticket = PositionGetTicket(i);        // Get the ticket number of the position at the specified index
         if(PositionSelectByTicket(ticket))          // Select the position with the specified ticket number
         {
            /*
               position properties:
               https://www.mql5.com/en/docs/constants/tradingconstants/positionproperties
            */

            string symbol = PositionGetString(POSITION_SYMBOL);      // Get the symbol of the selected position
            double volume = PositionGetDouble(POSITION_VOLUME);      // Get the volume of the selected position
            double profit = PositionGetDouble(POSITION_PROFIT);      // Get the profit of the selected position
            double priceOpen = PositionGetDouble(POSITION_PRICE_OPEN);

            Print("OnTrade: Position with ticket ", ticket, " on symbol ", symbol, " has volume ", volume, " and profit ", profit);
            string position = StringFormat("{ \"ticket\": %d, \"symbol\": \"%s\", \"volume\": %.2f, \"priceOpen\": %.2f, \"profit\": %.2f }", 
                                          ticket,
                                          symbol,
                                          priceOpen,
                                          profit); 
            
            if (i == totalPositions - 1) {
                positions = StringFormat("%s %s",  positions, position);
            } else {
                positions = StringFormat("%s %s,", positions, position);
            }
         }
   }
   positions = StringFormat("{ \"timestamp\": \"%s\", \"data\": [ %s ] }", GetTimeStamp(), positions);
   return positions;
}


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string GetAccountInfo()
{
   long accountLogin = AccountInfoInteger(ACCOUNT_LOGIN);
   double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   double profit = AccountInfoDouble(ACCOUNT_PROFIT);
   double margin = AccountInfoDouble(ACCOUNT_MARGIN);
   double freeMargin = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
   double marginLevel = AccountInfoDouble(ACCOUNT_MARGIN_LEVEL);
   string marginLevelStr = StringFormat("%.2f %%", marginLevel);

   Print("Account Login: ", accountLogin);
   Print("Balance: ", balance);
   Print("Profit: ", profit);
   Print("Margin: ", margin);
   Print("Free Margin: ", freeMargin);
   Print("Margin Level: ", marginLevel, " %");

   string accountInfo = StringFormat("{ \"timestamp\": \"%s\", \"accountLogin\": %d,  \"balance\": %.2f,  \"profit\": %.2f, \"margin\": %.2f, \"freeMargin\": %.2f, \"marginLevel\": %.2f }\n",
                                     GetTimeStamp(),
                                     accountLogin,
                                     balance,
                                     profit,
                                     margin,
                                     freeMargin,
                                     marginLevel);

   return accountInfo;
}


/* Get Event Type */
string GetTradeEvent(int type) {
   
    switch(type)
    {
      case TRADE_TRANSACTION_ORDER_ADD:     
         return "TRADE_TRANSACTION_ORDER_ADD";

      case TRADE_TRANSACTION_ORDER_UPDATE:  
         return "TRADE_TRANSACTION_ORDER_UPDATE";

      case TRADE_TRANSACTION_ORDER_DELETE:  
         return "TRADE_TRANSACTION_ORDER_DELETE";

      case TRADE_TRANSACTION_DEAL_ADD:      
         return "TRADE_TRANSACTION_DEAL_ADD";

      case TRADE_TRANSACTION_DEAL_UPDATE:   
         return "TRADE_TRANSACTION_DEAL_UPDATE";

      case TRADE_TRANSACTION_DEAL_DELETE:   
         return "TRADE_TRANSACTION_DEAL_DELETE";

      case TRADE_TRANSACTION_POSITION:      
         return "TRADE_TRANSACTION_POSITION";

      case TRADE_TRANSACTION_REQUEST:
         return "TRADE_TRANSACTION_REQUEST";
         
      case TRADE_TRANSACTION_HISTORY_ADD:   
         return "TRADE_TRANSACTION_HISTORY_ADD";

      case TRADE_TRANSACTION_HISTORY_DELETE:
         return "TRADE_TRANSACTION_HISTORY_DELETE";

      case TRADE_TRANSACTION_HISTORY_UPDATE:
         return "TRADE_TRANSACTION_HISTORY_UPDATE";

      default:
         return "UNKNOWN";
   }
}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnTrade()
{
   int positions = PositionsTotal();   // number of open positions
   int orders = OrdersTotal();         // number of active orders
   int deals = HistoryDealsTotal();    // number of deals in the trade history cache

   Print("OnTrade: Trade Transaction Type: ", tradeTransactionType);
   
   string timestamp = GetTimeStamp();
   
   string accountInfo = GetAccountInfo();
   // SendPost(accountInfo);
   
   string orderList = GetOrderList();
   // SendPost(orderList);
   
   string positionList = GetPositionList();
   // SendPost(positionList);
   
   string event = GetTradeEvent(tradeTransactionType);
   
   string updatedStatus = StringFormat("{ \"event\": \"%s\", \"timestamp\": \"%s\", \"account\": %s, \"orders\": %s,  \"positions\": %s }", 
                              event,
                              timestamp,
                              accountInfo,
                              orderList,
                              positionList);
   
   SendPost(updatedStatus);
   
   if(tradeTransactionType == TRADE_TRANSACTION_HISTORY_ADD || tradeTransactionType == TRADE_TRANSACTION_HISTORY_DELETE || tradeTransactionType == TRADE_TRANSACTION_HISTORY_UPDATE)
   {

      Print("OnTrade: Sending Notification to Server ...");
   }

   /* list all positions */
   for(int i = positions-1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);   // select position with ticket
      if(ticket > 0) {
         double profit = PositionGetDouble(POSITION_PROFIT);
         Print("OnTrade: Remaining position[", i, "/", positions,"]: ticket:", ticket, " profit:", profit);
      }
   }
   
   /* list all orders */
   for(int i = orders-1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket > 0)
      {
         string comment = OrderGetString(ORDER_COMMENT);
         string symbol = OrderGetString(ORDER_SYMBOL);

         Print("OnTrade: Active Order[", i, "/", orders,"]: ticket:", ticket, " symbol:", symbol, " comment:", comment);
      }
   }


   for(int i = deals-1; i >= 0; i--)
   {
      /* History Deals */
   }
}



//+------------------------------------------------------------------+
//| TradeTransaction function                                        |
//+------------------------------------------------------------------+
int tradeTransactionType;

// This function is called when a trade event occurs
void OnTradeTransaction(const MqlTradeTransaction& trans,
                        const MqlTradeRequest& request,
                        const MqlTradeResult& result)
{
   tradeTransactionType = trans.type;

   // https://www.mql5.com/en/docs/constants/tradingconstants/enum_trade_transaction_type
   string msg;

   switch(trans.type)
     {
      case TRADE_TRANSACTION_ORDER_ADD:     // 0
         Print("OnTradeTransaction: type: ", trans.type, "; A new order was added. Order ID: ", trans.order);
         break;

      case TRADE_TRANSACTION_ORDER_UPDATE:  // 1
         Print("OnTradeTransaction: type: ", trans.type, "; An existing order was updated. Order ID: ", trans.order);
         break;

      case TRADE_TRANSACTION_ORDER_DELETE:  // 2
         Print("OnTradeTransaction: type: ", trans.type, "; An order was deleted from the list of active orders. Order ID: ", trans.order);
         break;

      case TRADE_TRANSACTION_DEAL_ADD:      // 6
         Print("OnTradeTransaction: type: ", trans.type, "; A deal was added to history. Deal ID: ", trans.deal);
         break;

      case TRADE_TRANSACTION_DEAL_UPDATE:   //
         Print("OnTradeTransaction: type: ", trans.type, "; A deal in history was updated. Deal ID: ", trans.deal);
         break;

      case TRADE_TRANSACTION_DEAL_DELETE:   //
         Print("OnTradeTransaction: type: ", trans.type, "; A deal was deleted from history. Deal ID: ", trans.deal);
         break;

      case TRADE_TRANSACTION_POSITION:      //
         Print("OnTradeTransaction: type: ", trans.type, "; A position change not related to a trade execution occurred. Position ID: ", trans.position);

         break;

      case TRADE_TRANSACTION_REQUEST:
         Print("OnTradeTransaction: type: ", trans.type, "; A trade request has been processed by the server and the result of its processing has been received.");
         break;

      case TRADE_TRANSACTION_HISTORY_ADD:   // 3
         Print("OnTradeTransaction: TRADE_TRANSACTION_HISTORY(ADD): ", trans.type);
         break;

      case TRADE_TRANSACTION_HISTORY_DELETE:
         Print("OnTradeTransaction: TRADE_TRANSACTION_HISTORY(DELETE): ", trans.type);
         break;

      case TRADE_TRANSACTION_HISTORY_UPDATE:
         Print("OnTradeTransaction: TRADE_TRANSACTION_HISTORY(UPDATE): ", trans.type);

         break;

      default:
         Print("OnTradeTransaction: Unknown transaction type: ", trans.type);
         break;
     }

   msg = StringFormat("{ \"transaction\": %d }", trans.type);
   PrintFormat("OnTradeTransaction: data: %s", msg);
}


//+------------------------------------------------------------------+


     HDFTACTGRP(*NO)                                                                 
      *                                                                              
     FQPRINT    O    F  132        PRINTER                                           
      *                                                                              
      /COPY QSYSINC/QRPGLESRC,QTOCNETSTS                                             
     Din               DS                  QUALIFIED                                 
     D d1                                  LIKEDS(QTOA0100)                          
     D d2                                  LIKEDS(QTOA0200)                          
      *                                                                              
      /COPY QSYSINC/QRPGLESRC,QUSEC                                                  
      *                                                                              
     Dparams_len       S              9B 0                                           
      *                                                                              
     C     params        PLIST                                                       
     C                   PARM                    in                                  
     C                   PARM                    params_len                          
     C                   PARM      'TCPA0200'    format_name       8                 
     C                   PARM                    QUSEC                               
      *                                                                              
     C                   EVAL      QUSBPRV = %LEN(QUSEC)                             
     C                   EVAL      params_len = %LEN(in)                             
     C                   CALLB     'QtocRtvTCPA' params                              
      *                                                                              
     C                   IF        QUSBAVL = 0                                       
     C                   MOVE      in.d1         QTOA0100                            
     C                   MOVE      in.d2         QTOA0200                            
     C                   EXCEPT    TCPATR                                            
     C                   ELSE                                                        
     C                   EXCEPT    ERRORPRT                                          
     C                   ENDIF                                                       
      *                                                                              
     C                   EVAL      *INLR = *ON                                       
      *                                                                              
     OQPRINT    E            ERRORPRT    1  2                                        
     O                                           40 '** TCP/IP V4 STACK -            
     O                                              ATTRIBUTES **'                   
     O                                           +5 '(API ERROR)'                    
     O          E            ERRORPRT       1                                        
     O                                           40 'BYTES AVAILABLE :'              
     O                       QUSBAVL       P     60                                  
     O          E            ERRORPRT       1                                        
     O                                           40 'EXCEPTION ID :'                 
     O                       QUSEI               60                                  
      *                                                                              
     O          E            TCPATR      1  2                                        
     O                                           40 '** TCP/IP V4 STACK -            
     O                                              ATTRIBUTES **'                   
     O                                           +5 '(<DEFAULT> IS BASED ON -        
     O                                              V5R4.)'                          
     O          E            TCPATR         1                                        
     O                                           40 'IP DATAGRAM FORWARDING :'       
     O                       QTOIPDF       P     60                                  
     O                                           +1 '(<0=DISABLED>, 1=-              
     O                                              ENABLED)'                        
     O          E            TCPATR         1                                        
     O                                           40 'UDP CHECKSUM :'                 
     O                       QTOUDPC       P     60                                  
     O                                           +1 '(0=NO, <1=YES>)'                
     O          E            TCPATR         1                                        
     O                                           40 'LOG PROTOCOL ERRORS :'          
     O                       QTOLPE        P     60                                  
     O                                           +1 '(0=NOTLOGGED, 1=-               
     O                                              LOGGED)'                         
     O          E            TCPATR         1                                        
     O                                           40 'IP SOURCE ROUTING :'            
     O                       QTOIPSR00     P     60                                  
     O                                           +1 '(0=DISABLED, <1=ENABLED>)'      
     O          E            TCPATR         1                                        
     O                                           40 'TCP URGENT POINTER :'           
     O                       QTOTCPUP      P     60                                  
     O                                           +1 '(<1=BSD>, 2=RFC)'               
     O          E            TCPATR         1                                        
     O                                           40 'IP REASSEMBLY TIMEOUT :'        
     O                       QTOIPRT       P     60                                  
     O                                           +1 '(SEC <10>)'                     
     O          E            TCPATR         1                                        
     O                                           40 'IP TIME TO LIVE :'              
     O                       QTOIPTTL      P     60                                  
     O                                           +1 '(TTL VALUE <64>)'               
     O          E            TCPATR         1                                        
     O                                           40 'TCP KEEP ALIVE :'               
     O                       QTOTCPKA      P     60                                  
     O                                           +1 '(MIN <120>)'                    
     O          E            TCPATR         1                                        
     O                                           40 'TCP RECEIVE BUFFER :'           
     O                       QTOTCPRB      P     60                                  
     O                                           +1 '(BYTES <8192>)'                 
     O          E            TCPATR         1                                        
     O                                           40 'TCP SEND BUFFER :'              
     O                       QTOTCPSB      P     60                                  
     O                                           +1 '(BYTES <8192>)'                 
     O          E            TCPATR         1                                        
     O                                           40 'ARP CACHE TIMEOUT :'            
     O                       QTOARPCT      P     60                                  
     O                                           +1 '(MIN <5>)'                      
     O          E            TCPATR         1                                        
     O                                           40 'MTU PATH DISCOVERY :'           
     O                       QTOMTUPD      P     60                                  
     O                                           +1 '(0=DISABLED, <1=ENABLED>)'      
     O          E            TCPATR         1                                        
     O                                           40 'MTU DISCOVERY INTERVAL :'       
     O                       QTOMTUDI      P     60                                  
     O                                           +1 '(MIN <10>)'                     
     O          E            TCPATR         1                                        
     O                                           40 'QOS ENABLEMENT :'               
     O                       QTOQSE        P     60                                  
     O                                           +1 '(1=*TOS, 2=*YES, <3=*NO>)'      
     O          E            TCPATR         1                                        
     O                                           40 'QOS TIMER RESOLUTION :'         
     O                       QTOQSTR       P     60                                  
     O                                           +1 '(MILLISECONDS <100>)'           
     O          E            TCPATR         1                                        
     O                                           40 'QOS DATA PATH -                 
     O                                              OPTIMIZATION :'                  
     O                       QTOQSDPO      P     60                                  
     O                                           +1 '(<1=NORMAL>, 2=*MINDELAY)'      
     O          E            TCPATR         1                                        
     O                                           40 'DEAD GATEWAY DETECTION -        
     O                                              ENABLEMENT :'                    
     O                       QTODGDE       P     60                                  
     O                                           +1 '(0=OFF, <1=ON>)'                
     O          E            TCPATR         1                                        
     O                                           40 'DEAD GATEWAY DETECTION -        
     O                                              INTERVAL :'                      
     O                       QTODGDI       P     60                                  
     O                                           +1 '(MIN <2>)'                      
     O          E            TCPATR         1                                        
     O                                           40 'TCP TIME WAIT TIMEOUT :'        
     O                       QTOCPTWT      P     60                                  
     O                                           +1 '(SEC <120>)'                    
     O          E            TCPATR         1                                        
     O                                           40 'TCP R1 RETRANSMISSION -         
     O                                              COUNT :'                         
     O                       QTOPR1RC      P     60                                  
     O                                           +1 '(COUNT <3>)'                    
     O          E            TCPATR         1                                        
     O                                           40 'TCP R2 RETRANSMISSION -         
     O                                              COUNT :'                         
     O                       QTOPR2RC      P     60                                  
     O                                           +1 '(COUNT <16>)'                   
     O          E            TCPATR         1                                        
     O                                           40 'TCP MINIMUM -                   
     O                                              RETRANSMISSION TIMEOUT :'        
     O                       QTOCPMRT      P     60                                  
     O                                           +1 '(MILLISECONDS <250>)'           
     O          E            TCPATR         1                                        
     O                                           40 'TCP CLOSE CONNECTION -          
     O                                              MESSAGE :'                       
     O                       QTOCPCCM      P     60                                  
     O                                           +1 '(<1=*THRESHOLD>, -              
     O                                              2=*ALL, 3=*NONE)'                
     O          E            TCPATR         1                                        
     O                                           40 'NETWORK FILE CACHE -            
     O                                              ENABLEMENT :'                    
     O                       QTONFCE       P     60                                  
     O                                           +1 '(0=*NO, 1=*YES)'                
     O          E            TCPATR         1                                        
     O                                           40 'NETWORK FILE CACHE -            
     O                                              INTERVAL :'                      
     O                       QTONFCI       P     60                                  
     O          E            TCPATR         1                                        
     O                                           40 'NETWORK FILE CACHE SIZE :'      
     O                       QTONFCS       P     60                                  
     O                                           +1 '(MB)'                           
     O          E            TCPATR         1                                        
     O                                           40 'EXPLICIT CONGESSION -           
     O                                              NOTIFICATION :'                  
     O                       QTOECNE       P     60                                  
     O                                           +1 '(<0=DISABLED>, 1=-              
     O                                              ENABLED)'                        
     O          E            TCPATR      2  1                                        
     O                                          100 '* REFERENCE : HTTP://-          
     O                                              PUBLIB.BOULDER.IBM.COM/-         
     O                                              INFOCENTER/ISERIES/-             
     O                                              V5R4/TOPIC/APIS/-                
     O                                              QTOCRTVTCPA.HTM'                 
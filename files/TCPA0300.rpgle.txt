     HDFTACTGRP(*NO)                                                                 
      *                                                                              
     FQPRINT    O    F  132        PRINTER                                           
      *                                                                              
      /COPY QSYSINC/QRPGLESRC,QTOCNETSTS                                             
     Din               DS                  QUALIFIED                                 
     D d1                                  LIKEDS(QTOA0100)                          
     D d3                                  LIKEDS(QTOA0300)                          
     D dns1                                LIKEDS(QTOPALIA) INZ                      
     D dns2                                LIKEDS(QTOPALIA) INZ                      
     D dns3                                LIKEDS(QTOPALIA) INZ                      
      *                                                                              
      /COPY QSYSINC/QRPGLESRC,QUSEC                                                  
      *                                                                              
     Dparams_len       S              9B 0                                           
     Ddns              S             15    DIM(3)                                    
     DQTODSL_80        S             80                                              
     DQTODN_80         S             80                                              
      *                                                                              
     C     params        PLIST                                                       
     C                   PARM                    in                                  
     C                   PARM                    params_len                          
     C                   PARM      'TCPA0300'    format_name       8                 
     C                   PARM                    QUSEC                               
      *                                                                              
     C                   EVAL      QUSBPRV = %LEN(QUSEC)                             
     C                   EVAL      params_len = %LEN(in)                             
     C                   CALLB     'QtocRtvTCPA' params                              
      *                                                                              
     C                   IF        QUSBAVL = 0                                       
     C                   MOVE      in.d1         QTOA0100                            
     C                   MOVE      in.d3         QTOA0300                            
     C                   EVAL      QTODSL_80 = %STR(%ADDR(QTODSL) : 80)              
     C                   EVAL      QTODN_80 = %SUBST(QTODN : 1 : 80)                 
      * The number of elements in the list of Domain Name Server (DNS).              
     C                   IF        QTONOIA = 0                                       
     C                   SETON                                        10             
     C                   ELSE                                                        
     C                   EVAL      dns(1) = in.dns1.QTOIA01                          
     C                   EVAL      dns(2) = in.dns2.QTOIA01                          
     C                   EVAL      dns(3) = in.dns3.QTOIA01                          
     C                   ENDIF                                                       
     C                   EXCEPT    TCPATR                                            
     C                   ELSE                                                        
     C                   EXCEPT    ERRORPRT                                          
     C                   ENDIF                                                       
      *                                                                              
     C                   EVAL      *INLR = *ON                                       
      *                                                                              
     OQPRINT    E            ERRORPRT    1  2                                        
     O                                           40 '** TCP/IP DOMAIN -              
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
     O                                           40 '** TCP/IP DOMAIN -              
     O                                              ATTRIBUTES **'                   
     O                                           +5 '(<DEFAULT> IS BASED ON -        
     O                                              V5R4.)'                          
     O*         E            TCPATR         1                                        
     O*                                          40 'OFFSET TO LIST INTERNET -       
     O*                                             ADDR :'                          
     O*                      QTOOTLIA      P     60                                  
     O*         E            TCPATR         1                                        
     O*                                          40 'NUMBER OF INTERNET -            
     O*                                             ADDRESSES :'                     
     O*                      QTONOIA       P     60                                  
     O*         E            TCPATR         1                                        
     O*                                          40 'ENTRY LEN LIST INTERNET -       
     O*                                             ADDR :'                          
     O*                      QTOELLIA      P     60                                  
     O          E            TCPATR         1                                        
     O                                           40 'DNS PROTOCOL :'                 
     O                       QTODNSP       P     60                                  
     O                                           +1 '(1=UDP, 2=TCP)'                 
     O          E            TCPATR         1                                        
     O                                           40 'RETRIES :'                      
     O                       QTOTRIES      P     60                                  
     O                                           +1 '(NUMBER <2>)'                   
     O          E            TCPATR         1                                        
     O                                           40 'TIME INTERVAL :'                
     O                       QTOTI         P     60                                  
     O                                           +1 '(SEC <2>)'                      
     O          E            TCPATR         1                                        
     O                                           40 'SEARCH ORDER :'                 
     O                       QTOSO00       P     60                                  
     O                                           +1 '(1=LOCAL, <2=REMOTE>)'          
     O          E            TCPATR         1                                        
     O                                           40 'INITIAL DNS SERVER :'           
     O                       QTOIDNSS      P     60                                  
     O                                           +1 '(<1=FIRST>, 2=ROTATE)'          
     O          E            TCPATR         1                                        
     O                                           40 'DNS LISTENING PORT :'           
     O                       QTODNSLP      P     60                                  
     O                                           +1 '(PORT <53>)'                    
     O          E            TCPATR         1                                        
     O                                           40 'HOST NAME :'                    
     O                       QTOHN               +1                                  
     O          E            TCPATR         1                                        
     O                                           40 'DOMAIN NAME :'                  
     O                       QTODN_80            +1                                  
     O          E            TCPATR         1                                        
     O                                           40 'DOMAIN SEARCH LIST :'           
     O                       QTODSL_80           +1                                  
     O          E    10      TCPATR         1                                        
     O                                           40 'DNS INTERNET ADDRESS :'         
     O                                           60 '(NO DNS DEFINED)'               
     O          E   N10      TCPATR         1                                        
     O                                           40 'DNS INTERNET ADDRESS 1 :'       
     O                       dns(1)              +1                                  
     O          E   N10      TCPATR         1                                        
     O                                           40 'DNS INTERNET ADDRESS 2 :'       
     O                       dns(2)              +1                                  
     O          E   N10      TCPATR         1                                        
     O                                           40 'DNS INTERNET ADDRESS 3 :'       
     O                       dns(3)              +1                                  
     O          E            TCPATR      2  1                                        
     O                                          100 '* REFERENCE : HTTP://-          
     O                                              PUBLIB.BOULDER.IBM.COM/-         
     O                                              INFOCENTER/ISERIES/-             
     O                                              V5R4/TOPIC/APIS/-                
     O                                              QTOCRTVTCPA.HTM'                 
CREATE TABLE SYSTEM_B.SALES_ORDER 
(
  ID NUMBER(10) NOT NULL 
, CLIENT VARCHAR2(100) NOT NULL 
, PRICE NUMBER(8,2) NOT NULL 
, CONSTRAINT SALES_ORDER_PK PRIMARY KEY 
  (
    ID 
  )
  ENABLE 
);

ALTER USER SYSTEM_B IDENTIFIED BY welcome1;

GRANT CONNECT, RESOURCE TO SYSTEM_B;


//Declare variables for functions
int x;
String dataUART;
int sec = 1;
int scan_step = 10;

//Declare pin functions on EasyDriver
const int dir1 = 17; // direction
const int stp1 = 16; // steps
const int EN1 = 4; // Enable HIGH (disabled) / LOW(enabled)
const int dir2 = 23; // direction
const int stp2 = 19; // steps
const int EN2 = 34; // Enable HIGH (disabled) / LOW(enabled)


void setup() {
  Serial.begin(115200); // Configura la velocidad de baudios para la comunicación serial USB (para depuración)
  pinMode(stp1, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(EN1, OUTPUT);
  pinMode(stp2, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(EN2, OUTPUT);
  Serial.println("Ready...");
  DisableMotores();
}

void loop() {
   // Leer desde el puerto serial USB (para depuración)
  if (Serial.available()) {
    dataUART = Serial.readStringUntil('\n');
    //Serial.println(dataUART);
        
    if (dataUART.equals("stp")){
      //Serial.println("stop");
      DisableMotores();
      dataUART = "";
    }
    if (dataUART == "ste"){
      //Serial.println("step");
      dataUART = "";
    }
    if (dataUART == "SCC"){
      SCC();
    }
    if (dataUART == "SCW"){
      SCW();
    }
    if (dataUART == "MCC"){
      MCC();
    }
    if (dataUART == "MCW"){
      MCW();
    }

    String turn = dataUART.substring(0,2);
    String motor = dataUART.substring(2,dataUART.length());
    /*
        Serial.print("Giro:");
        Serial.println(turn);
        Serial.print("Motor:");
        Serial.println(motor);
     */
    if (turn=="CC" || turn=="CW"){
 
        if(turn=="CC" && motor == "1"){
            digitalWrite(EN1, LOW);
            digitalWrite(dir1, LOW);
            while(!dataUART.equals("stp")){
                  digitalWrite(stp1,HIGH); //Trigger one step ForwardReverse
                  delay(sec);
                  digitalWrite(stp1,LOW); //Pull step pin low so it can be triggered again
                  delay(sec);
                  while (Serial.available() > 0) {
                    dataUART = Serial.readStringUntil('\n');
                    if (dataUART == "SCC"){SCC();}
                    if (dataUART == "SCW"){SCW();}
                  }
            }
            DisableMotores();
        }
        
        if(turn=="CW" && motor == "1"){
            digitalWrite(EN1, LOW);
            digitalWrite(dir1, HIGH);
            while(!dataUART.equals("stp")){
                  digitalWrite(stp1,HIGH); //Trigger one step ForwardReverse
                  delay(sec);
                  digitalWrite(stp1,LOW); //Pull step pin low so it can be triggered again
                  delay(sec);
                  while (Serial.available() > 0) {
                    dataUART = Serial.readStringUntil('\n');
                    if (dataUART == "SCC"){SCC();}
                    if (dataUART == "SCW"){SCW();}
                  }
            }
            DisableMotores();
        }

        if(turn=="CC" && motor == "2"){
            digitalWrite(EN2, LOW);
            digitalWrite(dir2, LOW);
            while(!dataUART.equals("stp")){
                  digitalWrite(stp2,HIGH); //Trigger one step ForwardReverse
                  delay(sec);
                  digitalWrite(stp2,LOW); //Pull step pin low so it can be triggered again
                  delay(sec);
                  while (Serial.available() > 0) {
                    dataUART = Serial.readStringUntil('\n');
                  }
            }
            DisableMotores();
        }
        
        if(turn=="CW" && motor == "2"){
            digitalWrite(EN2, LOW);
            digitalWrite(dir2, HIGH);
            while(!dataUART.equals("stp")){
                  digitalWrite(stp2,HIGH); //Trigger one step ForwardReverse
                  delay(sec);
                  digitalWrite(stp2,LOW); //Pull step pin low so it can be triggered again
                  delay(sec);
                  while (Serial.available() > 0) {
                    dataUART = Serial.readStringUntil('\n');
                  }
            }
            DisableMotores();
        }

        
        dataUART = "";
    }

    

    dataUART = "";

  }
}


void MCC()
{
    digitalWrite(EN2, LOW);
    digitalWrite(dir2, LOW);
    for(x= 0; x<100; x++){
        digitalWrite(stp2,HIGH); //Trigger one step forward
        delay(sec);
        digitalWrite(stp2,LOW); //Pull step pin low so it can be triggered again
        delay(sec);
    }
    digitalWrite(EN2, HIGH);
}

void MCW()
{
    digitalWrite(EN2, LOW);
    digitalWrite(dir2, HIGH);
    for(x= 0; x<100; x++){
        digitalWrite(stp2,HIGH); //Trigger one step forward
        delay(sec);
        digitalWrite(stp2,LOW); //Pull step pin low so it can be triggered again
        delay(sec);
    }
    digitalWrite(EN2, HIGH);
}

void SCC()
{
    digitalWrite(EN2, LOW);
    digitalWrite(dir2, LOW);
    for(x= 0; x<scan_step; x++){
        digitalWrite(stp2,HIGH); //Trigger one step forward
        delay(sec);
        digitalWrite(stp2,LOW); //Pull step pin low so it can be triggered again
        delay(sec);
    }
    digitalWrite(EN2, HIGH);
}

void SCW()
{
    digitalWrite(EN2, LOW);
    digitalWrite(dir2, HIGH);
    for(x= 0; x<scan_step; x++){
        digitalWrite(stp2,HIGH); //Trigger one step forward
        delay(sec);
        digitalWrite(stp2,LOW); //Pull step pin low so it can be triggered again
        delay(sec);
    }
    digitalWrite(EN2, HIGH);
}



void DisableMotores()
{
  digitalWrite(stp1, LOW);
  digitalWrite(dir1, LOW);
  digitalWrite(EN1, HIGH);
  digitalWrite(stp2, LOW);
  digitalWrite(dir2, LOW);
  digitalWrite(EN2, HIGH);
}

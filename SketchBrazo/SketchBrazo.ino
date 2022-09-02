
/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>
int val= 0, trash, newval= 0, state=0, reading, numservo = 0;

Servo myservo1;  // create servo object to control a servo
Servo myservo2;
Servo myservo3;
Servo myservo4;
Servo myservo5;
Servo myservo6;
Servo myservo7;
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
Servo servos[7];
int posns[7];


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);
  myservo1.attach(2);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(3);
  myservo3.attach(4);
  myservo4.attach(5);
  myservo5.attach(6);
  myservo6.attach(7);
  myservo7.attach(8);
  servos[0]=myservo4;
  servos[1]=myservo1;
  servos[2]=myservo2;
  servos[3]=myservo3;
  servos[4]=myservo5;
  servos[5]=myservo6;
  servos[6]=myservo7;
  for(int i = 0; i < 7; i++){
    posns[i] = 90;
  }
  posns[1] = 85;
  posns[2] = 80;
  posns[4] = 90;
  posns[5] = 20;
  for(int i=0;i<6;i++){
    servos[i].write(posns[i]);
  }
  delay(1000);
  Serial.println("Ready");
}

void loop() {
  
  if(Serial.available()){
    reading = Serial.parseInt();
    //while(Serial.available()){
    //  trash=Serial.read();
    //}
    //trash = Serial.read();
    //Serial.println(reading);
    //Serial.print("State: ");
    //Serial.println(state);
    if(reading == 0 && state == 0){
      //Serial.print("Servo: ");
      state = 1;
    }else if(state == 1){
      numservo = reading;
      state = 0;
      //Serial.println(numservo);
    }else if(state == 0 && reading == 1){
      state = 2;
      //Serial.print("Angulo: ");
    }else if(state == 2){
      state = 0;
      val = posns[numservo];
      if(numservo == 1){
        reading = map(reading,0,90,20,85);
      }else if(numservo == 2){
        reading = map(reading,0,90,80,15);
      }else if(numservo == 4){
        reading = map(reading,0,90,90,180);
      }else if(numservo == 0){
        reading = map(reading,0,90,90,0);
      }else if(numservo == 3){
        reading = map(reading,0,90,90,155);
      }
      posns[numservo]=reading;
      //Serial.println(newval);
      if(posns[numservo] < val){
        //Serial.println(posns[numservo]);  
        //Serial.println(val);
        for(int i = val; i > posns[numservo]; i--){
          servos[numservo].write(i);
          //Serial.println(i);
          delay(20);
        }
      }else if(posns[numservo] > val){
        //Serial.println(posns[numservo]);
        //Serial.println(val);
        for(int i = val; i < posns[numservo]; i++){
          servos[numservo].write(i);
          //Serial.println(i);
          delay(20);
        }
      }
    }
  }
  delay(15); 
}

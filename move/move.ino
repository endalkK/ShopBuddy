#include <SparkFun_TB6612.h>

//pins for the motor control
#define AIN1 2
#define BIN1 7 
#define AIN2 4 
#define BIN2 8
#define PWMA 5
#define PWMB 6
#define STBY 9

// pins for the encoder inputs
#define RH_ENCODER_A 29 //28 //26 
#define RH_ENCODER_B 28 //29 //27
#define LH_ENCODER_A 27 //26 //28
#define LH_ENCODER_B 26 //27 //29

const int offsetA = 1;
const int offsetB = 1;

Motor motor1 = Motor(AIN1, AIN2, PWMA, offsetA, STBY);
Motor motor2 = Motor(BIN1, BIN2, PWMB, offsetB, STBY);

volatile int lastRightEncoded = 0;
volatile int lastLeftEncoded = 0;
volatile long rightEncoderValue = 0;
volatile long leftEncoderValue = 0;

//Previous encoder reading
volatile long lastLeftCount = 0;
volatile long lastRightCount = 0;
volatile unsigned long lastTime = 0;

#define ENCODER_COUNTS_PER_ROTATION 540.0386946
#define wheelRadius  0.0388 
#define wheelBase  0.1 

long encoderCountsFor90Degrees = wheelBase/(8*wheelRadius) * ENCODER_COUNTS_PER_ROTATION; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LH_ENCODER_A, INPUT_PULLUP);
  pinMode(LH_ENCODER_B, INPUT_PULLUP);
  pinMode(RH_ENCODER_A, INPUT_PULLUP);
  pinMode(RH_ENCODER_B, INPUT_PULLUP);
  attachInterrupt(RH_ENCODER_A , updateRightEncoder, CHANGE);
  attachInterrupt(RH_ENCODER_B , updateRightEncoder, CHANGE);
  attachInterrupt(LH_ENCODER_A , updateLeftEncoder, CHANGE);
  attachInterrupt(LH_ENCODER_B , updateLeftEncoder, CHANGE);
}

void loop() {
  // put your main code here, to run repeatedly:

}
void updateRightEncoder(){
  int MSB = digitalRead(RH_ENCODER_A); //MSB = most significant bit
  int LSB = digitalRead(RH_ENCODER_B); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastRightEncoded << 2) | encoded; //adding it to the previous encoded value

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) rightEncoderValue --;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) rightEncoderValue ++;

  lastRightEncoded = encoded; //store this value for next time
}

void updateLeftEncoder(){
  int MSB = digitalRead(LH_ENCODER_A); //MSB = most significant bit
  int LSB = digitalRead(LH_ENCODER_B); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number
  int sum  = (lastLeftEncoded << 2) | encoded; //adding it to the previous encoded value

  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) leftEncoderValue ++;
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) leftEncoderValue --;

  lastLeftEncoded = encoded; //store this value for next time
}
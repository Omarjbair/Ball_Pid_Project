#include <LiquidCrystal.h>
#include <LCD_I2C.h>
#include <PID_v1.h>
#include <Servo.h>
LCD_I2C lcd(0x27, 16, 2);

//const int rs = 3, en = 2, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
//LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

Servo yServo, xServo;

double xSetpoint, xInput, xOutput, ySetpoint, yInput, yOutput, x, y;
String Data;


PID yPID(&yInput, &yOutput, &ySetpoint, 0.1, 0.03, 0.08, REVERSE);
PID xPID(&xInput, &xOutput, &xSetpoint, 0.3, 0.05, 0.15, REVERSE);


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  yServo.attach(10);
  yServo.write(70);

  xServo.attach(9);
  xServo.write(60);

  ySetpoint = 200;
  xSetpoint = 300;

  yPID.SetMode(AUTOMATIC);
  xPID.SetMode(AUTOMATIC);

  lcd.begin();
  lcd.backlight();
}

void loop() {
  if (Serial.available())
  {
    Data = Serial.readString();

    x = Data.substring(0, Data.indexOf(",")).toDouble();
    y = Data.substring(Data.indexOf(",") + 1).toDouble();


    xInput = x;
    xPID.Compute();
    xPID.SetOutputLimits(40, 75);
    xServo.write(xOutput);


    yInput = y;
    yPID.Compute();
    yPID.SetOutputLimits(10, 90);
    yServo.write(yOutput);



    lcd.setCursor(0, 1);
    lcd.print(x);
    lcd.setCursor(8, 1);
    lcd.print(y);
    delay(100);
    lcd.clear();
  }
  else
  {
    yServo.write(70);
    xServo.write(60);
  }
}

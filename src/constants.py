class Constants:

    class PWM:
        FREQUENCY = 8000  # Hz

    class Motors:
        # PIN GPIO COLOR
        # 18  24   VIOLET
        # 13  27   BLUE
        # 12  18   BROWN
        # 18  10   YELLOW
        # 10  15   ORANGE
        # 15  22   WHITE
        # 9   GND  BLACK

        LEFT_REV_PIN = 15
        RIGHT_REV_PIN = 22

        FRONT_LEFT_MOTOR_PWM_PIN = 24
        FRONT_RIGHT_MOTOR_PWM_PIN = 18

        BACK_LEFT_MOTOR_PWM_PIN = 27
        BACK_RIGHT_MOTOR_PWM_PIN = 10

Notes for dev

Electrode Interface Board (powered by the MCB, communication via I2C or SPI):
    19 x INA118 amplifiers 
        Amplifier Circuits (each eamp circuit should have a corresponding filter circuit connected in series with the output of the amplifier):
            - Input impedance resistor: 100 kOhms
            - Feedback resistor: 10 kOhms
            - Compensation capacitor: 10 pF
            - Filtering Capacitor: 1 uF
            - Filtering Resistor; 10 kOhms

    19 x Op-amp - TL072 (used to buffer and amplify the filtered signals before routing to the multiplexers)
    2 x CD74HC4067 multiplexers ( Selects which electrode signal to route to the MCB)
    3 x HC-49U 16 Mhz Crystal quartz resonators (provides clock signals for the amp circuites and other comps)
        - Capacitors: 15 pF to 33 pF
    3 x LED Indicators (on, communicating)

Microcontroller Board:
    1 x ESP32-WROOM-CD2102 microcontroller (built in bluetooth and wifi)
    4 x ADS1015 ADCs (digitizes the signal)
    1 x ADS1115
        - CD74HC4067 #1: Connects to ADS1015 #1 and selects between channels 0-3
        - CD74HC4067 #2: Connects to ADS1015 #1 and selects between channels 4-7
        - CD74HC4067 #3: Connects to ADS1015 #2 and selects between channels 8-11
        - CD74HC4067 #4: Connects to ADS1015 #2 and selects between channels 12-15
        - CD74HC4067 #5: Connects to ADS1115 and selects between channels 16-19
    1 x 3.7V 1000mAh LiPo battery (powers everything)
    1 x TP4056 Charging module (charges LiPo battery via USB-C, 5 v, cutoff voltage 4.2v, charging current 1000mA, 3A overcurrent protection, 2.5v overdischarge protection)
    1 x LM1117-3.3 voltage regulator
        - Input capacitor: 10 uF
        - Output capacitor: 1 uF
    1 x TXB0108PWR Logic level shifter (enables communication)
        -  10 kOhm pull-up resistor
    5 x CD74HC4067 I2C multiplexers
        - 4.7 kOhm pull-up resistor
    1 x MPU-9250 gyroscope and accelerometer
    2 x 2N3904 NPN transistors (used to control the power supply to the ADS1286 ADC's; MCU sets GPIO pin to logic high level)
    1 x IRLML2502 MOSFETs (provides power to the MPU-2950)
    3 x LED indicators (on, communicating, bluetooth connected)


Breakdownish - 
19 x $3.33 (INA118) = $63.27
19 x $0.20 (1uF Capacitor) = $3.80
19 x $0.01 (10kOhm Resistor) = $0.19
19 x $0.01 (100kOhm Resistor) = $0.19
19 x $0.01 (10pF Capacitor) = $0.19
19 x $0.01 (10kOhm Resistor) = $0.19
19 x $0.61 (TL072) = $11.59
2 x $0.39 (CD74HC4067) = $0.78
3 x $0.44 (HC-49U 16 Mhz Crystal) = $1.32
57 x $0.01 (10pF - 33pF Capacitor) = $0.57
3 x $0.14 (LED) = $0.42
1 x $7.45 (ESP32-WROOM-CD2102) = $7.45
4 x $2.43 (ADS1015) = $9.72
1 x $2.76 (ADS1115) = $2.76
5 x $0.39 (CD74HC4067) = $1.95
1 x $8.51 (MPU-9250) = $8.51
2 x $0.03 (2N3904 NPN Transistor) = $0.06
1 x $0.40 (IRLML2502 MOSFET) = $0.40
3 x $0.14 (LED) = $0.42
1 x $7.95 (3.7V 1000mAh LiPo Battery) = $7.95
1 x $6.95 (TP4056 Charging module) = $6.95
1 x $0.56 (LM1117-3.3 3.3V Voltage Regulator) = $0.56
1 x $1.02 (TXB0108PWR Logic Level Shifter) = $1.02
1 x $0.28 (10uF Capacitor) = $0.28
5 x $0.01 (4.7 kOhm Resistor) = $0.05

The total cost of all components is approximately $119.43. 
// Turbidity Water Disposal System

// Pin Definitions

#define BOTTOM_TURBIDITY_PIN A0 // Analog input for bottom turbidity sensor
#define TOP_TURBIDITY_PIN A1    // Analog input for top turbidity sensor
#define RESERVOIR_VALVE 2       // Digital output for reservoir solenoid valve and main tank
#define DISPOSAL_VALVE 3        // Digital output for turbid water disposal solenoid valve and main tank
#define TAP_VALVE_ONE 4         // Digital output for tap solenoid valve between main tank and tap
#define TAP_VALVE_TWO 5         // Digital output for tap solenoid valve between reservoir and tap

#define TURBIDITY_THRESHOLD_ONE 300 // Threshold for turbidity sensor readings, have to be calibrated
#define TURBIDITY_THRESHOLD_TWO 300 // Threshold for turbidity sensor readings, have to be calibrated

// Variable Definitions
int bottomTurbidity = 0;  // Variable to store bottom turbidity sensor reading
int topTurbidity = 0;     // Variable to store top turbidity sensor reading
bool waterTurbid = false; // Flag to indicate if water is turbid

void setup()
{
    // Initialize serial communication for debugging
    Serial.begin(9600);

    pinMode(RESERVOIR_VALVE, OUTPUT); // Set reservoir valve pin as output
    pinMode(DISPOSAL_VALVE, OUTPUT);  // Set disposal valve pin as output
    pinMode(TAP_VALVE_ONE, OUTPUT);   // Set tap valve one pin as output
    pinMode(TAP_VALVE_TWO, OUTPUT);   // Set tap valve two pin as output

    // Close all valves at startup
    closeAllValves();

    Serial.println("Turbidity Water Disposal System Initialized");
}

void loop()
{
    bottomTurbidity = analogRead(BOTTOM_TURBIDITY_PIN); // Read bottom turbidity sensor
    topTurbidity = analogRead(TOP_TURBIDITY_PIN);       // Read top turbidity sensor

    bottomTurbidity = (float) bottomTurbidity * (5.0/1024.0)
    topTurbidity = (float) bottomTurbidity * (5.0/1024.0)


    Serial.print("Bottom Turbidity: ");
    Serial.println(bottomTurbidity); // Print bottom turbidity reading
    Serial.print("Top Turbidity: ");
    Serial.println(topTurbidity); // Print top turbidity reading

    // Check if water is turbid based on the threshold
    if (bottomTurbidity > TURBIDITY_THRESHOLD || topTurbidity > TURBIDITY_THRESHOLD)
    {
        waterTurbid = true;
        Serial.println("Water is turbid. Activating disposal system.");
        handleTurbidWater(); // Handle turbid water disposal
    }
    else
    {
        waterTurbid = false;
        Serial.println("Water is clear.");
        handleClearWater(); // Handle clear water state
    }
    delay(1000); // Delay for 1 second before the next loop iteration
}

void handleTurbidWater()
{
    Serial.println("Turbid water detected - diverting to disposal tank.");

    // Open turbid water disposal valve and tap valve two and close reservoir valve and tap valve one
    digitalWrite(DISPOSAL_VALVE, HIGH);
    digitalWrite(TAP_VALVE_TWO, HIGH);

    digitalWrite(RESERVOIR_VALVE, LOW);
    digitalWrite(TAP_VALVE_ONE, LOW);
}

void handleClearWater()
{
    Serial.println("Clear water detected - diverting to reservoir.");

    // Open reservoir valve and tap valve one and close disposal valve and tap valve two
    digitalWrite(RESERVOIR_VALVE, HIGH);
    digitalWrite(TAP_VALVE_ONE, HIGH);

    digitalWrite(DISPOSAL_VALVE, LOW);
    digitalWrite(TAP_VALVE_TWO, LOW);
}

void closeAllValves()
{
    // Close all valves at startup
    digitalWrite(RESERVOIR_VALVE, LOW);
    digitalWrite(DISPOSAL_VALVE, LOW);
    digitalWrite(TAP_VALVE_ONE, LOW);
    digitalWrite(TAP_VALVE_TWO, LOW);
}
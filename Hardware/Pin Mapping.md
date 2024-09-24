| OpenPLC | Pico GPIO | Pico Pin |     | Purpose      |
|---------|-----------|----------|-----|--------------|
| Relay Outputs |
| QX0.0   | GP21      | 27       | → | Pump Power   |
| QX0.1   | GP20      | 26       | → | Motor Power  |
| QX0.2   | GP19      | 25       | → | White Pusher |
| QX0.3   | GP18      | 24       | → | Red Pusher   |
| QX0.4   | GP17      | 22       | → | Blue Pusher  |
| QX0.5   | GP16      | 21       | → |              |
| QX0.6   | GP15      | 20       | → |              |
| QX0.7   | GP14      | 19       | → |              |
| Main Inputs |
| IX0.0   | GP6       | 9        | ← |                        |
| IX0.1   | GP7       | 10       | ← |                        |
| IX0.2   | GP8       | 11       | ← | Incoming Light Barrier |
| IX0.3   | GP9       | 12       | ← |                        |
| IX0.4   | GP10      | 14       | ← | Rotary Encoder         |
| IX0.5   | GP11      | 15       | ← | Outgoing Light Barrier |
| IX0.6   | GP12      | 16       | ← |                        |
| IX0.7   | GP13      | 17       | ← |                        |
| IO Expander |
| -       | MCP.GP0   | -        | → | Colour LED R |
| -       | MCP.GP1   | -        | → | Colour LED B |
| -       | MCP.GP2   | -        | → | Colour LED G |
| -       | MCP.GP3   | -        | → | Status LED R |
| -       | MCP.GP4   | -        | → | Status LED B |
| -       | MCP.GP5   | -        | → | Status LED G |
| -       | MCP.GP6   | -        | ← | Green Button |
| -       | MCP.GP7   | -        | ← | Red Button   |
| Other |				
| I2C SDA | GP0       | 1        | ↔ | MCP IO Expander |
| I2C SCL | GP1       | 2        | → | MCP IO Expander |
| IW0     | GP26      | 31       | ← | Colour Sensor   |
| IW1     | GP27      | 32       | ← |                 |
| IW2     | GP28      | 34       | ← |                 |
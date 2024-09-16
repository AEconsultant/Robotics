# modbusBitBridge

### This scrip can be used to bridge M bit data between 2 Elite EC robots.

- It is intended to run on the master robot.
- Dont forget to setup the slave robot as a modbus slave.
- the example code gets data from master robot M variables and writes it to the slave variables of the same number.
    - Note that this is not mandatory and the M addresses may change
- Master robot is reading slave variables and writing them the its own M adress.
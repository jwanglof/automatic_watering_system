"use strict";

/**
 *
 */
class Resistance {
  /**
   * Create a resistance
   * @param readValue
   */
  constructor (readValue) {
    this.readValue = readValue;
  }

  /**
   * Get the resistance of an analog read
   * @returns {number}
   */
  get analogResistance () {
    return (1023 - this.readValue) / this.readValue;
  }

  /**
   * Get the resistance of an analog read, with a 10 bit value
   * @returns {number}
   */
  get analogResistance10Bit () {
    return (1023 - this.readValue) * 10000 / this.readValue;
  }

  get digitalResistance () {
    return null;
  }
}

module.exports = Resistance;
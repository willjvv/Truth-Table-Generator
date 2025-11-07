# Truth-Table-Generator
A web-based tool to generate truth tables for logical expressions. Simply open `truth_table_gen.html` in your browser, enter an expression, and see the resulting truth table.

# Supported Operators
*   `~` (NOT / Tilde)
*   `&` (AND / Ampersand)
*   `v` (OR / Wedge)
*   `→` (IMPLIES / Arrow)
*   `↔` (IFF / Double Arrow)

**Note:** Variables must be uppercase letters (e.g., P, Q, R). All binary operations must be enclosed in parentheses, for example `(P & Q)`.

# Examples
Expression: `(P & Q)`

+----+----+---------+

| P  | Q  | (P & Q) |

+----+----+---------+

| T  | T  |    T    |

| T  | F  |    F    |

| F  | T  |    F    |

| F  | F  |    F    |

+----+----+---------+


Expression: `(P v Q)`

+----+----+---------+

| P  | Q  | (P v Q) |

+----+----+---------+

| T  | T  |    T    |

| T  | F  |    T    |

| F  | T  |    T    |

| F  | F  |    F    |

+----+----+---------+


Expression: `(~P)`

+---+------+

| P | (~P) |

+---+------+

| T |  F   |

| F |  T   |

+---+------+


Expression: `(P → Q)`

+----+----+---------+

| P  | Q  | (P → Q) |

+----+----+---------+

| T  | T  |    T    |

| T  | F  |    F    |

| F  | T  |    T    |

| F  | F  |    T    |

+----+----+---------+


Expression: `((P & Q) v (~R))`

+---+---+---+-----------------+

| P | Q | R | ((P & Q) v (~R)) |

+---+---+---+-----------------+

| T | T | T |        T        |

| T | T | F |        T        |

| T | F | T |        F        |

| T | F | F |        T        |

| F | T | T |        F        |

| F | T | F |        T        |

| F | F | T |        F        |

| F | F | F |        T        |

+---+---+---+-----------------+

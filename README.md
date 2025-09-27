# Truth-Table-Generator
Input a logical expression in LaTeX format and the program will calculate and display its truth table.

# Supported Operators
- \land (and)
- \lor (or)
- \lnot (not)
- \rightarrow (implies)
- \leftrightarrow (iff)

# Examples
Expression: p \land q
+----+----+-----------+
| p  | q  | p \land q |
+----+----+-----------+
| F  | F  |     F     |
| F  | T  |     F     |
| T  | F  |     F     |
| T  | T  |     T     |
+----+----+-----------+

Expression: p \lor q
+----+----+----------+
| p  | q  | p \lor q |
+----+----+----------+
| F  | F  |    F     |
| F  | T  |    T     |
| T  | F  |    T     |
| T  | T  |    T     |
+----+----+----------+

Expression: \lnot p
+----+---------+
| p  | \lnot p |
+----+---------+
| F  |    T    |
| T  |    F    |
+----+---------+

Expression: p \rightarrow q
+----+----+-----------------+
| p  | q  | p \rightarrow q |
+----+----+-----------------+
| F  | F  |        T        |
| F  | T  |        T        |
| T  | F  |        F        |
| T  | T  |        T        |
+----+----+-----------------+

Expression: p \leftrightarrow q
+----+----+---------------------+
| p  | q  | p \leftrightarrow q |
+----+----+---------------------+
| F  | F  |          T          |
| F  | T  |          F          |
| T  | F  |          F          |
| T  | T  |          T          |
+----+----+---------------------+

Expression: (p \land q) \lor \lnot r
+----+----+----+--------------------------+
| p  | q  | r  | (p \land q) \lor \lnot r |
+----+----+----+--------------------------+
| F  | F  | F  |            T             |
| F  | F  | T  |            F             |
| F  | T  | F  |            T             |
| F  | T  | T  |            F             |
| T  | F  | F  |            T             |
| T  | F  | T  |            F             |
| T  | T  | F  |            T             |
| T  | T  | T  |            T             |
+----+----+----+--------------------------+

Expression: p \land (q \lor r)
+----+----+----+--------------------+
| p  | q  | r  | p \land (q \lor r) |
+----+----+----+--------------------+
| F  | F  | F  |         F          |
| F  | F  | T  |         F          |
| F  | T  | F  |         F          |
| F  | T  | T  |         F          |
| T  | F  | F  |         F          |
| T  | F  | T  |         T          |
| T  | T  | F  |         T          |
| T  | T  | T  |         T          |
+----+----+----+--------------------+

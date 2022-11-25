 transitionSystemFromCircuit(numberOfInputs, numberOfRegisters, numberOfOutputs, updateRegisters, computeOutputs)

המקבלת את מספר הקלטים, מספר האוגרים, את מספר הפלטים ואת פונקציות העדכון ויצירת הפלט שהגדרנו בהרצאה ומחזירה מערכת מעברים כפי שהגדרנו, בפורמט שבו השתמשנו בתרגילים הקודמים.

לדוגמה: עבור המערכת המניה שהגדרנו בשקף מספר 9 בהרצאה הקריאה לפונקציה תראה כך:

transitionSystemFromCircuit(1, 2, 1, lambda s: ((s[2] and s[1]) ^ s[0], s[2] ^ s[1]), lambda s: (s[0] and s[1] and s[2],))

והפלט יהיה:

{'S': {(False, False, False), (True, True, False), (False, True, False), (True, False, True), (False, False, True), (True, True, True), (False, True, True), (True, False, False)},
'I': {(False, False, False), (False, False, True)},
'Act': {(True,), (False,)},
'to': {((False, True, False), (False,), (False, True, False)), ((True, True, True), (False,), (False, False, False)), ((True, True, True), (True,), (False, False, True)), ((False, True, True), (False,), (True, False, False)), ((True, False, False), (False,), (True, False, False)), ((True, True, False), (True,), (True, True, True)), ((True, False, True), (True,), (True, True, True)), ((True, True, False), (False,), (True, True, False)), ((False, True, True), (True,), (True, False, True)), ((True, False, True), (False,), (True, True, False)), ((False, True, False), (True,), (False, True, True)), ((False, False, False), (True,), (False, False, True)), ((False, False, True), (True,), (False, True, True)), ((False, False, True), (False,), (False, True, False)), ((True, False, False), (True,), (True, False, True)), ((False, False, False), (False,), (False, False, False))},
'AP': {'r2', 'y1', 'x1', 'r1'},
'L': <function>}

שימו לב שפורמט המצבים הוא (r1, r2, ..., rn, x1, x2, ..., xm)


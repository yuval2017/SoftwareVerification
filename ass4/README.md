
transition_system_from_program_graph(pg, vars, labels)

המקבלת גרף תוכנית מהצורה המופיעה בקובץ שבקישור בשם PG, מילון בשם vars המגדיר את שמות המשתנים ואת הערכים שיכול לקבל כל משתנה וקבוצה labels של תנאים שישמשו לתיוג (תיוג מצב יכיל תנאי מהרשימה אם ורק אם התנאי מתקיים במצב). כפי שמופיע בדוגמה בקובץ שבקישור (המכיל גם הדפסה בפורמט שניתן להעתיק לאתר https://dreampuf.github.io/GraphvizOnline לנוחיותכם).  הפונקציה מחזירה מערכת מעברים, בפורמט שעבדנו איתו בתרגילים הקודמים, המייצגת את פרישת גרף התוכנית כפי שלמדנו. הניחו שהקלט שהתוכנית שלכם מקבלת הוא תקין.

ככל הנראה תרצו להשתמש ב-HashableDict לצורך מימוש קבוצת המצבים:
class HashableDict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))

הנחיה חשובה: כפי שדיברנו בהרצאה, אין טעם לפרוש את המצבים שאינם נגישים במערכת המעברים. מערכת המעברים שתוחזר אמורה להכיל רק מצבים נגישים. הדרך לעשות זאת היא לפרוש את המצבים והמעברים ב-DFS. להתחיל ממצבי ההתחלה, לעבור לעוקבים שלהם, לעוקבים של העוקבים,..., עד שלא מוצאים מצבים חדשים.

קלט לדוגמה:
def evaluate(cond, eta):
    return {
        'true': lambda eta: True,
        'ncoke > 0': lambda eta: eta['ncoke'] > 0,
        'nsprite > 0': lambda eta: eta['nsprite'] > 0,
        'ncoke=0 && nsprite=0': lambda eta: eta['ncoke'] == 0 and eta['nsprite'] == 0,
        'ncoke=2 && nsprite=2': lambda eta: eta['ncoke'] == 2 and eta['nsprite'] == 2,
    }[cond](eta)

def effect(act, eta):
    return {
        'coin': lambda eta: eta,
        'ret_coin': lambda eta: eta,
        'refill': lambda eta: {'ncoke': 2, 'nsprite': 2},
        'get_coke': lambda eta: {**eta, 'ncoke': eta['ncoke'] - 1},
        'get_sprite': lambda eta: {**eta, 'nsprite': eta['nsprite'] - 1},
    }[act](eta)

pg = {
    'Loc': {'start', 'select'},
    'Loc0': {'start'},
    'Act': {'coin', 'refill', 'get_coke', 'get_sprite', 'ret_coin'},
    'Eval': evaluate,
    'Effect': effect,
    'to': {
        ('start', 'true', 'coin', 'select'),
        ('start', 'true', 'refill', 'start'),
        ('select', 'ncoke > 0', 'get_coke', 'start'),
        ('select', 'nsprite > 0', 'get_sprite', 'start'),
        ('select', 'ncoke=0 && nsprite=0', 'ret_coin', 'start')
    },
    'g0': "ncoke=2 && nsprite=2",
}

vars = {'ncoke': range(3), 'nsprite': range(3)}

labels = {"ncoke > 0", "nsprite > 0"}

הפלט:
{'S': {('select', {'ncoke': 1, 'nsprite': 1}), ('select', {'ncoke': 2, 'nsprite': 2}), ('start', {'ncoke': 2, 'nsprite': 0}), ('start', {'ncoke': 1, 'nsprite': 1}), ('select', {'ncoke': 1, 'nsprite': 0}),
       ('start', {'ncoke': 2, 'nsprite': 2}), ('select', {'ncoke': 2, 'nsprite': 1}), ('start', {'ncoke': 1, 'nsprite': 0}), ('start', {'ncoke': 2, 'nsprite': 1}), ('select', {'ncoke': 0, 'nsprite': 2}),
       ('start', {'ncoke': 0, 'nsprite': 2}), ('select', {'ncoke': 1, 'nsprite': 2}), ('start', {'ncoke': 1, 'nsprite': 2}), ('select', {'ncoke': 0, 'nsprite': 1}), ('start', {'ncoke': 0, 'nsprite': 1}),
       ('select', {'ncoke': 0, 'nsprite': 0}), ('start', {'ncoke': 0, 'nsprite': 0}), ('select', {'ncoke': 2, 'nsprite': 0})},
 'Act': {'refill', 'coin', 'get_sprite', 'ret_coin', 'get_coke'},
 'to': {(('select', {'ncoke': 2, 'nsprite': 2}), 'get_sprite', ('start', {'ncoke': 2, 'nsprite': 1})), (('start', {'ncoke': 2, 'nsprite': 0}), 'refill', ('start', {'ncoke': 2, 'nsprite': 2})),
        (('select', {'ncoke': 2, 'nsprite': 2}), 'get_coke', ('start', {'ncoke': 1, 'nsprite': 2})), (('start', {'ncoke': 0, 'nsprite': 2}), 'refill', ('start', {'ncoke': 2, 'nsprite': 2})),
        (('start', {'ncoke': 1, 'nsprite': 0}), 'coin', ('select', {'ncoke': 1, 'nsprite': 0})), (('select', {'ncoke': 0, 'nsprite': 1}), 'get_sprite', ('start', {'ncoke': 0, 'nsprite': 0})),
        (('select', {'ncoke': 0, 'nsprite': 0}), 'ret_coin', ('start', {'ncoke': 0, 'nsprite': 0})), (('select', {'ncoke': 0, 'nsprite': 2}), 'get_sprite', ('start', {'ncoke': 0, 'nsprite': 1})),
        (('select', {'ncoke': 1, 'nsprite': 1}), 'get_sprite', ('start', {'ncoke': 1, 'nsprite': 0})), (('start', {'ncoke': 1, 'nsprite': 0}), 'refill', ('start', {'ncoke': 2, 'nsprite': 2})),
        (('start', {'ncoke': 1, 'nsprite': 1}), 'refill', ('start', {'ncoke': 2, 'nsprite': 2})), (('start', {'ncoke': 2, 'nsprite': 2}), 'coin', ('select', {'ncoke': 2, 'nsprite': 2})),
        (('start', {'ncoke': 2, 'nsprite': 1}), 'refill', ('start', {'ncoke': 2, 'nsprite': 2})), (('start', {'ncoke': 0, 'nsprite': 1}), 'coin', ('select', {'ncoke': 0, 'nsprite': 1})),
        (('select', {'ncoke': 1, 'nsprite': 2}), 'get_coke', ('start', {'ncoke': 0, 'nsprite': 2})), (('start', {'ncoke': 1, 'nsprite': 2}), 'coin', ('select', {'ncoke': 1, 'nsprite': 2})),
        (('start', {'ncoke': 2, 'nsprite': 1}), 'coin', ('select', {'ncoke': 2, 'nsprite': 1})), (('start', {'ncoke': 1, 'nsprite': 2}), 'refill', ('start', {'ncoke': 2, 'nsprite': 2})),
        (('start', {'ncoke': 0, 'nsprite': 0}), 'coin', ('select', {'ncoke': 0, 'nsprite': 0})), (('select', {'ncoke': 1, 'nsprite': 1}), 'get_coke', ('start', {'ncoke': 0, 'nsprite': 1})),
        (('select', {'ncoke': 2, 'nsprite': 0}), 'get_coke', ('start', {'ncoke': 1, 'nsprite': 0})), (('select', {'ncoke': 1, 'nsprite': 0}), 'get_coke', ('start', {'ncoke': 0, 'nsprite': 0})),
        (('select', {'ncoke': 1, 'nsprite': 2}), 'get_sprite', ('start', {'ncoke': 1, 'nsprite': 1})), (('start', {'ncoke': 0, 'nsprite': 1}), 'refill', ('start', {'ncoke': 2, 'nsprite': 2})),
        (('start', {'ncoke': 1, 'nsprite': 1}), 'coin', ('select', {'ncoke': 1, 'nsprite': 1})), (('select', {'ncoke': 2, 'nsprite': 1}), 'get_coke', ('start', {'ncoke': 1, 'nsprite': 1})),
        (('start', {'ncoke': 2, 'nsprite': 0}), 'coin', ('select', {'ncoke': 2, 'nsprite': 0})), (('select', {'ncoke': 2, 'nsprite': 1}), 'get_sprite', ('start', {'ncoke': 2, 'nsprite': 0})),
        (('start', {'ncoke': 0, 'nsprite': 0}), 'refill', ('start', {'ncoke': 2, 'nsprite': 2})), (('start', {'ncoke': 0, 'nsprite': 2}), 'coin', ('select', {'ncoke': 0, 'nsprite': 2})),
        (('start', {'ncoke': 2, 'nsprite': 2}), 'refill', ('start', {'ncoke': 2, 'nsprite': 2}))},
 'I': {('start', {'ncoke': 2, 'nsprite': 2})},
 'AP': {'ncoke > 0', 'start', 'nsprite > 0', 'select'},
 'L': <function _transition_system_from_program_graph.<locals>.<lambda> at 0x0000021E758DA160>}


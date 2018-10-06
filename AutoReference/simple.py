sq="'"
tq='"""'
program="""print('sq="%s"' % sq)
print('tq=%s%s%s' % (sq, tq, sq))
print('program=%s%s%s' % (tq, program, tq))
print(program)
"""
print('sq="%s"' % sq)
print('tq=%s%s%s' % (sq, tq, sq))
print('program=%s%s%s' % (tq, program, tq))
print(program)


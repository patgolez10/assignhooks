
class SampleClass():
    name = ''
    cnt = 0

    def __assignpre__(self, lhs_name, rhs_name, rhs):
        print('PRE: assigning %s = %s' % (lhs_name, rhs_name))
        print('PRE: rhs=', rhs)
        # can return rhs or any function of it if desired
        self.cnt += 1
        return rhs

    def __assignpost__(self, lhs_name, rhs_name):
        print('POST: lhs', self)
        print('POST: assigning %s = %s' % (lhs_name, rhs_name))
        self.name = f"{lhs_name}"


def fun():
    print('-- before assign to a')
    a = 1
    print('a', a)

    print('-- before assign to b')
    b = SampleClass()
    print('b.name', repr(b.name))
    print('b.cnt', b.cnt)
    assert b.cnt == 0

    print('-- before assign to c')
    c = b
    print('c.name', repr(c.name))
    print('c.cnt', c.cnt)
    assert c.cnt == 0

    print('-- before assing to d')
    d = c
    print('d.name', repr(d.name))
    print('d.cnt', d.cnt)
    assert d.cnt == 0

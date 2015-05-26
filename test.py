def test(**kw):
    params = dict(user='root', password='5088794')
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.iteritems():
        te = kw.pop(k, v)
        params[k] = te
    return params
def test2(**kw):
    params = dict(user='root', password='5088794')
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.iteritems():
        print
        params[k] = kw.pop(k)
    return params
if __name__ == '__main__':
    t = test(test='test', charset='utf9')
    #t2 = test2(test='test', charset='utf9')
    print t
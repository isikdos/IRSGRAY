from sqlalchemy.orm.exc import NoResultFound
import datetime

def Get_One_Or_Create(session,
                      model,
                      create_method='',
                      create_method_kwargs=None,
                      **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        session.add(created)
        return created, True

def Date_2_Int(date):
    return int(date.strftime('%s'))

def Int_2_Date(dateint):
    return datetime.datetime.fromtimestamp(dateint)

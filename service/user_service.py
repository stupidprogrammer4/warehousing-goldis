from database.uow import user_repo
from typing import Dict
import bcrypt
from config import SALT


async def login(username: str, password: str) -> Dict:
    resp = {'status': 200, 'message': ''}
    try:
        login_err = False
        user = await user_repo.get_by_username(username)
        if user is None:
            login_err = True
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), SALT).decode('utf8')
            if hashed_password != user.password:
                login_err = True
        if login_err:
            resp['status'] = 400
            resp['message'] = 'اطلاعات کاربری نادرست است'
        else:
            resp['backurl'] = '/dashboard'
    except Exception as err:
        resp['status'] = 500
        resp['message'] = 'خطای سرور: {}'.format(err)
    
    return resp
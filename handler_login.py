import template
from dbapi.user import User


def check_login(username, password):
    result = User.find('username', username)
    if not result:
        return None
    else:
        user = result[0]
    if user is not None and username == user.username and password == user.password:
        return user
    return None


def login(response):
    response.write('''
        <!doctype html>
        <html>
            <head>
            </head>
            <body>
                <h1>Hello!</h1>
                <form action='/authenticate' method="POST">
                    <label>Username:
                        <input type='text' name='username'>
                    </label>
                    <p><label>Password:
                        <input type='password' name='password'>
                    </label>
                    <p><input type='submit' value='login'>
                </form>
            </body>
        </html>''')

def authenticate(response):
    username = response.get_field('username')
    password = response.get_field('password')
    if check_login(username, password) or response.get_secure_cookie('username'):
        response.set_secure_cookie('username', username)
        response.redirect('/user/{}'.format(username))

    else:
        response.write('''
            <!doctype html>
            <html>
                <head>
                </head>
                <body>
                    <p>Incorrect username or password, or username and password.</p>
                </body>
            </html>''')

def logout(response):
    response.clear_cookie('username')
    response.redirect('/')

def changepassword(response):
    old_password = response.get_field('old password')
    new_password_1 = response.get_field('new password 1')
    new_password_2 = response.get_field('new password 2')
    username = str(response.get_secure_cookie('username'), 'utf-8')
    if new_password_1 == new_password_2:
        user = check_login(username, old_password)
        if user is not None:
            user.update('password', new_password_1)
            response.write('''
                <!doctype html>
                <html>
                    <head>
                    </head>
                    <body>
                        <p>Password seems to have changed.</p>
                        <p><a href='/user/{}'>Home</a></p>
                    </body>
                </html>'''.format(username))
        else:
            response.write('''
                <!doctype html>
                <html>
                    <head>
                    </head>
                    <body>
                        <p>Old password is incorrect.</p>
                        <p><form action='/changepassword'>
                            <label>Old password:
                                <input type='text' name='old password'>
                            </label>
                            <p><label>New password:
                                <input type='password' name='new password 1'>
                            </label>
                            <p><label>New password:
                                <input type='password' name='new password 2'>
                            </label>
                            <p><input type='submit' value='change password'>
                        </form>
                        <p><a href='/'>Home</a></p>
                    </body>
                </html>''')
    else:
        response.write('''
            <!doctype html>
            <html>
                <head>
                </head>
                <body>
                    <p>Passwords do not match.</p>
                    <p><form action='/changepassword'>
                        <label>Old password:
                            <input type='text' name='old password'>
                        </label>
                        <p><label>New password:
                            <input type='password' name='new password 1'>
                        </label>
                        <p><label>New password:
                            <input type='password' name='new password 2'>
                        </label>
                        <p><input type='submit' value='change password'>
                    </form>
                    <p><a href='/'>Home</a></p>
                </body>
            </html>''')

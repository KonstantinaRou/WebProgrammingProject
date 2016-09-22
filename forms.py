import re

class RegistrationForm:
    
    EMAIL_REGEX =re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

    def __init__(self, email, password, repassword):
        self.email = email
        self.password = password
        self.repassword = repassword

    def validate(self):
        errors = {}
        if not self.email:
            errors['email']= "This field is required"
        elif not self.EMAIL_REGEX.match(self.email):
            errors['email']= "Plerase enter a valid email address"
        if not self.password:
            errors['password']= "This field is required"    
        else:
            password_length = len(self.password)
            if password_length < 4 or password_length>10: 
                errors['password'] = "Password must be between 4 and 10 characters "
        if not self.repassword:
            errors['repassword']= "This field is required"
        elif self.repassword!=self.password:
            errors['repassword']="Passwords must match"
        return errors


class ProfileForm:
    
    LETTERSONLY_REGEX =re.compile('^[a-zA-Z]+$')
    DATE_REGEX = re.compile('(^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$)')
    URL_REGEX=re.compile('\(?(?:(http|https):\/\/)?(?:((?:[^\W\s]|\.|-|[:]{1})+)@{1})?((?:www.)?(?:[^\W\s]|\.|-)+[\.][^\W\s]{2,4}|localhost(?=\/)|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::(\d*))?([\/]?[^\s\?]*[\/]{1})*(?:\/?([^\s\n\?\[\]\{\}\#]*(?:(?=\.)){1}|[^\s\n\?\[\]\{\}\.\#]*)?([\.]{1}[^\s\?\#]*)?)?(?:\?{1}([^\s\n\#\[\]]*))?([\#][^\s\n]*)?\)?')

    def __init__(self, name, surname,birthdate,website):
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.website=website

    def validate(self):
        errors = {}
        if not self.name:
            errors['name']= "This field is required"
        elif not self.LETTERSONLY_REGEX.match(self.name):
            errors['name']= "Names should contain only letters"
        if not self.surname:
            errors['surname']= "This field is required" 
        elif not self.LETTERSONLY_REGEX.match(self.surname):
            errors['surname']= "Surnames should contain only letters"
        
        if self.birthdate and not self.DATE_REGEX.match(self.birthdate):
            errors['birthdate']= "Invalid date format. DD/MM/YYYY"
        if self.website and not self.URL_REGEX.match(self.website):
            errors['website']="Invalid website format."
        return errors

class LoginValidate:
    def __init__(self,email,password):
        self.email = email
        self.password=password

    def validate(self):
        errors={}
        if not self.email:
            errors['email']= "This field is required to log in"
        elif not self.password:
            errors['password']= "This field is required to log in" 
        return errors

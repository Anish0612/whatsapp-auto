class Country_Code_Exception(Exception):
    """
    Country Code is not present in the Phone Number
    """
    pass

class Invalid_Phone_Number(Exception):
    """
    Phone number given is invalid
    """
    pass

class Login_Failed(Exception):
    """"
    Whatsapp Login Failed
    """

class Invalid_Group_Link(Exception):
    """
    Group link given is invalid
    """
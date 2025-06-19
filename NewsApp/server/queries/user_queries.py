GET_USER_BY_EMAIL = """
    SELECT Id, Email, Username, PasswordHash, Role
    FROM Users
    WHERE Email = ?
"""

CREATE_USER = """
    INSERT INTO Users (Username, Email, PasswordHash)
    VALUES (?, ?, ?)
"""

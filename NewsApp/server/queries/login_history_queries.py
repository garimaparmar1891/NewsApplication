RECORD_LOGIN = """
    INSERT INTO LoginHistory (UserId)
    VALUES (?)
"""

GET_LAST_LOGIN = """
    SELECT TOP 1 LoginTime 
    FROM LoginHistory 
    WHERE UserId = ? 
    ORDER BY LoginTime DESC
"""

GET_CATEGORY_BY_NAME = """
    SELECT Id, Name FROM Categories WHERE Name = ?
"""

GET_CATEGORIES = """
    SELECT Id, Name FROM Categories ORDER BY Name
"""

GET_CATEGORY_IS_HIDDEN = """
    SELECT IsHidden FROM Categories WHERE Id = ?
"""

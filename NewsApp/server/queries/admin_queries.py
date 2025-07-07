GET_EXTERNAL_SERVERS = """
    SELECT Id, Name, ApiKey, BaseUrl, IsActive, LastAccessed
    FROM ExternalServers
    ORDER BY Name
"""

GET_ACTIVE_EXTERNAL_SERVERS = """
    SELECT Id, Name, ApiKey, BaseUrl, IsActive, LastAccessed
    FROM ExternalServers
    WHERE IsActive = 1
    ORDER BY Name
"""

UPDATE_EXTERNAL_SERVER = """
    UPDATE ExternalServers
    SET {fields}
    WHERE Id = ?
"""

INSERT_CATEGORY = """
    INSERT INTO Categories (Name)
    VALUES (?)
"""

GET_ALL_KEYWORDS = """
    SELECT Id, Word, CategoryId
    FROM Keywords
    ORDER BY Word
"""

INSERT_KEYWORD = """
    INSERT INTO Keywords (Word, CategoryId)
    VALUES (?, ?)
"""

DELETE_KEYWORD = """
    DELETE FROM Keywords 
    WHERE LOWER(Word) = LOWER(?)
"""

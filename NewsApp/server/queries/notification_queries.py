GET_LAST_LOGIN = """
SELECT TOP 1 LoginTime
FROM LoginHistory
WHERE UserId = ?
ORDER BY LoginTime DESC
"""

GET_NOTIFICATIONS_SINCE = """
SELECT Id, Message, CreatedAt
FROM Notifications
WHERE UserId = ? AND CreatedAt > ?
ORDER BY CreatedAt DESC
"""

def MARK_NOTIFICATIONS_READ(n):
    return f"""
    UPDATE Notifications
    SET IsRead = 1
    WHERE Id IN ({','.join(['?'] * n)})
    """

UPSERT_NOTIFICATION_PREF = """
MERGE NotificationPreferences AS target
USING (SELECT ? AS UserId, ? AS CategoryId) AS source
ON target.UserId = source.UserId AND target.CategoryId = source.CategoryId
WHEN MATCHED THEN
    UPDATE SET IsEnabled = ?
WHEN NOT MATCHED THEN
    INSERT (UserId, CategoryId, IsEnabled)
    VALUES (?, ?, ?);

"""

GET_ENABLED_CATEGORIES = """
SELECT np.CategoryId
FROM NotificationPreferences np
JOIN Categories c ON np.CategoryId = c.Id
WHERE np.UserId = ? AND np.IsEnabled = 1 AND c.IsHidden = 0
"""

GET_USER_KEYWORDS = """
SELECT CategoryId, Keyword
FROM UserKeywords
WHERE UserId = ?
"""

CHECK_USER_KEYWORD_EXISTS = """
SELECT 1
FROM UserKeywords
WHERE UserId = ? AND CategoryId = ? AND LOWER(Keyword) = LOWER(?)
"""

INSERT_USER_KEYWORD = """
INSERT INTO UserKeywords (UserId, CategoryId, Keyword)
VALUES (?, ?, ?)
"""

GET_UNSENT_ARTICLES = """
SELECT A.Id, A.Title, A.Content, A.CategoryId, A.PublishedAt, A.Source, A.Url
FROM Articles A
LEFT JOIN SentNotifications SN ON A.Id = SN.ArticleId AND SN.UserId = ?
JOIN Categories C ON A.CategoryId = C.Id
WHERE A.CategoryId = ?
  AND SN.Id IS NULL
  AND C.IsHidden = 0
  AND (
        LOWER(A.Title) LIKE ?
        OR LOWER(A.Content) LIKE ?
      )
ORDER BY A.PublishedAt DESC
"""

MARK_ARTICLE_AS_SENT = """
INSERT INTO SentNotifications (UserId, ArticleId)
SELECT ?, ?
WHERE NOT EXISTS (
    SELECT 1 FROM SentNotifications WHERE UserId = ? AND ArticleId = ?
)
"""

GET_USERS_WITH_PREFS = """
SELECT DISTINCT U.Id, U.Email, U.Username
FROM Users U
JOIN NotificationPreferences NP ON U.Id = NP.UserId
WHERE NP.IsEnabled = 1
"""

GET_USER_PREFERENCES = """
SELECT np.CategoryId, c.Name AS CategoryName, np.IsEnabled
FROM NotificationPreferences np
JOIN Categories c ON np.CategoryId = c.Id
WHERE np.UserId = ? AND c.IsHidden = 0
"""

GET_UNREAD_NOTIFICATIONS = """
SELECT N.Id, N.ArticleId, N.Message, N.CreatedAt, A.Title, A.Source
FROM Notifications N
JOIN Articles A ON N.ArticleId = A.Id
JOIN Categories C ON A.CategoryId = C.Id
WHERE N.UserId = ? AND N.IsRead = 0 AND C.IsHidden = 0
ORDER BY N.CreatedAt DESC
"""

MARK_NOTIFICATIONS_AS_READ = """
UPDATE Notifications
SET IsRead = 1
WHERE UserId = ? AND IsRead = 0
"""

INSERT_NOTIFICATION = """
INSERT INTO Notifications (UserId, ArticleId, Message, IsRead, CreatedAt)
VALUES (?, ?, ?, 0, GETDATE())
"""

GET_ARTICLES_BY_CATEGORIES = """
SELECT A.Id, A.Title, A.Content, A.CategoryId, A.PublishedAt, A.Source, A.Url
FROM Articles A
JOIN Categories C ON A.CategoryId = C.Id
LEFT JOIN SentNotifications SN ON A.Id = SN.ArticleId AND SN.UserId = ?
WHERE A.CategoryId IN ({placeholders}) AND SN.Id IS NULL AND C.IsHidden = 0
ORDER BY A.PublishedAt DESC
"""

from constants.messages import (
    INPUT_CANNOT_BE_EMPTY,
    PLEASE_ENTER_VALID_NUMBER,
    PLEASE_ENTER_VALID_ID,
    PLEASE_ENTER_VALID_ACTION,
    ENTER_ARTICLE_ID_PROMPT,
    ENTER_KEYWORD_PROMPT,
    ENTER_START_DATE_PROMPT,
    ENTER_END_DATE_PROMPT
)

def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print(INPUT_CANNOT_BE_EMPTY)

def get_valid_integer_input(prompt, valid_ids=None):
    while True:
        user_input = input(prompt).strip()
        if not user_input.isdigit():
            print(PLEASE_ENTER_VALID_NUMBER)
            continue
        
        user_id = int(user_input)
        if valid_ids is not None and user_id not in valid_ids:
            print(PLEASE_ENTER_VALID_ID)
            continue
            
        return user_id

def get_valid_action_input(prompt, valid_actions):
    while True:
        user_input = input(prompt).lower().strip()
        if user_input in valid_actions:
            return user_input
        print(PLEASE_ENTER_VALID_ACTION.format(', '.join(valid_actions)))

def get_article_id_input(action):
    return input(ENTER_ARTICLE_ID_PROMPT.format(action)).strip()

def get_search_input():
    keyword = get_non_empty_input(ENTER_KEYWORD_PROMPT)
    start_date = input(ENTER_START_DATE_PROMPT).strip()
    end_date = input(ENTER_END_DATE_PROMPT).strip()
    return keyword, start_date, end_date 

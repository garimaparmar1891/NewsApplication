from utils.header import print_welcome_message
from utils.token_storage import clear_token
from utils.http_client import authorized_request
from utils.read_article import read_article
from utils.endpoints import (
    SAVE_ARTICLE,
    REPORT_ARTICLE
)

ITEMS_PER_PAGE = 5

def interactive_paginated_menu(articles, context_label="Articles"):
    page = 0
    total_pages = (len(articles) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    while True:
        print_welcome_message()
        start_index, end_index = print_articles_page(articles, page, context_label)
        print(f"Page {page + 1} of {total_pages}")
        print("\nOptions:")
        print("1. Read article by ID")
        print("2. Save article by ID")
        print("3. Next page")
        print("4. Previous page")
        print("5. Go back to main menu")
        print("6. Logout")
        print("7. Report article by ID")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            article_id_input = prompt_article_id("read")
            if article_id_input.isdigit():
                article_id = int(article_id_input)
                article = next((a for a in articles if a["Id"] == article_id), None)
                if article:
                    read_article(article)
                else:
                    print("Article ID not found.")
            else:
                print("Invalid input. Please enter a valid numeric article ID.")

        elif choice == "2":
            article_id_input = prompt_article_id("save")
            if article_id_input.isdigit():
                article_id = int(article_id_input)
                article = next((a for a in articles if a["Id"] == article_id), None)
                if article:
                    save_article(article_id)
                else:
                    print("Article ID not found.")
            else:
                print("Invalid input. Please enter a valid numeric article ID.")

        elif choice == "3":
            if end_index >= len(articles):
                print("You are on the last page.")
            else:
                page += 1

        elif choice == "4":
            if page == 0:
                print("You are already on the first page.")
            else:
                page -= 1

        elif choice == "5":
            break

        elif choice == "6":
            clear_token()
            print("Logged out successfully.")
            exit()

        elif choice == "7":
            article_id_input = prompt_article_id("report")
            if article_id_input.isdigit():
                article_id = int(article_id_input)
                article = next((a for a in articles if a["Id"] == article_id), None)
                if article:
                    report_article(article_id)
                else:
                    print("Article ID not found.")
            else:
                print("Invalid input. Please enter a valid numeric article ID.")

        else:
            print("Invalid choice. Please try again.")

def print_articles_page(articles, page, context_label):
    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    current_articles = articles[start_index:end_index]
    print(f"\n{context_label}:\n")
    for article in current_articles:
        print(f"(Article ID: {article.get('Id')}) → {article.get('Title')}\n")
    return start_index, end_index

def prompt_article_id(action):
    return input(f"Enter article ID to {action}: ").strip()

def save_article(article_id):
    save_resp = authorized_request("POST", SAVE_ARTICLE.format(article_id=article_id))
    if save_resp.ok:
        print("Article saved successfully.")
    else:
        print("Failed to save article:", save_resp.json().get("message", save_resp.text))

def report_article(article_id):
    reason = input("Enter reason for reporting this article: ").strip()
    if not reason:
        print("Report reason cannot be empty.")
        return
    report_resp = authorized_request("POST", REPORT_ARTICLE.format(article_id=article_id), json={"reason": reason})
    if report_resp.ok:
        print("Report submitted successfully.")
    else:
        print("Failed to report article:", report_resp.json().get("message", report_resp.text))

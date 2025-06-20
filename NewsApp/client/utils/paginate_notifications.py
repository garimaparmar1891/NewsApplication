from utils.header import print_welcome_message

def paginate_notifications(notifications, items_per_page=5):
    total = len(notifications)
    if total == 0:
        print("No notifications to display.")
        return

    page = 0
    while True:
        print_welcome_message()
        start = page * items_per_page
        end = start + items_per_page
        current_page_notifications = notifications[start:end]

        for idx, note in enumerate(current_page_notifications, start=start + 1):
            print(f"\n[{idx}] {note.get('title', 'No Title')}")
            print(f"From      : {note.get('source', 'N/A')}")
            print(f"Message   : {note.get('message', 'No message')}")
            print(f"Received  : {note.get('created_at', '')}")
            print(f"ArticleId : {note.get('article_id')}")
            print("-" * 60)

        print(f"\nShowing {start + 1}-{min(end, total)} of {total} notifications\n")
        print("1. Go to Next Page")
        print("2. Go to Previous Page")
        print("3. Go Back to Main Menu")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            if end >= total:
                print("You are on the last page.")
            else:
                page += 1

        elif choice == "2":
            if page == 0:
                print("You are already on the first page.")
            else:
                page -= 1

        elif choice == "3":
            break

        elif choice == "4":
            from utils.token_storage import clear_token
            clear_token()
            print("Logged out successfully.")
            exit()

        else:
            print("Invalid choice. Please try again.")

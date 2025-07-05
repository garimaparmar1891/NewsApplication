from features.admin.keyword.keywords_manager import KeywordsManager

class KeywordsMenu:
    """Handles the keyword management menu for admin."""

    def show(self):
        while True:
            print("\n--- Keyword Management ---")
            print("1. Add Keyword")
            print("2. Delete Keyword")
            print("3. View Keywords")
            print("4. Go to Main Menu")
            choice = input("Select an option: ").strip()

            if choice == "1":
                KeywordsManager.add_keyword()
            elif choice == "2":
                KeywordsManager.delete_keyword()
            elif choice == "3":
                KeywordsManager.view_keywords()
            elif choice == "4":
                break
            else:
                print("Invalid option. Try again.")
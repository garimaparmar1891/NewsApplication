class PrintHelpers:
    """Helper methods for admin print/display actions."""

    @staticmethod
    def print_server_list(servers):
        for idx, server in enumerate(servers, start=1):
            print(f"\n[{idx}] Server: {server.get('name')}")
            print(f"Active         : {'Yes' if server.get('is_active') else 'No'}")
            print(f"Last Accessed  : {server.get('last_accessed')}")
            print("-" * 50)

    @staticmethod
    def print_server_details(servers):
        print("\nServer Details")
        for idx, server in enumerate(servers, start=1):
            print(f"\n[{idx}] Server: {server.get('name')}")
            print(f"API Key       : {server.get('api_key')}")
            print("-" * 50)

    @staticmethod
    def print_reported_articles(reports):
        if not reports:
            print("No reports found.")
            return

        for report in reports:
            print(f"\nArticle ID   : {report['ArticleId']}")
            print(f"Reported By  : {report['Username']} ({report['Email']})")
            print(f"Reason       : {report['Reason']}")
            print("-" * 40)


    @staticmethod
    def print_result_message(success, message):
        status = "Success:" if success else "Error:"
        print(f"{status} {message}")

    @staticmethod
    def print_blocked_keywords(keywords):
        if not keywords:
            print("No blocked keywords found.")
        else:
            print("\nBlocked Keywords:")
            for kw in keywords:
                print(f" - {kw['Keyword']}")


    @staticmethod
    def print_success(message):
        print(f"Success: {message}")

    @staticmethod
    def print_error(message):
        print(f"Error: {message}")
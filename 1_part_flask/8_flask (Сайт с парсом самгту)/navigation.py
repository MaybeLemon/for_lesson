def get_nav(app):
    # all_routes = app.url_map._rules
    with app.app_context():
        nav = [
            {'name': 'Generate', 'url': '/'},
            {'name': 'Select', 'url': '/selector'},
        ]
    return nav


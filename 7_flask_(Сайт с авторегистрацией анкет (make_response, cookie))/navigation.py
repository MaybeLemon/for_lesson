def get_nav(app):
    # all_routes = app.url_map._rules
    with app.app_context():
        nav = [
            {'name': 'Authorize', 'url': '/'},
            {'name': 'Selector', 'url': '/selector'},
        ]
    return nav


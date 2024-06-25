
        tags = list(manga_tree.item(item, 'tags'))
        if 'hover' not in tags:
            tags.append('hover')
            manga_tree.item(item, tags=tuple(tags))
            manga_tree.current_item = item
    else:
        tags = list(manga_tree.item(item, 'tags'))
        if 'hover' in tags:
            tags = [i for i in tags if i != 'hover']
            manga_tree.item(item, tags=tuple(tags))
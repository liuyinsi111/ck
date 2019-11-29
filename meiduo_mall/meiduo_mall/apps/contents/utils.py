from goods.models import GoodsChannel

def get_categories():
    categories = {}
    goods_channel_qs = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel_model in goods_channel_qs:
        group_id = channel_model.group_id
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}
        cat1 = channel_model.category
        cat1.url = channel_model.url
        group_data = categories[group_id]
        cat1_list = group_data['channels']
        cat1_list.append(cat1)

        cat2_qs = cat1.subs.all()
        for cat2 in cat2_qs:
            cat3_qs = cat2.subs.all()
            cat2.sub_cats = cat3_qs
            group_data['sub_cats'].append(cat2)
    return categories
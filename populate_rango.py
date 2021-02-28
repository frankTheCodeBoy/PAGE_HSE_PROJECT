import os
os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 
        'tango_rango.settings'
    )
import django
django.setup()
from rango_app.models import Category, Page

def populate():

    fashion_pages = [
        {
            'title': "Men Classic Fashion Lifestyle", 
            'url': "https://www.menfashion.com/",
            'views': 15
        },
        {
            'title': "Real Men Real Style",
            'url': "https://www.realmenrealstyle/",
            'views': 57
        },
        {
            'title': "The Super Woman Style Guide",
            'url': "https://www.thetrendspotter.net/top-style-tips-for-women/",
            'views': 44
        },
    ]

    travel_pages = [
        {
            'title': "My 100 Best Tips From Ten Years Of Travel",
            'url': "https://www.neverendingfootsteps.com/100-best-travel-tips/",
            'views': 101
        },
        {
            'title': "Ten Places To Go In Africa And What To Do There!",
            'url':
            "https://www.smartertravel.com/best-places-to-go-in-africa-where-to-go-in-africa/",
            'views': 25
        },
        {
            'title': "Enjoying Your Flight Indefinately",
            'url': "https://www.foreverbreak.com/travel/tips/flight-enjoyable/",
            'views': 35
        },
    ]

    food_pages = [
        {
            'title': "How To Prepare Italian Pizza",
            'url':"https://www.walksofitaly.com/blog/food-and-wine/Italian-pizza-dough-recipe/",
            'views': 37       
        },
        {
            'title': "100 Most Popular African Foods",
            'url': "https://www.tasteatlas.com/100-most-popular-foods-in-africa/",
            'views': 29
        },
    ]


    cats = {
        "Fashion and Style": {"pages": fashion_pages, "views": 128, "likes": 64},
        "Food and Cuisine": {"pages": food_pages, "views": 64, "likes": 32},
        "Travel and Leisure": {"pages": travel_pages, "views": 32, "likes": 16},
    }

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
        
    c.save()
    return c 

if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()















































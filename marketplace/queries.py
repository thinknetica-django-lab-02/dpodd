from apps.main.models import Tag, Customer, Category, Goods
from django.contrib.auth import get_user_model

User = get_user_model()


t1, _ = Tag.objects.get_or_create(name="New")
t2, _ = Tag.objects.get_or_create(name="Hot")


cat1, _ = Category.objects.get_or_create(name="Supplements")
cat2, _ = Category.objects.get_or_create(name="Sportswear")

u_ivan, _ = User.objects.get_or_create(username="Ivan")
u_petr, _ = User.objects.get_or_create(username="Petr")

customer, _ = Customer.objects.get_or_create(user=u_petr)

item1, _ = Goods.objects.get_or_create(
                                    title="Protein", description="A bottle of fine protein, 700g",
                                    category=cat1, price=100.0, seller=u_ivan,
                                    customer=customer
                                    )
item2, _ = Goods.objects.get_or_create(
                                    title="Nike Running Shoes", description="A model for running",
                                    category=cat2, price=5000.0, seller=u_ivan,
                                    )
item2, _ = Goods.objects.get_or_create(
                                    title="Reebok Speed Shoes", description="A model for running",
                                    category=cat2, price=5550.0, seller=u_ivan,
                                    )

item1.tags.add(t2)
item2.tags.add(t1)
item2.tags.add(t2)

items_of_category1 = Goods.objects.filter(category=cat1)
items_of_category2 = Goods.objects.filter(category=cat2)

print(f"Filtered by category {cat1.name}: ",  items_of_category1)
print(f"Filtered by category {cat2.name}: ",  items_of_category2)

items_with_tag1 = Goods.objects.filter(tags__in=[t1])
items_with_tag2 = Goods.objects.filter(tags__in=[t2])


print(f"Filtered by tag {t1.name}: ",  items_with_tag1)
print(f"Filtered by tag {t2.name}: ",  items_with_tag2)

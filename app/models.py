from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    is_farmer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f'{self.category_name}'

    @property
    def count_active_auctions(self):
        return Auction.objects.filter(category=self).count()

class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=800, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_creator')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='auction_category')
    date_created = models.DateTimeField(default=timezone.now)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    current_bid = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)], blank=True, null=True)
    buyer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True
    )
    watchers = models.ManyToManyField(
        User,
        related_name='watchlist',
        blank = True
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Auction# {self.id}: {self.title} ({self.creator})'

class Image(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='get_images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.image}'

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Bid# {self.id}: {self.amount} on {self.auction.title} by {self.user.username}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='get_comments')
    comment = models.TextField(max_length=500)
    date_created = models.DateTimeField(default=timezone.now)

    def get_creation_date(self):
        return self.date_created.strftime('%B %d %Y')

    def __str__(self):
        return f'Comment# {self.id}: {self.user.username} on {self.auction.title}: {self.comment}'
    
class Product(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(max_length=800, null=True)
	creator = models.ForeignKey(User, on_delete=models.CASCADE ,related_name = 'inventory_creator')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'inventory_category')
	date_created = models.DateTimeField(default=timezone.now)
	quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
	price = models.FloatField()
	active = models.BooleanField(default=True)
	digital = models.BooleanField(default=True,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	Invbuyer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True
    )
	Invwatchers = models.ManyToManyField(
        User,
        related_name='invwatchlist',
        blank = True
    )

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
        

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
        


class ShippingAddress(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
import factory.django
import factory.fuzzy
from faker import Faker

from books.models import Author, Book, Category
from users.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "john%s" % n)
    email = factory.LazyAttribute(lambda o: "%s@example.org" % o.username)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = fake.text(max_nb_chars=5)


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: "cat_name%s" % n)
    pseudonym = fake.first_name()
    about = fake.sentence(nb_words=5)


path = "test_data/example.jpg"


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    author = factory.RelatedFactory(AuthorFactory)
    category = factory.SubFactory(CategoryFactory)
    title = fake.text(max_nb_chars=5)
    description = fake.sentence(nb_words=5)
    price = factory.fuzzy.FuzzyDecimal(55.99)
    publisher = fake.text(max_nb_chars=5)
    language = fake.language_name()
    pages = fake.random_int(min=2, max=4)
    isbn = 1234569874123
    # cover_image = factory.django.ImageField(upload_to='test_data')
    cover_image = "books/example.jpg"


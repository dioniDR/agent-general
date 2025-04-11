import random
import string

class FakeProvider:
    @staticmethod
    def random_name(length=8):
        """Generate a random name with the given length."""
        return ''.join(random.choices(string.ascii_letters, k=length)).capitalize()

    @staticmethod
    def random_email(domain='example.com'):
        """Generate a random email address."""
        name = FakeProvider.random_name().lower()
        return f"{name}@{domain}"

    @staticmethod
    def random_phone_number():
        """Generate a random phone number in the format XXX-XXX-XXXX."""
        return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

    @staticmethod
    def random_address():
        """Generate a random address."""
        street_number = random.randint(100, 9999)
        street_name = FakeProvider.random_name(length=random.randint(5, 10))
        street_type = random.choice(['St', 'Ave', 'Blvd', 'Rd', 'Ln'])
        city = FakeProvider.random_name(length=random.randint(5, 10))
        state = FakeProvider.random_name(length=2).upper()
        zip_code = random.randint(10000, 99999)
        return f"{street_number} {street_name} {street_type}, {city}, {state} {zip_code}"

    @staticmethod
    def random_company_name():
        """Generate a random company name."""
        adjectives = ['Global', 'Dynamic', 'Innovative', 'Creative', 'Efficient']
        nouns = ['Solutions', 'Systems', 'Concepts', 'Designs', 'Technologies']
        return f"{random.choice(adjectives)} {random.choice(nouns)}"
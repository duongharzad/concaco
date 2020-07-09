from django.utils import timezone
from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError
from django.utils.text import slugify
from faker import Faker
import random
from itertools import islice

from blog.models import Post


class Command(BaseCommand):
    help = 'Fake data post'

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help='number of record', default=1)

    def create_bulk_data(self, n):
        fake = Faker(['en_US'])
        users = User.objects.all()

        for _ in range(n):
            paragraphs = fake.paragraphs()
            author = random.choice(users)
            title = paragraphs[0].split('.')[0]
            slug = slugify(title)
            body = "\n ".join(paragraphs)
            status = random.choice(["published", "draft"])
            created = fake.date_time_between(start_date='-10y', end_date='now')
            updated = created + timezone.timedelta(hours=random.randint(1,23), days=random.randint(1,100))

            yield Post(
                 author=author,
                 title=title,
                 slug = slug,
                 body=body,
                 status=status,
                 created=created,
                 updated=updated
                 )

    def handle(self, *args, **options):
        N = options['number']
        count = 0

        objs = self.create_bulk_data(N)
        while True:
            batch = list(islice(objs, 100))
            if not batch:
                break
            Post.objects.bulk_create(batch, ignore_conflicts=True)
            count += len(batch)
            self.stdout.write(f"> {count} post")

        # collect stats
        posts = Post.objects.all()
        total = posts.count()
        draft_count = posts.filter(status="draft").count()

        self.stdout.write(f"Total {total} post (draft: {draft_count}, published: {total - draft_count})")

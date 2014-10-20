from django.test import TestCase
from .models import Entry

class Test(TestCase):
    def test_check(self):
        self.assertEqual(1+1, 2)

class EntryModelTests(TestCase):
    
    def test_created_time_updated_on_add(self):
        """
        The creation time should be set to timezone.now() when a blog entry is
        created.
        """
    # testing this slighty indirectly by checking that if two entries are created
    # in sequence, the second one has a later creation_time. Hard to test that
    # creation time == timezone.now() because of time delay between creating and
    # testing.
        first_entry = Entry.objects.create(title="title 1", text='text 1')
        second_entry = Entry.objects.create(title="title 2", text='text 2')
        print first_entry.created_date
        print second_entry.created_date

        self.assertEqual(first_entry.created_date < second_entry.created_date,
                         True)

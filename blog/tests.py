from django.test import TestCase
from .models import Entry

#need to sort out name spaces at some point and use reverse, but this will do for now
HOME_URL = "/"
DASHBOARD_URL= "/dashboard/"
NEW_URL = "/dashboard/new/"
EDIT_URL = "/dashboard/%d/edit/"

def create_entries(data):
    """
    Model factory: data is a list containing tuples of EntryModel data:
        [('title', 'text'),('title', 'text',...]
    It returns a tuple of populated entry model intances. 
    """
    return [Entry.objects.create(title=_title, text=_text)\
            for _title, _text in data]


class EntryModelTests(TestCase):
    
    def test_created_date_updated_on_add(self):
        """
        The creation date should be set to timezone.now() when a blog entry is
        created.
        """
    # testing this slighty indirectly by checking that if two entries are created
    # in sequence, the second one has a later creation_date. Hard to test that
    # creation time == timezone.now() because of time delay between creating and
    # testing.
        first_entry = Entry.objects.create(title="title 2", text='text 2')
        second_entry = Entry.objects.create(title="title 1", text='text 1')

        self.assertEqual(first_entry.created_date < second_entry.created_date,
                         True)

    def test_created_date_not_updated_on_edit(self):
        """
        The created time should not be updated for an existing entry when it is
        edited
        """
        entry = Entry.objects.create(title="title", text='text')
        created = entry.created_date
        entry.title = "something"

        self.assertEqual(created, entry.created_date)

class BlogViewTests(TestCase):
    
    def test_entries_are_in_created_date_order(self):
        """
        The entries in the context should be ordered by created_date.
        this check the EntryModel class Meta behaviour
        """

        entries = create_entries([('title 1', 'text 1'),
                                  ('title 2', 'text 2'),
                                  ('title 3', 'text 3')])
        
        context_entries = self.client.get(HOME_URL).context['entries']
        for i in range(len(context_entries)):
            self.assertEqual(entries[i], context_entries[i])

class DashboardViewTests(TestCase):
    
    def test_entries_are_in_created_date_order(self):
        """
        The entries in the context should be ordered by created_date.
        this check the EntryModel class Meta behaviour
        """
        entries = create_entries([('title 1', 'text 1'),
                                  ('title 2', 'text 2'),
                                  ('title 3', 'text 3')])
        
        context_entries = self.client.get(DASHBOARD_URL).context['entries']
        for i in range(len(context_entries)):
            self.assertEqual(entries[i], context_entries[i])

class NewEntryViewTests(TestCase):

    def test_get_request_provides_blank_form(self):
        """
        A blank EntryForm should be served when the NewEntry page is visited for
        the first time
        """
        form = self.client.get(NEW_URL).context['form']

        self.assertEqual(form.instance.title, '')
        self.assertEqual(form.instance.text, '')
    
    def test_valid_post_request_creates_new_entry(self):
        """
        If the form data is valid a new entry should be created and the data should
        match the form inout data
        """

        # check title valid upper limit
        # well that was awkward!
        title = 'a'* (Entry._meta.get_field('title').max_length - 1)
        form_data = {'title' : title, 'text' : 'New Text'}
        response = self.client.post(NEW_URL, form_data, follow=True)

        self.assertEqual(len(response.context['entries']),1)
        self.assertEqual(response.context['entries'][0].title, form_data['title'])
        self.assertEqual(response.context['entries'][0].text, form_data['text'])

    def test_valid_post_request_redirects_to_dashboard(self):
        """
        If the form data is valid redirect to dashboard
        """
        form_data = {'title' : 'New Title', 'text' : 'New Text'}
        response = self.client.post(NEW_URL, form_data, follow=True)

        self.assertIn('/dashboard/', response.redirect_chain[0][0])
        self.assertNotIn('/new/', response.redirect_chain[0][0])

    def test_empty_title_post_no_redirect(self):
        """
        If the title field is invalid we should not be commited redirected to 
        the dashboard.
        """
        response = self.client.post(NEW_URL, 
                                    {'title' : '', 'text' : 'text'},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain),0)

    def test_title_over_char_limit_post_no_redirect(self):
        """
        Title text with more than 200 chars is invalid.
        """
        title = 'a'* (Entry._meta.get_field('title').max_length + 1)
        response = self.client.post(NEW_URL, 
                                    {'title' : title, 'text' : 'text'},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain),0)

    def test_empty_text_post_no_redirect(self):
        """
        If the text field is invalid we should not be commited redirected to 
        the dashboard.
        """
        response = self.client.post(NEW_URL, 
                                    {'title' : 'title', 'text' : ''},
                                    follow=True)

        self.assertEqual(len(response.redirect_chain),0)

class EditEntryViewTests(TestCase):
    
    def test_get_requests_populates_form_with_existing_data(self):
        """
        A pre-populate EntryForm should be served when editing an existing entry
        """
        entry = create_entries([('title', 'new post')])[0]
        form = self.client.get(EDIT_URL % entry.pk).context['form']
        
        self.assertEqual(form.instance.title, entry.title)
        self.assertEqual(form.instance.text, entry.text)

    def test_valid_post_edits_existing_entry(self):
        """
        The entry that we edit should be updated with the data provided in the form
        """
        new_data = {'title' : 'update', 'text' : 'update'}
        entry = create_entries([('title', 'new post')])[0]
        response = self.client.post((EDIT_URL % entry.pk), 
                                    new_data,
                                    follow=True)
        
        self.assertEqual(response.context['entries'][0].title, new_data['title'])
        self.assertEqual(response.context['entries'][0].text, new_data['text'])

    def test_valid_post_doesnt_create_new_entry(self):
        """
        Editing an entry should not create a new entry
        """
        new_data = {'title' : 'update', 'text' : 'update'}
        entry1, entry2 = create_entries([('title 1', 'post 1'),
                                         ('title 2', 'post 2')])

        response = self.client.post((EDIT_URL % entry2.pk),
                                    new_data,
                                    follow=True)

        self.assertEqual(len(response.context['entries']), 2)

    def test_valid_post_redirects_to_dashboard(self):
        """
        If the form input data is valid redirect to dashboard for viewing
        """
        new_data = {'title' : 'update', 'text' : 'update'}
        entry = create_entries([('title', 'new post')])[0]
        response = self.client.post((EDIT_URL % entry.pk), 
                                    new_data,
                                    follow=True)

        self.assertIn('/dashboard/', response.redirect_chain[0][0])
        self.assertNotIn('/edit/', response.redirect_chain[0][0])

    def test_invalid_post_no_redirect(self):
        """
        If the form input data is invalid don't redirect to the dashboard
        """
        #tested various forms of invalid data with new posts, so only check once
        #here
        new_data = {'title' : 'update', 'text' : ''}
        entry = create_entries([('title', 'new post')])[0]
        response = self.client.post((EDIT_URL % entry.pk), 
                                    new_data,
                                    follow=True)

        self.assertEqual(len(response.redirect_chain), 0)

    def test_delete_entry_removes_entry(self):
        """
        check the entry is actually deleted.
        """
        entries = create_entries([('title 1','text 1'),
                                  ('title 2','text 2')])
        entry_count = len(entries)
        entry1, entry2 = entries

        response = self.client.post((EDIT_URL % entry2.pk),
                                    {'delete': 'delete'},
                                    follow=True)

        self.assertEqual(len(response.context['entries']), entry_count - 1)
    
    def test_delete_entry_redirects_to_dashboard(self):
        """
        If an entry is deleted redirect to dashboard for viewing
        """
        entry = create_entries([('title', 'new post')])[0]
        response = self.client.post((EDIT_URL % entry.pk), 
                                    {'delete':'delete'},
                                    follow=True)

        self.assertIn('/dashboard/', response.redirect_chain[0][0])
        self.assertNotIn('/edit/', response.redirect_chain[0][0])
    
    def test_delete_entry_removes_correct_entry(self):
        """
        check the entry is actually deleted.
        """
        entries = create_entries([('title 1','text 1'),
                                  ('title 2','text 2')])
        entry_count = len(entries)
        entry1, entry2 = entries

        response = self.client.post((EDIT_URL % entry2.pk),
                                    {'delete': 'delete'},
                                    follow=True)
        # diagnostic
        self.assertEqual(len(response.context['entries']), entry_count - 1)
        self.assertEqual(response.context['entries'][0].pk, entry1.pk) 

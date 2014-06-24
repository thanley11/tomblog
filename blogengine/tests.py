from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post
import markdown
# Create your tests here.

class PostTest(TestCase):
    def test_create_post_(self):
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()

        post.save()

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        self.assertEquals(only_post.title, 'My first post')
        self.assertEquals(only_post.text, 'This is my first blog post')
        self.assertEquals(only_post.pub_date.day, post.pub_date.day)
        self.assertEquals(only_post.pub_date.month, post.pub_date.month)
        self.assertEquals(only_post.pub_date.year, post.pub_date.year)
        self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEquals(only_post.pub_date.second, post.pub_date.second)

class AdminTest(LiveServerTestCase):
    fixtures = ['users.json']

    def setup(self):
        self.client = Client()

    def test_login(self):

        response = self.client.get('/admin/')

        self.assertEquals(response.status_code, 200)

        self.assertTrue('Log in' in response.content)

        self.client.login(username='bobsmith', password='password')

        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        self.assertTrue('Log out' in response.content)

    def test_logout(self):

        # Log in user
        self.client.login(username='bobsmith', password='password')

        # Check the response
        response = self.client.get('/admin/')

        self.assertEquals(response.status_code, 200)

        # Check 'log out' in response
        self.assertTrue('Log out' in response.content)

        # Log out user
        self.client.logout()

        # Check the response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'log in' in response
        self.assertTrue('Log in' in response.content)

    def test_create_post(self):

        # Log in
        self.client.login(username='bobsmith', password='password')

        # Check the response code
        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEquals(response.status_code, 200)

        # Create new post
        response = self.client.post('/admin/blogengine/post/add/', {
            'title': 'My first post',
            'text': 'This is my first post',
            'pub_date_0': '2014-06-18',
            'pub_date_1': '22:00:04',
            'slug': 'my-first-post'
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content)
        # Check new post in db
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

    def test_edit_post(self):
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()

        # Log in
        self.client.login(username='bobsmith', password='password')

        response = self.client.post('/admin/blogengine/post/1/', {
            'title': 'My second post',
            'text': 'This is my second post',
            'pub_date_0': '2014-06-10',
            'pub_date_1': '21:00:02',
            'slug' : 'my-second-post'
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)

        self.assertTrue('changed successfully' in response.content)

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post.title, 'My second post')
        self.assertEquals(only_post.text, 'This is my second post')

    def test_delete_post(self):
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first post'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.save()

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        self.client.login(username='bobsmith', password="password")

        response = self.client.post('/admin/blogengine/post/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        self.assertTrue('deleted successfully' in response.content)

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)

class PostViewTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        post = Post()
        post.title = "My first post"
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.pub_date = timezone.now()
        post.slug = 'my-first-post'
        post.save()

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts),1)

        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        self.assertTrue(post.title in response.content)
        self.assertTrue(markdown.markdown(post.text) in response.content)

        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b')  in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)


        self.assertTrue('<a href="http://127.0.0.1:8000/"my first blog post</a>' in response.content)

    def test_post_page(self):
        post = Post()
        post.title = "My first post"
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.pub_date = timezone.now()
        post.slug = 'my-first-post'
        post.save()

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts),1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        post_url = only_post.get_absolute_url()

        response = self.client.get(post_url)
        self.assertEquals(response.status_code, 200)

        self.assertTrue(post.title in response.content)
        self.assertTrue(markdown.markdown(post.text) in response.content)

        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b')  in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)


        self.assertTrue('<a href="http://127.0.0.1:8000/"my first blog post</a>' in response.content)

class PostTest(TestCase):
    def test_create_post(self):
        post = Post()

        post.title = "My first post"
        post.text = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()

        post.save()

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        self.assertEquals(only_post.title, 'My first post')
        self.assertEquals(only_post.text, 'This is my first blog post')
        self.assertEquals(only_post.slug, 'my-first-post')
        self.assertEquals(only_post.pub_date.day, post.pub_date.day)
        self.assertEquals(only_post.pub_date.month, post.pub_date.month)
        self.assertEquals(only_post.pub_date.year, post.pub_date.year)
        self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEquals(only_post.pub_date.second, post.pub_date.second)

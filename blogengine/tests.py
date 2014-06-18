from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post
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

    def test_login(self):
        c = Client()

        response = c.get('/admin/')

        self.assertEquals(response.status_code, 200)

        self.assertTrue('Log in' in response.content)

        c.login(username='bobsmith',password='password')

        response = c.get('/admin/')
        self.assertEquals(response.status_code, 200)

        self.assertTrue('Log out' in response.content)
    
    def test_logout(self):
        # Get client
        c = Client()

        # Log in user
        c.login(username='bobsmith',password='password')

        # Check the response
        response = c.get('/admin/')
        self.assertEquals(response.status_code, 200)
       
        # Check 'log out' in response
        self.assertTrue('Log out' in response.content)
            
        # Log out user
        c.logout()

        # Check the response code
        response = c.get('/admin/')
        self.assertEquals(response.status_code, 200)
       
        # Check 'log in' in response
        self.assertTrue('Log in' in response.content)
 





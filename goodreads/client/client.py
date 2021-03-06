
# Global imports
import datetime
import urllib
import webbrowser
import xml.etree.ElementTree as ET
import time as t
#from sys import maxint as MAX_INT

# Local imports
from .author import Author
from .book import Book
from .comparison import Comparison
from .request import GoodreadsRequest, GoodreadsRequestError
from .session import GoodreadsSession, GoodreadsSessionError

class Client:
    """ A client for interacting with Goodreads resources."""

    host = "https://www.goodreads.com/"
    session = None

    def __init__(self, **kwargs):
        """
        Create a client instance using the provided options.
        The passed options should be passed as kwargs.
        """
        self.client_id     = kwargs.get('client_id')
        self.client_secret = kwargs.get('client_secret')
        self.query_dict = { 'key' : self.client_id }

    def authenticate(self, access_token=None, access_token_secret=None):
        """ Go through Open Auththenication process. """
        self.session = GoodreadsSession(self.client_id, self.client_secret,
                                       access_token, access_token_secret)

        if access_token and access_token_secret:
            self.session.oath_resume()
        else: # Access not yet granted, allow via browser
            url = self.session.oath_start()
            webbrowser.open(url)
            while input('Have you authorized me? (y/n) ') != 'y':
                pass
            self.session.oauth_finish()

    def get_access_tokens():
        """ Return access tokens for storage, so that sessions can be 
        resumed easily.
        Returns: (access_token, access_token_secret) """
        if not self.session:
            raise GoodreadsSessionError("No authenticated session.")
        return self.session.access_token, self.session.access_token_secret

    def book_title(self, **query_dict):
        """
        Get information about a book.
        Input Example: {'author' : 'Chuck Palahniuk', 'title' : 'Fight Club'}
        """
        goodreads_request = GoodreadsRequest("book/title.xml", query_dict, self)
        response = goodreads_request.request()
        return Book(response['book'])
    
    def get_books_user(self, user_id):
        if not self.session:
            raise GoodreadsSessionError("No authenticated session.")
        books_user = []                
        page = 1
        resp = self.session.get("/review/list.xml",{'v': 2, 'id': user_id, 'page':page})
        while resp['reviews']['@end'] != '0':
            if int(resp['reviews']['@total']) - int(resp['reviews']['@start']) == 0:
                 books_user.append(list(resp['reviews']['review']['book']['id'].values())[1])
            else:
                for i in range(len(resp['reviews']['review'])):
                    books_user.append(list(resp['reviews']['review'][i]['book']['id'].values())[1])
            page+=1
            resp = self.session.get("/review/list.xml",{'v': 2, 'id': user_id, 'page':page})
            t.sleep(1)
        return books_user

    def author_by_id(self, **query_dict):
        """
        Get information about an author from their id.
        Input example: { 'id' : '2546' }
        """
        goodreads_request = GoodreadsRequest("author/show.xml", query_dict, self)
        response = goodreads_request.request()
        return Author(response['author'])

    def get_author_id(self, name):
        """ Get the id of an author given the name."""
        name = urllib.quote_plus(name)
        goodreads_request = GoodreadsRequest("api/author_url/"+name, {}, self)
        response = goodreads_request.request()
        return response['author']['@id']

    def get_book_id(self, isbn):
        """ Get book id given the isbn. """
        goodreads_request = GoodreadsRequest("book/isbn_to_id/"+isbn, {}, self)
        response = goodreads_request.request(return_raw=True)
        return response
        
    def get_review_user(self, id, genero):
        """ Get review's information the id. """
        goodreads_request = GoodreadsRequest("review/show.xml",{'id':id, 'key':'2uQMlznVEwfI4YTVFQwsA'},self)
        response = goodreads_request.request(return_raw=True)
        root = ET.fromstring(response)
        userReview = {}
        userXml = root.find('review/user')
        userReview['id_user'] = userXml.find('id').text
        userReview['nombre'] = userXml.find('display_name').text
        userReview['enlace'] = userXml.find('link').text
        userReview['genero'] = genero
        userReview['id_libro'] = root.find('review/book/id').text
        userReview['review'] = root.find('review/body').text
        return userReview

    def get_friends(self, user_id, num=30):
        """ Get pages of user's friends list. (30 per page)
        Returns: ((id, name),) """
        if not self.session:
            raise GoodreadsSessionError("No authenticated session.")

        # Iterate through pages
        friends = []
        page, end, total = 1, 0, 1
        while end < num and end < total:
            data_dict = self.session.get('friend/user/'+user_id,
                                        {'format':'xml', 'page':str(page)})
            data_dict = data_dict['friends']
            # Check to see if  there is 'user' (friend) data
            if len(data_dict) == 3:
                break # No friends :(
            else: # Update progress
                end = int(data_dict['@end'])
                total = int(data_dict['@total'])
                page += 1
            # Add page's list to total
            friends.extend([(user['id'], user['name']) for user in data_dict['user']])
        # Return compiled list of friends
        return friends
        
    def get_followers(self, user_id, num=30):
        """ Get pages of user's friends list. (30 per page)
            Returns: ((id, name),) """
        if not self.session:
            raise GoodreadsSessionError("No authenticated session.")

        # Iterate through pages
        followers = []
        page, end, total = 1, 0, 1
        while end < num and end < total:
            data_dict = self.session.get('user/'+user_id + '/followers',
                                        {'format':'xml', 'page':str(page)})
            data_dict = data_dict['followers']
            # Check to see if  there is 'user' (friend) data
            if len(data_dict) == 3:
                break # No followers :(
            else: # Update progress
                end = int(data_dict['@end'])
                total = int(data_dict['@total'])
                page += 1
            # Add page's list to total
            followers.extend([(user['id'], user['name']) for user in data_dict['user']])
        # Return compiled list of friends
        return followers

    def get_auth_user(self):
        """ Get the OAuthenticated user id and name """
        if not self.session:
            raise GoodreadsSessionError("No authenticated session.")

        data_dict = self.session.get('api/auth_user', {'format':'xml'})
        # Parse response
        user_id = data_dict['user']['@id']
        name = data_dict['user']['name']
        return user_id, name

    def compare_books(self, user_id):
        """ Compare books between the authenticated user and another. """
        if not self.session:
            raise GoodreadsSessionError("No authenticated session.")
        data_dict = self.session.get('user/compare/'+user_id, {'format':'xml'})
        return Comparison(data_dict['compare'])


import bs4
import json
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import *
from .models import Movies, WatchList, WatchedList


class RegisterView(CreateAPIView):
    """
    Register API

         Request body{
            "username":"username",
            "password":"password"
         }
    """
    serializer_class = RegisterSerializer

class LoginView(APIView):
    """
    Login API

         Request body{
            "username":"username",
            "password":"password"
         }
    """
    def post(self, requset):
        data= requset.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=data["username"], password=data["password"])
            if user:
                token, create = Token.objects.get_or_create(user=user)
                return Response(data={"token":token.key, "user_id":user.id}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)


class ScrapeMoviesView(APIView):
    """
    Scrape Movies API
        Request body {
            "url":"https://www.imdb.com/chart/top/"
        }
    """
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        url = request.data["url"]
        response = requests.get(url)
        if response.status_code == 200:
            html_soup = bs4.BeautifulSoup(response.text, 'html.parser')
            movies = html_soup.find("tbody", "lister-list").find_all("tr")
            print(movies)
            movies_dict = {}
            for movie in movies:
                movies_dict["title"] = movie.find('td', "titleColumn").find("a").get_text()
                movies_dict["poster"] = "https://www.imdb.com/" + str(movie.find('td', 'posterColumn').find("a", href=True)["href"])
                movies_dict["rating"] = movie.find("td", "ratingColumn imdbRating").find("strong").get_text()
                existed  = Movies.objects.filter(title=movies_dict["title"])
                if not existed:
                    serializer = MoviesSerializer(data=movies_dict)
                    if serializer.is_valid():
                        serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=response.status_code)


class MovieList(ListAPIView):
    """
    Movielist API

        Get request, if want to search/filter with any keyword use
         :param search=django

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MoviesSerializer
    def get_queryset(self):
        if self.request.query_params:
            search_title = self.request.query_params["search"]
            queryset = Movies.objects.filter(title__icontains=search_title)
            return queryset
        queryset = Movies.objects.all()
        return queryset

class MovieDetail(RetrieveAPIView):
    """
    MovieDetail API

        Request body {
            "id":2
        }
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MoviesSerializer
    def get_object(self):
        data_id = self.request.data["id"]
        queryset = Movies.objects.get(id=data_id)
        return queryset

class WatchListAddView(ListCreateAPIView):
    """
    WatchList API for List and create

        Request(to add movie in watchlist) body {
            "movie_id":2
        }

        Use get method to get the list of watchlist movies
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WatchListSerializer
    def get_queryset(self):
        queryset = WatchList.objects.filter(user=self.request.user)
        return queryset
    def post(self, request, *args, **kwargs):
        try:
            movie_id = request.data["movie_id"]
            data_dict = {"user":request.user.id, "movie":movie_id}
            serializer = WatchListSerializer(data=data_dict)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=json.dumps(data_dict), status=status.HTTP_201_CREATED)
        except Exception as e:
            raise e

class WatchedListAddView(ListCreateAPIView):
    """
    WatchedList API for List and create

        Request(to add movie in watchedlist) body {
            "movie_id":2
        }

        Use get method to get the list of watchedlist movies
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WatchedListSerializer
    def get_queryset(self):
        queryset = WatchedList.objects.filter(user=self.request.user)
        return queryset
    def post(self, request, *args, **kwargs):
        try:
            movie_id = request.data["movie_id"]
            data_dict = {"user":request.user.id, "movie":movie_id}
            serializer = WatchedListSerializer(data=data_dict)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=json.dumps(data_dict), status=status.HTTP_201_CREATED)
        except Exception as e:
            raise e

class WatchListRemoveView(DestroyAPIView):
    """
    Remove movie from Watched list

        Request(delete method) body {
            "movie_id":2
        }
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WatchListSerializer
    def get_object(self):
        try:
            object = WatchList.objects.get(user=self.request.user, movie=self.request.data["movie_id"])
        except Exception as e:
            raise e
        return object

class WatchedListRemoveView(DestroyAPIView):
    """
    Remove movie from Watched list

        Request(delete method) body {
            "movie_id":2
        }
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WatchedListSerializer
    def get_object(self):
        try:
            object = WatchedList.objects.get(user=self.request.user, movie=self.request.data["movie_id"])
        except Exception as e:
            raise e
        return object


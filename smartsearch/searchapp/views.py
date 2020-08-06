from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
# from apiclient.discovery import build
from googleapiclient.discovery import build
from .utils import SearchResults
from . import *
from .forms import SearchForm, UserRegisterForm, UserProfileForm
import bs4
import urllib3


class SearchView(TemplateView):
    template_name = "googlesearch/result.html"

    def get_context_data(self, **kwargs):

        context = super(SearchView, self).get_context_data(**kwargs)

        service = build("customsearch", GOOGLE_SEARCH_API_VERSION,
                        developerKey=GOOGLE_SEARCH_API_KEY)

        # add a "try" block to see if googleapiclient throws a 400 error
        try:
            results = service.cse().list(
                q=self.request.GET.get('q', ''),
                start=self.page_to_index(),
                num=GOOGLE_SEARCH_RESULTS_PER_PAGE,
                cx=GOOGLE_SEARCH_ENGINE_ID,
            ).execute()

            results = SearchResults(results)
            pages = self.calculate_pages()

        # if googleapiclient raises an error, we need to catch it here
        except:

            # run the search again starting with a defined page 1 instead of the "user" defined
            results = service.cse().list(
                q=self.request.GET.get('q', ''),
                start=1,
                num=GOOGLE_SEARCH_RESULTS_PER_PAGE,
                cx=GOOGLE_SEARCH_ENGINE_ID,
            ).execute()

            # set some default values used for the context below
            page = 1

            # previous, current, next pages
            pages = [0, 1, 2]

            results = SearchResults(results)

        """ Set some defaults """
        context.update({
            'items': [],
            'total_results': 0,
            'current_page': 0,
            'prev_page': 0,
            'next_page': 0,
            'search_terms': self.request.GET.get('q', ''),
            'error': results
        })

        """ Now parse the results and send back some
            useful data """

        context.update({
            'items': results.items,
            'total_results': results.total_results,
            'current_page': pages[1],
            'prev_page': pages[0],
            'next_page': pages[2],
            'search_terms': results.search_terms,
        })

        return context

    def calculate_pages(self):
        """ Returns a tuple consisting of
            the previous page, the current page,
            and the next page """

        current_page = int(self.request.GET.get('p', 1))
        return (current_page - 1, current_page, current_page + 1)

    def page_to_index(self, page=None):
        """ Converts a page to the start index """

        if page is None:
            page = self.request.GET.get('p', 1)

        return int(page) * int(GOOGLE_SEARCH_RESULTS_PER_PAGE) + 1 - int(GOOGLE_SEARCH_RESULTS_PER_PAGE)


class index(View):
    def get(self, request):
        form = SearchForm()
        context = {
            'form': form,
        }
        return render(request, 'searchapp/index.html', context)

    def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():
            search = request.POST.get('search_text')
            http = urllib3.PoolManager()
            r = http.request('GET', search)
            soup = bs4.BeautifulSoup(r.data, 'html.parser')
            data = soup.prettify()

            output = open('document_file/text3.txt', 'w', encoding='utf-8')
            for line in data:
                output.write(line)
            output.close()
        return render(request, 'searchapp/index.html')


# def login(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         print(form)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             # password = form.cleaned_data.get('password')
#             # my_user = authenticate(username=username, password=password)
#             # login(request, my_user)
#             print(username)
#             return HttpResponse('You dont have an account with us')
#             # return HttpResponseRedirect(reverse('searchapp:home-page'))
#     else:
#         form = UserRegisterForm()
#         return render(request, 'searchapp/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            my_user = authenticate(username=username, password=password)
            login(request, my_user)
            return redirect('searchapp:profile')
    else:
        form = UserRegisterForm()
    return render(request, 'searchapp/register.html', {'form': form})


@login_required()
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('searchapp:home-page')
    else:
        form = UserProfileForm()
        context = {
            'form': form
        }
        return render(request, 'searchapp/profile.html', context)


def home(request):
    return render(request, 'searchapp/home.html')

def result(request):
    return render(request, 'searchapp/result.html')
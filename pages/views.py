from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import EstimateForm, QuestionForm, ForumForm
from .models import Question, Estimate, Forum
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateResponseMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.forms import formset_factory
from django.contrib import messages
from .yes import DoubleView
from django.shortcuts import get_object_or_404
from django.db.models import Count, F, Value
from django.urls import reverse_lazy

# to relate, one needs to relate to a full object instance
# load question instance
# then relate estimate to that instance




class HomeView(DoubleView):
    model = Question
    form = EstimateForm
    form_class = EstimateForm
    #success_url = '/'
    slug_url_kwarg = 'topic'
    def get_template_names(self):
        return 'pages/home.html'

    def add_to_tracked(self, question):
        user = self.request.user
        #if user.is_anonymous:       #########this breaks HomeView
        #    return
        id = user.id
        f = User.objects.filter(id = id)[0]
        question.tracked_by.add(f)


    def get_success_url__(self):
        req_post = self.get_submit_values()
        topic = req_post[0]
        pk = req_post[1]
        rel_q = Question.objects.filter(id=pk)[0]
        user = self.request.user
        if user.is_anonymous:
            pass
        else:
            self.add_to_tracked(rel_q)
        slug = rel_q.slug
        success_url_str = 'p/'+ topic + '/'+ str(pk) + '/' + str(slug) +'/'
        self.success_url = success_url_str
        return self.success_url



class ForumView(DoubleView):
    model = Question
    form = EstimateForm
    form_class = EstimateForm
    success_url = '/'
    def get_template_names(self):
        return 'pages/question_list.html'

    def add_to_tracked(self, question):
        question.tracked_by.add(self.request.user)

    def get_success_url__(self):
        req_post = self.get_submit_values()
        topic = req_post[0]
        pk = req_post[1]
        rel_q = Question.objects.filter(id=pk)[0]
        self.add_to_tracked(rel_q)
        slug = rel_q.slug

        success_url_str = str(pk) + '/' + str(slug) +'/'
        self.success_url = success_url_str
        return self.success_url

##############################################

class TrackedQuestionsView(LoginRequiredMixin, ListView):
    template_name = 'tracked.html'
    def get_queryset(self, *args, **kwargs):

        user = self.request.user
        if user.is_anonymous:
            return
        id = user.id
        print('id: ' +str(user))
        current_user = User.objects.filter(id = id)[0]
        queryset = current_user.question_set.all()
        return queryset



class PopularQuestionsView(DoubleView):
    model = Question
    form = EstimateForm
    form_class = EstimateForm
    slug_url_kwarg = 'topic'

    success_url = reverse_lazy('author-list', kwargs={})
    def get_template_names(self):
        return 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = {}
        pk = self.kwargs.get(self.pk_url_kwarg)
        raw_set = Estimate.objects.filter(related_question=pk)

        context['estimate_set'] = merge_sort(raw_set)
        print('context detail: ' + str(context))
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_success_url__(self):
        req_post = self.get_submit_values()
        topic = req_post[0]
        pk = req_post[1]
        rel_q = Question.objects.filter(id=pk)[0]
        slug = rel_q.slug

        success_url_str = 'p/'+ topic + '/'+ str(pk) + '/' + str(slug) +'/'
        self.success_url = success_url_str
        return reverse_lazy('question-detail', kwargs={'pk':pk,
                                                        'slug': slug,
                                                        'topic':topic
                                                        })


##############################################

class CreateForumView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ForumForm
    template_name = 'pages/forum_form.html'
    success_url = '{slug}/'
    success_message = "%(topic)s was created successfully"

    def form_valid(self, form):
        form.instance.author =  self.request.user
        return super().form_valid(form)




class ForumDetailView(DetailView):
    model = Forum
    #template = myapp/article_detail.html:

class ForumUpdateView(UpdateView):
    model = Forum
    fields = ['description', 'image']


    def form_valid(self, form):
        form.instance.author =  self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


##################################################




class EstimateListView(LoginRequiredMixin, ListView):
    model = Estimate
 #default <app>/<model>_<classview>
    context_object_name = 'object_list' # default is 'object'|| returns a list
    #ordering = ['date-posted']
    def get_queryset(self):
        user = self.request.user
        return Estimate.objects.filter(author = user)



class EstimateDetailView(DetailView):
    model = Estimate
    template_name = 'view-estimate.html'


class EstimateCreateView(LoginRequiredMixin, CreateView):
    model = Estimate
    fields = ['estimate', 'body', 'related_question']

    def form_valid(self, form):
        form.instance.author =  self.request.user
        return super().form_valid(form)

    #ordering = ['date-posted']


class EstimateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Estimate
    fields = ['body']

    def form_valid(self, form):
        form.instance.author =  self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class EstimateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Estimate
    success_url ='/'
#    template_name = 'view-estimate.html'
    def test_func(self):
        post = self.get_object()
        if self.request.user == object.author:
            return True
        return False

#######################################################

def merge_sort(unsorted_list):
    if len(unsorted_list) <= 1:
        return unsorted_list
# Find the middle point and devide it
    middle = len(unsorted_list) // 2
    left_list = unsorted_list[:middle]
    right_list = unsorted_list[middle:]

    left_list = merge_sort(left_list)
    right_list = merge_sort(right_list)
    return list(merge(left_list, right_list))

# Merge the sorted halves

def merge(left_half,right_half):
    res = []
    while len(left_half) != 0 and len(right_half) != 0:
        if left_half[0].author.profile.score < right_half[0].author.profile.score:
            res.append(left_half[0])
            left_half.remove(left_half[0])
        else:
            res.append(right_half[0])
            right_half.remove(right_half[0])
    if len(left_half) == 0:
        res = res + right_half
    else:
        res = res + left_half
    return res

################################################################

class QuestionListView(ListView): #ProcessFormView,
    model = Question
    template_name = 'pages/question_list.html'
    context_object_name = 'question_set'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        EstimateFormSet = formset_factory(EstimateForm, max_num=5, extra=3)
        context['estimate_formset'] = EstimateFormSet
        return context


class QuestionDetailView(DetailView):
    model = Question
    topic_url_kwarg = 'topic'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        topic = self.kwargs.get(self.topic_url_kwarg)
        forum = Forum.objects.filter(topic=topic)[0].id
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug, 'forum': forum })

        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        pk = self.kwargs.get(self.pk_url_kwarg)
        raw_set = Estimate.objects.filter(related_question=pk)

        context['estimate_set'] = merge_sort(raw_set)
        print('context detail: ' + str(context))
        context.update(kwargs)
        return super().get_context_data(**context)





class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question']
    slug_url_kwarg = 'topic'

    def get_slug_fields(self):
        topic = self.kwargs.get(self.slug_url_kwarg)
        print('this is th etopic' +str(topic))
        forum = Forum.objects.filter(topic=topic)
        print('forum' + str(forum))
        return forum[0]

    def form_valid(self, form):
        form.instance.author =  self.request.user
        form.instance.forum = self.get_slug_fields()
        return super().form_valid(form)

    #ordering = ['date-posted']


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['collapse']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.author =  self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        # Check permissions for the request.user here
        self.fields = ['collapse']
        return super().dispatch(request, *args, **kwargs)



class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url ='/'
#    template_name = 'view-estimate.html'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


###################################################

####################################################


def homepage(request):
    total_num = 5
    index_list =[]
    question_set = Question.objects.all()[:total_num]
    for q in question_set:
        index_list.append(q.id)
    if request.method == 'POST' :
        print('request.POST.get' + str(request.POST.get('name')))

        form = EstimateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estimate inputted!')
            return redirect('get_estimate')
    else:
        question_set = Question.objects.all()[:total_num]
        formset = EstimateForm

    context = {'question_set':question_set, 'estimate_form':formset}
    return render(request, 'pages/question_list.html', context)



def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')

        topic_query = Forum.objects.filter(topic__icontains=search)
        desc_query = Forum.objects.filter(description__icontains=search)

        forums = (topic_query | desc_query).distinct()

        return render(request, 'searchbar.html', {'forums': forums})

def piechart(request):
    return render(request, 'piechart.html', {})

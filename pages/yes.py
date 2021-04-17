from django.views.generic.base import ContextMixin, TemplateResponseMixin, View
from django.views.generic.edit import ProcessFormView, FormMixin, ModelFormMixin
from django.views.generic.list import MultipleObjectTemplateResponseMixin, MultipleObjectMixin
from django.forms import formset_factory , BaseFormSet
from pprint import pprint
from django.core.paginator import Paginator
from django.forms.utils import ErrorList
from django.core.exceptions import ImproperlyConfigured
from .forms import EstimateForm
from .models import Question, Forum, Estimate
from django.utils.functional import cached_property
from django.db.models import Count
from django.contrib.auth.models import User


#def gen():
#    while True:
#        yield 1

gen = [str(i) for i in range(100)]
gen.pop(0)

class DoubleSet(BaseFormSet):
    #prefix = 'form',
    def __init__(self, offset=0, end=None, step=1, model=None, #form_kwargs={},
                model_kwargs={}, *args, **kwargs):
            super(DoubleSet, self).__init__(*args, **kwargs)
            self.offset = offset
            self.end = end
            self.step = step
            self.model = model
            #self.form_kwargs = form_kwargs
            self.model_kwargs = model_kwargs

    def _generator(self):
        while True:
            yield 1

    def make_set(self, model_kwargs={}):
        counter = 0
        #counter = self._generator()
        self.double_list = []
        model_set = self.model.objects.annotate(Count('tracked_by')).filter(**model_kwargs)[self.offset:self.end:self.step]
        for obj in model_set:
            form = self._construct_form(counter, **self.get_set_form_kwargs(counter))
            topic = Forum.objects.filter(topic=obj.forum)[0].topic

            predictors = set()
            for estimates in Estimate.objects.filter(related_question=obj):
                predictors.add(estimates.author.id)

            pair = {'question':obj, 'trackers':obj.tracked_by__count, 'form':form, 'topic': topic, 'predictors': predictors}
            self.double_list.append(pair)
            counter += 1
        return self.double_list


    def add_prefix(self,  field_name):
        return '%s-%s' % (self.prefix, field_name) if self.prefix else field_name


    def _construct_form(self, i, **kwargs):
        defaults = {
            'auto_id': self.auto_id,
            'prefix': self.add_prefix(i),
            'error_class': self.error_class,
            'use_required_attribute': False,
        }
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial and 'initial' not in kwargs:
            try:
                defaults['initial'] = self.initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty, unless they're part of
        # the minimum forms.
        if i >= self.initial_form_count() and i >= self.min_num:
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form

    @cached_property
    def forms(self):
        return [
            self._construct_form(i, **self.get_set_form_kwargs(i))
            for i in range(self.total_form_count())
        ]

    def get_set_form_kwargs(self, index):
        return self.form_kwargs.copy()

    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            use_required_attribute=False,
            **self.get_set_form_kwargs(None)
        )
        self.add_fields(form, None)
        return form

    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:

                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                self.add_error(name, e)



class MultipleObjectTemplateResponseMixin(TemplateResponseMixin):
    template_name_suffix = '_list'

    def get_template_names(self):
        try:
            names = super().get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        if hasattr(self.object_list, 'model'):
            opts = self.object_list.model._meta
            names.append("%s/%s%s.html" % (opts.app_label, opts.model_name, self.template_name_suffix))
        elif not names:
            raise ImproperlyConfigured(
                "%(cls)s requires either a 'template_name' attribute "
                "or a get_queryset() method that returns a QuerySet." % {
                    'cls': self.__class__.__name__,
                }
            )
        return names

class DoubleObjectMixin(ContextMixin):
    def __init__(self, form=EstimateForm, number_of_items =1,
                    *args, **kwargs):
        super(DoubleObjectMixin, self).__init__(*args, **kwargs)
        self.form = form
        self.number_of_items = number_of_items
        self.slugs = None
    allow_empty = True
    queryset = None
    model = None
    paginate_by = None
    paginate_orphans = 0
    context_object_name = 'double_list'
    paginator_class = Paginator
    page_kwarg = 'page'
    ordering = None

    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    topic_url_kwarg = 'topic'

    def get_form(self):
        return self.form

    def get_slug_fields(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk == '':
            slug = ''
        self.slug_dict = {'pk':pk, 'slug':slug}

        topic = self.kwargs.get(self.topic_url_kwarg)
        if topic != None:
            forum = Forum.objects.filter(topic__iexact=topic)[0]
            self.slug_dict.update({'forum':forum})

        return self.slug_dict


    def get_queryset(self, author=None):
        slug_dict = self.get_slug_fields()
        try:
            forum = slug_dict['forum']
            filter_dict = slug_dict.copy()
            filter_dict.update({'forum':forum.id})

        except:
            filter_dict ={}
        #why was filter_dict = {} here?
        search_dict ={}
        for k,v in filter_dict.items():
            if v:
                search_dict.update({k: v})


        class_created = formset_factory(EstimateForm, formset=DoubleSet, min_num=self.number_of_items) #
        doubleset = class_created()
        doubleset.model = self.model

        queryset = doubleset.make_set(search_dict)

        if author:
            for pair in queryset:
                if author in pair['predictors']:
                    pair['predictors'] = True
                else:
                    pair['predictors'] = False

        ordering = self.get_ordering()
        if ordering and annotation:
            if isinstance(ordering, str):
                ordering = (ordering,)
            if isinstance(annotation, str):
                annotation = (annotation,)
            queryset = queryset.annotate(annotation=Count(annotation)).order_by("-%s" % (annotation))
        if ordering: # this may cause a bug
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_ordering(self):
        return self.ordering

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_paginate_by(self, queryset):
        return self.paginate_by

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        return self.paginator_class(
            queryset, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def get_paginate_orphans(self):
        return self.paginate_orphans

    def get_allow_empty(self):
        return self.allow_empty

    def get_context_object_name(self, object_list):
        """Get the name of the item to be used in the context."""
        if self.context_object_name:
            return self.context_object_name
        else:
            return 'double_list'

    def get_context_data(self, *, object_list=None, model_kwargs={}, **kwargs):
        queryset = self.get_queryset()#object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = 'double_list' #self.get_context_object_name(queryset)
        try:
            topic = self.slug_dict['forum']
            print('context toopic' + str(topic))
        except:
            topic = ''
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset,
                'topic': topic,
                'gen': gen
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset,
                'topic': topic,
                'gen': gen
            }

        context.update(kwargs)
        return context


def _get_form(request, formcls, submit_name): #submit name works
    data = request.POST if submit_name in request.POST else None
    if data != None:
        edited_data = data.copy()
        related_question_id = edited_data.pop(submit_name)
        newform = formcls(data = edited_data)
        for i in newform.data:
            prefix_chars = []
            dash_count = 0
            for c in i:
                prefix_chars.append(c)
                if c == '-':
                    dash_count +=1
                if dash_count > 1:
                    prefix_chars.pop()
                    prefix =''.join(prefix_chars)
                    newform.prefix = prefix
                    return newform
    return EstimateForm()


class DoubleView(MultipleObjectTemplateResponseMixin,DoubleObjectMixin, FormMixin, ProcessFormView):
    def get_submit_values(self):
        submit_value_str = self.request.POST['submit-question-id']
        submit_values = submit_value_str.split(',')
        return submit_values

    def get_rel_q(self):
        req_post = self.get_submit_values()
        pk = req_post[1]
        rel_q = Question.objects.filter(id=pk)[0]
        return rel_q

    def get_success_url__(self):
        req_post = self.get_submit_values()
        topic = req_post[0]
        pk = req_post[1]
        rel_q = Question.objects.filter(id=pk)[0]
        slug = rel_q.slug
        home_url_str = 'p/'+ topic + '/' + str(pk) + '/' + str(slug) +'/'
        success_url_str = str(pk) + '/' + str(slug) +'/'
        self.success_url = success_url_str
        return self.success_url


    def post(self, request, *args, **kwargs):
        form = _get_form(request, EstimateForm, 'submit-question-id')
        user = self.request.user

        if form.is_valid():
            post = form.save(commit=False)
            rel_q = self.get_rel_q()
            post.related_question = rel_q
            if user.is_anonymous:
                post.author = User.objects.filter(id=1)[0]

            else:
                post.author = user
                post.save()
                print('Post Saved!')

            self.get_success_url__()
            return self.form_valid(post)

        else:
            print('Form not Valid')
            return self.form_invalid(form)

    def get_queryset(self):
        user = self.request.user.id
        return super().get_queryset(author=user)

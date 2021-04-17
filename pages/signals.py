from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Estimate, Question
from algorithm import simple_scores as ss
import string
from django.utils.text import slugify

"""
def unique_slug_generator(instance, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.question[:31])
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug = slug).exists()

    if qs_exists:
        new_slug = "{slug}".format(slug = slug)
        return unique_slug_generator(instance, new_slug = new_slug)

    return slug

def pre_save_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_receiver, sender = Question)"""


def update_question(sender, instance, **kwargs):
    q = instance.related_question
    index = q.id
    estimate_set = Estimate.objects.filter(related_question=index)

    #algorithm
    new_pred = ss.find_predictions(estimate_set) #takes query set

    q.prediction = new_pred
    q.save()

    print(instance.related_question.prediction)
    print(q.prediction)
    print('question updated to ' + str(new_pred))

post_save.connect(update_question, sender=Estimate)


def update_user_score(sender, instance, **kwargs):
    if instance.collapse == None:
        print('None')

    elif instance.collapse != None:
        truth = instance.collapse
        index = instance.id
        asker = instance.author

        estimate_set = Estimate.objects.filter(related_question=index, author=asker)

        for est in estimate_set:
            predictor = est.author.profile
            guess = est.estimate/100
            old_score = predictor.score
            predictor.total_estimates += 1
            all_est = predictor.total_estimates
            predictor.score = ss.predictor_score(truth, guess, all_est, old_score)
            est.score = ss.single_score(truth, guess)
            predictor.save()
            print(str(predictor) + ' predicted ' + str(est.estimate))
            print(str(predictor) + ' has scored ' + str(predictor.score))

post_save.connect(update_user_score, sender=Question)


#Estimate.objects.filter(author=predictor)

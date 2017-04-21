from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User

from ask_cherkasov.models import Question, Tag, UserData, QuestionLike, Answer, AnswerLike

from random import choice, randint

class Command(BaseCommand):
  def handle(self, *args, **options):
    users = User.objects.all()
    users.delete()
    userdata = UserData.objects.all()
    userdata.delete()
    tags = Tag.objects.all()
    tags.delete()
    questions = Question.objects.all()
    questions.delete()
    qlikes = QuestionLike.objects.all()
    qlikes.delete()
    alikes = AnswerLike.objects.all()
    alikes.delete()
    answers = Answer.objects.all()
    answers.delete()

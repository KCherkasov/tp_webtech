from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User

from ask_cherkasov.models import Question, QuestionLike, Answer, AnswerLike

from random import choice, randint

class Command(BaseCommand):
  help = 'Fills database with fake likes'
  def add_arguments(self, parser):
    parser.add_argument('--ans_likes', action = 'store', dest = 'answer_likes', default = 5, help = 'Number of likes per answer')
    parser.add_argument('--que_likes', action = 'store', dest = 'question_likes', default = 5, help = 'Number of questions per question')

  def handle(self, *args, **options):
    ans_num = int(options['answer_likes'])
    que_num = int(options['question_likes'])

    users = User.objects.all()[1:]
    questions = Question.objects.all()

    for question in questions:
      self.stdout.write('[%d] question' % (question.id))
      for i in range(0, que_num):
        QuestionLike.objects.add_or_update(author = choice(users), question = question, value = choice([-1, 1]))
    
    answers = Answer.objects.all()

    for answer in answers:
      self.stdout.write('[%d] answer' % (answer.id))
      for i in range(0, ans_num):
        AnswerLike.objects.add_or_update(author = choice(users), answer = answer, value = choice([-1, 1]))
